---
title: Scale a Cluster with PD Microservices Using TiUP
summary: Learn how to scale a cluster with PD microservices using TiUP.
---

# Scale a Cluster with PD Microservices Using TiUP

This document describes how to scale a cluster with PD microservices enabled using TiUP, including how to add or remove TSO/Scheduling nodes using TiUP.

To view the current cluster name list, run `tiup cluster list`.

For example, assume that the original topology of the cluster is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |

## Add TSO/Scheduling nodes

This section exemplifies how to add a TSO node with the IP address `10.0.1.8` and a Scheduling node with the IP address `10.0.1.9`.

### 1. Configure the scale-out topology

> **Note:**
>
> - By default, the port and directory information is not required. However, in the case of multiple instances on a single machine, you need to allocate different ports and directories for these instances. If the ports or directories have conflicts, you will receive a notification during deployment or scaling.
> - Starting from TiUP v1.0.0, the scale-out configuration inherits the `global` configuration of the original cluster.

Add the scale-out topology configuration in the `scale-out.yml` file:

```shell
vi scale-out.yml
```

The following is the configuration example for the TSO node:

```ini
tso_servers:
  - host: 10.0.1.8
    port: 3379
```

The following is the configuration example for the Scheduling node:

```ini
scheduling_servers:
  - host: 10.0.1.9
    port: 3379
```

To view the configuration of the current cluster, run `tiup cluster edit-config <cluster-name>`. Because the parameter configuration of `global` and `server_configs` is inherited by `scale-out.yml`, it also takes effect in `scale-out.yml`.

### 2. Run the scale-out command

Before you run the `scale-out` command, use the `check` and `check --apply` commands to detect and automatically repair potential risks in the cluster:

1. Check for potential risks:

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. Enable automatic repair:

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3. Run the `scale-out` command:

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

In the preceding commands:

- `scale-out.yml` is the scale-out configuration file.
- `--user root` indicates logging in to the target machine as the `root` user to complete the cluster scale out. The `root` user is expected to have `ssh` and `sudo` privileges to the target machine. Alternatively, you can use other users with `ssh` and `sudo` privileges to complete the deployment.
- `[-i]` and `[-p]` are optional. If you have configured login to the target machine without a password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the root user (or other users specified by `--user`) that has access to the target machine. `[-p]` is used to input the user password interactively.

If you see `Scaled cluster <cluster-name> out successfully`, the scale-out operation succeeds.

### 3. Check the cluster status

```shell
tiup cluster display <cluster-name>
```

Access the monitoring platform at <http://10.0.1.5:3000> using your browser to monitor the status of the cluster and the new nodes.

After the scale-out, the cluster topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |
| 10.0.1.8   | TSO   |
| 10.0.1.9   | Scheduling   |

## Remove TSO/Scheduling nodes

This section exemplifies how to remove a TSO node with the IP address `10.0.1.8` and a Scheduling node with the IP address `10.0.1.9`.

### 1. View the node ID information

```shell
tiup cluster display <cluster-name>
```

```
Starting /root/.tiup/components/cluster/v1.16/cluster display <cluster-name>

TiDB Cluster: <cluster-name>

TiDB Version: v8.2.0

ID       Role         Host    Ports                            Status  Data Dir        Deploy Dir

--       ----         ----      -----                            ------  --------        ----------

10.0.1.4:2379  pd           10.0.1.4    2379/2380                        Healthy data/pd-2379      deploy/pd-2379

10.0.1.1:20160 tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

10.0.1.2:20160 tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

10.0.1.5:20160 tikv        10.0.1.5    20160/20180                     Up      data/tikv-20160     deploy/tikv-20160

10.0.1.4:4000  tidb        10.0.1.4    4000/10080                      Up      -                 deploy/tidb-4000

10.0.1.5:9090  prometheus   10.0.1.5    9090                             Up      data/prometheus-9090  deploy/prometheus-9090

10.0.1.5:3000  grafana      10.0.1.5    3000                             Up      -            deploy/grafana-3000

10.0.1.5:9093  alertmanager 10.0.1.5    9093/9094                        Up      data/alertmanager-9093 deploy/alertmanager-9093

10.0.1.6:3379  tso          10.0.1.6    3379                            Up|P     data/tso-3379     deploy/tso-3379

10.0.1.8:3379  tso          10.0.1.8    3379                            Up       data/tso-3379    deploy/tso-3379

10.0.1.7:3379  scheduling   10.0.1.7    3379                            Up|P     data/scheduling-3379     deploy/scheduling-3379

10.0.1.9:3379  scheduling   10.0.1.9    3379                            Up       data/scheduling-3379     deploy/scheduling-3379
```

### 2. Run scale-in commands

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379
tiup cluster scale-in <cluster-name> --node 10.0.1.9:3379
```

The `--node` parameter is the ID of the node to be taken offline.

If you see `Scaled cluster <cluster-name> in successfully`, the scale-in operation succeeds.

### 3. Check the cluster status

Run the following command to check if the nodes are successfully removed:

```shell
tiup cluster display <cluster-name>
```

Access the monitoring platform at <http://10.0.1.5:3000> using your browser to monitor the status of the entire cluster.

After the scale-in, the current topology is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |
