---
title: JSON & Search
summary: "シナリオ: CityDrive は、抽出された各フレームにメタデータ JSON ペイロードを付加します。この JSON データはバックグラウンドツールによって動画のキーフレームから抽出され、シーン認識や物体検出のような豊富な非構造化情報を含みます。これを外部システムに複製することなく、Elasticsearch スタイルの構文で {{{ .lake }}} 内の JSON をフィルタリングする必要があります。{{{ .lake }}} の外にコピーせずに JSON を扱います。"
---

# JSON & Search

> **Scenario:** CityDrive は、抽出された各フレームにメタデータ JSON ペイロードを付加します。この JSON データはバックグラウンドツールによって動画のキーフレームから抽出され、シーン認識や物体検出のような豊富な非構造化情報を含みます。これを外部システムに複製することなく、Elasticsearch スタイルの構文で {{{ .lake }}} 内の JSON をフィルタリングする必要があります。{{{ .lake }}} の外にコピーせずに JSON を扱います。

{{{ .lake }}} は、これらの異種シグナルを 1 つの warehouse に保持します。転置インデックスは VARIANT カラムに対する Elasticsearch スタイルの検索を実現し、bitmap テーブルはラベルのカバレッジを要約し、ベクトルインデックスは類似検索に応答し、ネイティブの GEOMETRY カラムは空間フィルタをサポートします。

## 1. メタデータテーブルを作成する {#1-create-the-metadata-table}

すべての検索が同じ構造に対して実行されるよう、フレームごとに 1 つの JSON ペイロードを保存します。

```sql
CREATE DATABASE IF NOT EXISTS video_unified_demo;
USE video_unified_demo;

CREATE OR REPLACE TABLE frame_metadata_catalog (
    doc_id      STRING,
    meta_json   VARIANT,
    captured_at TIMESTAMP,
    INVERTED INDEX idx_meta_json (meta_json)
);

-- Sample rows for the queries below.
INSERT INTO frame_metadata_catalog VALUES
  ('FRAME-0101', PARSE_JSON('{"scene":{"weather_code":"rain","lighting":"day"},"camera":{"sensor_view":"roof"},"vehicle":{"speed_kmh":32.4},"detections":{"objects":[{"type":"vehicle","confidence":0.88},{"type":"brake_light","confidence":0.64}]},"media_meta":{"tagging":{"labels":["hard_brake","rain","downtown_loop"]}}}'), '2025-01-01 08:15:21'),
  ('FRAME-0102', PARSE_JSON('{"scene":{"weather_code":"rain","lighting":"day"},"camera":{"sensor_view":"roof"},"vehicle":{"speed_kmh":24.8},"detections":{"objects":[{"type":"pedestrian","confidence":0.92},{"type":"bike","confidence":0.35}]},"media_meta":{"tagging":{"labels":["pedestrian","swerve","crosswalk"]}}}'), '2025-01-01 08:33:54'),
  ('FRAME-0201', PARSE_JSON('{"scene":{"weather_code":"overcast","lighting":"day"},"camera":{"sensor_view":"front"},"vehicle":{"speed_kmh":48.1},"detections":{"objects":[{"type":"lane_merge","confidence":0.74},{"type":"vehicle","confidence":0.41}]},"media_meta":{"tagging":{"labels":["lane_merge","urban"]}}}'), '2025-01-01 11:12:02'),
  ('FRAME-0301', PARSE_JSON('{"scene":{"weather_code":"clear","lighting":"day"},"camera":{"sensor_view":"front"},"vehicle":{"speed_kmh":52.6},"detections":{"objects":[{"type":"vehicle","confidence":0.82},{"type":"hard_brake","confidence":0.59}]},"media_meta":{"tagging":{"labels":["hard_brake","highway"]}}}'), '2025-01-02 09:44:18'),
  ('FRAME-0401', PARSE_JSON('{"scene":{"weather_code":"lightfog","lighting":"night"},"camera":{"sensor_view":"rear"},"vehicle":{"speed_kmh":38.9},"detections":{"objects":[{"type":"traffic_light","confidence":0.78},{"type":"vehicle","confidence":0.36}]},"media_meta":{"tagging":{"labels":["night_lowlight","traffic_light"]}}}'), '2025-01-03 21:18:07');
```

> マルチモーダルデータ（ベクトル埋め込み、GPS 軌跡、タグ bitmap）が必要ですか？ここで示した検索結果と組み合わせられるように、[Vector](/tidb-cloud-lake/guides/vector-search-guide.md) および [Geo](/tidb-cloud-lake/guides/geo-analytics.md) ガイドからスキーマを取得してください。

## 2. `QUERY()` を使った検索パターン {#2-search-patterns-with-query}

### 配列マッチ {#array-match}

```sql
SELECT doc_id,
       captured_at,
       meta_json['detections'] AS detections
FROM frame_metadata_catalog
WHERE QUERY('meta_json.detections.objects.type:pedestrian')
ORDER BY captured_at DESC
LIMIT 5;
```

出力例:

```
doc_id     | captured_at          | detections
FRAME-0102 | 2025-01-01 08:33:54 | {"objects":[{"confidence":0.92,"type":"pedestrian"},{"confidence":0.35,"type":"bike"}]}
```

### ブール AND {#boolean-and}

```sql
SELECT doc_id, captured_at
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain
             AND meta_json.camera.sensor_view:roof')
ORDER BY captured_at;
```

出力例:

```
doc_id     | captured_at
FRAME-0101 | 2025-01-01 08:15:21
FRAME-0102 | 2025-01-01 08:33:54
```

### ブール OR / リスト {#boolean-or-list}

```sql
SELECT doc_id,
       meta_json['media_meta']['tagging']['labels'] AS labels
FROM frame_metadata_catalog
WHERE QUERY('meta_json.media_meta.tagging.labels:(hard_brake OR swerve OR lane_merge)')
ORDER BY captured_at DESC
LIMIT 10;
```

出力例:

```
doc_id     | labels
FRAME-0301 | ["hard_brake","highway"]
FRAME-0201 | ["lane_merge","urban"]
FRAME-0102 | ["pedestrian","swerve","crosswalk"]
FRAME-0101 | ["hard_brake","rain","downtown_loop"]
```

### 数値範囲 {#numeric-ranges}

```sql
SELECT doc_id,
       meta_json['vehicle']['speed_kmh']::DOUBLE AS speed
FROM frame_metadata_catalog
WHERE QUERY('meta_json.vehicle.speed_kmh:{30 TO 80}')
ORDER BY speed DESC
LIMIT 10;
```

出力例:

```
doc_id     | speed
FRAME-0301 | 52.6
FRAME-0201 | 48.1
FRAME-0401 | 38.9
FRAME-0101 | 32.4
```

### ブースト {#boosting}

```sql
SELECT doc_id,
       SCORE() AS relevance
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain AND (meta_json.media_meta.tagging.labels:hard_brake^2 OR meta_json.media_meta.tagging.labels:swerve)')
ORDER BY relevance DESC
LIMIT 8;
```

出力例:

```
doc_id     | relevance
FRAME-0101 | 7.0161
FRAME-0102 | 3.6252
```

`QUERY()` は Elasticsearch のセマンティクス（ブールロジック、範囲、ブースト、リスト）に従います。`SCORE()` は Elasticsearch の関連度を公開するため、SQL 内で結果を再ランキングできます。演算子の完全な一覧については、[検索関数](/tidb-cloud-lake/sql/full-text-search-functions.md) を参照してください。