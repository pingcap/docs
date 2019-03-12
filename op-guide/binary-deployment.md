---
title: Deploy TiDB Using the Binary
category: operations
---

# Deploy TiDB Using the Binary

## Overview

The following guide provides installation instructions from tarball on Linux. A complete TiDB cluster contains PD, TiKV, and TiDB. To start the database service, follow the order of PD -> TiKV -> TiDB. To stop the database service, follow the order of stopping TiDB -> TiKV -> PD.

Before you start, see [TiDB architecture](../overview.md#tidb-architecture) and [Software and Hardware Requirements](op-guide/recommendation.md).

This document describes the binary deployment of three scenarios:

1. [Single node cluster deployment](#single-node-cluster-deployment) for trying out TiDB.
2. [Multiple nodes cluster deployment for testing](#multiple-nodes-cluster-deployment-for-test) TiDB across multiple nodes and exploring features in more detail.
3. [Multiple nodes cluster deployment](#multiple-nodes-cluster-deployment) for production deployments.

## TiDB components and default ports

### TiDB database components (required)

See the following table for the default ports for the TiDB components:

| Component | Default Port | Protocol | Description |
| :-- | :-- | :-- | :----------- |
| ssh | 22 | TCP | sshd service |
| TiDB|  4000  | TCP | the communication port for the application and DBA tools |
| TiDB| 10080  |  TCP | the communication port to report TiDB status |
| TiKV|  20160 |  TCP | the TiKV communication port  |
| PD | 2379 | TCP | the communication port between TiDB and PD |
| PD | 2380 | TCP | the inter-node communication port within the PD cluster |

### TiDB database components (optional)

See the following table for the default ports for the optional TiDB components:

| Component | Default Port | Protocol | Description |
| :-- | :-- | :-- | :------------------------ |
| Prometheus |  9090| TCP | the communication port for the Prometheus service |
| Pushgateway |  9091 | TCP | the aggregation and report port for TiDB, TiKV, and PD monitor |
| Node_exporter|  9100| TCP | the communication port to report the system information of every TiDB cluster node |
| Grafana | 3000 | TCP | the port for the external Web monitoring service and client (Browser) access |
| alertmanager | 9093 | TCP | the port for the alert service |

## Configure and check the system before installation

### Operating system
For the operating system, it is recommended to use RHEL/CentOS 7.3 or higher. The following additional requirements are recommended:
| Configuration | Description |
| :-- | :-------------------- |
| Supported Platform | RHEL/CentOS 7.3+ ([more details](./recommendation.md) |
| File System  |  ext4 is recommended |
| Swap Space  |  Should be disabled  |
| Disk Block Size  |  Set the system disk `Block` size to `4096` |

### Network and firewall

| Configuration | Description |
| :-- | :------------------- |
| Firewall / Port | Check whether the ports required by TiDB are accessible between the nodes |

### Operating system parameters

| Configuration | Description |
| :-- | :-------------------------- |
| Nice Limits | For system users, set the default value of `nice` in TiDB to `0` |
| min_free_kbytes | The setting for `vm.min_free_kbytes` in `sysctl.conf` needs to be high enough |
| User Open Files Limit | For database administrators, set the number of TiDB open files to `1000000` |
| System Open File Limits | Set the number of system open files to `1000000` |
| User Process Limits | For TiDB users, set the `nproc` value to `4096` in `limits.conf` |
| Address Space Limits | For TiDB users, set the space to `unlimited` in `limits.conf` |
| File Size Limits | For TiDB users, set the `fsize` value to `unlimited` in `limits.conf` |
| Disk Readahead | Set the value of the `readahead` data disk to `4096` at a minimum |
| NTP service | Configure the NTP time synchronization service for each node |
| SELinux  | Turn off the SELinux service for each node |
| CPU Frequency Scaling | It is recommended to turn on CPU overclocking |
| Transparent Hugepages | For Red Hat 7+ and CentOS 7+ systems, it is required to set the Transparent Hugepages to `always` |
| I/O Scheduler | Set the I/O Scheduler of data disks to the `deadline` mode |
| vm.swappiness | Set `vm.swappiness = 0` |


> **Note**: To adjust the operating system parameters, contact your system administrator.

### Database running user

| Configuration | Description |
| :-- | :---------------------------- |
| LANG environment | Set `LANG = en_US.UTF8` |
| TZ time zone | Set the TZ time zone of all nodes to the same value |

## Create the database running user account

In the Linux environment, create TiDB on each installation node as a database running user, and set up the SSH mutual trust between cluster nodes. To create a running user and open SSH mutual trust, contact the system administrator. Here is an example:

```bash
$ useradd tidb
$ usermod -a -G tidb tidb
$ su - tidb
Last login: Tue Aug 22 12:06:23 CST 2017 on pts/2
-bash-4.2$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/tidb/.ssh/id_rsa):
Created directory '/home/tidb/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/tidb/.ssh/id_rsa.
Your public key has been saved in /home/tidb/.ssh/id_rsa.pub.
The key fingerprint is:
5a:00:e6:df:9e:40:25:2c:2d:e2:6e:ee:74:c6:c3:c1 tidb@t001
The key's randomart image is:
+--[ RSA 2048]----+
|    oo. .        |
|  .oo.oo         |
| . ..oo          |
|  .. o o         |
| .  E o S        |
|  oo . = .       |
| o. * . o        |
| ..o .           |
| ..              |
+-----------------+

-bash-4.2$ cd .ssh
-bash-4.2$ cat id_rsa.pub >> authorized_keys
-bash-4.2$ chmod 644 authorized_keys
-bash-4.2$ ssh-copy-id -i ~/.ssh/id_rsa.pub 192.168.1.100
```

## Download the official binary package



```
# Download the package.
$ wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
$ wget http://download.pingcap.org/tidb-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
$ sha256sum -c tidb-latest-linux-amd64.sha256

# Extract the package.
$ tar -xzf tidb-latest-linux-amd64.tar.gz
$ cd tidb-latest-linux-amd64
```

## Single node cluster deployment

After downloading the TiDB binary package, you can run and test the TiDB cluster on a standalone server. Follow the steps below to start PD, TiKV and TiDB:

1. Start PD.

    ```bash
    $ ./bin/pd-server --data-dir=pd \
                    --log-file=pd.log &
    ```


2. Start TiKV.

    ```bash
    $ ./bin/tikv-server --pd="127.0.0.1:2379" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="127.0.0.1:2379" \
                      --log-file=tidb.log &
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

## Multiple nodes cluster deployment for test

If you want to test TiDB but have a limited number of nodes, you can use one PD instance to test the entire cluster.

Assuming that you have four nodes, you can deploy 1 PD instance, 3 TiKV instances, and 1 TiDB instance. See the following table for details:

| Name | Host IP | Services |
| :-- | :-- | :------------------- |
| Node1 | 192.168.199.113 | PD1, TiDB |
| Node2 | 192.168.199.114 | TiKV1 |
| Node3 | 192.168.199.115 | TiKV2 |
| Node4 | 192.168.199.116 | TiKV3 |

Follow the steps below to start PD, TiKV and TiDB:

1. Start PD on Node1.

    ```bash
    $ ./bin/pd-server --name=pd1 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380" \
                    --log-file=pd.log &
    ```

2. Start TiKV on Node2, Node3 and Node4.

    ```bash
    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.114:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.115:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.116:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB on Node1.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379" \
                      --log-file=tidb.log
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

## Multiple nodes cluster deployment

For the production environment, multiple nodes cluster deployment is recommended. Before you begin, see [Software and Hardware Requirements](./recommendation.md).

Assuming that you have six nodes, you can deploy 3 PD instances, 3 TiKV instances, and 1 TiDB instance. See the following table for details:

| Name  | Host IP | Services |
| :-- | :-- | :-------------- |
| Node1 | 192.168.199.113| PD1, TiDB |
| Node2 | 192.168.199.114| PD2 |
| Node3 | 192.168.199.115| PD3 |
| Node4 | 192.168.199.116| TiKV1 |
| Node5 | 192.168.199.117| TiKV2 |
| Node6 | 192.168.199.118| TiKV3 |

Follow the steps below to start PD, TiKV, and TiDB:

1. Start PD on Node1, Node2, and Node3 in sequence.

    ```bash
    $ ./bin/pd-server --name=pd1 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &

    $ ./bin/pd-server --name=pd2 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.114:2379" \
                    --peer-urls="http://192.168.199.114:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &

    $ ./bin/pd-server --name=pd3 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.115:2379" \
                    --peer-urls="http://192.168.199.115:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &
    ```

2. Start TiKV on Node4, Node5 and Node6.

    ```bash
    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.116:20160" \
                      --status-addr="192.168.199.116:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.117:20160" \
                      --status-addr="192.168.199.117:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.118:20160" \
                      --status-addr="192.168.199.118:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB on Node1.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --log-file=tidb.log &
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

> **Note**:
>
> - If you start TiKV or deploy PD in the production environment, it is highly recommended to specify the path for the configuration file using the `--config` parameter. If the parameter is not set, TiKV or PD does not read the configuration file.
> - To tune TiKV, see [Performance Tuning for TiKV](./tune-TiKV.md).
> - If you use `nohup` to start the cluster in the production environment, write the startup commands in a script and then run the script. If not, the `nohup` process might abort because it receives exceptions when the Shell command exits. For more information, see [The TiDB/TiKV/PD process aborts unexpectedly](../trouble-shooting.md#the-tidbtikvpd-process-aborts-unexpectedly).

## TiDB monitor and alarm deployment

To install and deploy the environment for TiDB monitor and alarm service, see the following table for the system information:

| Name  | Host IP | Services |
| :-- | :-- | :-------------- |
| Node1 | 192.168.199.113| PD1, TiDB, node_export, Prometheus, Grafana |
| Node2 | 192.168.199.114| PD2, node_export |
| Node3 | 192.168.199.115| PD3, node_export |
| Node4 | 192.168.199.116| TiKV1, node_export |
| Node5 | 192.168.199.117| TiKV2, node_export |
| Node6 | 192.168.199.118| TiKV3, node_export |

### Download the binary package

```
# Download the package.
$ wget https://github.com/prometheus/prometheus/releases/download/v2.2.1/prometheus-2.2.1.linux-amd64.tar.gz
$ wget https://github.com/prometheus/node_exporter/releases/download/v0.15.2/node_exporter-0.15.2.linux-amd64.tar.gz
$ wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.6.3.linux-x64.tar.gz

# Extract the package.
$ tar -xzf prometheus-2.2.1.linux-amd64.tar.gz
$ tar -xzf node_exporter-0.15.2.linux-amd64.tar.gz
$ tar -xzf grafana-4.6.3.linux-x64.tar.gz
```

### Start the monitor service

####  Start `node_exporter` on Node1, Node2, Node3 and Node4.

```
$ cd node_exporter-0.15.2.linux-amd64

# Start the node_exporter service.
$ ./node_exporter --web.listen-address=":9100" \
    --log.level="info" &
```


#### Start Prometheus in Node1.

```
$ cd prometheus-2.2.1.linux-amd64

# Edit the Configuration file:

$ vi prometheus.yml

...
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default (10s).
  external_labels:
    cluster: 'test-cluster'
    monitor: "prometheus"

scrape_configs:
  - job_name: "overwritten-nodes"
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
    - targets:
      - '192.168.199.113:9100'
      - '192.168.199.114:9100'
      - '192.168.199.115:9100'
      - '192.168.199.116:9100'
      - '192.168.199.117:9100'
      - '192.168.199.118:9100'

  - job_name: "tidb"
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
    - targets:
      - '192.168.199.113:10080'

  - job_name: "pd"
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
    - targets:
      - '192.168.199.113:2379'
      - '192.168.199.114:2379'
      - '192.168.199.115:2379'

  - job_name: "tikv"
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
    - targets:
      - '192.168.199.116:20180'
      - '192.168.199.117:20180'
      - '192.168.199.118:20180'
...

# Start Prometheus:
$ ./prometheus \
    --config.file="./prometheus.yml" \
    --web.listen-address=":9090" \
    --web.external-url="http://192.168.199.113:9090/" \
    --web.enable-admin-api \
    --log.level="info" \
    --storage.tsdb.path="./data.metrics" \
    --storage.tsdb.retention="15d" &
```

#### Start Grafana in Node1.

```
$ cd grafana-4.6.3

# Edit the Configuration file:

$ vi conf/grafana.ini

...

[paths]
data = ./data
logs = ./data/log
plugins = ./data/plugins
[server]
http_port = 3000
domain = 192.168.199.113
[database]
[session]
[analytics]
check_for_updates = true
[security]
admin_user = admin
admin_password = admin
[snapshots]
[users]
[auth.anonymous]
[auth.basic]
[auth.ldap]
[smtp]
[emails]
[log]
mode = file
[log.console]
[log.file]
level = info
format = text
[log.syslog]
[event_publisher]
[dashboards.json]
enabled = false
path = ./data/dashboards
[metrics]
[grafana_net]
url = https://grafana.net

...

# Start the Grafana service:
$ ./bin/grafana-server \
    --config="./conf/grafana.ini"
```
