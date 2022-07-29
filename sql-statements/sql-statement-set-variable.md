---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL Statement Reference
summary: An overview of the usage of SET [GLOBAL|SESSION] <variable> for the TiDB database.
---

# <code>SET [GLOBAL|SESSION] &#x3C;variable></code> {#code-set-global-session-x3c-variable-code}

ステートメント`SET [GLOBAL|SESSION]`は、スコープが`SESSION`または`GLOBAL`のTiDBの組み込み変数の1つを変更します。

> **ノート：**
>
> MySQLと同様に、 `GLOBAL`変数への変更は、既存の接続にもローカル接続にも適用されません。新しいセッションのみが値の変更を反映します。

## あらすじ {#synopsis}

**SetStmt：**

![SetStmt](/media/sqlgram/SetStmt.png)

**VariableAssignment：**

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

`sql_mode`の値をグローバルに更新します。更新後に値`SQL_mode`を確認すると、 `SESSION`レベルの値が更新されていないことがわかります。

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

`SET SESSION`を使用すると、すぐに有効になります。

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

## MySQLの互換性 {#mysql-compatibility}

次の動作の違いが適用されます。

-   `SET GLOBAL`で行った変更は、クラスタのすべてのTiDBインスタンスに伝播されます。これは、変更がレプリカに伝播されないMySQLとは異なります。
-   TiDBは、いくつかの変数を読み取り可能と設定可能の両方として提示します。これは、アプリケーションとコネクタの両方がMySQL変数を読み取ることが一般的であるため、MySQLの互換性のために必要です。次に例を示します。JDBCコネクタは、動作に依存していなくても、クエリキャッシュ設定の読み取りと設定の両方を行います。
-   `SET GLOBAL`で行われた変更は、TiDBサーバーの再起動後も保持されます。これは、TiDBの`SET GLOBAL`は、MySQL8.0以降で利用可能な`SET PERSIST`と同様に動作することを意味します。

## も参照してください {#see-also}

-   [[グローバル|セッション]変数を表示する](/sql-statements/sql-statement-show-variables.md)
