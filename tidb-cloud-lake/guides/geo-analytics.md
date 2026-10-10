---
title: Geo Analytics
summary: CityDrive は、フラグ付きフレームごとに高精度な GPS 位置情報と信号までの距離を記録します。この地理空間データはダッシュカムの GPS モジュールに由来し、動画キーフレームのタイムスタンプと正確に対応付けられています。運用チームは「これはどこで起きたのか？」という問いに、SQL だけで答えられます。
---

# Geo Analytics

> **Scenario:** CityDrive は、フラグ付きフレームごとに高精度な GPS 位置情報と信号までの距離を記録します。この地理空間データはダッシュカムの GPS モジュールに由来し、動画キーフレームのタイムスタンプと正確に対応付けられています。運用チームは「これはどこで起きたのか？」という問いに、SQL だけで答えられます。

`frame_geo_points` と `signal_contact_points` は、このガイドの他の部分と同じ `video_id`/`frame_id` キーを共有しているため、データをコピーせずに SQL メトリクスから地図へ移行できます。

## 1. 位置テーブルを作成する {#1-create-location-tables}

JSON ガイドに従っている場合、これらのテーブルはすでに存在します。以下のスニペットは、それらの構造と深圳のサンプルをいくつか示しています。

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

ドキュメント: [Geospatial types](/tidb-cloud-lake/sql/geospatial.md)。

---

## 2. 空間フィルター {#2-spatial-filters}

各フレームがダウンタウンの主要座標からどれだけ離れていたかを測定したり、ポリゴン内に含まれるかどうかを確認したりできます。メートル単位の距離が必要な場合は、SRID 3857 に変換してください。

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

出力例:

```
frame_id  | video_id         | event_tag  | meters_from_hq
FRAME-0102| VID-20250101-001 | pedestrian | 180.277138577
FRAME-0101| VID-20250101-001 | hard_brake | 324.291965923
```

Tip: デバッグ時には `ST_ASTEXT(l.geom)` を追加するか、大圏距離の計算には [`HAVERSINE`](/tidb-cloud-lake/sql/geospatial-functions.md#distance--measurements) を使用してください。

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

出力例:

```
frame_id  | video_id         | event_tag
FRAME-0101| VID-20250101-001 | hard_brake
FRAME-0102| VID-20250101-001 | pedestrian
```

---

## 3. Hex 集計 {#3-hex-aggregations}

ダッシュボード向けに、リスクの高いフレームを六角形のバケットに集計します。

```sql
SELECT GEO_TO_H3(ST_X(position_wgs84), ST_Y(position_wgs84), 8) AS h3_cell,
       COUNT(*) AS frame_count,
       AVG(f.risk_score) AS avg_risk
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
GROUP BY h3_cell
ORDER BY avg_risk DESC;
```

出力例:

```
h3_cell         | frame_count | avg_risk
613635011200942079| 1          | 0.81
613635011532292095| 1          | 0.74
613635011238690815| 1          | 0.67
613635015391051775| 1          | 0.63
613635011309993983| 1          | 0.59
```

ドキュメント: [H3 functions](/tidb-cloud-lake/sql/geospatial-functions.md#h3-indexing--conversion)。

---

## 4. 交通コンテキスト {#4-traffic-context}

`signal_contact_points` と `frame_geo_points` を結合して保存済みメトリクスを検証したり、空間述語と JSON 検索を組み合わせたりできます。

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

出力例:

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

出力例:

```
frame_id  | event_tag   | labels
FRAME-0301| hard_brake  | ["hard_brake","highway"]
```

このパターンでは、まず地理条件で絞り込み、その後で残ったフレームに対して JSON 検索を適用できます。

---

## 5. ヒートマップ ビューを公開する {#5-publish-a-heatmap-view}

重い SQL を再実行することなく、geo heatmap を BI ツールや GIS ツールに公開できます。

```sql
CREATE OR REPLACE VIEW v_citydrive_geo_heatmap AS
SELECT GEO_TO_H3(ST_X(position_wgs84), ST_Y(position_wgs84), 7) AS h3_cell,
       COUNT(*)                              AS frames,
       AVG(f.risk_score)                     AS avg_risk
FROM frame_geo_points AS l
JOIN frame_events AS f USING (frame_id)
GROUP BY h3_cell;
```

出力例:

```
h3_cell         | frames | avg_risk
609131411584057343| 1    | 0.81
609131411919601663| 1    | 0.74
609131411617611775| 1    | 0.67
609131415778361343| 1    | 0.63
609131411684720639| 1    | 0.59
```

{{{ .lake }}} は現在、まったく同じ `video_id` に対してベクトル、テキスト、空間クエリを提供できるため、調査チームは別々のパイプラインを突き合わせる必要がありません。