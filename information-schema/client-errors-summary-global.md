---
title: CLIENT_ERRORS_SUMMARY_GLOBAL
summary: 了解关于 `CLIENT_ERRORS_SUMMARY_GLOBAL` INFORMATION_SCHEMA 表的信息。
---

# CLIENT_ERRORS_SUMMARY_GLOBAL

表 `CLIENT_ERRORS_SUMMARY_GLOBAL` 提供了连接到 TiDB 服务器的所有客户端返回的 SQL 错误和警告的全局摘要。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围的重复键值。
* 权限错误。
* 表不存在。

客户端错误通过 MySQL 服务器协议返回给客户端，应用程序应采取适当的措施。`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL` 表提供了一个高级概览，在应用程序未正确处理（或记录） TiDB 服务器返回的错误的场景中非常有用。

可以使用语句 `FLUSH CLIENT_ERRORS_SUMMARY` 重置汇总计数。该摘要仅在每个 TiDB 服务器本地生效，并且只保留在内存中。重启 TiDB 服务器后，摘要将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_GLOBAL;
```

输出如下：

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| ERROR_NUMBER  | bigint(64)    | NO   |      | NULL    |       |
| ERROR_MESSAGE | varchar(1024) | NO   |      | NULL    |       |
| ERROR_COUNT   | bigint(64)    | NO   |      | NULL    |       |
| WARNING_COUNT | bigint(64)    | NO   |      | NULL    |       |
| FIRST_SEEN    | timestamp     | YES  |      | NULL    |       |
| LAST_SEEN     | timestamp     | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段说明：

* `ERROR_NUMBER`：返回的 MySQL 兼容错误编号。
* `ERROR_MESSAGE`：与错误编号对应的错误信息（以预处理语句形式）。
* `ERROR_COUNT`：该错误被返回的次数。
* `WARNING_COUNT`：该警告被返回的次数。
* `FIRST_SEEN`：首次发送该错误（或警告）的时间。
* `LAST_SEEN`：最近一次发送该错误（或警告）的时间。

以下示例显示在连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后，摘要会被重置：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_GLOBAL;
```

输出如下：

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+--------------+---------------+-------------+---------------+---------------------+---------------------+
| ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
|         1365 | Division by 0 |           0 |             1 | 2021-03-18 13:10:51 | 2021-03-18 13:10:51 |
+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```