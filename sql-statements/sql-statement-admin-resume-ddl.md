---
title: ADMIN RESUME DDL JOBS
summary: TiDB データベースの ADMIN RESUME DDL の使用法の概要。
---

# 管理者履歴書DDLジョブ {#admin-resume-ddl-jobs}

`ADMIN RESUME DDL`使用すると、一時停止中のDDLジョブを再開できます。2 は`job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行すると確認できます。

このステートメントを使用すると、一時停止中のDDLジョブを再開できます。再開が完了した後も、DDLジョブを実行するSQL文は実行中として表示されます。すでに完了しているDDLジョブを再開しようとすると、列`RESULT`にエラー`DDL Job:90 not found`が表示されます。これは、ジョブがDDL待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminResumeDDLStmt ::=
    'ADMIN' 'RESUME' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

`ADMIN RESUME DDL JOBS`現在一時停止中の DDL ジョブを再開し、ジョブが正常に再開されたかどうかを返します。

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

再開に失敗した場合は、失敗の具体的な理由が表示されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   クラスタのアップグレード中は、実行中のDDLジョブが一時停止され、アップグレード中に開始されたDDLジョブも一時停止されます。アップグレード後、一時停止されていたすべてのDDLジョブは再開されます。アップグレード中の一時停止と再開の操作は自動的に実行されます。詳細は[TiDB スムーズアップグレード](/smooth-upgrade-tidb.md)ご覧ください。
> -   このステートメントは複数のDDLジョブを再開できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDLジョブの`job_id`のステートメントを取得できます。
> -   その他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`報告します。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   クラスタのアップグレード中は、実行中のDDLジョブが一時停止され、アップグレード中に開始されたDDLジョブも一時停止されます。アップグレード後、一時停止されていたすべてのDDLジョブは再開されます。アップグレード中の一時停止と再開の操作は自動的に実行されます。詳細は[TiDB スムーズアップグレード](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)ご覧ください。
> -   このステートメントは複数のDDLジョブを再開できます。1 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して、DDLジョブの`job_id`のステートメントを取得できます。
> -   その他のステータス ( `paused`以外) の DDL ジョブは再開できず、再開操作は失敗します。
> -   ジョブを複数回再開しようとすると、TiDB はエラー`Error Number: 8261`報告します。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
-   [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)
