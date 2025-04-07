---
title: CANCEL TRAFFIC JOBS
summary: An overview of the usage of CANCEL TRAFFIC JOBS for the TiDB database.
---

# CANCEL TRAFFIC JOBS

TiDB v9.0.0 introduces the `CANCEL TRAFFIC JOBS` syntax, which is used to cancel all traffic capture or replay jobs being executed by [TiProxy](/tiproxy/tiproxy-overview.md) in the cluster. This operation requires the following privileges:

- To cancel traffic capture jobs, you need the `SUPER` or [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#dynamic-privileges) privilege.
- To cancel traffic replay jobs, you need the `SUPER` or [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#dynamic-privileges) privilege.

## Synopsis

```ebnf+diagram
TrafficStmt ::=
    "CANCEL" "TRAFFIC" "JOBS"
```

## Examples

Assume that there are currently two TiProxy instances capturing traffic:

```sql
SHOW TRAFFIC JOBS;
```

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON | PARAMS                                                                     |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

Cancel the current jobs:

```sql
CANCEL TRAFFIC JOBS;
```

```
Query OK, 0 rows affected (0.13 sec)
```

Check the jobs again and it shows that the jobs have been canceled:

```sql
SHOW TRAFFIC JOBS;
```

```
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME                   | INSTANCE       | TYPE    | PROGRESS | STATUS   | FAIL_REASON      | PARAMS                                                                     |
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.10:3080 | capture | 45%      | canceled | manually stopped | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 | 2024-12-17 11:34:42.000000 | 10.1.0.11:3080 | capture | 45%      | canceled | manually stopped | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------------------------+----------------+---------+----------+----------+------------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [TiProxy traffic replay](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
