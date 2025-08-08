---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN CANCEL DDL の使用法の概要。
category: reference
---

# 管理者によるDDLのキャンセル {#admin-cancel-ddl}

`ADMIN CANCEL DDL`文は実行中のDDLジョブをキャンセルします。3 `job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行することで確認できます。

`ADMIN CANCEL DDL`文を使用すると、コミットされているもののまだ実行が完了していないDDLジョブをキャンセルすることもできます。キャンセル後、DDLジョブを実行するSQL文は`ERROR 8214 (HY000): Cancelled DDL job`エラーを返します。すでに完了しているDDLジョブをキャンセルした場合は、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブがDDL待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminCancelDDLStmt ::=
    'ADMIN' 'CANCEL' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

現在実行中の DDL ジョブをキャンセルし、対応するジョブが正常にキャンセルされたかどうかを返すには、 `ADMIN CANCEL DDL JOBS`使用します。

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

ジョブをキャンセルする操作が失敗した場合、具体的な理由が表示されます。

> **注記：**
>
> -   バージョン6.2.0より前では、この操作のみがDDLジョブをキャンセルでき、他のすべての操作や環境変更（マシンの再起動やクラスタの再起動など）ではこれらのジョブをキャンセルできませんでした。バージョン6.2.0以降では、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを使用して実行中のDDLジョブを強制終了することでキャンセルできるようになりました。
> -   この操作では、複数のDDLジョブを同時にキャンセルできます。1 ステートメントを使用して、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ジョブのIDを取得できます。
> -   キャンセルするジョブが完了している場合、キャンセル操作は失敗します。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
