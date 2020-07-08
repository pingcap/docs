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

## `ADMIN REPAIR` statement

To overwrite the metadata of the stored table in an untrusted way in extreme cases, use `ADMIN REPAIR TABLE`:

{{< copyable "sql" >}}

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

Here “untrusted” means that you need to manually ensure that the metadata of the original table can be covered by the `CREATE TABLE STATEMENT` operation. To use this `REPAIR` statement, enable the [`repair-mode`](/tidb-configuration-file.md#repair-mode) configuration item, and make sure that the tables to be repaired are listed in the [`repair-table-list`](/tidb-configuration-file.md#repair-table-list).

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* 