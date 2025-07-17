---
title: AUTO_RANDOM
summary: 学习 AUTO_RANDOM 属性。
---

# AUTO_RANDOM <span class="version-mark">新特性于 v3.1.0</span>

## 用户场景

由于 `AUTO_RANDOM` 的值是随机且唯一的，`AUTO_RANDOM` 常用于替代 [`AUTO_INCREMENT`](/auto-increment.md)，以避免 TiDB 为连续 ID 分配而导致的单个存储节点的写入热点。如果当前的 `AUTO_INCREMENT` 列是主键且类型为 `BIGINT`，可以执行 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` 语句，将其从 `AUTO_INCREMENT` 转换为 `AUTO_RANDOM`。

<CustomContent platform="tidb">

关于在 TiDB 中处理高并发写入密集型工作负载的更多信息，参见 [高并发写入的最佳实践](/best-practices/high-concurrency-best-practices.md)。

</CustomContent>

在 [CREATE TABLE](/sql-statements/sql-statement-create-table.md) 语句中，`AUTO_RANDOM_BASE` 参数用于设置 `auto_random` 的初始递增部分值。此选项可以视为内部接口的一部分，你可以忽略此参数。

## 基本概念

`AUTO_RANDOM` 是一种列属性，用于自动为 `BIGINT` 列分配值。自动分配的值是 **随机** 且 **唯一** 的。

要创建带有 `AUTO_RANDOM` 列的表，可以使用以下语句。`AUTO_RANDOM` 列必须包含在主键中，并且 `AUTO_RANDOM` 列必须是主键的第一列。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

你可以将关键字 `AUTO_RANDOM` 包裹在可执行注释中。更多细节请参考 [TiDB 特定注释语法](/comment-syntax.md#tidb-specific-comment-syntax)。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

在执行 `INSERT` 语句时：

- 如果你明确指定了 `AUTO_RANDOM` 列的值，则会按原样插入表中。
- 如果没有明确指定 `AUTO_RANDOM` 列的值，TiDB 会生成一个随机值并插入表中。

```sql
tidb> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255)) /*T! PRE_SPLIT_REGIONS=2 */ ;
Query OK, 0 rows affected, 1 warning (0.01 sec)

tidb> INSERT INTO t(a, b) VALUES (1, 'string');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---+--------+
| a | b      |
+---+--------+
| 1 | string |
+---+--------+
1 row in set (0.01 sec)

tidb> INSERT INTO t(b) VALUES ('string2');
Query OK, 1 row affected (0.00 sec)

tidb> INSERT INTO t(b) VALUES ('string3');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---------------------+---------+
| a                   | b       |
+---------------------+---------+
|                   1 | string  |
| 1152921504606846978 | string2 |
| 4899916394579099651 | string3 |
+---------------------+---------+
3 rows in set (0.00 sec)

tidb> SHOW CREATE TABLE t;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                    |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint NOT NULL /*T![auto_rand] AUTO_RANDOM(5) */,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T! PRE_SPLIT_REGIONS=2 */ |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

