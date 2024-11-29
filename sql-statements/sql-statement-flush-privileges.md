---
title: FLUSH PRIVILEGES | TiDB SQL Statement Reference
summary: TiDB データベースの FLUSH PRIVILEGES の使用法の概要。
---

# フラッシュ権限 {#flush-privileges}

ステートメント`FLUSH PRIVILEGES`は、権限テーブルから権限のメモリ内コピーを再ロードするように TiDB に指示します。 `mysql.user`などのテーブルを手動で編集した後は、このステートメントを実行する必要があります。ただし、 `GRANT`や`REVOKE`などの権限ステートメントを使用した後は、このステートメントを実行する必要はありません。このステートメントを実行するには、 `RELOAD`権限が必要です。

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

## MySQL 互換性 {#mysql-compatibility}

TiDB の`FLUSH PRIVILEGES`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [ショーグラント](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
