---
title: SELECT | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SELECT 的概述。
---

# SELECT

`SELECT` 语句用于从 TiDB 读取数据。

## 概述

```ebnf+diagram
SelectStmt ::=
    ( SelectStmtBasic | SelectStmtFromDualTable | SelectStmtFromTable )
    OrderBy? SelectStmtLimit? SelectLockOpt? SelectStmtIntoOption

SelectStmtBasic ::=
    "SELECT" SelectStmtOpts Field ("," Field)* ( "HAVING" Expression)?

SelectStmtFromDualTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" "DUAL" WhereClause?

SelectStmtFromTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" TableRefsClause
    WhereClause? GroupByClause? ( "HAVING" Expression)? WindowClause?

SelectStmtOpts ::=
    TableOptimizerHints DefaultFalseDistictOpt PriorityOpt SelectStmtSQLSmallResult
    SelectStmtSQLBigResult SelectStmtSQLBufferResult SelectStmtSQLCache SelectStmtCalcFoundRows
    SelectStmtStraightJoin

TableRefsClause ::=
    TableRef ( ',' TableRef )*

TableRef ::=
    TableFactor
|   JoinTable

TableFactor ::=
    TableName ( "PARTITION" "(" Identifier ("," Identifier)* ")" )? ("AS" TableAlias)? AsOfClause? TableSample?

JoinTable ::=
    TableRef
    (
        ("INNER" | "CROSS")? "JOIN" TableRef JoinClause?
        | "STRAIGHT_JOIN" TableRef "ON" Expression
        | ("LEFT" | "RIGHT") "OUTER"? "JOIN" TableRef JoinClause
        | "NATURAL" ("LEFT" | "RIGHT") "OUTER"? "JOIN" TableFactor
    )

JoinClause ::=
    ("ON" Expression
    | "USING" "(" ColumnNameList ")" )

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression

SelectStmtLimit ::=
    ("LIMIT" LimitOption ( ("," | "OFFSET") LimitOption )?
| "FETCH" ("FIRST" | "NEXT") LimitOption? ("ROW" | "ROWS") "ONLY" )

SelectLockOpt ::= 
    ( 'FOR' 'UPDATE' ( 'OF' TableList )? 'NOWAIT'?
|   'LOCK' 'IN' 'SHARE' 'MODE' )

TableList ::=
    TableName ( ',' TableName )*

WhereClause ::=
    "WHERE" Expression

GroupByClause ::=
    "GROUP" "BY" Expression

OrderBy ::=
    "ORDER" "BY" Expression

WindowClause ::=
    "WINDOW" WindowDefinition ("," WindowDefinition)*

TableSample ::=
    'TABLESAMPLE' 'REGIONS' '(' ')'
```

## 语法元素说明

