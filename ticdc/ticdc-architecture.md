---
title: TiCDC New Architecture
summary: Introduces the features, architectural design, deployment guide, and notes of the TiCDC new architecture.
---

# TiCDC New Architecture

Starting from [TiCDC v8.5.4-release.1](https://github.com/pingcap/ticdc/releases/tag/v8.5.4-release.1), TiCDC introduces a new architecture that improves the performance, scalability, and stability of real-time data replication while reducing resource costs. This new architecture redesigns TiCDC core components and optimizes its data processing workflows, offering the following advantages:

- **Higher single-node performance**: a single node can replicate up to 500,000 tables, achieving replication throughput of up to 190 MiB/s on a single node in wide table scenarios.
- **Enhanced scalability**: cluster replication capability scales almost linearly. A single cluster can expand to over 100 nodes, support more than 10,000 changefeeds, and replicate millions of tables within a single changefeed.
- **Improved stability**: changefeed latency is reduced and performance is more stable in scenarios with high traffic, frequent DDL operations, and cluster scaling events. Resource isolation and priority scheduling reduce interference between multiple changefeed tasks.
- **Lower resource costs**: with improved resource utilization and reduced redundancy, CPU and memory resource usage can decrease by up to 50% in typical scenarios.

## Architectural design

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-1.png)

The TiCDC new architecture consists of two core components: Log Service and Downstream Adapter.

- Log Service: as the core data service layer, Log Service fetches information such as row changes and DDL events from the upstream TiDB cluster, and then temporarily stores the change data on local disks. It also responds to data requests from the Downstream Adapter, periodically merging and sorting DML and DDL data and pushing the sorted data to the Downstream Adapter.
- Downstream Adapter: as the downstream data replication adaptation layer, Downstream Adapter handles user-initiated changefeed operations. It schedules and generates related replication tasks, fetches data from the Log Service, and replicates the fetched data to downstream systems.

By separating the architecture into stateful and stateless components, the TiCDC new architecture significantly improves system scalability, reliability, and flexibility. Log Service, as the stateful component, focuses on data acquisition, sorting, and storage. Decoupling it from changefeed processing logic enables data sharing across multiple changefeeds, effectively improving resource utilization and reducing system overhead. Downstream Adapter, as the stateless component, uses a lightweight scheduling mechanism that allows quick migration of replication tasks between instances. It can dynamically adjust the splitting and merging of replication tasks based on workload changes, ensuring low-latency replication in various scenarios.

## Comparison between the classic and new architectures

The new architecture is designed to address common issues during continuous system scaling, such as performance bottlenecks, insufficient stability, and limited scalability. Compared with the [classic architecture](/ticdc/ticdc-classic-architecture.md), the new architecture achieves significant optimizations in the following key dimensions:

| Feature | TiCDC classic architecture | TiCDC new architecture |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| **Processing logic driver** | Timer-driven | Event-driven |
| **Task triggering mechanism** | Timer-triggered main loop that checks tasks every 50 ms, with limited processing performance | Event-driven, triggered by events such as DML changes, DDL changes, and changefeed operations. Events in the queue are processed as quickly as possible without waiting for the fixed 50 ms interval, reducing additional latency |
| **Task scheduling method** | Each changefeed runs a main loop that polls for tasks | Events are queued and processed concurrently by multiple threads |
| **Task processing efficiency** | Each task goes through multiple cycles, creating performance bottlenecks | Events are processed immediately without waiting for fixed intervals, reducing latency |
| **Resource consumption** | Frequent checks on inactive tables waste CPU resources | Consumer threads only process queued events, avoiding the consumption of checking inactive tasks |
| **Complexity** | O(n), performance degrades as the number of tables increases | O(1), not affected by the number of tables, improving efficiency |
| **CPU utilization** | Each changefeed can only use one logical CPU | Each changefeed can fully utilize the parallel processing capabilities of multi-core CPUs |
| **Scalability** | Poor scalability (limited by the number of CPUs) | Strong scalability through multi-threaded processing and event queues |
| **Changefeed interference** | The owner node might cause interference between changefeeds | Event-driven mode avoids interference between changefeeds |

![Comparison between the TiCDC classic and new architectures](/media/ticdc/ticdc-new-arch-2.png)

