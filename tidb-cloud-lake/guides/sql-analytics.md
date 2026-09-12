---
title: SQL 分析
summary: 场景：CityDrive 将所有行车记录仪记录 stage 到共享关系型表中。这些关系型数据（例如视频元信息、事件标签）由后台处理流水线从原始行车记录仪视频的关键帧中提取而来。
---

# SQL 分析

> **场景：** CityDrive 将所有行车记录仪记录 stage 到共享关系型表中。这些关系型数据（例如视频元信息、事件标签）由后台处理流水线从原始行车记录仪视频的关键帧中提取而来。随后，分析人员可以基于所有下游工作负载共用的同一组 `video_id` / `frame_id` 对进行过滤、JOIN 和聚合。

本演练对该目录中关系型数据的一侧进行建模，并重点介绍实用的 SQL 构建模块。这里的示例 ID 也会在 JSON、向量、地理空间和 ETL 指南中再次出现。

## 1. 创建基础表 {#1-create-the-base-tables}

`citydrive_videos` 用于存储片段元信息，而 `frame_events` 用于记录从每个片段中提取出的关键帧事件。

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

文档： [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)、[INSERT](/tidb-cloud-lake/sql/insert.md)。

---

## 2. 过滤工作集 {#2-filter-the-working-set}

将分析范围限定在数据填充数据中的 1 月 1 日至 3 日快照上，以确保演示始终会返回结果行。

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

