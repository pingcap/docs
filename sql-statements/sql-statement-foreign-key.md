---
title: FOREIGN KEY
summary: An overview of the usage of FOREIGN KEY for the TiDB database.
---

# FOREIGN KEY

Starting from v6.6.0, TiDB supports the foreign key feature, which allows cross-table referencing of related data, and foreign key constraints to maintain data consistency.

The foreign key is defined in the child table. The syntax is as follows:

```sql
[CONSTRAINT identifier] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]

reference_option:
    RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT
```

## Naming

The naming of a foreign key follows the following rules:

- If a name is specified in `CONSTRAINT identifier`, the specified name is used.
- If no name is specified in `CONSTRAINT identifier`, but a name is specified in `FOREIGN KEY identifier`, the name specified in the `FOREIGN KEY identifier` is used.
- If neither `CONSTRAINT identifier` nor `FOREIGN KEY identifier` specifies a name, a name is automatically generated, such as `fk_1`, `fk_2`, and `fk_3`.
- The foreign key name must be unique in the current table. Otherwise, an error `ERROR 1826: Duplicate foreign key constraint name 'fk'` is reported when the foreign key is created.

## Restrictions

When creating a foreign key, the following conditions must be met:

- Neither the parent table nor the child table is a temporary table.
- The user has the `REFERENCES` privilege on the parent table.
- The columns referenced by the foreign key in the parent table and the child table are of the same data type and have the same size, precision, length, character set, and collation.
- The columns in the foreign key cannot reference themselves.
- The columns in the foreign key and the columns in the referenced parent table have corresponding indexes, and the order of the columns in the index matches that in the foreign key. This is to use the index to avoid full table scans when performing foreign key constraint checks.

    - If there is no corresponding foreign key index in the parent table, an error `ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'` is reported.
    - If there is no corresponding foreign key index in the child table, an index is automatically created with the same name as the foreign key.

- It is not supported to create a foreign key on a column of the `BLOB` or `TEXT` type.
- It is not supported to create a foreign key on a partitioned table.
- It is not supported to create a foreign key on a virtual generated column.

## Reference operations

If an `UPDATE` or `DELETE` operation affects a foreign key value in the parent table, the corresponding foreign key value in the child table is determined by the reference operation defined by the `ON UPDATE` or `ON DELETE` clause in the foreign key definition. The reference operations include the following:

- `CASCADE`: automatically updates or deletes the matching rows in the child table when the `UPDATE` or `DELETE` operation affects the parent table. The cascade operation is performed in a depth-first manner.
- `SET NULL`: automatically sets the matching foreign key columns in the child table to `NULL` when the `UPDATE` or `DELETE` operation affects the parent table.
- `RESTRICT`: denies the `UPDATE` or `DELETE` operation if the child table contains matching rows.
- `NO ACTION`: the same as `RESTRICT`.
- `SET DEFAULT`: the same as `RESTRICT`.

If there is no matching foreign key value in the parent table, the `INSERT` or `UPDATE` operation on the child table is rejected.

If the foreign key definition does not specify `ON DELETE` or `ON UPDATE`, the default behavior is `NO ACTION`.

If the foreign key is defined on a `STORED GENERATED COLUMN`, the `CASCADE`, `SET NULL`, and `SET DEFAULT` references are not supported.

## Usage examples of foreign keys

The following example uses a single-column foreign key to associate the parent table and the child table:

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT,
    INDEX idx_pid (pid),
    FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE
);
```

The following is a more complex example where the `product_order` table has two foreign keys that reference the other two tables. One of the foreign keys references two indexes on the `product` table, and the other references a single index on the `customer` table:

```sql
CREATE TABLE product (
    category INT NOT NULL,
    id INT NOT NULL,
    price DECIMAL(20,10),
    PRIMARY KEY(category, id)
);

CREATE TABLE customer (
    id INT KEY
);

CREATE TABLE product_order (
    id INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(id),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
);
```

## Create a foreign key constraint

To create a foreign key constraint, you can use the following `ALTER TABLE` statement:

```sql
ALTER TABLE table_name
    ADD [CONSTRAINT [identifier]] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]
