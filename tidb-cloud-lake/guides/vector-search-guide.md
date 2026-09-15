---
title: 向量搜索
summary: 在该场景中，CityDrive 将每一帧的 embedding 直接保存在 {{{ .lake }}} 中。这些向量 embedding 来自 AI 模型对视频关键帧的推导结果，用于捕获视觉语义特征。语义相似度搜索（“查找看起来像这样的帧”）可以与传统 SQL 分析同时运行——无需单独的向量服务。
---

# 向量搜索

> **场景：** CityDrive 将每一帧的 embedding 直接保存在 {{{ .lake }}} 中。这些向量 embedding 来自 AI 模型对视频关键帧的推导结果，用于捕获视觉语义特征。语义相似度搜索（“查找看起来像这样的帧”）可以与传统 SQL 分析同时运行——无需单独的向量服务。

`frame_embeddings` 表与 `frame_events`、`frame_metadata_catalog` 和 `frame_geo_points` 共享相同的 `frame_id` 键，这使得语义搜索与经典 SQL 能够紧密结合。

## 1. 准备 embedding 表 {#1-prepare-the-embedding-table}

生产模型通常会输出 512–1536 维。下面的示例使用 512 维，这样你可以直接将其复制到演示集群中，而无需修改 DDL。

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

> 这个数组生成器只是为了让本教程自包含。在生产环境中，请将其替换为模型生成的真实 embedding。

如果你还没有运行 SQL Analytics 指南，请先创建配套的 `frame_events` 表，并填充与向量演练中关联查询相同的示例数据行：

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

文档： [Vector 类型](/tidb-cloud-lake/sql/vector.md) 和 [向量索引](/tidb-cloud-lake/sql/vector.md#vector-indexing)。

---

## 2. 运行余弦搜索 {#2-run-cosine-search}

从某一帧中取出 embedding，并让 HNSW 索引返回最接近的邻居。

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

示例输出：

```
frame_id  | video_id         | distance
FRAME-0101| VID-20250101-001 | 0.0000
FRAME-0201| VID-20250101-002 | 0.9801
FRAME-0102| VID-20250101-001 | 0.9842
```

距离越小，表示越相似。即使有数百万帧，`VECTOR INDEX` 也能将延时保持在较低水平。

你可以在向量比较之前或之后添加传统谓词（route、video、sensor view），以缩小候选集。

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

示例输出：

```
frame_id  | sensor_view | distance
FRAME-0401| rear_cam    | 1.0537
```

优化器在遵循 `sensor_view` 过滤条件的同时，仍会使用向量索引。

---

## 3. 丰富相似帧结果 {#3-enrich-similar-frames}

先将最相似的匹配结果物化出来，再使用 `frame_events` 对其进行补充，以供下游分析使用。

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

示例输出：

```
frame_id  | video_id         | event_tag      | risk_score | distance
FRAME-0102| VID-20250101-001 | pedestrian     | 0.67       | 0.0000
FRAME-0201| VID-20250101-002 | lane_merge     | 0.74       | 0.9802
FRAME-0101| VID-20250101-001 | hard_brake     | 0.81       | 0.9842
FRAME-0401| VID-20250103-001 | night_lowlight | 0.63       | 1.0020
```

由于 embedding 与关系型表存放在一起，你可以从“看起来相似的帧”进一步切换到“同时带有 `hard_brake` 标签、特定天气条件或 JSON 检测结果的帧”，而无需将数据导出到其他服务。

如果要限制某个角色在向量搜索期间可以检索哪些文档，可以附加一个 [行访问策略](/tidb-cloud-lake/guides/row-access-policy.md#vector--rag-document-visibility)，这样可见性由引擎强制执行，而不是通过在查询中塞入文档 ID 来实现。