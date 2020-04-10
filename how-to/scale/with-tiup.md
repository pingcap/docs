---
title: Scale the TiDB Cluster Using TiUP
summary:
Category: how-to
---

# Scale the TiDB Cluster Using TiUP

The capacity of a TiDB cluster can be increased or decreased without affecting the online services.

This document describes how to scale the TiDB, TiKV, PD or TiFlash nodes using TiUP. If you have not installed TiUP, [install TiUP on the Control Machine](/how-to/upgrade/using-tiup.md#install-tiup-on-the-control-machine) and import the cluster into TiUP before you scale the TiDB cluster.

To view the current cluster name list, run `tiup cluster list`.

The following example shows the original topology of the cluster:

| Host IP | Service |
|:---|:----|
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD |
| 10.0.1.5 | TiKV + Monitor |
| 10.0.1.1 | TiKV |
| 10.0.1.2 | TiKV |

## 1. Scale out a TiDB/TiKV/PD node

If you want to add a TiDB node to the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to add the TiKV or PD node.

### 1.1 Configure the scale-out topology

> **Note:**
>
> * The port information is not required by default.
> * If the cluster is deployed on a single machine with multiple instances, you need to allocate different ports. If the ports or directories have conflicts, a notification is sent to you during deployment or scaling.

Add the scale-out topology configuration in the `scale-out.yaml` file:

{{< copyable "shell-regular" >}}

```shell
vi scale-out.yaml
```

```
tidb_servers:
 - host: 10.0.1.5
   ssh_port: 22
   port: 4000
   status_port: 10080
```

To view the whole configuration of the current cluster, run `tiup cluster edit-config <cluster-name>`. The global configuration in `global` and `server_configs` also takes effect in `scale-out.yaml`.

After the configuration, the current topology of the cluster is as follows:

| Host IP | Service |
|:---|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | **TiDB** + TiKV + Monitor   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

### 1.2 Run the scale-out command

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

If you see the `Scaled cluster <cluster-name> out successfully`, the scale-out operation is successfully completed.

### 1.3 Check the cluster status

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

Access the monitoring platform at <http://10.0.1.5:3200> using your browser to monitor the status of the cluster and the new node.

## 2. Scale out a TiFlash node

If you want to add a TiFlash node to the `10.0.1.4` host, take the following steps.

### 2.1 Add the node information to the `scale-out.yaml` file

Create the `scale-out.yaml` file to add the TiFlash node information.

{{< copyable "" >}}

```ini
tiflash_servers:
    - host: 10.0.1.4
```

Currently, you can only add IP but not domain name.

### 2.2 Run the scale-out command

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out <cluster-name> scale-out.yaml
```

### 2.3 View the cluster status

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

Access the monitoring platform at <http://10.0.1.5:3200> using your browser, and view the status of the cluster and the new node.

## 3. Scale in a TiDB/TiKV/PD node

If you want to remove a TiKV node from the `10.0.1.5` host, take the following steps.

> **Note:**
>
> You can take similar steps to remove the TiDB or PD node.

### 3.1 View the node ID information

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
10.0.1.4:2379   pd           10.0.1.4    2379/2380                        Healthy data/pd-2379            deploy/pd-2379
10.0.1.1:20160  tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
10.0.1.2:20160  tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
10.0.1.5:20160  tikv         10.0.1.5    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
10.0.1.3:4000   tidb         10.0.1.3    4000/10080                       Up      -                       deploy/tidb-4000
10.0.1.4:4000   tidb         10.0.1.4    4000/10080                       Up      -                       deploy/tidb-4000
10.0.1.5:4000   tidb         10.0.1.5    4000/10080                       Up      -                       deploy/tidb-4000
10.0.1.3:9000   tiflash      10.0.1.3    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
10.0.1.4:9000   tiflash      10.0.1.4    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
10.0.1.5:9290   prometheus   10.0.1.5    9290                             Up      data/prometheus-9290    deploy/prometheus-9290
10.0.1.5:3200   grafana      10.0.1.5    3200                             Up      -                       deploy/grafana-3200
10.0.1.5:9293   alertmanager 10.0.1.5    9293/9294                        Up      data/alertmanager-9293  deploy/alertmanager-9293
```

### 3.2 Run the scale-in 

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
```

The `--node` parameter is the ID of the node to be taken offline.

If you see the `Scaled cluster <cluster-name> in successfully`, the scale-in operation is successfully completed.

### 3.3 Check the cluster status

The offline process takes some time. If the node to be scaled in becomes `Tombstone`, that means the offline operation is successful.

To check the offline status, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

The current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.3   | TiDB + TiFlash   |
| 10.0.1.4   | TiDB + PD + TiFlash   |
| 10.0.1.5   | TiDB + Monitor **(TiKV is deleted)**   |
| 10.0.1.1   | TiKV    |
| 10.0.1.2   | TiKV    |

Access the monitoring platform at <http://10.0.1.5:3200> using your browser to monitor the status of the cluster.

## 4. Scale in a TiFlash node

If you want to remove the TiFlash node from the `10.0.1.4` host, take the following steps.

> **Note:**
>
> The offline process described in this section does not delete the data on the offline node. If you need to take the node online again, delete the data manually.

### 4.1 Take the node offline

Take down the node to be scaled in. See [Take a TiFlash node down](/reference/tiflash/maintain.md#take-a-tiflash-node-down) for details.

### 4.2 Check the node status

Check whether the node has been offline successfully using Grafana or pd-ctl (the offline process takes some time).

### 4.3 Shutdown the TiFlash process

After the `store` corresponding to TiFlash disappears, or the `state_name` becomes `Tombstone`, execute the following command to shutdown the TiFlash process:

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
```

### 4.4 View the cluster status

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

Access the monitoring platform at <http://10.0.1.5:3200> using your browser, and view the status of the cluster.
