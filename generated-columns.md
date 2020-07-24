---
title: Generated Columns
summary: Learn how to use generated columns.
category: reference
aliases: ['/docs/dev/reference/sql/generated-columns/']
---

# Generated Columns

TiDB supports generated columns as part of MySQL 5.7 compatibility. One of the primary use cases for generated columns is to extract data out of a JSON data type and enable it to be indexed.

## Index JSON using generated column

In both MySQL 5.7 and TiDB, columns of type JSON can not be indexed directly. i.e. The following table structure is **not supported**:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

To index a JSON column, you must first extract it as a generated column.

Using the `city` stored generated column as an example, you are then able to add an index:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED,
    KEY (city)
);
```

In this table, the `city` column is a **generated column**. As the name implies, the column is generated from other columns in the table, and cannot be assigned a value when inserted or updated. This column is generated based on a defined expression and is stored in the database. Thus this column can be read directly, not in a way that its dependent column `address_info` is read first and then the data is calculated. The index on `city` however is _stored_ and uses the same structure as other indexes of the type `varchar(64)`.

You can use the index on the stored generated column in order to speed up the following statement:

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

If no data exists at path `$.city`, `JSON_EXTRACT` returns `NULL`. If you want to enforce a constraint that `city` must be `NOT NULL`, you can define the `generated column` as follows:

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED NOT NULL,
    KEY (city)
);
```

Both `INSERT` and `UPDATE` statements check the `generated column` definition. Rows that do not pass validation return errors:

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## Use generated virtual columns

TiDB also supports generated virtual columns. Different from generated store columns, generated virtual columns are **virtual** in that they are generated as needed and are not stored in the database or cached in the memory.

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL
);
```

## Replace expression with generated column

When an expression that appears in a query has been stored as a generated column with an index, TiDB replaces the expression with the corresponding generated column. Therefore, TiDB can use this index when generating the query plan.

The following example illustrates how to create a generated column for the expression `a+1` and add an index to speed up the query.

{{< copyable "sql" >}}

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
4 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

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
2 rows in set (0.01 sec)
```

> **Note:**
>
> Only when the type of expression to be replaced is strictly equal to that of the generated column, the replacement is performed.
>
> In the above example, the type of `a` is `int`, while the column type of `a+1` is `bigint`. If the type of the generated column is defined as `int`, the replacement is not performed.
>
> For more details about type conversion rules, see [Type Conversion in Expression Evaluation](/functions-and-operators/type-conversion-in-expression-evaluation.md)

## Limitations

The current limitations of JSON and generated columns are as follows:

- You cannot add the generated column in the storage type of `STORED` through `ALTER TABLE`.
- You can neither convert a generated stored column to a normal column through the `ALTER TABLE` statement nor convert a normal column to a generated stored column.
- You cannot modify the **expression** of a generated stored column through the `ALTER TABLE` statement.
- Not all [JSON functions](/functions-and-operators/json-functions.md) are supported.
- Currently, the replacement rule is valid only when the generated column is a virtual column. You cannot replace the input expression with the generated stored column. However, you can use the index by using the generated column itself.
