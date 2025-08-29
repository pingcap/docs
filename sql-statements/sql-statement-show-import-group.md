---
title: SHOW IMPORT GROUP
summary: An overview of the usage of SHOW IMPORT GROUP in TiDB.
---

# SHOW IMPORT

The `SHOW IMPORT GROUP` statement is used to show the groups of IMPORT jobs created in TiDB. This statement can only show jobs created by the current user.

## Required privileges

- `SHOW IMPORT GROUPS`: if a user has the `SUPER` privilege, this statement shows all import groups in TiDB. Otherwise, this statement only shows groups created by the current user.
- `SHOW IMPORT GROUP <group-key>`: only the creator of an import group or users with the `SUPER` privilege can use this statement to view a specific import group.

## Synopsis

```ebnf+diagram
ShowImportGroupsStmt ::=
    'SHOW' 'IMPORT' 'GROUPS'

ShowImportGroupStmt ::=
    'SHOW' 'IMPORT' 'GROUP' GroupKey
```

The output fields of the `SHOW IMPORT` statement are described as follows:

| Column           | Description             |
|------------------|-------------------------|
| Group_Key        | The key of the group                  |
| Total_Jobs       | Total number of jobs in this group                  |
| Pending     | Number of pending jobs in this group                     |
| Running            | Number of running jobs in this group |
| Completed           | Number of completed jobs in this group |
| Failed | Number of failed jobs in this group  |
| Cancelled | Number of cancelled jobs in this group |
| First_Job_Create_Time   | The earliest create time of the jobs in this group |
| Last_Job_Update_Time      | The latest update time of the jobs in this group |

## Example

```sql
SHOW IMPORT GROUPS;
```

```
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
| Group_Key    | Total_Jobs | Pending | Running | Completed | Failed | Cancelled | First_Job_Create_Time      | Last_Job_Update_Time       |
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
| system_group |          1 |       0 |       1 |         0 |      0 |         0 | 2025-08-07 01:36:18.479055 | 2025-08-07 01:36:18.479055 |
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
| user_group   |          1 |       1 |       0 |         0 |      0 |         0 | 2025-08-07 01:37:26.162268 | NULL                       |
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
2 rows in set (0.01 sec)
```

```sql
SHOW IMPORT GROUP "system_group";
```

```
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
| Group_Key    | Total_Jobs | Pending | Running | Completed | Failed | Cancelled | First_Job_Create_Time      | Last_Job_Update_Time       |
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
| system_group |          1 |       0 |       1 |         0 |      0 |         0 | 2025-08-07 01:36:18.479055 | 2025-08-07 01:36:18.479055 |
+--------------+------------+---------+---------+-----------+--------+-----------+----------------------------+----------------------------+
1 row in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
