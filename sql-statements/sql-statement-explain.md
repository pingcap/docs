---
title: EXPLAIN | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 EXPLAIN 的概述。
---

# `EXPLAIN`

`EXPLAIN` 语句显示查询的执行计划，而不执行该查询。它补充了 `EXPLAIN ANALYZE` 语句，后者会执行该查询。如果 `EXPLAIN` 的输出与预期结果不符，可以考虑对查询涉及的每个表执行 `ANALYZE TABLE`，以确保表统计信息是最新的。

> **注意：**
>
> 某些子查询在优化阶段会被预先执行，以生成最优的执行计划，即使在 `EXPLAIN` 语句中也是如此。关于此行为的更多信息以及如何禁用它，请参见 [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) 和 [禁用子查询的提前执行](#disable-the-early-execution-of-subqueries)。

`DESC` 和 `DESCRIBE` 语句是 `EXPLAIN` 语句的别名。`EXPLAIN <tableName>` 的替代用法详见 [`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)。

TiDB 支持 `EXPLAIN [options] FOR CONNECTION connection_id` 语句，但此语句与 MySQL 中的 `EXPLAIN FOR` 不同。更多详情请参见 [`EXPLAIN FOR CONNECTION`](#explain-for-connection)。

## 概要

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|   'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

## `EXPLAIN` 输出格式

> **注意：**
>
> 当你使用 MySQL 客户端连接到 TiDB 时，为了更清晰地阅读输出结果且避免换行，可以使用 `pager less -S` 命令。然后，在输出 `EXPLAIN` 结果后，可以按键盘上的右箭头 <kbd>→</kbd> 向右滚动输出内容。

> **注意：**
>
> 在返回的执行计划中，从 v6.4.0 起，`IndexJoin` 和 `Apply` 操作符的所有 probe 端子节点的 `estRows` 含义与 v6.4.0 之前不同。详细信息请参见 [TiDB 查询执行计划概览](/explain-overview.md#understand-explain-output)。

目前，TiDB 中的 `EXPLAIN` 输出包含 5 列：`id`、`estRows`、`task`、`access object`、`operator info`。执行计划中的每个操作符由这些属性描述，`EXPLAIN` 输出中的每一行描述一个操作符。每个属性的说明如下：

| 属性名          | 描述 |
|:----------------|:----------------------------------------------------------------------------------------------------------|
| id              | 操作符 ID 是整个执行计划中操作符的唯一标识。在 TiDB 2.1 中，ID 格式会显示操作符的树状结构。数据从子节点流向父节点。每个操作符只有一个父节点。 |
| estRows         | 预估该操作符输出的行数。此数字根据统计信息和操作符逻辑估算得出。在 TiDB 4.0 的早期版本中，`estRows` 被称为 `count`。 |
| task            | 操作符所属的任务类型。目前，执行计划分为两类任务：**root** 任务，在 tidb-server 上执行；以及 **cop** 任务，在 TiKV 或 TiFlash 上并行执行。任务层级的执行计划拓扑结构为：一个 root 任务后跟多个 cop 任务。root 任务使用 cop 任务的输出作为输入。cop 任务指 TiDB 下推到 TiKV 或 TiFlash 的任务。每个 cop 任务在 TiKV 集群或 TiFlash 集群中分布，由多个进程执行。 |
| access object   | 操作符访问的数据项信息，包括 `table`、`partition` 和 `index`（如果有的话）。只有直接访问数据的操作符才会有此信息。 |
| operator info   | 关于操作符的其他信息。每个操作符的 `operator info` 内容不同。可以参考以下示例。 |

## 示例

```sql
EXPLAIN SELECT 1;
```

```sql
+-------------------+---------+------+---------------+---------------+
| id                | estRows | task | access object | operator info |
+-------------------+---------+------+---------------+---------------+
| Projection_3      | 1.00    | root |               | 1->Column#1   |
| └─TableDual_4     | 1.00    | root |               | rows:1        |
+-------------------+---------+------+---------------+---------------+
2 rows in set (0.00 sec)
```

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.10 sec)
```

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
EXPLAIN SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

```sql
DESC SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

```sql
DESCRIBE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

```sql
EXPLAIN INSERT INTO t1 (c1) VALUES (4);
```

```sql
+----------+---------+------+---------------+---------------+
| id       | estRows | task | access object | operator info |
+----------+---------+------+---------------+---------------+
| Insert_1 | N/A     | root |               | N/A           |
+----------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

```sql
EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
```

```sql
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Update_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

```sql
EXPLAIN DELETE FROM t1 WHERE c1=3;
```

```sql
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Delete_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.01 sec)
```

要指定 `EXPLAIN` 输出的格式，可以使用 `FORMAT = xxx` 语法。目前，TiDB 支持以下格式：

| FORMAT | 描述 |
| ------ | ------ |
| Not specified  | 如果未指定格式，`EXPLAIN` 使用默认格式 `row`。 |
| `brief`        | `EXPLAIN` 输出中的操作符 ID 被简化，与未指定 `FORMAT` 时相比。 |
| `dot`          | `EXPLAIN` 输出 DOT 执行计划，可通过 `dot` 程序（在 `graphviz` 包中）生成 PNG 文件。 |
| `row`          | `EXPLAIN` 以表格格式输出结果。详细信息请参见 [理解查询执行计划](/explain-overview.md)。 |
| `tidb_json`    | `EXPLAIN` 以 JSON 格式输出执行计划，并将操作符信息存储在 JSON 数组中。 |
| `verbose`      | `EXPLAIN` 以 `row` 格式输出结果，增加 `estCost` 列，显示查询的预估成本。更多用法请参见 [SQL 计划管理](/sql-plan-management.md)。 |
| `plan_cache`   | `EXPLAIN` 以 `row` 格式输出结果，附带 [Plan Cache](/sql-non-prepared-plan-cache.md#diagnostics) 信息作为警告。 |

<SimpleTab>

<div label="brief">

以下是 `EXPLAIN` 中 `FORMAT` 设置为 `"brief"` 时的示例：


```sql
EXPLAIN FORMAT = "brief" DELETE FROM t1 WHERE c1 = 3;
```

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| Delete                  | N/A     | root      |               | N/A                            |
| └─TableReader           | 0.00    | root      |               | data:Selection                 |
|   └─Selection           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.001 sec)
```

</div>

<div label="DotGraph">

除了 MySQL 标准结果格式外，TiDB 还支持 DotGraph 格式，你需要在 `FORMAT` 中指定 `"dot"`，示例如下：


```sql
CREATE TABLE t(a bigint, b bigint);
EXPLAIN format = "dot" SELECT A.a, B.b FROM t A JOIN t B ON A.a > B.b WHERE A.a < 10;
```

```sql
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dot 内容                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|
digraph Projection_8 {
subgraph cluster8{
node [style=filled, color=lightgrey]
color=black
label = "root"
"Projection_8" -> "HashJoin_9"
"HashJoin_9" -> "TableReader_13"
"HashJoin_9" -> "Selection_14"
"Selection_14" -> "TableReader_17"
}
subgraph cluster12{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_12" -> "TableFullScan_11"
}
subgraph cluster16{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_16" -> "TableFullScan_15"
}
"TableReader_13" -> "Selection_12"
"TableReader_17" -> "Selection_16"
}
 |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

如果你的电脑安装了 `dot` 程序，可以用以下方法生成 PNG 文件：

```bash
dot xx.dot -T png -O

上述语句返回的 xx.dot 即为结果内容。
```

如果你的电脑没有 `dot` 程序，可以将结果复制到 [此网站](http://www.webgraphviz.com/) 获取树状图：

![Explain Dot](/media/explain_dot.png)

</div>

<div label="JSON">

若要以 JSON 格式输出，在 `EXPLAIN` 语句中指定 `FORMAT = "tidb_json"`。示例如下：

```sql
CREATE TABLE t(id int primary key, a int, b int, key(a));
EXPLAIN FORMAT = "tidb_json" SELECT id FROM t WHERE a = 1;
```

```
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TiDB_JSON                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| [
    {
        "id": "Projection_4",
        "estRows": "10.00",
        "taskType": "root",
        "operatorInfo": "test.t.id",
        "subOperators": [
            {
                "id": "IndexReader_6",
                "estRows": "10.00",
                "taskType": "root",
                "operatorInfo": "index:IndexRangeScan_5",
                "subOperators": [
                    {
                        "id": "IndexRangeScan_5",
                        "estRows": "10.00",
                        "taskType": "cop[tikv]",
                        "accessObject": "table:t, index:a(a)",
                        "operatorInfo": "range:[1,1], keep order:false, stats:pseudo"
                    }
                ]
            }
        ]
    }
]
```

在输出中，`id`、`estRows`、`taskType`、`accessObject` 和 `operatorInfo` 的含义与默认格式中的列相同。`subOperators` 是存储子节点的数组。子节点的字段和含义与父节点相同。如果某个字段缺失，表示该字段为空。

</div>

</SimpleTab>

## MySQL 兼容性

* TiDB 中 `EXPLAIN` 的格式和潜在的执行计划与 MySQL 有较大差异。
* TiDB 不支持 `FORMAT=JSON` 或 `FORMAT=TREE` 选项。
* TiDB 中 `FORMAT=tidb_json` 是默认 `EXPLAIN` 结果的 JSON 格式输出。其格式和字段与 MySQL 中的 `FORMAT=JSON` 输出不同。

### `EXPLAIN FOR CONNECTION`

`EXPLAIN FOR CONNECTION` 用于获取当前执行的 SQL 查询或连接中最后执行的 SQL 查询的执行计划。输出格式与 `EXPLAIN` 相同，但 TiDB 中的实现与 MySQL 不同。它们的差异（除输出格式外）如下：

- 如果连接处于空闲状态，MySQL 返回空结果，而 TiDB 返回最后执行的查询计划。
- 如果尝试获取当前会话的执行计划，MySQL 返回错误，而 TiDB 正常返回结果。
- MySQL 要求登录用户与被查询的连接相同，或登录用户具有 **`PROCESS`** 权限；而 TiDB 要求登录用户与被查询的连接相同，或登录用户具有 **`SUPER`** 权限。

## 相关链接

* [理解查询执行计划](/explain-overview.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
