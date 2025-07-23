---
title: AUTO_INCREMENT
summary: 了解 TiDB 的 `AUTO_INCREMENT` 列属性。
---

# AUTO_INCREMENT

本文档介绍了 `AUTO_INCREMENT` 列属性，包括其概念、实现原理、自动递增相关特性以及限制。

<CustomContent platform="tidb">

> **Note:**
>
> `AUTO_INCREMENT` 属性可能会在生产环境中引起热点问题。详情请参见 [Troubleshoot HotSpot Issues](/troubleshoot-hot-spot-issues.md)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> `AUTO_INCREMENT` 属性可能会在生产环境中引起热点问题。详情请参见 [Troubleshoot HotSpot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

你也可以在 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句中使用 `AUTO_INCREMENT` 参数，指定自增字段的起始值。

## 概念

`AUTO_INCREMENT` 是一种列属性，用于自动填充默认列值。当 `INSERT` 语句未指定 `AUTO_INCREMENT` 列的值时，系统会自动为该列分配值。

出于性能考虑，`AUTO_INCREMENT` 数字会以批次（默认为 3 万）分配给每个 TiDB 服务器。这意味着虽然 `AUTO_INCREMENT` 数字保证唯一，但在每个 TiDB 服务器上的值是单调递增的。

> **Note:**
>
> 如果你希望 `AUTO_INCREMENT` 数字在所有 TiDB 服务器上都是单调递增的，并且你的 TiDB 版本是 v6.5.0 或更高版本，建议开启 [MySQL 兼容模式](#mysql-compatibility-mode)。

以下是 `AUTO_INCREMENT` 的基本示例：


```sql
CREATE TABLE t(id int PRIMARY KEY AUTO_INCREMENT, c int);
```


```sql
INSERT INTO t(c) VALUES (1);
INSERT INTO t(c) VALUES (2);
INSERT INTO t(c) VALUES (3), (4), (5);
```

```sql
mysql> SELECT * FROM t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
+----+---+
5 rows in set (0.01 sec)
```

此外，`AUTO_INCREMENT` 还支持显式指定列值的 `INSERT` 语句。在这种情况下，TiDB 会存储显式指定的值：


```sql
INSERT INTO t(id, c) VALUES (6, 6);
```

```sql
mysql> SELECT * FROM t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
| 6  | 6 |
+----+---+
6 rows in set (0.01 sec)
```

上述用法与 MySQL 中的 `AUTO_INCREMENT` 用法相同，但在隐式分配的具体值方面，TiDB 与 MySQL 存在显著差异。

## 实现原理

TiDB 以以下方式实现 `AUTO_INCREMENT` 的隐式分配：

每个自增列使用一个全局可见的键值对记录已分配的最大 ID。在分布式环境中，节点之间的通信存在一定开销。因此，为了避免写放大问题，每个 TiDB 节点在分配 ID 时会申请一批连续的 ID 作为缓存，等第一批 ID 分配完毕后，再申请下一批 ID。因此，TiDB 节点在每次分配 ID 时不会向存储节点申请。例如：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

假设集群中有两个 TiDB 实例，分别为 `A` 和 `B`。如果在 `A` 和 `B` 上分别执行如下 `INSERT` 语句：

```sql
INSERT INTO t (c) VALUES (1)
```

实例 `A` 可能会缓存 `[1,30000]` 的自增 ID，实例 `B` 可能会缓存 `[30001,60000]` 的自增 ID。在待执行的 `INSERT` 语句中，这两个实例缓存的 ID 会被依次分配给 `AUTO_INCREMENT` 列作为默认值。

## 基本特性

### 唯一性

> **Warning:**
>
> 当集群中存在多个 TiDB 实例，且表结构中包含自增 ID 时，建议不要同时使用显式插入和隐式分配，即不要在使用自增列的默认值和自定义值之间切换。否则可能会破坏隐式分配值的唯一性。

在上述示例中，按顺序执行以下操作：

1. 客户端向实例 `B` 插入语句 `INSERT INTO t VALUES (2, 1)`，将 `id` 设置为 `2`，插入成功。

2. 客户端向实例 `A` 发送语句 `INSERT INTO t (c) VALUES (1)`。该语句未指定 `id` 的值，因此由 `A` 分配 ID。此时，由于 `A` 缓存的 ID 范围为 `[1, 30000]`，可能会将 `2` 作为自增 ID 的值，并将本地计数器加 `1`。此时，数据库中已存在 ID 为 `2` 的数据，导致返回 `Duplicated Error` 错误。

### 单调性

TiDB 保证 `AUTO_INCREMENT` 值在每个服务器上是单调递增的（始终递增）。考虑以下示例，连续生成的 `AUTO_INCREMENT` 值为 1-3：


```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

+---+---------------------+
| a | b                   |
+---+---------------------+
| 1 | 2020-09-09 20:38:22 |
| 2 | 2020-09-09 20:38:22 |
| 3 | 2020-09-09 20:38:22 |
+---+---------------------+
3 rows in set (0.00 sec)
```

单调递增不等同于连续。考虑以下示例：


```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a VARCHAR(10), cnt INT NOT NULL DEFAULT 1, UNIQUE KEY (a));
INSERT INTO t (a) VALUES ('A'), ('B');
SELECT * FROM t;
INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   1 |
|  2 | B    |   1 |
+----+------+-----+
2 rows in set (0.00 sec)

Query OK, 3 rows affected (0.00 sec)
Records: 2  Duplicates: 1  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   2 |
|  2 | B    |   1 |
|  4 | C    |   1 |
+----+------+-----+
3 rows in set (0.00 sec)
```

在此示例中，`INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;` 语句中，`A` 的 `AUTO_INCREMENT` 值为 `3`，但未被使用，因为该语句中存在重复键 `A`，导致出现序列中的空隙。这种行为在法律上是允许的，虽然与 MySQL 不同。MySQL 在事务中被中止和回滚等场景下也会出现序列中的空隙。

## AUTO_ID_CACHE

如果在不同的 TiDB 服务器上执行 `INSERT` 操作，`AUTO_INCREMENT` 序列可能会出现“跳跃”现象。这是因为每个服务器都拥有自己的 `AUTO_INCREMENT` 缓存：


```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
INSERT INTO t (a) VALUES (NULL);
SELECT * FROM t;
```

```sql
Query OK, 1 row affected (0.03 sec)

+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
+---------+---------------------+
4 rows in set (0.00 sec)
```

对初始 TiDB 服务器的新的 `INSERT` 操作会生成 `AUTO_INCREMENT` 值 `4`，因为该 TiDB 服务器的 `AUTO_INCREMENT` 缓存中仍有空间可用。在这种情况下，序列值不能被视为全局单调递增，因为值 `4` 在值 `2000001` 之后插入：


```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
+---------+---------------------+
5 rows in set (0.00 sec)
```

`AUTO_INCREMENT` 缓存不会在 TiDB 服务器重启后保留。以下是在重启后执行的 `INSERT` 语句：


```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
+---------+---------------------+
6 rows in set (0.00 sec)
```

TiDB 服务器频繁重启可能会导致 `AUTO_INCREMENT` 数值耗尽。在上述示例中，初始 TiDB 服务器的缓存中仍有 `[5-30000]` 的值未被使用。这些值会丢失，不会被重新分配。

不建议依赖 `AUTO_INCREMENT` 数值的连续性。考虑以下示例，某个 TiDB 服务器的缓存范围为 `[2000001-2030000]`，通过手动插入值 `2029998`，可以观察到新的缓存范围被重新申请的行为：


```sql
mysql> INSERT INTO t (a) VALUES (2029998);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
| 2029998 | 2020-09-09 21:08:11 |
| 2029999 | 2020-09-09 21:08:11 |
| 2030000 | 2020-09-09 21:08:11 |
| 2060001 | 2020-09-09 21:08:11 |
| 2060002 | 2020-09-09 21:08:11 |
+---------+---------------------+
11 rows in set (0.00 sec)
```

在插入值 `2030000` 后，下一个值变成了 `2060001`，这是因为另一个 TiDB 服务器获取了中间缓存范围 `[2030001-2060000]`。当部署多个 TiDB 服务器时，`AUTO_INCREMENT` 序列中会出现间隙，因为缓存请求是交错的。

### 缓存大小控制

在早期版本的 TiDB 中，自动递增 ID 的缓存大小对用户是透明的。从 v3.0.14、v3.1.2 和 v4.0.rc-2 开始，TiDB 引入了 `AUTO_ID_CACHE` 表选项，允许用户设置分配自增 ID 的缓存大小。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t values();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)

SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                             |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=101 /*T![auto_id_cache] AUTO_ID_CACHE=100 */ |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此时，如果重启 TiDB，自动递增 ID 缓存会丢失，新的插入操作会从高于之前缓存范围的值开始分配 ID：


```sql
INSERT INTO t VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
| 101 |
+-----+
2 rows in set (0.01 sec)
```

新分配的值为 `101`，表明分配自增 ID 的缓存大小为 `100`。

此外，当批量 `INSERT` 语句中连续 ID 数量超过 `AUTO_ID_CACHE` 时，TiDB 会相应增加缓存大小，以确保语句能正常插入数据。

### 清除自增 ID 缓存

在某些场景下，可能需要清除自增 ID 缓存以确保数据一致性。例如：

<CustomContent platform="tidb">

- 在使用 [Data Migration (DM)](/dm/dm-overview.md) 进行增量复制的场景中，一旦复制完成，写入下游 TiDB 的数据会从 DM 切换到你的应用写操作。同时，自增列的 ID 写入模式通常也会从显式插入切换为隐式分配。
- 在 TiDB Lightning 完成数据导入后，会自动清除自增 ID 缓存。但 TiCDC 不会在增量数据同步后自动清除缓存。因此，在停止 TiCDC 后、进行故障转移前，你需要手动清除下游集群中的自增 ID 缓存。

</CustomContent>
<CustomContent platform="tidb-cloud">

- 在使用 [Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md) 功能进行增量复制的场景中，一旦复制完成，写入下游 TiDB 的数据会从 DM 切换到你的应用写操作。同时，自增列的 ID 写入模式通常也会从显式插入切换为隐式分配。
- 在 TiDB Lightning 完成数据导入后，会自动清除自增 ID 缓存。但 TiCDC 不会在增量数据同步后自动清除缓存。因此，在停止 TiCDC 后、进行故障转移前，你需要手动清除下游集群中的自增 ID 缓存。

</CustomContent>

- 当你的应用涉及显式 ID 插入和隐式 ID 分配时，你需要清除自增 ID 缓存，以避免未来隐式分配的 ID 与之前显式插入的 ID 冲突，从而导致主键冲突错误。更多信息请参见 [Uniqueness](/auto-increment.md#uniqueness)。

要在集群中所有 TiDB 节点上清除自增 ID 缓存，可以执行带有 `AUTO_INCREMENT = 0` 的 `ALTER TABLE` 语句，例如：


```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

INSERT INTO t VALUES(50);
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+----+
| a  |
+----+
|  1 |
| 50 |
+----+
2 rows in set (0.01 sec)
```

```sql
ALTER TABLE t AUTO_INCREMENT = 0;
Query OK, 0 rows affected, 1 warning (0.07 sec)

SHOW WARNINGS;
+---------+------+-------------------------------------------------------------------------+
| Level   | Code | Message                                                                 |
+---------+------+-------------------------------------------------------------------------+
| Warning | 1105 | Can't reset AUTO_INCREMENT to 0 without FORCE option, using 101 instead |
+---------+------+-------------------------------------------------------------------------+
1 row in set (0.01 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
|  50 |
| 101 |
+-----+
3 rows in set (0.01 sec)
```

### 自增步长和偏移

从 v3.0.9 和 v4.0.0-rc.1 开始，类似 MySQL 的行为，自动递增列隐式分配的值由会话变量 `@@auto_increment_increment` 和 `@@auto_increment_offset` 控制。

隐式分配的 ID 满足以下关系式：

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL 兼容模式

TiDB 提供了一个 MySQL 兼容模式，用于确保自增列的 ID 严格递增且间隙最小。启用此模式的方法是在创建表时设置 `AUTO_ID_CACHE` 为 `1`：


```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

当 `AUTO_ID_CACHE` 设置为 `1` 时，所有 TiDB 实例上的 ID 都是严格递增的，每个 ID 保证唯一，且与默认缓存模式（`AUTO_ID_CACHE 0`，缓存 3 万值）相比，ID 之间的间隙最小。

例如，设置 `AUTO_ID_CACHE 1` 后，可能会出现如下序列：


```sql
INSERT INTO t VALUES (); -- 返回 ID 1
INSERT INTO t VALUES (); -- 返回 ID 2
INSERT INTO t VALUES (); -- 返回 ID 3
-- 故障转移后
INSERT INTO t VALUES (); -- 可能返回 ID 5
```

而在默认缓存（`AUTO_ID_CACHE 0`）下，可能会出现较大的间隙：


```sql
INSERT INTO t VALUES (); -- 返回 ID 1
INSERT INTO t VALUES (); -- 返回 ID 2
-- 新的 TiDB 实例申请下一批
INSERT INTO t VALUES (); -- 返回 ID 30001
```

虽然 ID 始终递增且没有像 `AUTO_ID_CACHE 0` 那样的明显间隙，但在以下场景中仍可能出现小的间隙。这些间隙是为了保证 ID 的唯一性和严格递增特性而存在的。

- 在故障转移时，主实例退出或崩溃

  开启 MySQL 兼容模式后，分配的 ID 具有**唯一性**和**单调递增**，行为几乎与 MySQL 相同。即使跨多个 TiDB 实例访问，也能保持 ID 的单调递增。但如果中心化服务的主实例崩溃，可能会出现少量不连续的 ID。这是因为在故障转移过程中，备用实例会丢弃部分由主实例分配的 ID，以确保 ID 的唯一性。

- 在 TiDB 节点的滚动升级过程中
- 在正常的并发事务中（类似 MySQL）

> **Note:**
>
> `AUTO_ID_CACHE 1` 的行为和性能在 TiDB 版本中不断演进：
>
> - 在 v6.4.0 之前，每次 ID 分配都需要一次 TiKV 事务，影响性能。
> - 在 v6.4.0，TiDB 引入了集中式分配服务，将 ID 分配作为内存操作，大幅提升性能。
> - 从 v8.1.0 开始，TiDB 移除了在主节点退出时的自动 `forceRebase` 操作，以实现更快的重启。虽然这可能导致故障转移时出现额外的不连续 ID，但可以避免在许多表使用 `AUTO_ID_CACHE 1` 时的写入阻塞。

## 限制

目前，`AUTO_INCREMENT` 在 TiDB 中的使用存在以下限制：

- 在 TiDB v6.6.0 及之前版本，定义的列必须是主键或索引前缀。
- 必须定义在 `INTEGER`、`FLOAT` 或 `DOUBLE` 类型的列上。
- 不能与 `DEFAULT` 列值同时指定在同一列上。
- 不允许使用 `ALTER TABLE` 添加或修改带有 `AUTO_INCREMENT` 属性的列，包括使用 `ALTER TABLE ... MODIFY/CHANGE COLUMN` 为已有列添加 `AUTO_INCREMENT`，或使用 `ALTER TABLE ... ADD COLUMN` 添加带有 `AUTO_INCREMENT` 的列。
- 可以使用 `ALTER TABLE` 移除 `AUTO_INCREMENT` 属性，但从 v2.1.18 和 v3.0.4 起，TiDB 使用会话变量 `@@tidb_allow_remove_auto_inc` 控制是否允许通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 移除 `AUTO_INCREMENT`。默认情况下，不允许使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 移除 `AUTO_INCREMENT`。
- `ALTER TABLE` 需要使用 `FORCE` 选项才能将 `AUTO_INCREMENT` 设置为更小的值。
- 将 `AUTO_INCREMENT` 设置为小于 `MAX(<auto_increment_column>)` 的值会导致主键冲突，因为预先存在的值不会被跳过。