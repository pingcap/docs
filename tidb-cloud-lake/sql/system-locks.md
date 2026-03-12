---
title: system.locks
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.262"/>

Contains information about the locks in the system.

See also: [SHOW LOCKS](../../10-sql-commands/00-ddl/14-transaction/show-locks.md)

```sql
SELECT * FROM system.locks;

+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
| table_id | revision | type  | status  | user | node                   | query_id                             | created_on                 | acquired_on                | extra_info |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
|       57 |     4517 | TABLE | HOLDING | root | xzi6pRbLUYasuA9QFB36m6 | d7989971-d5ec-4764-8e37-afe38ebc13e2 | 2023-12-13 09:56:47.295684 | 2023-12-13 09:56:47.310805 |            |
|       57 |     4521 | TABLE | WAITING | zzq  | xzi6pRbLUYasuA9QFB36m6 | 4bc78044-d4fc-4fe1-a5c5-ff6ab1e3e372 | 2023-12-13 09:56:48.419774 | NULL                       |            |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
```