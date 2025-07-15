---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
---

# AUTO_RANDOM <span class="version-mark">New in v3.1.0</span>

## User scenario

Since the value of `AUTO_RANDOM` is random and unique, `AUTO_RANDOM` is often used in place of [`AUTO_INCREMENT`](/auto-increment.md) to avoid write hotspot in a single storage node caused by TiDB assigning consecutive IDs. If the current `AUTO_INCREMENT` column is a primary key and the type is `BIGINT`, you can execute the `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` statement to switch from `AUTO_INCREMENT` to `AUTO_RANDOM`.

<CustomContent platform="tidb">

For more information about how to handle highly concurrent write-heavy workloads in TiDB, see [Best Practices for High-Concurrency Writes](/best-practices/high-concurrency-best-practices.md).

</CustomContent>

The `AUTO_RANDOM_BASE` parameter in the [CREATE TABLE](/sql-statements/sql-statement-create-table.md) statement is used to set the initial incremental part value of `auto_random`. This option can be considered as a part of the internal interface. You can ignore this parameter.

## Basic concepts

`AUTO_RANDOM` is a column attribute that is used to automatically assign values to a `BIGINT` column. Values assigned automatically are **random** and **unique**.

To create a table with an `AUTO_RANDOM` column, you can use the following statements. The `AUTO_RANDOM` column must be included in a primary key, and the `AUTO_RANDOM` column is the first column in the primary key.

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

