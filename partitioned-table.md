---
title: 分区
summary: 了解如何在 TiDB 中使用分区。
---

# 分区

本文档介绍了 TiDB 的分区实现。

## 分区类型

本节介绍 TiDB 支持的分区类型。目前，TiDB 支持 [范围分区](#range-partitioning)、[范围 COLUMNS 分区](#range-columns-partitioning)、[列表分区](#list-partitioning)、[列表 COLUMNS 分区](#list-columns-partitioning)、[哈希分区](#hash-partitioning) 和 [键分区](#key-partitioning)。

- 范围分区、范围 COLUMNS 分区、列表分区和列表 COLUMNS 分区主要用于解决应用中大量删除带来的性能问题，并支持快速删除分区。
- 哈希分区和键分区主要用于写入量较大的场景下的数据分布。与哈希分区相比，键分区支持多列分布和非整型列分区。

### 范围分区

当表按范围分区时，每个分区包含分区表达式值位于给定范围内的行。各个范围必须是连续的且不重叠。你可以使用 `VALUES LESS THAN` 进行定义。

假设你需要创建一个包含人员记录的表，如下所示：

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

你可以根据需要以多种方式对表进行范围分区。例如，可以按 `store_id` 列进行分区：

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

在该分区方案中，`store_id` 为 1 到 5 的员工数据存储在 `p0` 分区，`store_id` 为 6 到 10 的员工数据存储在 `p1` 分区。范围分区要求分区按从小到大的顺序排列。

如果你插入一条数据 `(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`，它会落在 `p2` 分区。但如果插入的记录 `store_id` 大于 20，则会报错，因为 TiDB 无法确定该记录应插入哪个分区。此时，你可以在建表时使用 `MAXVALUE`：

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

`MAXVALUE` 表示比所有其他整数值都大的整数值。现在，所有 `store_id` 大于等于 16（定义的最大值）的记录都存储在 `p3` 分区。

你还可以按员工的职位代码（`job_code` 列的值）进行分区。假设两位数的职位代码代表普通员工，三位数代表办公室和客服人员，四位数代表管理人员。你可以这样创建分区表：

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

在此示例中，所有普通员工的数据存储在 `p0` 分区，办公室和客服人员在 `p1` 分区，管理人员在 `p2` 分区。

除了按 `store_id` 列分区外，你还可以按日期分区。例如，可以按员工离职年份分区：

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

在范围分区中，你可以基于 `timestamp` 列的值进行分区，并使用 `unix_timestamp()` 函数，例如：

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

不允许使用包含 timestamp 列的其他分区表达式。

当满足以下一个或多个条件时，范围分区特别有用：

* 你希望删除旧数据。例如，使用前述的 `employees` 表，可以通过 `ALTER TABLE employees DROP PARTITION p0;` 快速删除 1991 年前离职员工的所有记录。这比执行 `DELETE FROM employees WHERE YEAR(separated) <= 1990;` 更快。
* 你希望使用包含时间或日期值的列，或包含其他序列值的列。
* 你需要频繁在分区列上进行查询。例如，执行 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;` 时，TiDB 能快速判断只需扫描 `p2` 分区的数据，因为其他分区不满足 `WHERE` 条件。

### 范围 COLUMNS 分区

范围 COLUMNS 分区是范围分区的一个变体。你可以使用一个或多个列作为分区键。分区列的数据类型可以是整数、字符串（`CHAR` 或 `VARCHAR`）、`DATE` 和 `DATETIME`。不支持任何表达式（如非 COLUMNS 分区）。

与范围分区类似，范围 COLUMNS 分区也要求分区范围严格递增。如下示例中的分区定义是不被支持的：

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

```
Error 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition
```

假设你希望按姓名分区，并删除过期和无效数据，可以创建如下表：

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

上述 SQL 语句会按年份和姓名范围将数据分区为 `[ ('', ''), ('G', '2023-01-01 00:00:00') )`、`[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )`、`[ ('G', '2024-01-01 00:00:00'), ('M', '2023-01-01 00:00:00') )`、`[ ('M', '2023-01-01 00:00:00'), ('M', '2024-01-01 00:00:00') )`、`[ ('M', '2024-01-01 00:00:00'), ('S', '2023-01-01 00:00:00') )` 和 `[ ('S', '2023-01-01 00:00:00'), ('S', '2024-01-01 00:00:00') )`。这样你可以方便地删除无效数据，同时在 `name` 和 `valid_until` 列上都能受益于分区裁剪。此示例中，`[,)` 表示左闭右开区间。例如，`[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 表示姓名为 `'G'`，年份包含 `2023-01-01 00:00:00`，且大于 `2023-01-01 00:00:00` 但小于 `2024-01-01 00:00:00` 的数据范围。不包含 `(G, 2024-01-01 00:00:00)`。

### 范围 INTERVAL 分区

范围 INTERVAL 分区是范围分区的扩展，允许你轻松地按指定间隔创建分区。从 v6.3.0 开始，TiDB 引入了 INTERVAL 分区作为语法糖。

语法如下：

```sql
PARTITION BY RANGE [COLUMNS] (<partitioning expression>)
INTERVAL (<interval expression>)
FIRST PARTITION LESS THAN (<expression>)
LAST PARTITION LESS THAN (<expression>)
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

范围 INTERVAL 分区同样适用于 [范围 COLUMNS](#range-columns-partitioning) 分区。

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

它会创建如下表：

```
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
```

可选参数 `NULL PARTITION` 会创建一个定义为 `PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)` 的分区，仅当分区表达式计算结果为 `NULL` 时匹配。参见 [范围分区下 NULL 的处理](#handling-of-null-with-range-partitioning)，其中说明了 `NULL` 被认为小于任何其他值。

可选参数 `MAXVALUE PARTITION` 会创建最后一个分区，定义为 `PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`。

#### ALTER INTERVAL 分区表

INTERVAL 分区还增加了更简单的添加和删除分区语法。

以下语句更改第一个分区。它会删除所有小于给定表达式的分区，并将匹配的分区作为新的第一个分区。不影响 NULL PARTITION。

```
ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)
```

以下语句更改最后一个分区，即为新数据添加更高范围的分区。它会按当前 INTERVAL 添加新分区，直到包含给定表达式。不支持已存在 `MAXVALUE PARTITION` 的情况，因为这需要数据重组。

```
ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)
```

#### INTERVAL 分区细节与限制

- INTERVAL 分区特性仅涉及 `CREATE/ALTER TABLE` 语法。元数据无变化，因此用新语法创建或修改的表仍兼容 MySQL。
- `SHOW CREATE TABLE` 的输出格式无变化，以保持 MySQL 兼容性。
- 新的 `ALTER` 语法适用于符合 INTERVAL 的现有表。你无需用 `INTERVAL` 语法创建这些表。
- 对于 `RANGE COLUMNS` 分区，使用 `INTERVAL` 语法时，只能指定单个 `INTEGER`、`DATE` 或 `DATETIME` 类型的列作为分区键。

### 列表分区

列表分区与范围分区类似。不同的是，列表分区中，每个分区的分区表达式值属于给定的值集合。每个分区定义的值集合可以有任意数量的值，但不能有重复值。你可以使用 `PARTITION ... VALUES IN (...)` 子句定义值集合。

假设你要创建一个人员记录表，可以如下创建：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

假设有 20 家门店分布在 4 个区域，如下表所示：

```
| Region  | Store ID Numbers     |
| ------- | -------------------- |
| North   | 1, 2, 3, 4, 5        |
| East    | 6, 7, 8, 9, 10       |
| West    | 11, 12, 13, 14, 15   |
| Central | 16, 17, 18, 19, 20   |
```

如果你希望将同一区域的员工数据存储在同一个分区，可以基于 `store_id` 创建列表分区表：

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

如上创建分区后，你可以方便地添加或删除与特定区域相关的记录。例如，假设 East 区域的所有门店被出售给另一家公司，则可以通过执行 `ALTER TABLE employees TRUNCATE PARTITION pEast` 删除该区域所有员工的行数据，这比等价的 `DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)` 语句效率更高。

你也可以执行 `ALTER TABLE employees DROP PARTITION pEast` 删除所有相关行，但该语句还会将 `pEast` 分区从表定义中删除。在这种情况下，你需要执行 `ALTER TABLE ... ADD PARTITION` 语句恢复表的原分区方案。

#### 默认列表分区

从 v7.3.0 开始，你可以为列表分区或列表 COLUMNS 分区表添加默认分区。默认分区作为兜底分区，未匹配到任何分区值集合的行会被放入该分区。

> **注意：**
>
> 该功能是 TiDB 对 MySQL 语法的扩展。对于带有默认分区的列表分区或列表 COLUMNS 分区表，表中的数据无法直接同步到 MySQL。

以如下列表分区表为例：

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

你可以如下为表添加名为 `pDef` 的默认列表分区：

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef DEFAULT);
```

