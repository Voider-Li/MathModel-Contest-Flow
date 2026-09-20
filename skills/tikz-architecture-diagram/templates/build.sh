#!/usr/bin/env bash
# ============================================================================
# 架构图构建脚本:xelatex -> PDF/PNG/SVG
# 用法:在 templates/ 目录下跑 bash build.sh
# 产物:fig.pdf(矢量嵌入用) / fig.png(主图,300 dpi) / fig.svg(矢量可选)
# ============================================================================
set -e
cd "$(dirname "$0")"
NAME=fig

xelatex -interaction=nonstopmode -halt-on-error ${NAME}.tex >/dev/null
# 二次编译(若 \ref 引用 TikZ 资源)
xelatex -interaction=nonstopmode -halt-on-error ${NAME}.tex >/dev/null

if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 300 -singlefile ${NAME}.pdf ${NAME}
fi
if command -v pdftocairo >/dev/null 2>&1; then
  pdftocairo -svg ${NAME}.pdf ${NAME}.svg
fi

echo "[ok] built: ${NAME}.pdf (+ .png/.svg if available)"

# 字体豆腐块检测:出现 Missing character 视为失败
if grep -q "Missing character" ${NAME}.log; then
  echo "[FAIL] log 含 'Missing character'(中文渲染成空心方块),必须修字体后重渲"
  exit 2
fi