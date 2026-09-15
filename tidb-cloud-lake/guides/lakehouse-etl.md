---
title: Lakehouse ETL
summary: 场景：CityDrive 的数据工程团队将每一批行车记录仪数据导出为 Parquet（视频、帧事件、元信息 JSON、嵌入向量、GPS 轨迹、红绿灯距离）。这些 Parquet 文件汇总了从原始视频流中提取的所有多模态信号，构成了计算集群的基础。他们希望通过单个 COPY pipeline 来修改 {{{ .lake }}} 中的共享表，以刷新 {{{ .lake }}} 中的共享表。
---

# Lakehouse ETL

> **场景：** CityDrive 的数据工程团队将每一批行车记录仪数据导出为 Parquet（视频、帧事件、元信息 JSON、嵌入向量、GPS 轨迹、红绿灯距离）。这些 Parquet 文件汇总了从原始视频流中提取的所有多模态信号，构成了计算集群的基础。他们希望通过单个 COPY pipeline 来修改 {{{ .lake }}} 中的共享表，以刷新 {{{ .lake }}} 中的共享表。

加载流程非常直接：

```
Object storage → STAGE → COPY INTO tables → (optional) STREAMS/TASKS
```

根据你的环境调整存储桶路径或格式，然后粘贴下面的命令。语法与数据加载指南保持一致。

---

## 1. Create a Stage {#1-create-a-stage}

将一个可复用的 stage 指向存放 CityDrive 导出数据的存储桶。将凭证和 URL 替换为你自己的账户信息；这里使用 Parquet，但只要更改 `FILE_FORMAT`，也可以使用任何受支持的格式。

```sql
CREATE OR REPLACE CONNECTION citydrive_s3
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<AWS_ACCESS_KEY_ID>'
  SECRET_ACCESS_KEY = '<AWS_SECRET_ACCESS_KEY>';

CREATE OR REPLACE STAGE citydrive_stage
  URL = 's3://citydrive-lakehouse/raw/'
  CONNECTION = (CONNECTION_NAME = 'citydrive_s3')
  FILE_FORMAT = (TYPE = 'PARQUET');
```

> [!IMPORTANT]
> 请将示例中的 AWS 密钥和存储桶 URL 占位符替换为你环境中的真实值。没有有效凭证时，`LIST`、`SELECT ... FROM @citydrive_stage` 和 `COPY INTO` 语句都会因 S3 返回的 `InvalidAccessKeyId`/403 错误而失败。

快速检查：

```sql
LIST @citydrive_stage/videos/;
LIST @citydrive_stage/frame-events/;
LIST @citydrive_stage/manifests/;
LIST @citydrive_stage/frame-embeddings/;
LIST @citydrive_stage/frame-locations/;
LIST @citydrive_stage/traffic-lights/;
```

---

## 2. Peek at the Files {#2-peek-at-the-files}

在加载之前，对 stage 执行 `SELECT`，以确认 schema 和示例行。

```sql
SELECT *
FROM @citydrive_stage/videos/capture_date=2025-01-01/videos.parquet
LIMIT 5;

SELECT *
FROM @citydrive_stage/frame-events/batch_2025_01_01.parquet
LIMIT 5;
```

{{{ .lake }}} 会根据 stage 定义推导格式，因此这里不需要额外选项。

---

## 3. COPY INTO the Unified Tables {#3-copy-into-the-unified-tables}

每份导出数据都映射到各指南中共用的一张共享表。内联类型转换可以在上游字段顺序发生变化时，仍保持 schema 一致。

### `citydrive_videos` {#citydrive-videos}

