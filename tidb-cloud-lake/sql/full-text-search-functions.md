---
title: 全文検索関数
summary: "{{{ .lake }}} の全文検索関数は、転置インデックスが作成された半構造化 `VARIANT` データおよびプレーンテキストのカラムに対して、検索エンジンのようなフィルタリングを提供します。これらは、アセットとともに保存される AI 生成メタデータ（自動運転の動画フレームから得られる認識結果など）に最適です。"
---

# 全文検索関数

{{{ .lake }}} の全文検索関数は、転置インデックスが作成された半構造化 `VARIANT` データおよびプレーンテキストのカラムに対して、検索エンジンのようなフィルタリングを提供します。これらは、アセットとともに保存される AI 生成メタデータ（自動運転の動画フレームから得られる認識結果など）に最適です。

> **Note:**
>
> {{{ .lake }}} の検索関数は、[Elasticsearch Full-Text Search Functions](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html) に着想を得ています。

検索対象にするカラムについては、テーブル定義に転置インデックスを含めてください。

```sql
CREATE OR REPLACE TABLE frames (
  id INT,
  meta VARIANT,
  INVERTED INDEX idx_meta (meta)
);
```

## 検索関数 {#search-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [MATCH](/tidb-cloud-lake/sql/match.md) | 指定したカラム全体に対して、関連度順の検索を実行します。 | `MATCH('summary, tags', 'traffic light red')` |
| [QUERY](/tidb-cloud-lake/sql/query.md) | ネストされた `VARIANT` フィールドを含む、Lucene スタイルのクエリ式を評価します。 | `QUERY('meta.signals.traffic_light:red')` |
| [SCORE](/tidb-cloud-lake/sql/score.md) | `MATCH` または `QUERY` とともに使用した場合に、現在の行の関連度スコアを返します。 | `SELECT summary, SCORE() FROM frame_notes WHERE MATCH('summary, tags', 'traffic light red')` |

## クエリ構文の例 {#query-syntax-examples}

### 例: 単一キーワード {#example-single-keyword}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:pedestrian')
LIMIT 100;
```

### 例: Boolean AND {#example-boolean-and}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')
LIMIT 100;
```

### 例: Boolean OR {#example-boolean-or}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike')
LIMIT 100;
```

### 例: IN リスト {#example-in-list}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]')
LIMIT 100;
```

### 例: 包含範囲 {#example-inclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]')
LIMIT 100;
```

### 例: 排他範囲 {#example-exclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}')
LIMIT 100;
```

### 例: ブーストされたフィールド {#example-boosted-fields}

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0')
LIMIT 100;
```