---
title: ベクトル検索
summary: シナリオ: CityDrive は各フレームの埋め込みを {{{ .lake }}} に直接保持しています。これらのベクトル埋め込みは、動画キーフレームに対して AI モデルが推論を実行し、視覚的な意味特徴を捉えた結果です。意味的類似検索（「これに似たフレームを探す」）は、従来の SQL 分析と並行して実行でき、別個のベクトルサービスは不要です。
---

# ベクトル検索

> **Scenario:** CityDrive は各フレームの埋め込みを {{{ .lake }}} に直接保持しています。これらのベクトル埋め込みは、動画キーフレームに対して AI モデルが推論を実行し、視覚的な意味特徴を捉えた結果です。意味的類似検索（「これに似たフレームを探す」）は、従来の SQL 分析と並行して実行でき、別個のベクトルサービスは不要です。

`frame_embeddings` テーブルは、`frame_events`、`frame_metadata_catalog`、`frame_geo_points` と同じ `frame_id` キーを共有しているため、意味検索と従来の SQL を密接に連携させることができます。

## 1. 埋め込みテーブルを準備する {#1-prepare-the-embedding-table}

本番モデルは通常 512～1536 次元を出力します。以下の例では 512 を使用しているため、DDL を変更せずにそのままデモクラスターへコピーできます。

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

> この配列ジェネレーターは、チュートリアルを自己完結させるためだけのものです。本番では、これをモデルから得た実際の埋め込みに置き換えてください。

まだ SQL Analytics ガイドを実行していない場合は、補助となる `frame_events` テーブルを作成し、このベクトル検索の手順で結合する同じサンプル行を投入してください。

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

ドキュメント: [ベクトル型](/tidb-cloud-lake/sql/vector.md) および [ベクトルインデックス](/tidb-cloud-lake/sql/vector.md#vector-indexing)。

---

## 2. コサイン検索を実行する {#2-run-cosine-search}

あるフレームの埋め込みを取得し、HNSW インデックスで最も近い近傍を返します。

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

出力例:

```
frame_id  | video_id         | distance
FRAME-0101| VID-20250101-001 | 0.0000
FRAME-0201| VID-20250101-002 | 0.9801
FRAME-0102| VID-20250101-001 | 0.9842
```

距離が小さいほど、より類似しています。`VECTOR INDEX` により、数百万フレーム規模でもレイテンシーを低く保てます。

ベクトル比較の前後で、従来の述語（route、video、sensor view）を追加して Candidate 集合を絞り込めます。

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

出力例:

```
frame_id  | sensor_view | distance
FRAME-0401| rear_cam    | 1.0537
```

オプティマイザーは、`sensor_view` フィルターを適用しつつ、引き続きベクトルインデックスを使用します。

---

## 3. 類似フレームを拡張する {#3-enrich-similar-frames}

上位の一致結果を具体化し、その後 `frame_events` で拡張して下流の分析に利用します。

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

出力例:

```
frame_id  | video_id         | event_tag      | risk_score | distance
FRAME-0102| VID-20250101-001 | pedestrian     | 0.67       | 0.0000
FRAME-0201| VID-20250101-002 | lane_merge     | 0.74       | 0.9802
FRAME-0101| VID-20250101-001 | hard_brake     | 0.81       | 0.9842
FRAME-0401| VID-20250103-001 | night_lowlight | 0.63       | 1.0020
```

埋め込みがリレーショナルテーブルの隣に存在するため、「見た目が似ているフレーム」から、「`hard_brake` タグ、特定の天候、または JSON 検出結果も持つフレーム」へと、データを別サービスへエクスポートすることなく分析を展開できます。

ベクトル検索中にロールが取得できるドキュメントを制限するには、[行アクセスポリシー](/tidb-cloud-lake/guides/row-access-policy.md#vector--rag-document-visibility) を適用してください。これにより、可視性はクエリにドキュメント ID を詰め込むのではなく、エンジンによって強制されます。