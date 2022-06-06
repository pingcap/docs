---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH PRIVILEGES for the TiDB database.
---

# フラッシュ特権 {#flush-privileges}

このステートメントは、TiDBをトリガーして、特権テーブルから特権のメモリ内コピーを再ロードします。 `mysql.user`などのテーブルを手動で編集した後、 `FLUSH PRIVILEGES`を実行する必要があります。 `GRANT`や`REVOKE`などの特権ステートメントを使用した後は、このステートメントを実行する必要はありません。このステートメントを実行するには、 `RELOAD`特権が必要です。

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
|   LogTypeOpt 'LOGS'
|   TableOrTables TableNameListOpt WithReadLockOpt
```

## 例 {#examples}

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [権限管理](/privilege-management.md)
