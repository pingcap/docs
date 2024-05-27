---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN CANCEL DDL の使用法の概要。
category: reference
---

# 管理者はDDLをキャンセルします {#admin-cancel-ddl}

`ADMIN CANCEL DDL`ステートメントを使用すると、実行中の DDL ジョブをキャンセルできます。 `job_id`は、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行することで見つかります。

`ADMIN CANCEL DDL`ステートメントを使用すると、コミットされているがまだ実行が完了していない DDL ジョブをキャンセルすることもできます。キャンセル後、DDL ジョブを実行する SQL ステートメントは`ERROR 8214 (HY000): Cancelled DDL job`エラーを返します。すでに完了している DDL ジョブをキャンセルすると、 `RESULT`列に`DDL Job:90 not found`エラーが表示されます。これは、ジョブが DDL 待機キューから削除されたことを示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

現在実行中の DDL ジョブをキャンセルし、対応するジョブが正常にキャンセルされたかどうかを返すには、 `ADMIN CANCEL DDL JOBS`使用します。

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

ジョブをキャンセルする操作が失敗した場合は、具体的な理由が表示されます。

> **注記：**
>
> -   v6.2.0 より前では、この操作のみが DDL ジョブをキャンセルでき、他のすべての操作や環境変更 (マシンの再起動やクラスターの再起動など) ではこれらのジョブをキャンセルできませんでした。v6.2.0 以降では、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを使用して、進行中の DDL ジョブを強制終了してキャンセルすることもできます。
> -   この操作では、複数の DDL ジョブを同時にキャンセルできます。1 ステートメントを使用して[`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) DDL ジョブの ID を取得できます。
> -   キャンセルするジョブが完了している場合、キャンセル操作は失敗します。

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
