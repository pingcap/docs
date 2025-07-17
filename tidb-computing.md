---
title: TiDB 计算
summary: 了解 TiDB 数据库的计算层。
---

# TiDB 计算

基于 TiKV 提供的分布式存储，TiDB 构建了结合了事务处理能力和数据分析能力的计算引擎。本文档首先介绍一种将数据映射到 TiKV 中 (Key, Value) 键值对的算法，然后介绍 TiDB 如何管理元数据，最后说明 TiDB SQL 层的架构。

关于计算层所依赖的存储方案，本文仅介绍 TiKV 的行存储结构。对于 OLAP 服务，TiDB 引入了列存储方案 [TiFlash](/tiflash/tiflash-overview.md) 作为 TiKV 的扩展。

## 将表数据映射到 Key-Value

本节描述将数据映射到 TiDB 中 (Key, Value) 键值对的方案。待映射的数据包括以下两类：

- 表中每一行的数据，以下简称表数据。
- 表中所有索引的数据，以下简称索引数据。

### 表数据到 Key-Value 的映射

在关系型数据库中，一个表可能有许多列。为了将每一行中每一列的数据映射到 (Key, Value) 键值对，需要考虑如何构造 Key。首先，在 OLTP 场景下，存在许多对单行或多行数据的增删改查操作，这需要数据库能够快速读取一行数据。因此，每个 Key 应该具有唯一的 ID（显式或隐式），以便快速定位。然后，许多 OLAP 查询需要对整个表进行扫描。如果能将表中所有行的 Key 编码成一个范围，整个表就可以通过范围查询高效扫描。

基于上述考虑，TiDB 中表数据到 Key-Value 的映射设计如下：

- 为了确保同一表的数据保持在一起，便于搜索，TiDB 为每个表分配一个表 ID，用 `TableID` 表示。表 ID 是在整个集群中唯一的整数。
- TiDB 为表中的每一行数据分配一个行 ID，用 `RowID` 表示。行 ID 也是整数，在表内唯一。对于行 ID，TiDB 做了一个小的优化：如果表有一个整数类型的主键，TiDB 会使用该主键的值作为行 ID。

每一行数据根据以下规则编码为 (Key, Value) 键值对：

```
Key:   tablePrefix{TableID}_recordPrefixSep{RowID}
Value: [col1, col2, col3, col4]
```

