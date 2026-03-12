---
title: SQL Analytics
---

> **Scenario:** CityDrive stages all dash-cam records into shared relational tables. This relational data (e.g., video metadata, event tags) is extracted by background processing pipelines from keyframes of the raw dash-cam video. Analysts can then filter, join, and aggregate on the same `video_id` / `frame_id` pairs used by all downstream workloads.

This walkthrough models the relational side of that catalog and highlights practical SQL building blocks. The sample IDs here appear again in the JSON, vector, geo, and ETL guides.

## 1. Create the Base Tables
`citydrive_videos` stores clip metadata, while `frame_events` records the interesting frames pulled from each clip.

```sql
CREATE OR REPLACE TABLE citydrive_videos (
    video_id       STRING,
    vehicle_id     STRING,
    capture_date   DATE,
    route_name     STRING,
    weather        STRING,
    camera_source  STRING,
    duration_sec   INT
);

CREATE OR REPLACE TABLE frame_events (
    frame_id     STRING,
    video_id     STRING,
    frame_index  INT,
    collected_at TIMESTAMP,
    event_tag    STRING,
    risk_score   DOUBLE,
    speed_kmh    DOUBLE
);

INSERT INTO citydrive_videos VALUES
  ('VID-20250101-001', 'VEH-21', '2025-01-01', 'Downtown Loop',       'Rain',     'roof_cam', 3580),
  ('VID-20250101-002', 'VEH-05', '2025-01-01', 'Port Perimeter',      'Overcast', 'front_cam',4020),
  ('VID-20250102-001', 'VEH-21', '2025-01-02', 'Airport Connector',   'Clear',    'front_cam',3655),
  ('VID-20250103-001', 'VEH-11', '2025-01-03', 'CBD Night Sweep',     'LightFog', 'rear_cam', 3310);

INSERT INTO frame_events VALUES
  ('FRAME-0101', 'VID-20250101-001', 125, '2025-01-01 08:15:21', 'hard_brake',      0.81, 32.4),
  ('FRAME-0102', 'VID-20250101-001', 416, '2025-01-01 08:33:54', 'pedestrian',      0.67, 24.8),
  ('FRAME-0201', 'VID-20250101-002', 298, '2025-01-01 11:12:02', 'lane_merge',      0.74, 48.1),
  ('FRAME-0301', 'VID-20250102-001', 188, '2025-01-02 09:44:18', 'hard_brake',      0.59, 52.6),
  ('FRAME-0401', 'VID-20250103-001', 522, '2025-01-03 21:18:07', 'night_lowlight',  0.63, 38.9),
  -- Deliberate orphan to illustrate NOT EXISTS
  ('FRAME-0501', 'VID-MISSING-001', 10, '2025-01-04 10:00:00', 'sensor_fault',     0.25, 15.0);

-- Needed for the JOIN patterns below; same schema as the JSON & Search guide.
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

Docs: [CREATE TABLE](/sql/sql-commands/ddl/table/ddl-create-table), [INSERT](/sql/sql-commands/dml/dml-insert).

---

## 2. Filter the Working Set
Keep investigations focused on the Jan 1–3 snapshot from the seed data so the demo always returns rows.

```sql
WITH recent_videos AS (
    SELECT *
    FROM citydrive_videos
    WHERE capture_date >= '2025-01-01'
      AND capture_date < '2025-01-04'
)
SELECT v.video_id,
       v.route_name,
       v.weather,
       COUNT(f.frame_id) AS flagged_frames
FROM recent_videos v
LEFT JOIN frame_events f USING (video_id)
GROUP BY v.video_id, v.route_name, v.weather
ORDER BY flagged_frames DESC;
```

Docs: [DATEADD](/sql/sql-functions/datetime-functions/date-add), [GROUP BY](/sql/sql-commands/query-syntax/query-select#group-by-clause).

Sample output:

```
video_id        | route_name         | weather   | flagged_frames
VID-20250101-001| Downtown Loop      | Rain      | 2
VID-20250101-002| Port Perimeter     | Overcast  | 1
VID-20250102-001| Airport Connector  | Clear     | 1
VID-20250103-001| CBD Night Sweep    | LightFog  | 1
```

---

## 3. JOIN Patterns
### INNER JOIN for frame context
```sql
SELECT f.frame_id,
       f.event_tag,
       f.risk_score,
       v.route_name,
       v.camera_source
