---
title: ALTER RESOURCE GROUP
summary: Learn the usage of ALTER RESOURCE GROUP in TiDB.
---

# ALTER RESOURCE GROUP

The `ALTER RESOURCE GROUP` statement is used to modify the resource group in a database.

## Synopsis

```ebnf+diagram
AlterResourceGroupStmt:
   "ALTER" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList BurstableOption

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

ResourceGroupName:
   Identifier

ResourceGroupOptionList:
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption:
    "RRU_PER_SEC" EqOpt stringLit
|   "WRU_PER_SEC" EqOpt stringLit

BurstableOption ::=
    ("BURSTABLE")?

```

TiDB supports the following `DirectResourceGroupOption`, where [RU (Resource Unit)](/tidb-RU.md) is TiDB's unified abstraction unit for CPU, IO, and other system resources.

| Parameter     | Description                         | Example                |
|---------------|-------------------------------------|------------------------|
|`RRU_PER_SEC`  | Quota of RU read per second         |`RRU_PER_SEC = 500`     |
|`WRU_PER_SEC`  | Quota of RU write per second        |`WRU_PER_SEC = 300`     |

If the `BURSTABLE` attribute is set, the corresponding resource group allows the system resources to be used exceeding the quota if the system resources are sufficient.

> **Note:**
> 
> The `ALTER RESOURCE GROUP` statement can only be executed when the global variable [`tidb_enable_resource_group`](/system-variables.md#tidb_enable_resource_control-new-in-v660) is set to `ON`.

## Examples

Create a resource group named `rg1` and modify its properties.

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1
    ->  RRU_PER_SEC = 500
    ->  WRU_PER_SEC = 300
    ->  BURSTABLE
    -> ;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
| rg1  |   tenancy    | {"RRU_PER_SEC": 500, "WRU_PER_SEC": 300, "BURSTABLE": true} |
+------+--------------+---------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ALTER RESOURCE GROUP IF NOT EXISTS rg1
    ->  RRU_PER_SEC = 600
    ->  WRU_PER_SEC = 400
    -> ;
Query OK, 0 rows affected (0.09 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
| rg1  |   tenancy    | {"RRU_PER_SEC": 600, "WRU_PER_SEC": 400, "BURSTABLE": false} |
+------+--------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

MySQL also supports [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html). However, the accepted parameters are different from TiDB so that they are not compatible.

## See also

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [RU](/tidb-RU.md)
