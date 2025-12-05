---
title: 全局索引
summary: 了解 TiDB 全局索引的使用场景、优势、用法、工作原理和限制。
---

# 全局索引

在引入全局索引之前，TiDB 为每个分区创建一个本地索引，即每个分区一个本地索引。这种索引方式存在[一个限制](/partitioned-table.md#partitioning-keys-primary-keys-and-unique-keys)：主键和唯一键必须包含所有分区键，以保证数据的全局唯一性。此外，当查询需要跨多个分区访问数据时，TiDB 必须扫描每个分区的数据才能返回结果。

为了解决这些问题，TiDB 在 [v8.3.0](https://docs.pingcap.com/tidb/stable/release-8.3.0) 中引入了全局索引功能。单个全局索引覆盖整个表的数据，即使主键和唯一键不包含分区键，也能保证全局唯一性。此外，借助全局索引，TiDB 可以一次性访问跨多个分区的索引数据，无需逐个查找每个分区的本地索引。这大大提升了非分区键的查询性能。从 v8.5.4 开始，非唯一索引也可以创建为全局索引。

## 优势

全局索引可以显著提升查询性能，增强索引设计的灵活性，并降低数据迁移和应用修改的成本。

### 查询性能提升

全局索引能够有效提升非分区列的查询效率。当查询涉及非分区列时，全局索引可以快速定位相关数据，避免对所有分区进行全表扫描。这显著减少了 Coprocessor（cop）任务的数量，尤其在分区数量较多的场景下效果更为明显。

基准测试显示，当表包含 100 个分区时，在 sysbench 的 `select_random_points` 场景下，性能提升最高可达 53 倍。

### 索引设计更灵活

全局索引消除了分区表唯一键必须包含所有分区列的限制，极大提升了索引设计的灵活性。你可以根据实际的查询模式和业务逻辑创建索引，而不再受限于分区方案。这种灵活性不仅提升了查询性能，也支持了更广泛的应用需求。

### 降低数据迁移和应用修改成本

在数据迁移和应用修改过程中，全局索引可以显著减少额外调整工作量。如果没有全局索引，你可能需要更改分区方案或重写 SQL 查询以规避索引限制。有了全局索引，这些修改可以避免，从而降低开发和运维成本。

例如，在将表从 Oracle 数据库迁移到 TiDB 时，可能会遇到不包含分区列的唯一索引，因为 Oracle 支持全局索引。在 TiDB 引入全局索引之前，必须修改表结构以符合 TiDB 的分区规则。现在，TiDB 支持全局索引，迁移时只需将这些索引定义为全局索引，即可保持与 Oracle 一致的表结构行为，大大降低迁移成本。

## 全局索引的限制

- 如果在索引定义中未显式指定 `GLOBAL` 关键字，TiDB 默认创建本地索引。
- `GLOBAL` 和 `LOCAL` 关键字仅适用于分区表，对非分区表无效。换句话说，在非分区表中，全局索引和本地索引没有区别。
- `DROP PARTITION`、`TRUNCATE PARTITION` 和 `REORGANIZE PARTITION` 等 DDL 操作也会触发全局索引的更新。这些 DDL 操作需要等待全局索引更新完成后才能返回结果，因此执行时间相应增加。尤其在数据归档场景（如 `DROP PARTITION` 和 `TRUNCATE PARTITION`）下表现明显。没有全局索引时，这些操作通常可以立即完成；但有全局索引时，随着需要更新的索引数量增加，执行时间也会增加。
- 包含全局索引的表不支持 `EXCHANGE PARTITION` 操作。
- 默认情况下，分区表的主键为聚簇索引，且必须包含分区键。如果你需要主键不包含分区键，可以在建表时显式将主键指定为非聚簇全局索引，例如：`PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。
- 如果全局索引添加在表达式列上，或全局索引为前缀索引（如 `UNIQUE KEY idx_id_prefix (id(10)) GLOBAL`），则需要手动收集该全局索引的统计信息。

## 功能演进

- **v7.6.0 之前**：TiDB 仅支持分区表的本地索引。这意味着分区表上的唯一键必须包含分区表达式中的所有列。未使用分区键的查询需要扫描所有分区，导致查询性能下降。
- **[v7.6.0](https://docs.pingcap.com/tidb/stable/release-7.6.0)**：引入 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) 系统变量以开启全局索引。但当时该功能仍在开发中，不建议生产环境使用。
- **[v8.3.0](https://docs.pingcap.com/tidb/stable/release-8.3.0)**：全局索引作为实验特性发布。你可以在定义索引时通过 `GLOBAL` 关键字显式创建全局索引。
- **[v8.4.0](https://docs.pingcap.com/tidb/stable/release-8.4.0)**：全局索引功能正式 GA。你可以直接使用 `GLOBAL` 关键字创建全局索引，无需设置 `tidb_enable_global_index` 系统变量。从该版本起，该系统变量被废弃，值固定为 `ON`，即默认启用全局索引。
- **[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0)**：全局索引支持包含分区表达式中的所有列。

## 全局索引 vs. 本地索引

下图展示了全局索引与本地索引的区别：

![Global Index vs. Local Index](/media/global-index-vs-local-index.png)

**全局索引适用场景**：

- **数据归档不频繁**：如医疗行业，部分业务数据需保留 30 年，通常按月分区，一次性创建 360 个分区，后续很少进行 `DROP` 或 `TRUNCATE` 操作。在此场景下，全局索引更适合，因为它能提供跨分区一致性和更高的查询性能。
- **跨分区查询**：当查询需要跨多个分区访问数据时，全局索引可以避免对所有分区的全表扫描，提升查询效率。

**本地索引适用场景**：

- **数据归档频繁**：如果数据归档操作频繁，且大多数查询仅限于单个分区，本地索引能提供更好的性能。
- **分区交换场景**：如银行等行业，处理后的数据先写入普通表，验证后再交换到分区表，以减少对分区表的性能影响。在这种情况下，建议使用本地索引，因为一旦使用全局索引，分区表将不再支持分区交换。

## 全局索引 vs. 聚簇索引

由于聚簇索引和全局索引的底层原理约束，单个索引不能同时作为聚簇索引和全局索引。但每种索引在不同查询场景下都能带来不同的性能收益。当你需要同时利用两者优势时，可以将分区列包含在聚簇索引中，并单独创建一个不包含分区列的全局索引。

假设你有如下表结构：

```sql
CREATE TABLE `t` (
  `id` int DEFAULT NULL,
  `ts` timestamp NULL DEFAULT NULL,
  `data` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800)
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

在上述 `t` 表中，`id` 列为唯一值。为了同时优化点查和范围查询，可以在建表语句中定义聚簇索引 `PRIMARY KEY(id, ts)`，并定义一个不包含分区列的全局索引 `UNIQUE KEY id(id)`。这样，基于 `id` 的点查会使用全局索引 `id` 并选择 `PointGet` 执行计划；范围查询则会使用聚簇索引，因为聚簇索引相比全局索引避免了一次额外的回表操作，提升了查询效率。

修改后的表结构如下：

```sql
CREATE TABLE `t` (
  `id` int NOT NULL,
  `ts` timestamp NOT NULL,
  `data` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`, `ts`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `id` (`id`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (UNIX_TIMESTAMP(`ts`))
(PARTITION `p0` VALUES LESS THAN (1735660800),
 PARTITION `p1` VALUES LESS THAN (1738339200)
 ...)
```

这种方式既优化了基于 `id` 的点查，也提升了范围查询的性能，并确保表的分区列能在基于时间戳的查询中得到有效利用。

## 用法

要创建全局索引，在索引定义中添加 `GLOBAL` 关键字。

> **注意：**
>
> 全局索引会影响分区管理。执行 `DROP`、`TRUNCATE` 或 `REORGANIZE PARTITION` 操作时，会触发表级全局索引的更新。这意味着这些 DDL 操作只有在对应全局索引更新完成后才会返回，可能会增加执行时间。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3),
    KEY idx1(col1) GLOBAL
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

在上述示例中，唯一索引 `uidx12` 和非唯一索引 `idx1` 成为全局索引，而 `uidx3` 仍为普通唯一索引。

注意，聚簇索引不能为全局索引。例如：

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

```
ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function
```

聚簇索引不能同时作为全局索引。这是因为如果聚簇索引为全局索引，表将不再是分区表。聚簇索引的 key 是分区级别行数据的 key，而全局索引是在表级别定义的，两者存在冲突。如果你需要将主键作为全局索引，必须显式定义为非聚簇索引。例如：

```sql
PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL
```

你可以通过 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 的输出中的 `GLOBAL` 索引选项来识别全局索引：

```sql
SHOW CREATE TABLE t1\G
```

```
       Table: t1
Create Table: CREATE TABLE `t1` (
  `col1` int NOT NULL,
  `col2` date NOT NULL,
  `col3` int NOT NULL,
  `col4` int NOT NULL,
  UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
  UNIQUE KEY `uidx3` (`col3`),
  KEY `idx1` (`col1`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY HASH (`col3`) PARTITIONS 4
1 row in set (0.00 sec)
```

或者，你也可以查询 [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md) 表，并通过输出中的 `IS_GLOBAL` 列来识别全局索引。

```sql
SELECT * FROM information_schema.tidb_indexes WHERE table_name='t1';
```

```
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
| test         | t1         |          1 | idx1     |            1 | col1        |     NULL |               | NULL       |        3 | YES        | NO        |         1 |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
3 rows in set (0.00 sec)
```

在对普通表进行分区或对分区表重新分区时，你可以根据需要将索引更新为全局索引或本地索引。

例如，以下 SQL 语句将表 `t1` 按 `col1` 列重新分区，并将全局索引 `uidx12` 和 `idx1` 更新为本地索引，将本地索引 `uidx3` 更新为全局索引。`uidx3` 是 `col3` 上的唯一索引，为保证 `col3` 在所有分区间的唯一性，`uidx3` 必须为全局索引。`uidx12` 和 `idx1` 是 `col1` 上的索引，可以为全局索引或本地索引。

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL, idx1 LOCAL);
```

## 工作原理

本节介绍全局索引的工作原理，包括其设计原则和实现方式。

### 设计原则

在 TiDB 分区表中，本地索引的 key 前缀为 Partition ID，而全局索引的前缀为 Table ID。该设计保证了全局索引数据在 TiKV 上连续分布，从而减少索引查找时的 RPC 请求数量。

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  KEY idx(k),
  KEY global_idx(k) GLOBAL
) partition by hash(id) partitions 5;
```

以上述表结构为例：`idx` 为本地索引，`global_idx` 为全局索引。`idx` 的数据分布在 5 个不同的范围（如 `PartitionID1_i_xxx`、`PartitionID2_i_xxx`），而 `global_idx` 的数据集中在一个范围（`TableID_i_xxx`）。

当执行与 `k` 相关的查询（如 `SELECT * FROM sbtest WHERE k > 1`）时，本地索引 `idx` 会生成 5 个独立的范围，而全局索引 `global_idx` 只生成一个范围。由于 TiDB 中每个范围对应一次或多次 RPC 请求，使用全局索引可以将 RPC 请求数量减少数倍，从而提升索引查询性能。

下图展示了在执行 `SELECT * FROM sbtest WHERE k > 1` 语句时，分别使用 `idx` 和 `global_idx` 两种索引时的 RPC 请求和数据流动差异。

![Mechanism of Global Indexes](/media/global-index-mechanism.png)

### 编码方式

在 TiDB 中，索引条目以键值对形式编码。对于分区表，TiKV 层将每个分区视为独立的物理表，拥有各自的 `partitionID`。因此，分区表索引条目的编码方式如下：

```
唯一键
Key:
- PartitionID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle

非唯一键
Key:
- PartitionID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_Padding

- CommonHandle
 - TailLen_IndexVersion
```

对于全局索引，索引条目的编码方式有所不同。为保证全局索引的 key 布局与当前索引 key 编码兼容，新的索引编码布局定义如下：

```
唯一键
Key:
- TableID_indexID_ColumnValues

Value:
- IntHandle
 - TailLen_PartitionID_IntHandle

- CommonHandle
 - TailLen_IndexVersion_CommonHandle_PartitionID

非唯一键
Key:
- TableID_indexID_ColumnValues_Handle

Value:
- IntHandle
 - TailLen_PartitionID

- CommonHandle
 - TailLen_IndexVersion_PartitionID
```

该编码方案将 `TableID` 放在全局索引 key 的开头，而 `PartitionID` 存储在 value 中。这样设计的优点是实现了与现有索引 key 编码的兼容性，但也带来一些挑战。例如，在执行 `DROP PARTITION` 或 `TRUNCATE PARTITION` 等 DDL 操作时，由于索引条目并非连续存储，需要额外处理。

## 性能测试结果

以下测试基于 sysbench 的 `select_random_points` 场景，主要用于对比不同分区策略和索引方式下的查询性能。

测试所用表结构如下：

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `k_1` (`k`)
  /* Key `k_1` (`k`, `c`) GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
/* Partition by hash(`id`) partitions 100 */
/* Partition by range(`id`) xxxx */
```

压力 SQL 如下：

```sql
SELECT id, k, c, pad
FROM sbtest
WHERE k IN (xx, xx, xx)
```

范围分区（100 个分区）：

| 表类型                                                            | 并发 1 | 并发 32 | 并发 64 | 平均 RU |
| ----------------------------------------------------------------- | ------ | ------- | ------- | ------- |
| 聚簇非分区表                                                      | 225    | 19,999  | 30,293  | 7.92    |
| 按主键范围分区的聚簇表                                            | 68     | 480     | 511     | 114.87  |
| 按主键范围分区且 `k`、`c` 上有全局索引的聚簇表                    | 207    | 17,798  | 27,707  | 11.73   |

哈希分区（100 个分区）：

| 表类型                                                           | 并发 1 | 并发 32 | 并发 64 | 平均 RU |
| ---------------------------------------------------------------- | ------ | ------- | ------- | ------- |
| 聚簇非分区表                                                     | 166    | 20,361  | 28,922  | 7.86    |
| 按主键哈希分区的聚簇表                                           | 60     | 244     | 283     | 119.73  |
| 按主键哈希分区且 `k`、`c` 上有全局索引的聚簇表                   | 156    | 18,233  | 15,581  | 10.77   |

上述测试表明，在高并发环境下，全局索引可以显著提升分区表的查询性能，性能提升最高可达 50 倍。同时，全局索引大幅降低了 Request Unit（RU）消耗。随着分区数量的增加，性能收益更加明显。