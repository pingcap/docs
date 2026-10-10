---
title: Tasks によるデータロードの自動化
summary: Tasks は SQL をラップし、{{{ .lake }}} がスケジュールに従って、または条件が満たされたときに実行できるようにします。[CREATE TASK](/tidb-cloud-lake/sql/create-task.md) で定義する際は、以下の設定項目を考慮してください。
---

# Tasks によるデータロードの自動化

Tasks は SQL をラップし、{{{ .lake }}} がスケジュールに従って、または条件が満たされたときに実行できるようにします。[CREATE TASK](/tidb-cloud-lake/sql/create-task.md) で定義する際は、以下の設定項目を考慮してください。

![alt text](/media/tidb-cloud-lake/task.png)

- **Name & warehouse** – すべての task には warehouse が必要です。

    ```sql
    CREATE TASK ingest_orders
    WAREHOUSE = 'etl_wh'
    AS SELECT 1;
    ```

- **Trigger** – 固定間隔、CRON、または `AFTER another_task` を指定できます。

    ```sql
    CREATE TASK mytask
    WAREHOUSE = 'default'
    SCHEDULE = 2 MINUTE
    AS ...;
    ```

- **Guards** – 条件式が true の場合にのみ実行します。

    ```sql
    CREATE TASK mytask
    WAREHOUSE = 'default'
    WHEN STREAM_STATUS('mystream') = TRUE
    AS ...;
    ```

- **Error handling** – N 回失敗した後に一時停止する、または通知を送信します。

    ```sql
    CREATE TASK mytask
    WAREHOUSE = 'default'
    SUSPEND_TASK_AFTER_NUM_FAILURES = 3
    AS ...;
    ```

- **SQL payload** – `AS` の後に記述した内容が、その task によって実行されます。

    ```sql
    CREATE TASK bump_age
    WAREHOUSE = 'default'
    SCHEDULE = USING CRON '0 0 1 1 * *' 'UTC'
    AS UPDATE employees SET age = age + 1;
    ```

## 例 1: スケジュールされたコピー {#example-1-scheduled-copy}

センサーデータを継続的に生成し、Parquet として保存して、テーブルにロード (load) します。すべての `CREATE/ALTER TASK` 文で、`'etl_wh_small'` を**あなたの** warehouse 名に置き換えてください。

### 手順 1. デモ用オブジェクトを準備する {#step-1-prepare-demo-objects}

```sql
-- Create a playground schema and target table
CREATE DATABASE IF NOT EXISTS task_demo;
USE task_demo;

CREATE OR REPLACE TABLE sensor_events (
    event_time  TIMESTAMP,
    sensor_id   INT,
    temperature DOUBLE,
    humidity    DOUBLE
);

-- Stage that will store the generated Parquet files
CREATE OR REPLACE STAGE sensor_events_stage;
```

### 手順 2. Task 1 — ファイルを生成する {#step-2-task-1-generate-files}

`task_generate_data` は、1 分ごとに 100 件のランダムな測定値を stage に書き込みます。各実行で新しい Parquet ファイルが生成され、下流のコンシューマーがそれを取り込みできます。

```sql
CREATE OR REPLACE TASK task_generate_data
    WAREHOUSE = 'etl_wh_small' -- replace with your warehouse
    SCHEDULE = 1 MINUTE
AS
COPY INTO @sensor_events_stage
FROM (
    SELECT
        NOW()            AS event_time,
        number           AS sensor_id,
        20 + RAND() * 5  AS temperature,
        60 + RAND() * 10 AS humidity
    FROM numbers(100)
)
FILE_FORMAT = (TYPE = PARQUET);
```

### 手順 3. Task 2 — ファイルをロードする {#step-3-task-2-load-the-files}

`task_consume_data` は同じ間隔で stage をスキャンし、新しく生成されたすべての Parquet ファイルを `sensor_events` テーブルにコピーします。`PURGE = TRUE` 句により、すでに取り込み済みのファイルはクリーンアップされます。

```sql
CREATE OR REPLACE TASK task_consume_data
    WAREHOUSE = 'etl_wh_small' -- replace with your warehouse
    SCHEDULE = 1 MINUTE
AS
COPY INTO sensor_events
FROM @sensor_events_stage
PATTERN = '.*[.]parquet'
FILE_FORMAT = (TYPE = PARQUET)
PURGE = TRUE;
```

