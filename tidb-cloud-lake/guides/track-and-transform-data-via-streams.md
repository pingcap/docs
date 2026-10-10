---
title: Streams によるデータの追跡と変換
summary: {{{ .lake }}} の stream は常時稼働する変更テーブルであり、コミットされたすべての INSERT、UPDATE、DELETE は、消費されるまでキャプチャされます。このページは簡潔にまとめています。まず概要をすばやく確認し、その後に実際の出力を含む 1 つのラボで、stream の動作を確認できます。
---

# Streams によるデータの追跡と変換

{{{ .lake }}} の stream は常時稼働する変更テーブルです。コミットされたすべての INSERT、UPDATE、DELETE は、消費されるまでキャプチャされます。このページは簡潔にまとめています。まず概要をすばやく確認し、その後に実際の出力を含む 1 つのラボで、stream の動作を確認できます。

## Stream の概要 {#stream-overview}

- Stream はテーブルストレージを複製しません。消費されるまで、影響を受けた各行について最新の変更を一覧表示します。
- 消費（task、INSERT ... SELECT、`WITH CONSUME` など）を行うと、stream はクリアされますが、新しいデータを受け取れる状態は維持されます。
- `APPEND_ONLY` のデフォルトは `true` です。UPDATE/DELETE イベントをキャプチャする必要がある場合にのみ、`APPEND_ONLY = false` を設定してください。

| モード | キャプチャ対象 | 一般的な用途 |
| --- | --- | --- |
| Standard (`APPEND_ONLY = false`) | INSERT + UPDATE + DELETE。行ごとに最新状態へ集約されます。 | 緩やかに変化するディメンション、コンプライアンス監査。 |
| Append-Only (`APPEND_ONLY = true`, default) | INSERT のみ。 | 追記専用のファクト/イベント取り込み。 |

## 例 1: Append-Only Stream {#example-1-append-only-stream}

以下のステートメントを任意の {{{ .lake }}} デプロイメント（Cloud worksheet またはローカル）で実行し、デフォルトの append-only モードが insert をどのようにキャプチャして消費するかを確認します。

### 1. テーブルと stream を作成する {#1-create-table-and-stream}

```sql
CREATE OR REPLACE TABLE sensor_readings (
    sensor_id INT,
    temperature DOUBLE
);

-- APPEND_ONLY defaults to true, so no extra clause is required.
CREATE OR REPLACE STREAM sensor_readings_stream
    ON TABLE sensor_readings;
```

### 2. 行を挿入してプレビューする {#2-insert-rows-and-preview}

```sql
INSERT INTO sensor_readings VALUES (1, 21.5), (2, 19.7);

SELECT sensor_id, temperature, change$action, change$is_update
FROM sensor_readings_stream;
```

出力:

```
┌────────────┬───────────────┬───────────────┬──────────────────┐
│ sensor_id  │ temperature   │ change$action │ change$is_update │
├────────────┼───────────────┼───────────────┼──────────────────┤
│          1 │ 21.5          │ INSERT        │ false            │
│          2 │ 19.7          │ INSERT        │ false            │
└────────────┴───────────────┴───────────────┴──────────────────┘
```

### 3. 消費する（任意） {#3-consume-optional}

```sql
SELECT sensor_id, temperature
FROM sensor_readings_stream WITH CONSUME;

SELECT * FROM sensor_readings_stream; -- now empty
```

`WITH CONSUME` は stream を 1 回読み取り、差分をクリアするため、次のラウンドでは新しい INSERT をキャプチャできます。

## 例 2: Standard Stream（Updates & Deletes） {#example-2-standard-stream-updates-deletes}

UPDATE や DELETE を含むすべての変更に反応する必要がある場合は、Standard モードに切り替えます。

### 1. Standard stream を作成する {#1-create-a-standard-stream}

```sql
CREATE OR REPLACE STREAM sensor_readings_stream_std
    ON TABLE sensor_readings
    APPEND_ONLY = false;
```

### 2. 行を変更して比較する {#2-mutate-rows-and-compare}

```sql
DELETE FROM sensor_readings WHERE sensor_id = 1;     -- remove old reading
INSERT INTO sensor_readings VALUES (1, 22);         -- same sensor, new value
DELETE FROM sensor_readings WHERE sensor_id = 2;     -- pure deletion
INSERT INTO sensor_readings VALUES (3, 18.5);        -- brand-new sensor

SELECT * FROM sensor_readings_stream; -- still empty (Append-Only ignores non-inserts)

SELECT sensor_id, temperature, change$action, change$is_update
FROM sensor_readings_stream_std
ORDER BY change$row_id;
```

出力:

```
┌────────────┬───────────────┬───────────────┬──────────────────┐
│ sensor_id  │ temperature   │ change$action │ change$is_update │
├────────────┼───────────────┼───────────────┼──────────────────┤
│          1 │ 21.5          │ DELETE        │ true             │
│          1 │ 22            │ INSERT        │ true             │
│          2 │ 19.7          │ DELETE        │ false            │
│          3 │ 18.5          │ INSERT        │ false            │
└────────────┴───────────────┴───────────────┴──────────────────┘
```

