---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
category: reference
---

# Troubleshoot a TiFlash Cluster

This section describes some commonly encountered issues when using TiFlash, the reasons, and the solutions.

## TiFlash replica is always unavailable

This is because TiFlash is in an abnormal state caused by configuration errors or environment issues. Take the following steps to identify the faulty component:

1. Check whether PD enables the `Placement Rules` feature (to enable the feature, see the step 2 of [Add TiFlash component to an existing TiDB cluster](/tiflash/deploy-tiflash.md#add-tiflash-component-to-an-existing-tidb-cluster):

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    The expected result is `"enable-placement-rules": "true"`.

2. Check whether the TiFlash process is working correctly by viewing `UpTime` on the TiFlash-Summary monitoring panel.

3. Check whether the TiFlash proxy status is normal through `pd-ctl`.

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    The TiFlash proxy's `store.labels` includes information such as `{"key": "engine", "value": "tiflash"}`. You can check this information to confirm a TiFlash proxy.

4. Check whether `pd buddy` can correctly print the logs (the log path is the value of `log` in the [flash.flash_cluster] configuration item; the default log path is under the `tmp` directory configured in the TiFlash configuration file).

5. Check whether the value of `max-replicas` in PD is less than or equal to the number of TiKV nodes in the cluster. If not, PD cannot replicate data to TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    Reconfirm the value of `max-replicas`.

6. Check whether the remaining disk space of the machine (where `store` of the TiFlash node is) is sufficient. By default, when the remaining disk space is less than 20% of the `store` capacity (which is controlled by the `low-space-ratio` parameter), PD cannot schedule data to this TiFlash node.

## TiFlash query time is unstable, and the error log prints many `Lock Exception` messages

This is because large amounts of data are written to the cluster, which causes that the TiFlash query encounters a lock and requires query retry.

You can set the query timestamp to one second earlier in TiDB. For example, if the current time is '2020-04-08 20:15:01', you can execute `set @@tidb_snapshot='2020-04-08 20:15:00';` before you execute the query. This makes less TiFlash queries encounter a lock and mitigates the risk of unstable query time.

## Some queries return the `Region Unavailable` error

If the load pressure on TiFlash is too heavy and it causes that TiFlash data replication falls behind, some queries might return the `Region Unavailable` error.

In this case, you can balance the load pressure by adding more TiFlash nodes.

## Data file corruption

Take the following steps to handle the data file corruption:

1. Refer to [Take a TiFlash node down](#take-a-tiflash-node-down) to take the corresponding TiFlash node down.
2. Delete the related data of the TiFlash node.
3. Redeploy the TiFlash node in the cluster.
