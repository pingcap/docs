---
title: Partitioning
summary: 学习如何在 TiDB 中使用分区。
---

# Partitioning {#partitioning}

本文介绍了 TiDB 的分区实现。

## Partitioning types {#partitioning-types}

本节介绍 TiDB 支持的分区类型。目前，TiDB 支持 [Range partitioning](#range-partitioning)、[Range COLUMNS partitioning](#range-columns-partitioning)、[List partitioning](#list-partitioning)、[List COLUMNS partitioning](#list-columns-partitioning)、[Hash partitioning](#hash-partitioning) 和 [Key partitioning](#key-partitioning)。

-   Range partitioning、Range COLUMNS partitioning、List partitioning 和 List COLUMNS partitioning 用于解决应用中大量删除操作引起的性能问题，并支持快速删除分区。
-   Hash partitioning 和 Key partitioning 用于在写入量大的场景中分散数据。与 Hash partitioning 相比，Key partitioning 支持多列分布和非整数列的分区。

### Range partitioning {#range-partitioning}

当表按 Range 分区时，每个分区包含分区表达式值落在某个范围内的行。范围必须是连续且不重叠的。可以通过 `VALUES LESS THAN` 来定义。

假设你需要创建一个包含人员记录的表，示例如下：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
);
```

你可以根据需要用不同方式按 Range 分区。例如，可以用 `store_id` 列进行分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);
```

在此分区方案中，`store_id` 为 1 到 5 的员工行存放在 `p0` 分区，`store_id` 为 6 到 10 的存放在 `p1`。Range 分区要求分区必须按顺序，从最低到最高。

如果插入一行数据 `(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`，它会落在 `p2` 分区。但如果插入 `store_id` 大于 20 的记录，则会报错，因为 TiDB 无法知道该插入到哪个分区。这时可以在创建表时用 `MAXVALUE`：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

`MAXVALUE` 表示比所有其他整数值都大的整数值。现在，`store_id` 大于等于 16（最高定义值）的所有记录都存放在 `p3` 分区。

你也可以用 `job_code` 列的值进行分区，假设两位数的 `job_code` 表示普通员工，三位数表示办公室和客户支持人员，四位数表示管理人员。示例如下：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (job_code) (
    PARTITION p0 VALUES LESS THAN (100),
    PARTITION p1 VALUES LESS THAN (1000),
    PARTITION p2 VALUES LESS THAN (10000)
);
```

在此例中，普通员工的行存放在 `p0`，办公室和客户支持人员存放在 `p1`，管理人员存放在 `p2`。

除了用 `store_id` 分区外，还可以用日期进行分区。例如，用员工的离职年份进行分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY RANGE ( YEAR(separated) ) (
    PARTITION p0 VALUES LESS THAN (1991),
    PARTITION p1 VALUES LESS THAN (1996),
    PARTITION p2 VALUES LESS THAN (2001),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

在 Range 分区中，也可以基于 `timestamp` 列的值进行分区，例如用 `unix_timestamp()` 函数：

```sql
CREATE TABLE quarterly_report_status (
    report_id INT NOT NULL,
    report_status VARCHAR(20) NOT NULL,
    report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
    PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
    PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
    PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
    PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
    PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
    PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
    PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
    PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
    PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
    PARTITION p9 VALUES LESS THAN (MAXVALUE)
);
```

不允许在分区表达式中使用其他包含时间戳列的表达式。

Range 分区在满足以下条件时特别有用：

-   你想删除旧数据。例如，用前述的 `employees` 表，可以用 `ALTER TABLE employees DROP PARTITION p0;` 快速删除 1990 年之前离职的员工数据，比执行 `DELETE FROM employees WHERE YEAR(separated) <= 1990;` 更快。
-   你想用包含时间或日期值的列，或由其他系列产生的值的列进行分区。
-   你需要频繁对分区列进行查询。例如，执行如下查询时：

```sql
EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;
```

TiDB 可以快速知道只需要扫描 `p2` 分区中的数据，因为其他分区不符合 `WHERE` 条件。

### Range COLUMNS partitioning {#range-columns-partitioning}

Range COLUMNS 分区是 Range 分区的变体。可以用一个或多个列作为分区键。分区列的数据类型可以是整数、字符串（`CHAR` 或 `VARCHAR`）、`DATE` 和 `DATETIME`。不支持任何表达式（如非列分区）。

与 Range 分区一样，Range COLUMNS 分区也要求分区范围严格递增。以下示例中的分区定义不被支持：

```sql
CREATE TABLE t(
    a int,
    b datetime,
    c varchar(8)
) PARTITION BY RANGE COLUMNS(`c`,`b`)
(PARTITION `p20240520A` VALUES LESS THAN ('A','2024-05-20 00:00:00'),
 PARTITION `p20240520Z` VALUES LESS THAN ('Z','2024-05-20 00:00:00'),
 PARTITION `p20240521A` VALUES LESS THAN ('A','2024-05-21 00:00:00'));
```

    Error 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

假设你想用名字进行分区，删除旧的无效数据，可以如下创建表：

```sql
CREATE TABLE t (
  valid_until datetime,
  name varchar(255) CHARACTER SET ascii,
  notes text
)
PARTITION BY RANGE COLUMNS(name, valid_until)
(PARTITION `p2022-g` VALUES LESS THAN ('G','2023-01-01 00:00:00'),
 PARTITION `p2023-g` VALUES LESS THAN ('G','2024-01-01 00:00:00'),
 PARTITION `p2022-m` VALUES LESS THAN ('M','2023-01-01 00:00:00'),
 PARTITION `p2023-m` VALUES LESS THAN ('M','2024-01-01 00:00:00'),
 PARTITION `p2022-s` VALUES LESS THAN ('S','2023-01-01 00:00:00'),
 PARTITION `p2023-s` VALUES LESS THAN ('S','2024-01-01 00:00:00'))
