---
title: CREATE TABLE LIKE | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE TABLE LIKE の使用法の概要。
---

# 次のようなテーブルを作成する {#create-table-like}

このステートメントは、データをコピーせずに、既存のテーブルの定義をコピーします。

## 概要 {#synopsis}

```ebnf+diagram
CreateTableLikeStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName LikeTableWithOrWithoutParen OnCommitOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

LikeTableWithOrWithoutParen ::=
    'LIKE' TableName
|   '(' 'LIKE' TableName ')'

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL);
Query OK, 0 rows affected (0.13 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

## 分割前の地域 {#pre-split-region}

コピー元のテーブルに`PRE_SPLIT_REGIONS`属性が定義されている場合、 `CREATE TABLE LIKE`文で作成されたテーブルはこの属性を継承し、新しいテーブルのリージョンは分割されます。5の詳細については、 `PRE_SPLIT_REGIONS` [`CREATE TABLE`文](/sql-statements/sql-statement-create-table.md)参照してください。

## MySQLの互換性 {#mysql-compatibility}

TiDBの`CREATE TABLE LIKE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
