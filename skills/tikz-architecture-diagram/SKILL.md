---
name: tikz-architecture-diagram
description: 学术顶刊风格的系统/平台层级架构图绘制——用 TikZ + xelatex 把「自下而上的 N 层架构」画成期刊级矢量插图(层带 + 左侧层标块 + 白色组件盒 + 层间数据流箭头),并附构建管线、文字防遮盖核验、论文嵌入全流程。只要用户提到画架构图/系统架构/平台框架/分层架构/技术栈分层图/总体框架图/论文总体架构图/顶刊风格插图/五层架构/机理图,都应使用本 skill,即使没明说"架构"。
---

# TikZ 学术架构图绘制

把"系统自下而上分为 N 层、每层若干模块"这类内容画成学术顶刊风格的矢量架构图。核心是**绝对坐标**布局:层带、层标块、组件盒、箭头全部用 cm 坐标先算好再写,天然杜绝部件互相遮盖;字体按 中文宋体 + 西文 Times 风格,配色用 Okabe-Ito 低饱和分层用色。

本 skill 是 `mathmodel-contest-flow` 的捆绑子 skill,也可独立取出使用(把本目录整体复制到 `~/.claude/skills/tikz-architecture-diagram/` 或 `~/.workbuddy/skills/` 下即可被单独识别)。

## 在数学建模论文中的职责边界(重要,别画错图)

数模论文里有两类结构图,**分工严格,不要混用**:

| 图 | 数量 | 位置 | 用什么画 |
|---|---|---|---|
| **论文总体架构图** | 全文 1 张 | **问题分析节**(第 4 节)末尾 | **本 skill**(分层架构:数据层→模型层→求解层→结果层→结论层) |
| 各小问求解流程图 | 每问 1 张 | 每问"模型建立与求解"开头 | `mathmodel-contest-flow/references/visualization.md` 第 5.1.1 节的**蛇形(横向)TikZ 流程图模板**(现代柔和 6 色) |

判据:**表达"全文如何分层组织、各问如何归位"的用本 skill;表达"某一问从输入到输出怎么一步步算"的用原流程图模板。** 总体架构图承载"这篇论文的骨架",放在问题分析节收尾,让评委在读正文前先看懂全局;小问流程图承载"这一问的算法链路",不要用分层架构的形式去画,也不要把总体架构图复制成多张充当流程图。

## 何时用 / 触发点

- 用户要求"架构图 / 系统架构 / 平台框架 / 分层架构 / 技术栈分层 / 总体框架 / 论文总体架构图 / 顶刊风格插图",内容呈现为若干层、每层若干功能模块。
- 用户给的是一段分层描述(如"自下而上分为五层:数据接入层……数据层……应用层"),要转成一张图。
- 数模论文写到"问题分析"节,需要一张统领全文的总体架构图。

不适用:数据图表(交给 matplotlib,见 `visualization.md`)、纯步骤流程图(交给 `visualization.md` 第 5.1.1 节的蛇形(横向)TikZ 流程图模板)。

## 工作流

1. **拆层次**:从描述中分出层(自下而上),每层的模块、方法、产出。把每层压缩成"层名 + 4~8 字职能副题 + 若干组件名"。忠实原文,方法括号(如"评分模型")放进组件副题。数模场景的典型五层:数据与题面层 → 模型构建层 → 算法求解层 → 结果输出层 → 结论与推广层。
2. **定画布**:先抄 `templates/fig.tex` 的结构再改内容;画布固定 17.2 × 13.8 cm(期刊整幅友好,宽 > 高)。组件多就调盒宽盒数,别压缩字号硬塞。
3. **写代码**:照"设计配方"节布局;层内组件数按内容增减(见"增减组件盒")。
4. **构建**:跑 `templates/build.sh`(xelatex → PDF/PNG/SVG)。
5. **核验**:查 log 无 `Missing character`(= 中文豆腐块,出现必须修);跑 `scripts/check_overlap.py` 确认文字零重叠零越界;核对每个标签居中落盒。
6. **嵌入论文**:PDF 矢量嵌入 LaTeX(见"交付"节),配 100–150 字长说明 caption。

## 设计配方

### 字体(中文宋体 + 西文 Times 风格,跨平台自动回退)

