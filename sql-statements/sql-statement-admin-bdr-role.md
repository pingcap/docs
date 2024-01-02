---
title: ADMIN [SET|SHOW] BDR ROLE
summary: An overview of the usage of ADMIN [SET|SHOW] BDR ROLE for the TiDB database.
---

# ADMIN [SET|SHOW] BDR ROLE

- Use `ADMIN SET BDR ROLE` to set the BDR role of the cluster. Currently, you can set three BDR roles for a TiDB cluster: `PRIMARY`, `SECONDARY`, and `LOCAL_ONLY` (default). For more information about BDR roles, see [DDL Synchronization in TiCDC Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md#ddl-replication).
- Use `ADMIN SHOW BDR ROLE` to show the BDR role of the cluster.

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Synopsis

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY' | 'LOCAL_ONLY')
```

## Examples

The default BDR role of a TiDB cluster is `LOCAL_ONLY`. Run the folloiwng command to show the BDR role of the cluster.

```sql
ADMIN SHOW BDR ROLE;
```

```sql
+------------+
| BDR_ROLE   |
+------------+
| local_only |
+------------+
1 row in set (0.01 sec)
```

Run the following command to set the BDR role to `PRIMARY`.

```sql
ADMIN SET BDR ROLE PRIMARY;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
| primary  |
+----------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
