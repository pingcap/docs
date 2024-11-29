---
title: ADMIN CHECKSUM TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN の使用法の概要。
category: reference
---

# 管理者チェックサムテーブル {#admin-checksum-table}

`ADMIN CHECKSUM TABLE`ステートメントは、テーブルのデータとインデックスの CRC64 チェックサムを計算します。

<CustomContent platform="tidb">

[チェックサム](/tidb-lightning/tidb-lightning-glossary.md#checksum)は、テーブル データと`table_id`などのプロパティに基づいて計算されます。つまり、データは同じだが`table_id`値が異なる 2 つのテーブルでは、チェックサムが異なります。

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 、 [TiDB データ移行](/dm/dm-overview.md) 、または[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)を使用してテーブルをインポートした後、データの整合性を検証するためにデフォルトで`ADMIN CHECKSUM TABLE <table>`実行されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[チェックサム](https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#checksum)は、 `table_id`などのテーブル データとプロパティに基づいて計算されます。つまり、データは同じだが`table_id`値が異なる 2 つのテーブルでは、チェックサムが異なります。

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してテーブルをインポートした後、データの整合性を検証するためにデフォルトで`ADMIN CHECKSUM TABLE <table>`実行されます。

</CustomContent>

## 概要 {#synopsis}

```ebnf+diagram
AdminChecksumTableStmt ::=
    'ADMIN' 'CHECKSUM' 'TABLE' TableNameList

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

テーブル`t1`を作成します:

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

`t1`にデータを挿入します:

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

`t1`のチェックサムを計算します。

```sql
ADMIN CHECKSUM TABLE t1;
```

出力は次のようになります。

```sql
+---------+------------+----------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor   | Total_kvs | Total_bytes |
+---------+------------+----------------------+-----------+-------------+
| test    | t1         | 10909174369497628533 |         3 |          75 |
+---------+------------+----------------------+-----------+-------------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