You can wrap the keyword `AUTO_RANDOM` in an executable comment. For more details, refer to [TiDB specific comment syntax](/comment-syntax.md#tidb-specific-comment-syntax).

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

When you execute an `INSERT` statement:

- If you explicitly specify the value of the `AUTO_RANDOM` column, it is inserted into the table as is.
- If you do not explicitly specify the value of the `AUTO_RANDOM` column, TiDB generates a random value and inserts it into the table.

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

The `AUTO_RANDOM(S, R)` column value automatically assigned by TiDB has a total of 64 bits:

- `S` is the number of shard bits. The value ranges from `1` to `15`. The default value is `5`.
- `R` is the total length of the automatic allocation range. The value ranges from `32` to `64`. The default value is `64`.

The structure of an `AUTO_RANDOM` value with a signed bit is as follows:

| Signed bit | Reserved bits | Shard bits | Auto-increment bits |
|---------|-------------|--------|--------------|
| 1 bit | `64-R` bits | `S` bits | `R-1-S` bits |

The structure of an `AUTO_RANDOM` value without a signed bit is as follows:

| Reserved bits | Shard bits | Auto-increment bits |
|-------------|--------|--------------|
| `64-R` bits | `S` bits | `R-S` bits |

- Whether a value has a signed bit depends on whether the corresponding column has the `UNSIGNED` attribute.
- The length of the sign bit is determined by the existence of an `UNSIGNED` attribute. If there is an `UNSIGNED` attribute, the length is `0`. Otherwise, the length is `1`.
- The length of the reserved bits is `64-R`. The reserved bits are always `0`.
- The content of the shard bits is obtained by calculating the hash value of the starting time of the current transaction. To use a different length of shard bits (such as 10), you can specify `AUTO_RANDOM(10)` when creating the table.
- The value of the auto-increment bits is stored in the storage engine and allocated sequentially. Each time a new value is allocated, the value is incremented by 1. The auto-increment bits ensure that the values of `AUTO_RANDOM` are unique globally. When the auto-increment bits are exhausted, an error `Failed to read auto-increment value from storage engine` is reported when the value is allocated again.
- Value range: the maximum number of bits for the final generated value = shard bits + auto-increment bits. The range of a signed column is `[-(2^(R-1))+1, (2^(R-1))-1]`, and the range of an unsigned column is `[0, (2^R)-1]`.
- You can use `AUTO_RANDOM` with `PRE_SPLIT_REGIONS`. When a table is created successfully, `PRE_SPLIT_REGIONS` pre-splits data in the table into the number of Regions as specified by `2^(PRE_SPLIT_REGIONS)`.

> **Note:**
>
> Selection of shard bits (`S`):
>
> - Since there is a total of 64 available bits, the shard bits length affects the auto-increment bits length. That is, as the shard bits length increases, the length of auto-increment bits decreases, and vice versa. Therefore, you need to balance the randomness of allocated values and available space.
> - The best practice is to set the shard bits as `log(2, x)`, in which `x` is the current number of storage engines. For example, if there are 16 TiKV nodes in a TiDB cluster, you can set the shard bits as `log(2, 16)`, that is `4`. After all regions are evenly scheduled to each TiKV node, the load of bulk writes can be uniformly distributed to different TiKV nodes to maximize resource utilization.
>
> Selection of range (`R`):
>
> - Typically, the `R` parameter needs to be set when the numeric type of the application cannot represent a full 64-bit integer.
> - For example, the range of JSON number is `[-(2^53)+1, (2^53)-1]`. TiDB can easily assign an integer beyond this range to a column defined as `AUTO_RANDOM(5)`, causing unexpected behaviors when the application reads the column. In such cases, you can replace `AUTO_RANDOM(5)` with `AUTO_RANDOM(5, 54)` for signed columns, and replace `AUTO_RANDOM(5)` with `AUTO_RANDOM(5, 53)` for unsigned columns, ensuring that TiDB does not assign integers greater than `9007199254740991` (2^53-1) to the column.

Values allocated implicitly to the `AUTO_RANDOM` column affect `last_insert_id()`. To get the ID that TiDB last implicitly allocates, you can use the `SELECT last_insert_id ()` statement.

To view the shard bits number of the table with an `AUTO_RANDOM` column, you can execute the `SHOW CREATE TABLE` statement. You can also see the value of the `PK_AUTO_RANDOM_BITS=x` mode in the `TIDB_ROW_ID_SHARDING_INFO` column in the `information_schema.tables` system table. `x` is the number of shard bits.

After creating a table with an `AUTO_RANDOM` column, you can use `SHOW WARNINGS` to view the maximum implicit allocation times:

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
SHOW WARNINGS;
```

The output is as follows:

```sql
+-------+------+---------------------------------------------------------+
| Level | Code | Message                                                 |
+-------+------+---------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 288230376151711743 |
+-------+------+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## Implicit allocation rules of IDs

TiDB implicitly allocates values to `AUTO_RANDOM` columns similarly to `AUTO_INCREMENT` columns. They are also controlled by the session-level system variables [`auto_increment_increment`](/system-variables.md#auto_increment_increment) and [`auto_increment_offset`](/system-variables.md#auto_increment_offset). The auto-increment bits (ID) of implicitly allocated values conform to the equation `(ID - auto_increment_offset) % auto_increment_increment == 0`.

## Clear the auto-increment ID cache

When you insert data with explicit values into an `AUTO_RANDOM` column in a deployment with multiple TiDB server instances, potential ID collisions can occur, similar to an `AUTO_INCREMENT` column. If explicit inserts happen to use ID values that conflict with the internal counter TiDB uses for automatic generation, this can lead to errors. 

Here's how the collision can happen: each `AUTO_RANDOM` ID consists of random bits and an auto-incrementing part. TiDB uses an internal counter for this auto-incrementing part. If you explicitly insert an ID where the auto-incrementing part matches the counter's next value, a duplicate key error might occur when TiDB later attempts to generate the same ID automatically. For more details, see [AUTO_INCREMENT Uniqueness](/auto-increment.md#uniqueness).

With a single TiDB instance, this issue doesn't occur because the node automatically adjusts its internal counter when processing explicit insertions, preventing any future collisions. In contrast, with multiple TiDB nodes, each node maintains its own cache of IDs, which needs to be cleared to prevent collisions after explicit insertions. To clear these unallocated cached IDs and avoid potential collisions, you have two options: 

### Option 1: Automatically rebase (Recommended)

```sql
ALTER TABLE t AUTO_RANDOM_BASE=0;
```

This statement automatically determines an appropriate base value. Although it produces a warning message similar to `Can't reset AUTO_INCREMENT to 0 without FORCE option, using XXX instead`, the base value **will** change and you can safely ignore this warning.

> **Note:**
>
> You cannot set `AUTO_RANDOM_BASE` to `0` with the `FORCE` keyword. Attempting this results in an error.

### Option 2: Manually set a specific base value

If you need to set a specific base value (for example, `1000`), use the `FORCE` keyword:

```sql
ALTER TABLE t FORCE AUTO_RANDOM_BASE = 1000;
```

This approach is less convenient because it requires you to determine an appropriate base value yourself.

> **Note:**
>
> When using `FORCE`, you must specify a non-zero positive integer.

Both commands modify the starting point for the auto-increment bits used in subsequent `AUTO_RANDOM` value generations across all TiDB nodes. They do not affect already allocated IDs.

## Restrictions

Pay attention to the following restrictions when you use `AUTO_RANDOM`:

- To insert values explicitly, you need to set the value of the `@@allow_auto_random_explicit_insert` system variable to `1` (`0` by default). It is **not** recommended that you explicitly specify a value for the column with the `AUTO_RANDOM` attribute when you insert data. Otherwise, the numeral values that can be automatically allocated for this table might be used up in advance.
- Specify this attribute for the primary key column **ONLY** as the `BIGINT` type. Otherwise, an error occurs. In addition, when the attribute of the primary key is `NONCLUSTERED`, `AUTO_RANDOM` is not supported even on the integer primary key. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
- You cannot use `ALTER TABLE` to modify the `AUTO_RANDOM` attribute, including adding or removing this attribute.
- You cannot use `ALTER TABLE` to change from `AUTO_INCREMENT` to `AUTO_RANDOM` if the maximum value is close to the maximum value of the column type.
- You cannot change the column type of the primary key column that is specified with `AUTO_RANDOM` attribute.
- You cannot specify `AUTO_RANDOM` and `AUTO_INCREMENT` for the same column at the same time.
- You cannot specify `AUTO_RANDOM` and `DEFAULT` (the default value of a column) for the same column at the same time.
- When`AUTO_RANDOM` is used on a column, it is difficult to change the column attribute back to `AUTO_INCREMENT` because the auto-generated values might be very large.
