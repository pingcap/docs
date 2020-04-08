---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to deploy a TiDB cluster easily using TiUP.
category: how-to
---

# Deploy a TiDB Cluster Using TiUP

## Stop a cluster

To stop the `tidb-test` cluster, run the following command:

{{< copyable "shell-regular" >}}

```shell
cluster stop tidb-test
```

The expected output is as follows. `Stopped cluster tidb-test successfully` indicates the cluster is successfully stopped.

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster stop tidb-test
+ [ Serial ] - SSHKeySet: privateKey=/home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa, publicKey=/home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa.pub
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.5
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.5
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.2
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.1
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [ Serial ] - ClusterOperate: operation=StopOperation, options={Roles:[] Nodes:[] Force:false}
Stopping component alertmanager
    Stopping instance 10.0.1.4
    Stop alertmanager 10.0.1.4:9104 success

...... Omit some logs ......

Checking service state of pd
    10.0.1.5
           Active: inactive (dead) since Saturday 2020-04-04 15:35:42 CST; 15s ago
Checking service state of tikv
    10.0.1.1
           Active: inactive (dead) since Saturday 2020-04-04 15:35:21 CST; 38s ago
    10.0.1.2
           Active: inactive (dead) since Saturday 2020-04-04 15:35:23 CST; 37s ago
    10.0.1.3
           Active: inactive (dead) since Saturday 2020-04-04 15:35:24 CST; 37s ago
Checking service state of tidb
    10.0.1.5
           Active: inactive (dead) since Saturday 2020-04-04 15:35:15 CST; 49s ago
Checking service state of prometheus
    10.0.1.4
           Active: inactive (dead) since Saturday 2020-04-04 15:35:12 CST; 53s ago
Checking service state of grafana
    10.0.1.4
           Active: inactive (dead) since Saturday 2020-04-04 15:35:10 CST; 56s ago
Checking service state of alertmanager
    10.0.1.4
           Active: inactive (dead) since Saturday 2020-04-04 15:35:09 CST; 59s ago
Stopped cluster `tidb-test` successfully
```

## Destroy a cluster

> **Warning:**
>
> Perform this operation carefully in a production environment. The cleanup task cannot be rolled back after this operation is confirmed.

To destroy the `tidb-test` cluster, including data and services, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster destroy tidb-test
```

The expected output is as follows. `Destroy cluster tidb-test successfully` indicates the cluster is successfully destroyed.

```log
Starting /home/tidb/.tiup/components/cluster/v0.4.3/cluster destroy tidb-test
This operation will destroy TiDB v4.0.0-beta.2 cluster tidb-test and its data.
Do you want to continue? [y/N]: y
Destroying cluster...
+ [ Serial ] - SSHKeySet: privateKey=/home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa, publicKey=/home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa.pub
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.2
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.1
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [Parallel] - UserSSH: user=tidb, host=10.0.1.4
+ [ Serial ] - ClusterOperate: operation=StopOperation, options={Roles:[] Nodes:[] Force:false}
Stopping component alertmanager
    Stopping instance 10.0.1.4
    Stop alertmanager 10.0.1.4:9104 success

...... Omit some logs ......

    Destroy monitored on 10.0.1.1 success
Destroying monitored 10.0.1.2
Destroying monitored
    Destroying instance 10.0.1.2
Destroy monitored on 10.0.1.2 success
Destroying monitored 10.0.1.4
Destroying monitored
    Destroying instance 10.0.1.4
Destroy monitored on 10.0.1.4 success
Destroying component pd
Destroying instance 10.0.1.4
Deleting paths on 10.0.1.4: /tidb-data/pd-2379 /tidb-deploy/pd-2379 /tidb-deploy/pd-2379/log /etc/systemd/system/pd-2379.service
Destroy 10.0.1.4 success
Destroying monitored 10.0.1.4
Destroying monitored
    Destroying instance 10.0.1.4
Destroy monitored on 10.0.1.4 success
Destroyed cluster `tidb-test` successfully
```

## Deployment FAQs

This section describes common problems and solutions when you deploy TiDB clusters using TiUP.

### Default port

| Component | Port variable | Default port | Description |
| :-- | :-- | :-- | :-- |
| TiDB | port | 4000  | the communication port for the application and DBA tools |
| TiDB | status_port | 10080  | the communication port to report TiDB status |
| TiKV | port | 20160 | the TiKV communication port |
| TiKV | status_port   | 20180   | the communication port to report the TiKV status |
| PD | client_port | 2379 | the communication port between TiDB and PD |
| PD | peer_port | 2380 | the inter-node communication port within the PD cluster |
| Pump | port | 8250  | the Pump communication port |
| Drainer | port | 8249 | the Drainer communication port |
| Prometheus | port | 9090 | the communication port for the Prometheus service |
| Node_exporter | node_exporter_port | 9100 | the communication port to report the system information of every TiDB cluster node |
| Blackbox_exporter | blackbox_exporter_port | 9115 | the Blackbox_exporter communication port，used to monitor ports in a TiDB cluster |
| Grafana | grafana_port |  3000 | the port for the external web monitoring service and client (Browser) access |
| Alertmanager | web_port | 9093 | the port for the web monitoring service |
| Alertmanager | cluster_port | 9094 | the monitoring communication port |

### Default directory