```

上述 SQL 语句会按年份和名字进行分区，范围为 `[ ('', ''), ('G', '2023-01-01 00:00:00') )`，`[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )`，`[ ('G', '2024-01-01 00:00:00'), ('M', '2023-01-01 00:00:00') )`，`[ ('M', '2023-01-01 00:00:00'), ('M', '2024-01-01 00:00:00') )`，`[ ('M', '2024-01-01 00:00:00'), ('S', '2023-01-01 00:00:00') )` 和 `[ ('S', '2023-01-01 00:00:00'), ('S', '2024-01-01 00:00:00') )`。这样可以方便地删除无效数据，同时利用分区裁剪（partition pruning）对 `name` 和 `valid_until` 两列进行优化。在此例中，`[,)` 表示左闭右开区间。例如，`[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 表示名字为 `'G'`，年份在 `2023-01-01 00:00:00`（包含）到 `2024-01-01 00:00:00`（不包含）之间的数据范围，不包括 `(G, 2024-01-01 00:00:00)`。

### Range INTERVAL partitioning {#range-interval-partitioning}

Range INTERVAL 分区是 Range 分区的扩展，允许你轻松创建指定间隔的分区。从 v6.3.0 版本开始，TiDB 引入了 INTERVAL 分区，作为语法糖。

语法如下：

```sql
PARTITION BY RANGE [COLUMNS] (<分区表达式>)
INTERVAL (<间隔表达式>)
FIRST PARTITION LESS THAN (<表达式>)
LAST PARTITION LESS THAN (<表达式>)
[NULL PARTITION]
[MAXVALUE PARTITION]
```

例如：

```sql
CREATE TABLE employees (
    id int unsigned NOT NULL,
    fname varchar(30),
    lname varchar(30),
    hired date NOT NULL DEFAULT '1970-01-01',
    separated date DEFAULT '9999-12-31',
    job_code int,
    store_id int NOT NULL
) PARTITION BY RANGE (id)
INTERVAL (100) FIRST PARTITION LESS THAN (100) LAST PARTITION LESS THAN (10000) MAXVALUE PARTITION
```

它会创建如下表：

```sql
CREATE TABLE `employees` (
  `id` int unsigned NOT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL,
  `hired` date NOT NULL DEFAULT '1970-01-01',
  `separated` date DEFAULT '9999-12-31',
  `job_code` int DEFAULT NULL,
  `store_id` int NOT NULL
)
PARTITION BY RANGE (`id`)
(PARTITION `P_LT_100` VALUES LESS THAN (100),
 PARTITION `P_LT_200` VALUES LESS THAN (200),
...
 PARTITION `P_LT_9900` VALUES LESS THAN (9900),
 PARTITION `P_LT_10000` VALUES LESS THAN (10000),
 PARTITION `P_MAXVALUE` VALUES LESS THAN (MAXVALUE))
```

Range INTERVAL 分区也支持 [Range COLUMNS](#range-columns-partitioning)。

例如：

```sql
CREATE TABLE monthly_report_status (
    report_id int NOT NULL,
    report_status varchar(20) NOT NULL,
    report_date date NOT NULL
)
PARTITION BY RANGE COLUMNS (report_date)
INTERVAL (1 MONTH) FIRST PARTITION LESS THAN ('2000-01-01') LAST PARTITION LESS THAN ('2025-01-01')
```

它会创建此表：

    CREATE TABLE `monthly_report_status` (
      `report_id` int NOT NULL,
      `report_status` varchar(20) NOT NULL,
      `report_date` date NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    PARTITION BY RANGE COLUMNS(`report_date`)
    (PARTITION `P_LT_2000-01-01` VALUES LESS THAN ('2000-01-01'),
     PARTITION `P_LT_2000-02-01` VALUES LESS THAN ('2000-02-01'),
    ...
     PARTITION `P_LT_2024-11-01` VALUES LESS THAN ('2024-11-01'),
     PARTITION `P_LT_2024-12-01` VALUES LESS THAN ('2024-12-01'),
     PARTITION `P_LT_2025-01-01` VALUES LESS THAN ('2025-01-01'))

可选参数 `NULL PARTITION` 会创建一个定义为 `PARTITION P_NULL VALUES LESS THAN (<列类型的最小值>)` 的分区，仅在分区表达式为 `NULL` 时匹配。详见 [Handling of NULL with Range partitioning](#handling-of-null-with-range-partitioning)，该部分说明 `NULL` 被视为小于任何其他值。

可选参数 `MAXVALUE PARTITION` 会创建最后一个分区，定义为 `PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`。

#### ALTER INTERVAL partitioned tables {#alter-interval-partitioned-tables}

INTERVAL 分区还支持简化的添加和删除分区的语法。

以下语句会更改第一个分区。它会删除所有值小于给定表达式的分区，并将匹配的分区设为新的第一个分区。不会影响 NULL 分区。

```sql
ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)
```

以下语句会更改最后一个分区，即增加范围更大的新分区，留出空间存放新数据。它会添加新的分区，范围由当前的 INTERVAL 决定，直到包含给定的表达式。如果存在 `MAXVALUE PARTITION`，则不支持此操作，因为需要重新组织数据。

```sql
ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)
```

#### INTERVAL partitioning details and limitations {#interval-partitioning-details-and-limitations}

-   INTERVAL 分区功能仅涉及 `CREATE/ALTER TABLE` 语法，不会改变元数据，因此用新语法创建或修改的表仍然兼容 MySQL。
-   `SHOW CREATE TABLE` 的输出格式没有变化，以保持 MySQL 兼容。
-   新的 `ALTER` 语法适用于符合 INTERVAL 的现有表，无需用 `INTERVAL` 语法创建这些表。
-   要在 `RANGE COLUMNS` 分区中使用 `INTERVAL` 语法，只能指定单个整数、日期或日期时间类型的列作为分区键。

### List partitioning {#list-partitioning}

List 分区类似于 Range 分区。不同之处在于，List 分区中每个分区的所有行的分区表达式值都在某个值集内。每个分区定义的值集可以有任意多个值，但不能有重复值。可以用 `PARTITION ... VALUES IN (...)` 来定义值集。

假设你要创建一个人员记录表。示例如下：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

假设有 20 个门店，分布在 4 个区域，见下表：

    | Region  | Store ID Numbers     |
    | ------- | -------------------- |
    | North   | 1, 2, 3, 4, 5        |
    | East    | 6, 7, 8, 9, 10       |
    | West    | 11, 12, 13, 14, 15   |
    | Central | 16, 17, 18, 19, 20   |

如果你想把同一区域的员工数据存放在同一分区，可以用 `store_id` 进行 List 分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
```

创建分区后，可以方便地添加或删除某个区域的相关记录。例如，假设东区（East）所有门店都被卖给了另一家公司，可以用 `ALTER TABLE employees TRUNCATE PARTITION pEast` 快速删除该区域的所有数据，比用 `DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)` 更高效。

也可以用 `ALTER TABLE employees DROP PARTITION pEast` 删除整个分区，但这会同时删除分区定义中的 `pEast`，需要用 `ALTER TABLE ... ADD PARTITION` 恢复原有分区方案。

#### Default List partition {#default-list-partition}

从 v7.3.0 版本开始，可以为 List 或 List COLUMNS 分区表添加默认分区。默认分区作为备用分区，不匹配任何值集的行会存放在此分区。

> **Note:**
>
> 该功能是 TiDB 对 MySQL 语法的扩展。带有默认分区的 List 或 List COLUMNS 分区表，表中的数据不能直接复制到 MySQL。

以如下 List 分区表为例：

```sql
CREATE TABLE t (
  a INT,
  b INT
)
PARTITION BY LIST (a) (
  PARTITION p0 VALUES IN (1, 2, 3),
  PARTITION p1 VALUES IN (4, 5, 6)
);
Query OK, 0 rows affected (0.11 sec)
```

可以为表添加名为 `pDef` 的默认分区：

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef DEFAULT);
```

或

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef VALUES IN (DEFAULT));
```

这样，插入的值如果不在任何分区的值集内，就会自动放入默认分区。

```sql
INSERT INTO t VALUES (7, 7);
Query OK, 1 row affected (0.01 sec)
```

也可以在创建 List 或 List COLUMNS 分区表时添加默认分区。例如：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20),
    PARTITION pDefault DEFAULT
);
```

如果没有定义默认分区，插入值必须在 `PARTITION ... VALUES IN (...)` 定义的值集内，否则会报错。例如：

```sql
CREATE TABLE t (
  a INT,
  b INT
)
PARTITION BY LIST (a) (
  PARTITION p0 VALUES IN (1, 2, 3),
  PARTITION p1 VALUES IN (4, 5, 6)
);
Query OK, 0 rows affected (0.11 sec)

INSERT INTO t VALUES (7, 7);
ERROR 1525 (HY000): Table has no partition for value 7
```

为避免此错误，可以在 `INSERT` 时加 `IGNORE` 关键字。加上后，`INSERT` 只会插入匹配分区值集的行，不匹配的行会被忽略，不会报错。例如：

```sql
test> TRUNCATE t;
Query OK, 1 row affected (0.00 sec)

test> INSERT IGNORE INTO t VALUES (1, 1), (7, 7), (8, 8), (3, 3), (5, 5);
Query OK, 3 rows affected, 2 warnings (0.01 sec)
Records: 5  Duplicates: 2  Warnings: 2

test> select * from t;
+------+------+
| a    | b    |
+------+------+
|    5 |    5 |
|    1 |    1 |
|    3 |    3 |
+------+------+
3 rows in set (0.01 sec)
```

### List COLUMNS partitioning {#list-columns-partitioning}

List COLUMNS 分区是 List 分区的变体。可以用多列作为分区键。除了整数类型外，还可以用字符串、`DATE` 和 `DATETIME` 类型的列作为分区列。

假设你要将以下 12 个城市的门店员工划分为 4 个区域，示例如下：

```sql
    | Region | Cities                         |
    | :----- | ------------------------------ |
    | 1      | LosAngeles,Seattle, Houston    |
    | 2      | Chicago, Columbus, Boston      |
    | 3      | NewYork, LongIsland, Baltimore |
    | 4      | Atlanta, Raleigh, Cincinnati   |
```

可以用 List COLUMNS 分区，将每行存放在对应城市的分区中，示例如下：

```sql
CREATE TABLE employees_1 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(city) (
    PARTITION pRegion_1 VALUES IN('LosAngeles', 'Seattle', 'Houston'),
    PARTITION pRegion_2 VALUES IN('Chicago', 'Columbus', 'Boston'),
    PARTITION pRegion_3 VALUES IN('NewYork', 'LongIsland', 'Baltimore'),
    PARTITION pRegion_4 VALUES IN('Atlanta', 'Raleigh', 'Cincinnati')
);
```

与 List 分区不同，List COLUMNS 分区不需要在 `COLUMNS()` 中用表达式转换列值为整数。

List COLUMNS 分区也可以用 `DATE` 和 `DATETIME` 类型的列实现，示例如下。此例用与前例相同的列名，但用 `hired` 列进行 List COLUMNS 分区：

```sql
CREATE TABLE employees_2 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(hired) (
    PARTITION pWeek_1 VALUES IN('2020-02-01', '2020-02-02', '2020-02-03',
        '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07'),
    PARTITION pWeek_2 VALUES IN('2020-02-08', '2020-02-09', '2020-02-10',
        '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14'),
    PARTITION pWeek_3 VALUES IN('2020-02-15', '2020-02-16', '2020-02-17',
        '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21'),
    PARTITION pWeek_4 VALUES IN('2020-02-22', '2020-02-23', '2020-02-24',
        '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28')
);
```

此外，还可以在 `COLUMNS()` 中添加多个列。例如：

```sql
CREATE TABLE t (
    id int,
    name varchar(10)
)
PARTITION BY LIST COLUMNS(id,name) (
     partition p0 values IN ((1,'a'),(2,'b')),
     partition p1 values IN ((3,'c'),(4,'d')),
     partition p3 values IN ((5,'e'),(null,null))
);
```

### Hash partitioning {#hash-partitioning}

Hash 分区用于确保数据均匀分散到若干分区中。使用 Range 分区时，必须在定义时指定每个分区的值范围；使用 Hash 分区时，只需指定分区数。

创建 Hash 分区表时，在 `CREATE TABLE` 语句后加上 `PARTITION BY HASH (expr)` 子句。`expr` 是返回整数的表达式。如果列类型为整数，可以直接用列名。还可能需要加 `PARTITIONS num`，其中 `num` 是正整数，表示分区数。

示例：用 `store_id` 将表分成 4 个分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH(store_id)
PARTITIONS 4;
```

如果不指定 `PARTITIONS num`，默认为 1。

也可以用返回整数的表达式进行分区，例如按入职年份分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

最优的 Hash 函数是作用于单个表列，且值随列值变化而单调递增或递减的函数。

例如，`date_col` 是 `DATE` 类型列，`TO_DAYS(date_col)` 的值会随 `date_col` 变化而变化。`YEAR(date_col)` 与 `TO_DAYS(date_col)` 不同，因为并非每个 `date_col` 的变化都导致 `YEAR(date_col)` 的变化。

反之，假设有 `int_col` 列，类型为 `INT`。考虑表达式 `POW(5-int_col,3) + 6`，它不是一个好的 Hash 函数，因为 `int_col` 变化时，表达式的结果不成比例地变化。例如，从 5 变到 6 时，表达式结果变为 -1；从 6 变到 7 时，变化为 -7。

总结：当表达式形式更接近 `y = cx` 时，更适合作为 Hash 函数。因为非线性越强，数据在分区中的分散越不均。

理论上，涉及多个列值的表达式也可以进行裁剪（pruning），但判断哪些表达式适用较为困难且耗时。因此，不建议使用涉及多个列的哈希表达式。

TiDB 在使用 `PARTITION BY HASH` 时，会根据表达式的模数决定数据落在哪个分区。即：如果分区表达式为 `expr`，分区数为 `num`，则用 `MOD(expr, num)` 来决定数据存放的分区。假设定义如下：

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

插入一行数据，`col3` 为 `'2005-09-15'`，则会落在分区 1：

    MOD(YEAR('2005-09-01'),4)
    =  MOD(2005,4)
    =  1

### Key partitioning {#key-partitioning}

从 v7.0.0 版本开始，TiDB 支持 Key 分区。对于早于 v7.0.0 的版本，如果尝试创建 Key 分区表，TiDB 会将其作为非分区表创建并发出警告。

Key 分区和 Hash 分区都能将数据均匀分散到若干分区中。不同之处在于，Hash 分区只支持基于指定的整数表达式或整数列进行分散，而 Key 分区支持基于列列表进行分散，且分区列不限于整数类型。TiDB 的 Key 分区哈希算法与 MySQL 不同，导致数据分布也不同。

创建 Key 分区表时，在 `CREATE TABLE` 后加上 `PARTITION BY KEY (columnList)`。`columnList` 是一个或多个列名组成的列列表。每个列的类型可以是任何类型，除了 `BLOB`、`JSON` 和 `GEOMETRY`（注意 TiDB 不支持 `GEOMETRY`）。还可能需要加 `PARTITIONS num`（表示分区数的正整数）或定义分区名。例如，加入 `(PARTITION p0, PARTITION p1)` 表示将表划分为两个分区，名为 `p0` 和 `p1`。

示例：用 `store_id` 列进行 Key 分区，划分为 4 个分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY KEY(store_id)
PARTITIONS 4;
```

如果不指定 `PARTITIONS num`，默认为 1。

也可以用非整数列（如 `VARCHAR`）进行 Key 分区。例如，用 `fname` 列进行分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY KEY(fname)
PARTITIONS 4;
```

还可以用多个列进行分区。例如，用 `fname` 和 `store_id` 组成列列表，划分为 4 个分区：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY KEY(fname, store_id)
PARTITIONS 4;
```

与 MySQL 类似，TiDB 支持用空的分区列列表创建 Key 分区表，例如：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY KEY()
PARTITIONS 4;
```

如果表没有主键但有唯一键，则用唯一键作为分区键：

```sql
CREATE TABLE k1 (
    id INT NOT NULL,
    name VARCHAR(20),
    UNIQUE KEY (id)
)
PARTITION BY KEY()
PARTITIONS 2;
```

但如果唯一键列未定义为 `NOT NULL`，则会失败。

#### TiDB 如何处理线性 Hash 分区 {#how-tidb-handles-linear-hash-partitions}

在 v6.4.0 之前，如果在 TiDB 执行 [MySQL Linear Hash](https://dev.mysql.com/doc/refman/8.0/en/partitioning-linear-hash.html) 分区的 DDL 语句，只会创建非分区表。如果仍想用分区表，需要修改 DDL。

从 v6.4.0 开始，TiDB 支持解析 MySQL 的 `PARTITION BY LINEAR HASH` 语法，但会忽略其中的 `LINEAR` 关键字。已有的 MySQL Linear Hash 分区的 DDL 和 DML 语句可以直接在 TiDB 中执行，无需修改：

-   对于 MySQL Linear Hash 分区的 `CREATE` 语句，TiDB 会创建非线性 Hash 分区表（注意，TiDB 中没有 Linear Hash 分区表）。如果分区数是 2 的幂，TiDB 中的行分布与 MySQL 相同；否则，分布不同。这是因为非线性分区表用简单的“模分区数”，而线性分区用“模下一幂次并折叠值”的方式。详见 [#38450](https://github.com/pingcap/tidb/issues/38450)。

-   对于其他 MySQL Linear Hash 分区的语句，TiDB 也会按 MySQL 的方式执行，只是当分区数不是 2 的幂时，行的分布会不同，导致 [partition selection](#partition-selection)、`TRUNCATE PARTITION` 和 `EXCHANGE PARTITION` 的结果不同。

### TiDB 如何处理线性 Key 分区 {#how-tidb-handles-linear-key-partitions}

从 v7.0.0 开始，TiDB 支持解析 MySQL 的 `PARTITION BY LINEAR KEY` 语法，但会忽略 `LINEAR` 关键字，使用非线性哈希算法。

在 v7.0.0 之前，尝试创建 Key 分区表会被作为非分区表创建并发出警告。

### TiDB 如何处理 NULL {#how-tidb-partitioning-handles-null}

在 TiDB 中，允许用 `NULL` 作为分区表达式的计算结果。

> **Note:**
>
> `NULL` 不是整数。TiDB 的分区实现会将 `NULL` 视为比任何其他整数值都小，就像 `ORDER BY` 一样。

#### Range 分区中 NULL 的处理 {#handling-of-null-with-range-partitioning}

当向 Range 分区表插入一行，且用于确定分区的列值为 `NULL` 时，该行会存放在最小的分区中。

```sql
CREATE TABLE t1 (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY RANGE(c1) (
    PARTITION p0 VALUES LESS THAN (0),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

    Query OK, 0 rows affected (0.09 sec)

```sql
select * from t1 partition(p0);
```

    +------|--------+
    | c1   | c2     |
    +------|--------+
    | NULL | mothra |
    +------|--------+
    1 row in set (0.00 sec)

```sql
select * from t1 partition(p1);
```

    Empty set (0.00 sec)

```sql
select * from t1 partition(p2);
```

    Empty set (0.00 sec)

删除 `p0` 分区后验证结果：

```sql
alter table t1 drop partition p0;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
select * from t1;
```

    Empty set (0.00 sec)

#### Hash 分区中 NULL 的处理 {#handling-of-null-with-hash-partitioning}

在 Hash 分区中，处理 `NULL` 的方式不同——如果分区表达式的结果为 `NULL`，则视为 `0`。

```sql
CREATE TABLE th (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY HASH(c1)
PARTITIONS 2;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
```

    Query OK, 2 rows affected (0.04 sec)

```sql
select * from th partition (p0);
```

    +------|--------+
    | c1   | c2     |
    +------|--------+
    | NULL | mothra |
    |    0 | gigan  |
    +------|--------+
    2 rows in set (0.00 sec)

```sql
select * from th partition (p1);
```

    Empty set (0.00 sec)

可以看到，插入的 `(NULL, 'mothra')` 和 `(0, 'gigan')` 落在同一分区。

> **Note:**
>
> `NULL` 值在 TiDB 的 Hash 分区中处理方式与 [MySQL 分区中 NULL 的处理](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html) 一致，但实际行为与 MySQL 不完全相同。换句话说，MySQL 在此场景中的实现与其文档描述不一致。TiDB 的实际行为与本文描述一致。

#### Key 分区中 NULL 的处理 {#handling-of-null-with-key-partitioning}

Key 分区中，处理 `NULL` 的方式与 Hash 分区相同。若分区字段值为 `NULL`，视为 `0`。

## Partition management {#partition-management}

对于 `RANGE`、`RANGE COLUMNS`、`LIST` 和 `LIST COLUMNS` 分区表，可以进行如下管理：

-   使用 `ALTER TABLE <table name> ADD PARTITION (<partition specification>)` 添加分区。
-   使用 `ALTER TABLE <table name> DROP PARTITION <list of partitions>` 删除分区。
-   使用 `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>` 清空指定分区中的所有数据。`TRUNCATE PARTITION` 的逻辑类似于 [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)，但作用于分区。
-   使用 `ALTER TABLE <table name> REORGANIZE PARTITION <list of partitions> INTO (<new partition definitions>)` 进行合并、拆分或其他变更。

对于 `HASH` 和 `KEY` 分区表，可以进行如下管理：

-   使用 `ALTER TABLE <table name> COALESCE PARTITION <number of partitions to decrease by>` 减少分区数。此操作会在在线状态下将整个表复制到新的分区数中，重新组织分区。
-   使用 `ALTER TABLE <table name> ADD PARTITION <number of partitions to increase by | (additional partition definitions)>` 增加分区数。此操作也会在在线状态下复制整个表。
-   使用 `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>` 清空指定分区中的数据，逻辑同 [`TRUNCATE TABLE`]。

`EXCHANGE PARTITION` 通过交换一个分区和非分区表实现，类似于重命名表的操作 `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`。

例如，`ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` 会交换 `partitioned_table` 的 `p1` 分区和 `non_partitioned_table` 表。

确保所有要交换的行都符合分区定义，否则操作会失败。

注意，TiDB 有一些特定功能可能影响 `EXCHANGE PARTITION`，当表结构包含这些功能时，需要确保 `EXCHANGE PARTITION` 满足 [MySQL 的 EXCHANGE PARTITION 条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)。同时，确保这些特定功能在分区表和非分区表中定义一致。这些功能包括：

<CustomContent platform="tidb">

-   [Placement Rules in SQL](/placement-rules-in-sql.md): placement policies 一致。

</CustomContent>

-   [TiFlash](/tikv-overview.md): TiFlash 副本数一致。
-   [Clustered Indexes](/clustered-indexes.md): 分区表和非分区表都为 `CLUSTERED` 或都为 `NONCLUSTERED`。

此外，`EXCHANGE PARTITION` 与其他组件的兼容性有限制。分区表和非分区表都必须定义相同。

-   TiFlash：当分区表和非分区表的 TiFlash 副本定义不同，不能执行 `EXCHANGE PARTITION`。
-   TiCDC：当分区表和非分区表都含有主键或唯一键时，TiCDC 会复制 `EXCHANGE PARTITION` 操作，否则不会。
-   TiDB Lightning 和 BR：在导入（TiDB Lightning）或恢复（BR）过程中不执行 `EXCHANGE PARTITION`。

### 管理 Range、Range COLUMNS、List 和 List COLUMNS 分区 {#manage-range-range-columns-list-and-list-columns-partitions}

本节以以下 SQL 创建的分区表为例，介绍如何管理 Range 和 List 分区。

```sql
CREATE TABLE members (
    id int,
    fname varchar(255),
    lname varchar(255),
    dob date,
    data json
)
PARTITION BY RANGE (YEAR(dob)) (
 PARTITION pBefore1950 VALUES LESS THAN (1950),
 PARTITION p1950 VALUES LESS THAN (1960),
 PARTITION p1960 VALUES LESS THAN (1970),
 PARTITION p1970 VALUES LESS THAN (1980),
 PARTITION p1980 VALUES LESS THAN (1990),
 PARTITION p1990 VALUES LESS THAN (2000));

CREATE TABLE member_level (
 id int,
 level int,
 achievements json
)
PARTITION BY LIST (level) (
 PARTITION l1 VALUES IN (1),
 PARTITION l2 VALUES IN (2),
 PARTITION l3 VALUES IN (3),
 PARTITION l4 VALUES IN (4),
 PARTITION l5 VALUES IN (5));
```

#### Drop partitions {#drop-partitions}

```sql
ALTER TABLE members DROP PARTITION p1990;

ALTER TABLE member_level DROP PARTITION l5;
```

#### Truncate partitions {#truncate-partitions}

```sql
ALTER TABLE members TRUNCATE PARTITION p1980;

ALTER TABLE member_level TRUNCATE PARTITION l4;
```

#### Add partitions {#add-partitions}

```sql
ALTER TABLE members ADD PARTITION (PARTITION `p1990to2010` VALUES LESS THAN (2010));

ALTER TABLE member_level ADD PARTITION (PARTITION l5_6 VALUES IN (5,6));
```

对于 Range 分区表，`ADD PARTITION` 会在最后一个已有分区后追加新分区。新分区的 `VALUES LESS THAN` 定义的值必须大于已有分区，否则会报错：

```sql
ALTER TABLE members ADD PARTITION (PARTITION p1990 VALUES LESS THAN (2000));
```

    ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

#### 重新组织分区 {#reorganize-partitions}

拆分分区：

```sql
ALTER TABLE members REORGANIZE PARTITION `p1990to2010` INTO
(PARTITION p1990 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2010),
 PARTITION p2010 VALUES LESS THAN (2020),
 PARTITION p2020 VALUES LESS THAN (2030),
 PARTITION pMax VALUES LESS THAN (MAXVALUE));

ALTER TABLE member_level REORGANIZE PARTITION l5_6 INTO
(PARTITION l5 VALUES IN (5),
 PARTITION l6 VALUES IN (6));
```

合并分区：

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1950,p1950 INTO (PARTITION pBefore1960 VALUES LESS THAN (1960));

ALTER TABLE member_level REORGANIZE PARTITION l1,l2 INTO (PARTITION l1_2 VALUES IN (1,2));
```

修改分区方案定义：

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1960,p1960,p1970,p1980,p1990,p2000,p2010,p2020,pMax INTO
(PARTITION p1800 VALUES LESS THAN (1900),
 PARTITION p1900 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2100));

ALTER TABLE member_level REORGANIZE PARTITION l1_2,l3,l4,l5,l6 INTO
(PARTITION lOdd VALUES IN (1,3,5),
 PARTITION lEven VALUES IN (2,4,6));
```

在重新组织分区时，需注意以下要点：

-   重新组织（包括合并或拆分）会将原有分区变成一组新的定义，但不能改变分区类型（如由 List 改为 Range，或 Range COLUMNS 改为 Range）。
-   对于 Range 分区，只能重新组织相邻的分区：

```sql
ALTER TABLE members REORGANIZE PARTITION p1800,p2000 INTO (PARTITION p2000 VALUES LESS THAN (2100));
```

    ERROR 8200 (HY000): Unsupported REORGANIZE PARTITION of RANGE; not adjacent partitions

-   若要修改范围的终点，新的 `VALUES LESS THAN` 定义的值必须覆盖最后一个分区中的所有行，否则会报错：

```sql
INSERT INTO members VALUES (313, "John", "Doe", "2022-11-22", NULL);
ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2050)); -- 这会成功，因为 2050 覆盖了现有行
ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2020)); -- 这会失败，因为 2022 不在范围内
```

    ERROR 1526 (HY000): Table has no partition for value 2022

-   对于 List 分区，要修改某个分区的值集，新的定义必须覆盖该分区中的所有值，否则会报错：

```sql
INSERT INTO member_level (id, level) values (313, 6);
ALTER TABLE member_level REORGANIZE PARTITION lEven INTO (PARTITION lEven VALUES IN (2,4));
```

    ERROR 1526 (HY000): Table has no partition for value 6

-   重新组织后，相关分区的统计信息会变得过时，系统会发出如下警告。此时可以用 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句更新统计信息。

```sql
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 管理 Hash 和 Key 分区 {#manage-hash-and-key-partitions}

本节以以下 SQL 创建的分区表为例，介绍如何管理 Hash 分区。对于 Key 分区，也可以用相同的管理语句。

```sql
CREATE TABLE example (
  id INT PRIMARY KEY,
  data VARCHAR(1024)
)
PARTITION BY HASH(id)
PARTITIONS 2;
```

#### 增加分区数 {#increase-the-number-of-partitions}

将 `example` 表的分区数增加 1（从 2 增加到 3）：

```sql
ALTER TABLE example ADD PARTITION PARTITIONS 1;
```

也可以用定义分区的方式增加。例如，将分区数从 3 增加到 5，并指定新加入的分区名为 `pExample4` 和 `pExample5`：

```sql
ALTER TABLE example ADD PARTITION
(PARTITION pExample4 COMMENT = 'not p3, but pExample4 instead',
 PARTITION pExample5 COMMENT = 'not p4, but pExample5 instead');
```

#### 减少分区数 {#decrease-the-number-of-partitions}

不同于 Range 和 List 分区，Hash 和 Key 分区不支持 `DROP PARTITION`，但可以用 `COALESCE PARTITION` 减少分区数，或用 `TRUNCATE PARTITION` 删除特定分区中的所有数据。

将 `example` 表的分区数减少 1（从 5 到 4）：

```sql
ALTER TABLE example COALESCE PARTITION 1;
```

> **Note:**
>
> 改变 Hash 或 Key 分区表的分区数会将所有数据复制到新的分区数中，重新组织分区。因此，操作后会出现统计信息过时的警告。可以用 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息。
>
> ```sql
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                                |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
> ```

可以用 `SHOW CREATE TABLE` 查看当前 `example` 表的定义：

```sql
SHOW CREATE TABLE\G
```

    *************************** 1. row ***************************
           Table: example
    Create Table: CREATE TABLE `example` (
      `id` int NOT NULL,
      `data` varchar(1024) DEFAULT NULL,
      PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    PARTITION BY HASH (`id`)
    (PARTITION `p0`,
     PARTITION `p1`,
     PARTITION `p2`,
     PARTITION `pExample4` COMMENT 'not p3, but pExample4 instead')
    1 row in set (0.01 sec)

#### 清空分区 {#truncate-partitions}

清空某个分区中的所有数据：

```sql
ALTER TABLE example TRUNCATE PARTITION p0;
```

    Query OK, 0 rows affected (0.03 sec)

### 将分区表转换为非分区表 {#convert-a-partitioned-table-to-a-non-partitioned-table}

将分区表转换为非分区表，可以用以下语句，去除分区，复制所有行，并在线重建索引：

```sql
ALTER TABLE <table_name> REMOVE PARTITIONING
```

例如，将 `members` 分区表转换为非分区表：

```sql
ALTER TABLE members REMOVE PARTITIONING
```

### 对已有表进行分区 {#partition-an-existing-table}

要对已有的非分区表进行分区，或修改已分区表的分区类型，可以用以下语句，复制所有行，在线重建索引，依据新的分区定义：

```sql
ALTER TABLE <table_name> PARTITION BY <新分区类型和定义> [UPDATE INDEXES (<index name> {GLOBAL|LOCAL}[ , <index name> {GLOBAL|LOCAL}...])]
```

示例：将 `members` 表改为 Hash 分区，分 10 个分区：

```sql
ALTER TABLE members PARTITION BY HASH(id) PARTITIONS 10;
```

将 `member_level` 表改为 Range 分区：

```sql
ALTER TABLE member_level PARTITION BY RANGE(level)
(PARTITION pLow VALUES LESS THAN (1),
 PARTITION pMid VALUES LESS THAN (3),
 PARTITION pHigh VALUES LESS THAN (7),
 PARTITION pMax VALUES LESS THAN (MAXVALUE));
```

在对非分区表或已分区表重新分区时，可以根据需要更新索引为全局或本地：

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2),
    UNIQUE KEY uidx3(col3)
);

ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL);
```

## Partition pruning {#partition-pruning}

[Partition pruning](/partition-pruning.md) 是一种优化技术，思想简单——不要扫描不匹配的分区。

假设你创建了一个分区表 `t1`：

```sql
CREATE TABLE t1 (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    region_code TINYINT UNSIGNED NOT NULL,
    dob DATE NOT NULL
)

PARTITION BY RANGE( region_code ) (
    PARTITION p0 VALUES LESS THAN (64),
    PARTITION p1 VALUES LESS THAN (128),
    PARTITION p2 VALUES LESS THAN (192),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

如果你想得到以下 `SELECT` 语句的结果：

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

显然，结果只在 `p1` 和 `p2` 分区中，即只需在 `p1` 和 `p2` 中搜索匹配的行。排除不需要的分区就是所谓的“裁剪（pruning）”。如果优化器能裁剪掉部分分区，分区表的查询会比非分区表快得多。

优化器可以通过以下两种场景中的 `WHERE` 条件进行裁剪：

-   partition_column = 常量
-   partition_column IN (常量1, 常量2, ..., 常量N)

目前，分区裁剪不支持 `LIKE` 条件。

### 分区裁剪生效的某些情况 {#some-cases-for-partition-pruning-to-take-effect}

1.  分区裁剪使用了查询条件在分区表上，因此如果查询条件不能根据优化规则下推到分区表，裁剪不生效。

    例如：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    create table t2 (x int);
    ```

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x where t2.x > 5;
    ```

    在此查询中，左连接会转为内连接，然后 `t1.x > 5` 从 `t1.x = t2.x` 和 `t2.x > 5` 推导出来，因此可以用在裁剪中，只剩下 `p1` 分区。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    在此查询中，`t2.x > 5` 不能下推到 `t1` 的分区表，因此裁剪不会生效。

2.  由于裁剪在计划优化阶段完成，不适用于过滤条件在执行阶段才知道的情况。

    例如：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    ```

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    该查询从 `t2` 读取一行，用于 `t1` 的子查询。理论上，子查询中的 `t1.x > val` 表达式可以用来裁剪，但实际上在执行阶段才会生效。

3.  由于当前实现的限制，如果查询条件不能下推到 TiKV，也不能用作裁剪。

    以 `fn(col)` 表达式为例。如果 TiKV 的协处理器支持此 `fn` 函数，`fn(col)` 可能会在计划优化阶段根据谓词下推规则下推到叶子节点（即分区表），从而支持裁剪。

    如果不支持，则不会下推，`fn(col)` 会成为叶子节点上方的 `Selection` 节点。当前的裁剪实现不支持此类计划树。

4.  仅支持等值条件的 Hash 和 Key 分区。

5.  Range 分区中，裁剪生效的条件是分区表达式为 `col` 或 `fn(col)`，且查询条件为 `>`, `<`, `=`, `>=`, `<=` 之一。如果表达式为 `fn(col)`，则 `fn` 必须是单调递增或递减的。

    如果 `fn` 是单调的，对于任意 `x` 和 `y`，若 `x > y`，则 `fn(x) > fn(y)`，此时 `fn` 可以称为“严格单调”。又如，若 `x > y`，则 `fn(x) >= fn(y)`，此时 `fn` 也可以称为“单调”。理论上，所有单调函数都支持裁剪。

    目前，TiDB 只支持以下单调函数：

    -   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    -   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)
    -   [`EXTRACT(<时间单位> FROM <DATETIME/DATE/TIME列>)`](/functions-and-operators/date-and-time-functions.md)。对于 `DATE` 和 `DATETIME` 列，`YEAR` 和 `YEAR_MONTH` 时间单位被视为单调函数。对于 `TIME` 列，`HOUR`、`HOUR_MINUTE`、`HOUR_SECOND` 和 `HOUR_MICROSECOND` 被视为单调函数。注意，`WEEK` 不支持作为 `EXTRACT` 的时间单位。

    例如，分区表达式为简单列：

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    或表达式为 `fn(col)`，其中 `fn` 为 `to_days`：

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    例外情况是 `floor(unix_timestamp())` 作为分区表达式。TiDB 会逐个优化此类情况，因此支持裁剪。

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## Partition selection {#partition-selection}

`SELECT` 语句支持分区选择，通过 `PARTITION` 选项实现。

```sql
SET @@sql_mode = '';

CREATE TABLE employees  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(25) NOT NULL,
    store_id INT NOT NULL,
    department_id INT NOT NULL
)

PARTITION BY RANGE(id)  (
    PARTITION p0 VALUES LESS THAN (5),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN (15),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);

INSERT INTO employees VALUES
    ('', 'Bob', 'Taylor', 3, 2), ('', 'Frank', 'Williams', 1, 2),
    ('', 'Ellen', 'Johnson', 3, 4), ('', 'Jim', 'Smith', 2, 4),
    ('', 'Mary', 'Jones', 1, 1), ('', 'Linda', 'Black', 2, 3),
    ('', 'Ed', 'Jones', 2, 1), ('', 'June', 'Wilson', 3, 1),
    ('', 'Andy', 'Smith', 1, 3), ('', 'Lou', 'Waters', 2, 4),
    ('', 'Jill', 'Stone', 1, 4), ('', 'Roger', 'White', 3, 2),
    ('', 'Howard', 'Andrews', 1, 2), ('', 'Fred', 'Goldberg', 3, 3),
    ('', 'Barbara', 'Brown', 2, 3), ('', 'Alice', 'Rogers', 2, 2),
    ('', 'Mark', 'Morgan', 3, 3), ('', 'Karen', 'Cole', 3, 2);
```

可以查看存放在 `p1` 分区的行：

```sql
SELECT * FROM employees PARTITION (p1);
```

    +----|-------|--------|----------|---------------+
    | id | fname | lname  | store_id | department_id |
    +----|-------|--------|----------|---------------+
    |  5 | Mary  | Jones  |        1 |             1 |
    |  6 | Linda | Black  |        2 |             3 |
    |  7 | Ed    | Jones  |        2 |             1 |
    |  8 | June  | Wilson |        3 |             1 |
    |  9 | Andy  | Smith  |        1 |             3 |
    +----|-------|--------|----------|---------------+
    5 rows in set (0.00 sec)

如果想获取多个分区中的行，可以用用逗号分隔的分区名列表。例如，`SELECT * FROM employees PARTITION (p1, p2)` 会返回 `p1` 和 `p2` 分区中的所有行。

使用分区选择时，仍然可以使用 `WHERE` 条件和 `ORDER BY`、`LIMIT` 等选项，也支持 `HAVING` 和 `GROUP BY` 等聚合操作。

```sql
SELECT * FROM employees PARTITION (p0, p2)
    WHERE lname LIKE 'S%';
```

    +----|-------|--------|----------|---------------+
    | id | fname | lname | store_id | department_id |
    +----|-------|--------|----------|---------------+
    |  4 | Jim   | Smith |        2 |             4 |
    | 11 | Jill  | Stone |        1 |             4 |
    +----|-------|--------|----------|---------------+
    2 rows in set (0.00 sec)

```sql
SELECT id, CONCAT(fname, ' ', lname) AS name
    FROM employees PARTITION (p0) ORDER BY lname;
```

    +----|----------------+
    | id | name           |
    +----|----------------+
    |  3 | Ellen Johnson  |
    |  4 | Jim Smith      |
    |  1 | Bob Taylor     |
    |  2 | Frank Williams |
    +----|----------------+
    4 rows in set (0.06 sec)

```sql
SELECT store_id, COUNT(department_id) AS c
    FROM employees PARTITION (p1,p2,p3)
    GROUP BY store_id HAVING c > 4;
```

    +---|----------+
    | c | store_id |
    +---|----------+
    | 5 |        2 |
    | 5 |        3 |
    +---|----------+
    2 rows in set (0.00 sec)

分区选择支持所有类型的表分区，包括 Range 和 Hash。对于 Hash 分区，如果未指定分区名，则会自动使用 `p0`、`p1`、`p2`...或 `pN-1` 作为分区名。

`SELECT` 也可以在 `INSERT ... SELECT` 中使用分区选择。

## 分区限制和注意事项 {#restrictions-and-limitations-on-partitions}

本节介绍 TiDB 中分区表的一些限制和注意事项。

-   不支持用 [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 改变分区表的列类型。
-   不支持用 [`ALTER TABLE ... CACHE`](/cached-tables.md) 设置分区表为缓存表。
-   TiDB 中的 [临时表](/temporary-tables.md) **不**兼容分区表。
-   不支持在分区表上创建 [外键](/foreign-key.md)。
-   [`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) 提示不适用于分区表及其相关索引，因为分区表上的索引不能按顺序读取。

### 分区键、主键和唯一键 {#partitioning-keys-primary-keys-and-unique-keys}

本节讨论分区键与主键和唯一键的关系。其规则如下：分区表上的每个唯一键（包括主键）都必须用到分区表达式中的所有列，因为主键本身也是唯一键。

> **Note:**
>
> 使用 [全局索引](#global-indexes) 时可以忽略此规则。

例如，以下建表语句无效：

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

在每个例子中，至少有一个唯一键未包含所有用于分区的列。

有效的示例如下：

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

以下会报错：

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

    ERROR 8264 (HY000): Global Index is needed for index 'col1', since the unique index is not including all partitioning columns, and GLOBAL is not given as IndexOption

原因是，`col1` 和 `col3` 都在分区表达式中，但都未同时出现在两个唯一键中。修改后，语句变为有效：

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3),
    UNIQUE KEY (col1, col3)
)
PARTITION BY HASH(col1 + col3)
    PARTITIONS 4;
```

以下表无法进行分区，因为没有列能同时出现在两个唯一键中：

```sql
CREATE TABLE t4 (
    col1 INT NOT NULL,
    col2 INT NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3),
    UNIQUE KEY (col2, col4)
);
```

因为每个主键本身就是唯一键，所以下述两条语句无效：

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col3),
    UNIQUE KEY(col2)
)

PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

原因是，主键未包含所有分区表达式中的列。补充缺失列后，语句变为有效：

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3),
    UNIQUE KEY(col2)
)
PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

如果表没有唯一键或主键，则此限制不适用。

在用 DDL 改表时，也要考虑此限制。例如，创建如下分区表：

```sql
CREATE TABLE t_no_pk (c1 INT, c2 INT)
    PARTITION BY RANGE(c1) (
        PARTITION p0 VALUES LESS THAN (10),
        PARTITION p1 VALUES LESS THAN (20),
        PARTITION p2 VALUES LESS THAN (30),
        PARTITION p3 VALUES LESS THAN (40)
    );
```

    Query OK, 0 rows affected (0.12 sec)

可以用 `ALTER TABLE` 添加非唯一索引，但若要添加唯一索引，索引列必须包含所有分区列。

在分区表中，不能定义前缀索引作为唯一索引，例如：

```sql
CREATE TABLE t (a varchar(20), b blob,
    UNIQUE INDEX (a(5)))
    PARTITION by range columns (a) (
    PARTITION p0 values less than ('aaaaa'),
    PARTITION p1 values less than ('bbbbb'),
    PARTITION p2 values less than ('ccccc'));
```

```sql
ERROR 8264 (HY000): Global Index is needed for index 'a', since the unique index is not including all partitioning columns, and GLOBAL is not given as IndexOption
```

#### 全局索引 {#global-indexes}

在引入全局索引之前，TiDB 为每个分区创建本地索引，导致 [限制](#partitioning-keys-primary-keys-and-unique-keys)：主键和唯一键必须包含分区键，以保证数据唯一性。此外，跨分区查询时，TiDB 需要扫描每个分区的索引数据。

为解决这些问题，TiDB 在 v8.3.0 引入全局索引。全局索引覆盖整个表的数据，只需一个索引即可保证主键和唯一键的全局唯一性，也可以跨多个分区访问索引数据，极大提升非分区键的查询性能，而不用逐个分区查找。

创建主键或唯一键的全局索引时，在索引定义中加 `GLOBAL` 关键字。

> **Note:**
>
> 全局索引会影响分区管理。`DROP`、`TRUNCATE` 和 `REORGANIZE PARTITION` 操作也会触发全局索引的更新，操作完成后才会返回结果，增加了执行时间。这在数据归档场景（如 `DROP PARTITION` 和 `TRUNCATE PARTITION`）尤为明显。没有全局索引时，这些操作通常可以立即完成，但有全局索引后，随着索引数量的增加，耗时也会增加。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

在上述例子中，`uidx12` 是全局索引，`uidx3` 是普通唯一索引。

注意，**聚簇索引**不能是全局索引，如示例：

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

    ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function

原因是，如果聚簇索引为全局索引，表就不再是分区的。因为索引的键也是分区层级的记录键，但全局索引是表级的，会冲突。如果要将主键设为全局索引，必须显式定义为非聚簇索引，例如 `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。

可以通过 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 输出中的 `GLOBAL` 索引选项识别全局索引。

```sql
SHOW CREATE TABLE t1\G
```

           Table: t1
    Create Table: CREATE TABLE `t1` (
      `col1` int NOT NULL,
      `col2` date NOT NULL,
      `col3` int NOT NULL,
      `col4` int NOT NULL,
      UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
      UNIQUE KEY `uidx3` (`col3`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    PARTITION BY HASH (`col3`) PARTITIONS 4
    1 row in set (0.00 sec)

或者查询 [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)，查看 `IS_GLOBAL` 列。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE table_name='t1';
```

    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    | TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    | test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
    | test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
    | test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
    +--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
    3 rows in set (0.00 sec)

在对非分区表或已分区表重新分区时，可以根据需要更新索引为全局索引或恢复为本地索引：

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL);
```

##### 全局索引的限制 {#limitations-of-global-indexes}

-   如果索引定义中未显式加 `GLOBAL`，则 TiDB 默认为本地索引。

-   `GLOBAL` 和 `LOCAL` 关键字仅适用于分区表，不影响非分区表。换句话说，非分区表中，全局索引和本地索引没有区别。

-   目前，TiDB 只支持在唯一列上创建唯一全局索引。如果要在非唯一列上创建全局索引，可以在索引中包含主键，形成复合索引。例如，非唯一列为 `col3`，主键为 `col1`，可以用如下语句创建全局索引：

    ```sql
    ALTER TABLE ... ADD UNIQUE INDEX(col3, col1) GLOBAL;
    ```

-   `DROP PARTITION`、`TRUNCATE PARTITION` 和 `REORGANIZE PARTITION` 等 DDL 操作也会触发全局索引的更新。这些操作需要等待全局索引更新完成后才返回，增加了执行时间。尤其在数据归档场景（如 `DROP PARTITION` 和 `TRUNCATE PARTITION`）中更明显。没有全局索引时，这些操作通常可以立即完成，但有全局索引后，随着索引数量的增加，耗时也会增加。

-   带有全局索引的表不支持 `EXCHANGE PARTITION`。

-   默认情况下，分区表的主键为聚簇索引，必须包含分区键。如果希望主键不包含分区键，可以在建表时显式定义为非聚簇索引，例如 `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。

-   如果在表达式列上添加了全局索引，或全局索引也是前缀索引（如 `UNIQUE KEY idx_id_prefix (id(10)) GLOBAL`），需要手动收集此全局索引的统计信息。

### 与函数相关的分区限制 {#partitioning-limitations-relating-to-functions}

只允许在分区表达式中使用以下列出的函数：

    ABS()
    CEILING()
    DATEDIFF()
    DAY()
    DAYOFMONTH()
    DAYOFWEEK()
    DAYOFYEAR()
    EXTRACT() (详见 EXTRACT() 函数与 WEEK 说明)
    FLOOR()
    HOUR()
    MICROSECOND()
    MINUTE()
    MOD()
    MONTH()
    QUARTER()
    SECOND()
    TIME_TO_SEC()
    TO_DAYS()
    TO_SECONDS()
    UNIX_TIMESTAMP() (用于 TIMESTAMP 列)
    WEEKDAY()
    YEAR()
    YEARWEEK()

### 与 MySQL 的兼容性 {#compatibility-with-mysql}

目前，TiDB 支持 Range 分区、Range COLUMNS 分区、List 分区、List COLUMNS 分区、Hash 分区和 Key 分区。MySQL 中的其他分区类型暂不支持。

对于不支持的分区类型，在 TiDB 中创建表时，分区信息会被忽略，表以普通表形式创建，并报告警告。

目前，TiDB 不支持 `LOAD DATA` 语法中的分区选择。

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

支持普通的 `LOAD DATA` 操作：

```sql
load local data infile "xxx" into t ...
```

但不支持 `Load Data` 的分区选择：

```sql
load local data infile "xxx" into t partition (p1)...
```

对于分区表，`select * from t` 返回的结果在分区之间无序。这与 MySQL 不同，MySQL 在分区之间有序，但分区内部无序。

```sql
create table t (id int, val int) partition by range (id) (
    partition p0 values less than (3),
    partition p1 values less than (7),
    partition p2 values less than (11));
```

    Query OK, 0 rows affected (0.10 sec)

```sql
insert into t values (1, 2), (3, 4),(5, 6),(7,8),(9,10);
```

    Query OK, 5 rows affected (0.01 sec)
    Records: 5  Duplicates: 0  Warnings: 0

TiDB 每次返回的结果都不同，例如：

```sql
select * from t;
```

    +------|------+
    | id   | val  |
    +------|------+
    |    7 |    8 |
    |    9 |   10 |
    |    1 |    2 |
    |    3 |    4 |
    |    5 |    6 |
    +------|------+
    5 rows in set (0.00 sec)

MySQL 返回的结果：

```sql
select * from t;
```

    +------|------+
    | id   | val  |
    +------|------+
    |    1 |    2 |
    |    3 |    4 |
    |    5 |    6 |
    |    7 |    8 |
    |    9 |   10 |
    +------|------+
    5 rows in set (0.00 sec)

### 动态裁剪模式 {#dynamic-pruning-mode}

TiDB 以 `dynamic` 或 `static` 模式访问分区表。自 v6.3.0 起，默认使用 `dynamic` 模式。但动态分区只有在收集到完整的表级统计信息或全局统计信息后才有效。如果在全局统计信息收集完成前启用 `dynamic` 裁剪模式，TiDB 会保持在 `static` 模式，直到统计信息收集完毕。详见 [Collect statistics of partitioned tables in dynamic pruning mode](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手动 `ANALYZE` 和普通查询使用会话级的 `tidb_partition_prune_mode` 设置。后台的 `auto-analyze` 使用全局设置。

在 `static` 模式下，分区表使用分区级统计信息。在 `dynamic` 模式下，使用表级全局统计信息。

切换到 `dynamic` 模式后，需要手动检查和收集统计信息。因为切换后，分区表只有分区级统计信息，没有表级统计信息。全局统计信息只在下一次 `auto-analyze` 时收集。

```sql
set session tidb_partition_prune_mode = 'dynamic';
show stats_meta where table_name like "t";
```

    +---------+------------+----------------+---------------------+--------------+-----------+
    | Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
    +---------+------------+----------------+---------------------+--------------+-----------+
    | test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
    | test    | t          | p1             | 2022-05-27 20:23:34 |            2 |         4 |
    | test    | t          | p2             | 2022-05-27 20:23:34 |            2 |         4 |
    +---------+------------+----------------+---------------------+--------------+-----------+
    3 rows in set (0.01 sec)

为了确保启用全局 `dynamic` 裁剪后 SQL 使用的统计信息正确，可以手动触发 `analyze`，对表或分区进行统计信息收集。

```sql
analyze table t partition p1;
show stats_meta where table_name like "t";
```

    +---------+------------+----------------+---------------------+--------------+-----------+
    | Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
    +---------+------------+----------------+---------------------+--------------+-----------+
    | test    | t          | global         | 2022-05-27 20:50:53 |            0 |         5 |
    | test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
    | test    | t          | p1             | 2022-05-27 20:50:52 |            0 |         2 |
    | test    | t          | p2             | 2022-05-27 20:50:08 |            0 |         2 |
    +---------+------------+----------------+---------------------+--------------+-----------+
    4 rows in set (0.00 sec)

如果在 `analyze` 过程中出现以下警告，说明分区统计信息不一致，需要重新收集分区或整个表的统计信息。

    | Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions

你也可以用脚本批量更新所有分区表的统计信息。详见 [Update statistics of partitioned tables in dynamic pruning mode](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

表级统计信息准备好后，可以启用全局动态裁剪模式，影响所有 SQL 语句和 `auto-analyze` 操作。

```sql
set global tidb_partition_prune_mode = dynamic
```

在 `static` 模式下，TiDB 使用多个操作符逐个访问每个分区，然后用 `Union` 合并结果。示例如下，这是一个简单的读取操作，TiDB 通过 `Union` 合并两个分区的结果：

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id)
    (partition p0 values less than (100),
     partition p1 values less than (200),
     partition p2 values less than (300),
     partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
```

    +------------------------------+----------+-----------+------------------------+--------------------------------+
    | id                           | estRows  | task      | access object          | operator info                  |
    +------------------------------+----------+-----------+------------------------+--------------------------------+
    | PartitionUnion_9             | 6646.67  | root      |                        |                                |
    | ├─TableReader_12             | 3323.33  | root      |                        | data:Selection_11              |
    | │ └─Selection_11             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
    | │   └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo |
    | └─TableReader_18             | 3323.33  | root      |                        | data:Selection_17              |
    |   └─Selection_17             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
    |     └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo |
    +------------------------------+----------+-----------+------------------------+--------------------------------+
    7 rows in set (0.00 sec)

在 `dynamic` 模式下，每个操作符支持直接访问多个分区，因此不再使用 `Union`。

```sql
mysql> set @@session.tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select * from t1 where id < 150;
+-------------------------+----------+-----------+-----------------+--------------------------------+
| id                      | estRows  | task      | access object   | operator info                  |
+-------------------------+----------+-----------+-----------------+--------------------------------+
| TableReader_7           | 3323.33  | root      | partition:p0,p1 | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |                 | lt(test.t1.id, 150)            |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1        | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------+--------------------------------+
3 rows in set (0.00 sec)
```

从上面结果可以看到，执行计划中的 `Union` 操作符消失了，裁剪仍然生效，且只访问了 `p0` 和 `p1`。

`dynamic` 模式使执行计划更简洁明了。省略 `Union` 可以提升执行效率，避免 `Union` 并发执行的问题。此外，`dynamic` 模式还支持带有 IndexJoin 的执行计划，而在 `static` 模式下不能使用（详见示例）。

**示例 1**：以下示例在 `static` 模式下，使用带 IndexJoin 的执行计划执行查询：

```sql
mysql> create table t1 (id int, age int, key(id)) partition by range(id)
    (partition p0 values less than (100),
     partition p1 values less than (200),
     partition p2 values less than (300),
     partition p3 values less than (400));
Query OK, 0 rows affected (0,08 sec)

mysql> create table t2 (id int, code int);
Query OK, 0 rows affected (0.01 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                             | estRows  | task      | access object          | operator info                                  |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_13                    | 12.49    | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─TableReader_42(Build)        | 9.99     | root      |                        | data:Selection_41                              |
| │ └─Selection_41               | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))   |
| │   └─TableFullScan_40         | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                 |
| └─PartitionUnion_15(Probe)     | 39960.00 | root      |                        |                                                |
|   ├─TableReader_18             | 9990.00  | root      |                        | data:Selection_17                              |
|   │ └─Selection_17             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                 |
|   ├─TableReader_24             | 9990.00  | root      |                        | data:Selection_23                              |
|   │ └─Selection_23             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_22       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                 |
|   ├─TableReader_30             | 9990.00  | root      |                        | data:Selection_29                              |
|   │ └─Selection_29             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_28       | 10000.00 | cop[tikv] | table:t1, partition:p2 | keep order:false, stats:pseudo                 |
|   └─TableReader_36             | 9990.00  | root      |                        | data:Selection_35                              |
|     └─Selection_35             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|       └─TableFullScan_34       | 10000.00 | cop[tikv] | table:t1, partition:p3 | keep order:false, stats:pseudo                 |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
17 rows in set, 1 warning (0.00 sec)

mysql> show warnings;
+---------+------+------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                            |
+---------+------+------------------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1, t2) */ or /*+ TIDB_INLJ(t1, t2) */ is inapplicable |
+---------+------+------------------------------------------------------------------------------------+
1 row in set (0,00 sec)
```

从示例 1 可以看到，即使使用了 `TIDB_INLJ` 提示，分区表的执行计划也不能选择 IndexJoin。

**示例 2**：以下示例在 `dynamic` 模式下，使用带 IndexJoin 的执行计划：

```sql
mysql> set @@tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object          | operator info                                                                                                       |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| IndexJoin_11                    | 12.49    | root      |                        | inner join, inner:IndexLookUp_10, outer key:test.t2.id, inner key:test.t1.id, equal cond:eq(test.t2.id, test.t1.id) |
| ├─TableReader_16(Build)         | 9.99     | root      |                        | data:Selection_15                                                                                                   |
| │ └─Selection_15                | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))                                                                        |
| │   └─TableFullScan_14          | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                                                      |
| └─IndexLookUp_10(Probe)         | 12.49    | root      | partition:all          |                                                                                                                     |
|   ├─Selection_9(Build)          | 12.49    | cop[tikv] |                        | not(isnull(test.t1.id))                                                                                             |
|   │ └─IndexRangeScan_7          | 12.50    | cop[tikv] | table:t1, index:id(id) | range: decided by [eq(test.t1.id, test.t2.id)], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_8(Probe)     | 12.49    | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                                                      |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