文档： [DATEADD](/tidb-cloud-lake/sql/date-add.md)、[GROUP BY](/tidb-cloud-lake/sql/select.md#group-by-clause)。

示例输出：

```
video_id        | route_name         | weather   | flagged_frames
VID-20250101-001| Downtown Loop      | Rain      | 2
VID-20250101-002| Port Perimeter     | Overcast  | 1
VID-20250102-001| Airport Connector  | Clear     | 1
VID-20250103-001| CBD Night Sweep    | LightFog  | 1
```

---

## 3. JOIN 模式 {#3-join-patterns}

### 用于帧上下文的 INNER JOIN {#inner-join-for-frame-context}

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

示例输出：

```
frame_id  | event_tag      | risk_score | route_name        | camera_source
FRAME-0101| hard_brake     | 0.81       | Downtown Loop     | roof_cam
FRAME-0102| pedestrian     | 0.67       | Downtown Loop     | roof_cam
FRAME-0201| lane_merge     | 0.74       | Port Perimeter    | front_cam
FRAME-0301| hard_brake     | 0.59       | Airport Connector | front_cam
FRAME-0401| night_lowlight | 0.63       | CBD Night Sweep   | rear_cam
```

### 用于 QA 的反连接 {#anti-join-qa}

```sql
SELECT frame_id
FROM frame_events f
WHERE NOT EXISTS (
    SELECT 1
    FROM citydrive_videos v
    WHERE v.video_id = f.video_id
);
```

示例输出：

```
frame_id
FRAME-0501
```

### 用于嵌套检测结果的 LATERAL FLATTEN {#lateral-flatten-for-nested-detections}

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

示例输出：

```
frame_id  | detected_type | confidence
FRAME-0102| pedestrian    | 0.92
FRAME-0102| bike          | 0.35
```

文档： [JOIN](/tidb-cloud-lake/sql/join.md)、[FLATTEN](/tidb-cloud-lake/sql/flatten.md)。

---

## 4. 用于车队 KPI 的聚合 {#4-aggregations-for-fleet-kpis}

### 按路线的行为 {#behaviour-by-route}

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

示例输出：

```
route_name         | event_tag      | occurrences | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
Port Perimeter     | lane_merge     | 1           | 0.74
Downtown Loop      | pedestrian     | 1           | 0.67
CBD Night Sweep    | night_lowlight | 1           | 0.63
Airport Connector  | hard_brake     | 1           | 0.59
```

### ROLLUP 总计 {#rollup-totals}

```sql
SELECT v.route_name,
       f.event_tag,
       COUNT(*) AS occurrences
FROM frame_events f
JOIN citydrive_videos v USING (video_id)
GROUP BY ROLLUP(v.route_name, f.event_tag)
ORDER BY v.route_name NULLS LAST, f.event_tag;
```

示例输出（前 6 行）：

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

### 用于路线 × 天气覆盖情况的 CUBE {#cube-for-route-weather-coverage}

```sql
SELECT v.route_name,
       v.weather,
       COUNT(DISTINCT v.video_id) AS videos
FROM citydrive_videos v
GROUP BY CUBE(v.route_name, v.weather)
ORDER BY v.route_name NULLS LAST, v.weather NULLS LAST;
```

示例输出（前 6 行）：

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

## 5. 窗口函数 {#5-window-functions}

### 每个视频的累计风险 {#running-risk-per-video}

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

示例输出（前 6 行）：

```
video_id        | collected_at         | risk_score | cumulative_risk
VID-20250101-001| 2025-01-01 08:15:21  | 0.81       | 0.81
VID-20250101-001| 2025-01-01 08:33:54  | 0.67       | 1.48
VID-20250101-002| 2025-01-01 11:12:02  | 0.74       | 0.74
VID-20250102-001| 2025-01-02 09:44:18  | 0.59       | 0.59
VID-20250103-001| 2025-01-03 21:18:07  | 0.63       | 0.63
VID-MISSING-001 | 2025-01-04 10:00:00  | 0.25       | 0.25
```

### 最近帧的滚动平均值 {#rolling-average-over-recent-frames}

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

示例输出（前 6 行）：

```
video_id        | frame_id   | frame_index | risk_score | rolling_avg_risk
VID-20250101-001| FRAME-0101 | 125         | 0.81       | 0.81
VID-20250101-001| FRAME-0102 | 416         | 0.67       | 0.74
VID-20250101-002| FRAME-0201 | 298         | 0.74       | 0.74
VID-20250102-001| FRAME-0301 | 188         | 0.59       | 0.59
VID-20250103-001| FRAME-0401 | 522         | 0.63       | 0.63
VID-MISSING-001 | FRAME-0501 | 10          | 0.25       | 0.25
```

文档：[窗口函数](/tidb-cloud-lake/sql/window-functions-overview.md)。

---

## 6. 聚合索引加速 {#6-aggregating-index-boost}

将仪表板中经常使用的汇总结果持久化。

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

当分析师重新运行熟悉的 KPI 时，优化器会直接从该索引提供结果：

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

示例输出：

```
route_name         | event_tag      | event_count | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
Port Perimeter     | lane_merge     | 1           | 0.74
Downtown Loop      | pedestrian     | 1           | 0.67
CBD Night Sweep    | night_lowlight | 1           | 0.63
Airport Connector  | hard_brake     | 1           | 0.59
```

文档：[聚合索引](/tidb-cloud-lake/guides/aggregating-index.md) 和 [EXPLAIN](/tidb-cloud-lake/sql/explain.md)。

---

## 7. 存储过程自动化 {#7-stored-procedure-automation}

对相关逻辑进行封装，使调度任务始终生成相同的报表。

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

示例输出：

```
route_name         | event_tag      | event_count | avg_risk
Downtown Loop      | hard_brake     | 1           | 0.81
CBD Night Sweep    | night_lowlight | 1           | 0.63
Downtown Loop      | pedestrian     | 1           | 0.67
Airport Connector  | hard_brake     | 1           | 0.59
Port Perimeter     | lane_merge     | 1           | 0.74
```

存储过程既可以手动触发，也可以通过 [TASKS](/tidb-cloud-lake/sql/task.md) 或编排工具触发。

---

有了这些表和模式后，CityDrive 其余指南就可以引用完全相同的 `video_id` 键：使用 `frame_metadata_catalog` 进行 JSON 搜索，使用帧向量嵌入进行相似度检索，使用 GPS 位置进行地理查询，并通过统一的 ETL 路径保持它们同步。