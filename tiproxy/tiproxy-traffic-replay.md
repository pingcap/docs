---
title: TiProxy Traffic Replay
summary: Introduce the use cases and steps for the TiProxy traffic replay feature.
---

# TiProxy Traffic Replay

> **Warning:**
>
> Currently, the TiProxy traffic replay feature is experimental. It is not recommended that you use it in production environments. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tiproxy/issues) on GitHub.

Starting from TiProxy v1.3.0, you can use TiProxy to capture access traffic in a TiDB production cluster and replay it in a test cluster at a specified rate. This feature enables you to reproduce actual workloads from the production cluster in a test environment, verifying SQL statement execution results and performance.

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-traffic-replay.png" alt="TiProxy traffic replay" width="800" />

## Use cases

Traffic replay is suitable for the following scenarios:

- **Verify TiDB version upgrades**: Replay production traffic on a test cluster with a new TiDB version to verify that the new TiDB version can successfully execute all SQL statements.
- **Assess change impact**: Simulate production traffic on a test cluster to verify the impact of changes on the cluster. For example, verify the effects before modifying configuration items or system variables, altering table schemas, or enabling new TiDB features.
- **Validate performance before TiDB scaling**: Replay traffic at corresponding rates on a test cluster with a new scale to validate whether the performance meets requirements. For example, to plan a 50% cluster downscale for cost savings, replay traffic at half speed to validate if SQL latency meets requirements after scaling.
- **Test performance limits**: Replay traffic multiple times on a test cluster of the same scale, increasing the replay rate each time to test the throughput limit of that scale and assess whether performance meets future business growth needs.

Traffic replay is not suitable for the following scenarios:

- Verify SQL compatibility between TiDB and MySQL: TiProxy only supports reading traffic files it generates and cannot capture traffic from MySQL for replay on TiDB.
- Compare SQL execution results between TiDB versions: TiProxy only verifies if SQL statements execute successfully but does not compare results.

## Usage

1. Prepare the test environment:

    1. Create a test cluster. For more information, see [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).
    2. Install `tiproxyctl` and ensure the host with `tiproxyctl` can connect to TiProxy instances in both production and test clusters. For more information, see [Install TiProxy Control](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control).
    3. Replicate data from the production cluster to the test cluster. For more information, see [Data Migration Overview](/migration-overview.md).
    4. Run the [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) statement in the test cluster to update statistics.

