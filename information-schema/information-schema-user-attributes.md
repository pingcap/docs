---
title: USER_ATTRIBUTES
summary: USER_ATTRIBUTES` INFORMATION_SCHEMA テーブルについて学習します。
---

# ユーザー属性 {#user-attributes}

`USER_PRIVILEGES`テーブルは、ユーザーのコメントとユーザー属性に関する情報を提供します。この情報は`mysql.user`システムテーブルから取得されます。

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

`USER_ATTRIBUTES`テーブル内のフィールドは次のように説明されます。

-   `USER` : ユーザー名。
-   `HOST` : ユーザーがTiDBに接続できるホスト。このフィールドの値が`％`の場合、ユーザーはどのホストからでもTiDBに接続できます。
-   `ATTRIBUTE` : [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントで設定されるユーザーのコメントと属性。

次に例を示します。

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
