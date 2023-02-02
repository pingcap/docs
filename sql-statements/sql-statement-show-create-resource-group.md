---
title: SHOW CREATE RESOURCE GROUP
summary: Learn the usage of SHOW CREATE RESOURCE GROUP in TiDB.
---

# SHOW CREATE RESOURCE GROUP

You can use the `SHOW CREATE RESOURCE GROUP` statement to view the current definition of a resource group.

## Synopsis

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
```

## Examples

View the current definition of the resource group `rg1` and recreate it in another TiDB cluster.

```sql
CREATE RESOURCE GROUP rg1 RRU_PER_SEC=100 WRU_PER_SEC=200;
Query OK, 0 rows affected (0.10 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1;
***************************[ 1. row ]***************************
Resource_Group        | rg1
Create Resource Group | CREATE RESOURCE GROUP `rg1` RRU_PER_SEC=100 WRU_PER_SEC=200
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension for MySQL.

## See also

* [TiDB RESOURCE CONTROL](/tidb-resource-control.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
