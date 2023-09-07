---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH PRIVILEGES for the TiDB database.
---

# フラッシュ特典 {#flush-privileges}

ステートメント`FLUSH PRIVILEGES`は、権限テーブルから権限のメモリ内コピーを再ロードするように TiDB に指示します。 `mysql.user`などのテーブルを手動で編集した後、このステートメントを実行する必要があります。ただし、 `GRANT`や`REVOKE`などの特権ステートメントを使用した後は、このステートメントを実行する必要はありません。このステートメントを実行するには、 `RELOAD`権限が必要です。

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

TiDB の`FLUSH PRIVILEGES`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [助成金を表示する](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">
  -   [権限管理](/privilege-management.md)
</CustomContent>
