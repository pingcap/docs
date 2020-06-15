---
title: SHUTDOWN
summary: Overview of the use of SHUTDOWN in the TiDB database.
category: reference
---

# SHUTDOWN

The `SHUTDOWN` statement is used to perform a shutdown operation in TiDB. Execution of the `SHUTDOWN` statement requires the user to have `SHUTDOWN privilege`.

## Synopsis

**Statement:**

![Statement](/media/sqlgram/ShutdownStmt.png)

## Examples

{{< copyable "sql" >}}

```sql
SHUTDOWN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

> **Attention:**
>
> Since TiDB is a distributed database, the shutdown operation in TiDB stops the client-connected TiDB instance, not the entire TiDB cluster.

The `SHUTDOWN` statement is partly compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.
