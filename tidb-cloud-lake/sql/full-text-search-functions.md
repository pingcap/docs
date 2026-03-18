---
title: Full-Text Search Functions
summary: Databend's full-text search functions deliver search-engine-style filtering for semi-structured VARIANT data and plain text columns that are indexed with an inverted index. They are ideal for AI-generated metadata—such as perception results from autonomous-driving video frames—stored alongside your assets.
---
Databend's full-text search functions deliver search-engine-style filtering for semi-structured `VARIANT` data and plain text columns that are indexed with an inverted index. They are ideal for AI-generated metadata—such as perception results from autonomous-driving video frames—stored alongside your assets.

> **Note:**
>
> Databend's search functions are inspired by [Elasticsearch Full-Text Search Functions](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html).

Include an inverted index in the table definition for the columns you plan to search:

```sql
CREATE OR REPLACE TABLE frames (
  id INT,
  meta VARIANT,
  INVERTED INDEX idx_meta (meta)
);
```

## Search Functions

| Function | Description | Example |
|----------|-------------|---------|
| [MATCH](/tidb-cloud-lake/sql/match.md) | Performs a relevance-ranked search across the listed columns. | `MATCH('summary, tags', 'traffic light red')` |
| [QUERY](/tidb-cloud-lake/sql/query.md) | Evaluates a Lucene-style query expression, including nested `VARIANT` fields. | `QUERY('meta.signals.traffic_light:red')` |
| [SCORE](/tidb-cloud-lake/sql/score.md) | Returns the relevance score for the current row when used with `MATCH` or `QUERY`. | `SELECT summary, SCORE() FROM frame_notes WHERE MATCH('summary, tags', 'traffic light red')` |

## Query Syntax Examples

### Example: Single Keyword

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:pedestrian')
LIMIT 100;
```

### Example: Boolean AND

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')
LIMIT 100;
```

### Example: Boolean OR

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike')
LIMIT 100;
```

### Example: IN List

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]')
LIMIT 100;
```

### Example: Inclusive Range

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]')
LIMIT 100;
```

### Example: Exclusive Range

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}')
LIMIT 100;
```

### Example: Boosted Fields

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0')
LIMIT 100;
```