| 语法元素 | 描述 |
|:--------------------- | :-------------------------------------------------- |
| `TableOptimizerHints` | 这是控制 TiDB 优化器行为的提示。更多信息请参考 [Optimizer Hints](/optimizer-hints.md)。 |
| `ALL`, `DISTINCT`, `DISTINCTROW` | `ALL`（默认）、`DISTINCT`/`DISTINCTROW` 修饰符指定是否返回重复行。`ALL` 表示返回所有匹配的行。 |
| `HIGH_PRIORITY` | `HIGH_PRIORITY` 赋予当前语句比其他语句更高的优先级。 |
| `SQL_CALC_FOUND_ROWS` | TiDB 不支持此功能，除非设置 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)，否则会返回错误。 |
| `SQL_CACHE`, `SQL_NO_CACHE` | `SQL_CACHE` 和 `SQL_NO_CACHE` 用于控制是否将请求结果缓存到 TiKV（RocksDB）的 BlockCache 中。对于一次性查询大量数据（如 `count(*)` 查询），建议填写 `SQL_NO_CACHE`，以避免冲刷热点用户数据到 BlockCache。 |
| `STRAIGHT_JOIN` | `STRAIGHT_JOIN` 强制优化器按照 `FROM` 子句中表的顺序进行联合查询。当优化器选择的连接顺序不佳时，可以使用此语法加快查询执行速度。 |
| `select_expr` | 每个 `select_expr` 表示要检索的列，包括列名和表达式。`*` 表示所有列。 |
| `FROM table_references` | `FROM table_references` 子句指示要从中检索行的表（如 `select * from t;`）、表的组合（如 `select * from t1 join t2;`）或甚至没有表（如 `select 1+1 from dual;`，等同于 `select 1+1;`）。 |
| `WHERE where_condition` | `WHERE` 子句（如果存在）指示行必须满足的条件。结果只包含满足条件的行。 |
| `GROUP BY` | `GROUP BY` 语句用于对结果集进行分组。 |
| `HAVING where_condition` | `HAVING` 子句和 `WHERE` 子句都用于过滤结果。`HAVING` 过滤 `GROUP BY` 的结果，而 `WHERE` 在聚合前过滤数据。 |
| `ORDER BY` | `ORDER BY` 子句用于根据列、表达式或 `select_expr` 列表中的项对数据进行升序或降序排序。 |
| `LIMIT` | `LIMIT` 子句用于限制返回的行数。`LIMIT` 接受一个或两个数字参数。一个参数时，表示最大返回行数，默认从第一行开始；两个参数时，第一个表示偏移量，第二表示最大返回行数。TiDB 还支持 `FETCH FIRST/NEXT n ROW/ROWS ONLY` 语法，效果与 `LIMIT n` 相同。可以省略 `n`，效果等同于 `LIMIT 1`。 |
| `Window window_definition` | 这是窗口函数的语法，通常用于进行一些分析性计算。更多信息请参考 [Window Function](/functions-and-operators/window-functions.md)。 |
| `FOR UPDATE` | `SELECT FOR UPDATE` 子句锁定结果集中的所有数据，以检测其他事务的并发更新。匹配查询条件但不存在于结果集中的数据（如其他事务在当前事务开始后写入的行）不会被读锁定。当 TiDB 使用 [Optimistic Transaction Mode](/optimistic-transaction.md) 时，事务冲突不会在语句执行阶段检测，因此当前事务不会像其他数据库（如 PostgreSQL）那样阻塞执行 `UPDATE`、`DELETE` 或 `SELECT FOR UPDATE`。在提交阶段，`SELECT FOR UPDATE` 所读行会在两阶段中提交，也就是说它们也会加入冲突检测。如果发生写冲突，所有包含 `SELECT FOR UPDATE` 的事务提交失败；如果没有冲突，提交成功。被锁定的行会生成新版本，以便在其他未提交事务提交时检测写冲突。当 TiDB 使用 [Pessimistic Transaction Mode](/pessimistic-transaction.md) 时，行为基本与其他数据库相同。详情请参见 [Differences from MySQL InnoDB](/pessimistic-transaction.md#differences-from-mysql-innodb)。TiDB 支持 `NOWAIT` 修饰符，详见 [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md#behaviors)。 |
| `LOCK IN SHARE MODE` | 为了保证兼容性，TiDB 解析这三个修饰符，但会忽略它们。 |
| `TABLESAMPLE` | 用于从表中抽取样本行。 |

> **注意：**
>
> 从 v6.6.0 版本开始，TiDB 支持 [Resource Control](/tidb-resource-control-ru-groups.md)。你可以利用此功能在不同资源组中以不同优先级执行 SQL 语句。通过为这些资源组配置合适的配额和优先级，可以获得更好的调度控制。当启用资源控制时，语句优先级（`HIGH_PRIORITY`）将不再生效。建议使用 [Resource Control](/tidb-resource-control-ru-groups.md) 来管理不同 SQL 语句的资源使用。

## 示例

### SELECT

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

```sql
mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock TABLESAMPLE REGIONS();
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         59.5000 |                 4 |
+-----------------+-------------------+
1 row in set (0.00 sec)

mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock;
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         54.9729 |           1000000 |
+-----------------+-------------------+
1 row in set (0.52 sec)
```

以上示例使用 `tiup bench tpcc prepare` 生成的数据。第一个查询展示了 `TABLESAMPLE` 的用法。

### SELECT ... INTO OUTFILE

`SELECT ... INTO OUTFILE` 语句用于将查询结果写入文件。

> **注意：**
>
> - 该语句仅适用于 TiDB 自托管版本，不支持 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)。
> - 该语句不支持将查询结果写入任何 [外部存储](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)，如 Amazon S3 或 GCS。

在语句中，可以通过以下子句指定输出文件的格式：

- `FIELDS TERMINATED BY`：指定字段分隔符。例如，可以设置为 `','` 输出逗号分隔值（CSV），或 `'\t'` 输出制表符分隔值（TSV）。
- `FIELDS ENCLOSED BY`：指定包裹每个字段的字符。
- `LINES TERMINATED BY`：指定行终止符，如果希望以特定字符结束一行。

假设有一个表 `t`，包含三列，定义如下：

```sql
mysql> CREATE TABLE t (a INT, b VARCHAR(10), c DECIMAL(10,2));
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t VALUES (1, 'a', 1.1), (2, 'b', 2.2), (3, 'c', 3.3);
Query OK, 3 rows affected (0.01 sec)
```

以下示例展示如何使用 `SELECT ... INTO OUTFILE` 将查询结果写入文件。

**示例 1：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file1';
Query OK, 3 rows affected (0.00 sec)
```

此时，查询结果存放在 `/tmp/tmp_file1`，内容如下：

```
1       a       1.10
2       b       2.20
3       c       3.30
```

**示例 2：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file2' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
Query OK, 3 rows affected (0.00 sec)
```

此时，查询结果存放在 `/tmp/tmp_file2`，内容如下：

```
"1","a","1.10"
"2","b","2.20"
"3","c","3.30"
```

**示例 3：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file3'
    -> FIELDS TERMINATED BY ',' ENCLOSED BY '\'' LINES TERMINATED BY '<<<\n';
Query OK, 3 rows affected (0.00 sec)
```

此时，查询结果存放在 `/tmp/tmp_file3`，内容如下：

```
'1','a','1.10'<<<
'2','b','2.20'<<<
'3','c','3.30'<<<
```

## MySQL 兼容性

- 不支持 `SELECT ... INTO @variable` 语法。
- 不支持 `SELECT ... INTO DUMPFILE` 语法。
- `SELECT .. GROUP BY expr` 不会像 MySQL 5.7 那样隐含 `GROUP BY expr ORDER BY expr`，而是遵循 MySQL 8.0 的行为，不隐含默认排序。
- `SELECT ... TABLESAMPLE ...` 是 TiDB 的扩展，旨在兼容其他数据库系统和 [ISO/IEC 9075-2](https://standards.iso.org/iso-iec/9075/-2/ed-6/en/) 标准，但目前不被 MySQL 支持。

## 相关链接

* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)