```latex
\usepackage[fontset=none]{ctex}
\IfFontExistsTF{SimSun}{\setCJKmainfont{SimSun}}{%              % Windows
  \IfFontExistsTF{Songti SC}{\setCJKmainfont{Songti SC}}{%      % macOS
    \IfFontExistsTF{Noto Serif CJK SC}{\setCJKmainfont{Noto Serif CJK SC}}{%  % Linux
      \setCJKmainfont{FandolSong-Regular}[Extension=.otf]}}}    % TeX Live 自带兜底
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{%
  \IfFontExistsTF{Liberation Serif}{\setmainfont{Liberation Serif}}{%
    \IfFontExistsTF{TeX Gyre Termes}{\setmainfont{TeX Gyre Termes}}{}}}
```

**不要硬写单一字体名**(如只写 `Noto Serif CJK SC`),换机器就是满屏豆腐块。`\IfFontExistsTF` 由 fontspec 提供,ctex 已自动加载。

字号:层名 `\small` 加粗、职能副题 `\footnotesize` 灰、组件标题 `\footnotesize` 加粗、组件副题 `\scriptsize` 灰。西文缩写(POS/ERP/LLM/ETL)与数字用主字体,混排基线差异是正常的。

### 配色(Okabe-Ito 低饱和分层用色,克制)

N 层按 **冷→暖** 逐层取 Okabe 色:天蓝 `#56B4E9` → 蓝 `#0072B2` → 青绿 `#009E73` → 琥珀 `#E69F00` → 洋红 `#CC79A7`(五层以上循环到灰色系)。一个创新亮点(如全问共享的统一符号体系、LLM 助手)用朱红 `#D55E00` 强调块,**全图只允许一处**。

```latex
\definecolor{cL1}{HTML}{56B4E9}   % 层带色,按需 cL2..cL5
\tikzset{
  band/.style  ={rounded corners=3pt, line width=0.5pt, draw=#1!45, fill=#1!7},
  head/.style  ={rounded corners=2pt, line width=0.5pt, draw=#1!60, fill=#1!15},
  box/.style   ={rounded corners=2pt, line width=0.5pt, draw=black!25, fill=white},
  boxacc/.style={rounded corners=2pt, line width=0.6pt, draw=#1!70, fill=#1!14},
  fwd/.style   ={-{Stealth[length=1.8mm]}, line width=0.6pt, draw=black!35},
  up/.style    ={-{Stealth[length=2.2mm]}, line width=0.7pt, draw=black!50},
}
```

原则:色带只做低饱和淡底(7%),组件一律白盒灰边,颜色信息由层带与层标块承载——多色但整体克制。

**与论文正文配色的关系**:架构图用 Okabe-Ito 分层色,与正文数据图选定的 nature/science/IEEE 配色**不冲突**(架构图是结构示意,不是数据图)。但若论文整体选了 IEEE 风格,可把层带色替换为 IEEE 系的深蓝→浅蓝渐层,保持气质统一。

### 布局坐标(核心,先算好再写)

画布 17.2 × 13.8 cm,自下而上排层带:

- 层带高:普通层 2.2 cm,内容多的核心层 3.0~3.6;层与层之间留 **0.4 cm 空隙**(放数据流箭头)。
- 左侧层标块 `x∈[0.2,3.1]`(中心 1.65)、高 1.5,垂直居中于所在层带;块内层名 + 职能副题。
- 内容区 `x∈[3.4,17.0]`(宽 13.6,中心 10.2)。
- 一行 n 个组件盒:`盒宽 w=(13.6-(n-1)×gap)/n`,gap 取 0.16(芯片)~ 0.40(大盒);盒高 1.1~1.5,垂直居中。中心 `x_i = 3.4 + w/2 + (i-1)(w+gap)`。
  - n=4, gap=0.30 → w=3.175,中心 4.99 / 8.46 / 11.94 / 15.41
  - n=3, gap=0.40 → w=4.267,中心 5.53 / 10.20 / 14.87
- 层间箭头:每段空隙正中 `x=10.2` 画一个向上 Stealth 箭头,表数据自下而上流动。

模板 `templates/fig.tex` 里的五层 y 坐标(已验证 17.2×13.8 精确闭合):

```
L1 0.25–2.45 | L2 2.85–5.85(核心层加高) | L3 6.25–8.45 | L4 8.85–11.05 | L5 11.45–13.55
```

**三条铁律(防遮盖/防错落/防编译崩):**

