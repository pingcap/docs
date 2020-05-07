---
title: Deploy and Maintain the TiDB Online Cluster Using TiUP
summary: Learns how to deploy and maintain the TiDB cluster using TiUP.
category: tools
---

# Deploy and Maintain the TiDB Online Cluster Using TiUP

This document focuses on how to use the TiUP cluster component. If you want to see the complete steps of online deployment, refer to [Deploy a TiDB Cluster Using TiUP](/how-to/deploy/orchestrated/tiup.md).

Similar to the TiUP playground component used for local deployment, the TiUP cluster component quickly deploys TiDB for production environment. Compared with playground, the cluster component provides more powerful cluster management features, including upgrading, scaling, and even operation and auditing.

To see the help file of the cluster component, run the following command:

```bash
tiup cluster
```

```
The component `cluster` is not installed; downloading from repository.
download https://tiup-mirrors.pingcap.com/cluster-v0.4.9-darwin-amd64.tar.gz 15.32 MiB / 15.34 MiB 99.90% 10.04 MiB p/s                                                   
Starting component `cluster`: /Users/joshua/.tiup/components/cluster/v0.4.9/cluster 
Deploy a TiDB cluster for production

Usage:
  tiup cluster [flags]
  tiup [command]

Available Commands:
  deploy      Deploy the cluster
  start       Start the deployed cluster
  stop        Stop the cluster
  restart     Restart the cluster
  scale-in    Scale in the cluster
  scale-out   Scale out the cluster
  destroy     Destroy the cluster
  upgrade     Upgrade the cluster
  exec        Execute commands on one or multiple machines in the cluster
  display     Get the cluster information
  list        Get the cluster list
  audit       View the cluster operation log
  import      Import a cluster deployed using TiDB-Ansible
  edit-config Edit the configuration of the TiDB cluster
  reload      Reload cluster configurations when necessary
  patch       Replace deployed components in the cluster with temporary component packages
  help        Print help information

Flags:
  -h, --help              Help information
      --ssh-timeout int   SSH connection timeout
  -y, --yes               Skip all confirmation steps
```

## Deploy the cluster

To deploy the cluster, run the `tiup cluster deploy` command. The common usage of the command is as follows:

```bash
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

You need to provide the cluster name, the TiDB version, and a topology file of the cluster to run this command.

To write a topology file, refer to [the example](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml). The following file is an example of the simplest topology:

```yaml
---

pd_servers:
  - host: 172.16.5.134
    name: pd-134
  - host: 172.16.5.139
    name: pd-139
  - host: 172.16.5.140
    name: pd-140

tidb_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

tikv_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

Save the file as `/tmp/topology.yaml`. If you want to use TiDB v3.0.12 and your cluster name is `prod-cluster`, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy prod-cluster v3.0.12 /tmp/topology.yaml
```

During the execution, TiUP confirms your topology again and requires the root password of the target machine:

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
Type        Host          Ports        Directories
----        ----          -----        -----------
pd          172.16.5.134  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380    deploy/pd-2379,data/pd-2379
tikv        172.16.5.134  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.139  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.140  20160/20180  deploy/tikv-20160,data/tikv-20160
tidb        172.16.5.134  4000/10080   deploy/tidb-4000
tidb        172.16.5.139  4000/10080   deploy/tidb-4000
tidb        172.16.5.140  4000/10080   deploy/tidb-4000
prometheus  172.16.5.134  9090         deploy/prometheus-9090,data/prometheus-9090
grafana     172.16.5.134  3000         deploy/grafana-3000
Attention:
    1. If the topology is not what you expected, check your yaml file.
    1. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:
```

After you enter the password, tiup-cluster downloads the required components and deploy them on the corresponding machines. When you see the following sentence, the deployment is successful:

```bash
Deployed cluster `prod-cluster` successfully
```

## View the cluster list

After the cluster is successfully deployed, view the cluster list by running the `tiup cluster list` command:

{{< copyable "shell-root" >}}

```bash
tiup cluster list
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster list
Name          User  Version    Path                                               PrivateKey
----          ----  -------    ----                                               ----------
prod-cluster  tidb  v3.0.12    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa
```

## Start the cluster

After the cluster is successfully deployed, start the cluster by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster start prod-cluster
```

If you forget the name of your cluster, view the cluster list by running `tiup cluster list`.

## Check the cluster status

TiUP provides the `tiup cluster display` command to view the status of each component in the cluster. With this command, you don't have to log in to each machine separately to see the component status. The usage of the command is as follows:

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Healthy|L  data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Healthy    data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Healthy    data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
```

For ordinary components, the `Status` column shows `Up` or `Down`, which indicates whether the service is running normally.

For the PD component, the `Status` column shows `Healthy` or `Down`, and sometimes `|L` if the PD node is a Leader.

## Scale in a node

> **Note:**
>
> This section describes only the example syntax of the scale-in command. For detailed steps of online scaling, refer to [Scale the TiDB Cluster Using TiUP](/how-to/scale/with-tiup.md).

Scaling in a node means taking the node offline. This operation removes the node from the cluster and deletes the related data files.

