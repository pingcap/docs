---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: TiDB データベースの FLUSH TABLES の使用法の概要。
---

# フラッシュテーブル {#flush-tables}

このステートメントはMySQLとの互換性のために含まれています。TiDBでは有効な用途はありません。

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

## MySQLの互換性 {#mysql-compatibility}

-   TiDBにはMySQLのようなテーブルキャッシュの概念がありません。そのため、 `FLUSH TABLES`解析されますが、互換性のためにTiDBでは無視されます。
-   ステートメント`FLUSH TABLES WITH READ LOCK`エラーを生成します。これは、TiDBが現在テーブルのロックをサポートしていないためです。この目的には、代わりに[歴史的な読み物](/read-historical-data.md)使用することをお勧めします。

## 参照 {#see-also}

-   [履歴データを読む](/read-historical-data.md)
