---
title: TRUNCATE TABLE
summary: テーブルのスキーマを保持したまま、テーブルからすべてのデータを削除します。テーブル内のすべての行を削除し、同じカラムと制約を持つ空のテーブルにします。なお、テーブルに割り当てられたディスク領域は解放されません。
---

# TRUNCATE TABLE

テーブルのスキーマを保持したまま、テーブルからすべてのデータを削除します。テーブル内のすべての行を削除し、同じカラムと制約を持つ空のテーブルにします。なお、テーブルに割り当てられたディスク領域は解放されません。

関連情報: [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md)

## 構文 {#syntax}

```sql
TRUNCATE TABLE [ <database_name>. ]table_name
```

## 例 {#examples}

```sql
root@localhost> CREATE TABLE test_truncate(a BIGINT UNSIGNED, b VARCHAR);
Processed in (0.027 sec)

root@localhost> INSERT INTO test_truncate(a,b) VALUES(1234, 'datalake');
1 rows affected in (0.060 sec)

root@localhost> SELECT * FROM test_truncate;

SELECT
  *
FROM
  test_truncate

┌───────────────────┐
│    a   │     b    │
│ UInt64 │  String  │
├────────┼──────────┤
│   1234 │ datalake │
└───────────────────┘
1 row in 0.019 sec. Processed 1 rows, 1B (53.26 rows/s, 17.06 KiB/s)

root@localhost> TRUNCATE TABLE test_truncate;

TRUNCATE TABLE test_truncate

0 row in 0.047 sec. Processed 0 rows, 0B (0 rows/s, 0B/s)

root@localhost> SELECT * FROM test_truncate;

SELECT
  *
FROM
  test_truncate

0 row in 0.017 sec. Processed 0 rows, 0B (0 rows/s, 0B/s)
```