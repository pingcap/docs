---
title: Derive TopN or Limit from row_numbwe Window Function 
summary: Explain how we convert a pattern of a filter on row_number to TopN or Limit operator. This enables further TopN/Limit pushdown to TiKV which can greatly improve performance. 
---

# Derive TopN /Limit from Window Functions

This document describes a rewrite optimization done by TiDB optimizer that recognizes the TopN/Limit pattern based on window functions. The rule is done as a logical rewrite and based on the pattern of  a filter on the window function row_number. A simple pattern example is 
- "select * from (select row_number() over (order by a) as rownumber from t) DT where rownumber <= 3". This query is basically computing Top 3 values from table 't' ordered by column 'a' and can be rewritten as 
- WITH t_topN as (select a from t1 order by a limit 3) select * from (select row_number() over (order by a) as rownumber from t_topN) DT where rownumber <= 3
The rewrite is targeted for TiKV and useful since a TopN/limit can be pushed down to storage and cut down data transfer needed to TiDB.  The rewrite works for cases where no order by (Limit instead of TopN) and if the window function has a partition by. TopN is enhanced to work on partitions but restricted to the case where the partition key is a prefix of cluster key (primary key).  Finally, the optimization can be turned onn/off through a variable called Optimization Rules and Blocklist for Expression Pushdown.

### Example 1: Push down to the Coprocessors in the storage layer

{{< copyable "sql" >}}

```sql
create table t(id int primary key, a int not null);
explain select * from t order by a limit 10;
```

```
+----------------------------+----------+-----------+---------------+--------------------------------+
| id                         | estRows  | task      | access object | operator info                  |
+----------------------------+----------+-----------+---------------+--------------------------------+
| TopN_7                     | 10.00    | root      |               | test.t.a, offset:0, count:10   |
| └─TableReader_15           | 10.00    | root      |               | data:TopN_14                   |
|   └─TopN_14                | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10   |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

