---
title: ALTER RESOURCE GROUP
summary: Learn the usage of ALTER RESOURCE GROUP in TiDB.
---

# ALTER RESOURCE GROUP

The `ALTER RESOURCE GROUP` statement is used to modify the resource group in a database.

## Synopsis

```ebnf+diagram
AlterResourceGroupStmt:
   "ALTER" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList

IfNotExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName:
   Identifier

ResourceGroupOptionList:
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption:
    "RU_PER_SEC" EqOpt stringLit
|   "BURSTABLE"

```

TiDB supports the following `DirectResourceGroupOption`, where [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) is TiDB's unified abstraction unit for CPU, IO, and other system resources.

| Option     | Description                         | Example                |
|---------------|-------------------------------------|------------------------|
|`RU_PER_SEC` | Rate of RU filling per second |`RU_PER_SEC = 500` indicates that this resource group is backfilled with 500 RUs per second |

If the `BURSTABLE` attribute is set, the corresponding resource group allows the available system resources to be used exceeding the quota.

> **Note:**
> 
> The `ALTER RESOURCE GROUP` statement can only be executed when the global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) is set to `ON`.

## Examples

Create a resource group named `rg1` and modify its properties.

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1
    ->  RU_PER_SEC = 100
    ->  BURSTABLE;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+-------------+-----------+
| NAME | RU_PER_SEC  | BURSTABLE |
+------+-------------+-----------+
| rg1  |         100 |  YES       |
+------+-------------+-----------+
1 rows in set (1.30 sec)
mysql> ALTER RESOURCE GROUP rg1
    ->  RU_PER_SEC = 200;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+-------------+-----------+
| NAME | RU_PER_SEC  |  BURSTABLE |
+------+-------------+-----------+
| rg1  |         200 | NO        |
+------+-------------+-----------+
1 rows in set (1.30 sec)
```

## MySQL compatibility

MySQL also supports [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html). However, the accepted parameters are different from TiDB so that they are not compatible.

## See also

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
