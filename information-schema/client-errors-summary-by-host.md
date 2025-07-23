---
title: CLIENT_ERRORS_SUMMARY_BY_HOST
summary: 了解 `CLIENT_ERRORS_SUMMARY_BY_HOST` INFORMATION_SCHEMA 表。
---

# CLIENT_ERRORS_SUMMARY_BY_HOST

表 `CLIENT_ERRORS_SUMMARY_BY_HOST` 提供了连接到 TiDB 服务器的客户端返回的 SQL 错误和警告的摘要。这些包括：

* 格式错误的 SQL 语句。
* 除零错误。
* 尝试插入超出范围或重复键值。
* 权限错误。
* 不存在的表。

这些错误通过 MySQL 服务器协议返回给客户端，应用程序应采取相应的措施。`INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_BY_HOST` 表提供了一种有用的方法，用于在应用程序未正确处理（或记录） TiDB 服务器返回的错误的场景中检查错误。

由于 `CLIENT_ERRORS_SUMMARY_BY_HOST` 按远程主机进行错误汇总，因此在诊断某个应用服务器产生的错误比其他服务器多的场景时非常有用。可能的场景包括：

* 过时的 MySQL 客户端库。
* 过时的应用程序（可能在部署新版本时遗漏了该服务器）。
* 用户权限中“host”部分的使用不正确。
* 不稳定的网络连接导致更多的超时或断开连接。

可以使用语句 `FLUSH CLIENT_ERRORS_SUMMARY` 重置汇总计数。该汇总在每个 TiDB 服务器本地，且仅在内存中保留。重启 TiDB 服务器后，汇总信息将会丢失。

```sql
USE INFORMATION_SCHEMA;
DESC CLIENT_ERRORS_SUMMARY_BY_HOST;
```

输出如下：

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| HOST          | varchar(255)  | NO   |      | NULL    |       |
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

* `HOST`：客户端的远程主机。
* `ERROR_NUMBER`：返回的 MySQL 兼容错误编号。
* `ERROR_MESSAGE`：与错误编号对应的错误信息（在预处理语句形式中）。
* `ERROR_COUNT`：该错误返回给客户端主机的次数。
* `WARNING_COUNT`：该警告返回给客户端主机的次数。
* `FIRST_SEEN`：首次从客户端主机看到此错误（或警告）的时间。
* `LAST_SEEN`：最近一次从客户端主机看到此错误（或警告）的时间。

以下示例显示在客户端连接到本地 TiDB 服务器时生成的警告。执行 `FLUSH CLIENT_ERRORS_SUMMARY` 后，汇总会被重置：

```sql
SELECT 0/0;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
FLUSH CLIENT_ERRORS_SUMMARY;
SELECT * FROM CLIENT_ERRORS_SUMMARY_BY_HOST;
```

输出如下：

```sql
+-----+
| 0/0 |
+-----+
| NULL |
+-----+
1 row in set, 1 warning (0.00 sec)

+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| HOST      | ERROR_NUMBER | ERROR_MESSAGE | ERROR_COUNT | WARNING_COUNT | FIRST_SEEN          | LAST_SEEN           |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
| 127.0.0.1 |         1365 | Division by 0 |           0 |             1 | 2021-03-18 12:51:54 | 2021-03-18 12:51:54 |
+-----------+--------------+---------------+-------------+---------------+---------------------+---------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Empty set (0.00 sec)
```