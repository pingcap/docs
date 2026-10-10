---
title: CREATE STREAM
summary: ストリームを作成します。
---

# CREATE STREAM

ストリームを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] [ <database_name>. ]<stream_name>
  ON TABLE [ <database_name>. ]<table_name>
  [ AT ( { TIMESTAMP => <timestamp> | SNAPSHOT => '<snapshot_id>' | STREAM => <existing_stream_name> } ) ]
  [ APPEND_ONLY = true | false ]
  [ COMMENT = '<comment>' ]
```

| パラメーター           | 説明                                                                                                                                                                                                                                                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `< database_name >` | ストリームは、テーブルやビューと同様に、特定のデータベースに属するオブジェクトとして扱われます。CREATE STREAM では、ストリームと関連付けられるテーブルで異なるデータベースを指定できます。データベースを明示的に指定しない場合、現在のデータベースが作成するストリームのデータベースとして使用されます。               |
| AT                  | `AT` の後に `TIMESTAMP =>` または `SNAPSHOT =>` を指定すると、指定した過去時点の timestamp または snapshot ID 以降のデータ変更を含むストリームを作成できます。`AT` の後に `STREAM =>` を指定すると、既存のストリームと同一の新しいストリームを作成でき、キャプチャされたデータ変更も同じ内容で保持されます。 |
| APPEND_ONLY         | `true` に設定すると、ストリームは `Append-Only` モードで動作します。`false` に設定すると、`Standard` モードで動作します。デフォルトは `true` です。ストリームの動作モードの詳細については、[How Stream Works](/tidb-cloud-lake/sql/stream.md#stream-management) を参照してください。                                        |

## 例 {#examples}

次の例では、`orders` テーブル内の変更を監視するために、`order_changes` という名前のストリームを作成します。

```sql
-- Create a table named 'orders'
CREATE TABLE orders (
    order_id INT,
    product_name VARCHAR,
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a stream named 'order_changes' for the table 'orders'
CREATE STREAM order_changes ON TABLE orders;

-- Insert order 1001 to the table 'orders'
INSERT INTO orders (order_id, product_name, quantity) VALUES (1001, 'Product A', 10);

-- Insert order 1002 to the table 'orders'
INSERT INTO orders (order_id, product_name, quantity) VALUES (1002, 'Product B', 20);

-- Retrieve all records from the 'order_changes' stream
SELECT * FROM order_changes;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
│            1001 │ Product A        │              10 │ 2024-03-28 03:24:16.539178 │ INSERT        │ false            │ b93a15e694db4134ab5a23afa8c92b20000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

次の例では、`AT` パラメーターを使用して、`order_changes` と同じデータ変更を含む `order_changes_copy` という名前の新しいストリームを作成します。

```sql
-- Create a stream 'order_changes_copy' on the 'orders' table, copying data changes from 'order_changes'
CREATE STREAM order_changes_copy ON TABLE orders AT (STREAM => order_changes);

-- Retrieve all records from the 'order_changes_copy' stream
SELECT * FROM order_changes_copy;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
│            1001 │ Product A        │              10 │ 2024-03-28 03:24:16.539178 │ INSERT        │ false            │ b93a15e694db4134ab5a23afa8c92b20000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

次の例では、`orders` テーブルに対して 2 つのストリームを作成します。各ストリームはそれぞれ `AT` パラメーターを使用して、特定の snapshot ID または timestamp 以降のデータ変更を取得します。

```sql
-- Retrieve snapshot and timestamp information from the 'orders' table
SELECT snapshot_id, timestamp from FUSE_SNAPSHOT('default','orders');

┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ f7f57c7d07f445a68e4aa53fa2578bbb │ 2024-03-28 03:24:16.633721 │
│ 11b9d81eabc94c7da648908f0ba313a1 │ 2024-03-28 03:24:16.611835 │
└───────────────────────────────────────────────────────────────┘

-- Create a stream 'order_changes_after_snapshot' on the 'orders' table, capturing data changes after a specific snapshot
CREATE STREAM order_changes_after_snapshot ON TABLE orders AT (SNAPSHOT => '11b9d81eabc94c7da648908f0ba313a1');

-- Query the 'order_changes_after_snapshot' stream to view data changes captured after the specified snapshot
SELECT * FROM order_changes_after_snapshot;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Create a stream 'order_changes_after_timestamp' on the 'orders' table, capturing data changes after a specific timestamp
CREATE STREAM order_changes_after_timestamp ON TABLE orders AT (TIMESTAMP => '2024-03-28 03:24:16.611835'::TIMESTAMP);

-- Query the 'order_changes_after_timestamp' stream to view data changes captured after the specified timestamp
SELECT * FROM order_changes_after_timestamp;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```