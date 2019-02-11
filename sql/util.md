---
title: Utility Statements
summary: Learn how to use the utility statements, including the `DESCRIBE`, `EXPLAIN`, and `USE` statements.
category: user guide
---

# Utility Statements

This document describes the utility statements, including the `DESCRIBE`, `EXPLAIN`, and `USE` statements.

## `DESCRIBE` statement

The `DESCRIBE` and `EXPLAIN` statements are synonyms, which can also be abbreviated as `DESC`. See the usage of the `EXPLAIN` statement.

## `EXPLAIN` statement

```sql
{EXPLAIN | DESCRIBE | DESC}
    tbl_name [col_name]

{EXPLAIN | DESCRIBE | DESC}
    [explain_type]
    explainable_stmt

explain_type:
    FORMAT = format_name

format_name:
    "DOT"

explainable_stmt: {
    SELECT statement
  | DELETE statement
  | INSERT statement
  | REPLACE statement
  | UPDATE statement
}
```

For more information about the `EXPLAIN` statement, see [Understand the Query Execution Plan](../sql/understanding-the-query-execution-plan.md).

In addition to the MySQL standard result format, TiDB also supports DotGraph and you need to specify `FORMAT = "dot"` as in the following example:

```sql
create table t(a bigint, b bigint);
desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;

TiDB > desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dot contents                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|
digraph HashRightJoin_7 {
subgraph cluster7{
node [style=filled, color=lightgrey]
color=black
label = "root"
"HashRightJoin_7" -> "TableReader_10"
"HashRightJoin_7" -> "TableReader_12"
}
subgraph cluster9{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_9" -> "TableScan_8"
}
subgraph cluster11{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"TableScan_11"
}
"TableReader_10" -> "Selection_9"
"TableReader_12" -> "TableScan_11"
}
 |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

If the `dot` program (in the `graphviz` package) is installed on your computer, you can generate a PNG file using the following method:

```bash
dot xx.dot -T png -O

The xx.dot is the result returned by the above statement.
```

If the `dot` program is not installed on your computer, copy the result to [this website](http://www.webgraphviz.com/) to get a tree diagram:

![Explain Dot](../media/explain_dot.png)

## `USE` statement

```sql
USE db_name
```

The `USE` statement is used to switch the default database. If the table in SQL statements does not display the specified database, then use the default database.

## `TRACE` statement

```sql
TRACE [FORMAT = format_name] traceable_stmt

format_name:
    "json" | "row"

traceable_stmt: {
    SELECT statement
  | DELETE statement
  | INSERT statement
  | REPLACE statement
  | UPDATE statement
}
```

```sql
mysql> trace format = 'row' select * from mysql.user;
+---------------------------|-----------------|------------+
| operation                 | startTS         | duration   |
+---------------------------|-----------------|------------+
| session.getTxnFuture      | 19:54:35.310841 | 4.255µs    |
|   ├─session.Execute       | 19:54:35.310837 | 928.349µs  |
|   ├─session.ParseSQL      | 19:54:35.310906 | 35.379µs   |
|   ├─executor.Compile      | 19:54:35.310972 | 420.688µs  |
|   ├─session.runStmt       | 19:54:35.311427 | 222.431µs  |
|   ├─session.CommitTxn     | 19:54:35.311601 | 14.696µs   |
|   ├─recordSet.Next        | 19:54:35.311828 | 419.797µs  |
|   ├─tableReader.Next      | 19:54:35.311834 | 379.932µs  |
|   ├─recordSet.Next        | 19:54:35.312310 | 26.831µs   |
|   └─tableReader.Next      | 19:54:35.312314 | 2.84µs     |
+---------------------------|-----------------|------------+
10 rows in set (0.00 sec)
```

When the `format` is `json`, the output is some `json` text. If the text is too long, they are split into multiple lines.

The `json` output can be viewed in the Web UI which is integrated in TiDB, here is an demo:

![](https://user-images.githubusercontent.com/1420062/48955365-8b82dc80-ef88-11e8-9ecb-22d0bcf565c3.gif)
