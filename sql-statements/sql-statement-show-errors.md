---
title: SHOW ERRORS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW ERRORS for the TiDB database.
---

# エラーを表示 {#show-errors}

このステートメントは、以前に実行されたステートメントからのエラーを示します。エラー バッファは、ステートメントが正常に実行されるとすぐにクリアされます。この場合、 `SHOW ERRORS`空のセットを返します。

どのステートメントがエラーと警告を生成するかの動作は、現在の`sql_mode`に大きく影響されます。

## あらすじ {#synopsis}

**ShowErrorsStmt:**

![ShowErrorsStmt](/media/sqlgram/ShowErrorsStmt.png)

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

TiDB の`SHOW ERRORS`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [警告を表示](/sql-statements/sql-statement-show-warnings.md)
