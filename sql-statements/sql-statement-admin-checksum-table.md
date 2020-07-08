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

{{< copyable "sql" >}}

```sql
ADMIN CHECKSUM TABLE tbl_name [, tbl_name] ...;
```

The above statement is used to get the 64-bit checksum value of `tbl_name`. This value is obtained by calculating CRC64 of all key-value pairs (including row data and index data) in the table.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* 