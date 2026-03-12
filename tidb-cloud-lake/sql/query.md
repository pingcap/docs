---
title: QUERY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.830"/>

`QUERY` filters rows by matching a Lucene-style query expression against columns that have an inverted index. Use dot notation to navigate nested fields inside `VARIANT` columns. The function is valid only in a `WHERE` clause.

:::info
Databend's QUERY function is inspired by Elasticsearch's [QUERY](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-query).
:::

## Syntax

```sql
QUERY('<query_expr>'[, '<options>'])
```

`<options>` is an optional semicolon-separated list of `key=value` pairs that adjusts how the search works.

## Building Query Expressions

| Expression | Purpose | Example |
|------------|---------|---------|
| `column:keyword` | Matches rows where `column` contains the keyword. Append `*` for suffix matching. | `QUERY('meta.detections.label:pedestrian')` |
| `column:"exact phrase"` | Matches rows that contain the exact phrase. | `QUERY('meta.scene.summary:"vehicle stopped at red traffic light"')` |
| `column:+required -excluded` | Requires or excludes terms in the same column. | `QUERY('meta.tags:+commute -cyclist')` |
| `column:term1 AND term2` / `column:term1 OR term2` | Combines multiple terms with boolean operators. `AND` has higher precedence than `OR`. | `QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')` |
| `column:IN [value1 value2 ...]` | Matches any value from the list. | `QUERY('meta.tags:IN [stop urban]')` |
| `column:[min TO max]` | Performs inclusive range search. Use `*` to leave one side open. | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |
| `column:{min TO max}` | Performs exclusive range search that omits the boundary values. | `QUERY('meta.vehicle.speed_kmh:{0 TO 10}')` |
| `column:term^boost` | Increases the weight of matches in a specific column. | `QUERY('meta.signals.traffic_light:red^1.0 meta.tags:urban^2.0')` |

### Nested `VARIANT` Fields

Use dot notation to address inner fields inside a `VARIANT` column. Databend evaluates the path across objects and arrays.

| Pattern | Description | Example |
|---------|-------------|---------|
| `variant_col.field:value` | Matches an inner field. | `QUERY('meta.signals.traffic_light:red')` |
| `variant_col.field:IN [ ... ]` | Matches any value inside arrays. | `QUERY('meta.detections.label:IN [pedestrian cyclist]')` |
| `variant_col.field:[min TO max]` | Applies range search to numeric inner fields. | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |

## Options

| Option | Values | Description | Example |
|--------|--------|-------------|---------|
| `fuzziness` | `1` or `2` | Matches terms within the specified Levenshtein distance. | `SELECT id FROM frames WHERE QUERY('meta.detections.label:pedestrain', 'fuzziness=1');` |
| `operator` | `OR` (default) or `AND` | Controls how multiple terms are combined when no explicit boolean operator is supplied. | `SELECT id FROM frames WHERE QUERY('meta.scene.weather:rain fog', 'operator=AND');` |
| `lenient` | `true` or `false` | Suppresses parsing errors and returns an empty result set when `true`. | `SELECT id FROM frames WHERE QUERY('meta.detections.label:()', 'lenient=true');` |

## Examples

### Set Up a Smart-Driving Dataset

```sql
CREATE OR REPLACE TABLE frames (
  id INT,
  meta VARIANT,
  INVERTED INDEX idx_meta (meta)
);

INSERT INTO frames VALUES
  (1, '{
         "frame":{"source":"dashcam_front","timestamp":"2025-10-21T08:32:05Z","location":{"city":"San Francisco","intersection":"Market & 5th","gps":[37.7825,-122.4072]}},
         "vehicle":{"speed_kmh":48,"acceleration":0.8,"lane":"center"},
         "signals":{"traffic_light":"green","distance_m":55,"speed_limit_kmh":50},
         "detections":[
           {"label":"car","confidence":0.96,"distance_m":15,"relative_speed_kmh":2},
           {"label":"pedestrian","confidence":0.88,"distance_m":12,"intent":"crossing"}
         ],
         "scene":{"weather":"clear","time_of_day":"day","visibility":"good"},
         "tags":["downtown","commute","green-light"],
         "model":"perception-net-v5"
       }'),
  (2, '{
         "frame":{"source":"dashcam_front","timestamp":"2025-10-21T08:32:06Z","location":{"city":"San Francisco","intersection":"Mission & 6th","gps":[37.7829,-122.4079]}},
         "vehicle":{"speed_kmh":9,"acceleration":-1.1,"lane":"center"},
         "signals":{"traffic_light":"red","distance_m":18,"speed_limit_kmh":40},
         "detections":[
           {"label":"traffic_light","state":"red","confidence":0.99,"distance_m":18},
           {"label":"bike","confidence":0.82,"distance_m":9,"relative_speed_kmh":3}
         ],
         "scene":{"weather":"clear","time_of_day":"day","visibility":"good"},
         "tags":["stop","cyclist","urban"],
         "model":"perception-net-v5"
       }'),
  (3, '{
         "frame":{"source":"dashcam_front","timestamp":"2025-10-21T08:32:07Z","location":{"city":"San Francisco","intersection":"SOMA School Zone","gps":[37.7808,-122.4016]}},
         "vehicle":{"speed_kmh":28,"acceleration":0.2,"lane":"right"},
         "signals":{"traffic_light":"yellow","distance_m":32,"speed_limit_kmh":25},
         "detections":[
           {"label":"traffic_sign","text":"SCHOOL","confidence":0.91,"distance_m":25},
           {"label":"pedestrian","confidence":0.76,"distance_m":8,"intent":"waiting"}
         ],
         "scene":{"weather":"overcast","time_of_day":"day","visibility":"moderate"},
         "tags":["school-zone","caution"],
         "model":"perception-net-v5"
       }');
```

### Example: Boolean AND

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### Example: Boolean OR

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike');
-- Returns id 2
```

### Example: IN List Matching

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]');
-- Returns id 2
```

### Example: Inclusive Range

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### Example: Exclusive Range

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}');
-- Returns id 2
```

### Example: Boost Across Fields

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0');
-- Returns id 2 with higher relevance
```

### Example: Detect High-Confidence Pedestrians

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:IN [pedestrian cyclist] AND meta.detections.confidence:[0.8 TO *]');
-- Returns ids 1 and 3
```

### Example: Filter by Phrase

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.scene.summary:"vehicle stopped at red traffic light"');
-- Returns id 2
```

### Example: School-Zone Filter

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.text:SCHOOL AND meta.scene.time_of_day:day');
-- Returns id 3
```