## Choose between the classic and new architectures

If your workload meets any of the following conditions, it is recommended to switch from the [classic TiCDC architecture](/ticdc/ticdc-classic-architecture.md) to the new architecture for better performance and stability:

- Bottlenecks in incremental scan performance: incremental scan tasks take an excessively long time to complete, leading to continuously increasing replication latency.
- Ultra-high traffic scenarios: the total changefeed traffic exceeds 700 MiB/s.
- Single tables with high-throughput writes in MySQL sink: the target table has **only one primary key or non-null unique key**.
- Large-scale table replication: the number of tables to be replicated exceeds 100,000.
- Frequent DDL operations causing latency: frequent execution of DDL statements significantly increases replication latency.

## New features

The new architecture supports **table-level task splitting** for MySQL sinks. You can enable this feature by setting `scheduler.enable-table-across-nodes = true` in the changefeed configuration.

When this feature is enabled, TiCDC automatically splits and distributes tables with **only one primary key or non-null unique key** across multiple nodes for parallel replication if those tables meet any of the following conditions. This improves replication efficiency and resource utilization:

- The table Region count exceeds the configured threshold (`100000` by default, adjustable via `scheduler.region-threshold`).
- The table write traffic exceeds the configured threshold (disabled by default, configurable via `scheduler.write-key-threshold`).

## Compatibility

### DDL progress tracking table

In the TiCDC classic architecture, DDL replication operations are strictly serial, thus the replication progress can be tracked only using the changefeed's `CheckpointTs`. In the new architecture, however, TiCDC replicates DDL changes for different tables in parallel whenever possible to improve DDL replication efficiency. To accurately record the DDL replication progress of each table in a downstream MySQL-compatible database, the TiCDC new architecture creates a table named `tidb_cdc.ddl_ts_v1` in the downstream database, specifically storing the DDL replication progress information of the changefeed.

### Changes in DDL replication behavior

- The classic TiCDC architecture does not support DDLs that swap table names (for example, `RENAME TABLE a TO c, b TO a, c TO b;`). The new architecture supports such DDLs.

- The new architecture unifies and simplifies the filtering rules for `RENAME` DDLs.

    - In the classic architecture, the filtering logic is as follows:

        - Single-table renaming: a DDL statement is replicated only if the old table name matches the filter rule.
        - Multi-table renaming: a DDL statement is replicated only if both old and new table names match the filter rules.

    - In the new architecture, for both single-table and multi-table renaming, a DDL statement is replicated as long as old table names in the statement match the filter rules.

        Take the following filter rule as an example:

        ```toml
        [filter]
        rules = ['test.t*']
        ```

        - In the classic architecture: for single-table renaming, such as `RENAME TABLE test.t1 TO ignore.t1`, the old table name `test.t1` matches the rule, so it will be replicated. For a multi-table renaming, such as `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`, because the new table name `ignore.t1` does not match the rule, it will not be replicated.
        - In the new TiCDC architecture: because the old table names in both `RENAME TABLE test.t1 TO ignore.t1` and `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;` match the rules, both DDL statements will be replicated.

## Limitations

The new TiCDC architecture incorporates all functionalities of the classic architecture. However, some features have not yet been fully tested. To ensure system stability, it is **NOT** recommended to use the following features in core production environments:

- [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md)
- [Redo Log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)
- [Pulsar Sink](/ticdc/ticdc-sink-to-pulsar.md)
- [Storage Sink](/ticdc/ticdc-sink-to-cloud-storage.md)

In addition, the new TiCDC architecture currently does not support splitting large transactions into multiple batches for downstream replication. As a result, there is still a risk of OOM when processing extremely large transactions. Make sure to evaluate and mitigate this risk appropriately before using the new architecture.

## Deployment steps

The TiCDC new architecture can only be deployed in TiDB clusters of v7.5.0 or later versions. Before deployment, make sure your TiDB cluster meets this version requirement.

You can deploy the TiCDC new architecture using TiUP or TiDB Operator.

<SimpleTab>
<div label="TiUP">

To deploy the TiCDC new architecture using TiUP, take the following steps:

1. If your TiDB cluster does not have TiCDC nodes yet, refer to [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster) to add new TiCDC nodes in the cluster. Otherwise, skip this step.

