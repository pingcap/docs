---
title: CREATE RESOURCE GROUP
summary: Learn the usage of CREATE RESOURCE GROUP in TiDB.
---

# CREATE RESOURCE GROUP

You can use the `CREATE RESOURCE GROUP` statement to create a resource group in the currently selected database.

## Synopsis

```ebnf+diagram
CreateResourceGroupStmt:
   "CREATE" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList BurstableOption

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

ResourceGroupName:
   Identifier

ResourceGroupOptionList:
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption:
    "RU_PER_SEC" EqOpt stringLit

BurstableOption ::=
    ("BURSTABLE")?

```

The resource group name parameter (`ResourceGroupName`) is globally unique and cannot be duplicated.

TiDB supports the following `DirectResourceGroupOption`, where [RU (Request Unit)](/tidb-RU.md) is TiDB's unified abstraction unit for CPU, IO, and other system resources.

| Option     | Description                         | Example                |
|---------------|-------------------------------------|------------------------|
|`RU_PER_SEC`  | Rate of RU filling per second   |`RU_PER_SEC = 500` indicates that this resource group is backfilled with 500 RU per second    |

If the `BURSTABLE` attribute is set, the corresponding resource group allows the system resources to be used exceeding the quota.

> **Note:**
>
> The `CREATE RESOURCE GROUP` statement can only be executed when the global variable [`tidb_enable_resource_group`](/system-variables.md#tidb_enable_resource_control-new-in-v660) is set to `ON`.

## Examples

Create two resource groups `rg1` and `rg2`.

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1
    ->  RU_PER_SEC = 100
    ->  BURSTABLE;
Query OK, 0 rows affected (0.08 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg2
    ->  RU_PER_SEC = 200
    ->  BURSTABLE;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1' or NAME = 'rg2';
+------+-------------+-----------+-----------+
| NAME | RU_PER_SEC  | RU_TOKENS | BURSTABLE |
+------+-------------+-----------+-----------+
| rg1  |         100 |    165135 | YES       |
| rg2  |         200 |    157158 | NO        |
+------+-------------+-----------+-----------+
2 rows in set (1.30 sec)
```

## MySQL compatibility

MySQL also supports [CREATE RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html). However, the accepted parameters are different from TiDB so that they are not compatible.

## See also

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [RU](/tidb-RU.md)
