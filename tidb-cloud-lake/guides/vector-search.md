---
title: Vector Search
---

> **Scenario:** CityDrive keeps embeddings for every frame directly in Databend. These vector embeddings are the result of AI models inferencing on video keyframes to capture visual semantic features. Semantic similarity search ("find frames that look like this") can run alongside traditional SQL analytics—no separate vector service required.

The `frame_embeddings` table shares the same `frame_id` keys as `frame_events`, `frame_metadata_catalog`, and `frame_geo_points`, which keeps semantic search and classic SQL glued together.

## 1. Prepare the Embedding Table
Production models tend to emit 512–1536 dimensions. The example below uses 512 so you can copy it straight into a demo cluster without changing the DDL.

```sql
CREATE OR REPLACE TABLE frame_embeddings (
    frame_id      STRING,
    video_id      STRING,
    sensor_view   STRING,
    embedding     VECTOR(512),
    encoder_build STRING,
    created_at    TIMESTAMP,
    VECTOR INDEX idx_frame_embeddings(embedding) distance='cosine'
);

-- SQL UDF: build 512 dims via ARRAY_AGG + window frame; tutorial placeholder only.
CREATE OR REPLACE FUNCTION demo_random_vector(seed STRING)
RETURNS TABLE(embedding VECTOR(512))
AS $$
SELECT CAST(
         ARRAY_AGG(rand_val) OVER (
           PARTITION BY seed
           ORDER BY seq
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
         )
         AS VECTOR(512)
       ) AS embedding
FROM (
  SELECT seed,
         dims.number AS seq,
         (RAND() * 0.2 - 0.1)::FLOAT AS rand_val
  FROM numbers(512) AS dims
) vals
QUALIFY ROW_NUMBER() OVER (PARTITION BY seed ORDER BY seq) = 1;
$$;

INSERT INTO frame_embeddings (frame_id, video_id, sensor_view, embedding, encoder_build, created_at)
SELECT 'FRAME-0101', 'VID-20250101-001', 'roof_cam', embedding, 'clip-lite-v1', '2025-01-01 08:15:21'
FROM demo_random_vector('FRAME-0101')
UNION ALL
SELECT 'FRAME-0102', 'VID-20250101-001', 'roof_cam', embedding, 'clip-lite-v1', '2025-01-01 08:33:54'
FROM demo_random_vector('FRAME-0102')
UNION ALL
SELECT 'FRAME-0201', 'VID-20250101-002', 'front_cam', embedding, 'night-fusion-v2', '2025-01-01 11:12:02'
FROM demo_random_vector('FRAME-0201')
UNION ALL
SELECT 'FRAME-0401', 'VID-20250103-001', 'rear_cam', embedding, 'night-fusion-v2', '2025-01-03 21:18:07'
FROM demo_random_vector('FRAME-0401');
```

> This array generator is just to keep the tutorial self-contained. Replace it with real embeddings from your model in production.

If you haven’t run the SQL Analytics guide yet, create the supporting `frame_events` table and seed the same sample rows the vector walkthrough joins against:

```sql
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
```

Docs: [Vector type](/sql/sql-reference/data-types/vector) and [Vector index](/sql/sql-reference/data-types/vector#vector-indexing).

---

## 2. Run Cosine Search
Pull the embedding from one frame and let the HNSW index return the closest neighbours.

```sql
WITH query_embedding AS (
    SELECT embedding
    FROM frame_embeddings
    WHERE frame_id = 'FRAME-0101'
)
SELECT e.frame_id,
       e.video_id,
       COSINE_DISTANCE(e.embedding, q.embedding) AS distance
FROM frame_embeddings AS e
CROSS JOIN query_embedding AS q
ORDER BY distance
LIMIT 3;
```

Sample output:

```
frame_id  | video_id         | distance
FRAME-0101| VID-20250101-001 | 0.0000
FRAME-0201| VID-20250101-002 | 0.9801
FRAME-0102| VID-20250101-001 | 0.9842
```

Lower distance = more similar. The `VECTOR INDEX` keeps latency low even with millions of frames.

Add traditional predicates (route, video, sensor view) before or after the vector comparison to narrow the candidate set.

```sql
WITH query_embedding AS (
    SELECT embedding
    FROM frame_embeddings
    WHERE frame_id = 'FRAME-0201'
)
SELECT e.frame_id,
       e.sensor_view,
       COSINE_DISTANCE(e.embedding, q.embedding) AS distance
FROM frame_embeddings AS e
CROSS JOIN query_embedding AS q
WHERE e.sensor_view = 'rear_cam'
ORDER BY distance
LIMIT 5;
```

Sample output:

```
frame_id  | sensor_view | distance
FRAME-0401| rear_cam    | 1.0537
```

The optimizer still uses the vector index while honoring the `sensor_view` filter.

---

## 3. Enrich Similar Frames
Materialize the top matches, then enrich them with `frame_events` for downstream analytics.

```sql
WITH query_embedding AS (
       SELECT embedding
       FROM frame_embeddings
       WHERE frame_id = 'FRAME-0102'
     ),
     similar_frames AS (
       SELECT frame_id,
              video_id,
              COSINE_DISTANCE(e.embedding, q.embedding) AS distance
       FROM frame_embeddings e
       CROSS JOIN query_embedding q
       ORDER BY distance
       LIMIT 5
     )
SELECT sf.frame_id,
       sf.video_id,
       fe.event_tag,
       fe.risk_score,
       sf.distance
FROM similar_frames sf
LEFT JOIN frame_events fe USING (frame_id)
ORDER BY sf.distance;
```

Sample output:

```
frame_id  | video_id         | event_tag      | risk_score | distance
FRAME-0102| VID-20250101-001 | pedestrian     | 0.67       | 0.0000
FRAME-0201| VID-20250101-002 | lane_merge     | 0.74       | 0.9802
FRAME-0101| VID-20250101-001 | hard_brake     | 0.81       | 0.9842
FRAME-0401| VID-20250103-001 | night_lowlight | 0.63       | 1.0020
```

Because the embeddings live next to relational tables, you can pivot from “frames that look alike” to “frames that also had `hard_brake` tags, specific weather, or JSON detections” without exporting data to another service.
