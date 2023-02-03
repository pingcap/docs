---
title: RESOURCE_GROUPS
summary: Learn the `RESOURCE_GROUPS` information_schema table.
---

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