1. **先画色带与底色块,再画文字节点**——TikZ 按书写顺序叠放,顺序反了文字会被色块盖住。模板把 5 条 `\layerband` 集中写在最前面就是为此。
2. **同一行组件盒的标题基线必须一致**:带副题的盒,标题放 `yc+0.28`、副题放 `yc-0.30`;没有副题的盒也把标题放在同样的 `yc+0.28`,不要"内容整体居中"——否则同一行里标题高低错落。
3. **`text width` 是 TeX 长度,不是 PGF 表达式**。要按盒宽自适应文本宽度必须用 `\dimexpr`:
   ```latex
   text width=\dimexpr#4cm-0.3cm\relax     % 正确
   text width={#4-0.3}cm                    % 报错 Unknown operator `cm'
   ```
   写错的征兆:log 里冒出 `Package PGF Math Error: Unknown operator` 且伴随大量 6.5pt 级 Overfull(文字被挤成单字换行)。

### 增减组件盒

- 一行放不下:把盒换小(芯片式 1.7~1.9 宽)或分行放。别为了塞下而压字号。
- 层内要表达流水线(如 参数估计→优化求解→仿真推演→稳健性检验):一行盒 + 盒间小 `fwd` 箭头(上一盒右边缘 `x_i+w/2` → 下一盒左边缘 `x_{i+1}-w/2`),末端结果盒用 `boxacc` 强调。
- 要点亮某模块:`boxacc` 强调块(如"统一符号体系与假设集"做成通栏长盒放核心层下方)。
- 核心层放两行:上行 4 盒(`yc=4.75`, h=1.35)+ 下行通栏强调条(`yc=3.40`, h=0.80),band 需加高到 3.0。

## 构建(templates/build.sh)

```bash
xelatex -interaction=nonstopmode -halt-on-error fig.tex
pdftoppm -png -r 300 -singlefile fig.pdf fig     # 300 dpi PNG
pdftocairo -svg fig.pdf fig.svg                   # 矢量 SVG
```

脚本输出 PNG(预览)+ PDF/SVG(矢量,嵌入 LaTeX 用)。**构建后必须检查 log**:出现 `Missing character` 就是中文渲染成了空心方块,属于失败,修字体后重渲,不能交付。`build.sh` 已内置该检测并以 exit 2 报错。

## 质量门禁(交付前逐项过)

- [ ] log 无 `Missing character` / 无 `PGF Math Error`
- [ ] log 无 Overfull(文字被挤压换行的征兆)
- [ ] `python scripts/check_overlap.py fig.pdf` 输出 `overlap=0  oob=0`
- [ ] `pdfinfo fig.pdf` 页面尺寸为 487.6 × 391.2 pt(= 17.2 × 13.8 cm),且仅 1 页
- [ ] 每个层名、组件标签都能在 `pdftotext fig.pdf -` 里找到,且位置落回对应盒
- [ ] 配色仅用上面定义的低饱和色;白盒灰边;朱红强调块全图仅一处
- [ ] 层数 ≤ 6、单层组件 ≤ 5(再多就是信息过载,应合并同类项)

## 交付:嵌入数模论文

总体架构图放**问题分析节末尾**,矢量 PDF 嵌入(不用 PNG,避免打印发虚):

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{figures/总体架构图_五层建模框架.pdf}
  \caption{本文总体建模架构。全文自下而上分五层组织:数据与题面层完成赛题
  拆解与附件数据清洗,得到统一口径的建模输入;模型构建层针对四个子问题分别
  建立幂律回归、整数规划、排队论仿真与多目标优化模型,四问共享同一套符号体系
  与假设集以保证前后一致;算法求解层按参数估计、优化求解、仿真推演、稳健性检验
  的顺序实现数值计算;结果输出层给出关键指标、调度方案与敏感性区间;结论与推广
  层完成模型评价与场景外延。层间箭头表示数据自下而上的单向流动。}
  \label{fig:arch}
\end{figure}
```

要点:

- 用 `[H]`(需 `\usepackage{float}`)固定就近,防止架构图漂到别的节去——它必须留在问题分析节。
- caption 写 **100–150 字**长说明(逐层交代职能 + 层间关系),不写"图1 总体架构图"这种光秃标题。详见 `mathmodel-contest-flow/references/writing.md` 图表说明文字规范。
- 文件名按详细命名规范:`总体架构图_五层建模框架.pdf`,不用 `arch.pdf`。
- 正文必须有一句 `\ref{fig:arch}` 引用并点出分层逻辑,不让图自说自话。
- 图宽 `0.95\textwidth`;因画布宽 > 高,占版面高度约 0.76 倍宽度,配 100–150 字 caption 后单页图表占比仍在 2/3 红线内(见 `writing.md` 单页图表占比规范)。

## 资源

- `templates/fig.tex` —— 可编译的五层架构模板(数模总体架构图示例),坐标带注释,改标签即用
- `templates/build.sh` —— 构建脚本(PDF/PNG/SVG + 豆腐块检测)
- `scripts/check_overlap.py` —— PDF 文字重叠/越界核验脚本