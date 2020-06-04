---
title: Scale the TiDB Cluster Using TiUP
summary: Learn how to scale the TiDB cluster using TiUP.
category: how-to
aliases: ['/docs/dev/how-to/scale/with-tiup/']
---

# Scale the TiDB Cluster Using TiUP

The capacity of a TiDB cluster can be increased or decreased without interrupting the online services.

This document describes how to scale the TiDB, TiKV, PD, TiCDC, or TiFlash nodes using TiUP. If you have not installed TiUP, refer to the steps in [Install TiUP on the control machine](/upgrade-tidb-using-tiup.md#install-tiup-on-the-control-machine) and import the cluster into TiUP before you use TiUP to scale the TiDB cluster.

To view the current cluster name list, run `tiup cluster list`.

For example, if the original topology of the cluster is as follows:

| Host IP | Service |
|:---|:----|
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD |
| 10.0.1.5 | TiKV + Monitor |
| 10.0.1.1 | TiKV |
| 10.0.1.2 | TiKV |

## Scale out a TiDB/PD/TiKV node

If you want to add a TiDB node to the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to add the PD node. Before you add the TiKV node, it is recommended that you adjust the PD scheduling parameters in advance according to the cluster load.

1. Configure the scale-out topology:

    > **Note:**
    >
    > * The port and directory information is not required by default.
    > * If multiple instances are deployed on a single machine, you need to allocate different ports and directories for them. If the ports or directories have conflicts, you will receive a notification during deployment or scaling.

    Add the scale-out topology configuration in the `scale-out.yaml` file:

    {{< copyable "shell-regular" >}}

    ```shell
    vi scale-out.yaml
    ```

    {{< copyable "" >}}

    ```ini
    tidb_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 4000
      status_port: 10080
      deploy_dir: /data/deploy/install/deploy/tidb-4000
      log_dir: /data/deploy/install/log/tidb-4000
    ```

    Here is a TiKV configuration file template:

    {{< copyable "" >}}

    ```ini
    tikv_servers:
    - host: 10.0.1.5
        ssh_port: 22
        port: 20160
        status_port: 20180
        deploy_dir: /data/deploy/install/deploy/tikv-20160
        data_dir: /data/deploy/install/data/tikv-20160
        log_dir: /data/deploy/install/log/tikv-20160
    ```

    Here is a PD configuration file template:

    {{< copyable "" >}}

    ```ini
    pd_servers:
    - host: 10.0.1.5
        ssh_port: 22
        name: pd-1
        client_port: 2379
        peer_port: 2380
        deploy_dir: /data/deploy/install/deploy/pd-2379
        data_dir: /data/deploy/install/data/pd-2379
        log_dir: /data/deploy/install/log/pd-2379
    ```

    To view the configuration of the current cluster, run `tiup cluster edit-config <cluster-name>`. Because the parameter configuration of `global` and `server_configs` is inherited by `scale-out.yaml` and thus also takes effect in `scale-out.yaml`.

    After the configuration, the current topology of the cluster is as follows:

    | Host IP | Service |
    |:---|:----|
    | 10.0.1.3   | TiDB + TiFlash   |
    | 10.0.1.4   | TiDB + PD   |
    | 10.0.1.5   | **TiDB** + TiKV + Monitor   |
    | 10.0.1.1   | TiKV    |
    | 10.0.1.2   | TiKV    |

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    If you see the `Scaled cluster <cluster-name> out successfully`, the scale-out operation is successfully completed.

3. Check the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser to monitor the status of the cluster and the new node.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | **TiDB** + TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale out a TiFlash node

If you want to add a TiFlash node to the `10.0.1.4` host, take the following steps.

> **Note:**
>
> When adding a TiFlash node to an existing TiDB cluster, you need to note the following things:
>
> 1. Confirm that the current TiDB version supports using TiFlash, otherwise upgrade your TiDB cluster to v4.0.0-rc or higher.
> 2. Download [pd-ctl](https://download.pingcap.org/tidb-v4.0.0-rc.2-linux-amd64.tar.gz) and execute the `config set enable-placement-rules true` command to enable the PD's Placement Rules.

1. Add the node information to the `scale-out.yaml` file:

    Create the `scale-out.yaml` file to add the TiFlash node information.

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 10.0.1.4
    ```

    Currently, you can only add IP but not domain name.

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

3. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster and the new node.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + **TiFlash**    |
| 10.0.1.5   | TiDB+ TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale out a TiCDC node

If you want to add two TiCDC nodes to the `10.0.1.3` and `10.0.1.4` hosts, take the following steps.

1. Add the node information to the `scale-out.yaml` file:

    Create the `scale-out.yaml` file to add the TiCDC node information.

    {{< copyable "" >}}

    ```ini
    cdc_servers:
      - host: 10.0.1.3
      - host: 10.0.1.4
    ```

2. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

3. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster and the new nodes.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + **TiCDC**  |
| 10.0.1.4   | TiDB + PD + TiFlash + **TiCDC**  |
| 10.0.1.5   | TiDB+ TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale in a TiDB/PD/TiKV node

If you want to remove a TiKV node from the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to remove the TiDB and PD node.

1. View the node ID information:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ```
    Starting /root/.tiup/components/cluster/v0.4.6/cluster display <cluster-name>
    TiDB Cluster: <cluster-name>
    TiDB Version: v4.0.0-rc
    ID              Role         Host        Ports                            Status  Data Dir                Deploy Dir
    --              ----         ----        -----                            ------  --------                ----------
    10.0.1.3:8300   cdc          10.0.1.3    8300                             Up      -                       deploy/cdc-8300
    10.0.1.4:8300   cdc          10.0.1.4    8300                             Up      -                       deploy/cdc-8300
    10.0.1.4:2379   pd           10.0.1.4    2379/2380                        Healthy data/pd-2379            deploy/pd-2379
    10.0.1.1:20160  tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.2:20160  tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.5:20160  tikv         10.0.1.5    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.3:4000   tidb         10.0.1.3    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.4:4000   tidb         10.0.1.4    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.5:4000   tidb         10.0.1.5    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.3:9000   tiflash      10.0.1.3    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.4:9000   tiflash      10.0.1.4    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.5:9090   prometheus   10.0.1.5    9090                             Up      data/prometheus-9090    deploy/prometheus-9090
    10.0.1.5:3000   grafana      10.0.1.5    3000                             Up      -                       deploy/grafana-3000
    10.0.1.5:9093   alertmanager 10.0.1.5    9093/9294                        Up      data/alertmanager-9093  deploy/alertmanager-9093
    ```

2. Run the scale-in command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
    ```

    The `--node` parameter is the ID of the node to be taken offline.

    If you see the `Scaled cluster <cluster-name> in successfully`, the scale-in operation is successfully completed.

3. Check the cluster status:

    The scale-in process takes some time. If the status of the node to be scaled in becomes `Tombstone`, that means the scale-in operation is successful.

    To check the scale-in status, run the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster.

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + TiFlash + TiCDC |
| 10.0.1.5   | TiDB + Monitor **(TiKV is deleted)**   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale in a TiFlash node

If you want to remove the TiFlash node from the `10.0.1.4` host, take the following steps.

> **Note:**
>
> The scale-in process described in this section does not delete the data on the node that goes offline. If you need to bring the node back again, delete the data manually.

1. Take the node offline:

    To take offline the node to be scaled in, refer to [Take a TiFlash node down](/tiflash/maintain-tiflash.md#take-a-tiflash-node-down).

2. Check the node status:

    The scale-in process takes some time.

    You can use Grafana or pd-ctl to check whether the node has been successfully taken offline.

3. Scale in the TiFlash node:

    After the `store` corresponding to TiFlash disappears, or the `state_name` becomes `Tombstone`, it means that the TiFlash node has successfully gone offline. Then execute the following command to scale in the TiFlash node:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

4. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster.

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + TiCDC **（TiFlash is deleted）**  |
| 10.0.1.5   | TiDB + Monitor  |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

## Scale in a TiCDC node

If you want to remove the TiCDC node from the `10.0.1.4` host, take the following steps.

1. Take the node offline:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
    ```

2. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    Access the monitoring platform at <http://10.0.1.5:3000> using your browser, and view the status of the cluster.

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash + TiCDC  |
| 10.0.1.4   | TiDB + PD + **(TiCDC is deleted）**  |
| 10.0.1.5   | TiDB + Monitor  |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |
