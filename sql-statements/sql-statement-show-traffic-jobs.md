---
title: SHOW TRAFFIC JOBS
summary: An overview of the usage of SHOW TRAFFIC JOBS for the TiDB database.
---

# SHOW TRAFFIC JOBS

TiDB v9.0.0 introduces the `SHOW TRAFFIC JOBS` syntax, which is used to show all traffic capture or replay jobs executed by [TiProxy](/tiproxy/tiproxy-overview.md) in the cluster. In the output, each row represents a job of a TiProxy instance. Each TiProxy instance stores up to 10 most recent jobs.

The shown results vary depending on the privileges the current user has.

- A user with the [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#dynamic-privileges) privilege can view traffic capture jobs.
- A user with the [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#dynamic-privileges) privilege can view traffic replay jobs.
- A user with the `SUPER` privilege or both preceding privileges can view both traffic capture and traffic replay jobs at the same time.

The `SHOW TRAFFIC JOBS` statement returns the following columns:

| Column name | Description   |
| :-------- | :------------- |
| `START_TIME` | The start time of the job |
| `END_TIME` | The end time if the job has completed. Otherwise, it is empty. |
| `INSTANCE` | The address of the TiProxy instance |
| `TYPE` | The job type. `capture` indicates a traffic capture job, `replay` indicates a traffic replay job |
| `PROGRESS` | The completion percentage of the job |
| `STATUS` | The current status of the job. `running` indicates in progress, `done` indicates normal completion, and `canceled` indicates job failure. |
| `FAIL_REASON` | If the job fails, this column contains the reason for the failure. Otherwise, it is empty. For example, `manually stopped` means the user manually canceled the job by executing `CANCEL TRAFFIC JOBS`. |
| `PARAMS` | The parameters of the job |

## Synopsis

```ebnf+diagram
TrafficStmt ::=
    "SHOW" "TRAFFIC" "JOBS"
```

## Examples

Show the traffic capture or replay jobs:

```sql
SHOW TRAFFIC JOBS;
```

The following output example shows that two TiProxy instances are capturing traffic, and the progress is 45% for both:

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON | PARAMS                                                                     |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

The following output example shows that the traffic replay jobs of two TiProxy instances are manually canceled:

```
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
| START_TIME                 | END_TIME                   | INSTANCE       | TYPE   | PROGRESS | STATUS   | FAIL_REASON      | PARAMS                                                             |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.10:3080 | replay | 70%      | canceled | manually stopped | INPUT="/tmp/traffic", USER="root", SPEED=0.000000, READ_ONLY=false |
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:43.000000 | 10.1.0.11:3080 | replay | 69%      | canceled | manually stopped | INPUT="/tmp/traffic", USER="root", SPEED=0.000000, READ_ONLY=false |
+----------------------------+----------------------------+----------------+--------+----------+----------+------------------+--------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [TiProxy traffic replay](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
