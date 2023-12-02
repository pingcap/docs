---
title: ADMIN PAUSE DDL JOBS
summary: An overview of the usage of ADMIN PAUSE DDL JOBS for the TiDB database.
---

# 管理者による DDL ジョブの一時停止 {#admin-pause-ddl-jobs}

`ADMIN PAUSE DDL`指定すると、実行中の DDL ジョブを一時停止できます。 `job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)を実行すると見つかります。

このステートメントを使用すると、発行されたものの実行がまだ完了していない DDL ジョブを一時停止できます。一時停止後、DDL ジョブを実行する SQL ステートメントはすぐには戻りませんが、まだ実行中であるように見えます。すでに完了した DDL ジョブを一時停止しようとすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN PAUSE DDL JOBS`現在実行中の DDL ジョブを一時停止し、ジョブが正常に一時停止されたかどうかを返します。ジョブは`ADMIN RESUME DDL JOBS`までに再開できます。

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

一時停止が失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除いて DDL ジョブは一時停止されません。
> -   クラスターのアップグレード中、進行中の DDL ジョブは一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されていたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開の操作は自動的に行われます。詳細は[TiDB のスムーズなアップグレード](/smooth-upgrade-tidb.md)を参照してください。
> -   このステートメントは複数の DDL ジョブを一時停止できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除いて DDL ジョブは一時停止されません。
> -   クラスターのアップグレード中、進行中の DDL ジョブは一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されていたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開の操作は自動的に行われます。詳細は[TiDB のスムーズなアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)を参照してください。
> -   このステートメントは複数の DDL ジョブを一時停止できます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDL ジョブの`job_id`を取得できます。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