tidb> SHOW TABLE t REGIONS;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS               | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|     62798 | t_158_                      | t_158_r_2305843009213693952 |     62810 |              28 | 62811, 62812, 62810 |          0 |           151 |          0 |                    1 |                0 |                        |                  |
|     62802 | t_158_r_2305843009213693952 | t_158_r_4611686018427387904 |     62803 |               1 | 62803, 62804, 62805 |          0 |            39 |          0 |                    1 |                0 |                        |                  |
|     62806 | t_158_r_4611686018427387904 | t_158_r_6917529027641081856 |     62813 |               4 | 62813, 62814, 62815 |          0 |           160 |          0 |                    1 |                0 |                        |                  |
|      9289 | t_158_r_6917529027641081856 | 78000000                    |     48268 |               1 | 48268, 58951, 62791 |          0 |         10628 |      43639 |                    2 |             7999 |                        |                  |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
4 rows in set (0.00 sec)
```

由 TiDB 自动分配的 `AUTO_RANDOM(S, R)` 列值总共占用 64 位：

- `S` 是分片位数，范围为 `1` 到 `15`，默认值为 `5`。
- `R` 是自动分配范围的总长度，范围为 `32` 到 `64`，默认值为 `64`。

带符号位的 `AUTO_RANDOM` 值结构如下：

| Signed bit | Reserved bits | Shard bits | Auto-increment bits |
|---------|-------------|--------|--------------|
| 1 bit | `64-R` bits | `S` bits | `R-1-S` bits |

无符号位的 `AUTO_RANDOM` 值结构如下：

| Reserved bits | Shard bits | Auto-increment bits |
|-------------|--------|--------------|
| `64-R` bits | `S` bits | `R-S` bits |

- 是否有符号位，取决于对应列是否具有 `UNSIGNED` 属性。
- 符号位的长度由是否存在 `UNSIGNED` 属性决定。如果存在，长度为 `0`；否则为 `1`。
- 保留位的长度为 `64-R`，且始终为 `0`。
- 分片位的内容通过计算当前事务起始时间的哈希值获得。若需使用不同长度的分片位（如 10 位），可以在创建表时指定 `AUTO_RANDOM(10)`。
- 自动递增位的值存储在存储引擎中，并按顺序分配。每次分配新值时，值会加 1。自动递增位确保 `AUTO_RANDOM` 的值在全局范围内唯一。当自动递增位耗尽时，再次分配值会报错 `Failed to read auto-increment value from storage engine`。
- 值范围：最终生成值的最大位数 = 分片位数 + 自动递增位数。带符号列的范围为 `[-(2^(R-1))+1, (2^(R-1))-1]`，无符号列的范围为 `[0, (2^R)-1]`。
- 你可以在创建表时使用 `AUTO_RANDOM` 搭配 `PRE_SPLIT_REGIONS`。当表创建成功后，`PRE_SPLIT_REGIONS` 会将表中的数据预先分割成 `2^(PRE_SPLIT_REGIONS)` 个 Region。

> **注意：**
>
> 分片位（`S`）的选择：
>
> - 由于总共有 64 位可用，分片位长度影响自动递增位的长度。即，分片位越长，自动递增位越短，反之亦然。因此，你需要在随机性和空间利用之间权衡。
> - 最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 为当前存储引擎的数量。例如，如果 TiDB 集群中有 16 个 TiKV 节点，可以将分片位设置为 `log(2, 16)`，即 `4`。所有 Region 均匀调度到每个 TiKV 节点后，批量写入的负载可以均匀分布，最大化资源利用率。
>
> 选择范围（`R`）：
>
> - 通常，当应用的数值类型不能表示完整的 64 位整数时，需要设置 `R` 参数。
> - 例如，JSON 数字的范围为 `[-(2^53)+1, (2^53)-1]`。TiDB 可以轻松为定义为 `AUTO_RANDOM(5)` 的列分配超出此范围的整数，导致应用在读取列时出现意外行为。在这种情况下，可以将 `AUTO_RANDOM(5)` 替换为 `AUTO_RANDOM(5, 54)`（有符号列），将 `AUTO_RANDOM(5)` 替换为 `AUTO_RANDOM(5, 53)`（无符号列），确保 TiDB 不会为列分配大于 `9007199254740991`（2^53-1）的整数。

隐式分配给 `AUTO_RANDOM` 列的值会影响 `last_insert_id()`。你可以使用 `SELECT last_insert_id()` 来获取 TiDB 最后隐式分配的 ID。

要查看带有 `AUTO_RANDOM` 列的表的分片位数，可以执行 `SHOW CREATE TABLE`。你也可以在 `information_schema.tables` 系统表中的 `TIDB_ROW_ID_SHARDING_INFO` 列看到 `PK_AUTO_RANDOM_BITS=x` 模式的值，其中 `x` 为分片位数。

在创建带有 `AUTO_RANDOM` 列的表后，可以使用 `SHOW WARNINGS` 查看最大隐式分配次数：

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
SHOW WARNINGS;
```

输出示例：

