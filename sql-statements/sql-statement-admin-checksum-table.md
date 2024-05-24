---
title: ADMIN CHECKSUM TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN CHECKSUM TABLE

The `ADMIN CHECKSUM TABLE` statement calculates a CRC64 checksum for the data and indexes of a table. This statement is used by programs such as TiDB Lightning to ensure that import operations have completed successfully.

The checksum will likely be different between different servers and if the table is re-created.

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
