---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH PRIVILEGES for the TiDB database.
---

# フラッシュ特典 {#flush-privileges}

このステートメントは、TiDB をトリガーして、権限テーブルから権限のメモリ内コピーを再ロードします。 `mysql.user`などのテーブルを手動で編集した後、 `FLUSH PRIVILEGES`を実行する必要があります。 `GRANT`や`REVOKE`などの特権ステートメントを使用した後は、このステートメントを実行する必要はありません。このステートメントを実行するには、 `RELOAD`権限が必要です。

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

このステートメントは、MySQL と完全な互換性があると理解されています。 GitHub では互換性の違いは[問題を通じて報告されました](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## こちらも参照 {#see-also}

-   [助成金を表示する](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
