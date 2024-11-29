---
title: RENAME INDEX | TiDB SQL Statement Reference
summary: TiDB データベースでの RENAME INDEX の使用法の概要。
---

# インデックス名の変更 {#rename-index}

ステートメント`ALTER TABLE .. RENAME INDEX` 、既存のインデックスの名前を新しい名前に変更します。この操作は TiDB では即座に実行され、メタデータの変更のみが必要です。

## 概要 {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName RenameIndexSpec ( ',' RenameIndexSpec )*

RenameIndexSpec
         ::= 'RENAME' ( 'KEY' | 'INDEX' ) Identifier 'TO' Identifier
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL, INDEX col1 (c1));
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `col1` (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 RENAME INDEX col1 TO c1;
Query OK, 0 rows affected (0.09 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `c1` (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`RENAME INDEX`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックスを表示](/sql-statements/sql-statement-show-indexes.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
