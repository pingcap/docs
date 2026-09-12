---
title: QUERY
summary: 使用 Lucene 风格的查询对具有倒排索引的列进行行过滤，并支持对嵌套 `VARIANT` 字段使用点表示法。
---

# QUERY

`QUERY` 通过将 Lucene 风格的查询表达式与具有倒排索引的列进行匹配来过滤行。使用点表示法可以访问 `VARIANT` 列中的嵌套字段。该函数仅在 `WHERE` 子句中有效。

> **Note:**
>
> {{{ .lake }}} 的 QUERY 函数受 Elasticsearch 的 [QUERY](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-query) 启发。

## 语法 {#syntax}

```sql
QUERY('<query_expr>'[, '<options>'])
```

`<options>` 是可选的、以分号分隔的 `key=value` 对列表，用于调整搜索的工作方式。

## 构建查询表达式 {#building-query-expressions}

| 表达式 | 用途 | 示例 |
|------------|---------|---------|
| `column:keyword` | 匹配 `column` 包含该关键字的行。追加 `*` 可进行后缀匹配。 | `QUERY('meta.detections.label:pedestrian')` |
| `column:"exact phrase"` | 匹配包含该精确短语的行。 | `QUERY('meta.scene.summary:"vehicle stopped at red traffic light"')` |
| `column:+required -excluded` | 在同一列中要求包含或排除某些词项。 | `QUERY('meta.tags:+commute -cyclist')` |
| `column:term1 AND term2` / `column:term1 OR term2` | 使用布尔运算符组合多个词项。`AND` 的优先级高于 `OR`。 | `QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')` |
| `column:IN [value1 value2 ...]` | 匹配列表中的任意值。 | `QUERY('meta.tags:IN [stop urban]')` |
| `column:[min TO max]` | 执行包含边界的范围搜索。使用 `*` 可使一侧保持开放。 | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |
| `column:{min TO max}` | 执行不包含边界值的范围搜索。 | `QUERY('meta.vehicle.speed_kmh:{0 TO 10}')` |
| `column:term^boost` | 提高特定列中匹配结果的权重。 | `QUERY('meta.signals.traffic_light:red^1.0 meta.tags:urban^2.0')` |

### 嵌套 `VARIANT` 字段 {#nested-variant-fields}

使用点表示法来访问 `VARIANT` 列中的内部字段。{{{ .lake }}} 会在对象和数组中对该路径进行求值。

| 模式 | 描述 | 示例 |
|---------|-------------|---------|
| `variant_col.field:value` | 匹配内部字段。 | `QUERY('meta.signals.traffic_light:red')` |
| `variant_col.field:IN [ ... ]` | 匹配数组中的任意值。 | `QUERY('meta.detections.label:IN [pedestrian cyclist]')` |
| `variant_col.field:[min TO max]` | 对数值型内部字段应用范围搜索。 | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |

## 选项 {#options}

| 选项 | 值 | 描述 | 示例 |
|--------|--------|-------------|---------|
| `fuzziness` | `1` 或 `2` | 匹配与指定 Levenshtein 距离以内的词项。 | `SELECT id FROM frames WHERE QUERY('meta.detections.label:pedestrain', 'fuzziness=1');` |
| `operator` | `OR`（默认）或 `AND` | 控制在未显式提供布尔运算符时，如何组合多个词项。 | `SELECT id FROM frames WHERE QUERY('meta.scene.weather:rain fog', 'operator=AND');` |
| `lenient` | `true` 或 `false` | 当为 `true` 时，抑制解析错误并返回空结果集。 | `SELECT id FROM frames WHERE QUERY('meta.detections.label:()', 'lenient=true');` |

## 示例 {#examples}

### 建立一个智能驾驶数据集 {#set-up-a-smart-driving-dataset}

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

### 示例：布尔 AND {#example-boolean-and}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### 示例：布尔 OR {#example-boolean-or}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike');
-- Returns id 2
```

### 示例：IN 列表匹配 {#example-in-list-matching}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]');
-- Returns id 2
```

### 示例：包含边界的范围 {#example-inclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### 示例：不包含边界的范围 {#example-exclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}');
-- Returns id 2
```

### 示例：跨字段 Boost {#example-boost-across-fields}

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0');
-- Returns id 2 with higher relevance
```

### 示例：检测高置信度行人 {#example-detect-high-confidence-pedestrians}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:IN [pedestrian cyclist] AND meta.detections.confidence:[0.8 TO *]');
-- Returns ids 1 and 3
```

### 示例：按短语过滤 {#example-filter-by-phrase}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.scene.summary:"vehicle stopped at red traffic light"');
-- Returns id 2
```

### 示例：学区过滤 {#example-school-zone-filter}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.text:SCHOOL AND meta.scene.time_of_day:day');
-- Returns id 3
```