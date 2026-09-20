# 阶段 3-4:代码实现与求解

代码是论文的底气。论文里每个数字都要能在代码里复现,代码与论文口径必须完全一致。本阶段的核心是:**真实数据 + 可复现 + 增量纠错**。

## 1. 防伪数据红线(最严重的失分项之一)

**红线**:严禁用 `np.random`/`random` 生成模拟数据却未读取真实数据文件。

智能体会自动检测"假数据"信号:
- 代码含 `np.random` / `random.rand` / `random.normal`
- 且未引用任何真实数据文件名

命中即触发纠错循环,强制改为读取真实数据文件。

**写码硬性要求(必须传达给编程手)**:

```
1. 必须用 pandas.read_excel / read_csv / openpyxl 读取上面列出的真实数据文件(用其绝对路径);
2. 严禁生成随机数或模拟数据(np.random、random 等),严禁假设文件名为 data.csv;
3. 结果写入当前脚本目录的 results/ 子目录,关键数字 print 出来;
4. 用 matplotlib 绘制至少 5 张可视化图,保存到 results/ 子目录:
   - 各图表达意思互不重复,覆盖中间求解过程、最终结果、关键指标对比、趋势等;
   - 图片文件名必须非常详细、能直接识别内容,格式「Q{题号}_{内容描述}_{图表类型}.png」(如 Q1_各赛季观众数时序折线图.png),严禁 fig1.png/result.png 这类无意义命名(详见 visualization.md 第 9 节);
   - 用 plt.savefig 保存;含中文时先设置字体(见 visualization.md 第 3 节的 font.family 列表配方,不要只用 font.sans-serif);
   - 每张图有标题与坐标轴标签,figsize 宽大于高(如 (8,5))。
```

## 2. 数据文件绝对路径传递

编程手必须用**绝对路径**读取数据,不能假设文件名为 `data.csv`。上下文里要明确列出:

```
数据文件(必须用绝对路径读取):
- 绝对路径:/abs/path/02_data/附件1.xlsx(文件名:附件1.xlsx)
- 绝对路径:/abs/path/02_data/附件2.csv(文件名:附件2.csv)

数据结构:
附件1.xlsx[Sheet1]: 列=['日期','场馆','观众数'], 行数=1000
附件2.csv: CSV, 列=['队名','胜场','负场'], 数据行数=20
```

## 3. 求解代码上下文模板

每问的完整上下文(所有纠错轮次共享,保证修复时也能看到问题/方案/数据):

```
问题 Q{idx}:{rephrased}(类型:{type})
选定建模方案:
{chosen_json}

数据文件(必须用绝对路径读取):
{data_files_text}

数据结构:
{data_overview}

{hard_reqs}
```

## 4. 写码 → 运行 → Search-Replace 纠错迭代

### 4.1 首版:完整代码
首版要求完整输出可运行 Python 代码。输出 JSON:
```json
{"code": "完整的 Python 代码(用真实换行与缩进)"}
```

**思考模型陷阱**:若编程手配置的是推理/思考模型(如 deepseek-v4-flash、reasoner),写代码时内容会落入 `reasoning_content` 导致 `content` 为空。此时需把编程手模型改为非思考模型(如 deepseek-chat)。

### 4.2 运行 + 纠错:Search-Replace 增量修复
**禁止重写全文**。只修复出错部分,避免长代码截断/为空。

输出 JSON:
```json
{
  "edits": [
    {
      "search": "代码中真实存在的原文片段(精确复制,含缩进与换行)",
      "replace": "替换后的代码"
    }
  ]
}
```

**Search-Replace 三级匹配策略**(从严格到宽松,命中即止,借鉴 Aider):

1. **精确匹配**(逐字符):`search in content` → 替换第一处。
2. **压缩空白后精确匹配**:对每行压缩空白(去缩进、压行内空格)再匹配,容忍缩进偏移、多/少空格、行尾空白。
3. **difflib 模糊匹配**(相似度 ≥ 0.6):处理行内容个别字符的细微差异。首尾行须压缩后一致,避免改错位置。

每个 edit 只替换第一处匹配。失败列表反馈给 LLM 重试(把"哪些 search 没匹配上"明确告知)。

### 4.3 假数据检测(运行成功后)
即使代码运行成功,若 `_looks_fake(code, data_files)` 为真(含随机数且未读真实文件),视为无效,触发纠错:

```python
def _looks_fake(code: str, data_files: list) -> bool:
    uses_random = ("np.random" in code) or ("random.rand" in code) or ("random.normal" in code)
    if not uses_random:
        return False
    names = [getattr(f, "name", str(f)) for f in data_files]
    reads_real = any(n in code for n in names)
    return not reads_real
```

### 4.4 纠错上限
每问最多 10 轮纠错。同一问题连续 2 轮仍不过,停下来换思路,如实告知用户。

