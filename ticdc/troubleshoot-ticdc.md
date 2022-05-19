---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
aliases: ['/docs/dev/ticdc/troubleshoot-ticdc/']
---

# Troubleshoot TiCDC

This document introduces the common issues and errors that you might encounter when using TiCDC, and the corresponding maintenance and troubleshooting methods.

> **Note:**
>
> In this document, the PD address specified in `cdc cli` commands is `--pd=http://10.0.10.25:2379`. When you use the command, replace the address with your actual PD address.

## How do I choose `start-ts` when creating a task in TiCDC?

The `start-ts` of a replication task corresponds to a Timestamp Oracle (TSO) in the upstream TiDB cluster. TiCDC requests data from this TSO in a replication task. Therefore, the `start-ts` of the replication task must meet the following requirements:

- The value of `start-ts` is larger than the `tikv_gc_safe_point` value of the current TiDB cluster. Otherwise, an error occurs when you create a task.
- Before starting a task, ensure that the downstream has all data before `start-ts`. For scenarios such as replicating data to message queues, if the data consistency between upstream and downstream is not required, you can relax this requirement according to your application need.

If you do not specify `start-ts`, or specify `start-ts` as `0`, when a replication task is started, TiCDC gets a current TSO and starts the task from this TSO.

## Why can't some tables be replicated when I create a task in TiCDC?

