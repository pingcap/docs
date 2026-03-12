---
title: JSON & Search
---

> **Scenario:** CityDrive attaches a metadata JSON payload to every extracted frame. This JSON data is extracted from video keyframes by background tools, containing rich unstructured information like scene recognition and object detection. We need to filter this JSON in Databend with Elasticsearch-style syntax without replicating it to an external system. JSON without copying it out of Databend.

Databend keeps these heterogeneous signals in one warehouse. Inverted indexes power Elasticsearch-style search on VARIANT columns, bitmap tables summarize label coverage, vector indexes answer similarity lookups, and native GEOMETRY columns support spatial filters.

## 1. Create the Metadata Table
Store one JSON payload per frame so every search runs against the same structure.

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

> Need multimodal data (vector embeddings, GPS trails, tag bitmaps)? Grab the schemas from the [Vector](./02-vector-db.md) and [Geo](./03-geo-analytics.md) guides so you can combine them with the search results shown here.

## 2. Search Patterns with `QUERY()`
### Array Match
```sql
SELECT doc_id,
       captured_at,
       meta_json['detections'] AS detections
FROM frame_metadata_catalog
WHERE QUERY('meta_json.detections.objects.type:pedestrian')
ORDER BY captured_at DESC
LIMIT 5;
```

Sample output:

```
doc_id     | captured_at          | detections
FRAME-0102 | 2025-01-01 08:33:54 | {"objects":[{"confidence":0.92,"type":"pedestrian"},{"confidence":0.35,"type":"bike"}]}
```

### Boolean AND
```sql
SELECT doc_id, captured_at
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain
             AND meta_json.camera.sensor_view:roof')
ORDER BY captured_at;
```

Sample output:

```
doc_id     | captured_at
FRAME-0101 | 2025-01-01 08:15:21
FRAME-0102 | 2025-01-01 08:33:54
```

### Boolean OR / List
```sql
SELECT doc_id,
       meta_json['media_meta']['tagging']['labels'] AS labels
FROM frame_metadata_catalog
WHERE QUERY('meta_json.media_meta.tagging.labels:(hard_brake OR swerve OR lane_merge)')
ORDER BY captured_at DESC
LIMIT 10;
```

Sample output:

```
doc_id     | labels
FRAME-0301 | ["hard_brake","highway"]
FRAME-0201 | ["lane_merge","urban"]
FRAME-0102 | ["pedestrian","swerve","crosswalk"]
FRAME-0101 | ["hard_brake","rain","downtown_loop"]
```

### Numeric Ranges
```sql
SELECT doc_id,
       meta_json['vehicle']['speed_kmh']::DOUBLE AS speed
FROM frame_metadata_catalog
WHERE QUERY('meta_json.vehicle.speed_kmh:{30 TO 80}')
ORDER BY speed DESC
LIMIT 10;
```

Sample output:

```
doc_id     | speed
FRAME-0301 | 52.6
FRAME-0201 | 48.1
FRAME-0401 | 38.9
FRAME-0101 | 32.4
```

### Boosting
```sql
SELECT doc_id,
       SCORE() AS relevance
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain AND (meta_json.media_meta.tagging.labels:hard_brake^2 OR meta_json.media_meta.tagging.labels:swerve)')
ORDER BY relevance DESC
LIMIT 8;
```

Sample output:

```
doc_id     | relevance
FRAME-0101 | 7.0161
FRAME-0102 | 3.6252
```

`QUERY()` follows Elasticsearch semantics (boolean logic, ranges, boosts, lists). `SCORE()` exposes the Elasticsearch relevance so you can re-rank results inside SQL. See [Search functions](/sql/sql-functions/search-functions) for the full operator list.
