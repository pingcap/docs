---
title: SET [NAMES|CHARACTER SET] |  TiDB SQL Statement Reference
summary: An overview of the usage of SET [NAMES|CHARACTER SET] for the TiDB database.
---

# [名前|キャラクターセット]を設定 {#set-names-character-set}

ステートメント`SET NAMES` 、 `SET CHARACTER SET` 、および`SET CHARSET` 、現在の接続の変数`character_set_client` 、 `character_set_results` 、および`character_set_connection`を変更します。

## あらすじ {#synopsis}

**SetNamesStmt:**

![SetNamesStmt](/media/sqlgram/SetNamesStmt.png)

**変数割り当てリスト:**

![VariableAssignmentList](/media/sqlgram/VariableAssignmentList.png)

**変数割り当て:**

![VariableAssignment](/media/sqlgram/VariableAssignment.png)

**文字セット名:**

![CharsetName](/media/sqlgram/CharsetName.png)

**文字列名:**

![StringName](/media/sqlgram/StringName.png)

**文字セットKw:**

![CharsetKw](/media/sqlgram/CharsetKw.png)

**文字セット名またはデフォルト:**

![CharsetNameOrDefault](/media/sqlgram/CharsetNameOrDefault.png)

## 例 {#examples}

```sql
mysql> SHOW VARIABLES LIKE 'character_set%';
+--------------------------+--------------------------------------------------------+
| Variable_name            | Value                                                  |
+--------------------------+--------------------------------------------------------+
| character_sets_dir       | /usr/local/mysql-5.6.25-osx10.8-x86_64/share/charsets/ |
| character_set_connection | utf8mb4                                                |
| character_set_system     | utf8                                                   |
| character_set_results    | utf8mb4                                                |
| character_set_client     | utf8mb4                                                |
| character_set_database   | utf8mb4                                                |
| character_set_filesystem | binary                                                 |
| character_set_server     | utf8mb4                                                |
+--------------------------+--------------------------------------------------------+
8 rows in set (0.01 sec)

mysql> SET NAMES utf8;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW VARIABLES LIKE 'character_set%';
+--------------------------+--------------------------------------------------------+
| Variable_name            | Value                                                  |
+--------------------------+--------------------------------------------------------+
| character_sets_dir       | /usr/local/mysql-5.6.25-osx10.8-x86_64/share/charsets/ |
| character_set_connection | utf8                                                   |
| character_set_system     | utf8                                                   |
| character_set_results    | utf8                                                   |
| character_set_client     | utf8                                                   |
| character_set_server     | utf8mb4                                                |
| character_set_database   | utf8mb4                                                |
| character_set_filesystem | binary                                                 |
+--------------------------+--------------------------------------------------------+
8 rows in set (0.00 sec)

mysql> SET CHARACTER SET utf8mb4;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW VARIABLES LIKE 'character_set%';
+--------------------------+--------------------------------------------------------+
| Variable_name            | Value                                                  |
+--------------------------+--------------------------------------------------------+
| character_set_connection | utf8mb4                                                |
| character_set_system     | utf8                                                   |
| character_set_results    | utf8mb4                                                |
| character_set_client     | utf8mb4                                                |
| character_sets_dir       | /usr/local/mysql-5.6.25-osx10.8-x86_64/share/charsets/ |
| character_set_database   | utf8mb4                                                |
| character_set_filesystem | binary                                                 |
| character_set_server     | utf8mb4                                                |
+--------------------------+--------------------------------------------------------+
8 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
-   [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)
-   [文字セットと照合のサポート](/character-set-and-collation.md)
