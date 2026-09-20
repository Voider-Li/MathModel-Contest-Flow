#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
论文版面体检脚本(数学建模论文交付前强制关卡)

一次性检测六类版面硬约束:
  1. 图表就近:图/表与正文首次引用是否同页或相邻页(LaTeX 浮动体会漂移)
  2. 说明文字:图题/表题字数是否落在 100-150 字区间
  3. 单页图表占比:单页图表视觉占位是否 <= 2/3 版心
  4. 图挨图:是否存在两图直接相邻、中间无正文段落(视觉上整页全是图)
  5. 正文页数:正文(不含附录)是否在 21-30 页,且硬性不超 30 页
  6. 乱码/缺字:全篇是否出现替换符(U+FFFD)或空心方块(U+25A1/25A0)

用法:
  python check_layout.py main.pdf                    # 自动找同目录同名 .tex
  python check_layout.py main.pdf --tex main.tex     # 显式指定源码
  python check_layout.py main.pdf --body-end 28      # 手动指定正文末页
  python check_layout.py main.pdf --max-ratio 0.667 --cap-min 100 --cap-max 150

说明:
  字数统计以 .tex 源码里的 \\caption{} 为准(精确,且能报出源码行号);
  找不到 .tex 时退化为从 PDF 提取,但 PDF 逐行成块,长 caption 只能量到首行,
  此时字数仅供参考,应补 --tex 参数。

依赖:PyMuPDF(pip install pymupdf)

