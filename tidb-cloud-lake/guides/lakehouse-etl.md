---
title: Lakehouse ETL
summary: Scenario CityDrive's data engineering team exports every batch of dash-cam data as Parquet (videos, frame events, metadata JSON, embeddings, GPS traces, traffic light distances). These Parquet files aggregate all multimodal signals extracted from the raw video streams, forming the foundation of the warehouse. They want to update Databend's shared tables via a single COPY pipeline. to refresh the shared tables in Databend.
---
> **Scenario:** CityDrive's data engineering team exports every batch of dash-cam data as Parquet (videos, frame events, metadata JSON, embeddings, GPS traces, traffic light distances). These Parquet files aggregate all multimodal signals extracted from the raw video streams, forming the foundation of the warehouse. They want to update Databend's shared tables via a single COPY pipeline. to refresh the shared tables in Databend.

The loading loop is straightforward:

```
Object storage → STAGE → COPY INTO tables → (optional) STREAMS/TASKS
```

Adjust the bucket path or format to match your environment, then paste the commands below. Syntax mirrors the data loading guides.

---

## 1. Create a Stage
Point a reusable stage at the bucket that holds the CityDrive exports. Swap the credentials/URL for your own account; Parquet is used here, but any supported format works with a different `FILE_FORMAT`.

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
> Replace the placeholder AWS keys and bucket URL with real values from your environment. Without valid credentials, `LIST`, `SELECT ... FROM @citydrive_stage`, and `COPY INTO` statements will fail with `InvalidAccessKeyId`/403 errors from S3.

Quick sanity check:

```sql
LIST @citydrive_stage/videos/;
LIST @citydrive_stage/frame-events/;
LIST @citydrive_stage/manifests/;
LIST @citydrive_stage/frame-embeddings/;
LIST @citydrive_stage/frame-locations/;
LIST @citydrive_stage/traffic-lights/;
```

---

## 2. Peek at the Files
Use a `SELECT` against the stage to confirm schema and sample rows before loading.

```sql
SELECT *
FROM @citydrive_stage/videos/capture_date=2025-01-01/videos.parquet
LIMIT 5;

SELECT *
FROM @citydrive_stage/frame-events/batch_2025_01_01.parquet
LIMIT 5;
```

Databend infers the format from the stage definition, so no extra options are required here.

---

## 3. COPY INTO the Unified Tables
Each export maps to one of the shared tables used across the guides. Inline casts keep schemas consistent even if upstream ordering changes.

### `citydrive_videos`
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

### `frame_events`
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

### `frame_metadata_catalog`
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

### `frame_embeddings`
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

### `frame_geo_points`
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

### `signal_contact_points`
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

After this step, every downstream workload—SQL analytics, Elasticsearch `QUERY()`, vector similarity, geospatial filters—reads the exact same data.

---

## 4. Streams for Incremental Reactions (Optional)
Use streams when you want downstream jobs to consume only the rows added since the last batch.

```sql
CREATE OR REPLACE STREAM frame_events_stream ON TABLE frame_events;

SELECT * FROM frame_events_stream;   -- shows newly copied rows
-- …process rows…
SELECT * FROM frame_events_stream WITH CONSUME;  -- advance the offset
```

`WITH CONSUME` ensures the stream cursor moves forward after the rows are handled. Reference: [Streams](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md).

---

## 5. Tasks for Scheduled Loads (Optional)
Tasks run **one SQL statement** on a schedule. Create lightweight tasks per table or wrap the logic in a stored procedure if you prefer one entry point.

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

Add more tasks for `frame_metadata_catalog`, embeddings, or GPS data using the same pattern. Full options: [Tasks](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md).

---

Once these jobs run, every guide in the Unified Workloads series reads from the same CityDrive tables—no extra ETL layers, no duplicate storage.
