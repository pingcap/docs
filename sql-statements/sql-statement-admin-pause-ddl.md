---
title: ADMIN PAUSE DDL JOBS
summary: TiDB データベースの ADMIN PAUSE DDL JOBS の使用法の概要。
---

# 管理者によるDDLジョブの一時停止 {#admin-pause-ddl-jobs}

`ADMIN PAUSE DDL`は実行中のDDLジョブを一時停止します。2 `job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行することで確認できます。

この文を使用すると、発行済みだがまだ実行が完了していないDDLジョブを一時停止できます。一時停止後、DDLジョブを実行するSQL文はすぐには戻りませんが、まだ実行中であるように見えます。すでに完了しているDDLジョブを一時停止しようとすると、列`RESULT`にエラー`DDL Job:90 not found`表示されます。これは、ジョブがDDL待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'PAUSE' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN PAUSE DDL JOBS`現在実行中のDDLジョブを一時停止し、ジョブが正常に一時停止されたかどうかを返します。ジョブは`ADMIN RESUME DDL JOBS`で再開できます。

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

一時停止に失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除き、DDL ジョブは一時停止されません。
> -   クラスタのアップグレード中は、実行中のDDLジョブが一時停止され、アップグレード中に開始されたDDLジョブも一時停止されます。アップグレード後、一時停止されていたすべてのDDLジョブは再開されます。アップグレード中の一時停止と再開の操作は自動的に実行されます。詳細は[TiDB スムーズアップグレード](/smooth-upgrade-tidb.md)ご覧ください。
> -   このステートメントは複数のDDLジョブを一時停止できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDLジョブの`job_id`のステートメントを取得できます。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除き、DDL ジョブは一時停止されません。
> -   クラスタのアップグレード中は、実行中のDDLジョブが一時停止され、アップグレード中に開始されたDDLジョブも一時停止されます。アップグレード後、一時停止されていたすべてのDDLジョブは再開されます。アップグレード中の一時停止と再開の操作は自動的に実行されます。詳細は[TiDB スムーズアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)ご覧ください。
> -   このステートメントは複数のDDLジョブを一時停止できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDLジョブの`job_id`のステートメントを取得できます。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
-   [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)
