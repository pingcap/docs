---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL Statement Reference
summary: An overview of the usage of SET [GLOBAL|SESSION] <variable> for the TiDB database.
---

# <code>SET [GLOBAL|SESSION] &#x3C;variable></code> {#code-set-global-session-x3c-variable-code}

ステートメント`SET [GLOBAL|SESSION]` 、スコープが`SESSION`または`GLOBAL`の TiDB の組み込み変数の 1 つを変更します。

> **ノート：**
>
> MySQL と同様に、 `GLOBAL`変数への変更は、既存の接続にもローカル接続にも適用されません。新しいセッションのみが値の変更を反映します。

## あらすじ {#synopsis}

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

**変数割り当て:**

![VariableAssignment](/media/sqlgram/VariableAssignment.png)

## 例 {#examples}

`sql_mode`の値を取得します。

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

`sql_mode`の値をグローバルに更新します。更新後に`SQL_mode`の値を確認すると、 `SESSION`レベルの値が更新されていないことがわかります。

```sql
mysql> SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

`SET SESSION`使用するとすぐに有効になります。

```sql
mysql> SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

次の動作の違いが適用されます。

-   `SET GLOBAL`で行われた変更は、クラスター内のすべての TiDB インスタンスに伝搬されます。これは、変更がレプリカに反映されない MySQL とは異なります。
-   TiDB は、いくつかの変数を読み取り可能かつ設定可能として提示します。これは、アプリケーションとコネクタの両方が MySQL 変数を読み取るのが一般的であるため、MySQL との互換性のために必要です。例: JDBC コネクタは、動作に依存していないにもかかわらず、クエリ キャッシュ設定の読み取りと設定の両方を行います。
-   `SET GLOBAL`で行った変更は、TiDBサーバーの再起動後も保持されます。これは、TiDB の`SET GLOBAL` 、MySQL 8.0 以降で使用可能な`SET PERSIST`に似た動作をすることを意味します。

## こちらもご覧ください {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
