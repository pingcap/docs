---
title: SELECT
summary: 从表中检索数据。
---

# SELECT

从表中检索数据。

## 语法 {#syntax}

```sql
[WITH]
SELECT
    [ALL | DISTINCT]
    [ TOP <n> ]
    <select_expr> | <col_name> [[AS] <alias>] | $<col_position> [, ...] | *
    COLUMNS <expr>
    [EXCLUDE (<col_name1> [, <col_name2>, <col_name3>, ...] ) ]
    [FROM table_references]
    [AT ...]
    [WHERE <expr>]
    [GROUP BY {{<col_name> | <expr> | <col_alias> | <col_position>},
         ... | <extended_grouping_expr>}]
    [HAVING <expr>]
    [ORDER BY {<col_name> | <expr> | <col_alias> | <col_position>} [ASC | DESC],
         [ NULLS { FIRST | LAST }]
    [LIMIT <row_count>]
    [OFFSET <row_count>]
    [IGNORE_RESULT]
```

- `SELECT` 语句还支持直接查询 stage 中的文件。语法和示例请参见[使用 {{{ .lake }}} 高效进行数据转换](/tidb-cloud-lake/sql/stage.md)。

- 本页示例中使用 `numbers(N)` 表进行测试。该表只有一个 UInt64 列（名为 `number`），包含从 0 到 N-1 的整数。

## SELECT 子句 {#select-clause}

### AS 关键字 {#as-keyword}

在 {{{ .lake }}} 中，你可以使用 `AS` 关键字为列指定别名。这样可以在 SQL 语句和查询结果中为列提供更具描述性且更易理解的名称：

- {{{ .lake }}} 建议在创建列别名时尽量避免使用特殊字符。不过，如果某些场景下确实需要使用特殊字符，则应将别名用反引号括起来，例如：`SELECT price AS \`$CA\` FROM ...`

- {{{ .lake }}} 会自动将别名转换为小写。例如，如果你将某列的别名设为 *Total*，那么它在结果中会显示为 *total*。如果你希望保留大小写，请将别名用反引号括起来：`\`Total\``。

```sql
SELECT number AS Total FROM numbers(3);
+--------+
| total  |
+--------+
|      0 |
|      1 |
|      2 |
+--------+

SELECT number AS `Total` FROM numbers(3);
+--------+
| Total  |
+--------+
|      0 |
|      1 |
|      2 |
+--------+
```

如果你在 `SELECT` 子句中为某列指定了别名，那么在该别名定义之后，你可以在 `WHERE`、`GROUP BY` 和 `HAVING` 子句中引用该别名，也可以在 `SELECT` 子句自身中引用它。

```sql
SELECT number * 2 AS a, a * 2 AS double FROM numbers(3) WHERE (a + 1) % 3 = 0;
+---+--------+
| a | double |
+---+--------+
| 2 |      4 |
+---+--------+

SELECT MAX(number) AS b, number % 3 AS c FROM numbers(100) GROUP BY c HAVING b > 8;
+----+---+
| b  | c |
+----+---+
| 99 | 0 |
| 97 | 1 |
| 98 | 2 |
+----+---+
```

如果你为某列指定的别名与列名相同，那么 `WHERE` 和 `GROUP BY` 子句会将该别名识别为列名；但是，`HAVING` 子句会将其识别为别名本身。

```sql
SELECT number * 2 AS number FROM numbers(3)
WHERE (number + 1) % 3 = 0
GROUP BY number
HAVING number > 5;

+--------+
| number |
+--------+
|     10 |
|     16 |
+--------+
```

### EXCLUDE 关键字 {#exclude-keyword}

按列名从结果中排除一个或多个列。该关键字通常与 `SELECT * ...` 一起使用，用于从结果中排除少量列，而不是检索所有列。

```sql
SELECT * FROM allemployees ORDER BY id;

---
| id | firstname | lastname | gender |
|----|-----------|----------|--------|
| 1  | Ryan      | Tory     | M      |
| 2  | Oliver    | Green    | M      |
| 3  | Noah      | Shuster  | M      |
| 4  | Lily      | McMeant   | F     |
| 5  | Macy      | Lee      | F      |

-- 从结果中排除 "id" 列
SELECT * EXCLUDE id FROM allemployees;

---
| firstname | lastname | gender |
|-----------|----------|--------|
| Noah      | Shuster  | M      |
| Ryan      | Tory     | M      |
| Oliver    | Green    | M      |
| Lily      | McMeant   | F     |
| Macy      | Lee      | F      |

-- 从结果中排除 "id" 和 "lastname" 列
SELECT * EXCLUDE (id,lastname) FROM allemployees;

---
| firstname | gender |
|-----------|--------|
| Oliver    | M      |
| Ryan      | M      |
| Lily      | F      |
| Noah      | M      |
| Macy      | F      |
```

### COLUMNS 关键字 {#columns-keyword}

COLUMNS 关键字提供了一种灵活的列选择机制，可基于字面量正则表达式模式和 lambda 表达式来选择列。

