---
title: ADMIN RESUME DDL JOBS
summary: An overview of the usage of ADMIN RESUME DDL for the TiDB database.
---

# 管理者の DDL ジョブの履歴書 {#admin-resume-ddl-jobs}

`ADMIN RESUME DDL`指定すると、一時停止した DDL ジョブを再開できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)を実行すると、 `job_id`見つけることができます。

このステートメントを使用して、一時停止した DDL ジョブを再開できます。再開が完了した後も、DDL ジョブを実行する SQL ステートメントは実行中として表示され続けます。すでに完了した DDL ジョブを再開しようとすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN RESUME DDL JOBS` 、現在一時停止されている DDL ジョブを再開し、ジョブが正常に再開されたかどうかを返します。

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

再開が失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   クラスターのアップグレード中、進行中の DDL ジョブは一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されていたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開の操作は自動的に行われます。詳細は[TiDB のスムーズなアップグレード](/smooth-upgrade-tidb.md)を参照してください。
> -   このステートメントにより、複数の DDL ジョブを再開できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。
> -   他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`を報告します。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   クラスターのアップグレード中、進行中の DDL ジョブは一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されていたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開の操作は自動的に行われます。詳細は[TiDB のスムーズなアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)を参照してください。
> -   このステートメントにより、複数の DDL ジョブを再開できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。
> -   他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`を報告します。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