2. Download the TiCDC binary package for the new architecture.

    The download link follows this format: `https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz`, where `${version}` is the TiCDC version, `${os}` is your operating system, and `${arch}` is the platform the component runs on (`amd64` or `arm64`).

    For example, to download the binary package of TiCDC v8.5.4-release.1 for Linux (x86-64), run the following command:

    ```shell
    wget https://tiup-mirrors.pingcap.com/cdc-v8.5.4-release.1-linux-amd64.tar.gz
    ```

3. If your TiDB cluster has running changefeeds, refer to [Pause a replication task](/ticdc/ticdc-manage-changefeed.md#pause-a-replication-task) to pause all replication tasks of the changefeeds.

    ```shell
    # The default server port of TiCDC is 8300.
    cdc cli changefeed pause --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

4. Patch the downloaded TiCDC binary file to your TiDB cluster using the [`tiup cluster patch`](/tiup/tiup-component-cluster-patch.md) command:

    ```shell
    tiup cluster patch <cluster-name> ./cdc-v8.5.4-release.1-linux-amd64.tar.gz -R cdc
    ```

5. Update the TiCDC configuration using the [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) command to enable the new architecture:

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    ```yaml
    server_configs:
      cdc:
        newarch: true
    ```

6. Refer to [Resume replication task](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task) to resume all replication tasks:

    ```shell
    # The default server port of TiCDC is 8300.
    cdc cli changefeed resume --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

</div>
<div label="TiDB Operator">

To deploy the TiCDC new architecture using TiDB Operator, take the following steps:

- If your TiDB cluster does not include a TiCDC component, refer to [Add TiCDC to an existing TiDB cluster](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-ticdc/#add-ticdc-to-an-existing-tidb-cluster) to add new TiCDC nodes. When doing so, specify the TiCDC image version as the new architecture version in the cluster configuration file.

    For example:

    ```yaml
    spec:
      ticdc:
        baseImage: pingcap/ticdc
        version: v8.5.4-release.1
        replicas: 3
        config:
          newarch = true
    ```

- If your TiDB cluster already includes a TiCDC component, take the following steps:

    1. If your TiDB cluster has running changefeeds, pause all replication tasks of the changefeeds:

        ```shell
        kubectl exec -it ${pod_name} -n ${namespace} -- sh
        ```

        ```shell
        # The default server port of TiCDC deployed via TiDB Operator is 8301.
        /cdc cli changefeed pause --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
        ```

    2. Update the TiCDC image version in the cluster configuration file to the new architecture version:

        ```shell
        kubectl edit tc ${cluster_name} -n ${namespace}
        ```

        ```yaml
        spec:
          ticdc:
            baseImage: pingcap/ticdc
            version: v8.5.4-release.1
            replicas: 3
        ```

        ```shell
        kubectl apply -f ${cluster_name} -n ${namespace}
        ```

    3. Resume all replication tasks:

        ```shell
        kubectl exec -it ${pod_name} -n ${namespace} -- sh
        ```

        ```shell
        # The default server port of TiCDC deployed via TiDB Operator is 8301.
        /cdc cli changefeed resume --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
        ```

</div>
</SimpleTab>

## Use the new architecture

After deploying the TiCDC nodes with the new architecture, you can continue using the same commands as in the classic architecture. There is no need to learn new commands or modify the commands used in the classic architecture.

For example, to create a replication task in a new architecture TiCDC node, run the following command:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

To query details about a specific replication task, run the following command:

```shell
cdc cli changefeed query -s --server=http://127.0.0.1:8300 --changefeed-id=simple-replication-task
```

For more command usage methods and details, see [Manage Changefeeds](/ticdc/ticdc-manage-changefeed.md).

## Monitoring

Currently, the monitoring dashboard **TiCDC-New-Arch** for the TiCDC new architecture is not managed by TiUP yet. To view this dashboard on Grafana, you need to manually import the [TiCDC monitoring metrics file](https://github.com/pingcap/ticdc/blob/master/metrics/grafana/ticdc_new_arch.json).

For detailed descriptions of each monitoring metric, see [Metrics for TiCDC in the new architecture](/ticdc/monitor-ticdc.md#metrics-for-ticdc-in-the-new-architecture).