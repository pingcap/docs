---
title: SHOW ERRORS | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW ERRORS の使用法の概要。
---

# エラーを表示 {#show-errors}

この文は、以前に実行された文のエラーを表示します。文が正常に実行されると、エラーバッファはすぐにクリアされます。その場合、 `SHOW ERRORS`空のセットを返します。

どのステートメントがエラーを生成するか、または警告を生成するかの動作は、現在の`sql_mode`に大きく影響されます。

## 概要 {#synopsis}

```ebnf+diagram
ShowErrorsStmt ::=
    "SHOW" "ERRORS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
mysql> select invalid;
ERROR 1054 (42S22): Unknown column 'invalid' in 'field list'
mysql> create invalid;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 14 near "invalid"
mysql> SHOW ERRORS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                   |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Error | 1054 | Unknown column 'invalid' in 'field list'                                                                                                                  |
| Error | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 14 near "invalid"  |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)

mysql> CREATE invalid2;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 15 near "invalid2"
mysql> SELECT 1;
+------+
| 1    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> SHOW ERRORS;
Empty set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW ERRORS`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [警告を表示](/sql-statements/sql-statement-show-warnings.md)
