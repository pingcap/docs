---
title: EXPLAIN RAW
summary: 显示 SQL 语句的逻辑执行计划，你可以使用它来分析、排查问题并提升查询效率。
---

# EXPLAIN RAW

显示 SQL 语句的逻辑执行计划，你可以使用它来分析、排查问题并提升查询效率。

## 语法 {#syntax}

```sql
EXPLAIN RAW <statement>
```

## 示例 {#examples}

```sql
explain raw select * from t1, t2 where (t1.a = t2.a and t1.a > 3) or (t1.a = t2.a);

Project: [a (#0),b (#1),a (#2),b (#3)]
 └── EvalScalar: [t1.a (#0), t1.b (#1), t2.a (#2), t2.b (#3)]
     └── Filter: [((t1.a (#0) = t2.a (#2)) AND (t1.a (#0) > 3)) OR (t1.a (#0) = t2.a (#2))]
         └── LogicalJoin: equi-conditions: [], non-equi-conditions: []
             ├── LogicalGet: default.default.t1
             └── LogicalGet: default.default.t2

explain raw select * from t1 inner join t2 on t1.a = t2.a and t1.b = t2.b and t1.a > 2;

 ----
 Project: [a (#0),b (#1),a (#2),b (#3)]
 └── EvalScalar: [t1.a (#0), t1.b (#1), t2.a (#2), t2.b (#3)]
     └── LogicalJoin: equi-conditions: [(t1.a (#0) = t2.a (#2)) AND (t1.b (#1) = t2.b (#3))], non-equi-conditions: [t1.a (#0) > 2]
         ├── LogicalGet: default.default.t1
         └── LogicalGet: default.default.t2
```