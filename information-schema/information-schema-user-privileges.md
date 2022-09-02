---
title: USER_PRIVILEGES
summary: Learn the `USER_PRIVILEGES` information_schema table.
---

# USER_PRIVILEGES {#user-privileges}

表`USER_PRIVILEGES`は、グローバル権限に関する情報を提供します。この情報は、 `mysql.user`システム テーブルから取得されます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC user_privileges;
```

```
+----------------+--------------+------+------+---------+-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------+--------------+------+------+---------+-------+
| GRANTEE        | varchar(81)  | YES  |      | NULL    |       |
| TABLE_CATALOG  | varchar(512) | YES  |      | NULL    |       |
| PRIVILEGE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| IS_GRANTABLE   | varchar(3)   | YES  |      | NULL    |       |
+----------------+--------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM user_privileges;
```

```
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | Select                  | YES          |
| 'root'@'%' | def           | Insert                  | YES          |
| 'root'@'%' | def           | Update                  | YES          |
| 'root'@'%' | def           | Delete                  | YES          |
| 'root'@'%' | def           | Create                  | YES          |
| 'root'@'%' | def           | Drop                    | YES          |
| 'root'@'%' | def           | Process                 | YES          |
| 'root'@'%' | def           | References              | YES          |
| 'root'@'%' | def           | Alter                   | YES          |
| 'root'@'%' | def           | Show Databases          | YES          |
| 'root'@'%' | def           | Super                   | YES          |
| 'root'@'%' | def           | Execute                 | YES          |
| 'root'@'%' | def           | Index                   | YES          |
| 'root'@'%' | def           | Create User             | YES          |
| 'root'@'%' | def           | Trigger                 | YES          |
| 'root'@'%' | def           | Create View             | YES          |
| 'root'@'%' | def           | Show View               | YES          |
| 'root'@'%' | def           | Create Role             | YES          |
| 'root'@'%' | def           | Drop Role               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
+------------+---------------+-------------------------+--------------+
28 rows in set (0.00 sec)
```

`USER_PRIVILEGES`テーブルのフィールドは次のとおりです。

-   `GRANTEE` : 付与されたユーザーの名前。形式は`'user_name'@'host_name'`です。
-   `TABLE_CATALOG` : テーブルが属するカタログの名前。この値は常に`def`です。
-   `PRIVILEGE_TYPE` : 付与される権限タイプ。各行には 1 つの特権タイプのみが表示されます。
-   `IS_GRANTABLE` : `GRANT OPTION`権限を持っている場合、値は`YES`です。それ以外の場合、値は`NO`です。
