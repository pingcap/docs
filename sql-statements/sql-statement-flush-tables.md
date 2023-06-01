---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH TABLES for the TiDB database.
---

# フラッシュテーブル {#flush-tables}

このステートメントは、MySQL との互換性のために組み込まれています。 TiDB では効果的な使用法がありません。

## あらすじ {#synopsis}

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

## MySQLの互換性 {#mysql-compatibility}

-   TiDB には、MySQL のようなテーブル キャッシュの概念がありません。したがって、 `FLUSH TABLES`は解析されますが、TiDB では互換性のために無視されます。
-   TiDB は現在テーブルのロックをサポートしていないため、ステートメント`FLUSH TABLES WITH READ LOCK`ではエラーが発生します。この目的には代わりに[履歴読み取り](/read-historical-data.md)を使用することをお勧めします。

## こちらも参照 {#see-also}

-   [履歴データの読み取り](/read-historical-data.md)
