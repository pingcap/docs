---
title: Generated Columns
summary: 学习如何使用 generated columns。
---

# Generated Columns

本文介绍了 generated columns 的概念和用法。

## Basic concepts

与普通列不同，generated column 的值由列定义中的表达式计算得出。在插入或更新 generated column 时，不能为其赋值，只能使用 `DEFAULT`。

有两种类型的 generated columns：virtual 和 stored。virtual generated column 不占用存储空间，读取时会计算得出。stored generated column 在写入（插入或更新）时计算，并占用存储空间。与 virtual generated columns 相比，stored generated columns 具有更好的读取性能，但占用更多磁盘空间。

无论是 virtual 还是 stored，都可以在 generated column 上创建索引。

## Usage

generated columns 的主要用途之一是从 JSON 数据类型中提取数据并对其建立索引。

在 MySQL 8.0 和 TiDB 中，JSON 类型的列不能直接建立索引。也就是说，以下表结构 **不支持**：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

为了对 JSON 列建立索引，必须先将其提取为 generated column。

以 `address_info` 中的 `city` 字段为例，可以创建一个 virtual generated column 并为其添加索引：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))), -- virtual generated column
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL, -- virtual generated column
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED, -- stored generated column
    KEY (city)
);
```

在此表中，`city` 列为 **virtual generated column**，并且已建立索引。以下查询可以利用索引加快执行速度：

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

```sql
EXPLAIN SELECT name, id FROM person WHERE city = 'Beijing';
```

```sql
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| id                              | estRows | task      | access object                  | operator info                                               |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| Projection_4                    | 10.00   | root      |                                | test.person.name, test.person.id                            |
| └─IndexLookUp_10                | 10.00   | root      |                                |                                                             |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:person, index:city(city) | range:["Beijing","Beijing"], keep order:false, stats:pseudo |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:person                   | keep order:false, stats:pseudo                              |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
```

从执行计划可以看出，索引 `city` 被用来读取满足条件 `city ='Beijing'` 的行的 **HANDLE**，然后利用该 HANDLE 读取对应行的数据。

如果路径 `$.city` 中没有数据，`JSON_EXTRACT` 会返回 `NULL`。如果你希望强制 `city` 不为 `NULL`，可以将 virtual generated column 定义为：

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) NOT NULL,
    KEY (city)
);
```

## Validation of generated columns

在 `INSERT` 和 `UPDATE` 语句中，都会检查 virtual column 的定义。未通过验证的行会返回错误：

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## Generated columns index replacement rule

当查询中的表达式与带索引的 generated column 严格等价时，TiDB 会用对应的 generated column 替换该表达式，以便优化器在构建执行计划时考虑该索引。

以下示例为表达式 `a+1` 创建了 generated column 并添加了索引。`a` 的列类型为 int，`a+1` 的列类型为 bigint。如果将 generated column 的类型设置为 int，则不会进行替换。关于类型转换规则，详见 [Type Conversion of Expression Evaluation](/functions-and-operators/type-conversion-in-expression-evaluation.md)。

```sql
create table t(a int);
desc select a+1 from t where a+1=3;
```

```sql
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Projection_4              | 8000.00  | root      |               | plus(test.t.a, 1)->Column#3    |
| └─TableReader_7           | 8000.00  | root      |               | data:Selection_6               |
|   └─Selection_6           | 8000.00  | cop[tikv] |               | eq(plus(test.t.a, 1), 3)       |
|     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
4 行，耗时 0.00 秒
```

```sql
alter table t add column b bigint as (a+1) virtual;
alter table t add index idx_b(b);
desc select a+1 from t where a+1=3;
```

```sql
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                     | estRows | task      | access object           | operator info                               |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                         | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t, index:idx_b(b) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
2 行，耗时 0.01 秒
```

> **Note:**
>
> 如果要替换的表达式和生成列都是字符串类型，但长度不同，仍可以通过将系统变量 [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) 设置为 `ON` 来实现替换。在配置该变量时，确保生成列计算出的值严格满足生成列的定义，否则可能因长度差异导致数据被截断，从而产生错误结果。详见 GitHub issue [#35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)。

## Limitations

目前关于 JSON 和 generated columns 的限制如下：

- 不能通过 `ALTER TABLE` 添加 stored generated column。
- 不能通过 `ALTER TABLE` 将 stored generated column 转换为普通列，也不能将普通列转换为 stored generated column。
- 不能通过 `ALTER TABLE` 修改 stored generated column 的表达式。
- 并非所有 [JSON 函数](/functions-and-operators/json-functions.md) 都被支持。
- 不支持 [`NULLIF()` 函数](/functions-and-operators/control-flow-functions.md#nullif)，可以使用 [`CASE` 函数](/functions-and-operators/control-flow-functions.md#case) 替代。
- 当前，生成列索引替换规则仅在生成列为 virtual 时有效，存储型生成列不适用，但索引仍可通过直接使用生成列本身来利用。
- 以下函数和表达式在定义生成列时不允许使用，使用时会返回错误：
    - 非确定性函数和表达式，如 `RAND`、`UUID` 和 `CURRENT_TIMESTAMP`。
    - 依赖会话或全局状态的函数，如 `CONNECTION_ID` 和 `CURRENT_USER`。
    - 影响系统状态或进行系统交互的函数，如 `GET_LOCK`、`RELEASE_LOCK` 和 `SLEEP`。