Because the offline process of the TiKV and TiDB Binlog components is asynchronous (which requires removing the node through API), and the process takes a long time to see if the node is successfully taken offline, special treatment is given to the TiKV and TiDB Binlog components.

- For TiKV and Binlog:

    - TiUP cluster takes the node offline through API and directly exits without waiting for the process to be completed.
    - Afterwards, when a command related to the cluster operation is executed, TiUP cluster examines whether there is a TiKV/Binlog node that has been taken offline. If not, TiUP cluster continues with the specified operation; If there is, TiUP cluster takes the following steps:

        1. Stop the service of the node that has been taken offline.
        2. Clean up the data file related to the node.
        3. Update the cluster topology and remove the node.

- For other components:

    - When taking the PD component down, TiUP cluster quickly deletes the specified node from the cluster through API, stops the specified PD service and deletes the related data file.
    - When taking other components down, TiUP cluster directly stops the service and deletes the related data file.

The basic usage of the scale-in command:

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

To use this command, you need to specify at least two parameters: the cluster name and the node ID. The node ID can be obtained by using the `tiup cluster display` command as in the previous section.

For example, to scale in the TiKV node on `172.16.5.140`, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

By running `tiup cluster display`, you can see that the TiKV node is marked `Offline`:

{{< copyable "shell-root" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v0.4.5/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v3.0.12
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Healthy|L  data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Healthy    data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Healthy    data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Offline    data/tikv-20160       deploy/tikv-20160
```

After PD schedules the data on the node to other TiKV nodes, this node will be deleted automatically.

## Scale out a node

> **Note:**
>
> This section describes only the example syntax of the scale-out command. For detailed steps of online scaling, refer to [Scale the TiDB Cluster Using TiUP](/how-to/scale/with-tiup.md).

The scale-out operation has an inner logic similar to that of deployment. The TiUP cluster component firstly ensures the SSH connection of the node, creates the required directory on the target node, then executes the deployment, and starts the service.

When you scale out PD, the node is added to the cluster by `join`, and the configurations of services associated with PD are updated. When you scale out other services, the service is started directly and added to the cluster.

All services conduct correctness validation when they are scaled out. The validation results shows whether the scaling-out is successful.

To scale out a TiKV node and a PD node in the `tidb-test` cluster, take the following steps:

1. Create a `scale.yaml` file, and add IP of the new TiKV and PD nodes:

    > **Note:**
    >
    > Create a topology file, which includes only the description of the new nodes, not the existing nodes.

    ```yaml
    ---
    
    pd_servers:
      - ip: 172.16.5.140
    
    tikv_servers:
      - ip: 172.16.5.140
    ```

2. Perform the scale-out operation. TiUP cluster adds the corresponding nodes to the cluster according to the port, directory, and other information described in `scale.yaml`.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    After the command is executed, you can check the status of the scaled-out cluster by running `tiup cluster display tidb-test`.

## Rolling upgrade

> **Note:**
>
> This section describes only the example syntax of the upgrade command. For detailed steps of online upgrade, refer to [Upgrade TiDB Using TiUP](/how-to/upgrade/using-tiup.md).

The rolling upgrade feature leverages the distributed capabilities of TiDB. The upgrade process is made as transparent as possible to the application, and does not affect the business.

Before the upgrade, TiUP cluster checks whether the configuration file of each component is rational. If so, the components are upgraded node by node; if not, TiUP reports an error and exits. The operations vary with different nodes.

### Operations for different nodes

- Upgrade the PD node

    - First, upgrade non-Leader nodes.
    - After all the non-Leader nodes are upgraded, upgrade the Leader node.
        - The upgrade tool sends a command to PD that migrates Leader to an already upgraded node.
        - After the Leader role is switched to another node, upgrade the previous Leader node.
    - During the upgrade, if any unhealthy node is detected, the tool stops this upgrade operation and exits. You need to manually analyze the cause, fix the issue and run the upgrade again.

- Upgrade the TiKV node

    - First, add a scheduling operation in PD that migrates the Region Leader of this TiKV node. This ensures that the upgrade process does not affect the business.
    - After the Leader is migrated, upgrade this TiKV node.
    - After the upgraded TiKV is started normally, remove the scheduling of the Leader.

- Upgrade other services

    - Stop the service normally and update the node.

### Upgrade command

The parameters for the upgrade command is as follows:

```bash
Usage:
  tiup cluster upgrade <cluster-name> <version> [flags]

Flags:
      --force                  Force upgrade without transferring Leader (dangerous)
  -h, --help                   Help information
      --transfer-timeout int   Transfer Leader timeout

Global Flags:
      --ssh-timeout int   SSH connection timeout
  -y, --yes               Skip all confirmation steps
```

For example, the following command upgrades the cluster to v4.0.0-rc:

{{< copyable "shell-regular" >}}

```bash
tiup cluster upgrade tidb-test v4.0.0-rc
```

## Update configuration

If you want to dynamically update the component configurations, the TiUP cluster component saves a current configuration for each cluster. To edit this configuration, execute the `tiup cluster edit-config <cluster-name>` command. For example:

{{< copyable "shell-regular" >}}

```bash
tiup cluster edit-config prod-cluster
```

TiUP cluster opens the configuration file in the vi editor. After editing the file, save the changes. To apply the new configuration to the cluster, execute the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster reload prod-cluster
```

The command sends the configuration to the target machine and restarts the cluster to make the configuration take effect.

## Update component

For normal upgrade, you can use the `upgrade` command. But in some scenarios, such as debugging, you might need to replace the currently running cluster with a temporary package. To achieve this, use the `patch` command:

{{< copyable "shell-root" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  tiup cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   Help information
  -N, --node strings           Specifies the node to be replaced
      --overwrite              Use the currently specified temporary package in the future scale-out operation
  -R, --role strings           Specifies the service type to be replaced
      --transfer-timeout int   Transfer Leader timeout

Global Flags:
      --ssh-timeout int   SSH connection timeout
  -y, --yes               Skip all confirmation steps
```

If a TiDB hotfix package is in `/tmp/tidb-hotfix.tar.gz` and you want to replace all the TiDB packages in the cluster, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

You can also replace only one TiDB package in the cluster:

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## Import TiDB Ansible cluster

Before TiUP is released, TiDB Ansible is often used to deploy TiDB clusters. To enable TiUP to take over the cluster deployed by TiDB Ansible, use the `import` command.

The usage of the `import` command is as follows:

{{< copyable "shell-root" >}}

```bash
tiup cluster import --help
```

```
Import an exist TiDB cluster from TiDB-Ansible

Usage:
  tiup cluster import [flags]

Flags:
  -d, --dir string         Directory of TiDB-Ansible. Defaults to the current directory.
  -h, --help               Help Information
      --inventory string   Name of the inventory file ("inventory.ini" by default)
      --no-backup          Do not back up the Ansible directory. Used in the Ansible directory that has multiple inventory files.
  -r, --rename NAME        Rename the imported cluster

Global Flags:
      --ssh-timeout int   SSH connection timeout
  -y, --yes               Skip all confirmation steps
```

You can use either of the following two commands to import a TiDB Ansible cluster:

{{< copyable "shell-regular" >}}

```bash
cd tidb-ansible
tiup cluster import
```

{{< copyable "shell-regular" >}}

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## View the operation log

To view the operation log, use the `audit` command. The usage of the `audit` command is as follows:

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

If the `[audit-id]` parameter is not specified, the command shows a list of commands that have been executed. For example:

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit
```

```
Starting component `cluster`: /Users/joshua/.tiup/components/cluster/v0.6.0/cluster audit
ID      Time                       Command
--      ----                       -------
4BLhr0  2020-04-29T13:25:09+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKWjF  2020-04-28T23:36:57+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKVwH  2020-04-28T23:02:08+08:00  /Users/joshua/.tiup/components/cluster/v0.6.0/cluster deploy test v4.0.0-rc /tmp/topology.yaml
4BKKH1  2020-04-28T16:39:04+08:00  /Users/joshua/.tiup/components/cluster/v0.4.9/cluster destroy test
4BKKDx  2020-04-28T16:36:57+08:00  /Users/joshua/.tiup/components/cluster/v0.4.9/cluster deploy test v4.0.0-rc /tmp/topology.yaml
```

The first column is `audit-id`. To view the execution log of a certain command, pass the `audit-id` of the command as a parameter as follows:

{{< copyable "shell-regular" >}}

```bash
tiup cluster audit 4BLhr0
```

## Run commands on a machine in cluster

To run a command on the machine in the cluster, use the `exec` command. The usage of the `exec` command is as follows:

```bash
Usage:
  tiup cluster exec <cluster-name> [flags]

Flags:
      --command string   The command to be executed ("ls" by default)
  -h, --help             Help information
  -N, --node strings     Specify the ID of the node that you execute command on. Use the `display` command to get the node ID.
  -R, --role strings     Specify the role to be executed
      --sudo             Whether to use root privilege ("false" by default)
```

For example, to execute `ls /tmp` on all TiDB nodes, run the following command:

{{< copyable "shell-regular" >}}

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## Cluster controllers

Before TiUP is released, you can control the cluster using `tidb-ctl`, `tikv-ctl`, `pd-ctl`, and other tools. To make the tools easier to download and use, TiUP integrate them into an all-in-one component, `ctl`.

```bash
Usage:
  tiup ctl {tidb/pd/tikv/binlog/etcd} [flags]

Flags:
  -h, --help   help for tiup
```

This command has a corresponding relationship with those of the previous tools:

```bash
tidb-ctl [args] = tiup ctl tidb [args]
pd-ctl [args] = tiup ctl pd [args]
tikv-ctl [args] = tiup ctl tikv [args]
binlogctl [args] = tiup ctl bindlog [args]
etcdctl [args] = tiup ctl etcd [args]
```

For example, if you previously view the store by running `pd-ctl -u http://127.0.0.1:2379 store`, now you can run the following command in TiUP:

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 store
```
