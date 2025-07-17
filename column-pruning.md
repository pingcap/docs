---
title: Column Pruning
summary: 了解 TiDB 中的 column pruning 的用法。
---

# Column Pruning

column pruning 的基本思想是，对于在操作符中未使用的列，优化器在优化过程中无需保留它们。移除这些列可以减少 I/O 资源的使用，并有助于后续的优化。以下是一个列重复的示例：

假设在表 t 中有四个列（a、b、c 和 d）。你可以执行以下语句：

```sql
select a from t where b> 5
```

在这个查询中，只使用了列 a 和列 b，而列 c 和列 d 是冗余的。关于该语句的查询计划，`Selection` 操作符使用了列 b，然后 `DataSource` 操作符使用了列 a 和列 b。列 c 和列 d 可以被裁剪，因为 `DataSource` 操作符不读取它们。

因此，当 TiDB 在逻辑优化阶段进行自上而下的扫描时，会裁剪掉冗余的列以减少资源浪费。这个扫描过程被称为 "Column Pruning"，对应的规则是 `columnPruner`。如果你想禁用此规则，可以参考 [The Blocklist of Optimization Rules and Expression Pushdown](/blocklist-control-plan.md)。