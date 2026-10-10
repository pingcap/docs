---
title: Lakehouse ETL
summary: "シナリオ: CityDrive のデータエンジニアリングチームは、各バッチのダッシュカムデータを Parquet（動画、フレームイベント、メタデータ JSON、埋め込み、GPS トレース、信号機までの距離）としてエクスポートしています。これらの Parquet ファイルは、生の動画ストリームから抽出されたすべてのマルチモーダル信号を集約し、Warehouse の基盤を形成します。チームは、単一の COPY パイプラインを通じて {{{ .lake }}} の共有テーブルを更新し、{{{ .lake }}} 内の共有テーブルをリフレッシュしたいと考えています。"
---

# Lakehouse ETL

> **Scenario:** CityDrive のデータエンジニアリングチームは、各バッチのダッシュカムデータを Parquet（動画、フレームイベント、メタデータ JSON、埋め込み、GPS トレース、信号機までの距離）としてエクスポートしています。これらの Parquet ファイルは、生の動画ストリームから抽出されたすべてのマルチモーダル信号を集約し、Warehouse の基盤を形成します。チームは、単一の COPY パイプラインを通じて {{{ .lake }}} の共有テーブルを更新し、{{{ .lake }}} 内の共有テーブルをリフレッシュしたいと考えています。

ロード (load) ループはシンプルです。

```
Object storage → STAGE → COPY INTO tables → (optional) STREAMS/TASKS
```

バケットパスまたはフォーマットを環境に合わせて調整し、その後で以下のコマンドを貼り付けてください。構文はデータロードガイドと同じです。

---

## 1. stage を作成する {#1-create-a-stage}

CityDrive のエクスポートを格納しているバケットを指す、再利用可能な stage を作成します。認証情報と URL は自分のアカウントのものに置き換えてください。ここでは Parquet を使用していますが、`FILE_FORMAT` を変更すれば、サポートされている任意の形式を使用できます。

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
> プレースホルダーの AWS キーとバケット URL を、実際の環境の値に置き換えてください。有効な認証情報がない場合、`LIST`、`SELECT ... FROM @citydrive_stage`、および `COPY INTO` ステートメントは、S3 からの `InvalidAccessKeyId`/403 エラーで失敗します。

簡単な動作確認:

```sql
LIST @citydrive_stage/videos/;
LIST @citydrive_stage/frame-events/;
LIST @citydrive_stage/manifests/;
LIST @citydrive_stage/frame-embeddings/;
LIST @citydrive_stage/frame-locations/;
LIST @citydrive_stage/traffic-lights/;
```

---

## 2. ファイルの内容を確認する {#2-peek-at-the-files}

ロード前に、stage に対して `SELECT` を実行して、スキーマとサンプル行を確認します。

```sql
SELECT *
FROM @citydrive_stage/videos/capture_date=2025-01-01/videos.parquet
LIMIT 5;

SELECT *
FROM @citydrive_stage/frame-events/batch_2025_01_01.parquet
LIMIT 5;
```

{{{ .lake }}} は stage 定義からフォーマットを推論するため、ここでは追加オプションは不要です。

---

## 3. 統合テーブルに COPY INTO する {#3-copy-into-the-unified-tables}

各エクスポートは、各ガイドで共通して使用される共有テーブルのいずれか 1 つに対応します。インラインキャストにより、上流の列順が変わってもスキーマの一貫性を保てます。

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
         embedding::VECTOR(768), -- 実際の次元数に置き換えてください
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

このステップの後、下流のすべてのワークロード（SQL 分析、Elasticsearch `QUERY()`、ベクトル類似検索、地理空間フィルター）は、まったく同じデータを読み取ります。

---

## 4. 増分処理のための Streams（オプション） {#4-streams-for-incremental-reactions-optional}

下流ジョブで前回のバッチ以降に追加された行だけを消費したい場合は、streams を使用します。

```sql
CREATE OR REPLACE STREAM frame_events_stream ON TABLE frame_events;

SELECT * FROM frame_events_stream;   -- shows newly copied rows
-- …process rows…
SELECT * FROM frame_events_stream WITH CONSUME;  -- advance the offset
```

`WITH CONSUME` により、行の処理後に stream カーソルが先へ進むことが保証されます。参考: [Streams](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md).

---

## 5. スケジュールされたロード向けのタスク（任意） {#5-tasks-for-scheduled-loads-optional}

タスクは、スケジュールに従って**1 つの SQL 文**を実行します。テーブルごとに軽量なタスクを作成することも、単一のエントリポイントにしたい場合はロジックをストアドプロシージャにまとめることもできます。

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

同じパターンを使って、`frame_metadata_catalog`、embeddings、または GPS データ向けのタスクをさらに追加できます。すべてのオプションについては、[Tasks](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md) を参照してください。

---

これらのジョブが実行されると、Unified Workloads シリーズのすべてのガイドは同じ CityDrive テーブルを読み取るようになります。追加の ETL レイヤーも、重複したストレージも不要です。