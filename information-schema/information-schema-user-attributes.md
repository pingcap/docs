---
title: USER_ATTRIBUTES
summary: Learn the `USER_ATTRIBUTES` INFORMATION_SCHEMA table.
---

# USER_ATTRIBUTES {#user-attributes}

表`USER_PRIVILEGES`は、ユーザーのコメントとユーザー属性に関する情報を示します。この情報は`mysql.user`システム テーブルから取得されます。

```sql
USE information_schema;
DESC user_attributes;
```

```sql
+-----------+--------------+------+------+---------+-------+
| Field     | Type         | Null | Key  | Default | Extra |
+-----------+--------------+------+------+---------+-------+
| USER      | varchar(32)  | NO   |      | NULL    |       |
| HOST      | varchar(255) | NO   |      | NULL    |       |
| ATTRIBUTE | longtext     | YES  |      | NULL    |       |
+-----------+--------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

`USER_ATTRIBUTES`テーブルのフィールドは次のように説明されています。

-   `USER` : ユーザー名。
-   `HOST` : ユーザーが TiDB に接続できるホスト。このフィールドの値が`％`の場合、ユーザーは任意のホストから TiDB に接続できることを意味します。
-   `ATTRIBUTE` : [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントで設定されるユーザーのコメントと属性。

以下は例です。

```sql
CREATE USER testuser1 COMMENT 'This user is created only for test';
CREATE USER testuser2 ATTRIBUTE '{"email": "user@pingcap.com"}';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+---------------------------------------------------+
| USER      | HOST | ATTRIBUTE                                         |
+-----------+------+---------------------------------------------------+
| root      | %    | NULL                                              |
| testuser1 | %    | {"comment": "This user is created only for test"} |
| testuser2 | %    | {"email": "user@pingcap.com"}                     |
+-----------+------+---------------------------------------------------+
3 rows in set (0.00 sec)
```
