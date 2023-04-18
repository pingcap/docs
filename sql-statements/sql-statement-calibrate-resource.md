---
title: CALIBRATE RESOURCE
summary: An overview of the usage of CALIBRATE RESOURCE for the TiDB database.
---

# `CALIBRATE RESOURCE`

The `CALIBRATE RESOURCE` statement is used to estimate and output the ['Request Unit (RU)`](/tidb-resource-control#what-is-request-unit-ru) capacity of the current cluster. TiDB provides two methods for estimation:

- Method 1: view the capacity within a specified time window depending on the actual workload. The following constraints apply to improve the accuracy of the estimation:
    - The time window ranges from 10 minutes to 24 hours.
    - In the specified time window, if the CPU utilization of TiDB and TiKV is too low, you cannot estimate the capacity.

- Method 2: specify `WORKLOAD` to view the RU capacity. The default value is `TPCC`. The following options are currently supported:

    - OLTP_READ_WRITE
    - OLTP_READ_ONLY
    - OLTP_WRITE_ONLY
    - TPCC

> **Note:**
>
> The RU capacity of a cluster varies with the topology of the cluster and the hardware and software configuration of each component. The actual RU that each cluster can consume is also related to the actual workload. The estimated value in Method 2 is for reference only and might differ from the actual maximum value. It is recommended to use Method 1 for estimation based on the actual workload.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Synopsis

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' WorkloadOption

WorkloadOption ::=
( 'WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY') )
| ( 'START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)?

```

## Privileges

To execute this command, you need the following configuration and privileges:

- You have enabled [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660).
- You have `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.
- You have the `SELECT` privilege for all tables in the `METRICS_SCHEMA` schema.

## Examples

Specify the start time `START_TIME` and the time window `DURATION` to view the RU capacity according to the actual workload.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '20m';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

Specify the start time `START_TIME` and the end time `END_TIME` to view the RU capacity according to the actual workload.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' END_TIME '2023-04-18 08:20:00';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

When the time window range `DURATION` does not fall between 10 minutes and 24 hours, an alert occurs.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '25h';
ERROR 1105 (HY000): the duration of calibration is too long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '9m';
ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
```

When the workload within the time window is too low, an alert occurs.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead
```

Specify `WORKLOAD` to view the RU capacity. The default value is `TPCC`.

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 190470 |
+-------+
1 row in set (0.01 sec)

CALIBRATE RESOURCE WORKLOAD OLTP_WRITE_ONLY;
+-------+
| QUOTA |
+-------+
| 27444 |
+-------+
1 row in set (0.01 sec)
```
