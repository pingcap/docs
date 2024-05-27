---
title: ADMIN RESUME DDL JOBS
summary: TiDB データベースの ADMIN RESUME DDL の使用法の概要。
---

# 管理者履歴書DDLジョブ {#admin-resume-ddl-jobs}

`ADMIN RESUME DDL`すると、一時停止された DDL ジョブを再開できます。 `job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行すると見つかります。

このステートメントを使用して、一時停止された DDL ジョブを再開できます。再開が完了すると、DDL ジョブを実行する SQL ステートメントは引き続き実行中として表示されます。すでに完了している DDL ジョブを再開しようとすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN RESUME DDL JOBS`現在一時停止されている DDL ジョブを再開し、ジョブが正常に再開されたかどうかを返します。

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

再開が失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   クラスターのアップグレード中は、進行中の DDL ジョブが一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開操作は自動的に実行されます。詳細については、 [TiDB スムーズアップグレード](/smooth-upgrade-tidb.md)を参照してください。
> -   このステートメントは複数の DDL ジョブを再開できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。
> -   その他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`を報告します。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   クラスターのアップグレード中は、進行中の DDL ジョブが一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開操作は自動的に実行されます。詳細については、 [TiDB スムーズアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)を参照してください。
> -   このステートメントは複数の DDL ジョブを再開できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。
> -   その他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`を報告します。

</CustomContent>

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
