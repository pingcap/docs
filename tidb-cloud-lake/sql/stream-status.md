---
title: STREAM_STATUS
summary: 指定した stream のステータスに関する情報を提供し、`true` または `false` を取りうる単一カラムの結果 (`has_data`) を返します。
---

# STREAM_STATUS

指定した stream のステータスに関する情報を提供し、`true` または `false` を取りうる単一カラムの結果（`has_data`）を返します。

- `true`: stream に change data capture レコードが**含まれている可能性がある**ことを示します。
- `false`: 現在、stream に change data capture レコードが含まれていないことを示します。

> **Note:**
>
> 結果 (`has_data`) に `true` が含まれていても、change data capture レコードが確実に存在することを保証するものではありません。テーブルの compact 操作の実行など、他の操作によっても、実際には change data capture レコードが存在しない場合でも `true` になることがあります。

> **Note:**
>
> タスク内で `STREAM_STATUS` を使用する場合、stream を参照するときはデータベース名を含める必要があります（例: `STREAM_STATUS('mydb.stream_name')`）。

## 構文 {#syntax}

```sql
SELECT * FROM STREAM_STATUS('<database_name>.<stream_name>');
-- OR
SELECT * FROM STREAM_STATUS('<stream_name>');  -- Uses current database
```

## 例 {#examples}

```sql
-- Create a table 't' with a column 'c'
CREATE TABLE t (c int);

-- Create a stream 's' on the table 't'
CREATE STREAM s ON TABLE t;

-- Check the initial status of the stream 's'
SELECT * FROM STREAM_STATUS('s');

-- The result should be 'false' indicating no change data capture records initially
┌──────────┐
│ has_data │
├──────────┤
│ false    │
└──────────┘

-- Insert a value into the table 't'
INSERT INTO t VALUES (1);

-- Check the updated status of the stream 's' after the insertion
SELECT * FROM STREAM_STATUS('s');

-- The result should now be 'true' indicating the presence of change data capture records
┌──────────┐
│ has_data │
├──────────┤
│ true     │
└──────────┘

-- Example with database name specified
SELECT * FROM STREAM_STATUS('mydb.s');
```