`tablePrefix` 和 `recordPrefixSep` 都是用来区分 Key 空间中其他数据的特殊字符串常量。具体的字符串常量值在 [Mapping关系总结](#summary-of-mapping-relationships) 中介绍。

### 索引数据到 Key-Value 的映射

TiDB 支持主键和二级索引（包括唯一索引和非唯一索引）。与表数据映射方案类似，TiDB 为表的每个索引分配一个索引 ID，用 `IndexID` 表示。

对于主键和唯一索引，为了能根据 Key-Value 快速定位对应的 `RowID`，此类 Key-Value 编码如下：

```
Key:   tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
Value: RowID
```

对于不需要满足唯一性约束的普通二级索引，一个 Key 可能对应多行数据。需要根据 Key 的范围查询对应的 `RowID`，因此此类 Key-Value 必须按照以下规则编码：

```
Key:   tablePrefix{TableID}_indexPrefixSep{IndexID}_indexedColumnsValue_{RowID}
Value: null
```

### Mapping关系总结

上述所有编码规则中的 `tablePrefix`、`recordPrefixSep` 和 `indexPrefixSep` 都是用来区分 KV 与 Key 空间中其他数据的字符串常量，定义如下：

```
tablePrefix     = []byte{'t'}
recordPrefixSep = []byte{'r'}
indexPrefixSep  = []byte{'i'}
```

还需注意，在上述编码方案中，无论是表数据还是索引数据的 Key 编码方案，表中的所有行具有相同的 Key 前缀，索引的所有数据也具有相同的前缀。具有相同前缀的数据在 TiKV 的 Key 空间中会被一同存放。因此，通过精心设计后缀部分的编码方案，确保编码前后比较保持一致，可以在 TiKV 中以有序的方式存储表数据或索引数据。利用此编码方案，表中的所有行数据会按照 `RowID` 在 TiKV 的 Key 空间中有序排列，特定索引的数据也会根据索引数据的具体值 (`indexedColumnsValue`) 顺序存放。

### Key-Value 映射关系示例

本节通过一个简单示例帮助理解 TiDB 的 Key-Value 映射关系。假设 TiDB 中存在如下表：

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

每一行数据映射为一个 (Key, Value) 键值对，且该表的主键类型为 `int`，因此 `RowID` 的值即为主键值。假设该表的 `TableID` 为 `10`，则存储在 TiKV 上的表数据为：

```
t10_r1 --> ["TiDB", "SQL  Layer", 10]
t10_r2 --> ["TiKV", "KV  Engine", 20]
t10_r3 --> ["PD", " Manager", 30]
```

除了主键外，表中还有一个非唯一的普通二级索引 `idxAge`，其 `IndexID` 为 `1`，存储在 TiKV 上的索引数据为：

```
t10_i1_10_1 --> null
t10_i1_20_2 --> null
t10_i1_30_3 --> null
```

上述示例展示了关系模型到 TiDB 中 Key-Value 模型的映射规则，以及此映射方案背后的考虑。

## 元数据管理

TiDB 中的每个数据库和表都拥有元数据，指示其定义和各种属性。这些信息也需要持久化存储，TiDB 同样将其存储在 TiKV 中。

每个数据库或表都被赋予一个唯一的 ID。作为唯一标识符，在将表数据编码为 Key-Value 时，此 ID 会在 Key 中以 `m_` 前缀编码，构成一个存储序列化元数据的 Key-Value 对。

此外，TiDB 还使用一个专用的 (Key, Value) 键值对存储所有表结构信息的最新版本号。此 Key-Value 对是全局的，每当 DDL 操作状态发生变化时，其版本号会增加 `1`。TiDB 将此 Key-Value 持久化存储在 PD 服务器中，Key 为 `/tidb/ddl/global_schema_version`，Value 为 `int64` 类型的版本号值。同时，由于 TiDB 支持在线架构变更，它会在后台持续检测存储在 PD 服务器中的表结构信息的版本号是否发生变化，以确保在一定时间内可以获取到版本变更。

## SQL 层概述

TiDB 的 SQL 层，TiDB Server，将 SQL 语句转化为 Key-Value 操作，转发到分布式的 Key-Value 存储层 TiKV，组装 TiKV 返回的结果，最终将查询结果返回给客户端。

该层的节点是无状态的。这些节点本身不存储数据，完全是等价的。

### SQL 计算

最简单的 SQL 计算方案是前述的 [表数据到 Key-Value 的映射](#mapping-of-table-data-to-key-value)，它将 SQL 查询映射到 KV 查询，通过 KV 接口获取对应数据，并执行各种计算。

例如，要执行 `select count(*) from user where name = "TiDB"` 这条 SQL 语句，TiDB 需要读取表中的所有数据，然后检查 `name` 字段是否为 `TiDB`，如果是，则返回该行。过程如下：

1. 构造 Key 范围：表中所有 `RowID` 在 `[0, MaxInt64)` 范围内。根据行数据的 Key 编码规则，使用 `0` 和 `MaxInt64` 可以构造一个 `[StartKey, EndKey)` 的范围（左闭右开）。
2. 扫描 Key 范围：根据上述构造的范围读取 TiKV 中的数据。
3. 过滤数据：对每一行读取到的数据，计算表达式 `name = "TiDB"`。如果结果为 `true`，则返回该行；否则跳过。
4. 统计 `Count(*)`：对每一行满足条件的，累计到 `Count(*)` 的结果中。

**整个流程示意如下：**

![naive sql flow](/media/tidb-computing-native-sql-flow.jpeg)

此方案直观且可行，但在分布式数据库场景中存在一些明显的问题：

- 在扫描过程中，每一行都通过至少一个 RPC 开销的 KV 操作从 TiKV 读取，若数据量很大，开销会非常高。
- 不需要读取所有不满足条件的行。只需读取满足条件的行即可。
- 从返回的结果中，只需要满足条件的行数，而不需要行的具体值。

### 分布式 SQL 操作

为解决上述问题，应尽可能将计算靠近存储节点，避免大量 RPC 调用。首先，应将 SQL 谓词条件 `name = "TiDB"` 下推到存储节点进行计算，只返回符合条件的有效行，从而避免无意义的网络传输。然后，聚合函数 `Count(*)` 也可以下推到存储节点进行预聚合，每个节点只需返回一个 `Count(*)` 的结果，SQL 层再将各节点返回的 `Count(*)` 结果相加。

下图展示了数据逐层返回的流程：

![dist sql flow](/media/tidb-computing-dist-sql-flow.png)

### SQL 层架构

前述部分介绍了 SQL 层的一些功能，希望你对 SQL 语句的处理有了基本了解。实际上，TiDB 的 SQL 层要复杂得多，包含许多模块和层级。下图列出了重要模块及调用关系：

![tidb sql layer](/media/tidb-computing-tidb-sql-layer.png)

用户的 SQL 请求可以直接或通过 `Load Balancer` 发送到 TiDB Server。TiDB Server 会解析 `MySQL Protocol Packet`，获取请求内容，进行语法和语义分析，生成并优化查询计划，执行查询计划，获取并处理数据。所有数据都存储在 TiKV 集群中，因此在此过程中，TiDB Server 需要与 TiKV 交互以获取数据。最后，TiDB Server 将查询结果返回给用户。
