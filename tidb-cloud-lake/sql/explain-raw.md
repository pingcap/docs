---
title: EXPLAIN RAW
summary: クエリの分析、トラブルシューティング、効率改善に使用できる SQL 文の論理実行計画を表示します。
---

# EXPLAIN RAW

クエリの分析、トラブルシューティング、効率改善に使用できる SQL 文の論理実行計画を表示します。

## 構文 {#syntax}

```sql
EXPLAIN RAW <statement>
```

## 例 {#examples}

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