```sql
CREATE TABLE employee (
    employee_id INT,
    employee_name VARCHAR(255),
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO employee VALUES
(1, 'Alice', 'HR', 60000.00),
(2, 'Bob', 'IT', 75000.00),
(3, 'Charlie', 'Marketing', 50000.00),
(4, 'David', 'Finance', 80000.00);

-- Select columns with names starting with 'employee'
SELECT COLUMNS('employee.*') FROM employee;

┌────────────────────────────────────┐
│   employee_id   │   employee_name  │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
│               3 │ Charlie          │
│               4 │ David            │
└────────────────────────────────────┘

-- Select columns where the name contains the substring 'name'
SELECT COLUMNS(x -> x LIKE '%name%') FROM employee;

┌──────────────────┐
│   employee_name  │
├──────────────────┤
│ Alice            │
│ Bob              │
│ Charlie          │
│ David            │
└──────────────────┘
```

COLUMNS 关键字还可以与 EXCLUDE 一起使用，以在查询结果中显式排除特定列。

```sql
-- Select all columns excluding 'salary' from the 'employee' table
SELECT COLUMNS(* EXCLUDE salary) FROM employee;

┌───────────────────────────────────────────────────────┐
│   employee_id   │   employee_name  │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               1 │ Alice            │ HR               │
│               2 │ Bob              │ IT               │
│               3 │ Charlie          │ Marketing        │
│               4 │ David            │ Finance          │
└───────────────────────────────────────────────────────┘
```

### 列位置 {#column-position}

通过使用 $N，你可以表示 SELECT 子句中的某一列。例如，$2 表示第二列：

```sql
CREATE TABLE IF NOT EXISTS t1(a int, b varchar);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b');
SELECT a, $2 FROM t1;

+---+-------+
| a | $2    |
+---+-------+
| 1 | a     |
| 2 | b     |
+---+-------+
```

### 检索所有列 {#retrieving-all-columns}

`SELECT *` 语句用于从表或查询结果中检索所有列。这是一种便捷方式，无需指定单独的列名即可获取完整的数据集。

以下示例返回 my_table 中的所有列：

```sql
SELECT * FROM my_table;
```

{{{ .lake }}} 对 SQL 语法进行了扩展，允许查询以 `FROM <table>` 开始，而无需显式使用 `SELECT *`：

```sql
FROM my_table;
```

这等价于：

```sql
SELECT * FROM my_table;
```

## FROM 子句 {#from-clause}

SELECT 语句中的 FROM 子句用于指定要查询数据的源表或源表集合。你也可以将 FROM 子句放在 SELECT 子句之前，以提高代码可读性，尤其是在处理较长的 SELECT 列表或希望快速识别所选列来源时。

```sql
-- The following two statements are equivalent:

-- Statement 1: Using SELECT clause with FROM clause
SELECT number FROM numbers(3);

-- Statement 2: Equivalent representation with FROM clause preceding SELECT clause
FROM numbers(3) SELECT number;

+--------+
| number |
+--------+
|      0 |
|      1 |
|      2 |
+--------+
```

FROM 子句还可以指定一个位置，从而支持直接查询来自各种来源的数据，而无需先将其加载到表中。更多信息，参见[查询 stage 文件](/tidb-cloud-lake/sql/stage.md)。

## AT 子句 {#at-clause}

AT 子句使你能够查询数据的历史版本。更多信息，参见 [AT](/tidb-cloud-lake/sql/at.md)。

## WHERE 子句 {#where-clause}

```sql
SELECT number FROM numbers(3) WHERE number > 1;
+--------+
| number |
+--------+
|      2 |
+--------+
```

## GROUP BY 子句 {#group-by-clause}

```sql
--Group the rows of the result set by column alias
SELECT number%2 as c1, number%3 as c2, MAX(number) FROM numbers(10000) GROUP BY c1, c2;
+------+------+-------------+
| c1   | c2   | MAX(number) |
+------+------+-------------+
|    1 |    2 |        9995 |
|    1 |    1 |        9997 |
|    0 |    2 |        9998 |
|    0 |    1 |        9994 |
|    0 |    0 |        9996 |
|    1 |    0 |        9999 |
+------+------+-------------+

--Group the rows of the result set by column position in the SELECT list
SELECT number%2 as c1, number%3 as c2, MAX(number) FROM numbers(10000) GROUP BY 1, 2;
+------+------+-------------+
| c1   | c2   | MAX(number) |
+------+------+-------------+
|    1 |    2 |        9995 |
|    1 |    1 |        9997 |
|    0 |    2 |        9998 |
|    0 |    1 |        9994 |
|    0 |    0 |        9996 |
|    1 |    0 |        9999 |
+------+------+-------------+

```

## HAVING 子句 {#having-clause}

```sql
SELECT
    number % 2 as c1,
    number % 3 as c2,
    MAX(number) as max
FROM
    numbers(10000)
GROUP BY
    c1, c2
HAVING
    max > 9996;

+------+------+------+
| c1   | c2   | max  |
+------+------+------+
|    1 |    0 | 9999 |
|    1 |    1 | 9997 |
|    0 |    2 | 9998 |
+------+------+------+
```

