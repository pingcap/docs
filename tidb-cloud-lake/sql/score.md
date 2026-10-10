---
title: SCORE
summary: 反転インデックス検索条件に一致した行の関連性スコアを返します。
---

# SCORE

`SCORE()` は、反転インデックス検索によって現在の行に割り当てられた関連性スコアを返します。`WHERE` 句で [MATCH](/tidb-cloud-lake/sql/match.md) または [QUERY](/tidb-cloud-lake/sql/query.md) と一緒に使用します。

> **Note:**
>
> {{{ .lake }}} の SCORE 関数は、Elasticsearch の [SCORE](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-score) に着想を得ています。

## 構文 {#syntax}

```sql
SCORE()
```

## 例 {#examples}

### 例: MATCH 用のテキストノートを準備する {#example-prepare-text-notes-for-match}

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

### 例: MATCH の結果をスコアリングする {#example-score-match-results}

```sql
SELECT summary, SCORE()
FROM frame_notes
WHERE MATCH('summary^2, tags', 'traffic light red', 'operator=AND')
ORDER BY SCORE() DESC;
```

### 例: QUERY の結果をスコアリングする {#example-score-query-results}

[QUERY](/tidb-cloud-lake/sql/query.md) の例で使用した `frames` テーブルを再利用します。

```sql
SELECT id, SCORE()
FROM frames
WHERE QUERY('meta.detections.label:pedestrian^3 AND meta.scene.time_of_day:day');
```