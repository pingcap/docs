---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL Statement Reference
summary: TiDB データベースの SET [GLOBAL|SESSION] <variable> の使用法の概要。
---

# <code>SET [GLOBAL|SESSION] &#x3C;variable></code> {#code-set-global-session-x3c-variable-code}

ステートメント`SET [GLOBAL|SESSION]` TiDB の組み込み変数の 1 つを変更します。これらの変数は、 `SESSION`または`GLOBAL`スコープの[システム変数](/system-variables.md)または[ユーザー変数](/user-defined-variables.md)いずれかになります。

> **警告：**
>
> ユーザー定義変数はまだ実験的機能です。本番環境での使用はお勧めし**ません**。

> **注記：**
>
> MySQL と同様に、 `GLOBAL`変数への変更は既存の接続にもローカル接続にも適用されません。値の変更は新しいセッションにのみ反映されます。

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

## MySQL 互換性 {#mysql-compatibility}

次の動作の違いが適用されます。

-   `SET GLOBAL`で行われた変更は、クラスター内のすべての TiDB インスタンスに伝播されます。これは、変更がレプリカに伝播されない MySQL とは異なります。
-   TiDB は、いくつかの変数を読み取り可能かつ設定可能として提示します。これは、アプリケーションとコネクタの両方が MySQL 変数を読み取るのが一般的であるため、MySQL との互換性のために必要です。たとえば、JDBC コネクタは、動作に依存していないにもかかわらず、クエリ キャッシュ設定の読み取りと設定の両方を行います。
-   `SET GLOBAL`で行われた変更は、TiDBサーバーの再起動後も保持されます。つまり、TiDB の`SET GLOBAL`は、MySQL 8.0 以降で利用可能な`SET PERSIST`に似た動作をすることになります。
-   TiDB はグローバル変数を永続化するため、 `SET PERSIST`と`SET PERSIST_ONLY`サポートしません。

## 参照 {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
