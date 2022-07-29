---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH TABLES for the TiDB database.
---

# フラッシュテーブル {#flush-tables}

このステートメントは、MySQLとの互換性のために含まれています。 TiDBでは効果的な使用法はありません。

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

-   TiDBには、MySQLのようなテーブルキャッシュの概念がありません。したがって、 `FLUSH TABLES`は解析されますが、互換性のためにTiDBでは無視されます。
-   TiDBは現在テーブルのロックをサポートしていないため、ステートメント`FLUSH TABLES WITH READ LOCK`はエラーを生成します。代わりに、この目的で[歴史的な読み取り](/read-historical-data.md)を使用することをお勧めします。

## も参照してください {#see-also}

-   [履歴データを読む](/read-historical-data.md)