### 手順 4. Tasks を再開する {#step-4-resume-tasks}

```sql
ALTER TASK task_generate_data RESUME;
ALTER TASK task_consume_data RESUME;
```

どちらの task も、再開するまでは一時停止状態で開始されます。最初のファイル生成とコピーは、次の 1 分以内に行われるはずです。

### 手順 5. パイプラインを監視する {#step-5-monitor-the-pipeline}

```sql
-- Confirm that the tasks are running
SHOW TASKS LIKE 'task_%';

-- Inspect files on the stage (should shrink as PURGE removes processed files)
LIST @sensor_events_stage;

-- Check the ingested rows
SELECT *
FROM sensor_events
ORDER BY event_time DESC
LIMIT 5;

-- Review recent executions for troubleshooting
SELECT *
FROM task_history('task_consume_data', 5);

-- Change configuration later if needed
ALTER TASK task_consume_data
    SCHEDULE = 30 SECOND,
    WAREHOUSE = 'etl_wh_medium'; -- replace with your warehouse
```

テストが完了したら、`ALTER TASK ... SUSPEND` を使ってどちらの task も一時停止できます。

### 手順 6. Tasks を更新する {#step-6-update-tasks}

task を削除しなくても、スケジュール、warehouse、さらには SQL payload まで変更できます。

```sql
-- Tweak the schedule and warehouse
ALTER TASK task_consume_data
    SCHEDULE = 30 SECOND,
    WAREHOUSE = 'etl_wh_medium'; -- replace with your warehouse

-- Update the SQL payload (replace the existing body)
ALTER TASK task_consume_data
    AS
COPY INTO sensor_events
FROM @sensor_events_stage
FILE_FORMAT = (TYPE = PARQUET);

-- Resume after edits (tasks suspend when their SQL changes)
ALTER TASK task_consume_data RESUME;

-- Review execution history for verification
SELECT *
FROM task_history('task_consume_data', 5)
ORDER BY completed_time DESC;
```

`TASK_HISTORY` はステータス、実行時間、クエリ ID を返すため、変更内容を簡単に再確認できます。

## 例 2: Stream トリガーによるマージ {#example-2-stream-triggered-merge}

`WHEN STREAM_STATUS(...)` を使用すると、stream に新しい行がある場合にのみ実行できます。例 1 の `sensor_events` テーブルを再利用します。

### 手順 1. stream と latest テーブルを作成する {#step-1-create-stream-latest-table}

```sql
-- Create a stream on the sensor table (Standard mode to capture every mutation)
CREATE OR REPLACE STREAM sensor_events_stream
    ON TABLE sensor_events
    APPEND_ONLY = false;

-- Target table that keeps only the latest copy of each row
CREATE OR REPLACE TABLE sensor_events_latest AS
SELECT *
FROM sensor_events
WHERE 1 = 0;
```

### Step 2. 条件付きタスクを作成する {#step-2-create-the-conditional-task}

```sql
CREATE OR REPLACE TASK task_stream_merge
    WAREHOUSE = 'etl_wh_small' -- replace with your warehouse
    SCHEDULE = 1 MINUTE
    WHEN STREAM_STATUS('task_demo.sensor_events_stream') = TRUE
AS
INSERT INTO sensor_events_latest
SELECT *
FROM sensor_events_stream;

ALTER TASK task_stream_merge RESUME;
```

### Step 3. 動作を確認する {#step-3-verify-the-behavior}

```sql
SELECT *
FROM sensor_events_latest
ORDER BY event_time DESC
LIMIT 5;

SELECT *
FROM task_history('task_stream_merge', 5);
```

このタスクは、`STREAM_STATUS('<database>.<stream_name>')` が `TRUE` を返した場合にのみ実行されます。現在のスキーマに関係なくタスクが stream を解決できるよう、stream には必ずそのデータベース名をプレフィックスとして付けてください（例: `task_demo.sensor_events_stream`）。また、すべての `CREATE/ALTER TASK` では、自身の Warehouse 名を使用してください。