---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: TiDB データベースの FLUSH TABLES の使用法の概要。
---

# フラッシュテーブル {#flush-tables}

このステートメントは、MySQL との互換性のために含まれています。TiDB では有効な使用方法はありません。

## 概要 {#synopsis}

```ebnf+diagram
FlushStmt ::=
    'FLUSH' NoWriteToBinLogAliasOpt FlushOption

NoWriteToBinLogAliasOpt ::=
    ( 'NO_WRITE_TO_BINLOG' | 'LOCAL' )?

FlushOption ::=
    'PRIVILEGES'
|   'STATUS'
|    'TIDB' 'PLUGINS' PluginNameList
|    'HOSTS'
|    LogTypeOpt 'LOGS'
|    TableOrTables TableNameListOpt WithReadLockOpt

LogTypeOpt ::=
    ( 'BINARY' | 'ENGINE' | 'ERROR' | 'GENERAL' | 'SLOW' )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameListOpt ::=
    TableNameList?

WithReadLockOpt ::=
    ( 'WITH' 'READ' 'LOCK' )?
```

## 例 {#examples}

```sql
mysql> FLUSH TABLES;
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH TABLES WITH READ LOCK;
ERROR 1105 (HY000): FLUSH TABLES WITH READ LOCK is not supported.  Please use @@tidb_snapshot
```

## MySQL 互換性 {#mysql-compatibility}

-   TiDB には、MySQL のようなテーブル キャッシュの概念はありません。したがって、 `FLUSH TABLES`解析されますが、互換性のために TiDB では無視されます。
-   TiDB は現在テーブルのロックをサポートしていないため、ステートメント`FLUSH TABLES WITH READ LOCK`エラーが発生します。この目的には代わりに[歴史的な読み物](/read-historical-data.md)を使用することをお勧めします。

## 参照 {#see-also}

-   [履歴データを読む](/read-historical-data.md)
