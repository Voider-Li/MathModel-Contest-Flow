# cumcmthesis.cls（离线兜底副本）

本文件夹随 math-modeling-pro 一并提供 **cumcmthesis 文档类** 的离线副本，供论文阶段 0/5 获取后放到论文工作目录编译。

## 来源
- 文件：`cumcmthesis.cls`
- 版本：`v2.9`，日期 `2026/08/26`（取自 `\ProvidesClass` 声明）
- 性质：全国大学生数学建模竞赛（CUMCM）官方 LaTeX 模板，随 CTeX 宏集发布；类文件内部仅 `\RequirePackage` 标准宏包（ctex / geometry / amsmath / graphicx / float / booktabs …），**自包含、无额外本地同伴文件**，用 `xelatex` 编译。

## 用法（关键）
xelatex 要求 `cumcmthesis.cls` 在 `main.tex` 同目录（或在 `TEXINPUTS` 搜索路径）内。skill 里的副本**不会被自动加载**，必须显式复制：

```bash
# 阶段 0：本机没装时才复制（装了则优先用系统版）
kpsewhich cumcmthesis.cls || cp templates/cumcmthesis/cumcmthesis.cls 05_paper/

# 阶段 5：编译
cd 05_paper && xelatex main.tex
```

## 许可与再分发
- 本副本为官方模板的再分发，用于离线兜底；保留其原始 `\ProvidesClass` 版本与作者声明，**不修改、不据为己有、不闭源**。
- 若官方发布新版本（版本号/日期更大），以官方新版本为准，可替换本副本。
- 不捆绑任何赛事专属承诺书/编号页内容；`withoutpreface,bwprint` 选项即对应"电子版提交、去封面与编号页"。

## 注意
- 仅放 `.cls` 即可，无需 `.cfg` / `.bst` 等同伴文件（该类未依赖）。
- 版本漂移风险：本机若已通过 `tlmgr`/CTeX 装有更新版，请以系统版优先，避免两份并存导致歧义。
