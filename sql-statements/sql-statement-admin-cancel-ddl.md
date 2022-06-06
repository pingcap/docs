---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN CANCEL DDL for the TiDB database.
category: reference
---

# ADMIN CANCEL DDL {#admin-cancel-ddl}

`ADMIN CANCEL DDL`ステートメントを使用すると、実行中のDDLジョブをキャンセルできます。 `job_id`は、 `ADMIN SHOW DDL JOBS`を実行することで見つけることができます。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 例 {#examples}

現在実行中のDDLジョブをキャンセルし、対応するジョブが正常にキャンセルされたかどうかを返すには、 `ADMIN CANCEL DDL JOBS`を使用します。

{{< copyable "" >}}

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

操作がジョブのキャンセルに失敗した場合、特定の理由が表示されます。

> **ノート：**
>
> -   この操作のみがDDLジョブをキャンセルできます。他のすべての操作および環境の変更（マシンの再起動やクラスタの再起動など）では、これらのジョブをキャンセルできません。
> -   この操作により、複数のDDLジョブを同時にキャンセルできます。 `ADMIN SHOW DDL JOBS`ステートメントを使用してDDLジョブのIDを取得できます。
> -   キャンセルしたいジョブが終了した場合、キャンセル操作は失敗します。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
