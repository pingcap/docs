---
title: Quick Start Guide for the TiDB Database Platform
summary: Learn how to quickly get started with the TiDB platform and see if TiDB is the right choice for you.
aliases: ['/docs/dev/quick-start-with-tidb/','/docs/dev/test-deployment-using-docker/']
---

# Quick Start Guide for the TiDB Database Platform

> **Warning:**
>
> For production environments, **do not** deploy TiDB with the following three methods. Instead, it is recommended that you [deploy TiDB using TiUP](/production-deployment-using-tiup.md).

This document describes how to try out TiDB, a distributed SQL database, in a few minutes. You can choose any of the following three methods to get started with the TiDB database platform:

- [Deploy a local test environment using TiUP Playground](#deploy-a-local-test-environment-using-tiup-playground)
- [Set up a test environment on a single machine using TiUP Cluster](#set-up-a-test-environment-on-a-single-machine-using-tiup-cluster)
- [Try out TiDB with one click using TiDB-Wasm](#try-out-tidb-with-one-click-using-tidb-wasm)

## Deploy a local test environment using TiUP Playground

- Scenario: Quickly deploy a TiDB cluster on a local Mac or Linux OS machine. You can see the basic architecture of TiDB and how TiDB, TiKV, PD, monitoring, and other components run in a TiDB cluster.
- Time required: 1 minute

As a distributed system, a basic TiDB test cluster usually consists of 2 TiDB instances, 3 TiKV instances, and 3 PD instances. With TiUP Playground, you can quickly build the above test cluster by taking the following steps:

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding `profile` file. You need to modify the following `source` command according to the path.

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. Start the cluster in the current session:

    - If you want to start a TiDB cluster of the latest version with 1 TiDB instance, 1 TiKV instance, and 1 PD instance, run the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - If you want to specify the TiDB version and the number of the instances of each component, run a command like this:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v4.0.0 --db 2 --pd 3 --kv 3 --monitor
        ```

        The command downloads a v4.0.0 cluster to the local machine and starts it. `--monitor` means that the monitoring component is also deployed.

        To view the latest version, run `tiup list tidb`.

        This command returns the access methods of the cluster:

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root
        To connect TiDB: mysql --host 127.0.0.1 --port 4001 -u root
        To view the dashboard: http://127.0.0.1:2379/dashboard
        To view the monitor: http://127.0.0.1:9090
        ```

4. Start a new session to access TiDB:

    {{< copyable "shell-regular" >}}

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root
    ```

5. Access the Prometheus dashboard of TiDB at <http://127.0.0.1:9090>.

6. Access the TiDB Dashboard at <http://127.0.0.1:2379/dashboard>. The default username is `root`, with an empty password.

7. After the test, you can clean the cluster by taking the following steps:

    1. Stop the process by pressing `ctrl-c`.

    2. Run the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup clean --all
        ```

## Set up a test environment on a single machine using TiUP cluster

- Scenario: Experience a smallest TiDB cluster with the complete topology and simulate the production deployment steps on a single Linux server.
- Time required: 10 minutes

This section describes how to deploy a TiDB cluster using a YAML file of the smallest topology in TiUP.

### Prepare

Prepare a target machine that meets the following requirements:

- CentOS 7.3 or a later version is installed
- The Linux OS has access to the Internet, which is required to download TiDB and related software installation packages

The smallest TiDB cluster topology is as follows:

| Instance | Count | IP | Configuration |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 <br/> 10.0.1.1 <br/> 10.0.1.1 | Avoid conflict between the port and the directory |
| TiDB | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| PD | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| TiFlash | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| Monitor | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |

Other requirements for the target machine:

- The `root` user and its password is required
- [Stop the firewall service of the target machine](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines), or open the port needed by the TiDB cluster nodes
- Currently, TiUP only supports deploying TiDB on the x86_64 (AMD64) architecture (the ARM architecture will be supported in TiDB 4.0 GA):

    - It is recommended to use CentOS 7.3 or later versions on AMD64
    - It is recommended to use CentOS 7.6 1810 on ARM

### Deploy

> **Note:**
>
> You can log in to the target machine as a regular user or the `root` user. The following steps use the `root` user as an example.

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Install the cluster component of TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. If the TiUP cluster is already installed on the machine, update the software version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

4. Use the `root` user privilege to increase the connection limit of the `sshd` service. This is because TiUP needs to simulate deployment on multiple machines.

    1. Modify `/etc/ssh/sshd_config`, and set `MaxSessions` to `20`.
    2. Restart the `sshd` service:

        {{< copyable "shell-regular" >}}

        ```shell
        service sshd restart
        ```

5. Create and start the cluster:

    Edit the configuration file according to the following template, and name it as `topo.yaml`:

    {{< copyable "shell-regular" >}}

    ```yaml
    # # Global variables are applied to all deployments and used as the default value of
    # # the deployments if a specific deployment value is missing.
    global:
     user: "tidb"
     ssh_port: 22
     deploy_dir: "/tidb-deploy"
     data_dir: "/tidb-data"

    # # Monitored variables are applied to all the machines.
    monitored:
     node_exporter_port: 9100
     blackbox_exporter_port: 9115

    server_configs:
     tidb:
       log.slow-threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
     tiflash:
       logger.level: "info"

    pd_servers:
     - host: 10.0.1.1

    tidb_servers:
     - host: 10.0.1.1

    tikv_servers:
     - host: 10.0.1.1
       port: 20160
       status_port: 20180

     - host: 10.0.1.1
       port: 20161
       status_port: 20181

     - host: 10.0.1.1
       port: 20162
       status_port: 20182

    tiflash_servers:
     - host: 10.0.1.1

    monitoring_servers:
     - host: 10.0.1.1

    grafana_servers:
     - host: 10.0.1.1
    ```

    - `user: "tidb"`: Use the `tidb` system user (automatically created during deployment) to perform the internal management of the cluster. By default, use port 22 to log in to the target machine via SSH.
    - `replication.enable-placement-rules`: This PD parameter is set to ensure that TiFlash runs normally.
    - `host`: The IP of the target machine.

6. Execute the cluster deployment command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy <cluster-name> <tidb-version> ./topo.yaml --user root -p
    ```

    - `<cluster-name>`: Set the cluster name
    - `<tidb-version>`: Set the TiDB cluster version. You can see all the supported TiDB versions by running the `tiup list tidb` command

    Enter "y" and the `root` user's password to complete the deployment:

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

7. Start the cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

8. Access the cluster:

    - Access TiDB. The password is empty:

        {{< copyable "shell-regular" >}}

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    - Access the Grafana monitoring dashboard at <http://{grafana-ip}:3000>. The default username and password are both `admin`.

    - Access the TiDB Dashboard at <http://{pd-ip}:2379/dashboard>. The default username is `root`, and the password is empty.

    - To view the currently deployed cluster list:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster list
        ```

    - To view the cluster topology and status:

         {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster display <cluster-name>
        ```

## Try out TiDB with one click using TiDB-Wasm

- Scenario: Experiment with TiDB SQL and test the TiDB compatibility with MySQL queries.
- Time required: Instant

TiDB-Wasm enables you to run a TiDB server instance in a browser so that you can experiment with SQL and test TiDB compatibility with MySQL queries.

Click to try TiDB-Wasm playground: <https://tour.tidb.io>. It takes about 10 seconds to launch the TiDB server instance in your browser. The playground walks you through the basic TiDB SQL statements such as DDL, DML and CRUD operations.

## What's next

- If you have just deployed a TiDB cluster for the local test environment:

    - Learn [Basic SQL operations in TiDB](/basic-sql-operations.md)
    - Learn [TiDB key features and scenarios](/overview.md)
    - Learn [TiDB's compatibility with MySQL](/mysql-compatibility.md)

- If you are ready to deploy a TiDB cluster for the production environment:

    - [Deploy TiDB online using TiUP](/production-deployment-using-tiup.md)
    - [Deploy TiDB offline using TiUP](/production-offline-deployment-using-tiup.md)
    - [Deploy TiDB on Cloud using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.1)

> **Note:**
>
> By default, TiDB, TiUP and TiDB Dashboard share usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
