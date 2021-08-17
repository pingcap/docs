---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-index/','/docs/dev/reference/sql/statements/create-index/']
---

# CREATE INDEX

This statement adds a new index to an existing table. It is an alternative syntax to `ALTER TABLE .. ADD INDEX`, and included for MySQL compatibility.

## Synopsis

```ebnf+diagram
CreateIndexStmt ::=
    'CREATE' IndexKeyTypeOpt 'INDEX' IfNotExists Identifier IndexTypeOpt 'ON' TableName '(' IndexPartSpecificationList ')' IndexOptionList IndexLockAndAlgorithmOpt

IndexKeyTypeOpt ::=
    ( 'UNIQUE' | 'SPATIAL' | 'FULLTEXT' )?

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

IndexTypeOpt ::=
    IndexType?

IndexPartSpecificationList ::=
    IndexPartSpecification ( ',' IndexPartSpecification )*

IndexOptionList ::=
    IndexOption*

IndexLockAndAlgorithmOpt ::=
    ( LockClause AlgorithmClause? | AlgorithmClause LockClause? )?

IndexType ::=
    ( 'USING' | 'TYPE' ) IndexTypeName

IndexPartSpecification ::=
    ( ColumnName OptFieldLen | '(' Expression ')' ) Order

IndexOption ::=
    'KEY_BLOCK_SIZE' '='? LengthNum
|   IndexType
|   'WITH' 'PARSER' Identifier
|   'COMMENT' stringLit
|   IndexInvisible

IndexTypeName ::=
    'BTREE'
|   'HASH'
|   'RTREE'

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?

OptFieldLen ::=
    FieldLen?

IndexNameList ::=
    ( Identifier | 'PRIMARY' )? ( ',' ( Identifier | 'PRIMARY' ) )*

KeyOrIndex ::=
    'Key' | 'Index'
```

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## Expression index

In some scenarios, query conditions run a filtering process based on a certain expression. In this case, the query performance is relatively poor because general indexes can not take effect in those scenarios, so the query can only be completed by traversing the entire table. Expression indexes are the special index that can be built on an expression. Once an expression index is built, you can use the index for the expression-based query, which significantly speeds up the query performance.

If you want to build the indexes based on `col1+cols2`, run the following SQL statement as an example:

{{< copyable "sql" >}}

```sql
CREATE INDEX idx1 ON t1 ((col1 + col2));
```

Or you can run the following alternative statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 ADD INDEX idx1((col1 + col2));
```

You can also specify the expression index as you build the table:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), key index((col1 + col2)));
```

The method of deleting an expression index is the same as that of deleting a general index:

{{< copyable "sql" >}}

```sql
DROP INDEX idx1 ON t1;
```

> **Note:**
>
> An expression index can not be a primary key.
>
> An expression with expression indexes can not contain the following:
>
> - volatile functions, such as `rand()`, `now()`, and so on.
> - system variables and user variables.
> - a subquery.
> - `AUTO_INCREMENT` column. However, there is one exception: you can remove this restriction by setting the value of `tidb_enable_auto_increment_in_generated` (system variable) to `true`.
> - window functions.
> - the ROW functions, such as `create table t (j json, key k (((j,j))));`.
> - aggregate functions.
> 
> An expression index takes names implicitly by setting `_V$_{index_name}_{index_offset}`. Suppose you try to set a new expression index's name that a column has taken when creating an expression index. In that case, an error returns in this process. Besides, if you add a column with an existing name, the same error returns.
>
> The number of parameters of the functions that are in an expression with expression indexes must be correct.

When the expression in a query statement matches the expression in an expression index, the optimizer can choose to use the expression index for the query. In some cases, the optimizer may not select an expression index depending on statistics. At that time, you can force the optimizer to select an expression index by specifying optimizer hints.

For example, suppose you build the expression index `idx` on the expression `lower(col1)`:

If the results of the query statement are the same expressions, you can use expression indexes. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT lower(col1) FROM t;
```

If the same expressions are included in the filtering conditions, you can use expression indexes. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

When the queries are sorted by the same expressions, you can use expression indexes. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT * FROM t ORDER BY lower(col1);
```

If the same expressions are included in the aggregate (`GROUP BY`) functions, you can use expression indexes. Take the following statements as an example:

{{< copyable "sql" >}}

```sql
SELECT max(lower(col1)) FROM t；
SELECT min(col1) FROM t GROUP BY lower(col1);
```

To see the expression corresponding to the expression index, run `show index`, or check the system table `information_schema.tidb_indexes` and the table `information_schema.STATISTICS`. The Expression in the output indicates the corresponded expression. As for the indexes that are not expression indexes, the column shows `NULL`.

The cost of maintaining an expression index is higher than that of maintaining other indexes, because the value of the expression needs to be calculated whenever a row is inserted or updated. The value of the expression is already stored in the index, so this value does not require recalculation when the optimizer selects the expression index.

Therefore, when the query performance outweighs the insert and update performance, you can consider indexing the expressions.

Expression indexes have the same syntax and limitations as in MySQL. They are implemented by building indexes on generated virtual columns that are invisible, so the supported expressions inherit all [limitations of virtual generated columns](/generated-columns.md#limitations).

## Invisible index

Invisible indexes are indexes that are ignored by the query optimizer:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

For details, see [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md).

## Associated session variables

The global variables associated with the `CREATE INDEX` statement are `tidb_ddl_reorg_worker_cnt`, `tidb_ddl_reorg_batch_size`, `tidb_ddl_reorg_priority`, and `tidb_enable_auto_increment_in_generated`. Refer to [system variables](/system-variables.md#tidb_ddl_reorg_worker_cnt) for details.

## MySQL compatibility

* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* Descending indexes are not supported (similar to MySQL 5.7).
* Adding the primary key of the `CLUSTERED` type to a table is not supported. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
* Expression indexes are incompatible with the views. When you query contents via a view, the expression index can not be used at the same time.
* There are compatibility issues between expression indexes and bindings. When an expression in an expression index has constants, the binding created for the corresponding query expands its scope. For example, suppose the expression in the expression index is   `a+1`, and the corresponding query condition is  `a+1 > 2`. In this case, the binding is `a+? > ?`, which means that the queries such as  `a+2 > 2` are also forced to select expression indexes. It results in a poor execution plan. Besides, this also affects the baseline capturing and baseline evolution belonging to SQL Plan Management.

## See also

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
