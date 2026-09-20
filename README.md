# Math Modeling Pro

> 一套**自包含**的数学建模竞赛 skill：把「读题 → 交付」拆成 **11 个阶段**，并用 **8 条硬门禁**卡住质量下限。
> 模板、脚本、子技能全部随包分发，克隆下来即可用，不依赖任何外部技能。

适用赛事：国赛 CUMCM、美赛 MCM / ICM、校赛、企业赛、研究生赛——不绑定特定赛事。

---

## 为什么需要它

数学建模的难点往往不在「会不会建模」，而在**下限守不住**。翻车通常发生在这些地方：

- 只有一个主方法，没有基线，结论好或坏都无从判断；
- 数据挖掘散落在各问里，看不出数据究竟告诉建模什么；
- 最终指标来自训练集，没有独立测试集，泛化能力无从谈起；
- 参考文献随手凑，评委抽查一条就露馅；
- 论文里的数字和代码跑出来的对不上。

Math Modeling Pro 的思路是：**保留完整的全流程能力**（读题 / 建模 / 求解 / 可视化 / 写作 / 审稿），同时把上面这些短板固化成**不可跳过的门禁**。门禁不通过，就不算完成。

## 八条硬门禁

| 编号 | 门禁 | 级别 | 卡的是什么 |
|:--:|---|---|---|
| G1 | 基线对比 | 一致性级 | 每问一张「基线 vs 主方法 vs 备选」表，基线必须真实可比，禁用玩具基线 |
| G2 | 独立数据挖掘 | 缺整章 → 红线 | 数据挖掘独立成章，七项齐全，结论必须指向建模选择 |
| G3 | 独立测试集 | **红线** | 分类/预测/回归的主指标只能来自独立测试集，按独立单元划分 |
| G4 | 数据泄露 | **红线** | 时序只用过去、特征不用事后信息、标准化只在训练集 fit |
| G5 | 文献核验 | 编造 → 红线 | 先建库再写作，DOI 可解析，正文全部键值引用 |
| G6 | 数值冻结 | **红线** | 正文数字全部可溯源到冻结结果文件，写作期间不改数 |
| G7 | 代码可复现 | 一致性级 | 种子 / 依赖 / 路径固定，附录代码 = 交付代码 |
| G8 | 版面 | 超页 → 红线 | 图表就近、说明 100–150 字、单页占比 ≤2/3、正文 21–30 页、无乱码 |

任一条不过 → 进入修复循环，修完重跑全清单。**不允许「先交稿再补」。**

## 工作流：11 个阶段

```
0 环境自检 → 1 读题拆解 → 2 数据挖掘 → 3 方案建模 → 4 代码求解
           → 5 独立检验 → 6 可视化 → 7 文献库 → 8 论文写作 → 9 审稿修改 → 10 交付
```

每个阶段的输入、产物、检查点写在 `SKILL.md`；详细规范分散在下面这些文档里，按阶段查即可，不必全读。

| 阶段 | 对应文档 | 里面有什么 |
|:--:|---|---|
| 1 读题拆解 | `references/parsing.md` | 多格式解析协议、图片多模态识别、数据探查脚本、拆题 JSON |
| 2 数据挖掘 | `references/data-mining.md` | 七项内容清单、EDA 脚本骨架、「发现 → 影响」结论写法 |
| 3 方案建模 | `references/modeling.md` | 大道至简偏好序、候选方案、**基线对比门**、优化模型完整形式 |
| 4 代码求解 | `references/coding.md` | 防伪数据红线、Search-Replace 增量纠错、**数值冻结** |
| 5 独立检验 | `references/validation.md` | **独立测试集门**、数据泄露自查、模型检验章七项、失败样本分析 |
| 6 可视化 | `references/visualization.md` | 三套学术配色、八大绘图类型、字体配方、TikZ 流程图、命名规范 |
| 7 文献库 | `references/literature.md` | 文献门五条约束、库格式、检索与 DOI 核验来源 |
| 8 论文写作 | `references/writing.md` | 结构骨架、各部分长度、摘要规则、图表排版硬规范、降 AI 味 |
| 9 审稿修改 | `references/review.md` | 九维评审、八门禁复检、三级问题清单、逐页视觉审查、评分表 |

> 时间紧只读一份的话，读 `references/review.md`。

## 目录结构

```
math-modeling-pro/
├── SKILL.md                      # 主入口：核心理念 + 八门禁 + 11 阶段工作流
├── references/                   # 分阶段详细规范（9 份）
│   ├── parsing.md                #   读题与拆解
│   ├── data-mining.md            #   独立数据挖掘章
│   ├── modeling.md               #   方案选择与建模（含基线门）
│   ├── coding.md                 #   代码实现与求解（含数值冻结）
│   ├── validation.md             #   独立检验与稳健性
│   ├── visualization.md          #   可视化规范
│   ├── literature.md             #   文献管理与核验
│   ├── writing.md                #   论文写作规范
│   └── review.md                 #   审稿与修改
├── scripts/
│   ├── check_gates.py            # 门禁自检：工程结构 + G1–G7
│   └── check_layout.py           # 版面体检：占比/图挨图/说明字数/就近/乱码/页数
├── skills/
│   └── tikz-architecture-diagram/ # 子技能：论文总体架构图（分层架构 TikZ）
├── templates/
│   ├── cumcmthesis/cumcmthesis.cls # 官方类文件离线副本（编译兜底）
│   └── flow_snake.tex             # 各问解题流程图（蛇形横向 TikZ）
├── README.md
└── LICENSE
```

