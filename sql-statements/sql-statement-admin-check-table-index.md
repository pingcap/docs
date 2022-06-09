---
title: ADMIN CHECK [TABLE|INDEX] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# 管理者チェック[テーブル|インデックス] {#admin-check-table-index}

`ADMIN CHECK [TABLE|INDEX]`ステートメントは、テーブルとインデックスのデータの整合性をチェックします。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

`tbl_name`テーブル内のすべてのデータと対応するインデックスの整合性を確認するには、 `ADMIN CHECK TABLE`を使用します。

{{< copyable "" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラーメッセージが返されます。

{{< copyable "" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

上記のステートメントは、 `tbl_name`テーブルの`idx_name`インデックスに対応する列データとインデックスデータの整合性をチェックするために使用されます。整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラーメッセージが返されます。

{{< copyable "" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

上記のステートメントは、 `tbl_name`のテーブルの`idx_name`のインデックスに対応する列データとインデックスデータの整合性をチェックするために使用され、データ範囲（チェック対象）が指定されています。整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データに一貫性がないことを示すエラーメッセージが返されます。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [`ADMIN REPAIR`](/sql-statements/sql-statement-admin.md#admin-repair-statement)
