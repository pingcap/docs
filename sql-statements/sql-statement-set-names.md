---
title: SET [NAMES|CHARACTER SET] |  TiDB SQL Statement Reference
summary: TiDB データベースの SET [NAMES|CHARACTER SET] の使用法の概要。
---

# SET [名前|文字セット] {#set-names-character-set}

ステートメント`SET NAMES` 、および`SET CHARSET` `SET CHARACTER SET`現在の接続の変数`character_set_client` 、および`character_set_connection` `character_set_results`します。

## 概要 {#synopsis}

```ebnf+diagram
SetNamesStmt ::=
    "SET" ("NAMES" ("DEFAULT" | CharsetName ("COLLATE" ("DEFAULT" | CollationName))?) | ("CHARSET" | ("CHAR" | "CHARACTER") "SET") ("DEFAULT" | CharsetName))
```

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

TiDBの`SET [NAMES|CHARACTER SET]`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [[グローバル|セッション]変数を表示](/sql-statements/sql-statement-show-variables.md)
-   [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)
-   [文字セットと照合順序のサポート](/character-set-and-collation.md)