## ORDER BY 子句 {#order-by-clause}

```sql
--Sort by column name in ascending order.
SELECT number FROM numbers(5) ORDER BY number ASC;
+--------+
| number |
+--------+
|      0 |
|      1 |
|      2 |
|      3 |
|      4 |
+--------+

--Sort by column name in descending order.
SELECT number FROM numbers(5) ORDER BY number DESC;
+--------+
| number |
+--------+
|      4 |
|      3 |
|      2 |
|      1 |
|      0 |
+--------+

--Sort by column alias.
SELECT number%2 AS c1, number%3 AS c2  FROM numbers(5) ORDER BY c1 ASC, c2 DESC;
+------+------+
| c1   | c2   |
+------+------+
|    0 |    2 |
|    0 |    1 |
|    0 |    0 |
|    1 |    1 |
|    1 |    0 |
+------+------+

--Sort by column position in the SELECT list
SELECT * FROM t1 ORDER BY 2 DESC;
+------+------+
| a    | b    |
+------+------+
|    2 |    3 |
|    1 |    2 |
+------+------+

SELECT a FROM t1 ORDER BY 1 DESC;
+------+
| a    |
+------+
|    2 |
|    1 |
+------+

--Sort with the NULLS FIRST or LAST option.

CREATE TABLE t_null (
  number INTEGER
);

INSERT INTO t_null VALUES (1);
INSERT INTO t_null VALUES (2);
INSERT INTO t_null VALUES (3);
INSERT INTO t_null VALUES (NULL);
INSERT INTO t_null VALUES (NULL);

--{{{ .lake }}} considers NULL values larger than any non-NULL values.
--The NULL values appear last in the following example that sorts the results in ascending order:

SELECT number FROM t_null order by number ASC;
+--------+
| number |
+--------+
|      1 |
|      2 |
|      3 |
|   NULL |
|   NULL |
+--------+

-- To make the NULL values appear first in the preceding example, use the NULLS FIRST option:

SELECT number FROM t_null order by number ASC nulls first;
+--------+
| number |
+--------+
|   NULL |
|   NULL |
|      1 |
|      2 |
|      3 |
+--------+

-- Use the NULLS LAST option to make the NULL values appear last in descending order:

SELECT number FROM t_null order by number DESC nulls last;
+--------+
| number |
+--------+
|      3 |
|      2 |
|      1 |
|   NULL |
|   NULL |
+--------+
```

## LIMIT 子句 {#limit-clause}

```sql
SELECT number FROM numbers(1000000000) LIMIT 1;
+--------+
| number |
+--------+
|      0 |
+--------+

SELECT number FROM numbers(100000) ORDER BY number LIMIT 2 OFFSET 10;
+--------+
| number |
+--------+
|     10 |
|     11 |
+--------+
```

为了优化大结果集查询的性能，{{{ .lake }}} 默认启用了 `lazy_read_threshold` 选项，默认值为 1,000。该选项专门用于包含 LIMIT 子句的查询。启用 `lazy_read_threshold` 后，当查询中指定的 LIMIT 数量小于或等于你设置的阈值时，将触发该优化。要禁用此选项，请将其设置为 0。

<details>
  <summary>工作原理</summary>
    <div>该优化可提升同时包含 ORDER BY 子句和 LIMIT 子句的查询性能。启用后，如果查询中的 LIMIT 数量小于指定阈值，则只会获取并排序 ORDER BY 子句中涉及的列，而不是整个结果集。</div><br/><div>系统获取并排序 ORDER BY 子句中涉及的列后，会应用 LIMIT 约束，从已排序的结果集中选出所需数量的行。随后，系统将这个受限的行集作为查询结果返回。该方法通过仅获取和排序必要的列来减少资源消耗，并通过将处理的行数限制在所需子集内，进一步优化查询执行。</div>
</details>

```sql
SELECT * FROM hits WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10 ignore_result;
Empty set (0.300 sec)

set lazy_read_threshold=0;
Query OK, 0 rows affected (0.004 sec)

SELECT * FROM hits WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10 ignore_result;
Empty set (0.897 sec)
```

## OFFSET 子句 {#offset-clause}

```sql
SELECT number FROM numbers(5) ORDER BY number OFFSET 2;
+--------+
| number |
+--------+
|      2 |
|      3 |
|      4 |
+--------+
```

## IGNORE_RESULT {#ignore-result}

不输出结果集。

```sql
SELECT number FROM numbers(2);
+--------+
| number |
+--------+
|      0 |
|      1 |
+--------+

SELECT number FROM numbers(2) IGNORE_RESULT;
-- Empty set
```

## 嵌套子查询 {#nested-sub-selects}

SELECT 语句可以嵌套在查询中。

```
SELECT ... [SELECT ...[SELECT [...]]]
```

```sql
SELECT MIN(number) FROM (SELECT number%3 AS number FROM numbers(10)) GROUP BY number%2;
+-------------+
| min(number) |
+-------------+
|           1 |
|           0 |
+-------------+
```