或

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef VALUES IN (DEFAULT));
```

这样，插入的新值如果未匹配到任何分区的值集合，会自动进入默认分区。

```sql
INSERT INTO t VALUES (7, 7);
Query OK, 1 row affected (0.01 sec)
```

你也可以在创建列表分区或列表 COLUMNS 分区表时添加默认分区。例如：

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

对于没有默认分区的列表分区或列表 COLUMNS 分区表，使用 `INSERT` 语句插入的值必须匹配表中 `PARTITION ... VALUES IN (...)` 子句定义的值集合。如果插入的值未匹配到任何分区的值集合，则语句会失败并返回错误，如下所示：

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

要忽略上述错误，可以在 `INSERT` 语句中添加 `IGNORE` 关键字。添加后，`INSERT` 语句只会插入匹配分区值集合的行，不会插入未匹配的行，也不会返回错误：

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

### 列表 COLUMNS 分区

列表 COLUMNS 分区是列表分区的一个变体。你可以使用多列作为分区键。除了整数类型外，还可以使用字符串、`DATE` 和 `DATETIME` 类型的列作为分区列。

假设你要将以下 12 个城市的门店员工分为 4 个区域，如下表所示：

```
| Region | Cities                         |
| :----- | ------------------------------ |
| 1      | LosAngeles,Seattle, Houston    |
| 2      | Chicago, Columbus, Boston      |
| 3      | NewYork, LongIsland, Baltimore |
| 4      | Atlanta, Raleigh, Cincinnati   |
```

你可以使用列表 COLUMNS 分区创建表，并将每行数据存储在对应员工城市的分区中，如下所示：

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

与列表分区不同，列表 COLUMNS 分区无需在 `COLUMNS()` 子句中将列值转换为整数。

列表 COLUMNS 分区还可以使用 `DATE` 和 `DATETIME` 类型的列实现，如下例所示。该示例与前述 `employees_1` 表使用相同的列名和列，但基于 `hired` 列进行列表 COLUMNS 分区：

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

此外，你还可以在 `COLUMNS()` 子句中添加多列。例如：

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

### 哈希分区

哈希分区用于确保数据均匀分布到指定数量的分区中。使用范围分区时，你需要为每个分区指定列值的范围，而使用哈希分区时，只需指定分区数量。

要创建哈希分区表，需要在 `CREATE TABLE` 语句后添加 `PARTITION BY HASH (expr)` 子句。`expr` 是返回整数的表达式，可以是整型列名。此外，你还可以添加 `PARTITIONS num`，其中 `num` 是正整数，表示表被分为多少个分区。

以下操作创建了一个按 `store_id` 分为 4 个分区的哈希分区表：

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

如果未指定 `PARTITIONS num`，则默认分区数为 1。

你也可以为 `expr` 使用返回整数的 SQL 表达式。例如，可以按入职年份分区：

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

最高效的哈希函数是作用于单个表列，且其值随列值一致递增或递减的函数。

例如，`date_col` 是 `DATE` 类型的列，`TO_DAYS(date_col)` 表达式的值随 `date_col` 变化而变化。`YEAR(date_col)` 与 `TO_DAYS(date_col)` 不同，因为并非 `date_col` 的每一次变化都会导致 `YEAR(date_col)` 变化。

相反，假设你有一个 `int_col` 列，类型为 `INT`。考虑表达式 `POW(5-int_col,3) + 6`，它不是一个好的哈希函数，因为 `int_col` 的变化不会导致表达式结果成比例变化。例如，`int_col` 从 5 变为 6，表达式结果变化为 -1；但从 6 变为 7，结果变化可能为 -7。

总之，表达式越接近 `y = cx` 形式，越适合作为哈希函数。因为表达式越非线性，数据在各分区间分布越不均匀。

理论上，涉及多个列值的表达式也可以用于分区裁剪，但判断哪些表达式适合会非常困难且耗时。因此，不推荐使用涉及多列的哈希表达式。

使用 `PARTITION BY HASH` 时，TiDB 根据表达式结果的模数决定数据应落在哪个分区。即，如果分区表达式为 `expr`，分区数为 `num`，则 `MOD(expr, num)` 决定数据存储的分区。假设 `t1` 定义如下：

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

当你向 `t1` 插入一行数据，`col3` 的值为 '2005-09-15'，则该行会插入到分区 1：

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

### 键分区

从 v7.0.0 开始，TiDB 支持键分区。在 v7.0.0 之前的 TiDB 版本中，如果你尝试创建键分区表，TiDB 会将其作为非分区表创建并返回警告。

键分区和哈希分区都可以将数据均匀分布到指定数量的分区。不同之处在于，哈希分区只支持基于指定的整型表达式或整型列分布数据，而键分区支持基于列列表分布数据，且分区列不限于整型。TiDB 的键分区哈希算法与 MySQL 不同，因此表数据分布也不同。

要创建键分区表，需要在 `CREATE TABLE` 语句后添加 `PARTITION BY KEY (columnList)` 子句。`columnList` 是包含一个或多个列名的列列表，列表中每个列的数据类型可以是除 `BLOB`、`JSON` 和 `GEOMETRY`（注意 TiDB 不支持 `GEOMETRY`）以外的任意类型。此外，你还可以添加 `PARTITIONS num`（`num` 为正整数，表示表被分为多少个分区），或添加分区名称定义。例如，添加 `(PARTITION p0, PARTITION p1)` 表示将表分为两个名为 `p0` 和 `p1` 的分区。

以下操作创建了一个按 `store_id` 分为 4 个分区的键分区表：

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

如果未指定 `PARTITIONS num`，则默认分区数为 1。

你还可以基于非整型列（如 VARCHAR）创建键分区表。例如，可以按 `fname` 列分区：

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

你还可以基于多列创建键分区表。例如，可以按 `fname` 和 `store_id` 将表分为 4 个分区：

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

与 MySQL 类似，TiDB 支持在 `PARTITION BY KEY` 中指定空分区列列表创建键分区表。例如，以下语句使用主键 `id` 作为分区键创建分区表：

```sql
CREATE TABLE employees (
    id INT NOT NULL PRIMARY KEY,
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

如果表没有主键但包含唯一键，则唯一键会被用作分区键：

```sql
CREATE TABLE k1 (
    id INT NOT NULL,
    name VARCHAR(20),
    UNIQUE KEY (id)
)
PARTITION BY KEY()
PARTITIONS 2;
```

但如果唯一键列未定义为 `NOT NULL`，上述语句会失败。

#### TiDB 如何处理线性哈希分区

v6.4.0 之前，在 TiDB 中执行 [MySQL 线性哈希](https://dev.mysql.com/doc/refman/8.0/en/partitioning-linear-hash.html) 分区的 DDL 语句时，TiDB 只能创建非分区表。如果你仍希望在 TiDB 中使用分区表，需要修改 DDL 语句。

自 v6.4.0 起，TiDB 支持解析 MySQL 的 `PARTITION BY LINEAR HASH` 语法，但会忽略其中的 `LINEAR` 关键字。如果你有 MySQL 线性哈希分区的现有 DDL 和 DML 语句，可以直接在 TiDB 中执行，无需修改：

- 对于 MySQL 线性哈希分区的 `CREATE` 语句，TiDB 会创建非线性哈希分区表（注意 TiDB 没有线性哈希分区表）。如果分区数为 2 的幂，TiDB 哈希分区表中的行分布与 MySQL 线性哈希分区表相同。否则，TiDB 中这些行的分布与 MySQL 不同。这是因为非线性分区表使用简单的“分区数取模”，而线性分区表使用“下一个 2 的幂取模，并将分区数与下一个 2 的幂之间的值折叠”。详情参见 [#38450](https://github.com/pingcap/tidb/issues/38450)。

- 对于 MySQL 线性哈希分区的其他所有语句，除非分区数不是 2 的幂导致行分布不同（会影响 [分区选择](#partition-selection)、`TRUNCATE PARTITION` 和 `EXCHANGE PARTITION`），其余在 TiDB 中的行为与 MySQL 相同。

### TiDB 如何处理线性键分区

从 v7.0.0 开始，TiDB 支持解析 MySQL 的 `PARTITION BY LINEAR KEY` 语法用于键分区。但 TiDB 会忽略 `LINEAR` 关键字，使用非线性哈希算法。

v7.0.0 之前，如果你尝试创建键分区表，TiDB 会将其作为非分区表创建并返回警告。

### TiDB 分区对 NULL 的处理

TiDB 允许分区表达式的计算结果为 `NULL`。

> **注意：**
>
> `NULL` 不是整数。TiDB 的分区实现将 `NULL` 视为小于任何其他整数值，就像 `ORDER BY` 一样。

#### 范围分区下 NULL 的处理

当你向按范围分区的表插入一行数据，且用于分区的列值为 `NULL` 时，该行会插入到最小的分区。

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

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
select * from t1 partition(p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
+------|--------+
1 row in set (0.00 sec)
```

```sql
select * from t1 partition(p1);
```

```
Empty set (0.00 sec)
```

```sql
select * from t1 partition(p2);
```

```
Empty set (0.00 sec)
```

删除 `p0` 分区并验证结果：

```sql
alter table t1 drop partition p0;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
select * from t1;
```

```
Empty set (0.00 sec)
```

#### 哈希分区下 NULL 的处理

哈希分区表对 `NULL` 的处理方式不同——如果分区表达式的计算结果为 `NULL`，则视为 `0`。

```sql
CREATE TABLE th (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY HASH(c1)
PARTITIONS 2;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
```

```
Query OK, 2 rows affected (0.04 sec)
```

```sql
select * from th partition (p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
|    0 | gigan  |
+------|--------+
2 rows in set (0.00 sec)
```

```sql
select * from th partition (p1);
```

```
Empty set (0.00 sec)
```

你可以看到插入的记录 `(NULL, 'mothra')` 与 `(0, 'gigan')` 落在同一分区。

> **注意：**
>
> TiDB 中哈希分区对 `NULL` 的处理方式与 [MySQL 分区对 NULL 的处理](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html) 描述一致，但与 MySQL 实际行为不一致。换句话说，MySQL 在此场景下的实现与其文档描述不一致。
>
> 在此场景下，TiDB 的实际行为与本文档描述一致。

#### 键分区下 NULL 的处理

对于键分区，`NULL` 的处理方式与哈希分区一致。如果分区字段的值为 `NULL`，则视为 `0`。

## 分区管理

对于 `RANGE`、`RANGE COLUMNS`、`LIST` 和 `LIST COLUMNS` 分区表，你可以按如下方式管理分区：

- 使用 `ALTER TABLE <table name> ADD PARTITION (<partition specification>)` 语句添加分区。
- 使用 `ALTER TABLE <table name> DROP PARTITION <list of partitions>` 语句删除分区。
- 使用 `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>` 语句清空指定分区的数据。`TRUNCATE PARTITION` 的逻辑类似于 [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)，但作用于分区。
- 使用 `ALTER TABLE <table name> REORGANIZE PARTITION <list of partitions> INTO (<new partition definitions>)` 语句合并、拆分或修改分区。

对于 `HASH` 和 `KEY` 分区表，你可以按如下方式管理分区：

- 使用 `ALTER TABLE <table name> COALESCE PARTITION <number of partitions to decrease by>` 语句减少分区数。该操作会在线将整个表复制到新的分区数。
- 使用 `ALTER TABLE <table name> ADD PARTITION <number of partitions to increase by | (additional partition definitions)>` 语句增加分区数。该操作会在线将整个表复制到新的分区数。
- 使用 `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>` 语句清空指定分区的数据。`TRUNCATE PARTITION` 的逻辑类似于 [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)，但作用于分区。

`EXCHANGE PARTITION` 通过交换分区和非分区表实现，类似于 `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2` 的表重命名。

例如，`ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` 会交换 `partitioned_table` 表的 `p1` 分区与 `non_partitioned_table` 表。

确保你要交换到分区中的所有行都符合分区定义，否则语句会失败。

注意，TiDB 有一些特性可能影响 `EXCHANGE PARTITION`。当表结构包含这些特性时，你需要确保 `EXCHANGE PARTITION` 满足 [MySQL 的 EXCHANGE PARTITION 条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)。同时，确保这些特性在分区表和非分区表中定义一致。这些特性包括：

<CustomContent platform="tidb">

* [SQL 中的放置规则](/placement-rules-in-sql.md)：放置策略需一致。

</CustomContent>

* [TiFlash](/tikv-overview.md)：TiFlash 副本数需一致。
* [聚簇索引](/clustered-indexes.md)：分区表和非分区表都为 `CLUSTERED`，或都为 `NONCLUSTERED`。

此外，`EXCHANGE PARTITION` 与其他组件的兼容性有限制。分区表和非分区表必须定义一致。

- TiFlash：当分区表和非分区表的 TiFlash 副本定义不同时，无法执行 `EXCHANGE PARTITION` 操作。
- TiCDC：当分区表和非分区表都包含主键或唯一键时，TiCDC 会同步 `EXCHANGE PARTITION` 操作。否则，TiCDC 不会同步该操作。
- TiDB Lightning 和 BR：在使用 TiDB Lightning 导入或 BR 恢复时，不会执行 `EXCHANGE PARTITION` 操作。

### 管理 Range、Range COLUMNS、List 和 List COLUMNS 分区

本节以以下 SQL 语句创建的分区表为例，介绍如何管理范围分区和列表分区。

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

#### 删除分区

```sql
ALTER TABLE members DROP PARTITION p1990;

ALTER TABLE member_level DROP PARTITION l5;
```

#### 清空分区

```sql
ALTER TABLE members TRUNCATE PARTITION p1980;

ALTER TABLE member_level TRUNCATE PARTITION l4;
```

#### 添加分区

```sql
ALTER TABLE members ADD PARTITION (PARTITION `p1990to2010` VALUES LESS THAN (2010));

ALTER TABLE member_level ADD PARTITION (PARTITION l5_6 VALUES IN (5,6));
```

对于范围分区表，`ADD PARTITION` 会在现有分区后追加新分区。新分区的 `VALUES LESS THAN` 值必须大于现有分区，否则会报错：

```sql
ALTER TABLE members ADD PARTITION (PARTITION p1990 VALUES LESS THAN (2000));
```

```
ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition
```

#### 重组分区

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

更改分区方案定义：

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1960,p1960,p1970,p1980,p1990,p2000,p2010,p2020,pMax INTO
(PARTITION p1800 VALUES LESS THAN (1900),
 PARTITION p1900 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2100));

ALTER TABLE member_level REORGANIZE PARTITION l1_2,l3,l4,l5,l6 INTO
(PARTITION lOdd VALUES IN (1,3,5),
 PARTITION lEven VALUES IN (2,4,6));
```

重组分区时需注意以下要点：

- 重组分区（包括合并或拆分分区）可以将列出的分区变为一组新的分区定义，但不能更改分区类型（如将 List 类型改为 Range 类型，或将 Range COLUMNS 类型改为 Range 类型）。

- 对于范围分区表，只能重组其中的相邻分区。

    ```sql
    ALTER TABLE members REORGANIZE PARTITION p1800,p2000 INTO (PARTITION p2000 VALUES LESS THAN (2100));
    ```

    ```
    ERROR 8200 (HY000): Unsupported REORGANIZE PARTITION of RANGE; not adjacent partitions
    ```

- 对于范围分区表，修改区间末尾时，`VALUES LESS THAN` 新定义的区间必须覆盖最后一个分区的现有行。否则，现有行不再适用，会报错：

    ```sql
    INSERT INTO members VALUES (313, "John", "Doe", "2022-11-22", NULL);
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2050)); -- 该语句可正常执行，因为 2050 覆盖了现有行。
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2020)); -- 该语句会报错，因为 2022 不在新范围内。
    ```

    ```
    ERROR 1526 (HY000): Table has no partition for value 2022
    ```

- 对于列表分区表，修改分区定义的值集合时，新定义必须覆盖该分区的现有值。否则会报错：

    ```sql
    INSERT INTO member_level (id, level) values (313, 6);
    ALTER TABLE member_level REORGANIZE PARTITION lEven INTO (PARTITION lEven VALUES IN (2,4));
    ```

    ```
    ERROR 1526 (HY000): Table has no partition for value 6
    ```

- 分区重组后，对应分区的统计信息会过期，因此会收到如下警告。此时可以使用 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句更新统计信息。

    ```sql
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Level   | Code | Message                                                                                                                                                |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

### 管理哈希分区和键分区

本节以以下 SQL 语句创建的分区表为例，介绍如何管理哈希分区。对于键分区，也可使用相同的管理语句。

```sql
CREATE TABLE example (
  id INT PRIMARY KEY,
  data VARCHAR(1024)
)
PARTITION BY HASH(id)
PARTITIONS 2;
```

#### 增加分区数

将 `example` 表的分区数增加 1（从 2 增加到 3）：

```sql
ALTER TABLE example ADD PARTITION PARTITIONS 1;
```

你还可以通过添加分区定义指定分区选项。例如，以下语句将分区数从 3 增加到 5，并将新分区命名为 `pExample4` 和 `pExample5`：

```sql
ALTER TABLE example ADD PARTITION
(PARTITION pExample4 COMMENT = 'not p3, but pExample4 instead',
 PARTITION pExample5 COMMENT = 'not p4, but pExample5 instead');
```

#### 减少分区数

与范围分区和列表分区不同，哈希分区和键分区不支持 `DROP PARTITION`，但你可以使用 `COALESCE PARTITION` 减少分区数，或用 `TRUNCATE PARTITION` 删除指定分区的所有数据。

将 `example` 表的分区数减少 1（从 5 减少到 4）：

```sql
ALTER TABLE example COALESCE PARTITION 1;
```

> **注意：**
>
> 更改哈希分区或键分区表的分区数会通过将所有数据复制到新的分区数来重组分区。因此，更改哈希分区或键分区表的分区数后，会收到如下关于统计信息过期的警告。此时可以使用 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句更新统计信息。
>
> ```sql
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                                |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
> ```

要更好地了解 `example` 表当前的组织方式，可以如下显示用于重建 `example` 表的 SQL 语句：

```sql
SHOW CREATE TABLE\G
```

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
```

#### 清空分区

删除某个分区的所有数据：

```sql
ALTER TABLE example TRUNCATE PARTITION p0;
```

```
Query OK, 0 rows affected (0.03 sec)
```

### 将分区表转换为非分区表

要将分区表转换为非分区表，可以使用如下语句，该语句会移除分区、复制表的所有行，并在线重建索引：

```sql
ALTER TABLE <table_name> REMOVE PARTITIONING
```

例如，要将 `members` 分区表转换为非分区表，可以执行如下语句：

```sql
ALTER TABLE members REMOVE PARTITIONING
```

### 对现有表进行分区

要对现有的非分区表进行分区，或修改已分区表的分区类型，可以使用如下语句，该语句会根据新的分区定义复制所有行并在线重建索引：

```sql
ALTER TABLE <table_name> PARTITION BY <new partition type and definitions> [UPDATE INDEXES (<index name> {GLOBAL|LOCAL}[ , <index name> {GLOBAL|LOCAL}...])]
```

示例：

要将现有的 `members` 表转换为 10 个分区的 HASH 分区表，可以执行如下语句：

```sql
ALTER TABLE members PARTITION BY HASH(id) PARTITIONS 10;
```

要将现有的 `member_level` 表转换为范围分区表，可以执行如下语句：

```sql
ALTER TABLE member_level PARTITION BY RANGE(level)
(PARTITION pLow VALUES LESS THAN (1),
 PARTITION pMid VALUES LESS THAN (3),
 PARTITION pHigh VALUES LESS THAN (7)
 PARTITION pMax VALUES LESS THAN (MAXVALUE));
```

对非分区表进行分区或对已分区表重新分区时，可以根据需要将索引更新为全局索引或本地索引：

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

## 分区裁剪

[分区裁剪](/partition-pruning.md) 是一种优化，其基本思想非常简单——不扫描不匹配的分区。

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

如果你想获取如下 `SELECT` 语句的结果：

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

很明显，结果只会落在 `p1` 或 `p2` 分区，即只需在 `p1` 和 `p2` 中查找匹配的行。排除不需要的分区即为“裁剪”。如果优化器能够裁剪部分分区，则在分区表上的查询执行会比非分区表快得多。

优化器可以通过 `WHERE` 条件在以下两种场景下裁剪分区：

* partition_column = constant
* partition_column IN (constant1, constant2, ..., constantN)

目前，分区裁剪不支持 `LIKE` 条件。

### 分区裁剪生效的部分场景

1. 分区裁剪使用分区表上的查询条件，因此如果查询条件无法根据执行计划优化规则下推到分区表，则该查询不适用分区裁剪。

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

    在该查询中，left out join 被转换为 inner join，然后由 `t1.x = t2.x` 和 `t2.x > 5` 推导出 `t1.x > 5`，因此可用于分区裁剪，最终只保留分区 `p1`。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    在该查询中，`t2.x > 5` 无法下推到 `t1` 分区表，因此分区裁剪不会生效。

2. 由于分区裁剪在计划优化阶段完成，因此对于执行阶段才确定过滤条件的场景，分区裁剪不适用。

    例如：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    ```

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    该查询会从 `t2` 读取一行数据，并将结果用于 `t1` 的子查询。理论上，分区裁剪可以利用子查询中的 `t1.x > val` 表达式，但由于该条件在执行阶段才确定，因此不会生效。

3. 由于当前实现的限制，如果查询条件无法下推到 TiKV，则无法用于分区裁剪。

    以 `fn(col)` 表达式为例。如果 TiKV coprocessor 支持该 `fn` 函数，`fn(col)` 可能会根据谓词下推规则下推到叶子节点（即分区表），分区裁剪可以利用它。

    如果 TiKV coprocessor 不支持该 `fn` 函数，`fn(col)` 不会下推到叶子节点，而是在叶子节点之上形成 `Selection` 节点。当前分区裁剪实现不支持这种计划树。

4. 对于哈希分区和键分区，分区裁剪仅支持等值条件的查询。

5. 对于范围分区，分区裁剪生效的前提是分区表达式必须为 `col` 或 `fn(col)` 形式，且查询条件必须为 `>`、`<`、`=`、`>=`、`<=` 之一。如果分区表达式为 `fn(col)`，则 `fn` 必须是单调函数。

    如果 `fn` 是单调函数，则对于任意 `x` 和 `y`，若 `x > y`，则 `fn(x) > fn(y)`。此时 `fn` 可称为严格单调函数。对于任意 `x` 和 `y`，若 `x > y`，则 `fn(x) >= fn(y)`，此时 `fn` 也可称为“单调函数”。理论上，所有单调函数都支持分区裁剪。

    目前，TiDB 分区裁剪仅支持以下单调函数：

    * [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    * [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)
    * [`EXTRACT(<time unit> FROM <DATETIME/DATE/TIME column>)`](/functions-and-operators/date-and-time-functions.md)。对于 `DATE` 和 `DATETIME` 列，`YEAR` 和 `YEAR_MONTH` 时间单位被视为单调函数。对于 `TIME` 列，`HOUR`、`HOUR_MINUTE`、`HOUR_SECOND` 和 `HOUR_MICROSECOND` 被视为单调函数。注意 `EXTRACT` 的 `WEEK` 时间单位不支持分区裁剪。

    例如，分区表达式为简单列：

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    或分区表达式为 `fn(col)` 形式，`fn` 为 `to_days`：

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    一个例外是以 `floor(unix_timestamp())` 作为分区表达式。TiDB 针对此场景做了特殊优化，因此支持分区裁剪。

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## 分区选择

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

你可以查看存储在 `p1` 分区的行：

```sql
SELECT * FROM employees PARTITION (p1);
```

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
```

如果你想获取多个分区的行，可以用逗号分隔分区名。例如，`SELECT * FROM employees PARTITION (p1, p2)` 会返回 `p1` 和 `p2` 分区的所有行。

使用分区选择时，仍可使用 `WHERE` 条件和如 `ORDER BY`、`LIMIT` 等选项。也支持如 `HAVING`、`GROUP BY` 等聚合选项。

```sql
SELECT * FROM employees PARTITION (p0, p2)
    WHERE lname LIKE 'S%';
```

```
+----|-------|-------|----------|---------------+
| id | fname | lname | store_id | department_id |
+----|-------|-------|----------|---------------+
|  4 | Jim   | Smith |        2 |             4 |
| 11 | Jill  | Stone |        1 |             4 |
+----|-------|-------|----------|---------------+
2 rows in set (0.00 sec)
```

```sql
SELECT id, CONCAT(fname, ' ', lname) AS name
    FROM employees PARTITION (p0) ORDER BY lname;
```

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
```

```sql
SELECT store_id, COUNT(department_id) AS c
    FROM employees PARTITION (p1,p2,p3)
    GROUP BY store_id HAVING c > 4;
```

```
+---|----------+
| c | store_id |
+---|----------+
| 5 |        2 |
| 5 |        3 |
+---|----------+
2 rows in set (0.00 sec)
```

所有类型的表分区都支持分区选择，包括范围分区和哈希分区。对于哈希分区，如果未指定分区名，则自动使用 `p0`、`p1`、`p2`、...、`pN-1` 作为分区名。

`INSERT ... SELECT` 中的 `SELECT` 也可以使用分区选择。

## 分区的限制与约束

本节介绍 TiDB 分区表的一些限制和约束。

- 不支持使用 [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 语句更改分区表的列类型。
- 不支持使用 [`ALTER TABLE ... CACHE`](/cached-tables.md) 语句将分区表设置为缓存表。
- TiDB 中的 [临时表](/temporary-tables.md) **不** 支持与分区表兼容。
- 不支持在分区表上创建 [外键](/foreign-key.md)。
- [`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-) hint 对分区表及其相关索引无效，因为分区表上的索引无法有序读取。

### 分区键、主键和唯一键

本节讨论分区键与主键、唯一键的关系。其规则如下：分区表上的每个唯一键（包括主键）都必须包含分区表达式中的所有列，因为主键本质上也是唯一键。

> **注意：**
>
> 使用 [全局索引](#global-indexes) 时可以忽略此规则。

例如，以下建表语句是无效的：

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

在每种情况下，表中至少有一个唯一键未包含分区表达式中的所有列。

有效的语句如下：

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

以下示例会报错：

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

```
ERROR 8264 (HY000): Global Index is needed for index 'col1', since the unique index is not including all partitioning columns, and GLOBAL is not given as IndexOption
```

`CREATE TABLE` 语句失败的原因是，分区键包含了 `col1` 和 `col3`，但这两个列都不是表上所有唯一键的组成部分。经过如下修改后，`CREATE TABLE` 语句变为有效：

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

以下表无法进行分区，因为无法在分区键中包含属于两个唯一键的所有列：

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

由于每个主键本质上也是唯一键，所以下面两个语句是无效的：

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

上述示例中，主键未包含分区表达式引用的所有列。将缺失的列添加到主键后，`CREATE TABLE` 语句变为有效：

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

如果表没有唯一键或主键，则不受此限制。

在使用 DDL 语句变更表时，添加唯一索引时也需考虑此限制。例如，创建如下分区表：

```sql
CREATE TABLE t_no_pk (c1 INT, c2 INT)
    PARTITION BY RANGE(c1) (
        PARTITION p0 VALUES LESS THAN (10),
        PARTITION p1 VALUES LESS THAN (20),
        PARTITION p2 VALUES LESS THAN (30),
        PARTITION p3 VALUES LESS THAN (40)
    );
```

```
Query OK, 0 rows affected (0.12 sec)
```

你可以通过 `ALTER TABLE` 语句添加非唯一索引。但如果要添加唯一索引，必须包含 `c1` 列。

在分区表上，不能将前缀索引指定为唯一属性：

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

### 全局索引

在引入全局索引之前，TiDB 为每个分区创建本地索引，导致 [一个限制](#partitioning-keys-primary-keys-and-unique-keys)：主键和唯一键必须包含分区键以保证数据唯一性。此外，跨多个分区查询数据时，TiDB 需要扫描每个分区的数据返回结果。

为了解决这些问题，TiDB 在 v8.3.0 引入了全局索引功能。全局索引通过单一索引覆盖整个表的数据，使主键和唯一键无需包含所有分区键即可保证全局唯一性。此外，全局索引可以一次性访问跨多个分区的索引数据，而无需分别查找每个分区的本地索引，大幅提升非分区键的查询性能。从 v8.5.4 开始，非唯一索引也可以创建为全局索引。

要创建全局索引，可以在索引定义中添加 `GLOBAL` 关键字。

> **注意：**
>
> 全局索引会影响分区管理。`DROP`、`TRUNCATE` 和 `REORGANIZE PARTITION` 操作也会触发表级全局索引的更新，即这些 DDL 操作只有在对应表的全局索引全部更新完成后才会返回结果。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2) GLOBAL,
    UNIQUE KEY uidx3(col3),
    KEY idx1(col1) GLOBAL
)
PARTITION BY HASH(col3)
PARTITIONS 4;
```

在上述示例中，唯一索引 `uidx12` 和非唯一索引 `idx1` 是全局索引，`uidx3` 是普通唯一索引。

注意，**聚簇索引** 不能为全局索引，如下所示：

```sql
CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    PRIMARY KEY (col2) CLUSTERED GLOBAL
) PARTITION BY HASH(col1) PARTITIONS 5;
```

```
ERROR 1503 (HY000): A CLUSTERED INDEX must include all columns in the table's partitioning function
```

原因是如果聚簇索引为全局索引，则表不再分区。因为聚簇索引的键也是分区级的记录键，而全局索引是表级的，两者冲突。如果需要将主键设为全局索引，必须显式定义为非聚簇索引，例如 `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。

你可以通过 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 输出中的 `GLOBAL` 索引选项识别全局索引。

```sql
SHOW CREATE TABLE t1\G
```

```
       Table: t1
Create Table: CREATE TABLE `t1` (
  `col1` int NOT NULL,
  `col2` date NOT NULL,
  `col3` int NOT NULL,
  `col4` int NOT NULL,
  UNIQUE KEY `uidx12` (`col1`,`col2`) /*T![global_index] GLOBAL */,
  UNIQUE KEY `uidx3` (`col3`),
  KEY `idx1` (`col1`) /*T![global_index] GLOBAL */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY HASH (`col3`) PARTITIONS 4
1 row in set (0.00 sec)
```

你也可以查询 [`INFORMATION_SCHEMA.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md) 表，并查看输出中的 `IS_GLOBAL` 列。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE table_name='t1';
```

```
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| TABLE_SCHEMA | TABLE_NAME | NON_UNIQUE | KEY_NAME | SEQ_IN_INDEX | COLUMN_NAME | SUB_PART | INDEX_COMMENT | Expression | INDEX_ID | IS_VISIBLE | CLUSTERED | IS_GLOBAL |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
| test         | t1         |          0 | uidx12   |            1 | col1        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx12   |            2 | col2        |     NULL |               | NULL       |        1 | YES        | NO        |         1 |
| test         | t1         |          0 | uidx3    |            1 | col3        |     NULL |               | NULL       |        2 | YES        | NO        |         0 |
| test         | t1         |          1 | idx1     |            1 | col1        |     NULL |               | NULL       |        3 | YES        | NO        |         1 |
+--------------+------------+------------+----------+--------------+-------------+----------+---------------+------------+----------+------------+-----------+-----------+
3 rows in set (0.00 sec)
```

对非分区表进行分区或对已分区表重新分区时，可以根据需要将索引更新为全局索引或本地索引。

例如，以下 SQL 语句基于 `col1` 列重新分区表 `t1`，将全局索引 `uidx12` 和 `idx1` 更新为本地索引，将本地索引 `uidx3` 更新为全局索引。由于 `uidx3` 是 `col3` 列的唯一索引，因此必须为全局索引以保证 `col3` 在所有分区中的唯一性。`uidx12` 和 `idx1` 是 `col1` 列上的索引，可以为全局索引或本地索引。

```sql
ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL, idx1 LOCAL);
```

#### 全局索引的限制

- 如果索引定义中未显式指定 `GLOBAL` 关键字，TiDB 默认创建本地索引。
- `GLOBAL` 和 `LOCAL` 关键字仅适用于分区表，对非分区表无影响。换句话说，非分区表中全局索引和本地索引无区别。
- `DROP PARTITION`、`TRUNCATE PARTITION`、`REORGANIZE PARTITION` 等 DDL 操作也会触发全局索引的更新。这些 DDL 操作需等待全局索引更新完成后才返回结果，因此执行时间相应增加。尤其在数据归档场景下，如 `DROP PARTITION` 和 `TRUNCATE PARTITION`，没有全局索引时这些操作通常能立即完成，有全局索引时，需更新的索引越多，执行时间越长。
- 带有全局索引的表不支持 `EXCHANGE PARTITION` 操作。
- 默认情况下，分区表的主键为聚簇索引，且必须包含分区键。如果需要主键不包含分区键，可以在建表时显式指定主键为非聚簇全局索引，例如 `PRIMARY KEY(col1, col2) NONCLUSTERED GLOBAL`。
- 如果全局索引添加在表达式列上，或全局索引为前缀索引（如 `UNIQUE KEY idx_id_prefix (id(10)) GLOBAL`），则需要手动收集该全局索引的统计信息。

### 分区表达式相关函数的限制

分区表达式中只允许使用以下函数：

```
ABS()
CEILING()
DATEDIFF()
DAY()
DAYOFMONTH()
DAYOFWEEK()
DAYOFYEAR()
EXTRACT() (see EXTRACT() function with WEEK specifier)
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
UNIX_TIMESTAMP() (with TIMESTAMP columns)
WEEKDAY()
YEAR()
YEARWEEK()
```

### 与 MySQL 的兼容性

目前，TiDB 支持范围分区、范围 COLUMNS 分区、列表分区、列表 COLUMNS 分区、哈希分区和键分区。MySQL 支持的其他分区类型，TiDB 暂不支持。

对于不支持的分区类型，在 TiDB 中创建表时，分区信息会被忽略，表会以普通表形式创建，并返回警告。

TiDB 目前不支持 `LOAD DATA` 语法的分区选择。

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

常规的 `LOAD DATA` 操作是支持的：

```sql
load local data infile "xxx" into t ...
```

但 `Load Data` 不支持分区选择：

```sql
load local data infile "xxx" into t partition (p1)...
```

对于分区表，`select * from t` 返回的结果在分区间是无序的。这与 MySQL 的结果不同，MySQL 的结果在分区间有序，在分区内无序。

```sql
create table t (id int, val int) partition by range (id) (
    partition p0 values less than (3),
    partition p1 values less than (7),
    partition p2 values less than (11));
```

```
Query OK, 0 rows affected (0.10 sec)
```

```sql
insert into t values (1, 2), (3, 4),(5, 6),(7,8),(9,10);
```

```
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

TiDB 每次返回的结果都不同，例如：

```sql
select * from t;
```

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
```

MySQL 返回的结果如下：

```sql
select * from t;
```

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
```

## 动态裁剪模式

TiDB 访问分区表时有 `dynamic` 和 `static` 两种模式。自 v6.3.0 起，默认使用 `dynamic` 模式。但动态分区仅在收集了完整的表级统计信息（全局统计信息）后才生效。如果在全局统计信息收集完成前启用 `dynamic` 裁剪模式，TiDB 会保持在 `static` 模式，直到全局统计信息收集完成。关于全局统计信息的详细信息，参见 [动态裁剪模式下分区表的统计信息收集](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手动 ANALYZE 和普通查询使用会话级 `tidb_partition_prune_mode` 设置。后台的 `auto-analyze` 操作使用全局 `tidb_partition_prune_mode` 设置。

在 `static` 模式下，分区表使用分区级统计信息。在 `dynamic` 模式下，分区表使用表级全局统计信息。

从 `static` 模式切换到 `dynamic` 模式时，需要手动检查并收集统计信息。因为切换到 `dynamic` 模式后，分区表只有分区级统计信息，没有表级统计信息。全局统计信息只会在下次 `auto-analyze` 操作时收集。

```sql
set session tidb_partition_prune_mode = 'dynamic';
show stats_meta where table_name like "t";
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
| test    | t          | p1             | 2022-05-27 20:23:34 |            2 |         4 |
| test    | t          | p2             | 2022-05-27 20:23:34 |            2 |         4 |
+---------+------------+----------------+---------------------+--------------+-----------+
3 rows in set (0.01 sec)
```

为确保在启用全局 `dynamic` 裁剪模式后 SQL 语句使用的统计信息正确，你需要手动对表或表的某个分区执行 `analyze`，以获得全局统计信息。

```sql
analyze table t partition p1;
show stats_meta where table_name like "t";
```

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
```

如果在 `analyze` 过程中出现如下警告，说明分区统计信息不一致，需要重新收集这些分区或整个表的统计信息。

```
| Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions
```

你也可以使用脚本更新所有分区表的统计信息。详情参见 [动态裁剪模式下分区表统计信息的更新](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

表级统计信息准备好后，可以启用全局动态裁剪模式，对所有 SQL 语句和 `auto-analyze` 操作生效。

```sql
set global tidb_partition_prune_mode = dynamic
```

在 `static` 模式下，TiDB 会分别使用多个算子访问每个分区，然后用 `Union` 合并结果。以下示例是一个简单的读取操作，TiDB 用 `Union` 合并两个分区的结果：

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
        partition p0 values less than (100),
        partition p1 values less than (200),
        partition p2 values less than (300),
        partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
```

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
```

在 `dynamic` 模式下，每个算子支持直接访问多个分区，TiDB 不再使用 `Union`。

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

从上述查询结果可以看到，执行计划中的 `Union` 算子消失了，但分区裁剪仍然生效，执行计划只访问了 `p0` 和 `p1`。

`dynamic` 模式让执行计划更简单清晰。省略 Union 操作可以提升执行效率，避免 Union 并发执行带来的问题。此外，`dynamic` 模式还允许使用 IndexJoin 的执行计划，而 `static` 模式下无法使用（见下例）。

**示例 1**：以下示例在 `static` 模式下使用 IndexJoin 执行计划进行查询：

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

从示例 1 可以看到，即使使用了 `TIDB_INLJ` hint，分区表上的查询也无法选择 IndexJoin 的执行计划。

**示例 2**：以下示例在 `dynamic` 模式下使用 IndexJoin 执行计划进行查询：

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

从示例 2 可以看到，在 `dynamic` 模式下，执行查询时选择了 IndexJoin 的执行计划。

目前，`static` 裁剪模式不支持 prepared 和非 prepared 语句的计划缓存。

### 动态裁剪模式下分区表统计信息的更新

1. 找出所有分区表：

    ```sql
    SELECT DISTINCT CONCAT(TABLE_SCHEMA,'.', TABLE_NAME)
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA', 'mysql', 'sys', 'PERFORMANCE_SCHEMA', 'METRICS_SCHEMA');
    ```

    ```
    +-------------------------------------+
    | concat(TABLE_SCHEMA,'.',TABLE_NAME) |
    +-------------------------------------+
    | test.t                              |
    +-------------------------------------+
    1 row in set (0.02 sec)
    ```

2. 生成更新所有分区表统计信息的语句：

    ```sql
    SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;')
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    ```

    ```
    +----------------------------------------------------------------------+
    | concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') |
    +----------------------------------------------------------------------+
    | ANALYZE TABLE test.t ALL COLUMNS;                                    |
    +----------------------------------------------------------------------+
    1 row in set (0.01 sec)
    ```

    你可以将 `ALL COLUMNS` 替换为你需要的列。

3. 将批量更新语句导出到文件：

    ```shell
    mysql --host xxxx --port xxxx -u root -p -e "SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        FROM information_schema.PARTITIONS \
        WHERE TIDB_PARTITION_ID IS NOT NULL \
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4. 批量执行更新：

    在执行 `source` 命令前处理 SQL 语句：

    ```
    sed -i "" '1d' gatherGlobalStats.sql --- mac
    sed -i '1d' gatherGlobalStats.sql --- linux
    ```

    ```sql
    SET session tidb_partition_prune_mode = dynamic;
    source gatherGlobalStats.sql
    ```