FROM frame_events AS f
JOIN citydrive_videos AS v USING (video_id)
ORDER BY f.collected_at;
```

Sample output:

```
frame_id  | event_tag      | risk_score | route_name        | camera_source
FRAME-0101| hard_brake     | 0.81       | Downtown Loop     | roof_cam
FRAME-0102| pedestrian     | 0.67       | Downtown Loop     | roof_cam
FRAME-0201| lane_merge     | 0.74       | Port Perimeter    | front_cam
FRAME-0301| hard_brake     | 0.59       | Airport Connector | front_cam
FRAME-0401| night_lowlight | 0.63       | CBD Night Sweep   | rear_cam
```

### Anti join QA
```sql
SELECT frame_id
FROM frame_events f
WHERE NOT EXISTS (
    SELECT 1
    FROM citydrive_videos v
    WHERE v.video_id = f.video_id
);
```

Sample output:

```
frame_id
FRAME-0501
```

### LATERAL FLATTEN for nested detections
```sql
SELECT f.frame_id,
       obj.value['type']::STRING AS detected_type,
       obj.value['confidence']::DOUBLE AS confidence
FROM frame_events AS f
JOIN frame_metadata_catalog AS meta ON meta.doc_id = f.frame_id,
     LATERAL FLATTEN(input => meta.meta_json['detections']['objects']) AS obj
WHERE f.event_tag = 'pedestrian'
ORDER BY confidence DESC;
```

Sample output:

```
frame_id  | detected_type | confidence
FRAME-0102| pedestrian    | 0.92
FRAME-0102| bike          | 0.35
```

Docs: [JOIN](/sql/sql-commands/query-syntax/query-join), [FLATTEN](/sql/sql-functions/table-functions/flatten).

---

## 4. Aggregations for Fleet KPIs
### Behaviour by route
```sql
SELECT v.route_name,
       f.event_tag,
       COUNT(*) AS occurrences,
       AVG(f.risk_score) AS avg_risk
FROM frame_events f
JOIN citydrive_videos v USING (video_id)
GROUP BY v.route_name, f.event_tag
ORDER BY avg_risk DESC, occurrences DESC;
```

Sample output:

```
route_name         | event_tag      | occurrences | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
Port Perimeter     | lane_merge     | 1           | 0.74
Downtown Loop      | pedestrian     | 1           | 0.67
CBD Night Sweep    | night_lowlight | 1           | 0.63
Airport Connector  | hard_brake     | 1           | 0.59
```

### ROLLUP totals
```sql
SELECT v.route_name,
       f.event_tag,
       COUNT(*) AS occurrences
FROM frame_events f
JOIN citydrive_videos v USING (video_id)
GROUP BY ROLLUP(v.route_name, f.event_tag)
ORDER BY v.route_name NULLS LAST, f.event_tag;
```

Sample output (first 6 rows):

```
route_name         | event_tag      | occurrences
Airport Connector  | hard_brake     | 1
Airport Connector  | NULL           | 1
CBD Night Sweep    | night_lowlight | 1
CBD Night Sweep    | NULL           | 1
Downtown Loop      | hard_brake     | 1
Downtown Loop      | pedestrian     | 1
... (total rows: 10)
```

### CUBE for route × weather coverage
```sql
SELECT v.route_name,
       v.weather,
       COUNT(DISTINCT v.video_id) AS videos