```

The foreign key can be self-referencing, that is, referencing the same table. When you add a foreign key constraint to a table using `ALTER TABLE`, you need to first create an index on the parent table column that the foreign key references.

## Delete a foreign key constraint

To delete a foreign key constraint, you can use the following `ALTER TABLE` statement:

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

If the foreign key constraint is named when it is created, you can reference the name to delete the foreign key constraint. Otherwise, the constraint name is generated automatically. You can use `SHOW CREATE TABLE` to view the foreign key name:

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## Foreign key constraint check

Whether to enable the foreign key constraint check is controlled by the system variable [`foreign_key_checks`](/system-variables.md#foreign_key_checks). By default, this variable value is set to `ON`, meaning that the foreign key constraint check is enabled. This variable has two scopes: `GLOBAL` and `SESSION`. Keeping this variable enabled can ensure the integrity of foreign key reference relationships.

The effect of disabling [`foreign_key_checks`](/system-variables.md#foreign_key_checks) is as follows:

- When you delete a parent table referenced by a foreign key, the deletion can succeed only when the foreign key constraint check is disabled.
- When you import data to a database, the order of creating tables might be different from the foreign key dependency order, which might cause the creation of tables to fail. Only when the foreign key constraint check is disabled can the tables be created successfully. In addition, disabling the foreign key constraint check can speed up data import.
- When you import data to a database, if the data of the child table is imported first, an error will be reported. Only when the foreign key constraint check is disabled can the data of the child table be imported successfully.
- If an `ALTER TABLE` operation to be executed involves change of the foreign key, this operation succeeds only when the foreign key constraint check is disabled.

When the foreign key constraint check is disabled, the foreign key constraint check and reference operation are not executed, except for the following scenarios:

- When executing `ALTER TABLE`, if the definition of the foreign key is incorrect, an error is still reported.
- When deleting the index required by the foreign key, you should delete the foreign key first. Otherwise, an error is reported.
- When you create a foreign key but it does not meet related conditions or restrictions, an error is reported.

## Locking

When `INSERT` or `UPDATE` a child table, the foreign key constraint checks whether the corresponding foreign key value exists in the parent table, and locks the row in the parent table to avoid the foreign key value being deleted by other operations violating the foreign key constraint. The locking behavior is equivalent to performing a `SELECT FOR UPDATE` operation on the row where the foreign key value is located in the parent table. Because TiDB currently does not support `LOCK IN SHARE MODE`, if there are a lot of concurrent writes to the child table and most of the referenced foreign key values are the same, there might be serious lock conflicts. It is recommended to disable [`foreign_key_checks`](/system-variables.md#foreign_key_checks) when writing a large number of child table data.

## Definition and metadata of foreign keys

To view the definition of a foreign key constraint, use the `SHOW CREATE TABLE` statement:

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

You can get information about foreign keys from the [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md) system table. The following is an example query:

```sql
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+------------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME    | COLUMN_NAME      | CONSTRAINT_NAME |
+--------------+---------------+------------------+-----------------+
| test         | child         | pid              | fk_1            |
| test         | product_order | product_category | fk_1            |
| test         | product_order | product_id       | fk_1            |
| test         | product_order | customer_id      | fk_2            |
+--------------+---------------+------------------+-----------------+
```

## View execution plans with foreign keys

You can use the `EXPLAIN` statement to view execution plans. The `Foreign_Key_Check` operator performs the foreign key constraint check on DML statements that are executed.

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

You can use the `EXPLAIN ANALYZE` statement to view the execution of the foreign key reference behavior. The `Foreign_Key_Cascade` operator performs foreign key referencing for DML statements that are executed.

```sql
mysql> explain analyze delete from parent where id = 1;
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| id                               | estRows | actRows | task      | access object                   | execution info                                                                                                                                                                               | operator info                               | memory    | disk |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| Delete_2                         | N/A     | 0       | root      |                                 | time:117.3µs, loops:1                                                                                                                                                                        | N/A                                         | 380 Bytes | N/A  |
| ├─Point_Get_1                    | 1.00    | 1       | root      | table:parent                    | time:63.6µs, loops:2, Get:{num_rpc:1, total_time:29.9µs}                                                                                                                                     | handle:1                                    | N/A       | N/A  |
| └─Foreign_Key_Cascade_3          | 0.00    | 0       | root      | table:child, index:idx_pid      | total:1.28ms, foreign_keys:1                                                                                                                                                                 | foreign_key:fk_1, on_delete:CASCADE         | N/A       | N/A  |
|   └─Delete_7                     | N/A     | 0       | root      |                                 | time:904.8µs, loops:1                                                                                                                                                                        | N/A                                         | 1.11 KB   | N/A  |
|     └─IndexLookUp_11             | 10.00   | 1       | root      |                                 | time:869.5µs, loops:2, index_task: {total_time: 371.1µs, fetch_handle: 357.3µs, build: 1.25µs, wait: 12.5µs}, table_task: {total_time: 382.6µs, num: 1, concurrency: 5}                      |                                             | 9.13 KB   | N/A  |
|       ├─IndexRangeScan_9(Build)  | 10.00   | 1       | cop[tikv] | table:child, index:idx_pid(pid) | time:351.2µs, loops:3, cop_task: {num: 1, max: 282.3µs, proc_keys: 0, rpc_num: 1, rpc_time: 263µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:220.2µs, loops:0}   | range:[1,1], keep order:false, stats:pseudo | N/A       | N/A  |
|       └─TableRowIDScan_10(Probe) | 10.00   | 1       | cop[tikv] | table:child                     | time:223.9µs, loops:2, cop_task: {num: 1, max: 168.8µs, proc_keys: 0, rpc_num: 1, rpc_time: 154.5µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:145.6µs, loops:0} | keep order:false, stats:pseudo              | N/A       | N/A  |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
```

## Compatibility

### Compatibility between TiDB versions

Before v6.6.0, TiDB supports the syntax of creating foreign keys, but the created foreign keys are ineffective. If you upgrade a TiDB cluster created before v6.6.0 to v6.6.0 or later, the foreign keys created before the upgrade are still ineffective. Only the foreign keys created in v6.6.0 or later versions are effective. You can use the `SHOW CREATE TABLE` statement to check whether the foreign keys are effective. The invalid foreign key has a `/* FOREIGN KEY INVALID */` comment.

```sql
mysql> SHOW CREATE TABLE child\G
***************************[ 1. row ]***************************
Table        | child
Create Table | CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE /* FOREIGN KEY INVALID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### Compatibility with MySQL

- [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) does not support foreign keys.
- When you create a foreign key without specifying a name, the name generated by TiDB is different from that generated by MySQL. For example, the foreign key name generated by TiDB is `fk_1`, `fk_2`, and `fk_3`, while the foreign key name generated by MySQL is `table_name_ibfk_1`, `table_name_ibfk_2`, and `table_name_ibfk_3`.
