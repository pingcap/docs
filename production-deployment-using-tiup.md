---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
category: how-to
aliases: ['/docs/dev/how-to/deploy/orchestrated/tiup/']
---

# Deploy a TiDB Cluster Using TiUP

[TiUP](https://github.com/pingcap/tiup) is a cluster operation and maintenance tool introduced in TiDB 4.0. TiUP provides [TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster), a cluster management component written in Golang. By using TiUP cluster, you can easily perform daily database operations, including deploying, starting, stopping, destroying, scaling, and upgrading a TiDB cluster, and manage TiDB cluster parameters.

TiUP supports deploying TiDB, TiFlash, TiDB Binlog, and TiCDC. This document introduces how to deploy clusters of different topologies.

## Step 1: Check prerequisites

- [Hardware and software requirements](/hardware-and-software-requirements.md)
- [Environment and system configuration check](/check-before-deployment.md)

### Step 2: Install TiUP on the Control Machine

Log in to the Control Machine using a regular user account (take the `tidb` user as an example). All the following TiUP installation and cluster management operations can be performed by the `tidb` user.

1. Install TiUP by executing the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Set the TiUP environment variables:

    Redeclare the global environment variables:

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

    Confirm whether TiUP is installed:

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

3. Install the TiUP cluster component:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

4. If TiUP is already installed, update the TiUP cluster component to the latest version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

    Expected output will include `“Update successfully!”`.

5. Verify the current version of your TiUP cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --binary cluster
    ```

## Step 3: Edit the initialization configuration file

You need to manually create and edit the cluster initialization configuration file according to the cluster topology.

The following examples cover six common scenarios. You need to create a configuration file `topology.yaml` according to the topology description and templates in the corresponding links. For other scenarios, edit the configuration according to multiple templates.

You need to create a YAML configuration file on the Control Machine, such as `topology.yaml`.

The following sections provide a cluster configuration template for each of the following common scenarios:

- [The minial deployment topology](/minimal-deployment-topology.md)

    This is the basic cluster topology, including tidb-server, tikv-server, and pd-server. It is suitable for OLTP applications.

- [The TiFlash deployment topology](/tiflash-deployment-topology.md)

    This is to deploy TiFlash along with the minimal cluster topology. TiFlash is a columnar storage engine, and gradually becomes the standard configuration for the cluster topology. It is suitable for real-time HTAP applications.

- [The TiCDC deployment topology](/ticdc-deployment-topology.md)

    This is to deploy TiCDC along with the minimal cluster topology. TiCDC is a tool for replicating the incremental data of TiDB, introduced in TiDB 4.0. It supports multiple downstream platforms, such as TiDB, MySQL, and MQ. Compared with TiDB Binlog, TiCDC has lower latency and native high availability. After the deployment, start TiCDC and [create the replication task using `cdc cli`](/ticdc/manage-ticdc.md).

- [The TiDB Binlog deployment topology](/tidb-binlog-deployment-topology.md)

    This is to deploy TiDB Binlog along with the minimal cluster topology. TiDB Binlog is the widely used component for replicating incremental data. It provides near real-time backup and replication.

- [The hybrid deployment topology](/hybrid-deployment-topology.md)

    This is to deploy multiple mixed instances on a single machine, including deploying multiple instances on a single machine. You need to add extra configurations for the directory, port, resource ratio, and label.

- [The geo-distributed deployment topology](/geo-distributed-deployment-topology.md)

    This topology takes the typical architecture of 3 DC in 2 cities as an example. It introduces the geo-distributed deployment architecture and the key configuration that requires attention.

### Step 4: Execute the deployment command

> **Note:**
>
> You can use secret keys or interactive passwords for security authentication when you deploy TiDB using TiUP:
>
> - If you use secret keys, you can specify the path of the keys through `-i` or `--identity_file`;
> - If you use passwords, you do not need to add other parameters, tap `Enter` and you can enter the password interaction window.

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v4.0.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

In the above command:

- The name of the TiDB cluster deployed through TiUP cluster is `tidb-test`.
- The deployment version is `v4.0.0`. You can see other supported versions by running `tiup list tidb --refresh`.
- The initialization configuration file is `topology.yaml`.
- `--user root`: Log in to the target machine through the `root` key to complete the cluster deployment, or you can use other users with `ssh` and `sudo` privileges to complete the deployment.
- `[-i]` and `[-p]`: optional. If you have configured login to the target machine without password, these parameters are not required. If not, choose one of the two parameters. `[-i]` is the private key of the `root` user (or other users specified by `--user`) that has access to the deployment machine. `[-p]` is used to input the user password interactively.

At the end of the output log, you will see ```Deployed cluster `tidb-test` successfully```. This indicates that the deployment is successful.

### Step 5: Check the clusters managed by TiUP

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP supports managing multiple TiDB clusters. The command above outputs information of all the clusters currently managed by TiUP, including the name, deployment user, version, and secret key information:

```log
Starting /home/tidb/.tiup/components/cluster/v1.0.0/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v4.0.0      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

### Step 6: Check the status of the deployed TiDB cluster

For example, execute the following command to check the status of the `tidb-test` cluster:

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

Expected output will include the instance ID, role, host, listening port, and status (because the cluster is not started yet, so the status is `Down`/`inactive`), and directory information.

## Step 7: Start the TiDB cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

If the output log includes ```Started cluster `tidb-test` successfully```, the start is successful.

### Step 8: Verify the running status of the TiDB cluster

- Check the TiDB cluster status using TiUP

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display tidb-test
    ```

    If the `Status` is `Up` in the output, the cluster status is normal.

- Log in to the database by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    mysql -u root -h 10.0.1.4 -P 4000
    ```

For more ways to verify the cluster status, see [Verify the Cluster Running Status](/post-installation-check.md).