```sql
+-------+------+---------------------------------------------------------+
| Level | Code | Message                                                 |
+-------+------+---------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 288230376151711743 |
+-------+------+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## ID 的隐式分配规则

TiDB 对 `AUTO_RANDOM` 列的隐式分配值，类似于 `AUTO_INCREMENT` 列。它们也受会话级系统变量 [`auto_increment_increment`](/system-variables.md#auto_increment_increment) 和 [`auto_increment_offset`](/system-variables.md#auto_increment_offset) 控制。隐式分配值的自动递增位（ID）满足方程 `(ID - auto_increment_offset) % auto_increment_increment == 0`。

## 清除 auto-increment ID 缓存

当你在多 TiDB 服务器实例的部署中，向 `AUTO_RANDOM` 列插入显式值时，可能会发生 ID 冲突，类似于 `AUTO_INCREMENT` 列。如果显式插入的 ID 值与 TiDB 用于自动生成的内部计数器冲突，可能会导致错误。

冲突发生的原因如下：每个 `AUTO_RANDOM` ID 由随机位和自动递增部分组成。TiDB 使用内部计数器管理自动递增部分。如果你显式插入的 ID 的自动递增部分与计数器的下一个值相同，TiDB 在后续自动生成时可能会遇到重复键错误。更多细节请参见 [AUTO_INCREMENT 唯一性](/auto-increment.md#uniqueness)。

在单个 TiDB 实例中，不会出现此问题，因为节点在处理显式插入时会自动调整其内部计数器，避免未来冲突。而在多个 TiDB 节点中，每个节点维护自己的 ID 缓存，显式插入后需要清除这些缓存以防止冲突。为清除未分配的缓存 ID，避免潜在冲突，你有两个选项：

### 选项 1：自动重置（推荐）

```sql
ALTER TABLE t AUTO_RANDOM_BASE=0;
```

此语句会自动确定一个合适的基值。虽然会产生类似 `Can't reset AUTO_INCREMENT to 0 without FORCE option, using XXX instead` 的警告信息，但基值 **会** 改变，你可以安全忽略此警告。

> **注意：**
>
> 不能用 `FORCE` 关键字将 `AUTO_RANDOM_BASE` 设置为 `0`，否则会报错。

### 选项 2：手动设置特定的基值

如果你需要设置特定的基值（例如 `1000`），可以使用 `FORCE` 关键字：

```sql
ALTER TABLE t FORCE AUTO_RANDOM_BASE = 1000;
```

这种方式不太方便，因为你需要自己确定合适的基值。

> **注意：**
>
> 使用 `FORCE` 时，必须指定非零的正整数。

这两个命令会修改后续所有 TiDB 节点中 `AUTO_RANDOM` 值生成的起点，但不会影响已分配的 ID。

## 限制条件

使用 `AUTO_RANDOM` 时，请注意以下限制：

- 要插入显式值，你需要将系统变量 `@@allow_auto_random_explicit_insert` 设置为 `1`（默认为 `0`）。**不建议**在插入数据时显式指定带有 `AUTO_RANDOM` 属性的列的值，否则可能会提前用完此表可自动分配的数值。
- 仅能将此属性指定在主键列的 `BIGINT` 类型上，否则会报错。此外，当主键属性为 `NONCLUSTERED` 时，即使是整数主键，也不支持 `AUTO_RANDOM`。关于 `CLUSTERED` 类型主键的更多细节，请参考 [聚簇索引](/clustered-indexes.md)。
- 不能使用 `ALTER TABLE` 来修改 `AUTO_RANDOM` 属性，包括添加或删除此属性。
- 当最大值接近列类型最大值时，不能将 `AUTO_INCREMENT` 转为 `AUTO_RANDOM`。
- 不能更改带有 `AUTO_RANDOM` 属性的主键列的列类型。
- 不能同时为同一列指定 `AUTO_RANDOM` 和 `AUTO_INCREMENT`。
- 不能同时为同一列指定 `AUTO_RANDOM` 和 `DEFAULT`（列的默认值）。
- 当列使用 `AUTO_RANDOM` 时，若要将列属性改回 `AUTO_INCREMENT`，较为困难，因为自动生成的值可能非常大。