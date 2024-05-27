---
title: ADMIN CHECK [TABLE|INDEX] | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN の使用法の概要。
category: reference
---

# 管理者チェック [テーブル|インデックス] {#admin-check-table-index}

`ADMIN CHECK [TABLE|INDEX]`ステートメントは、テーブルとインデックスのデータの一貫性をチェックします。

以下はサポートされていません:

-   [FOREIGN KEY制約](/foreign-key.md)チェックしています。
-   [クラスター化された主キー](/clustered-indexes.md)が使用されている場合は、PRIMARY KEY インデックスをチェックします。

`ADMIN CHECK [TABLE|INDEX]`問題が見つかった場合は、インデックスを削除して再作成することで解決できます。問題が解決しない場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support)実行できます。

## 原則 {#principles}

`ADMIN CHECK TABLE`ステートメントは、テーブルをチェックするために次の手順を実行します。

1.  各インデックスについて、インデックス内のレコード数がテーブル内のレコード数と同じかどうかを確認します。

2.  各インデックスについて、各行の値をループし、その値をテーブル内の値と比較します。

`ADMIN CHECK INDEX`ステートメントを使用すると、指定されたインデックスのみがチェックされます。

## 概要 {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

`tbl_name`テーブル内のすべてのデータと対応するインデックスの一貫性をチェックするには、 `ADMIN CHECK TABLE`を使用します。

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データが不整合であることを示すエラー メッセージが返されます。

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

上記のステートメントは、 `tbl_name`のテーブル内の`idx_name`番目のインデックスに対応する列データとインデックス データの一貫性をチェックするために使用されます。一貫性チェックに合格すると、空の結果が返されます。それ以外の場合は、データが不一致であることを示すエラー メッセージが返されます。

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

上記のステートメントは、データ範囲（チェック対象）を指定して、 `tbl_name`のテーブルの`idx_name`のインデックスに対応する列データとインデックス データの整合性をチェックするために使用されます。整合性チェックに合格すると、空の結果が返されます。それ以外の場合は、データが不整合であることを示すエラー メッセージが返されます。

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN REPAIR`](/sql-statements/sql-statement-admin.md#admin-repair-statement)
