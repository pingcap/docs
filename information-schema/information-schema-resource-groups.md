---
title: RESOURCE_GROUPS
summary: Learn the `RESOURCE_GROUPS` information_schema table.
---

The `RESOURCE_GROUPS` table shows information about all resource groups. See [Resource Conctrol in TiDB](/tidb-resource-control.md).

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+-----------------+-------------+------+------+---------+-------+
| Field           | Type        | Null | Key  | Default | Extra |
+-----------------+-------------+------+------+---------+-------+
| NAME            | varchar(32) | NO   |      | NULL    |       |
| MODE            | varchar(12) | NO   |      | NULL    |       |
| RRU             | bigint(21)  | YES  |      | NULL    |       |
| RRU_TOKEN       | bigint(21)  | YES  |      | NULL    |       |
| WRU             | bigint(21)  | YES  |      | NULL    |       |
| WRU_TOKEN       | bigint(21)  | YES  |      | NULL    |       |
| CPU             | bigint(21)  | YES  |      | NULL    |       |
| READ_BANDWIDTH  | bigint(21)  | YES  |      | NULL    |       |
| WRITE_BANDWIDTH | bigint(21)  | YES  |      | NULL    |       |
+-----------------+-------------+------+------+---------+-------+
9 rows in set (0.08 sec)
```

## Examples

{{< copyable "sql" >}}

```sql
mysql> CREATE RESOURCE GROUP rg1 RRU_PER_SEC=1000 WRU_PER_SEC=2000 ; -- Use RU_MODE to create the resource group rg1
Query OK, 0 rows affected (0.34 sec)
mysql> SHOW CREATE RESOURCE GROUP rg1; -- Displays the definition of the rg1 resource group.
+----------------+------------------------------------------------------------------+
| Resource_Group | Create Resource Group                                            |
+----------------+------------------------------------------------------------------+
| rg1         | CREATE RESOURCE GROUP `rg1` RRU_PER_SEC=1000 WRU_PER_SEC=2000 |
+----------------+------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.placement_policies WHERE NAME = 'rg1'; -- Displays the runtime status of the resource group rg1.
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
| NAME   | MODE    | RRU  | RRU_TOKEN | WRU  | WRU_TOKEN | CPU  | READ_BANDWIDTH | WRITE_BANDWIDTH |
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
| rg1 | RU_MODE | 1000 |    168999 | 2000 |    249999 | NULL |           NULL |            NULL |
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
1 row in set (0.02 sec)
```

```sql
mysql> CREATE RESOURCE GROUP rg2 CPU="8" IO_READ_BANDWIDTH="1000Mi" IO_WRITE_BANDWIDTH="1000Mi"; -- Use RAW_MODE to create the resource group rg2
Query OK, 0 rows affected (0.20 sec)
mysql> show create resource group rg2; -- Displays the definition of the rg2 resource group.
+----------------+-----------------------------------------------------------------------------------------------+
| Resource_Group | Create Resource Group                                                                         |
+----------------+-----------------------------------------------------------------------------------------------+
| rg2         | CREATE RESOURCE GROUP `rg2` CPU="8" IO_READ_BANDWIDTH="1000Mi" IO_WRITE_BANDWIDTH="1000Mi" |
+----------------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg2'; -- Displays the runtime status of the resource group rg2.
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
| NAME   | MODE     | RRU  | RRU_TOKEN | WRU  | WRU_TOKEN | CPU  | READ_BANDWIDTH | WRITE_BANDWIDTH |
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
| rg2 | RAW_MODE | NULL |      NULL | NULL |      NULL | 8000 |     1048576000 |      1048576000 |
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
1 row in set (0.00 sec)
```
