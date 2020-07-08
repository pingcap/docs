---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN

TODO

## Synopsis

TODO

## Examples

## `ADMIN CHECK` related statement

To check the consistency of all the data and corresponding indexes in the `tbl_name` table, use `ADMIN CHECK TABLE`:

{{< copyable "sql" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...;
```

If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table. If the consistency check is passed, an empty result is returned; otherwise, an error message is returned indicating that the data is inconsistent.

{{< copyable "sql" >}}

```sql
ADMIN CHECK INDEX tbl_name idx_name (lower_val, upper_val) [, (lower_val, upper_val)] ...;
```

The above statement is used to check the consistency of the column data and index data corresponding to the `idx_name` index in the `tbl_name` table, with the data range (to be checked) specified. If the consistency check is passed, an empty result is returned. Otherwise, an error message is returned indicating that the data is inconsistent.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* 