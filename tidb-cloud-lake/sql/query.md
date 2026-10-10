---
title: QUERY
summary: 転置インデックスを持つカラムに対して Lucene スタイルのクエリで行をフィルタリングし、ネストされた VARIANT フィールドに対するドット記法をサポートします。
---

# QUERY

`QUERY` は、転置インデックスを持つカラムに対して Lucene スタイルのクエリ式を照合することで行をフィルタリングします。`VARIANT` カラム内のネストされたフィールドをたどるには、ドット記法を使用します。この関数は `WHERE` 句でのみ有効です。

> **Note:**
>
> {{{ .lake }}} の QUERY 関数は、Elasticsearch の [QUERY](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-query) に着想を得ています。

## 構文 {#syntax}

```sql
QUERY('<query_expr>'[, '<options>'])
```

`<options>` は省略可能な、セミコロン区切りの `key=value` ペアのリストで、検索の動作を調整します。

## クエリ式の構築 {#building-query-expressions}

| 式 | 目的 | 例 |
|------------|---------|---------|
| `column:keyword` | `column` にキーワードが含まれる行に一致します。接尾辞一致には `*` を追加します。 | `QUERY('meta.detections.label:pedestrian')` |
| `column:"exact phrase"` | 完全一致するフレーズを含む行に一致します。 | `QUERY('meta.scene.summary:"vehicle stopped at red traffic light"')` |
| `column:+required -excluded` | 同じカラム内で用語を必須または除外にします。 | `QUERY('meta.tags:+commute -cyclist')` |
| `column:term1 AND term2` / `column:term1 OR term2` | 複数の用語をブール演算子で組み合わせます。`AND` は `OR` より優先されます。 | `QUERY('meta.signals.traffic_light:red AND meta.vehicle.lane:center')` |
| `column:IN [value1 value2 ...]` | リスト内のいずれかの値に一致します。 | `QUERY('meta.tags:IN [stop urban]')` |
| `column:[min TO max]` | 境界値を含む範囲検索を実行します。片側を開放するには `*` を使用します。 | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |
| `column:{min TO max}` | 境界値を含まない範囲検索を実行します。 | `QUERY('meta.vehicle.speed_kmh:{0 TO 10}')` |
| `column:term^boost` | 特定のカラムでの一致の重みを増やします。 | `QUERY('meta.signals.traffic_light:red^1.0 meta.tags:urban^2.0')` |

### ネストされた `VARIANT` フィールド {#nested-variant-fields}

`VARIANT` カラム内の内部フィールドを指定するには、ドット記法を使用します。{{{ .lake }}} は、オブジェクトと配列をまたいでパスを評価します。

| パターン | 説明 | 例 |
|---------|-------------|---------|
| `variant_col.field:value` | 内部フィールドに一致します。 | `QUERY('meta.signals.traffic_light:red')` |
| `variant_col.field:IN [ ... ]` | 配列内のいずれかの値に一致します。 | `QUERY('meta.detections.label:IN [pedestrian cyclist]')` |
| `variant_col.field:[min TO max]` | 数値の内部フィールドに範囲検索を適用します。 | `QUERY('meta.vehicle.speed_kmh:[0 TO 10]')` |

## オプション {#options}

| オプション | 値 | 説明 | 例 |
|--------|--------|-------------|---------|
| `fuzziness` | `1` または `2` | 指定した Levenshtein 距離内の用語に一致します。 | `SELECT id FROM frames WHERE QUERY('meta.detections.label:pedestrain', 'fuzziness=1');` |
| `operator` | `OR` (default) または `AND` | 明示的なブール演算子が指定されていない場合に、複数の用語をどのように組み合わせるかを制御します。 | `SELECT id FROM frames WHERE QUERY('meta.scene.weather:rain fog', 'operator=AND');` |
| `lenient` | `true` または `false` | `true` の場合、解析エラーを抑制し、空の結果セットを返します。 | `SELECT id FROM frames WHERE QUERY('meta.detections.label:()', 'lenient=true');` |

## 例 {#examples}

### スマートドライビングのデータセットを準備する {#set-up-a-smart-driving-dataset}

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

### 例: ブール AND {#example-boolean-and}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red AND meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### 例: ブール OR {#example-boolean-or}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.signals.traffic_light:red OR meta.detections.label:bike');
-- Returns id 2
```

### 例: IN リスト一致 {#example-in-list-matching}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.tags:IN [stop urban]');
-- Returns id 2
```

### 例: 境界値を含む範囲 {#example-inclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:[0 TO 10]');
-- Returns id 2
```

### 例: 境界値を含まない範囲 {#example-exclusive-range}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.vehicle.speed_kmh:{0 TO 10}');
-- Returns id 2
```

### 例: フィールドをまたいだブースト {#example-boost-across-fields}

```sql
SELECT id, meta['frame']['timestamp'] AS ts, SCORE()
FROM frames
WHERE QUERY('meta.signals.traffic_light:red^1.0 AND meta.tags:urban^2.0');
-- Returns id 2 with higher relevance
```

### 例: 高信頼度の歩行者を検出する {#example-detect-high-confidence-pedestrians}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.label:IN [pedestrian cyclist] AND meta.detections.confidence:[0.8 TO *]');
-- Returns ids 1 and 3
```

### 例: フレーズでフィルタする {#example-filter-by-phrase}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.scene.summary:"vehicle stopped at red traffic light"');
-- Returns id 2
```

### 例: スクールゾーンフィルタ {#example-school-zone-filter}

```sql
SELECT id, meta['frame']['timestamp'] AS ts
FROM frames
WHERE QUERY('meta.detections.text:SCHOOL AND meta.scene.time_of_day:day');
-- Returns id 3
```