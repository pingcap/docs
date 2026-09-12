---
title: MATCH
summary: 在已建立索引的列中搜索与关键字匹配的内容，并且只能在 WHERE 子句中使用。
---

# MATCH

`MATCH` 用于在列出的列中搜索包含给定关键字的行。该函数只能出现在 `WHERE` 子句中。

> **Note:**
>
> {{{ .lake }}} 的 MATCH 函数受 Elasticsearch 的 [MATCH](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-match) 启发。

## 语法 {#syntax}

```sql
MATCH('<columns>', '<keywords>'[, '<options>'])
```

- `<columns>`：要搜索的列列表，以逗号分隔。可追加 `^<boost>` 以提高某一列相对于其他列的权重。
- `<keywords>`：要搜索的词项。可追加 `*` 进行后缀匹配，例如 `rust*`。
- `<options>`：可选参数，以分号分隔的 `key=value` 列表，用于微调搜索行为。

## 选项 {#options}

| 选项 | 取值 | 描述 | 示例 |
|--------|--------|-------------|---------|
| `fuzziness` | `1` 或 `2` | 在指定的 Levenshtein 距离内匹配关键字。 | `MATCH('summary, tags', 'pedestrain', 'fuzziness=1')` 可匹配包含正确拼写 `pedestrian` 的行。 |
| `operator` | `OR`（默认）或 `AND` | 当未指定布尔运算符时，控制如何组合多个关键字。 | `MATCH('summary, tags', 'traffic light red', 'operator=AND')` 要求同时包含这些词。 |
| `lenient` | `true` 或 `false` | 当为 `true` 时，抑制解析错误并返回空结果集。 | `MATCH('summary, tags', '()', 'lenient=true')` 会返回空结果，而不是报错。 |

## 示例 {#examples}

在许多 AI 流水线中，你可能会在 `VARIANT` 列中保存结构化元信息，同时将便于人类阅读的摘要物化出来以供搜索。以下示例存储了从 JSON 负载中提取的行车记录仪帧摘要和标签。

### 示例：构建可搜索的摘要 {#example-build-searchable-summaries}

```sql
CREATE OR REPLACE TABLE frame_notes (
  id INT,
  camera STRING,
  summary STRING,
  tags STRING,
  INVERTED INDEX idx_notes (summary, tags)
);

INSERT INTO frame_notes VALUES
  (1, 'dashcam_front',
      'Green light at Market & 5th with pedestrian entering the crosswalk',
      'downtown commute green-light pedestrian'),
  (2, 'dashcam_front',
      'Vehicle stopped at Mission & 6th red traffic light with cyclist ahead',
      'stop urban red-light cyclist'),
  (3, 'dashcam_front',
      'School zone caution sign in SOMA with pedestrian waiting near crosswalk',
      'school-zone caution pedestrian');
```

### 示例：布尔 AND {#example-boolean-and}

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary, tags', 'traffic light red', 'operator=AND');
-- Returns id 2
```

### 示例：模糊匹配 {#example-fuzzy-matching}

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary^2, tags', 'pedestrain', 'fuzziness=1');
-- Returns ids 1 and 3
```