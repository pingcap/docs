---
title: SQL Optimization Process
summary: 了解 TiDB 中 SQL 的逻辑和物理优化。
---

# SQL Optimization Process

在 TiDB 中，从输入查询到根据最终执行计划获取执行结果的过程如下所示：

![SQL Optimization Process](/media/sql-optimization.png)

在通过 `parser` 解析原始查询文本并进行一些简单的有效性检查后，TiDB 首先对查询进行一些逻辑等价的变换。关于详细的变换内容，请参见 [SQL Logical Optimization](/sql-logical-optimization.md)。

通过这些等价变换，这个查询在逻辑执行计划中变得更容易处理。完成等价变换后，TiDB 获取一个与原始查询等价的查询计划结构，然后根据数据分布和操作符的具体执行成本，获得最终的执行计划。详细内容请参见 [SQL Physical Optimization](/sql-physical-optimization.md)。

同时，在 TiDB 执行 [`PREPARE`](/sql-statements/sql-statement-prepare.md) 语句时，你可以选择启用缓存，以减少在 TiDB 中生成执行计划的成本。详细内容请参见 [Execution Plan Cache](/sql-prepared-plan-cache.md)。