---
title: Scale PD Microservice Nodes Using TiUP
summary: Learn how to scale PD microservice nodes in a cluster using TiUP and how to switch the PD working mode.
---

# Scale PD Microservices Nodes Using TiUP

This document describes how to scale [PD microservice](/pd-microservices.md) nodes (including TSO and Scheduling nodes) in a cluster and how to switch the PD working mode using TiUP.

To view the current cluster name list, run `tiup cluster list`.

For example, the original topology of the cluster is as follows:

| Host IP   | Service   |
|:----|:----|
| 10.0.1.4   | TiDB + PD   |
| 10.0.1.5   | TiKV + Monitor   |
| 10.0.1.1   | TiKV   |
| 10.0.1.2   | TiKV   |
| 10.0.1.6   | TSO   |
| 10.0.1.7   | Scheduling   |

## Add TSO/Scheduling nodes

> **Note:**
>
> To add TSO/Scheduling nodes to a TiDB cluster that have not enabled PD microservices yet, follow the instructions in [Switch from regular mode to microservices mode](#switch-from-regular-mode-to-microservices-mode) instead.

This section exemplifies how to add a TSO node (at IP address `10.0.1.8`) and a Scheduling node (at IP address `10.0.1.9`) to a TiDB cluster with PD microservices enabled.

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

> **Note:**
>
> For a cluster with PD microservices enabled, if you need to switch it to non-microservice mode, follow the instructions in [Switch from microservices mode to regular mode](#switch-from-microservices-mode-to-regular-mode) instead.

This section exemplifies how to remove a TSO node (at IP address `10.0.1.8`) and a Scheduling node (at IP address `10.0.1.9`) from a TiDB cluster with multiple TSO or Scheduling nodes.

### 1. View the node ID information

```shell
tiup cluster display <cluster-name>
```

```
Starting /root/.tiup/components/cluster/v1.16/cluster display <cluster-name>

TiDB Cluster: <cluster-name>

TiDB Version: v8.5.0

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

## Switch the PD working mode

You can switch PD services between the following two working modes:

- Regular mode: provides routing service, timestamp allocation, and cluster scheduling functions solely by PD nodes.
- Microservice mode: enables you to deploy the PD timestamp allocation function to TSO nodes (providing `tso` microservices) and the cluster scheduling function to Scheduling nodes (providing `scheduling` microservices) separately. In this way, these two functions are decoupled from the routing function of PD, which allows PD nodes to focus on the routing service for metadata.

> **Note:**
>
> During the mode switching, PD services will be unavailable for a few minutes.

### Switch from regular mode to microservices mode

For a cluster that has not enabled PD microservices, you can switch it to PD microservice mode and add a TSO node (at IP address `10.0.1.8`) and a Scheduling node (at IP address `10.0.1.9`) to it as follows:

1. Add the scale-out topology configuration in the `scale-out.yml` file:

    ```shell
    vi scale-out.yml
    ```

    The following is a configuration example:

    ```ini
    tso_servers:
      - host: 10.0.1.8
        port: 3379
    scheduling_servers:
      - host: 10.0.1.9
        port: 3379
    ```

2. Modify the cluster configuration and switch the cluster to PD microservice mode:

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    Add `pd_mode: ms` to `global`:

    ```ini
    global:
      user: tidb
       ssh_port: 22
       listen_host: 0.0.0.0
       deploy_dir: /tidb-deploy
       data_dir: /tidb-data
       os: linux
       arch: amd64
       systemd_mode: system
       pd_mode: ms
    ```

3. Perform a rolling update of the PD node configuration:

    ```shell
    tiup cluster reload <cluster-name> -R pd
    ```

    > **Note:**
    >
    > The PD timestamp allocation service will be unavailable after you run the preceding `reload` command and will be available again once the `scale-out` command in the next step completes execution.

4. Run the `scale-out` command to add PD microservice nodes:

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

### Switch from microservices mode to regular mode

For a cluster with PD microservices enabled (assume that it has a TSO node at IP address `10.0.1.8` and a Scheduling node at IP address `10.0.1.9`), you can switch it to non-microservice mode as follows:

1. Modify the cluster configuration and switch the cluster to non-microservice mode:

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    Remove `pd_mode: ms` from `global`:

    ```ini
    global:
      user: tidb
       ssh_port: 22
       listen_host: 0.0.0.0
       deploy_dir: /tidb-deploy
       data_dir: /tidb-data
       os: linux
       arch: amd64
       systemd_mode: system
    ```

2. Run the `scale-in` command to remove all PD microservice nodes:

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379,10.0.1.9:3379
    ```

    > **Note:**
    >
    > The PD timestamp allocation service will be unavailable after you run the preceding `scale-in` command and will be available again once the `reload` command in the next step completes execution.

3. Perform a rolling update of the PD node configuration:

    ```shell
    tiup cluster reload <cluster-name> -R pd
    ```