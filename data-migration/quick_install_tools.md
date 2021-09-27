---
title: Install TiDB data migration tools
summary: Learn how to install TiDB data migration tools, including Data Migration, Dumpling, and TiDB Lightning.
---

# Install TiDB data migration tools

This document describes how to install data migration tools.

## Prerequisites

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

## Install TiUP and components

Since TiDB 4.0, TiUP serves as the package manager to help you easily manage different cluster components in the TiDB ecosystem. Now you can manage any components with only one single TiUP command line.

1. Install TiUP

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

Redeclare the global environment variables:

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

2. Install Components

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning dm dmctl
```

> **Note:**
>
> To install a component of a specific version, you can use the `tiup install <component>[:version]` command.

3. Update TiUP and components

{{< copyable "shell-regular" >}}

```shell
tiup update --self && tiup update dm
```

## Deploy DM cluster

According to the intended cluster topology, you need to manually create and edit the cluster initialization configuration file.

You need to create a YAML configuration file (named topology.yaml for example) according to the configuration file template. For other scenarios, edit the configuration accordingly.

You can use the command `tiup dm template > topology.yaml` to generate a configuration file template quickly.

The configuration of deploying three DM-masters, three DM-workers, and one monitoring component instance is as follows:

```yaml
# Global variables are applied to all deployments and as the default value of
# them if the specific deployment value missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/dm-deploy"
  data_dir: "/dm-data"

server_configs:
  master:
    log-level: info
    # rpc-timeout: "30s"
    # rpc-rate-limit: 10.0
    # rpc-rate-burst: 40
  worker:
    log-level: info

master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    # peer_port: 8291
    # deploy_dir: "/dm-deploy/dm-master-8261"
    # data_dir: "/dm-data/dm-master-8261"
    # log_dir: "/dm-deploy/dm-master-8261/log"
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      # rpc-timeout: "30s"
      # rpc-rate-limit: 10.0
      # rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
    ssh_port: 22
    port: 8261
  - host: 10.0.1.19
    name: master3
    ssh_port: 22
    port: 8261

worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    # deploy_dir: "/dm-deploy/dm-worker-8262"
    # log_dir: "/dm-deploy/dm-worker-8262/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.dm-worker` values
    config:
      log-level: info
  - host: 10.0.1.19
    ssh_port: 22
    port: 8262

monitoring_servers:
  - host: 10.0.1.13
    ssh_port: 22
    port: 9090
    # deploy_dir: "/tidb-deploy/prometheus-8249"
    # data_dir: "/tidb-data/prometheus-8249"
    # log_dir: "/tidb-deploy/prometheus-8249/log"

grafana_servers:
  - host: 10.0.1.14
    port: 3000
    # deploy_dir: /tidb-deploy/grafana-3000

alertmanager_servers:
  - host: 10.0.1.15
    ssh_port: 22
    web_port: 9093
    # cluster_port: 9094
    # deploy_dir: "/tidb-deploy/alertmanager-9093"
    # data_dir: "/tidb-data/alertmanager-9093"
    # log_dir: "/tidb-deploy/alertmanager-9093/log"

# if monitored is set, node_exporter and blackbox_exporter will be
# deployed with the port specified, otherwise they are not deployed
# on the server to avoid conflict with tidb clusters
#monitored:
#  node_exporter_port: 9100
#  blackbox_exporter_port: 9115
```

> **Note:**
>
> 1. It is not recommend running too many workers on one host, each worker is recommended to be allocated at least 1 core cpu and 2 GiB memory.
>
> 2. The worker will be bound with an upstream database, when DM performs a full replication task, the worker exporting the full amount of data locally first, and then importing it into the downstream database. Therefore, the worker's host needs sufficient storage space (The storage path is specified later when creating the task)

Now, you can start deploying the dm cluster.

```shell
tiup dm deploy ${name} ${version} ./topology.yaml -u ${ssh_user} [-p] [-i /home/root/.ssh/gcp_rsa]
```

The parameters used in this step is as follows.

|Parameter|Description|
|-|-|
|`${name}` | The name of dm cluster,eg: dm-test|
|`${version}` | The version of the DM cluster. You can see other supported versions by running tiup list dm-master.
|`./topology.yaml`| Path of topology config file.|
|`-u` or `--user`|Log in to the target machine through the root key to complete the cluster deployment, or you can use other users with ssh and sudo privileges to complete the deployment.|
|`-p` or `--password`|Password of target hosts. If specified, password authentication will be used|
|`-i` or `--identity_file`|The path of the SSH identity file. If specified, public key authentication will be used. (default "/root/.ssh/id_rsa")|

At the end of the output log, you will see `Deployed cluster dm-test successfully`. This indicates that the deployment is successful.

TiUP supports managing multiple DM clusters. The command below outputs information of all the clusters currently managed by TiUP, including the name, deployment user, version, and secret key information:

{{< copyable "shell-regular" >}}

```shell
tiup dm list
```

```bash
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  v2.0.3  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

You can start dm cluster with the following command

{{< copyable "shell-regular" >}}

```shell
tiup dm start dm-test
```

If the output log includes Started cluster `dm-test` successfully, the start is successful. Alternatively, you can also verify the running status by following command.

{{< copyable "shell-regular" >}}

```shell
tiup dm display dm-test
```

## Helpful topics

- [Deploy TiUP offline](/production-deployment-using-tiup.md)
- [Deploy TiDB Lightning manually](/tidb-lightning/deploy-tidb-lightning.md)
- [Download Dumpling and DM](/download-ecosystem-tools.md)