| Module | Directory variable | Default directory | Description |
| :-- | :-- | :-- | :-- |
| Global | `deploy_dir` | `/home/tidb/deploy` | deployment directory |
| Global | `data_dir` | `/home/tidb/data` | data directory |
| Global | `log_dir` | `/home/tidb/deploy/log` | log directory |
| Monitored | `deploy_dir` | `/home/tidb/data` | deployment directory |
| Monitored | `data_dir` | `/home/tidb/deploy` | data directory |
| Monitored | `log_dir` | `/home/tidb/deploy` | log directory |
| Instance | `deploy_dir` | inherit global configuration | deployment directory |
| Instance | `data_dir` | inherit global configuration | data directory |
| Instance | `log_dir` | inherit global configuration | log directory |

### Parameter module configuration

This section describes the parameter module configuration in descending order.

#### 1. Instance parameter module

Taking the TiDB server as an example, the configuration of the instance parameter module (instances split by `- host`) is applied to the target node with the highest priority.

- The `config` configuration in the instance takes precedence over the `server_configs` parameter module configuration.
- The `ssh_port`, `deploy_dir`, `log_dir` configurations in the instance take precedence over the `global` parameter module configuration.

```yaml
tidb_servers:
  - host: 10.0.1.11
    ssh_port: 22
    port: 4000
    status_port: 10080
    deploy_dir: "deploy/tidb-4000"
    log_dir: "deploy/tidb-4000/log"
    numa_node: "0,1"
    # Config is used to overwrite the `server_configs.tidb` values
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwritten.log
```

#### 2. `global`, `server_configs`, `monitored` parameter modules

- The configuration in the `global` parameter module is global configuration and its priority is lower than that of the instance parameter module.

    ```yaml
    global:
    user: "tidb"
    ssh_port: 22
    deploy_dir: "deploy"
    data_dir: "data"
    ```

- The configuration of the `server_configs` parameter module applies to global monitoring and its priority is lower than that of the instance parameter module.

    ```yaml
    server_configs:
    tidb:
        binlog.enable: false
        binlog.ignore-error: false
    tikv:
        readpool.storage.low-concurrency: 8
        server.labels:
        zone: sh
        dc: sha
        rack: rack1
        host: host1
    pd:
        replication.enable-placement-rules: true
        label-property:
        reject-leader:
            - key: "dc"
            value: "bja"
    pump:
        gc: 7
    ```

- The configuration of the `monitored` parameter module applies to the monitored host. The default ports are `9100` and `9115`. If the directory is configured, it will be deployed to the user's `/home` directory by default. For example, if the `user` in the `global` parameter module is `"tidb"`, then it will be deployed to the `/home/tidb` directory.

    ```yaml
    # Monitored variables are used to
    monitored:
    node_exporter_port: 9100
    blackbox_exporter_port: 9115
    deploy_dir: "deploy/monitored-9100"
    data_dir: "data/monitored-9100"
    log_dir: "deploy/monitored-9100/log"
    ```

### How to check whether the NTP service is normal

1. Run the following command. If it returns `running`, then the NTP service is running.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

2. Run the `ntpstat` command. If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    synchronised to NTP server (85.199.214.101) at stratum 2
    time correct to within 91 ms
    polling server every 1024 s
    ```

    > **Note:**
    >
    > For the Ubuntu system, you need to install the `ntpstat` package.

- The following condition indicates the NTP service is not synchronizing normally:

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    unsynchronised
    ```

- The following condition indicates the NTP service is not running normally:

    {{< copyable "shell-regular" >}}

    ```bash
    ntpstat
    ```

    ```
    Unable to talk to NTP daemon. Is it running?
    ```

- To make the NTP service start synchronizing as soon as possible, run the following command. Replace `pool.ntp.org` with your NTP server.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop ntpd.service && \
    sudo ntpdate pool.ntp.org && \
    sudo systemctl start ntpd.service
    ```

- To install the NTP service manually on the CentOS 7 system, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum install ntp ntpdate && \
    sudo systemctl start ntpd.service && \
    sudo systemctl enable ntpd.service
    ```

### How to manually configure the SSH mutual trust and sudo without password

1. Log in to the deployment target machine respectively using the `root` user account, create the `tidb` user and set the login password.

    {{< copyable "shell-root" >}}

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2. To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

    {{< copyable "shell-root" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. Use the `tidb` user to log in to the Control Machine, and run the following command. Replace `10.0.1.1` with the IP of your deployment target machine, and enter the `tidb` user password of the deployment target machine as prompted. Successful execution indicates that SSH mutual trust is already created. This applies to other machines as well.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. Log in to the Control Machine using the `tidb` user account, and log in to the IP of the target machine using `ssh`. If you do not need to enter the password and can successfully log in, then the SSH mutual trust is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. After you login to the deployment target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

### How to stop the firewall service of deployment machines

1. Check the firewall status. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. Stop the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. Disable automatic start of the firewall service.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. Check the firewall status.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo systemctl status firewalld.service
    ```

### How to install the `numactl` tool

> **Note:**
>
> - Binding cores using NUMA is a method to isolate CPU resources and is suitable for deploying multiple instances on highly configured physical machines.
> - After completing deployment using `tiup cluster deploy`, you can use the `exec` command to perform cluster level management operations.

1. Log in to the target node to install. Take CentOS Linux release 7.7.1908 (Core) as an example.

    {{< copyable "shell-regular" >}}

    ```bash
    sudo yum -y install numactl
    ```

2. Run the `exec` command using `tiup cluster` to install in batches.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec --help
    ```

    ```
    Run shell command on host in the tidb cluster

    Usage:
    cluster exec <cluster-name> [flags]

    Flags:
        --command string   the command run on cluster host (default "ls")
    -h, --help             help for exec
        --sudo             use root permissions (default false)
    ```

    To use the sudo privilege to execute the installation command for all the target machines in the `tidb-test` cluster, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```
