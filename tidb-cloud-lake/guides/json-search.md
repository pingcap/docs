---
title: JSON & Search
summary: 在场景 CityDrive 中，每个提取出的帧都会附带一个元信息 JSON 负载。这些 JSON 数据由后台工具从视频关键帧中提取，包含场景识别、目标检测等丰富的非结构化信息。我们需要在 {{{ .lake }}} 中使用 Elasticsearch 风格的语法过滤这些 JSON，而无需将其复制到外部系统。JSON 无需从 {{{ .lake }}} 中导出。
---

# JSON & Search

> **场景：** CityDrive 为每个提取出的帧附加一个元信息 JSON 负载。这些 JSON 数据由后台工具从视频关键帧中提取，包含场景识别、目标检测等丰富的非结构化信息。我们需要在 {{{ .lake }}} 中使用 Elasticsearch 风格的语法过滤这些 JSON，而无需将其复制到外部系统。JSON 无需从 {{{ .lake }}} 中导出。

{{{ .lake }}} 将这些异构信号保存在同一个仓库中。倒排索引为 VARIANT 列提供 Elasticsearch 风格的搜索，位图表汇总标签覆盖情况，向量索引支持相似性查找，原生 GEOMETRY 列支持空间过滤。

## 1. 创建元信息表 {#1-create-the-metadata-table}

为每一帧存储一个 JSON 负载，这样每次搜索都基于相同的结构执行。

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

> 需要多模态数据（向量嵌入、GPS 轨迹、标签位图）？可以从 [向量](/tidb-cloud-lake/guides/vector-search-guide.md) 和 [地理空间](/tidb-cloud-lake/guides/geo-analytics.md) 指南中获取表结构，以便将它们与此处展示的搜索结果结合使用。

## 2. 使用 `QUERY()` 的搜索模式 {#2-search-patterns-with-query}

### 数组匹配 {#array-match}

```sql
SELECT doc_id,
       captured_at,
       meta_json['detections'] AS detections
FROM frame_metadata_catalog
WHERE QUERY('meta_json.detections.objects.type:pedestrian')
ORDER BY captured_at DESC
LIMIT 5;
```

示例输出：

```
doc_id     | captured_at          | detections
FRAME-0102 | 2025-01-01 08:33:54 | {"objects":[{"confidence":0.92,"type":"pedestrian"},{"confidence":0.35,"type":"bike"}]}
```

### 布尔 AND {#boolean-and}

```sql
SELECT doc_id, captured_at
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain
             AND meta_json.camera.sensor_view:roof')
ORDER BY captured_at;
```

示例输出：

```
doc_id     | captured_at
FRAME-0101 | 2025-01-01 08:15:21
FRAME-0102 | 2025-01-01 08:33:54
```

### 布尔 OR / 列表 {#boolean-or-list}

```sql
SELECT doc_id,
       meta_json['media_meta']['tagging']['labels'] AS labels
FROM frame_metadata_catalog
WHERE QUERY('meta_json.media_meta.tagging.labels:(hard_brake OR swerve OR lane_merge)')
ORDER BY captured_at DESC
LIMIT 10;
```

示例输出：

```
doc_id     | labels
FRAME-0301 | ["hard_brake","highway"]
FRAME-0201 | ["lane_merge","urban"]
FRAME-0102 | ["pedestrian","swerve","crosswalk"]
FRAME-0101 | ["hard_brake","rain","downtown_loop"]
```

### 数值范围 {#numeric-ranges}

```sql
SELECT doc_id,
       meta_json['vehicle']['speed_kmh']::DOUBLE AS speed
FROM frame_metadata_catalog
WHERE QUERY('meta_json.vehicle.speed_kmh:{30 TO 80}')
ORDER BY speed DESC
LIMIT 10;
```

示例输出：

```
doc_id     | speed
FRAME-0301 | 52.6
FRAME-0201 | 48.1
FRAME-0401 | 38.9
FRAME-0101 | 32.4
```

### Boosting {#boosting}

```sql
SELECT doc_id,
       SCORE() AS relevance
FROM frame_metadata_catalog
WHERE QUERY('meta_json.scene.weather_code:rain AND (meta_json.media_meta.tagging.labels:hard_brake^2 OR meta_json.media_meta.tagging.labels:swerve)')
ORDER BY relevance DESC
LIMIT 8;
```

示例输出：

```
doc_id     | relevance
FRAME-0101 | 7.0161
FRAME-0102 | 3.6252
```

`QUERY()` 遵循 Elasticsearch 语义（布尔逻辑、范围、boost、列表）。`SCORE()` 会暴露 Elasticsearch 的相关性分数，因此你可以在 SQL 内部对结果重新排序。完整的运算符列表，请参见[搜索函数](/tidb-cloud-lake/sql/full-text-search-functions.md)。