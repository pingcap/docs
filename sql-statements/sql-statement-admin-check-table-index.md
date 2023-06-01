---
title: ADMIN CHECK [TABLE|INDEX] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# 管理者チェック [表|索引] {#admin-check-table-index}

`ADMIN CHECK [TABLE|INDEX]`ステートメントは、テーブルとインデックスのデータの整合性をチェックします。 [<a href="/foreign-key.md">FOREIGN KEY 制約</a>](/foreign-key.md)チェックには対応していません。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

`tbl_name`テーブル内のすべてのデータと対応するインデックスの一貫性をチェックするには、 `ADMIN CHECK TABLE`使用します。

{{< copyable "" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラー メッセージが返されます。

{{< copyable "" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

上記のステートメントは、 `tbl_name`テーブルの`idx_name`インデックスに対応する列データとインデックス データの整合性をチェックするために使用されます。整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラー メッセージが返されます。

{{< copyable "" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

上記文は、 `tbl_name`テーブルの`idx_name`インデックスに対応する列データとインデックスデータの整合性を、データ範囲（チェック対象）を指定してチェックするために使用します。整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラー メッセージが返されます。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-admin.md#admin-repair-statement">`ADMIN REPAIR`</a>](/sql-statements/sql-statement-admin.md#admin-repair-statement)
