---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL Statement Reference
summary: TiDB データベースの SET [GLOBAL|SESSION] <variable> の使用法の概要。
---

# <code>SET [GLOBAL|SESSION] &#x3C;variable></code> {#code-set-global-session-x3c-variable-code}

文`SET [GLOBAL|SESSION]` TiDBの組み込み変数の1つを変更します。これらの変数は、 `SESSION`または`GLOBAL`スコープ、あるいは[ユーザー変数](/user-defined-variables.md)の[システム変数](/system-variables.md)かになります。

> **警告：**
>
> ユーザー定義変数はまだ実験的機能です。本番環境での使用は推奨さ**れません**。

> **注記：**
>
> MySQLと同様に、 `GLOBAL`変数への変更は既存の接続にもローカル接続にも適用されません。値の変更は新しいセッションにのみ反映されます。

## 概要 {#synopsis}

```ebnf+diagram
SetVariableStmt ::=
    "SET" Variable "=" Expression ("," Variable "=" Expression )*

Variable ::=
    ("GLOBAL" | "SESSION") SystemVariable
|   UserVariable 
```

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

`sql_mode`の値をグローバルに更新します。更新後に`SQL_mode`の値を確認すると、 `SESSION`レベルの値は更新されていないことがわかります。

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

ユーザー変数は`@`で始まります。

```sql
SET @myvar := 5;
Query OK, 0 rows affected (0.00 sec)

SELECT @myvar, @myvar + 1;
+--------+------------+
| @myvar | @myvar + 1 |
+--------+------------+
|      5 |          6 |
+--------+------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

次の動作の違いが適用されます。

-   MySQLでは、 `SET GLOBAL`で行われた変更はレプリカには適用されません。しかし、TiDBでは、 `SET GLOBAL`の適用範囲は特定のシステム変数によって異なります。

    -   グローバル変数: ほとんどのシステム変数 (たとえば、クラスターの動作やオプティマイザーの動作に影響するもの) の場合、 `SET GLOBAL`で行われた変更はクラスター内のすべての TiDB インスタンスに適用されます。
    -   インスタンス レベルの変数: 一部のシステム変数 (たとえば、 `max_connections` ) の場合、 `SET GLOBAL`で行われた変更は、現在の接続で使用されている TiDB インスタンスにのみ適用されます。

    したがって、 `SET GLOBAL`使用して変数を変更する場合は、常にその変数の[ドキュメント](/system-variables.md) 、特に「クラスターに保持」属性をチェックして、変更の範囲を確認してください。

-   TiDBは、いくつかの変数を読み取りと設定の両方が可能としています。これは、アプリケーションとコネクタの両方がMySQL変数を読み取るのが一般的であるため、MySQLとの互換性を保つために必要です。例えば、JDBCコネクタは、その動作に依存していないにもかかわらず、クエリキャッシュ設定の読み取りと設定の両方を行います。

-   `SET GLOBAL`で行われた変更は、TiDBサーバーの再起動後も保持されます。つまり、TiDB の`SET GLOBAL` 、MySQL 8.0 以降で利用可能な`SET PERSIST`に近い動作をすることになります。

-   TiDB はグローバル変数を永続化するため、 `SET PERSIST`と`SET PERSIST_ONLY`サポートしません。

## 参照 {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
