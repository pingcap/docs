---
title: RECLUSTER TABLE
summary: 对表重新聚簇。关于为什么以及何时需要对表重新聚簇，请参见 Re-clustering Table。
---

# RECLUSTER TABLE

> **注意：**
>
> 于 v1.2.25 引入。

对表重新聚簇。关于为什么以及何时需要对表重新聚簇，请参见 [对表重新聚簇](/tidb-cloud-lake/sql/cluster-key.md#cluster-key-management)。

## 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <table_name> RECLUSTER [ FINAL ] [ WHERE condition ] [ LIMIT <segment_count> ]
```

该命令对可处理的 segment 数量有一个限制，默认值为 `max_thread * 4`。你可以使用 **LIMIT** 选项修改此限制。或者，你还可以通过以下两种方式进一步对表中的数据进行聚簇：

- 对该表多次运行此命令。
- 使用 **FINAL** 选项持续优化该表，直到其完成全部聚簇。

> **注意：**
>
> 对表重新聚簇会消耗时间（如果包含 **FINAL** 选项，耗时会更长）和 credits（当你使用 {{{ .lake }}} 时）。在优化过程中，请勿对该表执行 DML 操作。

该命令不会从头开始对表进行聚簇。相反，它会使用聚簇算法，从最新的 **LIMIT** 个 segment 中选择并重组最混乱的现有存储块。

### 示例 {#examples}

```sql
-- create table
create table t(a int, b int) cluster by(a+1);

-- insert some data to t
insert into t values(1,1),(3,3);
insert into t values(2,2),(5,5);
insert into t values(4,4);

select * from clustering_information('default','t')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 3
   constant_block_count: 1
unclustered_block_count: 0
       average_overlaps: 1.3333
          average_depth: 2.0
  block_depth_histogram: {"00002":3}

-- alter table recluster
ALTER TABLE t RECLUSTER FINAL WHERE a != 4;

select * from clustering_information('default','t')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 2
   constant_block_count: 1
unclustered_block_count: 0
       average_overlaps: 1.0
          average_depth: 2.0
  block_depth_histogram: {"00002":2}
```