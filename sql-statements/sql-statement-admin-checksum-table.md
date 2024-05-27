---
title: ADMIN CHECKSUM TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN の使用法の概要。
category: reference
---

# 管理者チェックサムテーブル {#admin-checksum-table}

`ADMIN CHECKSUM TABLE`ステートメントは、テーブルのデータとインデックスの CRC64 チェックサムを計算します。このステートメントは、TiDB Lightningなどのプログラムによって、インポート操作が正常に完了したことを確認するために使用されます。

## 概要 {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

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
