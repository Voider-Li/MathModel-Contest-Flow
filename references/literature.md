# 阶段 5.8:文献管理与核验(强制门禁)

参考文献是论文可信度的一部分。评委抽查一条文献发现是编的,整篇的可信度都会受质疑。本文件规定:**先建库、再引用、后核验**,禁止硬编码编号、禁止凭记忆补 DOI。

> **门禁等级:一致性级(编造文献 → 红线级)。** 未核验或找不到原文的条目不得进入正文。

## 1. 文献门五条硬约束

1. **先建库再写作**:写正文之前先建 `references/` 文献库(`.bib` 或 `references.json`),正文只从库里引用。
2. **字段完整**:每条文献必须含 作者、标题、年份、期刊/会议/教材/标准、卷期页码、DOI 或 URL、来源文件或检索链接、`verified` 标记。
3. **真实可查**:只允许真实检索到的文献;找不到原文的标记 `unverified`,**不得进入正文**。
4. **键值引用**:正文用 `\cite{key}` 或 `@cite(key)`,**禁止手写"文献[5]"** 这类硬编码编号。
5. **交稿前逐条核验**:key 是否存在、是否被正文实际引用、作者/年份/期刊是否正确、正文表述是否与文献结论相符。

## 2. 文献库格式

`references/library.bib`(BibTeX,推荐)或 `references/references.json`:

```bibtex
@article{zhou2023forecast,
  author  = {周某某 and 李某某},
  title   = {基于时间序列的体育赛事上座率预测模型},
  journal = {系统工程理论与实践},
  year    = {2023},
  volume  = {43},
  number  = {6},
  pages   = {1650--1662},
  doi     = {10.12011/SETP2022-1234},
  url     = {https://www.cnki.net/...},
  source  = {CNKI 检索,2026-09-20},
  verified = {true}
}
```

```json
[
  {
    "key": "zhou2023forecast",
    "author": "周某某, 李某某",
    "title": "基于时间序列的体育赛事上座率预测模型",
    "year": 2023,
    "venue": "系统工程理论与实践",
    "volume": "43", "number": "6", "pages": "1650-1662",
    "doi": "10.12011/SETP2022-1234",
    "url": "https://www.cnki.net/...",
    "source": "CNKI 检索,2026-09-20",
    "verified": true
  }
]
```

## 3. 检索与核验来源(只用真实可访问的库)

### 中文检索
- 知网 CNKI:https://www.cnki.net
- 万方:https://www.wanfangdata.com.cn
- 维普:http://www.cqvip.com
- 百度学术:https://xueshu.baidu.com

### 英文检索
- Google Scholar:https://scholar.google.com
- Semantic Scholar:https://www.semanticscholar.org
- PubMed:https://pubmed.ncbi.nlm.nih.gov
- arXiv:https://arxiv.org
- DOAJ:https://doaj.org
- CORE:https://core.ac.uk
- DBLP:https://dblp.org

### DOI 与元数据核验
- Crossref 检索:https://search.crossref.org
- Crossref API:https://api.crossref.org/works?query.title=...
- OpenAlex:https://openalex.org
- DOI 解析:https://doi.org/<DOI>

## 4. 核验流程

1. **检索**:用关键词在中文/英文库检索,记录命中文献的原始页面 URL。
2. **取元数据**:优先用原始出版方/期刊官网页面;英文文献以期刊页面或 Crossref 返回为准;中文文献字段用原文核对。
3. **验 DOI**:把 DOI 拼到 `https://doi.org/<DOI>` 看能否解析到同一篇;Crossref API 返回的作者/年份/卷期要与页面一致。
4. **打标**:能追溯到原文的 `verified=true`;查不到全文的 `verified=false` 且不进正文。
5. **正文核对**:引用前确认正文表述与文献结论一致,**不能"引用一篇相关文献来替自己的结论背书"**。
6. **交稿复核**:跑 `scripts/check_gates.py` 检查未核验条目与被引用情况(见 §6)。

## 5. 常见踩坑

| 坑 | 后果 | 规避 |
|---|---|---|
| 凭记忆补 DOI/页码 | 编造文献,红线 | 每条都从检索页复制,DOI 必须能解析 |
| 硬编码"文献[5]" | 增删文献后编号全乱 | 一律 `\cite{key}` 自动编号 |
| 引了但正文没提 | 孤儿引用 | 交稿前核对每条都被正文实际引用 |
| 引"相关"文献替结论 | 张冠李戴 | 引用前读摘要/结论,确认支持你的说法 |
| 教材/标准没给版本年 | 无法追溯 | 补版本、年份、出版方 |
| 网络资源无访问日期 | 无法追溯 | 补 URL 与访问日期 |

## 6. 自动核验(scripts/check_gates.py 的文献项)

脚本会检查:
- `references/` 下是否存在 `.bib` / `references.json`;
- 是否有 `verified=false` / 缺 DOI 或 URL 的条目(报 key 与缺失字段);
- 正文 `.tex` 里是否出现硬编码 `文献[数字]` 或 `[数字]` 式引用(违规报行号);
- 文献库里是否有从未被 `\cite` 的条目(提示删除或补引用)。

## 7. 交付清单

- [ ] `references/` 文献库已建立(`.bib` 或 `references.json`)
- [ ] 每条文献字段完整(作者/标题/年份/来源/卷期页码/DOI 或 URL/来源链接/verified)
- [ ] 所有进正文的条目 `verified=true`,DOI 可解析
- [ ] 正文全部用 `\cite{key}`,无硬编码"文献[5]"
- [ ] 每条文献都被正文实际引用,无孤儿条目
- [ ] 正文表述与文献结论一致
- [ ] 参考文献格式统一(GB/T 7714 或赛事指定格式)