```sql
COPY INTO citydrive_videos (video_id, vehicle_id, capture_date, route_name, weather, camera_source, duration_sec)
FROM (
  SELECT video_id::STRING,
         vehicle_id::STRING,
         capture_date::DATE,
         route_name::STRING,
         weather::STRING,
         camera_source::STRING,
         duration_sec::INT
  FROM @citydrive_stage/videos/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

### `frame_events` {#frame-events}

```sql
COPY INTO frame_events (frame_id, video_id, frame_index, collected_at, event_tag, risk_score, speed_kmh)
FROM (
  SELECT frame_id::STRING,
         video_id::STRING,
         frame_index::INT,
         collected_at::TIMESTAMP,
         event_tag::STRING,
         risk_score::DOUBLE,
         speed_kmh::DOUBLE
  FROM @citydrive_stage/frame-events/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

### `frame_metadata_catalog` {#frame-metadata-catalog}

```sql
COPY INTO frame_metadata_catalog (doc_id, meta_json, captured_at)
FROM (
  SELECT doc_id::STRING,
         meta_json::VARIANT,
         captured_at::TIMESTAMP
  FROM @citydrive_stage/manifests/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

### `frame_embeddings` {#frame-embeddings}

```sql
COPY INTO frame_embeddings (frame_id, video_id, sensor_view, embedding, encoder_build, created_at)
FROM (
  SELECT frame_id::STRING,
         video_id::STRING,
         sensor_view::STRING,
         embedding::VECTOR(768), -- replace with your actual dimension
         encoder_build::STRING,
         created_at::TIMESTAMP
  FROM @citydrive_stage/frame-embeddings/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

### `frame_geo_points` {#frame-geo-points}

```sql
COPY INTO frame_geo_points (video_id, frame_id, position_wgs84, solution_grade, source_system, created_at)
FROM (
  SELECT video_id::STRING,
         frame_id::STRING,
         position_wgs84::GEOMETRY,
         solution_grade::INT,
         source_system::STRING,
         created_at::TIMESTAMP
  FROM @citydrive_stage/frame-locations/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

### `signal_contact_points` {#signal-contact-points}

```sql
COPY INTO signal_contact_points (node_id, signal_position, video_id, frame_id, frame_position, distance_m, created_at)
FROM (
  SELECT node_id::STRING,
         signal_position::GEOMETRY,
         video_id::STRING,
         frame_id::STRING,
         frame_position::GEOMETRY,
         distance_m::DOUBLE,
         created_at::TIMESTAMP
  FROM @citydrive_stage/traffic-lights/
)
FILE_FORMAT = (TYPE = 'PARQUET');
```

完成此步骤后，所有下游工作负载——SQL analytics、Elasticsearch `QUERY()`、向量相似度、地理空间过滤——都会读取完全相同的数据。

---

## 4. Streams for Incremental Reactions (Optional) {#4-streams-for-incremental-reactions-optional}

如果你希望下游作业只消费自上一批次以来新增的行，请使用 stream。

```sql
CREATE OR REPLACE STREAM frame_events_stream ON TABLE frame_events;

SELECT * FROM frame_events_stream;   -- shows newly copied rows
-- …process rows…
SELECT * FROM frame_events_stream WITH CONSUME;  -- advance the offset
```

`WITH CONSUME` 可确保在处理完这些行后，stream 游标继续向前推进。参考：[Streams](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md)。

---

## 5. Scheduled Loads 的任务（可选） {#5-tasks-for-scheduled-loads-optional}

任务会按调度运行**一条 SQL 语句**。你可以按表创建轻量级任务；如果你更希望只有一个入口点，也可以将相关逻辑封装在存储过程中。

```sql
CREATE OR REPLACE TASK task_load_citydrive_videos
  WAREHOUSE = 'default'
  SCHEDULE = 10 MINUTE
AS
  COPY INTO citydrive_videos (video_id, vehicle_id, capture_date, route_name, weather, camera_source, duration_sec)
  FROM (
    SELECT video_id::STRING,
           vehicle_id::STRING,
           capture_date::DATE,
           route_name::STRING,
           weather::STRING,
           camera_source::STRING,
           duration_sec::INT
    FROM @citydrive_stage/videos/
  )
  FILE_FORMAT = (TYPE = 'PARQUET');

ALTER TASK task_load_citydrive_videos RESUME;

CREATE OR REPLACE TASK task_load_frame_events
  WAREHOUSE = 'default'
  SCHEDULE = 10 MINUTE
 AS
  COPY INTO frame_events (frame_id, video_id, frame_index, collected_at, event_tag, risk_score, speed_kmh)
  FROM (
    SELECT frame_id::STRING,
           video_id::STRING,
           frame_index::INT,
           collected_at::TIMESTAMP,
           event_tag::STRING,
           risk_score::DOUBLE,
           speed_kmh::DOUBLE
    FROM @citydrive_stage/frame-events/
  )
  FILE_FORMAT = (TYPE = 'PARQUET');

ALTER TASK task_load_frame_events RESUME;
```

你可以使用相同的模式为 `frame_metadata_catalog`、embeddings 或 GPS 数据添加更多任务。完整选项请参见：[任务](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md)。

---

这些作业运行后，Unified Workloads 系列中的每篇指南都会从同一组 CityDrive 表中读取数据——无需额外的 ETL 层，也无需重复存储。