## 5. 可复现清单

每个 `solve.py` 必须满足:

- [ ] 用绝对路径读取真实数据文件
- [ ] 无模拟数据(或随机数仅用于算法本身如重启,且读真实数据)
- [ ] 关键数字 `print` 出来(供论文引用与重跑核对)
- [ ] 结果写入 `results/` 子目录(CSV + 图片)
- [ ] 至少 5 张可视化图,各图意思不重复
- [ ] 图片文件名详细可识别内容(`Q{题号}_{内容}_{图表类型}.png`,无 fig1.png)
- [ ] 含中文先设字体(见 `visualization.md` 第 3 节 font.family 列表配方)
- [ ] figsize 宽大于高(如 (8,5))
- [ ] 设随机种子(若算法含随机性,`np.random.seed(42)`)
- [ ] **按独立单元划分训练/验证/测试,最终指标来自独立测试集(门禁 G3,见 `validation.md` §1.1)**
- [ ] **关键结果已写入 `results/frozen_metrics.csv` 并冻结(门禁 G6,见 §9)**
- [ ] 脚本可独立运行(`python solve.py`),无外部依赖文件路径

## 6. 求解汇总提炼

求解完成后,从各问运行输出提炼"求解汇总",供论文手直接引用:

```
prompt:
以下是各问求解代码的运行输出,请提炼每问的关键数字与结论,生成「求解汇总」(供论文写作直接引用)。
{summary_input}

输出要求:逐问列出,格式「Q1:关键数字 + 结论」,语言简洁准确,只写汇总本身。
```

落 `04_solving/solve_summary.md` 和 `solve_summary.json`。

**踩坑教训**:
- 汇总失败不阻断流程,论文手仍可用 stdout 原文。
- 汇总里的关键数字会被论文手写进摘要,必须与代码运行结果完全一致(审稿时会核对)。

## 7. 代码—论文一致(交付前必查)

- 论文每个公式 → 代码里有对应实现,变量名/表达式对得上
- 论文描述的方法细节(初始化、贪心策略、局部搜索邻域、重启次数、停止条件、随机种子)→ 与代码实际行为一致
- 论文引用的每个关键数值(目标值、指标、改善率)→ **重跑脚本可复现**
- 附录代码与交付的支撑材料代码是**同一份**(论文用 `\lstinputlisting` 自动加载最终代码,不手抄)
- 命名/单位/口径在四处统一:论文正文、代码、结果 CSV、README

自动核对手段:
```bash
diff <(sed -n '/lstinputlisting/,/^}/p' main.tex) 支撑材料/代码/*.py   # 附录与交付代码一致
python solve.py | tee run.log                                           # 重跑核对关键数字
grep -E "关键数字|目标值" run.log                                         # 比对论文数字
```

## 8. 求解交付清单

- [ ] 每问 `Q{n}/solve.py` 可独立运行
- [ ] 用绝对路径读取真实数据,无假数据
- [ ] `results/` 下 ≥5 张图 + 结果 CSV
- [ ] 关键数字 print 出来
- [ ] `solve_summary.md` 已提炼
- [ ] 设随机种子(若算法含随机)
- [ ] 代码与论文口径一致
- [ ] 关键结果已冻结(见 §9)

## 9. 数值冻结门(硬门禁 G6)

**冻结 = 论文数字的唯一来源。** 在开始写论文之前,把一切会被写进正文的数字(测试集指标、对比表数值、敏感性区间、最优目标值、方案关键参数)统一写入结果文件并**冻结**,之后论文只引用冻结值。

**冻结时点(顺序不可颠倒):**

1. 阶段 4 求解完成 → 各问 `results/*.csv`;
2. 阶段 5 独立检验完成 → 测试集指标、对比表、稳健性/敏感性结果;
3. **确认全部跑通后**,写 `results/frozen_metrics.csv`(单一汇总文件),并在 `logs/` 记一条冻结时间戳;
4. 阶段 8 写作期间:**禁止**新增、改写或口头补充任何数值。

**冻结文件建议格式(`results/frozen_metrics.csv`):**

```csv
question,metric,value,unit,split,source_file,note
Q1,MAE,3.214,百万人,test,Q1/results/model_metrics.csv,主方法
Q1,MAE,4.902,百万人,test,Q1/results/baseline_metrics.csv,基线(上一期值)
Q2,objective,12840,元,full,Q2/results/opt_result.csv,最优目标值
```

- `source_file` 必须指向真实产物,每个正文数字都能顺藤摸瓜找到出处。
- 若某数字必须改动 → 回代码重跑 → 重新冻结 → **同步更新摘要/正文/表格/README**(见 `review.md` §5.2),不能只改一处。
- 交稿前跑 `python scripts/check_gates.py <task_dir>` 核验冻结文件存在且被引用。