Standard stream は、コンテキスト付きで各変更をキャプチャします。更新は同じ `sensor_id` に対する DELETE+INSERT として表示され、単独の削除/挿入は個別に表示されます。Append-Only stream は insert のみを追跡するため、空のままです。

## 例 3: 増分 Stream Join {#example-3-incremental-stream-join}

複数の append-only stream を join して、増分 KPI を生成します。{{{ .lake }}} の stream は消費されるまで新しい行を保持するため、各ロード (load) の後に同じクエリを実行できます。各実行では、[`WITH CONSUME`](/tidb-cloud-lake/sql/with-consume.md) により新しい行だけがドレインされるため、異なるタイミングで到着した更新も次の反復で引き続きマッチします。

### 1. テーブルと stream を作成する {#1-create-tables-and-streams}

```sql
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    segment VARCHAR,
    city VARCHAR
);

CREATE OR REPLACE TABLE orders (
    order_id INT,
    customer_id INT,
    amount DOUBLE
);

CREATE OR REPLACE STREAM customers_stream ON TABLE customers;
CREATE OR REPLACE STREAM orders_stream ON TABLE orders;
```

### 2. 最初のバッチをロードする {#2-load-the-first-batch}

```sql
INSERT INTO customers VALUES
    (101, 'VIP', 'Seattle'),
    (102, 'Standard', 'Austin'),
    (103, 'VIP', 'Austin');

INSERT INTO orders VALUES
    (5001, 101, 199.0),
    (5002, 101, 59.0),
    (5003, 102, 89.0);
```

### 3. 最初の増分クエリを実行する {#3-run-the-first-incremental-query}

```sql
WITH
    orders_delta AS (
        SELECT customer_id, amount
        FROM orders_stream WITH CONSUME
    ),
    customers_delta AS (
        SELECT customer_id, segment
        FROM customers_stream WITH CONSUME
    )
SELECT
    o.customer_id,
    c.segment,
    SUM(o.amount) AS incremental_sales
FROM orders_delta AS o
JOIN customers_delta AS c
    ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.segment
ORDER BY o.customer_id;
```

```
┌──────────────┬───────────┬────────────────────┐
│ customer_id  │ segment   │ incremental_sales  │
├──────────────┼───────────┼────────────────────┤
│          101 │ VIP       │ 258.0              │
│          102 │ Standard  │  89.0              │
└──────────────┴───────────┴────────────────────┘
```

これで stream は空になります。さらに行が到着すると、同じクエリは新しいデータだけをキャプチャします。

### 4. 次のバッチの後に再実行する {#4-run-again-after-the-next-batch}

```sql
-- New data arrives later
INSERT INTO customers VALUES (104, 'Standard', 'Denver');
INSERT INTO orders VALUES
    (5004, 101, 40.0),
    (5005, 104, 120.0);

-- Same incremental query as before
WITH
    orders_delta AS (
        SELECT customer_id, amount
        FROM orders_stream WITH CONSUME
    ),
    customers_delta AS (
        SELECT customer_id, segment
        FROM customers_stream WITH CONSUME
    )
SELECT
    o.customer_id,
    c.segment,
    SUM(o.amount) AS incremental_sales
FROM orders_delta AS o
JOIN customers_delta AS c
    ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.segment
ORDER BY o.customer_id;
```

```
┌──────────────┬───────────┬────────────────────┐
│ customer_id  │ segment   │ incremental_sales  │
├──────────────┼───────────┼────────────────────┤
│          101 │ VIP       │ 40.0               │
│          104 │ Standard  │ 120.0              │
└──────────────┴───────────┴────────────────────┘
```

各ストリームの行は `WITH CONSUME` が実行されるまで保持されるため、異なるタイミングで到着した INSERT でも次回の実行時に引き続きマッチします。関連する行がさらに到着する見込みがある場合はストリームを未消費のままにしておき、増分の差分を取り込むために後でクエリを再実行してください。

## ストリームワークフローに関する注意事項 {#stream-workflow-notes}

**Consumption**

- ストリームはトランザクション内で消費されます。`INSERT INTO target SELECT ... FROM stream` は、ステートメントがコミットされたときにのみストリームを空にします。
- 同時に成功できるコンシューマは 1 つだけで、他の並行ステートメントはロールバックされます。

**Modes**

- Append-Only ストリームは INSERT のみをキャプチャし、追記が多いワークロードに最適です。
- Standard ストリームは、消費し続ける限り update と delete を出力します。遅れて到着した update は次回の実行まで保持されます。

**Hidden Columns**

- ストリームは `change$action`、`change$is_update`、`change$row_id` を公開します。これらを使うと、{{{ .lake }}} が各行をどのように記録したかを把握できます。
- ベーステーブルには、行の来歴をデバッグするために `_origin_version`、`_origin_block_id`、`_origin_block_row_num` が追加されます。

**Integrations**

- スケジュールされた増分ロード (load) には、ストリームを `task_history('<name>', <limit>)` と組み合わせて使用します。
- 最新の差分のみを消費したい場合は [`WITH CONSUME`](/tidb-cloud-lake/sql/task.md) を使用します。