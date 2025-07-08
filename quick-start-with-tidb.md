---
title: Quick Start with TiDB Self-Managed
summary: Learn how to quickly get started with TiDB Self-Managed using TiUP playground and see if TiDB is the right choice for you.
---

# Quick Start with TiDB Self-Managed

This guide provides the quickest way to get started with TiDB Self-Managed. For non-production environments, you can deploy your TiDB database using either of the following methods:

- [Deploy a local test cluster](#deploy-a-local-test-cluster) (for macOS and Linux)
- [Simulate production deployment on a single machine](#simulate-production-deployment-on-a-single-machine) (for Linux only)

In addition, you can try out TiDB features on [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_quick_start).

> **Note:**
>
> The deployment method provided in this guide is **ONLY FOR** quick start, **NOT FOR** production or comprehensive functionality and stability testing.
>
> - To deploy a self-hosted production cluster, see the [production installation guide](/production-deployment-using-tiup.md).
> - To deploy TiDB on Kubernetes, see [Get Started with TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started).
> - To manage TiDB in the cloud, see [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart).

## Deploy a local test cluster

This section describes how to quickly deploy a local TiDB cluster for testing on a single macOS or Linux server. By deploying such a cluster, you can learn the basic architecture of the TiDB database and the operation of its components, such as TiDB, TiKV, PD, and the monitoring components.

<SimpleTab>
<div label="macOS">

As a distributed system, a basic TiDB test cluster usually consists of 2 TiDB instances, 3 TiKV instances, 3 PD instances, and optional TiFlash instances. With TiUP Playground, you can quickly set up a test cluster by following these steps:

1. Download and install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    If the following message is displayed, you have successfully installed TiUP:

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    Note the Shell profile path in the output above. You need to use the path in the next step.

    > **Note:**
    >
    > Starting from v5.2.0, TiDB supports running `tiup playground` on the machine that uses the Apple silicon chip.

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path. In this case, `${your_shell_profile}` is `/Users/user/.zshrc` from the output of Step 1.

    ```shell
    source ${your_shell_profile}
    ```

3. Start the cluster in the current session:

    > **Note:**
    >
    > - For the playground operated in the following way, after the deployment and testing are finished, TiUP will automatically clean up the cluster data. You will get a new cluster after re-running the command.
    > - If you want to persist data on storage, then add the `--tag` flag when you start the cluster. For details, see [Specify a tag when starting the TiDB cluster to store the data](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data).
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    - To start a TiDB cluster of the latest version with 1 TiDB instance, 1 TiKV instance, 1 PD instance, and 1 TiFlash instance, run the following command:

        ```shell
        tiup playground
        ```

        If this is the first time you run the command, TiUP will download the latest version of TiDB and start the cluster.

        The output displays a list of endpoints of the cluster:

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    - To specify the TiDB version and the number of instances of each component, run a command like this:

        ```shell
        tiup playground v8.5.1 --db 2 --pd 3 --kv 3
        ```

        It is recommended to run this command on a machine with at least 10 GiB of memory and 4 CPU cores. Insufficient resources might cause the system to crash.  

        To view all available versions, run `tiup list tidb`.

4. Start a new session to access the TiDB cluster endpoints:

    - Connect to the TiDB database:

        - Use the TiUP client to connect to TiDB.

            ```shell
            tiup client
            ```

        - Alternatively, you can use the MySQL client to connect to TiDB.

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    - Prometheus: <http://127.0.0.1:9090>.

    - [TiDB Dashboard](/dashboard/dashboard-intro.md): <http://127.0.0.1:2379/dashboard>. The default username is `root`, and the password is empty.

    - Grafana: <http://127.0.0.1:3000>. Both the default username and password are `admin`.

5. (Optional) [Load data to TiFlash](/tiflash/tiflash-overview.md#use-tiflash) for analysis.

6. Clean up the cluster after testing:

    1. Stop the above TiDB service by pressing <kbd>Control</kbd>+<kbd>C</kbd>.

    2. Run the following command after the service is stopped:

        ```shell
        tiup clean --all
        ```

> **Note:**
>
> TiUP Playground listens on `127.0.0.1` by default, and the service is only locally accessible. If you want the service to be externally accessible, specify the listening address using the `--host` parameter to bind the network interface card (NIC) to an externally accessible IP address.

</div>
<div label="Linux">

As a distributed system, a basic TiDB test cluster usually consists of 2 TiDB instances, 3 TiKV instances, 3 PD instances, and optional TiFlash instances. With TiUP Playground, you can quickly set up a test cluster by following these steps:

1. Download and install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    If the following message is displayed, you have successfully installed TiUP:

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: bash
    Shell profile:  /home/user/.bashrc
    /home/user/.bashrc has been modified to add tiup to PATH
    open a new terminal or source /home/user/.bashrc to use it
    Installed path: /home/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    Note the Shell profile path in the output above. You need to use the path in the next step.

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path.

    ```shell
    source ${your_shell_profile}
    ```

3. Start the cluster in the current session:

    > **Note:**
    >
    > - For the playground operated in the following way, after the deployment and testing are finished, TiUP will automatically clean up the cluster data. You will get a new cluster after re-running the command.
    > - If you want to persist data on storage, then add the `--tag` flag when you start the cluster. For details, see [Specify a tag when starting the TiDB cluster to store the data](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data).
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    - To start a TiDB cluster of the latest version with 1 TiDB instance, 1 TiKV instance, 1 PD instance, and 1 TiFlash instance, run the following command:

        ```shell
        tiup playground
        ```

        If this is the first time you run the command, TiUP will download the latest version of TiDB and start the cluster.

        The output displays a list of endpoints of the cluster:

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    - To specify the TiDB version and the number of instances of each component, run a command like this:

        ```shell
        tiup playground v8.5.1 --db 2 --pd 3 --kv 3
        ```

        To view all available versions, run `tiup list tidb`.

4. Start a new session to access the TiDB cluster endpoints:

    - Connect to the TiDB database:

        - Use the TiUP client to connect to TiDB.

            ```shell
            tiup client
            ```

        - Alternatively, you can use the MySQL client to connect to TiDB.

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    - Prometheus: <http://127.0.0.1:9090>.

    - [TiDB Dashboard](/dashboard/dashboard-intro.md): <http://127.0.0.1:2379/dashboard>. The default username is `root`, and the password is empty.

    - Grafana: <http://127.0.0.1:3000>. Both the default username and password are `admin`.

5. (Optional) [Load data to TiFlash](/tiflash/tiflash-overview.md#use-tiflash) for analysis.

6. Clean up the cluster after testing:

    1. Stop the process by pressing <kbd>Control</kbd>+<kbd>C</kbd>.

    2. Run the following command after the service is stopped:

        ```shell
        tiup clean --all
        ```

> **Note:**
>
> TiUP Playground listens on `127.0.0.1` by default, and the service is only locally accessible. If you want the service to be externally accessible, specify the listening address using the `--host` parameter to bind the network interface card (NIC) to an externally accessible IP address.

</div>
</SimpleTab>

## Simulate production deployment on a single machine

This section describes how to set up the smallest TiDB cluster with a full topology, and simulate production deployment steps on a single Linux server.

The following describes how to deploy a TiDB cluster using a YAML file of the smallest topology in TiUP.

### Prepare

Before deploying the TiDB cluster, ensure that the target machine meets the following requirements:

- CentOS 7.3 or a later version is installed.
- The Linux OS has access to the internet, which is required to download TiDB and related software installation packages.

The smallest TiDB cluster topology consists of the following instances:

| Instance | Count | IP | Configuration |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 | Use incremental port numbers to avoid conflicts |
| TiDB | 1 | 10.0.1.1 | Use default port and other configurations |
| PD | 1 | 10.0.1.1 | Use default port and other configurations |
| TiFlash | 1 | 10.0.1.1 | Use default port and other configurations |
| Monitor | 1 | 10.0.1.1 | Use default port and other configurations |

> **Note:**
>
> The IP addresses of the instances are given as examples only. In your actual deployment, replace the IP addresses with your actual IP addresses.

Other requirements for the target machine include:

- The `root` user and its password are required.
- [Stop the firewall service of the target machine](/check-before-deployment.md#check-the-firewall-service-of-target-machines), or open the ports needed by the TiDB cluster nodes.
- Currently, the TiUP cluster supports deploying TiDB on the x86_64 (AMD64) and ARM architectures:

    - It is recommended to use CentOS 7.3 or later versions on AMD64 architecture.
    - It is recommended to use CentOS 7.6 (1810) on ARM architecture.

### Deploy

> **Note:**
>
> You can log in to the target machine as a regular user or the `root` user. The following steps use the `root` user as an example.

1. Download and install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable.

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path.

    ```shell
    source ${your_shell_profile}
    ```

3. Install the cluster component of TiUP:

    ```shell
    tiup cluster
    ```

4. If the TiUP cluster is already installed on the machine, update the software version:

    ```shell
    tiup update --self && tiup update cluster
    ```

5. Increase the connection limit of the `sshd` service using the root user privilege. This is because TiUP needs to simulate deployment on multiple machines.

    1. Modify `/etc/ssh/sshd_config`, and set `MaxSessions` to `20`.
    2. Restart the `sshd` service:

        ```shell
        service sshd restart
        ```

6. Create and start the cluster:

    Create and edit the [topology configuration file](/tiup/tiup-cluster-topology-reference.md) according to the following template, and name it as `topo.yaml`:

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
       instance.tidb_slow_log_threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
       replication.location-labels: ["host"]
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
       config:
         server.labels: { host: "logic-host-1" }

     - host: 10.0.1.1
       port: 20161
       status_port: 20181
       config:
         server.labels: { host: "logic-host-2" }

     - host: 10.0.1.1
       port: 20162
       status_port: 20182
       config:
         server.labels: { host: "logic-host-3" }

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

7. Execute the cluster deployment command:

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    - `<cluster-name>`: sets the cluster name.
    - `<version>`: sets the TiDB cluster version, such as `v8.5.1`. You can see all the supported TiDB versions by running the `tiup list tidb` command.
    - `--user`: specifies the user to initialize the environment.
    - `-p`: specifies the password used to connect to the target machine.

        > **Note:**
        >
        > If you use secret keys, you can specify the path of the keys through `-i`. Do not use `-i` and `-p` at the same time.

    Enter "y" and the `root` user's password to complete the deployment:

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8. Start the cluster:

    ```shell
    tiup cluster start <cluster-name>
    ```

9. Access the cluster endpoints:

    - Install the MySQL client. If it is already installed, skip this step.

        ```shell
        yum -y install mysql
        ```

    - Connect to the TiDB database using the MySQL client. The password is empty:

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    - Grafana: <http://{grafana-ip}:3000>. The default username and password are both `admin`.

    - [TiDB Dashboard](/dashboard/dashboard-intro.md): <http://{pd-ip}:2379/dashboard>. The default username is `root`, and the password is empty.

10. (Optional) View the cluster list and topology.

    - To view the cluster list:

        ```shell
        tiup cluster list
        ```

    - To view the cluster topology and status:

        ```shell
        tiup cluster display <cluster-name>
        ```

    To learn more about the `tiup cluster` commands, see [TiUP Cluster Commands](/tiup/tiup-component-cluster.md).

11. Clean up the cluster after testing:

    1. Stop the above TiDB service by pressing <kbd>Control</kbd>+<kbd>C</kbd>.

    2. Run the following command after the service is stopped:

        ```shell
        tiup clean --all
        ```

## What's next

If you have just deployed a TiDB cluster for the local test environment, here are the next steps:

- Learn about basic SQL operations in TiDB by referring to [Basic SQL operations in TiDB](/basic-sql-operations.md).
- You can also migrate data to TiDB by referring to [Migrate data to TiDB](/migration-overview.md).
- Learn more about using TiUP to manage TiDB clusters by referring to [TiUP Overview](/tiup/tiup-overview.md).

If you are ready to deploy a TiDB cluster for the production environment, here are the next steps:

- [Deploy TiDB using TiUP](/production-deployment-using-tiup.md)
- Alternatively, you can deploy TiDB on Cloud using TiDB Operator by referring to the [TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable) documentation.

If you are an application developer and want to quickly build an application using TiDB, here are the next steps:

- [Developer Guide Overview](/develop/dev-guide-overview.md)
- [Build a {{{ .starter }}} Cluster](/develop/dev-guide-build-cluster-in-cloud.md)
- [Example Applications](/develop/dev-guide-sample-application-java-jdbc.md)

If you are looking for an analytics solution with TiFlash, here are the next steps:

- [TiFlash Overview](/tiflash/tiflash-overview.md)
- [Use TiFlash](/tiflash/tiflash-overview.md#use-tiflash)
