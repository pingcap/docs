---
title: TiCDC New Architecture
summary: Introduces the features, architectural design, deployment guide, and notes of the TiCDC new architecture.
---

# TiCDC New Architecture

Starting from v9.0.0, TiCDC introduces a new architecture that improves real-time data replication performance, scalability, and stability while reducing resource costs. This new architecture redesigns TiCDC core components and optimizes its data processing workflows, offering the following advantages:

- **Higher single-node performance**: a single node can replicate up to 500,000 tables, achieving replication throughput of up to 200 MiB/s in wide table scenarios.
- **Enhanced scalability**: cluster replication capability scales almost linearly. A single cluster can expand to over 100 nodes, support more than 10,000 changefeeds, and replicate millions of tables within a single changefeed.
- **Improved stability**: changefeed latency is reduced and performance is more stable in scenarios with high traffic, frequent DDL operations, and cluster scaling events. Resource isolation and priority scheduling reduce interference between multiple changefeed tasks.
- **Lower resource costs**: with improved resource utilization and reduced redundancy, CPU and memory resource usage efficiency improves by up to ten times in typical scenarios.

> **Warning:**
>
> The TiCDC new architecture is currently experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> The TiCDC new architecture does not yet support all the functionalities available in the [classic architecture](/ticdc/ticdc-classic-architecture.md). For more details, see [Limitations](#limitations).

## Architectural design

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-1.png)

The TiCDC new architecture consists of two core components: Log Service and Downstream Adapter.

- Log Service: as the core data service layer, Log Service fetches information such as row changes and DDL events from the upstream TiDB cluster, and then temporarily stores the change data on local disk. It also responds to data requests from the Downstream Adapter, periodically merging and sorting DML and DDL data and pushing the sorted data to the Downstream Adapter.
- Downstream Adapter: as the downstream data replication adaptation layer, Downstream Adapter handles user-initiated changefeed operations. It schedules and generates related replication tasks, fetches data from the Log Service, and replicates the fetched data to downstream systems.

By separating the architecture into stateful and stateless components, the TiCDC new architecture significantly improves system scalability, reliability, and flexibility. Log Service, as the stateful component, focuses on data acquisition, sorting, and storage. Decoupling it from changefeed processing logic enables data sharing across multiple changefeeds, effectively improving resource utilization and reducing system overhead. Downstream Adapter, as the stateless component, uses a lightweight scheduling mechanism that allows quick migration of replication tasks between instances. It can dynamically adjust the splitting and merging of replication tasks based on workload changes, ensuring low-latency replication in various scenarios.

## Comparison between the classic and new architectures

The new architecture is designed to address common issues during continuous system scaling, such as performance bottlenecks, insufficient stability, and limited scalability. Compared with the classic architecture, the new architecture achieves significant optimizations in the following key dimensions:

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

## Limitations

As an experimental feature, the TiCDC new architecture does not yet support all the functionalities available in the classic architecture. The following features will be available when the new architecture becomes generally available (GA) in future versions:

- [Split Update Events](/ticdc/ticdc-split-update-behavior.md)
- [Eventually Consistent Replication for Disaster Scenarios](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)
- Split large transactions
- [TiCDC Avro Protocol](/ticdc/ticdc-avro-protocol.md)
- [TiCDC CSV Protocol](/ticdc/ticdc-csv.md)
- [TiCDC Debezium Protocol](/ticdc/ticdc-debezium.md)
- [TiCDC Simple Protocol](/ticdc/ticdc-simple-protocol.md)
- [Event Filter](/ticdc/ticdc-filter.md#event-filter-rules)
- [TiCDC Data Integrity Validation for Single-Row Data](/ticdc/ticdc-integrity-check.md)
- [TiCDC Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md)
- [Replicate Data to Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Replicate Data to Storage Services](/ticdc/ticdc-sink-to-cloud-storage.md)

## Deployment steps

The TiCDC new architecture can only be deployed in TiDB clusters of v7.5.0 or later versions. Before deployment, make sure your TiDB cluster meets this version requirement.

You can use one of the following deployment methods:

- [Deploy a new TiDB cluster with new architecture TiCDC nodes using TiUP](#deploy-a-new-tidb-cluster-with-new-architecture-ticdc-nodes-using-tiup)
- [Deploy new architecture TiCDC nodes in an existing TiDB cluster using TiUP](#deploy-new-architecture-ticdc-nodes-in-an-existing-tidb-cluster-using-tiup)

### Deploy a new TiDB cluster with new architecture TiCDC nodes using TiUP

When deploying a new TiDB cluster of v9.0.0 or later using TiUP, you can also deploy the new architecture TiCDC at the same time. You only need to add the TiCDC related section and enable the new architecture in the configuration file that TiUP uses to start the TiDB cluster. The following is an example:

```yaml
cdc_servers:
  - host: 10.0.1.20
    config:
      newarch: true
  - host: 10.0.1.21
    config:
      newarch: true
```

> **Note:**
>
> The `newarch` configuration item is used only for the TiCDC new architecture. If the `newarch` configuration item is not specified, the classic architecture is used by default. If you still need to use the classic TiCDC architecture, do not add the `newarch` configuration item to the configuration file, as it might cause parsing failures.

For detailed instructions, see [Deploy a new TiDB cluster that includes TiCDC using TiUP](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup).

### Deploy new architecture TiCDC nodes in an existing TiDB cluster using TiUP

1. If your TiDB cluster does not have TiCDC nodes yet, refer to [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster) to add new TiCDC nodes in the cluster. Otherwise, skip this step.

2. If your TiDB cluster version is earlier than v9.0.0, you need to manually download the TiCDC binary package of v9.0.0 or later, and then patch the downloaded file to your TiDB cluster. Otherwise, skip this step.

    > **Warning:**
    >
    > After TiCDC is upgraded to the new architecture, rolling back to the classic architecture is not supported.

    1. Download the TiCDC binary file of v9.0.0 or later.

        The download link follows this format: `https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz`, where `${version}` is the TiCDC version, `${os}` is your operating system, and `${arch}` is the platform the component runs on (`amd64` or `arm64`).

        For example, to download the binary file of TiCDC v9.0.0-beta.1 for Linux (x86-64), run the following command:

        ```shell
        wget https://tiup-mirrors.pingcap.com/cdc-v9.0.0-beta.1-linux-amd64.tar.gz
        ```

    2. Patch the downloaded TiCDC binary file to your TiDB cluster using the [`tiup cluster patch`](/tiup/tiup-component-cluster-patch.md) command:

        ```shell
        tiup cluster patch <cluster-name> ./cdc-v9.0.0-beta.1-linux-amd64.tar.gz -R cdc
        ```

3. If your TiDB cluster has running changefeeds, refer to [Pause a replication task](/ticdc/ticdc-manage-changefeed.md#pause-a-replication-task) to pause all replication tasks of the changefeeds.

4. Update the TiCDC configuration using the [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) command:

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    ```yaml
    server_configs:
      cdc:
        newarch: true
    ```

5. Refer to [Resume replication Task](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task) to resume the replication tasks of all changefeeds.

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

The monitoring dashboard for the TiCDC new architecture is integrated into the Grafana dashboard, with the name **TiCDC-New-Arch**. You can view monitoring metrics related to the new architecture on this dashboard.

## Notes

- In the TiCDC classic architecture, DDL replication operations are strictly serial, thus the replication progress can be tracked only using the changefeed's `CheckpointTs`. In the new architecture, however, TiCDC replicates DDL changes for different tables in parallel whenever possible to improve DDL replication efficiency. To accurately record the DDL replication progress of each table in a downstream MySQL-compatible database, the TiCDC new architecture creates a table named `tidb_cdc.ddl_ts_v1` in the downstream database, specifically storing the DDL replication progress information of the changefeed.