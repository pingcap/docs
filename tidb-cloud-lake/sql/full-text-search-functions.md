---
title: 全文搜索函数
summary: "{{{ .lake }}} 的全文搜索函数可为使用倒排索引建立索引的半结构化 `VARIANT` 数据和纯文本列提供类似搜索引擎的过滤能力。它们非常适合与资产一同存储的 AI 生成元信息，例如来自自动驾驶视频帧的感知结果。"
---

# 全文搜索函数

{{{ .lake }}} 的全文搜索函数可为使用倒排索引建立索引的半结构化 `VARIANT` 数据和纯文本列提供类似搜索引擎的过滤能力。它们非常适合与资产一同存储的 AI 生成元信息，例如来自自动驾驶视频帧的感知结果。

> **注意：**
>
> {{{ .lake }}} 的搜索函数受 [Elasticsearch Full-Text Search Functions](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html) 启发。

在表定义中，为你计划搜索的列包含倒排索引：

```sql
CREATE OR REPLACE TABLE frames (
  id INT,
  meta VARIANT,
  INVERTED INDEX idx_meta (meta)
);
```

## 搜索函数 {#search-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [MATCH](/tidb-cloud-lake/sql/match.md) | 对列出的列执行按相关性排序的搜索。 | `MATCH('summary, tags', 'traffic light red')` |
| [QUERY](/tidb-cloud-lake/sql/query.md) | 对 Lucene 风格的查询表达式进行求值，包括嵌套的 `VARIANT` 字段。 | `QUERY('meta.signals.traffic_light:red')` |
| [SCORE](/tidb-cloud-lake/sql/score.md) | 与 `MATCH` 或 `QUERY` 一起使用时，返回当前行的相关性得分。 | `SELECT summary, SCORE() FROM frame_notes WHERE MATCH('summary, tags', 'traffic light red')` |

## 查询语法示例 {#query-syntax-examples}

### 示例：单个关键字 {#example-single-keyword}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:pedestrian')
LIMIT 100;
```

### 示例：布尔 AND {#example-boolean-and}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')
LIMIT 100;
```

### 示例：布尔 OR {#example-boolean-or}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike')
LIMIT 100;
```

### 示例：IN 列表 {#example-in-list}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]')
LIMIT 100;
```

### 示例：包含端点的范围 {#example-inclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]')
LIMIT 100;
```

### 示例：不包含端点的范围 {#example-exclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}')
LIMIT 100;
```

### 示例：字段加权 {#example-boosted-fields}

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0')
LIMIT 100;
```