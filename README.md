# Math Modeling Pro（数学建模竞赛全流程强化版 Skill）

[![Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](https://github.com/) [![LaTeX](https://img.shields.io/badge/LaTeX-cumcmthesis-green)](templates/cumcmthesis/) [![Python](https://img.shields.io/badge/Python-%E2%89%A53.10-blue)](scripts/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个面向**数学建模竞赛**（国赛 CUMCM / 美赛 MCM-ICM / 校赛 / 企业赛 / 研究生赛等，不限定特定赛事）的**自包含 Agent Skill**：把从「读题拆解」到「论文交付」的完整流程标准化为 11 个阶段，并内置 **8 条硬门禁**。每条规则都来自真实竞赛与真实工程中被评审纠正过的教训，可直接加载到 Claude Code / Codex / WorkBuddy 等 agentic 编码工具中使用。

本 skill 由两套来源融合而成：一套**自包含全流程能力包**（读题→建模→求解→可视化→写作→审稿，含模板/脚本/子技能），一套**门控式工作流**（强制基线对比、独立数据挖掘、独立测试集、文献核验、数值冻结）。融合后保留了前者的全部可执行细节与资源，补齐了后者的方法论硬约束，且**不依赖任何外部技能**。

## ✨ 核心特性

- **读题拆解**：赛题文件多模态解析、附件数据结构探查、按 Q1..Qn 拆题并判定问题类型
- **独立数据挖掘章**：强制独立成章，覆盖字段字典 / 缺失离群 / 分布 / 相关共线 / 分组差异 / 时序轨迹 / 特征工程与防泄漏七项，结论必须指向建模选择
- **方案选择**：大道至简偏好序（机理模型优先）、每问 2–3 个差异化候选 + 一个真实可比基线
- **代码实现**：防伪数据红线、绝对路径读真实文件、Search-Replace 增量纠错、可复现清单、**数值冻结**
- **独立检验**：按独立单元划分训练/验证/测试，最终指标只来自**独立测试集**；数据泄露六条自查、失败样本分析
- **可视化**：nature / science / IEEE 三套学术配色、八大绘图类型选择指南、宋体 + Times、TikZ 蛇形流程图、论文总体架构图
- **文献门**：先建库再写作，字段完整、DOI 可解析、键值引用、交稿前逐条核验
- **论文写作**：cumcmthesis 模板（离线 cls 自带）、摘要约 80% 版心、每问 ≥10 处公式推导、图表排版硬规范、正文 21–30 页
- **审稿修改**：九维评审 + 八门禁复检、三级问题清单、版面逐页视觉审查、图片乱码三道关、修复循环
- **自动化体检**：`check_gates.py`（工程结构/门禁）+ `check_layout.py`（版面六项），交付前一键扫描
- **降 AI 味**：论文读起来像资深参赛者手写，反模式清单见 `references/writing.md` §5

## 🚪 八条硬门禁

| # | 门禁 | 等级 | 一句话要求 |
|---|---|---|---|
| G1 | 基线对比 | 一致性级 | 每问一张"基线 vs 主方法 vs 备选"表，基线真实可比 |
| G2 | 独立数据挖掘 | 缺失整章→红线级 | 独立成章，七项内容齐全，结论指向建模 |
| G3 | 独立测试集 | **红线级** | 最终指标只来自独立测试集，按独立单元划分 |
| G4 | 数据泄露 | **红线级** | 时序只用过去、特征不用事后信息、只在训练集 fit |
| G5 | 文献 | 编造→红线级 | 先建库、字段完整、DOI 可解析、键值引用 |
| G6 | 数值冻结 | **红线级** | 正文数字全部来自冻结结果文件 |
| G7 | 代码可复现 | 一致性级 | 种子/依赖/路径固定，附录代码=交付代码 |
| G8 | 版面 | 页数超限→红线级 | 图表就近、说明 100–150 字、占比 ≤2/3、21–30 页、无乱码 |

## 📁 目录结构

```
math-modeling-pro/
├── SKILL.md                          # Skill 主入口：核心理念 + 八门禁 + 11 阶段工作流
├── references/
│   ├── parsing.md                    # 读题协议、数据探查、拆题 JSON
│   ├── data-mining.md                # 【新增】独立数据挖掘章七项、EDA 脚本骨架
│   ├── modeling.md                   # 大道至简偏好序、候选方案、基线对比门、优化模型完整形式
│   ├── coding.md                     # 防伪数据红线、Search-Replace 纠错、数值冻结门
│   ├── validation.md                 # 【新增】独立测试集门、数据泄露自查、模型检验章七项
│   ├── literature.md                 # 【新增】文献门、文献库格式、检索与 DOI 核验来源
│   ├── visualization.md              # 三套配色、八大图型、TikZ 蛇形流程图、图片命名
│   ├── writing.md                    # 结构骨架（含数据挖掘章/模型检验章）、摘要规则、排版硬规范
│   └── review.md                     # 九维评审、八门禁复检、三级问题清单、版面视觉审查
├── skills/
│   └── tikz-architecture-diagram/    # 子技能：论文总体架构图（分层架构 TikZ 画法）
├── templates/
│   ├── cumcmthesis/cumcmthesis.cls   # cumcmthesis v2.9 离线副本（xelatex 编译兜底）
│   └── flow_snake.tex                # 蛇形流程图 TikZ 模板
└── scripts/
    ├── check_gates.py                # 【新增】门禁自检（工程结构 + G1–G7）
    └── check_layout.py               # 交付前版面自动体检（六项违规报行号）
```

## 🚀 快速开始

### 1. 环境依赖

- Python ≥ 3.10（`pandas`、`openpyxl`、`matplotlib`、`pdfplumber`；版面体检另需 `pymupdf`）
- TeX Live / CTeX（`xelatex` + `cumcmthesis`，仓库已带离线 cls 兜底）
- 建议 `kpsewhich cumcmthesis.cls` 检查系统是否已装，未装则把 `templates/cumcmthesis/cumcmthesis.cls` 复制到论文目录

### 2. 安装为 Agent Skill

```bash
# 个人级（全项目可用）
cp -r math-modeling-pro ~/.claude/skills/          # Claude Code
cp -r math-modeling-pro ~/.workbuddy-ai/skills/    # WorkBuddy
# 项目级（仅当前项目）
cp -r math-modeling-pro <workspace>/.workbuddy-ai/skills/
```

安装后，只要对话中出现「数学建模 / 数模 / 国赛 / 美赛 / 建模论文 / 数据挖掘 / 独立测试集 / 文献核验」等关键词，agent 即会自动加载本 skill。

### 3. 一次竞赛任务的标准推进（11 阶段）

| 阶段 | 内容 | 产物 |
|---|---|---|
| 0 环境自检 | 依赖检查、cls 就位、目录骨架 | `logs/env_check.json` |
| 1 读题拆解 | 题面解析、数据探查、拆题 | `task_package.json` |
| 2 数据挖掘 | 独立 EDA、特征工程、防泄漏标注 | `Q0_eda/eda.py` + `results/`、`data_mining_summary.md` |
| 3 方案建模 | 每问 2–3 候选 + 基线，用户点选 | `modeling_doc.json` |
| 4 代码求解 | 真实数据、防伪红线、增量纠错、数值冻结 | `Q*/solve.py` + `results/`、`frozen_metrics.csv` |
| 5 独立检验 | 独立测试集、泄露自查、稳健性 | `reports/VALIDATION_REPORT.md` |
| 6 可视化 | 架构图 1 张 + 各问流程图 + 数据图 | `figures/` |
| 7 文献库 | 检索、建库、DOI 核验 | `references/library.bib` |
| 8 论文写作 | 分章节生成 + 编译修复循环 | `main.tex` / `main.pdf` |
| 9 审稿修改 | 九维评审 + 门禁复检 + 版面体检 | `review_report.json` |
| 10 交付 | 论文 PDF + 支撑材料 zip | `06_delivery/` |

时间紧只读一个文件的话，读 `references/review.md`。

### 4. 交付前一键体检

```bash
python scripts/check_gates.py <task_dir>                    # 工程结构 + 门禁 G1–G7
python scripts/check_layout.py main.pdf --tex main.tex      # 版面六项（就近/字数/占比/图挨图/页数/乱码）
```

两个脚本退出码非 0 即需修复。

## 🧭 两类结构图，别画错

| 类型 | 数量 | 位置 | 画法 |
|---|---|---|---|
| 论文总体架构图 | 全篇 1 张 | 问题分析节末尾 | `skills/tikz-architecture-diagram`（分层架构，Okabe-Ito 配色） |
| 各问解题流程图 | 每问 1 张 | 该问模型建立开头 | `templates/flow_snake.tex`（蛇形横向，现代柔和 6 色） |

两类图画风不混用。

## 🔀 与来源 skill 的关系

| | 来源 A（全流程能力包） | 来源 B（门控工作流） | **本 skill（融合）** |
|---|---|---|---|
| 自包含 | ✅ | ❌ 依赖外部技能 | ✅ |
| 模板/脚本/子技能 | ✅ | ❌ | ✅ |
| 版面自动机检 | ✅ | ❌ | ✅ |
| 独立测试集门 | ✖ | ✅ | ✅ |
| 独立数据挖掘章 | ✖ | ✅ | ✅ |
| 文献管理门 | ✖ | ✅ | ✅ |
| 数值冻结 / 决策留痕 | ✖ | ✅ | ✅ |

融合原则：**能力与资源全部来自 A，方法论硬门禁来自 B，二者互不削弱**。A 的写作/可视化细节与自动化脚本原样保留，B 的门禁改写为 A 的 reference 章节与检查项。

## 📜 许可证

[MIT](LICENSE)。其中 `templates/cumcmthesis/cumcmthesis.cls` 为 [cumcmthesis](https://github.com/latexstudio/CUMCMThesis)（LaTeX Studio）官方类文件的离线副本，遵循其原有许可证，此处仅作离线兜底，以系统安装版本优先。

## ⚠️ 免责声明

本仓库是竞赛方法论的标准化沉淀，仅供学习与研究使用。使用 AI 辅助参赛时请遵守目标赛事的官方规则（部分赛事要求披露 AI 工具使用情况）。
