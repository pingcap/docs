---
title: EXPLAIN
---

Shows the execution plan of a SQL statement. An execution plan is shown as a tree consisting of different operators where you can see how Databend will execute the SQL statement. An operator usually includes one or more fields describing the actions Databend will perform or the objects related to the query.

For example, the following execution plan returned by the EXPLAIN command includes an operator named *TableScan* with several fields.

```sql
EXPLAIN SELECT * FROM allemployees;

---
TableScan
├── table: default.default.allemployees
├── read rows: 5
├── read bytes: 592
├── partitions total: 5
├── partitions scanned: 5
└── push downs: [filters: [], limit: NONE]
```

If you are using Databend Cloud, you can utilize the Query Profile feature to visualize the execution plan of your SQL statements.

## Syntax

```sql
EXPLAIN <statement>
```

## Examples

```sql
EXPLAIN select t.number from numbers(1) as t, numbers(1) as t1 where t.number = t1.number;
----
Project
├── columns: [number (#0)]
└── HashJoin
    ├── join type: INNER
    ├── build keys: [numbers.number (#1)]
    ├── probe keys: [numbers.number (#0)]
    ├── filters: []
    ├── TableScan(Build)
    │   ├── table: default.system.numbers
    │   ├── read rows: 1
    │   ├── read bytes: 8
    │   ├── partitions total: 1
    │   ├── partitions scanned: 1
    │   └── push downs: [filters: [], limit: NONE]
    └── TableScan(Probe)
        ├── table: default.system.numbers
        ├── read rows: 1
        ├── read bytes: 8
        ├── partitions total: 1
        ├── partitions scanned: 1
        └── push downs: [filters: [], limit: NONE]
```