FROM citydrive_videos v
GROUP BY CUBE(v.route_name, v.weather)
ORDER BY v.route_name NULLS LAST, v.weather NULLS LAST;
```

Sample output (first 6 rows):

```
route_name         | weather  | videos
Airport Connector  | Clear    | 1
Airport Connector  | NULL     | 1
CBD Night Sweep    | LightFog | 1
CBD Night Sweep    | NULL     | 1
Downtown Loop      | Rain     | 1
Downtown Loop      | NULL     | 1
... (total rows: 13)
```

---

## 5. Window Functions
### Running risk per video
```sql
WITH ordered_events AS (
    SELECT video_id, collected_at, risk_score
    FROM frame_events
)
SELECT video_id,
       collected_at,
       risk_score,
       SUM(risk_score) OVER (
         PARTITION BY video_id
         ORDER BY collected_at
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_risk
FROM ordered_events
ORDER BY video_id, collected_at;
```

Sample output (first 6 rows):

```
video_id        | collected_at         | risk_score | cumulative_risk
VID-20250101-001| 2025-01-01 08:15:21  | 0.81       | 0.81
VID-20250101-001| 2025-01-01 08:33:54  | 0.67       | 1.48
VID-20250101-002| 2025-01-01 11:12:02  | 0.74       | 0.74
VID-20250102-001| 2025-01-02 09:44:18  | 0.59       | 0.59
VID-20250103-001| 2025-01-03 21:18:07  | 0.63       | 0.63
VID-MISSING-001 | 2025-01-04 10:00:00  | 0.25       | 0.25
```

### Rolling average over recent frames
```sql
SELECT video_id,
       frame_id,
       frame_index,
       risk_score,
       AVG(risk_score) OVER (
         PARTITION BY video_id
         ORDER BY frame_index
         ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
       ) AS rolling_avg_risk
FROM frame_events
ORDER BY video_id, frame_index;
```

Sample output (first 6 rows):

```
video_id        | frame_id   | frame_index | risk_score | rolling_avg_risk
VID-20250101-001| FRAME-0101 | 125         | 0.81       | 0.81
VID-20250101-001| FRAME-0102 | 416         | 0.67       | 0.74
VID-20250101-002| FRAME-0201 | 298         | 0.74       | 0.74
VID-20250102-001| FRAME-0301 | 188         | 0.59       | 0.59
VID-20250103-001| FRAME-0401 | 522         | 0.63       | 0.63
VID-MISSING-001 | FRAME-0501 | 10          | 0.25       | 0.25
```

Docs: [Window functions](/sql/sql-functions/window-functions).

---

## 6. Aggregating Index Boost
Persist frequently used summaries for dashboards.

```sql
CREATE OR REPLACE AGGREGATING INDEX idx_video_event_summary
AS
SELECT video_id,
       event_tag,
       COUNT(*)        AS event_count,
       AVG(risk_score) AS avg_risk
FROM frame_events
GROUP BY video_id, event_tag;
```

When analysts rerun a familiar KPI, the optimizer serves it from the index:

```sql
SELECT v.route_name,
       e.event_tag,
       COUNT(*)        AS event_count,
       AVG(e.risk_score) AS avg_risk
FROM frame_events e
JOIN citydrive_videos v USING (video_id)
WHERE v.capture_date >= '2025-01-01'
GROUP BY v.route_name, e.event_tag
ORDER BY avg_risk DESC;
```

Sample output:

```
route_name         | event_tag      | event_count | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
Port Perimeter     | lane_merge     | 1           | 0.74
Downtown Loop      | pedestrian     | 1           | 0.67
CBD Night Sweep    | night_lowlight | 1           | 0.63
Airport Connector  | hard_brake     | 1           | 0.59
```

Docs: [Aggregating Index](/guides/performance/aggregating-index) and [EXPLAIN](/sql/sql-commands/explain-cmds/explain).

---

## 7. Stored Procedure Automation
Wrap the logic so scheduled jobs always produce the same report.

```sql
CREATE OR REPLACE PROCEDURE citydrive_route_report(days_back UINT8)
RETURNS TABLE(route_name STRING, event_tag STRING, event_count BIGINT, avg_risk DOUBLE)
LANGUAGE SQL
AS
$$
BEGIN
  RETURN TABLE (
    SELECT v.route_name,
           e.event_tag,
           COUNT(*)          AS event_count,
           AVG(e.risk_score) AS avg_risk
    FROM frame_events e
    JOIN citydrive_videos v USING (video_id)
    WHERE v.capture_date >= DATEADD('day', -:days_back, DATE '2025-01-04')
    GROUP BY v.route_name, e.event_tag
  );
END;
$$;

CALL PROCEDURE citydrive_route_report(30);
```

Sample output:

```
route_name         | event_tag      | event_count | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
CBD Night Sweep    | night_lowlight | 1           | 0.63
Downtown Loop      | pedestrian     | 1           | 0.67
Airport Connector  | hard_brake     | 1           | 0.59
Port Perimeter     | lane_merge     | 1           | 0.74
```

Stored procedures can be triggered manually, via [TASKS](/guides/load-data/continuous-data-pipelines/task), or from orchestration tools.

---

With these tables and patterns in place, the rest of the CityDrive guides can reference the exact same `video_id` keys—`frame_metadata_catalog` for JSON search, frame embeddings for similarity, GPS locations for geo queries, and a single ETL path to keep them synchronized.
