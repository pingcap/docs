---
title: TiDB Computing
summary: 了解 TiDB 数据库的计算层。
---

# TiDB 计算

基于 TiKV 提供的分布式存储，TiDB 构建了结合强大事务处理能力与数据分析能力的计算引擎。本文档首先介绍一种将 TiDB 数据库表中的数据映射为 TiKV 中 (Key, Value) 键值对的数据映射算法，然后介绍 TiDB 如何管理元数据，最后阐述 TiDB SQL 层的架构。

关于计算层所依赖的存储方案，本文档仅介绍 TiKV 的行存储结构。对于 OLAP 服务，TiDB 引入了基于列存储的解决方案 [TiFlash](/tiflash/tiflash-overview.md)，作为 TiKV 的扩展。

## 表数据到 Key-Value 的映射

本节描述了 TiDB 中将数据映射为 (Key, Value) 键值对的方案。这里需要映射的数据包括以下两类：

- 表中每一行的数据，以下简称为表数据。
- 表中所有索引的数据，以下简称为索引数据。

### 表数据到 Key-Value 的映射

在关系型数据库中，一张表可能有很多列。要将一行中每一列的数据映射为 (Key, Value) 键值对，需要考虑如何构造 Key。首先，在 OLTP 场景下，存在大量对单行或多行数据的增、删、改、查操作，需要数据库能够快速读取一行数据。因此，每个 Key 应该有一个唯一的 ID（显式或隐式），以便快速定位。其次，许多 OLAP 查询需要全表扫描。如果能将一张表中所有行的 Key 编码为一个范围，就可以通过范围查询高效地扫描整张表。

基于上述考虑，TiDB 中表数据到 Key-Value 的映射设计如下：

- 为了保证同一张表的数据能够聚集在一起便于查找，TiDB 为每张表分配一个表 ID，用 `TableID` 表示。表 ID 是在整个集群中唯一的整数。
- TiDB 为表中的每一行数据分配一个行 ID，用 `RowID` 表示。行 ID 也是表内唯一的整数。对于行 ID，TiDB 做了一个小优化：如果表有整型主键，TiDB 会用该主键的值作为行 ID。

每一行数据会按照如下规则编码为一个 (Key, Value) 键值对：

```
Key:   tablePrefix{TableID}_recordPrefixSep{RowID}
Value: [col1, col2, col3, col4]
```