## 安装

```bash
# 个人级：所有项目可用
git clone https://github.com/Voider-Li/MathModel-Contest-Flow.git \
  ~/.workbuddy-ai/skills/math-modeling-pro      # WorkBuddy
  # 或 ~/.claude/skills/math-modeling-pro        # Claude Code

# 项目级：仅当前项目
git clone https://github.com/Voider-Li/MathModel-Contest-Flow.git \
  <你的项目>/.workbuddy-ai/skills/math-modeling-pro
```

对话里出现「数学建模 / 数模 / 国赛 / 美赛 / 建模论文 / 数据挖掘 / 独立测试集 / 文献核验」等词时，工具会自动加载本 skill。

### 环境依赖

- Python ≥ 3.10：`pandas`、`openpyxl`、`matplotlib`、`pdfplumber`
- 版面体检脚本另需 `pymupdf`
- TeX Live / CTeX：`xelatex` + `cumcmthesis`（仓库自带离线 `.cls` 兜底）

## 使用

正常做竞赛时，按 `SKILL.md` 的 11 个阶段推进即可，无需手动跑脚本。**交付前**必须跑一次自动体检：

```bash
# 门禁自检：目录结构、EDA 与数据挖掘章、基线对比、独立测试集、文献库、数值冻结、可复现
python scripts/check_gates.py <task_dir>

# 版面体检：单页占比与图挨图、说明文字字数、图表就近、乱码、正文页数
python scripts/check_layout.py main.pdf --tex main.tex
```

两个脚本**退出码非 0 即表示需要修复**。`check_gates.py` 的 G1 / G4 属启发式判断，会明确标注「需人工复核」，不能完全替代人工。

## 两类结构图，别画混

| 图 | 数量 | 放在哪 | 用什么画 |
|---|:--:|---|---|
| 论文总体架构图 | 全篇 1 张 | 问题分析节末尾 | `skills/tikz-architecture-diagram`（分层架构，Okabe-Ito 配色） |
| 各问解题流程图 | 每问 1 张 | 该问「模型建立」开头 | `templates/flow_snake.tex`（蛇形横向，现代柔和 6 色） |

判据：表达「全文怎么分层组织」的用架构图；表达「某一问怎么一步步算」的用流程图。两种画风不混用。

## 什么算「做完了」

不是「论文能编译」就算完，而是下面四条同时成立：

1. `check_gates.py` 退出码 0，八条门禁无红线级、无一致性级问题；
2. `check_layout.py` 退出码 0，版面六项全过；
3. 审稿评分表十个维度均 ≥ 4 分；
4. 支撑材料（代码 / 结果 CSV / README）与论文口径完全一致。

## 与上游的关系

本 skill 由两套来源融合而成，**能力与资源全部保留，方法论硬门禁为新增**：

| | 全流程能力包（上游） | 门控式工作流 | **本 skill** |
|---|:--:|:--:|:--:|
| 自包含、无外部依赖 | ✅ | ❌ | ✅ |
| 模板 / 脚本 / 子技能 | ✅ | ❌ | ✅ |
| 版面自动机检 | ✅ | ❌ | ✅ |
| 独立测试集门 | ✖ | ✅ | ✅ |
| 独立数据挖掘章 | ✖ | ✅ | ✅ |
| 文献核验门 | ✖ | ✅ | ✅ |
| 数值冻结 | ✖ | ✅ | ✅ |

## 致谢

本 skill 的**全流程能力底座**借鉴自开源项目 **[LEEHAHAHAHA/math-modeling-skill](https://github.com/LEEHAHAHAHA/math-modeling-skill)**。

读题拆解、建模方案选择、代码实现与增量纠错、可视化规范、论文写作与审稿流程，以及 `cumcmthesis` 离线类文件、TikZ 架构图子技能、`check_layout.py` 版面体检脚本等资源，均来自该项目。在此向原作者 **LEEHAHAHAHA** 及所有贡献者致以诚挚感谢。

本 skill 在其基础上补充了独立数据挖掘章、独立测试集检验、基线对比、文献核验与数值冻结等硬门禁，并继续以 MIT 许可证开源。如果本项目对你有帮助，也请一并给原项目点个 star。

## 许可证与免责

[MIT](LICENSE)。其中 `templates/cumcmthesis/cumcmthesis.cls` 是 [cumcmthesis](https://github.com/latexstudio/CUMCMThesis)（LaTeX Studio）官方类文件的离线副本，遵循其原有许可证，此处仅作离线兜底，实际以系统安装版本优先。

本仓库是竞赛方法论的标准化沉淀，仅供学习与研究使用。用 AI 辅助参赛时请遵守目标赛事的官方规则（部分赛事要求披露 AI 工具使用情况）。
