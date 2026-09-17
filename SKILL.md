---
name: mathmodel-contest-flow
description: 数学建模竞赛混合工作流。用于启动完整的国赛、美赛或同类建模任务，以 r1 顺序式流水线快速产出报告、图表和论文，同时以 r0 门控式技能强制方案对比、独立数据挖掘、独立测试集检验、决策留痕和最终审计。当用户要求“结合两套 skill”“新建模工作流”“保证对比明显和检验独立”时使用。
---

# 数学建模混合工作流（r1 速度 + r0 门禁）

## 定位

本 skill 是总控编排器，不替代任何下游 skill。它把 `r1`（当前环境中面向数学建模的顺序式技能，通常位于 agents/skills）的端到端交付速度与 `r0`（当前环境中面向 Codex 的门控式技能，通常位于 .codex/skills）的门控质量约束合成一条可执行流程。`r1`、`r0` 只是习惯叫法，不要依赖具体安装路径。

两条不可妥协的验收标准：

1. 每个子问题必须有可量化、可复现的方案对比，结论由对比表支撑。
2. 论文必须有独立成章的“数据挖掘”和“模型检验”，模型最终指标必须来自独立测试集。

## 模式

- `lean`：默认。适合 72 小时赛程。保留全部强制门禁，但压缩人工决策和审计文件。
- `submission`：面向冲刺国奖或赛前演练。保留 r0 的 method card、decision ledger、risk probe、QA 审计等完整证据链。

模式写入 `planning/session_config.json`。不允许用 `lean` 省略任何强制门禁。

## 可移植性

- 本 skill 不写死任何绝对路径，可直接复制到任意 agent 的 skills 根目录使用。
- 启动时通过当前会话的技能列表、环境默认技能根或用户指定的目录定位下游 skill；禁止假设 Windows 或 Linux 的固定路径。
- 若某个 `r0`/`r1` 技能在当前环境不存在，用等效人工步骤补齐同样产物，不能因路径不同跳过门禁。
- 每个 skill 都是独立目录，随本 skill 一起分发时保留其自身 `SKILL.md` 结构，不合并文件。
- 若 r0/r1 原技能已归档到本仓库 `skills/r0`、`skills/r1`，优先从仓库相对路径读取；环境无技能时用等效人工步骤补齐，不因归档跳过门禁。

## 启动

1. 读取或询问偏好：排版引擎（Typst/LaTeX）、竞赛类型、论文语言、子问题数量、实现语言（Python/MATLAB）、模式、可用时间。
2. 运行 `doctor`（r1）检查环境；缺失依赖先安装再继续。
3. 创建 `plan.md`、`todo.md` 和 `planning/session_config.json`。
4. 若工作区已有旧 r1 产物，先盘点再迁移，不覆盖用户已有内容。

## 模板优先级

1. **用户提供的模板优先**：若工作区存在 `全国大学生数学建模竞赛LaTeX模板/`，使用其中的 `cumcmthesis.cls` 和 `example.tex` 作为论文基础，保留封面、页眉、字体、行距和章节样式，不擅自替换为内置模板。
2. 用户没有提供模板时，才使用 `skills/r1/5writing/templates` 中的内置模板。
3. 开始写作前确认模板文件、编译命令和字体依赖可用；LaTeX 使用 `xelatex` 编译并跑两遍解决交叉引用。
4. 论文中的自定义样式只能修改正文相关设置，不能破坏模板的格式规范。

## 阶段与门禁

| 门禁 | 目的 | 主要 skill | 必须产出 | 放行条件 |
| --- | --- | --- | --- | --- |
| G0 设置 | 定偏好与计划 | `1start-mathmodel` 的偏好逻辑、`doctor` | `plan.md`、`todo.md`、`planning/session_config.json` | 偏好已记录、环境可用 |
| G1 问题框架 | 拆题、分类、数据盘点 | `problem-parser`、`problem-classifier`、`data-auditor-cleaner`、`related-paper-analyzer` | Qx framing、`data/data_report.md`、`data/data_profile.json` | 每个 Qx 的输出、评价口径、数据风险已知 |
| G2 方法筛选 | 定主方法+基线+备选 | `method-selector`、`decision-prompt-builder`、`modeler-decision-logger`、`model-assumptions-builder`、`symbol-table-builder` | `methods/Qx/qx_method_card.md`、`methods/Qx/qx_decisions.jsonl`、假设与符号表 | 主方法与基线被人工确认并留痕 |
| G3 数据挖掘 | 独立成章的数据分析 | `data-auditor-cleaner` 延续、探索性分析、特征工程 | `reports/DATA_MINING_REPORT.md`、论文独立数据挖掘章素材 | 缺失/离群/分布/相关/轨迹/防泄漏全部有结论 |
| G4 建模实现 | 只实现批准方法 | `model-code-analyzer`、`python-model-code-generator` 或 `matlab-model-code-generator`、对应 code-reviewer | `code/`、`results/`、`reports/RESULTS_REPORT.md` | 代码可复现、评审通过、基线已实现 |
| G5 对比与稳健性 | 数值对比+独立检验 | `robustness-checker`、`result-report-generator`、`figure-table-planner`、`math-figure-generator` | `reports/COMPARISON_REPORT.md`、对比表、ROC/曲线、独立测试集指标、冻结数值 | 每个 Qx 有基线对比；测试集指标已冻结 |
| G5.5 文献管理 | 建库、引用、核验 | `reference-manager`、`related-paper-analyzer` | `references/` 文献库、`.bib` 或 `references.json`、核验记录 | 每条文献真实可查、被正文实际引用、无硬编码编号 |
| G6 论文撰写 | 从冻结结果写论文 | `5writing`、`4drawio`、`paper-section-writer`、`paper-polisher`、`reference-manager` | `paper/` 完整章节、全部图表被引用 | 自动编号、无硬编码图号、无未引用图、无编造数值 |
| G7 最终验收 | 提交前全检 | `6verity`、`consistency-auditor`、`completeness-auditor`、`quality-assurance-auditor`、`solution-package-builder`、`论文评审` | `reports/VERIFY_REPORT.md`、提交包 | 编译通过、对比/检验/引用/一致性全 PASS |