2. Use the [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture) command to connect to the production cluster's TiProxy instance and start capturing traffic.

    > **Note:**
    >
    > - TiProxy captures traffic on all connections, including existing and newly created ones.
    > - In TiProxy primary-secondary mode, connect to the primary TiProxy instance.
    > - If TiProxy is configured with a virtual IP, it is recommended to connect to the virtual IP address.
    > - The higher the CPU usage of TiProxy, the greater the impact of traffic capture on QPS. To reduce the impact on the production cluster, it is recommended to reserve at least 30% of CPU capacity, which results in an approximately 3% decrease in average QPS. For detailed performance data, see [Traffic capture test](/tiproxy/tiproxy-performance-test.md#traffic-capture-test).
    > - TiProxy does not automatically delete previous capture files when capturing traffic again. You need to manually delete them.

    For example, the following command connects to the TiProxy instance at `10.0.1.10:3080`, captures traffic for one hour, and saves it to the `/tmp/traffic` directory on the TiProxy instance:

    ```shell
    tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
    ```

    Traffic files are automatically rotated and compressed. Example files in the `/tmp/traffic` directory:

    ```shell
    ls /tmp/traffic
    # meta    traffic-2024-08-29T17-37-12.477.log.gz  traffic-2024-08-29T17-43-11.166.log.gz traffic.log
    ```

    For more information, see [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture).

3. Copy the traffic file directory to the test cluster's TiProxy instance.
4. Use [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay) to connect to the test cluster's TiProxy instance and start replaying traffic.

    By default, SQL statements are executed at the same rate as in the production cluster, and each database connection corresponds to a connection in the production cluster to simulate the production load and ensure consistent transaction execution order.

    For example, the following command connects to the TiProxy instance at `10.0.1.10:3080` using username `u1` and password `123456`, reads traffic files from the `/tmp/traffic` directory on the TiProxy instance, and replays the traffic:

    ```shell
    tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    Because all traffic runs under user `u1`, ensure `u1` can access all databases and tables. If no such user exists, create one.

    For more information, see [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay).

5. View the replay report.

    After replay completion, the report is stored in the `tiproxy_traffic_replay` database on the test cluster. This database contains two tables: `fail` and `other_errors`.

    The `fail` table stores failed SQL statements, with the following fields:

    - `cmd_type`: the type of a failed command, such as `Query` (execute an ordinary statement), `Prepare` (prepare a statement), and `Execute` (execute a prepared statement).
    - `digest`: the digest of the failed SQL statement.
    - `sample_stmt`: the SQL text when the statement first failed.
    - `sample_err_msg`: the error message when the SQL statement failed.
    - `sample_conn_id`: the connection ID recorded in the traffic file for the SQL statement. You can use this to view the execution context in the traffic file.
    - `sample_capture_time`: the execution time recorded in the traffic file for the SQL statement. You can use this to view the execution context in the traffic file.
    - `sample_replay_time`: the time when the SQL statement failed during replay. You can use this to view error information in the TiDB log file.
    - `count`: the number of times the SQL statement failed.

    The following is an example output of the `fail` table:

    ```sql
    SELECT * FROM tiproxy_traffic_replay.fail LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
               cmd_type: StmtExecute
                 digest: 89c5c505772b8b7e8d5d1eb49f4d47ed914daa2663ed24a85f762daa3cdff43c
            sample_stmt: INSERT INTO new_order (no_o_id, no_d_id, no_w_id) VALUES (?, ?, ?) params=[3077 6 1]
         sample_err_msg: ERROR 1062 (23000): Duplicate entry '1-6-3077' for key 'new_order.PRIMARY'
         sample_conn_id: 1356
    sample_capture_time: 2024-10-17 12:59:15
     sample_replay_time: 2024-10-17 13:05:05
                  count: 4
    ```

    The `other_errors` table stores unexpected errors, such as network errors or database connection errors, with the following fields:

    - `err_type`: the type of error, presented as a brief error message. For example, `i/o timeout`.
    - `sample_err_msg`: the complete error message when the error first occurred.
    - `sample_replay_time`: the time when the error occurred during replay. You can use this to view error information in the TiDB log file.
    - `count`: the number of occurrences for this error.

    The following is an example output of the `other_errors` table:

    ```sql
    SELECT * FROM tiproxy_traffic_replay.other_errors LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
              err_type: failed to read the connection: EOF
        sample_err_msg: this is an error from the backend connection: failed to read the connection: EOF
    sample_replay_time: 2024-10-17 12:57:39
                 count: 1
    ```

    > **Note:**
    >
    > - The table schema of `tiproxy_traffic_replay` might change in future versions. It is not recommended to directly read data from `tiproxy_traffic_replay` in your application or tool development.
    > - Replay does not guarantee that the transaction execution order between connections exactly matches the capture sequence. This might lead to incorrect error reports.
    > - TiProxy does not automatically delete the previous replay report when replaying traffic. You need to manually delete it.

## Test throughput

To test cluster throughput, use the `--speed` option to adjust the replay rate.

For example, `--speed=2` executes SQL statements at twice the rate, reducing the total replay time by half:

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

Increasing the replay rate only reduces idle time between SQL statements and does not increase the number of connections. When session idle time is already short, increasing the speed might not effectively improve throughput. In such cases, you can deploy multiple TiProxy instances to replay the same traffic files simultaneously, increasing concurrency to improve throughput.

## View and manage tasks

During capture and replay, tasks automatically stop if unknown errors occur. To view the current task progress or error information from the last task, use the [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show) command:

```shell
tiproxyctl traffic show --host 10.0.1.10 --port 3080
```

For example, the following output indicates a running capture task:

```json
[
   {
      "type": "capture",
      "start_time": "2024-09-03T09:10:58.220644+08:00",
      "duration": "2h",
      "output": "/tmp/traffic",
      "progress": "45%",
      "status": "running"
   }
]
```

For more information, see [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show).

To cancel the current capture or replay task, use the [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel) command:

```shell
tiproxyctl traffic cancel --host 10.0.1.10 --port 3080
```

For more information, see [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel).

## Limitations

- TiProxy only supports replaying traffic files captured by TiProxy and does not support other file formats. Therefore, make sure to capture traffic from the production cluster using TiProxy first.
- TiProxy traffic replay does not support filtering SQL types and DML and DDL statements are replayed. Therefore, you need to restore the cluster data to its pre-replay state before replaying again.
- TiProxy traffic replay does not support testing [Resource Control](/tidb-resource-control-ru-groups.md) and [privilege management](/privilege-management.md) because TiProxy uses the same username to replay traffic.
- TiProxy does not support replaying [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) statements.

## More resources

For more information about the traffic replay of TiProxy, see the [design document](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-08-27-traffic-replay.md).