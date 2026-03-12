---
title: SHOW LOCKS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.262"/>

Provides a list of active transactions currently holding locks on tables, either for the current user across all their sessions or for all users within the Databend system. A lock is a synchronization mechanism that restricts access to shared resources, such as tables, ensuring orderly and controlled interactions among processes or threads within the Databend system to maintain data consistency and prevent conflicts. 

The operations, such as [UPDATE](../../10-dml/dml-update.md), [DELETE](../../10-dml/dml-delete-from.md), [OPTIMIZE TABLE](../01-table/60-optimize-table.md), [RECLUSTER TABLE](../06-clusterkey/dml-recluster-table.md), and [ALTER TABLE](../01-table/90-alter-table.md#column-operations), can result in table locks in the system. The table lock feature is enabled by default. In case of resource conflicts, you can examine specific details using the command. To disable this feature, execute `set enable_table_lock=0;`.

## Syntax

```sql
SHOW LOCKS [IN ACCOUNT] [WHERE <expr>]
```

| Parameter  | Description                                                                                                                                         |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| IN ACCOUNT | Displays lock information for all users within the Databend system. If omitted, the command returns locks for the current user across all sessions. |
| WHERE      | Filters locks based on the status; valid values include `HOLDING` and `WAITING`.                                                                    |

## Output

The command returns the lock information in a table with these columns:

| Column      | Description                                                                                                                                                                                                             |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| table_id    | Internal ID for the table associated with the lock.                                                                                                                                                                     |
| revision    | Revision number indicating the version of the transaction that initiated the lock. Commencing at 0, this number increases with each subsequent transaction, establishing a comprehensive order across all transactions. |
| type        | The type of lock, such as `TABLE`.                                                                                                                                                                                      |
| status      | The status of the lock, such as `HOLDING` or `WAITING`.                                                                                                                                                                 |
| user        | The user associated with the lock.                                                                                                                                                                                      |
| node        | The identifier of query node where the lock is held.                                                                                                                                                                    |
| query_id    | The query session ID related to the lock. Use it to [KILL](/sql/sql-commands/administration-cmds/kill) a query in case of dead locks or excessively prolonged lock holdings.                                                  |
| created_on  | Timestamp when the transaction that initiated the lock was created.                                                                                                                                                     |
| acquired_on | Timestamp when the lock was acquired.                                                                                                                                                                                   |
| extra_info  | Additional information related to the lock, if any.                                                                                                                                                                     |

## Examples

```sql
SHOW LOCKS IN ACCOUNT;
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
| table_id | revision | type  | status  | user | node                   | query_id                             | created_on                 | acquired_on                | extra_info |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
|       57 |     4517 | TABLE | HOLDING | root | xzi6pRbLUYasuA9QFB36m6 | d7989971-d5ec-4764-8e37-afe38ebc13e2 | 2023-12-13 09:56:47.295684 | 2023-12-13 09:56:47.310805 |            |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+

SHOW LOCKS;
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
| table_id | revision | type  | status  | user | node                   | query_id                             | created_on                 | acquired_on                | extra_info |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
|       57 |     4517 | TABLE | HOLDING | root | xzi6pRbLUYasuA9QFB36m6 | d7989971-d5ec-4764-8e37-afe38ebc13e2 | 2023-12-13 09:56:47.295684 | 2023-12-13 09:56:47.310805 |            |
|       57 |     4521 | TABLE | WAITING | zzq  | xzi6pRbLUYasuA9QFB36m6 | 4bc78044-d4fc-4fe1-a5c5-ff6ab1e3e372 | 2023-12-13 09:56:48.419774 | NULL                       |            |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+

SHOW LOCKS WHERE STATUS = 'HOLDING';
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
| table_id | revision | type  | status  | user | node                   | query_id                             | created_on                 | acquired_on                | extra_info |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
|       57 |     4517 | TABLE | HOLDING | root | xzi6pRbLUYasuA9QFB36m6 | d7989971-d5ec-4764-8e37-afe38ebc13e2 | 2023-12-13 09:56:47.295684 | 2023-12-13 09:56:47.310805 |            |
+----------+----------+-------+---------+------+------------------------+--------------------------------------+----------------------------+----------------------------+------------+
```
