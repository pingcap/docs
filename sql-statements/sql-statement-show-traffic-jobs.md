---
title: SHOW TRAFFIC JOBS
summary: An overview of the usage of SHOW TRAFFIC JOBS for the TiDB database.
---

# SHOW TRAFFIC JOBS

TiDB v9.0.0 introduces the `SHOW TRAFFIC JOBS` syntax, which is used to show all traffic capture or replay jobs executed by TiProxy in the cluster. Each row represents a job of a TiProxy instance. Each TiProxy instance saves at most the 10 most recent jobs.

The shown results vary depending on the privileges the current user has.

- If the user has the [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#dynamic-privileges) privilege, this statement shows traffic capture jobs.
- If the user has the [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#dynamic-privileges) privilege, this statement shows traffic replay jobs.
- If the user has the `SUPER` privilege or both above privileges, this statement shows both traffic capture and traffic replay jobs.

The `SHOW TRAFFIC JOBS` statement returns the following columns:

| Column name | Description   |
| :-------- | :------------- |
| `START_TIME` | The start time of the job |
| `END_TIME` | The end time if the job has finished, otherwise it is empty |
| `INSTANCE` | The address of the TiProxy instance |
| `TYPE` | The job type. `capture` indicates a traffic capture job, `replay` indicates a traffic replay job |
| `PROGRESS` | The completion percentage of the job |
| `STATUS` | The current status of the job. `running` means it is running, `done` means it is completed normally, and `canceled` means the job failed |
| `FAIL_REASON` | If the job fails, this column contains the reason for the failure, otherwise it is empty. For example, `manually stopped` means the user manually canceled the job by executing `CANCEL TRAFFIC JOBS` |

## Synopsis

```ebnf+diagram
TrafficStmt ::=
    "SHOW" "TRAFFIC" "JOBS"
```

## Examples

Show the traffic capture or replay jobs:

```sql
SHOW TRAFFIC JOBS
```

The following output example shows that two TiProxy instances are capturing traffic, and the progress is 45% for both:

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON |
+----------------------------+----------+----------------+---------+----------+---------+-------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             |
+----------------------------+----------+----------------+---------+----------+---------+-------------+
2 rows in set (0.01 sec)
```

The following output example shows that the traffic replay jobs of two TiProxy instances were manually canceled:

```
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+
| START_TIME                 | END_TIME                   | INSTANCE       | TYPE   | PROGRESS | STATUS   | FAIL_REASON      |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.10:3080 | replay | 70%      | canceled | manually stopped |
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:43.000000 | 10.1.0.11:3080 | replay | 69%      | canceled | manually stopped |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+
2 rows in set (0.01 sec)
```

## MySQL compatibility

The `SHOW TRAFFIC JOBS` syntax is TiDB-specific and not compatible with MySQL.

## See also

* [TiProxy traffic replay](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
