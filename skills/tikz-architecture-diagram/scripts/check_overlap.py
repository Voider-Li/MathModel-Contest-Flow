#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 文字重叠 / 越界 核验脚本

用法:python check_overlap.py figure.pdf

检测:
  1. 任意两文本片段的边界矩形相交面积 > 0,报为重叠
  2. 文本片段的边界超出页面裁切框,报为越界

依赖:pdfplumber
"""
import sys

try:
    import pdfplumber
except ImportError:
    print("[ERR] 需要 pip install pdfplumber", file=sys.stderr)
    sys.exit(2)


def rects_overlap(a, b):
    """两 dict(x0,top,x1,bottom) 是否重叠,带 0.5pt 容差"""
    return not (a["x1"] <= b["x0"] + 0.5 or
                b["x1"] <= a["x0"] + 0.5 or
                a["bottom"] <= b["top"] + 0.5 or
                b["bottom"] <= a["top"] + 0.5)


def main(path):
    n_overlap = 0
    n_oob = 0
    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages, 1):
            words = page.extract_words()
            for w in words:
                if w["x0"] < 0 or w["top"] < 0 or \
                   w["x1"] > page.width + 0.5 or w["bottom"] > page.height + 0.5:
                    print(f"  page {pi}: OOB text '{w['text']}' "
                          f"@ ({w['x0']:.1f},{w['top']:.1f})-"
                          f"({w['x1']:.1f},{w['bottom']:.1f})")
                    n_oob += 1
            for i, a in enumerate(words):
                for b in words[i + 1:]:
                    if rects_overlap(a, b):
                        print(f"  page {pi}: overlap '{a['text']}' <-> "
                              f"'{b['text']}'")
                        n_overlap += 1
    print(f"[summary] {path}: overlap={n_overlap}  oob={n_oob}")
    if n_overlap or n_oob:
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: check_overlap.py figure.pdf", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))