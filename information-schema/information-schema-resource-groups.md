---
title: RESOURCE_GROUPS
summary: Learn the `RESOURCE_GROUPS` information_schema table.
---

# RESOURCE_GROUPS

> **Warning:**
>
> This feature is experimental and its form and usage may change in subsequent versions.

The `RESOURCE_GROUPS` table shows information about all resource groups. See [Use Resource Control to Achieve Resource Isolation](/tidb-resource-control.md).

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+------------+-------------+------+------+---------+-------+
| Field      | Type        | Null | Key  | Default | Extra |
+------------+-------------+------+------+---------+-------+
| NAME       | varchar(32) | NO   |      | NULL    |       |
| RU_PER_SEC | bigint(21)  | YES  |      | NULL    |       |
| RU_TOKENS  | bigint(21)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

## Examples

{{< copyable "sql" >}}

```sql
mysql> CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- Create the resource group rg1
Query OK, 0 rows affected (0.34 sec)
mysql> SHOW CREATE RESOURCE GROUP rg1; -- Displays the definition of the rg1 resource group.
+----------------+---------------------------------------------+
| Resource_Group | Create Resource Group                       |
+----------------+---------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 |
+----------------+---------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1';
+------+------------+-----------+-----------+
| NAME | RU_PER_SEC | RU_TOKENS | BURSTABLE |
+------+------------+-----------+-----------+
| rg1  |       1000 |    100000 | NO        |
+------+------------+-----------+-----------+

The descriptions of the columns in the `RESOURCE_GROUPS` table are as follows:

* `NAME`: the name of the resource group.
* `RU_PER_SEC`：the backfilling speed of the resource group in [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)/second.
* `RU_TOKENS`: the number of tokens left in the resource group token bucket, and 1 token is an RU.
* `BURSTABLE`: whether to allow this resource group to overuse the remaining system resources.