`tablePrefix` 和 `recordPrefixSep` 都是用于区分 Key 空间中其他数据的特殊字符串常量。字符串常量的具体值在 [映射关系总结](#summary-of-mapping-relationships) 中介绍。

### 索引数据到 Key-Value 的映射

TiDB 支持主键和二级索引（包括唯一索引和非唯一索引）。与表数据的映射方案类似，TiDB 为表的每个索引分配一个索引 ID，用 `IndexID` 表示。

对于主键和唯一索引，需要能够根据键值对快速定位到对应的 `RowID`，因此这类键值对的编码方式如下：

```
Key:   tablePrefix{TableID}_indexPrefixSep{IndexID}_indexedColumnsValue
Value: RowID
```

对于不需要满足唯一性约束的普通二级索引，一个 Key 可能对应多行数据。需要根据 Key 的范围查询对应的 `RowID`。因此，键值对的编码方式如下：

```
Key:   tablePrefix{TableID}_indexPrefixSep{IndexID}_indexedColumnsValue_{RowID}
Value: null
```

### 映射关系总结

上述所有编码规则中的 `tablePrefix`、`recordPrefixSep` 和 `indexPrefixSep` 都是用于区分 Key 空间中其他数据的字符串常量，定义如下：

```
tablePrefix     = []byte{'t'}
recordPrefixSep = []byte{'r'}
indexPrefixSep  = []byte{'i'}
```

还需要注意的是，在上述编码方案中，无论是表数据还是索引数据的 Key 编码方案，同一张表的所有行都有相同的 Key 前缀，同一个索引的所有数据也有相同的前缀。具有相同前缀的数据会在 TiKV 的 Key 空间中排列在一起。因此，通过精心设计后缀部分的编码方式，保证编码前后比较结果一致，表数据或索引数据就可以有序地存储在 TiKV 中。采用这种编码方案，一张表的所有行数据会按照 `RowID` 在 TiKV 的 Key 空间中有序排列，某个索引的数据也会根据索引数据的具体值（`indexedColumnsValue`）在 Key 空间中顺序排列。

### Key-Value 映射关系示例

本节通过一个简单示例帮助你理解 TiDB 的 Key-Value 映射关系。假设 TiDB 中存在如下表：

```sql
CREATE TABLE User (
     ID int,
     Name varchar(20),
     Role varchar(20),
     Age int,
     PRIMARY KEY (ID),
     KEY idxAge (Age)
);
```

假设表中有 3 行数据：

```
1, "TiDB", "SQL Layer", 10
2, "TiKV", "KV Engine", 20
3, "PD", "Manager", 30
```

每一行数据会被映射为一个 (Key, Value) 键值对，并且该表有一个 int 类型的主键，所以 `RowID` 的值就是主键的值。假设该表的 `TableID` 为 `10`，那么其在 TiKV 上存储的表数据为：

```
t10_r1 --> ["TiDB", "SQL  Layer", 10]
t10_r2 --> ["TiKV", "KV  Engine", 20]
t10_r3 --> ["PD", " Manager", 30]
```

除了主键外，该表还有一个非唯一的普通二级索引 `idxAge`。假设 `IndexID` 为 `1`，那么其在 TiKV 上存储的索引数据为：

```
t10_i1_10_1 --> null
t10_i1_20_2 --> null
t10_i1_30_3 --> null
```

上述示例展示了 TiDB 从关系模型到 Key-Value 模型的映射规则，以及该映射方案背后的设计考量。

## 元数据管理

TiDB 中的每个数据库和表都有元数据，描述其定义和各种属性。这些信息同样需要持久化，TiDB 也将这些信息存储在 TiKV 中。

每个数据库或表都会分配一个唯一的 ID。作为唯一标识符，当表数据被编码为 Key-Value 时，这个 ID 会以 `m_` 前缀编码到 Key 中，构成一个以序列化元数据为 Value 的键值对。

此外，TiDB 还使用专门的 (Key, Value) 键值对来存储所有表结构信息的最新版本号。这个键值对是全局的，每当 DDL 操作状态发生变化时，其版本号会加 1。TiDB 将该键值对持久化存储在 PD server 中，Key 为 `/tidb/ddl/global_schema_version`，Value 是 `int64` 类型的版本号值。同时，由于 TiDB 支持在线变更表结构，它会保持一个后台线程，持续检测 PD server 中表结构信息的版本号是否发生变化。该线程也保证版本变更能在一定时间内被感知到。

## SQL 层概述

TiDB 的 SQL 层（TiDB Server）将 SQL 语句转换为 Key-Value 操作，转发到分布式 Key-Value 存储层 TiKV，组装 TiKV 返回的结果，最终将查询结果返回给客户端。

该层的节点是无状态的。这些节点本身不存储数据，且完全等价。

### SQL 计算

最简单的 SQL 计算方案就是上一节介绍的 [表数据到 Key-Value 的映射](#mapping-of-table-data-to-key-value)，即将 SQL 查询映射为 KV 查询，通过 KV 接口获取对应数据，并进行各种计算。

例如，执行 `select count(*) from user where name = "TiDB"` 这个 SQL 语句时，TiDB 需要读取表中的所有数据，然后判断 `name` 字段是否为 `TiDB`，如果是则返回该行。其过程如下：

1. 构造 Key Range：一张表中所有 `RowID` 的范围是 `[0, MaxInt64)`。根据行数据 Key 的编码规则，使用 `0` 和 `MaxInt64` 可以构造一个左闭右开的 `[StartKey, EndKey)` 范围。
2. 扫描 Key Range：根据上述构造的 Key 范围，从 TiKV 读取数据。
3. 过滤数据：对每一行读取到的数据，计算 `name = "TiDB"` 这个表达式。如果结果为 `true`，则返回该行，否则跳过。
4. 计算 `Count(*)`：对每一行满足条件的数据，累加到 `Count(*)` 的结果中。

**整个过程如下图所示：**

![naive sql flow](/media/tidb-computing-native-sql-flow.jpeg)

这种方案直观且可行，但在分布式数据库场景下存在一些明显问题：

- 在扫描数据时，每一行都需要通过一次 KV 操作从 TiKV 读取，至少有一次 RPC 开销，如果需要扫描的数据量很大，开销会非常高。
- 并不是所有行都需要读取，不满足条件的数据无需读取。
- 查询结果只需要返回满足条件的行数，而不需要这些行的具体值。

### 分布式 SQL 操作

为了解决上述问题，计算应尽量靠近存储节点，以避免大量 RPC 调用。首先，SQL 的谓词条件 `name = "TiDB"` 应下推到存储节点进行计算，只返回有效行，避免无意义的网络传输。其次，聚合函数 `Count(*)` 也可以下推到存储节点进行预聚合，每个节点只需返回一个 `Count(*)` 结果，SQL 层再对各节点返回的 `Count(*)` 结果进行求和。

下图展示了数据逐层返回的过程：

![dist sql flow](/media/tidb-computing-dist-sql-flow.png)

### SQL 层架构

前文介绍了 SQL 层的一些功能，希望你对 SQL 语句的处理流程有了基本了解。实际上，TiDB 的 SQL 层要复杂得多，包含许多模块和层次。下图列出了重要模块及其调用关系：

![tidb sql layer](/media/tidb-computing-tidb-sql-layer.png)

用户的 SQL 请求会直接或通过 `Load Balancer` 发送到 TiDB Server。TiDB Server 会解析 `MySQL Protocol Packet`，获取请求内容，对 SQL 请求进行语法和语义解析，制定并优化查询计划，执行查询计划，获取并处理数据。所有数据都存储在 TiKV 集群中，因此在此过程中，TiDB Server 需要与 TiKV 交互并获取数据。最后，TiDB Server 需要将查询结果返回给用户。