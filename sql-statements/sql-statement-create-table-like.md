---
title: CREATE TABLE LIKE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE TABLE LIKE for the TiDB database.
---

# 次のようなテーブルを作成します {#create-table-like}

このステートメントは、データをコピーせずに、既存のテーブルの定義をコピーします。

## あらすじ {#synopsis}

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

## 分割前の領域 {#pre-split-region}

コピーするテーブルが`PRE_SPLIT_REGIONS`属性で定義されている場合、 `CREATE TABLE LIKE`ステートメントで作成されたテーブルはこの属性を継承し、新しいテーブルのリージョンが分割されます。 `PRE_SPLIT_REGIONS`の詳細については、 [`CREATE TABLE`ステートメント](/sql-statements/sql-statement-create-table.md)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

TiDB の`CREATE TABLE LIKE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
