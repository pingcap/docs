---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
aliases: ['/docs/dev/ticdc/troubleshoot-ticdc/']
---

# Troubleshoot TiCDC

This document introduces the common issues and errors that you might encounter when using TiCDC, and the corresponding maintenance and troubleshooting methods.

## How do I choose `start-ts` when creating a task in TiCDC?

The `start-ts` of a replication task corresponds to a Timestamp Oracle (TSO) in the upstream TiDB cluster. TiCDC requests data from this TSO in a replication task. Therefore, the `start-ts` of the replication task must meet the following requirements:

- The value of `start-ts` is larger than the `tikv_gc_safe_point` value of the current TiDB cluster. Otherwise, an error occurs when you create a task.
- Before starting a task, ensure that the downstream has all data before `start-ts`. For scenarios such as replicating data to message queues, if the data consistency between upstream and downstream is not required, you can relax this requirement according to your application need.

If you do not specify `start-ts`, or specify `start-ts` as `0`, when a replication task is started, TiCDC gets a current TSO and starts the task from this TSO.

## Why can't I replicate some tables when I create a task in TiCDC?

When you execute `cdc cli changefeed create` to create a replication task, TiCDC checks whether the upstream tables meet the [replication restrictions](/ticdc/ticdc-overview.md#restrictions). If some tables do not meet the restrictions, `some tables are not eligible to replicate` is returned with a list of ineligible tables. You can choose `Y` or `y` to continue creating the task, and all updates on these tables are automatically ignored during the replication. If you choose an input other than `Y` or `y`, the replication task is not created.

## How do I handle replication interruption?

A replication task might be interrupted in the following known scenarios:

- The downstream continues to be abnormal, and TiCDC still fails after many retries.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling method: You can resume the replication task via the HTTP interface after the downstream is back to normal.

- Replication cannot continue because of incompatible SQL statement(s) in the downstream.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling procedures:
        1. Query the status information of the replication task using the `cdc cli changefeed query` command and record the value of `checkpoint-ts`.
        2. Use the new task configuration file and add the `ignore-txn-commit-ts` parameter to skip the transaction corresponding to the specified `commit-ts`.
        3. Stop the old replication task via HTTP API. Execute `cdc cli changefeed create` to create a new task and specify the new task configuration file. Specify `checkpoint-ts` recorded in step 1 as the `start-ts` and start a new task to resume the replication.

## What is `gc-ttl` and file sorting in TiCDC?

Since v4.0.0-rc.1, PD supports external services in setting the service-level GC safepoint. Any service can register and update its GC safepoint. PD ensures that the key-value data smaller than this GC safepoint is not cleaned by GC. Enabling this feature in TiCDC ensures that the data to be consumed by TiCDC is retained in TiKV without being cleaned by GC when the replication task is unavailable or interrupted.

When starting the TiCDC server, you can specify the Time To Live (TTL) duration of GC safepoint through `gc-ttl`, which means the longest time that data is retained within the GC safepoint. This value is set by TiCDC in PD, which is 86,400 seconds by default.

If the replication task is interrupted for a long time and a large volume of unconsumed data is accumulated, Out of Memory (OOM) might occur when TiCDC is started. In this situation, you can enable the file sorting feature of TiCDC that uses system files for sorting. To enable this feature, pass `--sort-engine=file` and `--sort-dir=/path/to/sort_dir` to the `cdc cli` command when creating a replication task. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --sort-engine="file" --sort-dir="/data/cdc/sort"
```

> **Note:**
>
> TiCDC (the 4.0 version) does not support dynamically modifying the file sorting and memory sorting yet.

## How do I handle the `Error 1298: Unknown or incorrect time zone: 'UTC'` error when creating the replication task or replicating data to MySQL?

This error is returned when the downstream MySQL does not load the time zone. You can load the time zone by running [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html). After loading the time zone, you can create tasks and migrate data normally.

{{< copyable "shell-regular" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

If you use MySQL in a special cloud environment, such Aliyun RDS, and you do not have the permission to modify MySQL, you need to specify the time zone using the `--tz` parameter.

First, query the time zone used by MySQL:

{{< copyable "shell-regular" >}}

```shell
show variables like '%time_zone%';
```

```
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | CST    |
| time_zone        | SYSTEM |
+------------------+--------+
```

Specify the time zone when you create the replication task and create the TiCDC service:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/" --tz=Asia/Shanghai
```

> **Note:**
>
> In MySQL, CST refers to the China Standard Time (UTC+08:00). Usually you cannot use `CST` directly in your system, but use `Asia/Shanghai` instead.

Be cautious when you set the time zone of the TiCDC server, because the time zone will be used for the conversion of time type. It is recommended that you use the same time zone in the upstream and downstream databases, and specify the time zone using `--tz` when you start the TiCDC server.

The TiCDC server chooses its time zone in the following priority:

- TiCDC first uses the time zone specified by `--tz`.
- When the above parameter is not available, TiCDC tries to read the timezone set by the `TZ` environment variable.
- When the above environment variable is not available, TiCDC uses the default time zone of the machine.

## How do I handle the incompatibility of configuration files caused by TiCDC upgrade?

Refer to [Notes for compatibility](/ticdc/manage-ticdc.md#notes-for-compatibility).

## Does TiCDC support outputting data changes in the Canal format?

Yes. To enable Canal output, specify the protocol as `canal` in the `--sink-uri` parameter. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **Note:**
>
> * This feature is introduced in TiCDC 4.0.2.
> * TiCDC currently only supports outputting data changes in the Canal format to Kafka.

For more information, refer to [Create a replication task](/ticdc/manage-ticdc.md#create-a-replication-task).

## How do I view the latency of TiCDC replication tasks?

To view the latency of TiCDC replication tasks, use `cdc cli`. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

The expected output is as follows:

```json
[{
    "id": "4e24dde6-53c1-40b6-badf-63620e4940dc",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

* `checkpoint`: TiCDC has replicated all data before this timestamp to downstream.
* `state`: The state of the replication task:

    * `normal`: The task runs normally.
    * `stopped`: The task is stopped manually or encounters an error.
    * `removed`: The task is deleted.

> **Note:**
>
> This feature is introduced in TiCDC 4.0.3.

## How do I know whether the replication task runs normally?

You can view the state of the replication tasks by using `cdc cli`. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the output of this command, `admin-job-type` shows the state of the replication task:

* `0`: Normal.
* `1`: Paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
* `2`: Resumed. The replication task resumes from `checkpoint-ts`.
* `3`: Removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. Only the replication status is retained for later queries.

## Why does the latency from TiCDC to Kafka become larger and larger?

* Check [whether the status of the replication task is normal](#how-do-i-know-whether-the-replication-task-runs-normally).
* Adjust the following parameters of Kafka:

    * Increase `message.max.bytes` in `server.properties` to `1073741824` (1 GB).
    * Increase `replica.fetch.max.bytes` in `server.properties` to `1073741824` (1 GB).
    * Increase `fetch.message.max.bytes` in `consumer.properties` to make it larger than `message.max.bytes`.

## TiCDC 把数据同步到 Kafka 时，是把一个事务内的所有变更都写到一个消息中吗？如果不是，是根据什么划分的？