When you execute `cdc cli changefeed create` to create a replication task, TiCDC checks whether the upstream tables meet the [replication restrictions](/ticdc/ticdc-overview.md#restrictions). If some tables do not meet the restrictions, `some tables are not eligible to replicate` is returned with a list of ineligible tables. You can choose `Y` or `y` to continue creating the task, and all updates on these tables are automatically ignored during the replication. If you choose an input other than `Y` or `y`, the replication task is not created.

## How do I view the state of TiCDC replication tasks?

To view the status of TiCDC replication tasks, use `cdc cli`. For example:

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
* `state`: The state of this replication task:
    * `normal`: The task runs normally.
    * `stopped`: The task is stopped manually or encounters an error. 
    * `removed`: The task is removed. 

> **Note:**
>
> This feature is introduced in TiCDC 4.0.3.

## TiCDC replication interruptions

### How do I know whether a TiCDC replication task is interrupted?

- Check the `changefeed checkpoint` monitoring metric of the replication task (choose the right `changefeed id`) in the Grafana dashboard. If the metric value stays unchanged, or the `checkpoint lag` metric keeps increasing, the replication task might be interrupted.
- Check the `exit error count` monitoring metric. If the metric value is greater than `0`, an error has occurred in the replication task.
- Execute `cdc cli changefeed list` and `cdc cli changefeed query` to check the status of the replication task. `stopped` means the task has stopped, and the `error` item provides the detailed error message. After the error occurs, you can search `error on running processor` in the TiCDC server log to see the error stack for troubleshooting.
- In some extreme cases, the TiCDC service is restarted. You can search the `FATAL` level log in the TiCDC server log for troubleshooting.

### How do I know whether the replication task is stopped manually?

You can know whether the replication task is stopped manually by executing `cdc cli`. For example: 

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the output of the above command, `admin-job-type` shows the state of this replication task:

* `0`: In progress, which means that the task is not stopped manually.
* `1`: Paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
* `2`: Resumed. The replication task resumes from `checkpoint-ts`.
* `3`: Removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. The replication status is retained only for later queries.

### How do I handle replication interruptions?

A replication task might be interrupted in the following known scenarios:

- The downstream continues to be abnormal, and TiCDC still fails after many retries.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.

    - Handling method: You can resume the replication task via the HTTP interface after the downstream is back to normal.

- Replication cannot continue because of incompatible SQL statement(s) in the downstream.

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling procedures:
        1. Query the status information of the replication task using the `cdc cli changefeed query` command and record the value of `checkpoint-ts`.
        2. Use the new task configuration file and add the `ignore-txn-start-ts` parameter to skip the transaction corresponding to the specified `start-ts`.
        3. Stop the old replication task via HTTP API. Execute `cdc cli changefeed create` to create a new task and specify the new task configuration file. Specify `checkpoint-ts` recorded in step 1 as the `start-ts` and start a new task to resume the replication.

- In TiCDC v4.0.13 and earlier versions, when TiCDC replicates the partitioned table, it might encounter an error that leads to replication interruption. 

    - In this scenario, TiCDC saves the task information. Because TiCDC has set the service GC safepoint in PD, the data after the task checkpoint is not cleaned by TiKV GC within the valid period of `gc-ttl`.
    - Handling procedures:
        1. Pause the replication task by executing `cdc cli changefeed pause -c <changefeed-id>`. 
        2. Wait for about one munite, and then resume the replication task by executing `cdc cli changefeed resume -c <changefeed-id>`.

### What should I do to handle the OOM that occurs after TiCDC is restarted after a task interruption?

- Update your TiDB cluster and TiCDC cluster to the latest versions. The OOM problem has already been resolved in **v4.0.14 and later v4.0 versions, v5.0.2 and later v5.0 versions, and the latest versions**. 

- In the above updated versions, you can enable the Unified Sorter to help you sort data in the disk when the system memory is insufficient. To enable this function, you can pass `--sort-engine=unified` to the `cdc cli` command when creating a replication task. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed update -c <changefeed-id> --sort-engine="unified" --pd=http://10.0.10.25:2379
```

If you fail to update your cluster to the above new versions, you can still enable Unified Sorter in **previous versions**. You can pass `--sort-engine=unified` and `--sort-dir=/path/to/sort_dir` to the `cdc cli` command when creating a replication task. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed update -c <changefeed-id> --sort-engine="unified" --sort-dir="/data/cdc/sort" --pd=http://10.0.10.25:2379
```

> **Note:**
>
> + Since v4.0.9, TiCDC supports the unified sorter engine.
> + TiCDC (the 4.0 version) does not support dynamically modifying the sorting engine yet. Make sure that the changefeed has stopped before modifying the sorter settings.
> + `sort-dir` has different behaviors in different versions. Refer to [compatibility notes for`sort-dir` and `data-dir`](/ticdc/ticdc-overview.md#compatibility-notes-for-sort-dir-and-data-dir), and configure it with caution. 
> + Currently, the unified sorter is an experimental feature. When the number of tables is too large (>=100), the unified sorter might cause performance issues and affect replication throughput. Therefore, it is not recommended to use it in a production environment. Before you enable the unified sorter, make sure that the machine of each TiCDC node has enough disk capacity. If the total size of unprocessed data changes might exceed 1 TB, it is not recommend to use TiCDC for replication.

## What is `gc-ttl` in TiCDC?

Since v4.0.0-rc.1, PD supports external services in setting the service-level GC safepoint. Any service can register and update its GC safepoint. PD ensures that the key-value data later than this GC safepoint is not cleaned by GC.

When the replication task is unavailable or interrupted, this feature ensures that the data to be consumed by TiCDC is retained in TiKV without being cleaned by GC.

When starting the TiCDC server, you can specify the Time To Live (TTL) duration of GC safepoint by configuring `gc-ttl`. You can also [use TiUP to modify](/ticdc/manage-ticdc.md#modify-ticdc-configuration-using-tiup) `gc-ttl`. The default value is 24 hours. In TiCDC, this value means:

- The maximum time the GC safepoint is retained at the PD after the TiCDC service is stopped.
- The maximum time a replication task can be suspended after the task is interrupted or manually stopped. If the time for a suspended replication task is longer than the value set by `gc-ttl`, the replication task enters the `failed` status, cannot be resumed, and cannot continue to affect the progress of the GC safepoint.

The second behavior above is introduced in TiCDC v4.0.13 and later versions. The purpose is to prevent a replication task in TiCDC from suspending for too long, causing the GC safepoint of the upstream TiKV cluster not to continue for a long time and retaining too many outdated data versions, thus affecting the performance of the upstream cluster.

> **Note:**
>
> In some scenarios, for example, when you use TiCDC for incremental replication after full replication with Dumpling/BR, the default 24 hours of `gc-ttl` may not be sufficient. You need to specify an appropriate value for `gc-ttl` when you start the TiCDC server.

## What is the complete behavior of TiCDC garbage collection (GC) safepoint?

If a replication task starts after the TiCDC service starts, the TiCDC owner updates the PD service GC safepoint with the smallest value of `checkpoint-ts` among all replication tasks. The service GC safepoint ensures that TiCDC does not delete data generated at that time and after that time. If the replication task is interrupted, or manually stopped, the `checkpoint-ts` of this task does not change. Meanwhile, PD's corresponding service GC safepoint is not updated either.

If the replication task is suspended longer than the time specified by `gc-ttl`, the replication task enters the `failed` status and cannot be resumed. The PD corresponding service GC safepoint will continue.

The Time-To-Live (TTL) that TiCDC sets for a service GC safepoint is 24 hours, which means that the GC mechanism does not delete any data if the TiCDC service can be recovered within 24 hours after it is interrupted.

## How do I handle the `Error 1298: Unknown or incorrect time zone: 'UTC'` error when creating the replication task or replicating data to MySQL?

This error is returned when the downstream MySQL does not load the time zone. You can load the time zone by running [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html). After loading the time zone, you can create tasks and replicate data normally.

{{< copyable "shell-regular" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

If the output of the command above is similar to the following one, the import is successful:

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

If the downstream is a special MySQL environment (a public cloud RDS or some MySQL derivative versions) and importing the time zone using the above method fails, you need to specify the MySQL time zone of the downstream using the `time-zone` parameter in `sink-uri`. You can first query the time zone used by MySQL:

1. Query the time zone used by MySQL:

    {{< copyable "sql" >}}

    ```sql
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

2. Specify the time zone when you create the replication task and create the TiCDC service:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/?time-zone=CST" --pd=http://10.0.10.25:2379
    ```

    > **Note:**
    >
    > CST might be an abbreviation for the following four different time zones:
    >
    > + Central Standard Time (USA) UT-6:00
    > + Central Standard Time (Australia) UT+9:30
    > + China Standard Time UT+8:00
    > + Cuba Standard Time UT-4:00
    >
    > In China, CST usually stands for China Standard Time.

## How to understand the relationship between the TiCDC time zone and the time zones of the upstream/downstream databases?

||Upstream time zone| TiCDC time zone|Downstream time zone|
| :-: | :-: | :-: | :-: |
| Configuration method | See [Time Zone Support](/configure-time-zone.md) | Configured using the `--tz` parameter when you start the TiCDC server |  Configured using the `time-zone` parameter in `sink-uri` |
| Description | The time zone of the upstream TiDB, which affects DML operations of the timestamp type and DDL operations related to timestamp type columns.| TiCDC assumes that the upstream TiDB's time zone is the same as the TiCDC time zone configuration, and performs related operations on the timestamp column.| The downstream MySQL processes the timestamp in the DML and DDL operations according to the downstream time zone setting.|

 > **Note:**
 >
 > Be careful when you set the time zone of the TiCDC server, because this time zone is used for converting the time type. Keep the upstream time zone, TiCDC time zone, and the downstream time zone consistent. The TiCDC server chooses its time zone in the following priority:
 >
 > - TiCDC first uses the time zone specified using `--tz`.
 > - When `--tz` is not available, TiCDC tries to read the time zone set using the `TZ` environment variable.
 > - When the `TZ` environment variable is not available, TiCDC uses the default time zone of the machine.

## What is the default behavior of TiCDC if I create a replication task without specifying the configuration file in `--config`?

If you use the `cdc cli changefeed create` command without specifying the `-config` parameter, TiCDC creates the replication task in the following default behaviors:

* Replicates all tables except system tables
* Enables the Old Value feature
* Skips replicating tables that do not contain [valid indexes](/ticdc/ticdc-overview.md#restrictions)

## How do I handle the incompatibility issue of configuration files caused by TiCDC upgrade?

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
> * TiCDC currently supports outputting data changes in the Canal format only to MQ sinks such as Kafka and Pulsar.

For more information, refer to [Create a replication task](/ticdc/manage-ticdc.md#create-a-replication-task).

## Why does the latency from TiCDC to Kafka become higher and higher?

* Check [how do I view the state of TiCDC replication tasks](#how-do-i-view-the-state-of-ticdc-replication-tasks).
* Adjust the following parameters of Kafka:

    * Increase the `message.max.bytes` value in `server.properties` to `1073741824` (1 GB).
    * Increase the `replica.fetch.max.bytes` value in `server.properties` to `1073741824` (1 GB).
    * Increase the `fetch.message.max.bytes` value in `consumer.properties` to make it larger than the `message.max.bytes` value.

## When TiCDC replicates data to Kafka, does it write all the changes in a transaction into one message? If not, on what basis does it divide the changes?

No. According to the different distribution strategies configured, TiCDC divides the changes on different bases, including `default`, `row id`, `table`, and `ts`.

For more information, refer to [Replication task configuration file](/ticdc/manage-ticdc.md#task-configuration-file).

## When TiCDC replicates data to Kafka, can I control the maximum size of a single message in TiDB?

Yes. You can set the `max-message-bytes` parameter to control the maximum size of data sent to the Kafka broker each time (optional, `10MB` by default). You can also set `max-batch-size` to specify the maximum number of change records in each Kafka message. Currently, the setting only takes effect when Kafka's `protocol` is `open-protocol` (optional, `16` by default).

## When TiCDC replicates data to Kafka, does a message contain multiple types of data changes?

Yes. A single message might contain multiple `update`s or `delete`s, and `update` and `delete` might co-exist.

## When TiCDC replicates data to Kafka, how do I view the timestamp, table name, and schema name in the output of TiCDC Open Protocol?

The information is included in the key of Kafka messages. For example:

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

For more information, refer to [TiCDC Open Protocol event format](/ticdc/ticdc-open-protocol.md#event-format).

## When TiCDC replicates data to Kafka, how do I know the timestamp of the data changes in a message?

You can get the unix timestamp by moving `ts` in the key of the Kafka message by 18 bits to the right.

## How does TiCDC Open Protocol represent `null`?

In TiCDC Open Protocol, the type code `6` represents `null`.

| Type | Code | Output Example | Note |
|:--|:--|:--|:--|
| Null | 6 | `{"t":6,"v":null}` | |

For more information, refer to [TiCDC Open Protocol column type code](/ticdc/ticdc-open-protocol.md#column-type-code).

## The `start-ts` timestamp of the TiCDC task is quite different from the current time. During the execution of this task, replication is interrupted and an error `[CDC:ErrBufferReachLimit]` occurs

Since v4.0.9, you can try to enable the unified sorter feature in your replication task, or use the BR tool for an incremental backup and restore, and then start the TiCDC replication task from a new time.

## How can I tell if a Row Changed Event of TiCDC Open Protocol is an `INSERT` event or an `UPDATE` event?

If the Old Value feature is not enabled, you cannot tell whether a Row Changed Event of TiCDC Open Protocol is an `INSERT` event or an `UPDATE` event. If the feature is enabled, you can determine the event type by the fields it contains:

* `UPDATE` event contains both `"p"` and `"u"` fields
* `INSERT` event only contains the `"u"` field
* `DELETE` event only contains the `"d"` field

For more information, refer to [Open protocol Row Changed Event format](/ticdc/ticdc-open-protocol.md#row-changed-event).

## How much PD storage does TiCDC use?

TiCDC uses etcd in PD to store and regularly update the metadata. Because the time interval between the MVCC of etcd and PD's default compaction is one hour, the amount of PD storage that TiCDC uses is proportional to the amount of metadata versions generated within this hour. However, in v4.0.5, v4.0.6, and v4.0.7, TiCDC has a problem of frequent writing, so if there are 1000 tables created or scheduled in an hour, it then takes up all the etcd storage and returns the `etcdserver: mvcc: database space exceeded` error. You need to clean up the etcd storage after getting this error. See [etcd maintaince space-quota](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota) for details. It is recommended to upgrade your cluster to v4.0.9 or later versions.

## Does TiCDC support replicating large transactions? Is there any risk?

TiCDC provides partial support for large transactions (more than 5 GB in size). Depending on different scenarios, the following risks might exist:

- When TiCDC's internal processing capacity is insufficient, the replication task error `ErrBufferReachLimit` might occur.
- When TiCDC's internal processing capacity is insufficient or the throughput capacity of TiCDC's downstream is insufficient, out of memory (OOM) might occur.

If you encounter an error above, it is recommended to use BR to restore the incremental data of large transactions. The detailed operations are as follows:

1. Record the `checkpoint-ts` of the changefeed that is terminated due to large transactions, use this TSO as the `--lastbackupts` of the BR incremental backup, and execute [incremental data backup](/br/use-br-command-line-tool.md#back-up-incremental-data).
2. After backing up the incremental data, you can find a log record similar to `["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]` in the BR log output. Record the `BackupTS` in this log.
3. [Restore the incremental data](/br/use-br-command-line-tool.md#restore-incremental-data).
4. Create a new changefeed and start the replication task from `BackupTS`.
5. Delete the old changefeed.

## When the downstream of a changefeed is a database similar to MySQL and TiCDC executes a time-consuming DDL statement, all other changefeeds are blocked. How should I handle the issue?

1. Pause the execution of the changefeed that contains the time-consuming DDL statement. Then you can see that other changefeeds are no longer blocked.
2. Search for the `apply job` field in the TiCDC log and confirm the `start-ts` of the time-consuming DDL statement.
3. Manually execute the DDL statement in the downstream. After the execution finishes, go on performing the following operations.
4. Modify the changefeed configuration and add the above `start-ts` to the `ignore-txn-start-ts` configuration item.
5. Resume the paused changefeed.

## After I upgrade the TiCDC cluster to v4.0.8, the `[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled` error is reported when I execute a changefeed

Since v4.0.8, if the `canal-json`, `canal` or `maxwell` protocol is used for output in a changefeed, TiCDC enables the old value feature automatically. However, if you have upgraded TiCDC from an earlier version to v4.0.8 or later, when the changefeed uses the `canal-json`, `canal` or `maxwell` protocol and the old value feature is disabled, this error is reported.

To fix the error, take the following steps:

1. Set the value of `enable-old-value` in the changefeed configuration file to `true`.
2. Execute `cdc cli changefeed pause` to pause the replication task.

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
    ```

3. Execute `cdc cli changefeed update` to update the original changefeed configuration.

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4. Execute `cdc cli changfeed resume` to resume the replication task.

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
    ```

## The `[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy` error is reported when I use TiCDC to create a changefeed

Solution: You need to execute the `pd-ctl service-gc-safepoint --pd <pd-addrs>` command to query the current GC safepoint and service GC safepoint. If the GC safepoint is smaller than the `start-ts` of the TiCDC replication task (changefeed), you can directly add the `--disable-gc-check` option to the `cdc cli create changefeed` command to create a changefeed.

If the result of `pd-ctl service-gc-safepoint --pd <pd-addrs>` does not have `gc_worker service_id`:

- If your PD version is v4.0.8 or earlier, refer to [PD issue #3128](https://github.com/tikv/pd/issues/3128) for details.
- If your PD is upgraded from v4.0.8 or an earlier version to a later version, refer to [PD issue #3366](https://github.com/tikv/pd/issues/3366) for details.

## `enable-old-value` is set to `true` when I create a TiCDC replication task, but `INSERT`/`UPDATE` statements from the upstream become `REPLACE INTO` after being replicated to the downstream

When a changefeed is created in TiCDC, the `safe-mode` setting defaults to `true`, which generates the `REPLACE INTO` statement to execute for the upstream `INSERT`/`UPDATE` statements.

Currently, users cannot modify the `safe-mode` setting, so this issue currently has no solution.

## When I use TiCDC to replicate messages to Kafka, Kafka returns the `Message was too large` error

For TiCDC v4.0.8 or earlier versions, you cannot effectively control the size of the message output to Kafka only by configuring the `max-message-bytes` setting for Kafka in the Sink URI. To control the message size, you also need to increase the limit on the bytes of messages to be received by Kafka. To add such a limit, add the following configuration to the Kafka server configuration.

```
# The maximum byte number of a message that the broker receives
message.max.bytes=2147483648
# The maximum byte number of a message that the broker copies
replica.fetch.max.bytes=2147483648
# The maximum message byte number that the consumer side reads
fetch.message.max.bytes=2147483648
```

## How can I find out whether a DDL statement fails to execute in downstream during TiCDC replication? How to resume the replication?

If a DDL statement fails to execute, the replication task (changefeed) automatically stops. The checkpoint-ts is the DDL statement's finish-ts minus one. If you want TiCDC to retry executing this statement in the downstream, use `cdc cli changefeed resume` to resume the replication task. For example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

If you want to skip this DDL statement that goes wrong, set the start-ts of the changefeed to the checkpoint-ts (the timestamp at which the DDL statement goes wrong) plus one. For example, if the checkpoint-ts at which the DDL statement goes wrong is `415241823337054209`, execute the following commands to skip this DDL statement:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --start-ts 415241823337054210
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

## The default value of the time type field is inconsistent when replicating a DDL statement to the downstream MySQL 5.7. What can I do?

Suppose that the `create table test (id int primary key, ts timestamp)` statement is executed in the upstream TiDB. When TiCDC replicates this statement to the downstream MySQL 5.7, MySQL uses the default configuration. The table schema after the replication is as follows. The default value of the `timestamp` field becomes `CURRENT_TIMESTAMP`:

{{< copyable "sql" >}}

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int(11) NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

From the result, you can see that the table schema before and after the replication is inconsistent. This is because the default value of `explicit_defaults_for_timestamp` in TiDB is different from that in MySQL. See [MySQL Compatibility](/mysql-compatibility.md#default-differences) for details.

Since v5.0.1 or v4.0.13, for each replication to MySQL, TiCDC automatically sets `explicit_defaults_for_timestamp = ON` to ensure that the time type is consistent between the upstream and downstream. For versions earlier than v5.0.1 or v4.0.13, pay attention to the compatibility issue caused by the inconsistent `explicit_defaults_for_timestamp` value when using TiCDC to replicate the time type data.

## When the sink of the replication downstream is TiDB or MySQL, what permissions do users of the downstream database need?

When the sink is TiDB or MySQL, the users of the downstream database need the following permissions:

- `Select`
- `Index`
- `Insert`
- `Update`
- `Delete`
- `Create`
- `Drop`
- `Alter`
- `Create View`

If you need to replicate `recover table` to the downstream TiDB, you should have the `Super` permission.
