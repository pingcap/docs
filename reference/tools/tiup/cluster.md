---
title: Deploy and Maintain the TiDB Online Cluster Using TiUP
summary:
category: tools
---

# Deploy and Maintain the TiDB Online Cluster Using TiUP

This document focuses on how to use the cluster component of TiUP. If you want the complete steps of online deployment, refer to [Deploy a TiDB Cluster Using TiUP](/how-to/deploy/orchestrated/tiup.md).

Similar to the TiUP playground component used for local deployment, the TiUP cluster component quickly deploys TiDB for production environment. Compared with playground, the cluster component provides more powerful cluster management capabilities, including upgrading, scaling, and even operation and auditing.

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
  patch       Replace deployed components on the cluster with temporary component packages
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

Save the file as `/tmp/topology.yaml`. If you want to use TiDB v4.0.0-rc, and if your cluster name is `prod-cluster`, run the following command:

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy prod-cluster v3.0.12 /tmp/topology.yaml
```

During the command execution, the system confirms your topology again and requires the root password of the target machine:

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

After you type in the password, tiup-cluster downloads the required components and deploy them on the corresponding machines. When you see the following sentence, the deployment is successful:

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

TiUP provides the `tiup cluster display` command to view the status of each component in the cluster so that you don't have to log in to each machine separately. Use the command as follows:

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

For ordinary components, the `Status` column shows `Up` or `Down`, which indicates whether the service is running normally. For the PD component, the `Status` column shows `Healthy` or `Down`, and sometimes `|L` if the PD is a Leader.

## Scale in a node

> **Note:**
>
> This section describes only the example syntax of the scale-in command. For detailed steps of online scaling, refer to [Scale the TiDB Cluster Using TiUP](/how-to/scale/with-tiup.md).

Scaling in a node means taking the node offline. This operation removes the node from the cluster and deletes the related data files.

Because the offline process of the TiKV and TiDB Binlog components is asynchronous (which requires the removing operation through API), and the process takes a long time to see if the node is successfully taken offline, special treatment is given to the TiKV and TiDB Binlog components.

- For TiKV and Binlog:

    - TiUP cluster takes the node offline through API and directly exits without waiting for the process to complete.
    - Afterwards, when a command related to the cluster operation is executed, TiUP cluster examines whether there is a TiKV/Binlog node that has been taken offline. If not, TiUP cluster continues with the specified operation; If there is, TiUP cluster takes the following steps:

        1. Stop the service of the node that has been taken offline.
        2. Clean up the data file related to the node.
        3. Update the cluster topology and remove the node.

- For other components:

    - When taking the PD component down, TiUP cluster quickly deletes the specified node from the cluster through API, stops the specified PD service and deletes the related date file.
    - When taking other components down, TiUP cluster directly stops the service and deletes the related data file.

The basic usage of the scale-in command:

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

You need to specify at least two parameters: the cluster name and the node ID. The node ID can be obtained by using the `tiup cluster display` command as in the previous section.

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

The scale-out operation has an inner logic similar to that of deployment. The TiUP cluster component firstly ensures the SSH connection of the node, creates the required directory on the target node, then executes the deployment and starts the service.

When you scale out PD, the node is added to the cluster 