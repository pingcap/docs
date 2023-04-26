---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH TABLES for the TiDB database.
---

# フラッシュテーブル {#flush-tables}

このステートメントは、MySQL との互換性のために含まれています。 TiDB では有効な使い方がありません。

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

## MySQL の互換性 {#mysql-compatibility}

-   TiDB には、MySQL のようなテーブル キャッシュの概念がありません。したがって、 `FLUSH TABLES`は解析されますが、互換性のために TiDB では無視されます。
-   TiDB は現在テーブルのロックをサポートしていないため、ステートメント`FLUSH TABLES WITH READ LOCK`エラーを生成します。代わりに、この目的のために[過去の読み取り](/read-historical-data.md)を使用することをお勧めします。

## こちらもご覧ください {#see-also}

-   [履歴データの読み取り](/read-historical-data.md)
