# 阶段 1:读题与拆解

读题是整个建模流程的地基。题读错了,后面全白费。本阶段的目标:把赛题文件解析成结构化任务包,把 N 问各自的问题、数据、约束列清楚,确认每问类型。

## 1. 赛题文件解析协议

赛题可能以多种格式提交,按以下顺序处理:

| 格式 | 工具 | 处理要点 |
|---|---|---|
| `.md` / `.txt` | 直接 `read_text(encoding="utf-8", errors="ignore")` | 最稳,首选 |
| `.pdf` | `pdfplumber` / `pypdf` / `fitz` | 提取文字;公式可能乱码,需人工或图识别补 |
| `.docx` / `.doc` | `python-docx`(`.doc` 需先转 `.docx` 或用 `textract`) | 注意 `.doc` 老格式二进制解析,utf-8 编码处理 |
| `.png` / `.jpg` / `.jpeg` | 多模态识别手(如有) | 公式转 LaTeX,生成"图N 描述" |

**多模态识别图片的 prompt**:
```
请识别这张题目图片(图{i})的内容,公式用 LaTeX。
```
识别结果存为 `{"fig_id": "图1", "desc": "..."}` 列表,供后续建模手参考。

**踩坑教训**:
- `.doc` 老格式二进制解析:必须用专门库,不要硬读 text;GBK 编码错误时用 `errors="ignore"` 或转 utf-8。
- PDF 公式提取常出乱码:把 PDF 每页当图片再做多模态识别,比直接提文字更可靠。
- 题目图片顺序:按文件名自然排序(`sorted(files, key=natural_key)`),避免图1/图10/图2 乱序。

## 2. 附件数据结构探查

在建模前必须摸清数据,否则单位/标签写反会毁掉整问。

**探查脚本**(落 `task_package.json` 的 `data_files` 字段):

```python
import csv, openpyxl, json
from pathlib import Path

def data_overview(data_dir: Path) -> str:
    lines = []
    for f in sorted(data_dir.glob("*")):
        if not f.is_file(): continue
        ext = f.suffix.lower()
        try:
            if ext in (".csv", ".tsv"):
                with open(f, encoding="utf-8-sig", errors="ignore") as fh:
                    header = next(csv.reader(fh), [])
                    n = sum(1 for _ in fh)
                lines.append(f"{f.name}: CSV, 列={header}, 数据行数={n}")
            elif ext in (".xlsx", ".xls"):
                wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
                for ws in wb.worksheets:
                    first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())
                    lines.append(f"{f.name}[{ws.title}]: 列={list(first)}, 行数={ws.max_row}")
            elif ext == ".json":
                lines.append(f"{f.name}: JSON 数据文件")
        except Exception as e:
            lines.append(f"{f.name}: 无法解析({e})")
    return "\n".join(lines) if lines else "(无数据文件)"
```

**探查要点**:
- 每个 sheet 的列名、行数、单位(从列名/表头推断,如"预测观众(百万人)" vs "人")。
- 缺失值:用 `df.isnull().sum()` 统计,记录缺失比例高的列。
- 数据类型:数值列 / 文本列 / 日期列,日期格式是否统一。
- 关键统计量:数值列的 min/max/mean/std,异常值(超出合理范围的)。

## 3. 拆题:把赛题拆成 Q1..Qn

建模手拿到题面 + 数据结构 + 图片描述后,拆题输出 JSON:

```json
{
  "questions": [
    {"index": 1, "rephrased": "一句话复述该问要解决的核心问题", "type": "回归|优化|评估|仿真|预测|分类"},
    {"index": 2, "rephrased": "...", "type": "..."}
  ],
  "data_requirements": ["字段X用于...","字段Y需做缺失处理..."]
}
```

**拆题要点**:
- `rephrased` 是一句话复述,不是抄题;要提炼核心任务(如"基于历史观众数据,预测下赛季各场观众数并给出置信区间")。
- `type` 决定后续建模偏好序(见 `modeling.md`):
  - **回归**:有标签连续值,要预测/解释 → 线性回归/对数线性/ARIMA
  - **优化**:有目标 + 约束,要决策 → 线性/整数规划/启发式
  - **评估**:要打分/排序/分级 → AHP/TOPSIS/熵权法/综合评价
  - **仿真**:要模拟系统行为 → 蒙特卡洛/离散事件/系统动力学
  - **预测**:时序预测 → ARIMA/指数平滑/机理模型
  - **分类**:有标签离散值 → 逻辑回归/决策树(+稳健性对照)
- 多问之间往往有递进关系(Q1 的结果是 Q2 的输入),在 `rephrased` 里点明。

## 4. 任务包落地

把解析结果落 `03_modeling/task_package.json`:

```json
{
  "task_id": "2026A",
  "user_description": "用户口述的额外要求(如有)",
  "problem_text": "完整题面文本(合并多文件)",
  "image_descriptions": [{"fig_id": "图1", "desc": "..."}],
  "data_files": [{"name": "data.xlsx", "path": "02_data/data.xlsx"}]
}
```

这个文件是后续所有阶段的唯一题面来源,避免重复解析。

## 5. 检查点 CP1:用户确认

向用户展示:
- 拆题结果(Q1..Qn 的 rephrased + type)
- 数据结构探查摘要
- 图片识别摘要(如有)

请用户确认:拆题是否完整?类型判定是否准确?有无遗漏的子任务?确认后才进入阶段 2。

## 6. 读题交付清单

- [ ] 赛题所有文件已解析(含图片多模态识别)
- [ ] 附件数据结构已探查(列名/行数/单位/缺失)
- [ ] 拆题 JSON 完整(每问 rephrased + type)
- [ ] `task_package.json` 已落地
- [ ] 用户在 CP1 确认通过
