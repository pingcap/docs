---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
category: reference
---

# Maintain a TiFlash Cluster

This document describes common operations when you maintain a TiFlash cluster, including checking the version, node logout, troubleshooting, critical logs, and a system table.

## Check the TiFlash version

There are two ways to check the TiFlash version:

- If the binary file name of TiFlash is `tiflash`, you can check the version by executing the `./tiflash version` command.

    However, to execute the above command, you need to add the directory path which includes the `libtiflash_proxy.so` dynamic library to the `LD_LIBRARY_PATH` environment variable. This is because the running of TiFlash relies on the `libtiflash_proxy.so` dynamic library.

    For example, when `tiflash` and `libtiflash_proxy.so` are in the same directory, you can first switch to this directory, and then use the following command to check the TiFlash version:

    {{< copyable "shell-regular" >}}

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

- Check the TiFlash version by referring to the TiFlash log. For the log path, see [[logger] in the tiflash.toml configuration file](/reference/tiflash/configuration.md#configuration-file-tiflashtoml). For example:

    ```
    <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2
    ```

## Logout a TiFlash node

Logouting a TiFlash node differs from [Scaling in the TiFlash node](/reference/tiflash/scale.md#scale-in-tiflash-node) in that the logout doesn't remove the node from TiDB Ansible; instead, it just safely shutdown the process.

Take the following steps to logout a TiFlash node:

> **Note:**
>
> After you logout the TiFlash node, if the number of the remaining nodes in the TiFlash cluster is greater than or equal to the maximum replicas of all data tables, you can go directly to step 3.

1. For a TiDB server, if the number of replicas of tables is greater than or equal to that of the remaining TiFlash nodes in the cluster, execute the following command:

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. To ensure TiFlash replicas of related tables are removed, see [View the Table Replication Progress](/reference/tiflash/use-tiflash.md#view-the-table-replication-progress). If you cannot view the replication progress of the related tables, it means that the replicas are removed.

3. Input the `store` command into [pd-ctl](/reference/tools/pd-control.md) (the binary file in `resources/bin` in the tidb-ansible directory) to view the `store id` of the TiFlash node.

4. Input `store delete <store_id>` into `pd-ctl`. Here `<store_id>` refers to the `store id` in step 3.

5. When the corresponding `store` of the node disappeared, or when `state_name` is changed to `Tomestone`, shutdown the TiFlash process.

> **Note:**
>
> If you don't cancel all tables replicated to TiFlash before all TiFlash nodes in a cluster stop running, you need to manually delete the replication rule in PD. Or you cannot successfully logout the TiFlash node.
>
> To manually delete the replication rule in PD, send the `DELETE` request `http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/<rule_id>`. `rule_id` refers to the `id` of the `rule` to be deleted.

## TiFlash troubleshooting

This section describes some common questions of TiFlash, the reasons, and the solutions.

### TiFlash replica is always in an unusable state

This is because TiFlash is in the exception status caused by the configuration error or the environment problems. You can take the following steps to identify the problem component:

1. Check whether PD enables the `Placement Rules` feature (to enable the feature, see the step 2 of [Add a TiFlash component in an existing TiDB Cluster](/reference/tiflash/deploy.md#add-a-TiFlash-component-in-an-existing-TiDB-cluster):

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    The expected result is `"enable-placement-rules": "true"`.

2. Check whether the TiFlash process in the operation system is working correctly using `UpTime` of the TiFlash-Summary monitor panel.

3. Check whether the TiFlash proxy status is normal through `pd-ctl`.

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    If `store.labels` includes information such as `{"key": "engine", "value": "tiflash"}`, it refers to the TiFlash proxy.

4. Check whether `pd buddy` can print the logs correctly (the value of `log` in the [flash.flash_cluster] configuration item of the log path, is by default the `tmp` directory configured by the TiFlash configuration file).

5. Check whether the value of `max-replicas` in PD is less than or equal to the number of TiKV nodes in the cluster. If not, PD cannot replicate data to TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    Reconfirm the value of `max-replicas`.

6. Check whether the remaining disk space of the machine (where `store` of the TiFlash node is) is sufficient. By default, when the remaining disk space is less than 20% of the `store` capacity (which is controlled by the `low-space-ratio` parameter), PD cannot schedule data to TiFlash.

### TiFlash query time is unstable, and error log prints many `Lock Exception` messages

This is because large amounts of data are written to the cluster, which leads to the situation that the TiFlash query encounters a lock and requires query retry.

You can set the query timestamp to one second earlier in TiDB (for example, `set @@tidb_snapshot=412881237115666555;`), to reduce the possibility that TiFlash query encounters a lock; thereby mitigating the risk of unstable query time.

### Partial queries return `Region Unavailable`

If the load pressure in TiFlash is so heavy that TiFlash data replication falls behind. Some queries might return error message `Region Unavailable`.

In this case, you can share the pressure by adding TiFlash nodes.

### Data file corruption

Take the following steps to handle the data file corruption:

1. Refer to [Logout a TiFlash node](/reference/tiflash/maintain.md#logout-a-tiflash-node) to logout the corresponding TiFlash node.
2. Delete the related data of the TiFlash node.
3. Redeploy the TiFlash node in the cluster.

## TiFlash critical logs

| Log Information | Log Description |
|---------------|-------------------|
| [ 23 ] <Information> KVStore: Start to persist [region 47, applied: term 6 index 10] | Data starts to be replicated (the number in the square brackets at the start of the log refers to the thread ID |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | `Handling DAG request` refers to that TiFlash starts to handle a Coprocessor request |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | `Handle DAG request done` refers to that TiFlash finishes a Coprocessor request |

You can find the beginning or the end of a Coprocessor request, and then locate the related logs of the Coprocessor request through the thread ID printed at the start of the log.

## TiFlash system table

The column names and their descriptions of the `information_schema.tiflash_replica` system table are as follows:

| Column Name | Description |
|---------------|-----------|
| TABLE_SCHEMA | database name |
| TABLE_NAME | table name |
| TABLE_ID | table ID |
| REPLICA_COUNT | number of TiFlash replicas |
| AVAILABLE | available or not (0/1)|
| PROGRESS | replication progress [0.0~1.0] |
