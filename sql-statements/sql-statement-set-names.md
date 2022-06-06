---
title: SET [NAMES|CHARACTER SET] |  TiDB SQL Statement Reference
summary: An overview of the usage of SET [NAMES|CHARACTER SET] for the TiDB database.
---

# SET [NAMES | CHARACTER SET] {#set-names-character-set}

ステートメント`SET NAMES` 、および`SET CHARACTER SET`は、現在の接続の変数`character_set_client` 、および`SET CHARSET`を`character_set_connection`し`character_set_results` 。

## あらすじ {#synopsis}

**SetNamesStmt：**

![SetNamesStmt](/media/sqlgram/SetNamesStmt.png)

**VariableAssignmentList：**

![VariableAssignmentList](/media/sqlgram/VariableAssignmentList.png)

**VariableAssignment：**

![VariableAssignment](/media/sqlgram/VariableAssignment.png)

**CharsetName：**

![CharsetName](/media/sqlgram/CharsetName.png)

**StringName：**

![StringName](/media/sqlgram/StringName.png)

**CharsetKw：**

![CharsetKw](/media/sqlgram/CharsetKw.png)

**CharsetNameOrDefault：**

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
-   [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)
-   [文字セットと照合のサポート](/character-set-and-collation.md)
