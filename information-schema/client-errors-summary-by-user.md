---
title: CLIENT_ERRORS_SUMMARY_BY_USER
summary: 了解 `CLIENT_ERRORS_SUMMARY_BY_USER` INFORMATION_SCHEMA 表。
---

# CLIENT_ERRORS_SUMMARY_BY_USER

表 `CLIENT_ERRORS_SUMMARY_BY_USER` 提供了连接到 TiDB 服务器的客户端返回的 SQL 错误和警告的摘要。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围或重复键值。
* 权限错误。
* 不存在的表。

客户端错误通过 MySQL 服务器协议返回给客户端，应用程序应采取适当的措施。`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_USER` 表提供了一种有用的方法，用于在应用程序未正确处理（或记录） TiDB 服务器返回的错误的场景中检查错误。

由于 `CLIENT_ERRORS_SUMMARY_BY_USER` 按用户汇总错误，因此在诊断某个用户服务器产生的错误多于其他服务器的场景时非常有用。可能的场景包括：

* 权限错误。
* 缺少表或关系对象。
* SQL 语法错误，或应用程序与 TiDB 版本之间的不兼容。

可以使用语句 `FLUSH CLIENT_ERRORS_SUMMARY` 重置汇总的计数。该摘要仅在每个 TiDB 服务器本地内存中保留。重启 TiDB 服务器后，摘要将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_USER;
```

输出如下：

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| USER          | varchar(64)   | NO   |      | NULL    |       |
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

字段说明：

* `USER`：已验证的用户。
* `ERROR_NUMBER`：返回的 MySQL 兼容错误编号。
* `ERROR_MESSAGE`：与错误编号匹配的错误信息（在预处理语句形式中）。
* `ERROR_COUNT`：该错误返回给用户的次数。
* `WARNING_COUNT`：该警告返回给用户的次数。
* `FIRST_SEEN`：首次向用户发送此错误（或警告）的时间。
* `LAST_SEEN`：最近一次向用户发送此错误（或警告）的时间。

以下示例显示在客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后，摘要会被重置：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_USER;
```

输出如下：

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| USER | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| root |         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:05:36 | 2021-03-18 13:05:36 |
+------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```