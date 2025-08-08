---
title: USER_PRIVILEGES
summary: USER_PRIVILEGES` information_schema テーブルについて学習します。
---

# ユーザー権限 {#user-privileges}

`USER_PRIVILEGES`のテーブルは、グローバル権限に関する情報を提供します。この情報は`mysql.user`のシステムテーブルから取得されます。

```sql
USE INFORMATION_SCHEMA;
DESC USER_PRIVILEGES;
```

出力は次のようになります。

```sql
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

`USER_PRIVILEGES`表の情報をビュー。

```sql
SELECT * FROM USER_PRIVILEGES;
```

出力は次のようになります。

<CustomContent platform="tidb">

```sql
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | SELECT                  | YES          |
| 'root'@'%' | def           | INSERT                  | YES          |
| 'root'@'%' | def           | UPDATE                  | YES          |
| 'root'@'%' | def           | DELETE                  | YES          |
| 'root'@'%' | def           | CREATE                  | YES          |
| 'root'@'%' | def           | DROP                    | YES          |
| 'root'@'%' | def           | PROCESS                 | YES          |
| 'root'@'%' | def           | REFERENCES              | YES          |
| 'root'@'%' | def           | ALTER                   | YES          |
| 'root'@'%' | def           | SHOW DATABASES          | YES          |
| 'root'@'%' | def           | SUPER                   | YES          |
| 'root'@'%' | def           | EXECUTE                 | YES          |
| 'root'@'%' | def           | INDEX                   | YES          |
| 'root'@'%' | def           | CREATE USER             | YES          |
| 'root'@'%' | def           | CREATE TABLESPACE       | YES          |
| 'root'@'%' | def           | TRIGGER                 | YES          |
| 'root'@'%' | def           | CREATE VIEW             | YES          |
| 'root'@'%' | def           | SHOW VIEW               | YES          |
| 'root'@'%' | def           | CREATE ROLE             | YES          |
| 'root'@'%' | def           | DROP ROLE               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
31 rows in set (0.00 sec)
```

</CustomContent>

<CustomContent platform="tidb-cloud">

<!--Compared with TiDB Self-Managed, the root user in TiDB Cloud does not have the SHUTDOWN and CONFIG privileges.-->

```sql
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | SELECT                  | YES          |
| 'root'@'%' | def           | INSERT                  | YES          |
| 'root'@'%' | def           | UPDATE                  | YES          |
| 'root'@'%' | def           | DELETE                  | YES          |
| 'root'@'%' | def           | CREATE                  | YES          |
| 'root'@'%' | def           | DROP                    | YES          |
| 'root'@'%' | def           | PROCESS                 | YES          |
| 'root'@'%' | def           | REFERENCES              | YES          |
| 'root'@'%' | def           | ALTER                   | YES          |
| 'root'@'%' | def           | SHOW DATABASES          | YES          |
| 'root'@'%' | def           | SUPER                   | YES          |
| 'root'@'%' | def           | EXECUTE                 | YES          |
| 'root'@'%' | def           | INDEX                   | YES          |
| 'root'@'%' | def           | CREATE USER             | YES          |
| 'root'@'%' | def           | CREATE TABLESPACE       | YES          |
| 'root'@'%' | def           | TRIGGER                 | YES          |
| 'root'@'%' | def           | CREATE VIEW             | YES          |
| 'root'@'%' | def           | SHOW VIEW               | YES          |
| 'root'@'%' | def           | CREATE ROLE             | YES          |
| 'root'@'%' | def           | DROP ROLE               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
29 rows in set (0.00 sec)
```

</CustomContent>

`USER_PRIVILEGES`テーブル内のフィールドは次のように説明されます。

-   `GRANTEE` : 許可されたユーザーの名前。形式は`'user_name'@'host_name'`です。
-   `TABLE_CATALOG` : テーブルが属するカタログの名前。この値は常に`def` 。
-   `PRIVILEGE_TYPE` : 付与する権限の種類。各行には1つの権限の種類のみが表示されます。
-   `IS_GRANTABLE` : `GRANT OPTION`権限がある場合、値は`YES`なります。それ以外の場合、値は`NO`になります。

## 参照 {#see-also}

-   [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)
