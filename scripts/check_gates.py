#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
门禁自检脚本(数学建模竞赛强化版 skill 交付前强制关卡)

在 `check_layout.py`(版面体检)之外,核验八条硬门禁里可自动检查的部分:
  [G2] 独立数据挖掘章:论文里是否有数据挖掘独立章 + EDA 脚本/产物
  [G1] 基线对比:是否出现"基线/对比"表或对比报告
  [G3] 独立测试集:是否出现"测试集"字样与冻结指标文件
  [G4] 数据泄露:源码里是否有"全数据 fit 标准化"等危险信号(启发式)
  [G5] 文献:文献库存在、字段完整、DOI/URL 齐全、无硬编码"文献[数字]"
  [G6] 数值冻结:results/frozen_metrics.csv 是否存在
  [G7] 代码可复现:每问 solve.py 是否存在、是否读真实数据(绝对路径)
  [G8] 版面:委托给 check_layout.py(本脚本仅提示)

用法:
  python check_gates.py <task_dir>
  python check_gates.py <task_dir> --tex 05_paper/main.tex

退出码:0 全部通过 / 1 存在违规 / 2 用法错误
依赖:仅标准库(版面体检另需 pymupdf,由 check_layout.py 负责)
"""
import argparse
import json
import re
import sys
from pathlib import Path

PASS, FAIL, WARN, SKIP = "PASS", "FAIL", "WARN", "SKIP"
results = []   # (gate, level, message)


def add(gate, level, msg):
    results.append((gate, level, msg))


def find_tex(task: Path):
    cands = list(task.glob("**/main.tex")) + list(task.glob("**/*.tex"))
    # 优先 05_paper/main.tex
    for c in cands:
        if c.name == "main.tex":
            return c
    return cands[0] if cands else None


def read_text(p: Path):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def check_structure(task: Path):
    expect = ["02_data", "04_solving", "05_paper"]
    miss = [d for d in expect if not (task / d).exists()]
    if miss:
        add("STRUCT", WARN, f"缺少约定目录:{', '.join(miss)}(按 SKILL.md 目录结构应存在)")
    else:
        add("STRUCT", PASS, "目录结构齐全(02_data / 04_solving / 05_paper)")


def check_data_mining(task: Path, tex_text: str):
    eda = list(task.glob("04_solving/**/eda*.py")) + list(task.glob("**/Q0_eda/*.py"))
    has_eda = bool(eda)
    has_chap = bool(re.search(r"数据挖掘|数据预处理", tex_text))
    if has_eda and has_chap:
        add("G2", PASS, f"数据挖掘章 + EDA 脚本齐全({eda[0].name if eda else ''})")
    elif has_chap and not has_eda:
        add("G2", WARN, "论文有数据挖掘章,但未找到 EDA 脚本(建议补 04_solving/Q0_eda/eda.py)")
    elif has_eda and not has_chap:
        add("G2", FAIL, "有 EDA 脚本但论文缺独立数据挖掘章(门禁要求独立成章)")
    else:
        add("G2", FAIL, "既无独立数据挖掘章,也无 EDA 脚本")


def check_baseline(task: Path, tex_text: str):
    has_word = bool(re.search(r"基线|对比表|baseline", tex_text, re.I))
    has_report = bool(list(task.glob("**/COMPARISON*")) or list(task.glob("**/*comparison*")))
    if has_word or has_report:
        add("G1", PASS, "检测到基线/对比相关内容")
    else:
        add("G1", FAIL, "未检测到基线对比表或对比报告(每问需一张基线对比表)")


def check_testset(task: Path, tex_text: str):
    has_word = bool(re.search(r"独立测试集|测试集|test set|hold-?out", tex_text, re.I))
    frozen = list(task.glob("**/frozen_metrics.csv"))
    if has_word and frozen:
        add("G3", PASS, f"出现测试集表述且存在冻结指标文件({frozen[0].name})")
    elif has_word:
        add("G3", WARN, "出现测试集表述,但未找到 frozen_metrics.csv(建议冻结测试集指标)")
    else:
        add("G3", FAIL, "未检测到'独立测试集'相关内容(分类/预测/回归题必须来自独立测试集)")


def check_leak(task: Path):
    hits = []
    for py in task.glob("**/*.py"):
        t = read_text(py)
        # 危险信号:对全数据 fit 标准化(常见泄露),或时序随机划分
        if re.search(r"fit_transform\([^)]*\)", t) and "train" not in py.name.lower():
            if not re.search(r"train|X_tr|X_train", t):
                hits.append(f"{py.name}: 可能对全数据 fit_transform(检查是否只在训练集 fit)")
    if hits:
        add("G4", WARN, "数据泄露启发式告警(请人工确认):" + ";".join(hits[:3]))
    else:
        add("G4", PASS, "未发现明显的全数据 fit 泄露信号(仍需按 validation.md §4 人工自查)")


def check_literature(task: Path, tex_text: str):
    libs = list(task.glob("references/*.bib")) + list(task.glob("references/*.json"))
    if not libs:
        add("G5", FAIL, "未找到文献库(references/*.bib 或 references/references.json)")
        return
    lib = libs[0]
    txt = read_text(lib)
    # 硬编码引用检查
    hard = re.findall(r"文献\s*\[\s*\d+\s*\]", tex_text)
    unverified = re.findall(r'"?verified"?\s*[:=]\s*(?:false|"false")', txt, re.I)
    missing_doi = len(re.findall(r"@\w+\{", txt)) - len(re.findall(r"(?i)doi\s*=", txt)) if lib.suffix == ".bib" else 0
    problems = []
    if hard:
        problems.append(f"正文出现硬编码引用 {len(hard)} 处(应改用 \\cite{{key}})")
    if unverified:
        problems.append(f"文献库有 {len(unverified)} 条 verified=false(不得进入正文)")
    if lib.suffix == ".bib" and missing_doi > 0:
        problems.append(f"约 {missing_doi} 条文献缺 DOI 字段")
    if problems:
        add("G5", FAIL, f"文献核验问题:{';'.join(problems)}")
    else:
        add("G5", PASS, f"文献库 {lib.name} 通过基本核验")


def check_freeze(task: Path):
    frozen = list(task.glob("**/frozen_metrics.csv"))
    if frozen:
        add("G6", PASS, f"数值冻结文件存在({frozen[0].relative_to(task)})")
    else:
        add("G6", FAIL, "未找到 results/frozen_metrics.csv(正文数字必须可溯源到冻结结果)")


def check_repro(task: Path):
    solves = list(task.glob("04_solving/**/solve*.py"))
    if not solves:
        add("G7", FAIL, "未找到求解脚本 04_solving/**/solve*.py")
        return
    no_data = []
    for s in solves:
        t = read_text(s)
        if not re.search(r"read_excel|read_csv|openpyxl|np\.load|loadtxt", t):
            no_data.append(s.name)
    if no_data:
        add("G7", WARN, f"以下求解脚本未见读真实数据调用:{', '.join(no_data)}")
    else:
        add("G7", PASS, f"找到 {len(solves)} 个求解脚本且均读真实数据")


def main():
    ap = argparse.ArgumentParser(description="数模竞赛强化版 skill 门禁自检")
    ap.add_argument("task_dir", help="任务根目录")
    ap.add_argument("--tex", help="显式指定论文 .tex(默认自动搜索 main.tex)")
    args = ap.parse_args()

    task = Path(args.task_dir).resolve()
    if not task.is_dir():
        print(f"[ERR] 目录不存在:{task}", file=sys.stderr)
        sys.exit(2)

    tex = Path(args.tex).resolve() if args.tex else find_tex(task)
    tex_text = read_text(tex) if tex else ""
    if not tex:
        add("PAPER", WARN, "未找到论文 .tex,论文相关门禁(G1/G2/G3/G5)按缺省处理")

    check_structure(task)
    check_data_mining(task, tex_text)
    check_baseline(task, tex_text)
    check_testset(task, tex_text)
    check_leak(task)
    check_literature(task, tex_text)
    check_freeze(task)
    check_repro(task)
    add("G8", SKIP, "版面门禁请另跑:python scripts/check_layout.py main.pdf --tex main.tex")

    # 输出
    width = max(len(g) for g, _, _ in results) + 2
    print(f"\n门禁自检报告:{task}\n" + "=" * 60)
    fails = 0
    for gate, level, msg in results:
        print(f"[{gate:<{width}}] {level:<4} {msg}")
        if level == FAIL:
            fails += 1
    print("=" * 60)
    print(f"结果:{'全部通过 ✅' if fails == 0 else f'{fails} 项未通过 ❌(进入修复循环)'}")
    print("说明:G4 为启发式告警,G8 由 check_layout.py 负责,均需人工复核。\n")
    sys.exit(0 if fails == 0 else 1)


if __name__ == "__main__":
    main()