退出码:0 全部通过 / 1 存在违规(须进修复循环)
"""
import argparse
import os
import re
import sys
from collections import Counter

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        print("[ERR] 需要 pip install pymupdf", file=sys.stderr)
        sys.exit(2)

# 图题/表题起始:兼容 "图1"、"图 1"、"图1:"、"表 3 xxx"
CAP_RE = re.compile(r"^\s*(图|表)\s*(\d+)\s*[:：.、]?\s*(.*)$", re.S)
# 正文引用:如"如图3所示"、"见表2"
REF_RE = re.compile(r"(图|表)\s*(\d+)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
# 连续的数字/字母串(每串计 1 字,贴近中文字数统计习惯)
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[.,][0-9]+)*")
# 乱码/缺字征兆:替换符、空心方块
GARBLE_RE = re.compile(r"[\ufffd\u25a1\u25a0]")


def count_zi(text):
    """中文语境下的「字数」:汉字数 + 数字/字母串数"""
    t = re.sub(r"\\[a-zA-Z]+\s*", " ", text)      # 去 LaTeX 命令名
    t = re.sub(r"[{}$~^_\\&%#]", " ", t)          # 去 LaTeX 符号
    return len(CJK_RE.findall(t)) + len(TOKEN_RE.findall(t))


def extract_tex_captions(path):
    """从 .tex 抓 \\caption{...},花括号配平;返回 [(行号, 原文)]"""
    try:
        with open(path, encoding="utf-8") as f:
            src = f.read()
    except (OSError, UnicodeDecodeError):
        return None
    out = []
    for m in re.finditer(r"\\caption\s*(?:\[[^\]]*\])?\s*\{", src):
        i, depth, buf = m.end(), 1, []
        while i < len(src) and depth:
            c = src[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            if depth:
                buf.append(c)
            i += 1
        out.append((src.count("\n", 0, m.start()) + 1, "".join(buf).strip()))
    return out


def merge_intervals(items, gap):
    """items: [(y0, y1, payload)] -> 合并纵向相邻/重叠区间"""
    if not items:
        return []
    items = sorted(items, key=lambda t: t[0])
    out = [[items[0][0], items[0][1], [items[0][2]]]]
    for y0, y1, p in items[1:]:
        if y0 <= out[-1][1] + gap:
            out[-1][1] = max(out[-1][1], y1)
            out[-1][2].append(p)
        else:
            out.append([y0, y1, [p]])
    return out


def page_graphics(page, text_top, text_bottom):
    """该页图形元素矩形(位图 + 矢量绘制),已剔除整页底框与页眉页脚线"""
    rects = []
    W, H = page.rect.width, page.rect.height
    try:
        for info in page.get_image_info():
            rects.append(fitz.Rect(info["bbox"]))
    except Exception:
        pass
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    for d in drawings:
        r = d.get("rect")
        if r is None:
            continue
        r = fitz.Rect(r)
        if r.is_empty or r.is_infinite:
            continue
        w, h = r.width, r.height
        if w > 0.95 * W and h > 0.95 * H:            # 整页背景框
            continue
        if h < 1.5 and w > 0.6 * W and (r.y1 < text_top or r.y0 > text_bottom):
            continue                                  # 页眉页脚横线
        if w * h < 4 and h < 0.5:                     # 碎屑
            continue
        rects.append(r)
    return rects


def page_paragraphs(page):
    """按行块的纵向邻接把 PDF 文本行聚成段;返回 [(y0,y1,text,zi)]"""
    blocks = []
    try:
        raw = page.get_text("blocks")
    except Exception:
        return blocks
    lines = []
    for b in raw:
        txt = (b[4] or "").strip()
        if txt:
            lines.append((b[1], b[3], txt))
    lines.sort(key=lambda t: t[0])
    for y0, y1, txt in lines:
        h = y1 - y0
        if blocks and y0 - blocks[-1][1] <= max(0.75 * h, 8.0) \
                and not CAP_RE.match(txt):
            prev = blocks[-1]
            blocks[-1] = [prev[0], max(prev[1], y1), prev[2] + txt]
        else:
            blocks.append([y0, y1, txt])
    return [(b[0], b[1], b[2], count_zi(b[2])) for b in blocks]


def detect_body_end(doc):
    """正文末页 = 第一处作为标题出现的「附录」所在页的前一页"""
    for pno in range(len(doc)):
        for line in doc[pno].get_text("text").splitlines():
            s = line.strip()
            if re.match(r"^附\s*录", s) and len(s) < 30:
                return pno          # 0-based pno == 1-based 的前一页
    return len(doc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--tex", default="", help="论文源码 .tex(用于精确统计字数)")
    ap.add_argument("--body-end", type=int, default=0,
                    help="正文末页(1-based);默认自动探测附录起始页")
    ap.add_argument("--max-ratio", type=float, default=2.0 / 3.0)
    ap.add_argument("--cap-min", type=int, default=100)
    ap.add_argument("--cap-max", type=int, default=150)
    ap.add_argument("--min-sep-chars", type=int, default=40,
                    help="判定两图之间「有正文」所需的最少字数")
    ap.add_argument("--page-min", type=int, default=21)
    ap.add_argument("--page-max", type=int, default=30)
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    npages = len(doc)
    body_end = args.body_end or detect_body_end(doc)

    tex = args.tex
    if not tex:
        cand = os.path.splitext(args.pdf)[0] + ".tex"
        if os.path.exists(cand):
            tex = cand
        else:
            cand = os.path.join(os.path.dirname(os.path.abspath(args.pdf)),
                                "main.tex")
            tex = cand if os.path.exists(cand) else ""
    tex_caps = extract_tex_captions(tex) if tex else None

    # 版心范围(排除页眉页脚)
    tops, bots = [], []
    for p in doc:
        for b in p.get_text("blocks"):
            tops.append(b[1])
            bots.append(b[3])
    text_top = min(tops) if tops else 0.0
    text_bottom = max(bots) if bots else doc[0].rect.height

    violations = []

    print("=" * 74)
    print(f"版面体检:{args.pdf}")
    print(f"总页数 {npages};正文末页判定为第 {body_end} 页"
          f"({'手动指定' if args.body_end else '自动探测附录位置'})")
    print(f"字数依据:{tex if tex_caps else 'PDF 提取(建议补 --tex 以精确统计)'}")
    print("=" * 74)

    # ---------- 全篇扫描:图表说明所在页 / 正文首次引用所在页 ----------
    cap_pages, ref_pages, pdf_caps = {}, {}, []
    for pno in range(npages):
        for (y0, y1, txt, zi) in page_paragraphs(doc[pno]):
            m = CAP_RE.match(txt)
            if m:
                key = (m.group(1), int(m.group(2)))
                cap_pages.setdefault(key, pno + 1)
                pdf_caps.append((pno + 1, f"{key[0]}{key[1]}", zi,
                                 m.group(3)[:26]))
            else:
                for r in REF_RE.finditer(txt):
                    ref_pages.setdefault((r.group(1), int(r.group(2))),
                                         pno + 1)

    # ---------- [1] 单页图表占比 与 图挨图(仅正文页) ----------
    print("\n[1] 单页图表占比 与 图挨图")
    hit1 = False
    band_h = max(text_bottom - text_top, 1.0)
    for pno in range(min(body_end, npages)):
        page, pg = doc[pno], pno + 1
        grects = page_graphics(page, text_top, text_bottom)
        if not grects:
            continue
        gbands = merge_intervals([(r.y0, r.y1, r) for r in grects], gap=14)
        paras = page_paragraphs(page)
        body = [p for p in paras if not CAP_RE.match(p[2])]

        occupied = sum(b[1] - b[0] for b in gbands)
        ratio = occupied / band_h
        if ratio > args.max_ratio:
            msg = (f"page {pg}: 图表视觉占位 {ratio*100:.0f}% > "
                   f"{args.max_ratio*100:.0f}%(图形带 {len(gbands)} 段,"
                   f"{occupied:.0f}pt / 版心 {band_h:.0f}pt)")
            print("  " + msg)
            violations.append(("图表占比超限", msg))
            hit1 = True

        for i in range(len(gbands) - 1):
            y_lo, y_hi = gbands[i][1], gbands[i + 1][0]
            sep = sum(zi for (by0, by1, t, zi) in body
                      if by0 >= y_lo - 2 and by1 <= y_hi + 2)
            if sep < args.min_sep_chars:
                msg = (f"page {pg}: 图挨图——两图形带之间仅 {sep} 字正文"
                       f"(阈值 {args.min_sep_chars}),y {y_lo:.0f}→{y_hi:.0f}")
                print("  " + msg)
                violations.append(("图挨图", msg))
                hit1 = True
    if not hit1:
        print("  OK:无单页图表超限,无图挨图")

    # ---------- [2] 说明文字字数 ----------
    print(f"\n[2] 图表说明文字字数({args.cap_min}-{args.cap_max} 字)")
    if tex_caps is not None:
        items = [(f"{tex}:{ln}", count_zi(t), t.replace("\n", " ")[:26])
                 for ln, t in tex_caps]
    else:
        items = [(f"page {pg} {key}", zi, head) for pg, key, zi, head in pdf_caps]
    bad = [it for it in items if not (args.cap_min <= it[1] <= args.cap_max)]
    for where, zi, head in bad:
        flag = "过短" if zi < args.cap_min else "过长"
        print(f"  {where}: {zi} 字({flag}) — {head}…")
        violations.append(("说明文字字数", f"{where}: {zi} 字({flag})"))
    if items and not bad:
        print(f"  OK:{len(items)} 条说明全部落在区间内")
    if not items:
        print("  WARN:未识别到任何图题/表题")

    # ---------- [3] 图表就近 ----------
    print("\n[3] 图表就近(与正文首次引用同页或相邻页)")
    far = []
    for key, cp in sorted(cap_pages.items()):
        rp = ref_pages.get(key)
        if rp is None:
            far.append((key, cp, None, "正文无引用(孤儿图表)"))
        elif abs(cp - rp) > 1:
            far.append((key, cp, rp, f"相隔 {abs(cp-rp)} 页"))
        elif cp < rp:
            far.append((key, cp, rp, "图表出现在引用之前"))
    for key, cp, rp, why in far:
        msg = (f"{key[0]}{key[1]}: 说明在第 {cp} 页,首次引用在第 "
               f"{rp if rp else '—'} 页 — {why}")
        print("  " + msg)
        violations.append(("图表就近", msg))
    if cap_pages and not far:
        print(f"  OK:{len(cap_pages)} 个图表均与首次引用同页或相邻页")

    # ---------- [4] 乱码 ----------
    print("\n[4] 乱码/缺字")
    hit4 = False
    for pno in range(npages):
        hits = GARBLE_RE.findall(doc[pno].get_text("text"))
        if hits:
            msg = f"page {pno+1}: 检出 {len(hits)} 个替换符/空心方块"
            print("  " + msg)
            violations.append(("乱码", msg))
            hit4 = True
    if not hit4:
        print("  OK:未检出替换符或空心方块")

    # ---------- [5] 正文页数 ----------
    print(f"\n[5] 正文页数(硬性 <= {args.page_max},建议 "
          f"{args.page_min}-{args.page_max})")
    print(f"  正文 {body_end} 页")
    if body_end > args.page_max:
        msg = f"正文 {body_end} 页 > 硬性上限 {args.page_max} 页,必须压缩"
        print("  " + msg)
        violations.append(("正文页数超限", msg))
    elif body_end < args.page_min:
        msg = f"正文 {body_end} 页 < 建议下限 {args.page_min} 页,内容偏薄"
        print("  " + msg)
        violations.append(("正文页数偏少", msg))
    else:
        print(f"  OK:落在 {args.page_min}-{args.page_max} 页区间")

    # ---------- 汇总 ----------
    print("\n" + "=" * 74)
    if violations:
        print("体检结论:需修复")
        for k, v in Counter(v[0] for v in violations).items():
            print(f"  - {k}: {v} 处")
        print("=" * 74)
        return 1
    print("体检结论:全部通过")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())