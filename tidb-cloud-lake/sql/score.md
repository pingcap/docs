---
title: SCORE
summary: 返回由倒排索引搜索条件匹配到的行的相关性得分。
---

# SCORE

`SCORE()` 返回倒排索引搜索为当前行分配的相关性得分。请将其与 `WHERE` 子句中的 [MATCH](/tidb-cloud-lake/sql/match.md) 或 [QUERY](/tidb-cloud-lake/sql/query.md) 一起使用。

> **注意：**
>
> {{{ .lake }}} 的 SCORE 函数受 Elasticsearch 的 [SCORE](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-score) 启发。

## 语法 {#syntax}

```sql
SCORE()
```

## 示例 {#examples}

### 示例：为 MATCH 准备文本注释 {#example-prepare-text-notes-for-match}

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

### 示例：为 MATCH 结果评分 {#example-score-match-results}

```sql
SELECT summary, SCORE()
FROM frame_notes
WHERE MATCH('summary^2, tags', 'traffic light red', 'operator=AND')
ORDER BY SCORE() DESC;
```

### 示例：为 QUERY 结果评分 {#example-score-query-results}

复用 [QUERY](/tidb-cloud-lake/sql/query.md) 示例中的 `frames` 表：

```sql
SELECT id, SCORE()
FROM frames
WHERE QUERY('meta.detections.label:pedestrian^3 AND meta.scene.time_of_day:day');
```