可以看到，在 `dynamic` 模式下，执行计划中支持 IndexJoin。

目前，`static` 裁剪模式不支持预处理语句和非预处理语句的计划缓存。

#### 在动态裁剪模式下更新分区表的统计信息 {#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

1.  找出所有分区表：

    ```sql
    SELECT DISTINCT CONCAT(TABLE_SCHEMA,'.', TABLE_NAME)
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA', 'mysql', 'sys', 'PERFORMANCE_SCHEMA', 'METRICS_SCHEMA');
    ```

        +-------------------------------------+
        | concat(TABLE_SCHEMA,'.',TABLE_NAME) |
        +-------------------------------------+
        | test.t                              |
        +-------------------------------------+
        1 row in set (0.02 sec)

2.  生成所有分区表的统计信息更新语句：

    ```sql
    SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;')
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    ```

        +----------------------------------------------------------------------+
        | concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') |
        +----------------------------------------------------------------------+
        | ANALYZE TABLE test.t ALL COLUMNS;                                    |
        +----------------------------------------------------------------------+
        1 row in set (0.01 sec)

    可以将 `ALL COLUMNS` 改为需要的列。

3.  导出批量更新语句到文件：

    ```shell
    mysql --host xxxx --port xxxx -u root -p -e "SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        FROM information_schema.PARTITIONS \
        WHERE TIDB_PARTITION_ID IS NOT NULL \
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4.  执行批量更新：

    在执行 `source` 前处理 SQL 语句：

        sed -i "" '1d' gatherGlobalStats.sql --- mac
        sed -i '1d' gatherGlobalStats.sql --- linux

    ```sql
    SET session tidb_partition_prune_mode = 'dynamic';
    source gatherGlobalStats.sql
    ```