## 强制门禁（任何模式不得跳过）

1. **基线门**：每个 Qx 的 method card 必须包含一个“能完成真实任务、产出可比指标”的基线；禁止用玩具方法冒充。
2. **数据挖掘门**：必须形成独立数据挖掘报告和论文独立章节，内容至少包括：变量字典、缺失/重复/离群、单变量分布、相关与共线性、分组差异、重复测量/时序轨迹、特征工程与防泄漏。
3. **独立检验门**：分类/预测/回归必须按独立单元（如个体、批次、时空单元）划分训练/验证/测试；最终指标只能来自从未参与训练的测试集。交叉验证可补充，但不能替代。
4. **对比门**：每个 Qx 结尾必须有“基线 vs 主方法 vs 备选”对比表；优化/分组类题目还要有风险、成本、误差或收益差异；分类题必须有多数类基线。
5. **论文门**：图号/表号/公式号全部自动编号并用交叉引用；禁止硬编码“图8”；生成但未引用的图必须删除或补正文；论文数值必须来自冻结结果。
6. **文献门**：先建文献库再写正文；每条文献必须有作者、标题、年份、期刊/来源、卷期页码、DOI 或 URL；禁止凭记忆补 DOI 和页码；正文用键值引用；交稿前逐条核验格式与语义。
7. **数值冻结门**：所有正文数字必须来自已冻结的结果文件；论文写作期间禁止新增、改写或口头补充数值。
8. **代码可复现门**：固定随机种子、依赖版本、数据路径；提交前代码必须能完整跑通；评审重点查数据泄漏、样本划分、除零和边界情况。
9. **图表门**：每张图必须被正文引用，未引用图删除；对比图放同一坐标系；坐标轴、单位、图例完整；图表标题与实际内容一致。
10. **表达门**：低拟合、低性能直说并解释原因；禁止用“明显提升”“最优”代替对比表和统计检验；符号、单位、变量名全篇一致。
11. **流程门**：多个 Agent 不写同一文件；产物固定命名；72 小时赛程设置硬性时间点，禁止最后一天临时改模型。
12. **Agent 约束门**：禁止编数据、编文献、编实验结果；失败或不确定必须明说；人工决策点必须停下问人；每个结论都能指到具体产物文件。

## 参考文献来源

- 中文检索：知网（https://www.cnki.net）、万方（https://www.wanfangdata.com.cn）、维普（http://www.cqvip.com）、百度学术（https://xueshu.baidu.com）。
- 英文检索：Google Scholar（https://scholar.google.com）、Semantic Scholar（https://www.semanticscholar.org）、PubMed（https://pubmed.ncbi.nlm.nih.gov）、arXiv（https://arxiv.org）、DOAJ（https://doaj.org）、CORE（https://core.ac.uk）。
- DOI 与元数据核验：Crossref（https://search.crossref.org）、Crossref API（https://api.crossref.org/works?query.title=...）、OpenAlex（https://openalex.org）、DOI 解析（https://doi.org/<DOI>）。
- 使用规则和字段要求见 `references/reference-sources.md`。

## 论文章节骨架

1. 问题重述与分析
2. 数据预处理与独立数据挖掘
3. 模型假设与符号说明
4. 各子问题建模与求解（每问末尾放对比总表）
5. 方案/模型对比汇总
6. 模型检验与评价（独立成章，含独立测试集）
7. 结论、优缺点与推广
8. 参考文献与附录

详细产出契约见 `references/gate-contracts.md`。

## 调用约定

- 优先按门禁表调用已安装 skill；进入每个 skill 前读取其 `SKILL.md`，遵守其前置条件和产物契约。
- r0 技能要求人工决策时，用 `decision-prompt-builder` 生成选择卡；AI 只给证据，不替用户拍板；用户决定由 `modeler-decision-logger` 追加记录。
- 若某个 r0 skill 缺失或环境不允许，必须用等效人工步骤补齐同样产物，不能直接跳过。
- r1 的 `4drawio` 负责非数据图；r0 的 `math-figure-generator` 负责数据图；两者不重复绘制。
- 若原 r0/r1 已从技能环境删除，但仓库中存在 `skills/r0`、`skills/r1` 归档，优先从归档相对路径读取；没有归档时按等效人工步骤执行。

## 结束条件

只有 G7 全 PASS 才算完成。若审计发现任一强制门禁未满足，回到对应门禁修复后重新运行后续依赖阶段，禁止“先交稿再补”。
