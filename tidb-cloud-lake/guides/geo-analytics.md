---
title: 地理空间分析
summary: CityDrive 会为每个已标记帧记录精确的 GPS 位置以及到信号源的距离。这些地理空间数据来自行车记录仪的 GPS 模块，并与视频关键帧的时间戳精确对齐。运维团队仅通过 SQL 就能回答“这件事发生在哪里？”。
---

# 地理空间分析

> **场景：** CityDrive 会为每个已标记帧记录精确的 GPS 位置以及到信号源的距离。这些地理空间数据来自行车记录仪的 GPS 模块，并与视频关键帧的时间戳精确对齐。运维团队仅通过 SQL 就能回答“这件事发生在哪里？”。

`frame_geo_points` 和 `signal_contact_points` 与本指南其余部分使用相同的 `video_id`/`frame_id` 键，因此你可以直接从 SQL 指标切换到地图，而无需复制数据。

## 1. 创建位置表 {#1-create-location-tables}

如果你已经完成 JSON 指南中的步骤，这些表已经存在。下面的代码片段展示了它们的结构以及一些深圳样例数据。

```sql
CREATE OR REPLACE TABLE frame_geo_points (
    video_id   STRING,
    frame_id   STRING,
    position_wgs84 GEOMETRY,
    solution_grade INT,
    source_system STRING,
    created_at TIMESTAMP
);

INSERT INTO frame_geo_points VALUES
  ('VID-20250101-001','FRAME-0101',TO_GEOMETRY('SRID=4326;POINT(114.0579123456789 22.543123456789)'),104,'fusion_gnss','2025-01-01 08:15:21'),
  ('VID-20250101-001','FRAME-0102',TO_GEOMETRY('SRID=4326;POINT(114.0610987654321 22.546098765432)'),104,'fusion_gnss','2025-01-01 08:33:54'),
  ('VID-20250101-002','FRAME-0201',TO_GEOMETRY('SRID=4326;POINT(114.104012345678 22.559456789012)'),104,'fusion_gnss','2025-01-01 11:12:02'),
  ('VID-20250102-001','FRAME-0301',TO_GEOMETRY('SRID=4326;POINT(114.082265432109 22.53687654321)'),104,'fusion_gnss','2025-01-02 09:44:18'),
  ('VID-20250103-001','FRAME-0401',TO_GEOMETRY('SRID=4326;POINT(114.119501234567 22.544365432101)'),104,'fusion_gnss','2025-01-03 21:18:07');

CREATE OR REPLACE TABLE signal_contact_points (
    node_id     STRING,
    signal_position GEOMETRY,
    video_id    STRING,
    frame_id    STRING,
    frame_position GEOMETRY,
    distance_m  DOUBLE,
    created_at  TIMESTAMP
);

INSERT INTO signal_contact_points VALUES
  ('SIG-0001', TO_GEOMETRY('SRID=4326;POINT(114.058500123456 22.543800654321)'), 'VID-20250101-001', 'FRAME-0101', TO_GEOMETRY('SRID=4326;POINT(114.0579123456789 22.543123456789)'), 0.012345, '2025-01-01 08:15:30'),
  ('SIG-0002', TO_GEOMETRY('SRID=4326;POINT(114.118900987654 22.544800123456)'), 'VID-20250103-001', 'FRAME-0401', TO_GEOMETRY('SRID=4326;POINT(114.119501234567 22.544365432101)'), 0.008765, '2025-01-03 21:18:20');

-- Frames and JSON tables these queries join against (same rows as SQL & Search guides).
CREATE OR REPLACE TABLE frame_events (
    frame_id     STRING,
    video_id     STRING,
    frame_index  INT,
    collected_at TIMESTAMP,
    event_tag    STRING,
    risk_score   DOUBLE,
    speed_kmh    DOUBLE
);

INSERT INTO frame_events VALUES
  ('FRAME-0101', 'VID-20250101-001', 125, '2025-01-01 08:15:21', 'hard_brake',      0.81, 32.4),
  ('FRAME-0102', 'VID-20250101-001', 416, '2025-01-01 08:33:54', 'pedestrian',      0.67, 24.8),
  ('FRAME-0201', 'VID-20250101-002', 298, '2025-01-01 11:12:02', 'lane_merge',      0.74, 48.1),
  ('FRAME-0301', 'VID-20250102-001', 188, '2025-01-02 09:44:18', 'hard_brake',      0.59, 52.6),
  ('FRAME-0401', 'VID-20250103-001', 522, '2025-01-03 21:18:07', 'night_lowlight',  0.63, 38.9),
  ('FRAME-0501', 'VID-MISSING-001', 10, '2025-01-04 10:00:00', 'sensor_fault',     0.25, 15.0);

CREATE OR REPLACE TABLE frame_metadata_catalog (
    doc_id      STRING,
    meta_json   VARIANT,
    captured_at TIMESTAMP,
    INVERTED INDEX idx_meta_json (meta_json)
);

INSERT INTO frame_metadata_catalog VALUES
  ('FRAME-0101', PARSE_JSON('{"scene":{"weather_code":"rain","lighting":"day"},"camera":{"sensor_view":"roof"},"vehicle":{"speed_kmh":32.4},"detections":{"objects":[{"type":"vehicle","confidence":0.88},{"type":"brake_light","confidence":0.64}]},"media_meta":{"tagging":{"labels":["hard_brake","rain","downtown_loop"]}}}'), '2025-01-01 08:15:21'),
  ('FRAME-0102', PARSE_JSON('{"scene":{"weather_code":"rain","lighting":"day"},"camera":{"sensor_view":"roof"},"vehicle":{"speed_kmh":24.8},"detections":{"objects":[{"type":"pedestrian","confidence":0.92},{"type":"bike","confidence":0.35}]},"media_meta":{"tagging":{"labels":["pedestrian","swerve","crosswalk"]}}}'), '2025-01-01 08:33:54'),
  ('FRAME-0201', PARSE_JSON('{"scene":{"weather_code":"overcast","lighting":"day"},"camera":{"sensor_view":"front"},"vehicle":{"speed_kmh":48.1},"detections":{"objects":[{"type":"lane_merge","confidence":0.74},{"type":"vehicle","confidence":0.41}]},"media_meta":{"tagging":{"labels":["lane_merge","urban"]}}}'), '2025-01-01 11:12:02'),
  ('FRAME-0301', PARSE_JSON('{"scene":{"weather_code":"clear","lighting":"day"},"camera":{"sensor_view":"front"},"vehicle":{"speed_kmh":52.6},"detections":{"objects":[{"type":"vehicle","confidence":0.82},{"type":"hard_brake","confidence":0.59}]},"media_meta":{"tagging":{"labels":["hard_brake","highway"]}}}'), '2025-01-02 09:44:18'),
  ('FRAME-0401', PARSE_JSON('{"scene":{"weather_code":"lightfog","lighting":"night"},"camera":{"sensor_view":"rear"},"vehicle":{"speed_kmh":38.9},"detections":{"objects":[{"type":"traffic_light","confidence":0.78},{"type":"vehicle","confidence":0.36}]},"media_meta":{"tagging":{"labels":["night_lowlight","traffic_light"]}}}'), '2025-01-03 21:18:07');
```

