---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: TiDB データベースの FLUSH PRIVILEGES の使用法の概要。
---

# フラッシュ権限 {#flush-privileges}

文`FLUSH PRIVILEGES` 、TiDB に権限テーブルからメモリ内の権限コピーを再ロードするよう指示します。 `mysql.user`のようなテーブルを手動で編集した後は、この文を実行する必要があります。ただし、 `GRANT`や`REVOKE`ような権限文を使用した後は、この文を実行する必要はありません。この文を実行するには、 `RELOAD`権限が必要です。

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
|   LogTypeOpt 'LOGS'
|   TableOrTables TableNameListOpt WithReadLockOpt
```

## 例 {#examples}

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`FLUSH PRIVILEGES`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [ショーグラント](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
