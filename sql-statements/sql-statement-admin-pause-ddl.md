---
title: ADMIN PAUSE DDL JOBS
summary: TiDB データベースの ADMIN PAUSE DDL JOBS の使用法の概要。
---

# 管理者による DDL ジョブの一時停止 {#admin-pause-ddl-jobs}

`ADMIN PAUSE DDL`使用すると、実行中の DDL ジョブを一時停止できます。 `job_id`は、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行すると見つかります。

このステートメントを使用すると、発行されたがまだ実行が完了していない DDL ジョブを一時停止できます。一時停止後、DDL ジョブを実行する SQL ステートメントはすぐには返されませんが、まだ実行されているように見えます。すでに完了している DDL ジョブを一時停止しようとすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'PAUSE' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN PAUSE DDL JOBS`現在実行中の DDL ジョブを一時停止し、ジョブが正常に一時停止されたかどうかを返します。ジョブは`ADMIN RESUME DDL JOBS`で再開できます。

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

一時停止に失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除いて DDL ジョブは一時停止されません。
> -   クラスターのアップグレード中は、進行中の DDL ジョブが一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開操作は自動的に実行されます。詳細については、 [TiDB スムーズアップグレード](/smooth-upgrade-tidb.md)参照してください。
> -   このステートメントは複数の DDL ジョブを一時停止できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)を使用して、DDL ジョブの`job_id`取得できます。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   このステートメントは DDL ジョブを一時停止できますが、他の操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、クラスターのアップグレードを除いて DDL ジョブは一時停止されません。
> -   クラスターのアップグレード中は、進行中の DDL ジョブが一時停止され、アップグレード中に開始された DDL ジョブも一時停止されます。アップグレード後、一時停止されたすべての DDL ジョブが再開されます。アップグレード中の一時停止および再開操作は自動的に実行されます。詳細については、 [TiDB スムーズアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)参照してください。
> -   このステートメントは複数の DDL ジョブを一時停止できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)を使用して、DDL ジョブの`job_id`取得できます。

</CustomContent>

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
