---
title: ADMIN CHECKSUM TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN CHECKSUM TABLE

The `ADMIN CHECKSUM TABLE` statement calculates a CRC64 checksum for the data and indexes of a table.

<CustomContent platform="tidb">

The [checksum](/tidb-lightning/tidb-lightning-glossary.md#checksum) is calculated based on table data and properties such as `table_id`. This means that two tables with the same data but different `table_id` values will get different checksums.

After importing a table using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md), [TiDB Data Migration](/dm/dm-overview.md), or [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md), `ADMIN CHECKSUM TABLE <table>` is executed by default to validate data integrity.

</CustomContent>

<CustomContent platform="tidb-cloud">

The [checksum](https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#checksum) is calculated over the table data and properties like the `table_id`. This means that two tables with the same data but different `table_id` values will get different checksums.

After importing a table using [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md), `ADMIN CHECKSUM TABLE <table>` is executed by default to validate data integrity.

</CustomContent>

## Synopsis

```ebnf+diagram
AdminChecksumTableStmt ::=
    'ADMIN' 'CHECKSUM' 'TABLE' TableNameList

TableNameList ::=
    TableName ( ',' TableName )*
```

## Examples

Create table `t1`:

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

Insert some data into `t1`:

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

Calculate the checksum for `t1`:

```sql
ADMIN CHECKSUM TABLE t1;
```

The output is as follows:

```sql
+---------+------------+----------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor   | Total_kvs | Total_bytes |
+---------+------------+----------------------+-----------+-------------+
| test    | t1         | 10909174369497628533 |         3 |          75 |
+---------+------------+----------------------+-----------+-------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