文档：[地理空间类型](/tidb-cloud-lake/sql/geospatial.md)。

---

## 2. 空间过滤 {#2-spatial-filters}

你可以测量每个帧与市中心某个关键坐标点之间的距离，或者检查它是否落在某个多边形内部。当你需要米级距离时，请转换为 SRID 3857。

```sql
SELECT l.frame_id,
       l.video_id,
       f.event_tag,
       ST_DISTANCE(
         ST_TRANSFORM(l.position_wgs84, 3857),
         ST_TRANSFORM(TO_GEOMETRY('SRID=4326;POINT(114.0600 22.5450)'), 3857)
       ) AS meters_from_hq
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
WHERE ST_DISTANCE(
        ST_TRANSFORM(l.position_wgs84, 3857),
        ST_TRANSFORM(TO_GEOMETRY('SRID=4326;POINT(114.0600 22.5450)'), 3857)
      ) <= 400
ORDER BY meters_from_hq;
```

示例输出：

```
frame_id  | video_id         | event_tag  | meters_from_hq
FRAME-0102| VID-20250101-001 | pedestrian | 180.277138577
FRAME-0101| VID-20250101-001 | hard_brake | 324.291965923
```

提示：调试时可以添加 `ST_ASTEXT(l.geom)`，或者切换到 [`HAVERSINE`](/tidb-cloud-lake/sql/geospatial-functions.md#distance--measurements) 来进行大圆距离计算。

```sql
WITH school_zone AS (
    SELECT TO_GEOMETRY('SRID=4326;POLYGON((
        114.0505 22.5500,
        114.0630 22.5500,
        114.0630 22.5420,
        114.0505 22.5420,
        114.0505 22.5500
    ))') AS poly
)
SELECT l.frame_id,
       l.video_id,
       f.event_tag
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
CROSS JOIN school_zone
WHERE ST_CONTAINS(poly, l.position_wgs84);
```

示例输出：

```
frame_id  | video_id         | event_tag
FRAME-0101| VID-20250101-001 | hard_brake
FRAME-0102| VID-20250101-001 | pedestrian
```

---

## 3. 六边形聚合 {#3-hex-aggregations}

将高风险帧聚合到六边形存储桶中，以便用于仪表板展示。

```sql
SELECT GEO_TO_H3(ST_X(position_wgs84), ST_Y(position_wgs84), 8) AS h3_cell,
       COUNT(*) AS frame_count,
       AVG(f.risk_score) AS avg_risk
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
GROUP BY h3_cell
ORDER BY avg_risk DESC;
```

示例输出：

```
h3_cell         | frame_count | avg_risk
613635011200942079| 1          | 0.81
613635011532292095| 1          | 0.74
613635011238690815| 1          | 0.67
613635015391051775| 1          | 0.63
613635011309993983| 1          | 0.59
```

文档：[H3 函数](/tidb-cloud-lake/sql/geospatial-functions.md#h3-indexing--conversion)。

---

## 4. 交通上下文 {#4-traffic-context}

将 `signal_contact_points` 与 `frame_geo_points` 进行关联，以验证已存储的指标，或将空间谓词与 JSON 搜索结合使用。

```sql
SELECT t.node_id,
       t.video_id,
       t.frame_id,
       ST_DISTANCE(t.signal_position, t.frame_position) AS recomputed_distance,
       t.distance_m AS stored_distance,
       l.source_system
FROM signal_contact_points AS t
JOIN frame_geo_points AS l USING (frame_id)
WHERE t.distance_m < 0.03  -- roughly < 30 meters depending on SRID
ORDER BY t.distance_m;
```

示例输出：

```
node_id | video_id         | frame_id  | recomputed_distance | stored_distance | source_system
SIG-0002| VID-20250103-001 | FRAME-0401| 0.000741116         | 0.008765        | fusion_gnss
SIG-0001| VID-20250101-001 | FRAME-0101| 0.000896705         | 0.012345        | fusion_gnss
```

```sql
WITH near_junction AS (
    SELECT frame_id
    FROM frame_geo_points
    WHERE ST_DISTANCE(
            ST_TRANSFORM(position_wgs84, 3857),
            ST_TRANSFORM(TO_GEOMETRY('SRID=4326;POINT(114.0830 22.5370)'), 3857)
          ) <= 200
)
SELECT f.frame_id,
       f.event_tag,
       meta.meta_json['media_meta']['tagging']['labels'] AS labels
FROM near_junction nj
JOIN frame_events AS f USING (frame_id)
JOIN frame_metadata_catalog AS meta
  ON meta.doc_id = nj.frame_id
WHERE QUERY('meta_json.media_meta.tagging.labels:hard_brake');
```

示例输出：

```
frame_id  | event_tag   | labels
FRAME-0301| hard_brake  | ["hard_brake","highway"]
```

这种模式允许你先按地理位置进行过滤，再对筛选后保留下来的帧应用 JSON 搜索。

---

## 5. 发布热力图视图 {#5-publish-a-heatmap-view}

将地理热力图暴露给 BI 或 GIS 工具，而无需重新运行高开销 SQL。

```sql
CREATE OR REPLACE VIEW v_citydrive_geo_heatmap AS
SELECT GEO_TO_H3(ST_X(position_wgs84), ST_Y(position_wgs84), 7) AS h3_cell,
       COUNT(*)                              AS frames,
       AVG(f.risk_score)                     AS avg_risk
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
GROUP BY h3_cell;
```

示例输出：

```
h3_cell         | frames | avg_risk
609131411584057343| 1    | 0.81
609131411919601663| 1    | 0.74
609131411617611775| 1    | 0.67
609131415778361343| 1    | 0.63
609131411684720639| 1    | 0.59
```

{{{ .lake }}} 现在可以基于完全相同的 `video_id` 同时提供向量、文本和空间查询，因此调查团队再也不需要在不同的数据处理管道之间进行对账。