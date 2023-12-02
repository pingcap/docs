---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN CANCEL DDL for the TiDB database.
category: reference
---

# 管理者が DDL をキャンセル {#admin-cancel-ddl}

`ADMIN CANCEL DDL`ステートメントを使用すると、実行中の DDL ジョブをキャンセルできます。 `job_id` [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)を実行すると見つかります。

`ADMIN CANCEL DDL`ステートメントを使用すると、コミットされたがまだ実行が完了していない DDL ジョブをキャンセルすることもできます。キャンセル後、DDL ジョブを実行する SQL ステートメントは`ERROR 8214 (HY000): Cancelled DDL job`エラーを返します。すでに完了した DDL ジョブをキャンセルすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

現在実行中の DDL ジョブをキャンセルし、対応するジョブが正常にキャンセルされたかどうかを返すには、 `ADMIN CANCEL DDL JOBS`を使用します。

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

操作がジョブのキャンセルに失敗した場合は、特定の理由が表示されます。

> **注記：**
>
> -   DDL ジョブをキャンセルできるのはこの操作のみです。他のすべての操作や環境の変更 (マシンの再起動やクラスターの再起動など) では、これらのジョブをキャンセルすることはできません。
> -   この操作により、複数の DDL ジョブを同時にキャンセルできます。 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)ステートメントを使用して DDL ジョブの ID を取得できます。
> -   キャンセルしたいジョブが終了している場合、キャンセル操作は失敗します。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
