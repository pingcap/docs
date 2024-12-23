---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy a local TiDB cluster using the playground component of TiUP.
aliases: ['/docs/dev/tiup/tiup-playground/','/docs/dev/reference/tools/tiup/playground/']
---

# Quickly Deploy a Local TiDB Cluster

The TiDB cluster is a distributed system that consists of multiple components. A typical TiDB cluster consists of at least three PD nodes, three TiKV nodes, and two TiDB nodes. If you want to have a quick experience on TiDB, you might find it time-consuming and complicated to manually deploy so many components. This document introduces the playground component of TiUP and how to use it to quickly build a local TiDB test environment.

## TiUP playground overview

The basic usage of the playground component is shown as follows:

```bash
tiup playground ${version} [flags]
```

If you directly execute the `tiup playground` command, TiUP uses the locally installed TiDB, TiKV, and PD components or installs the stable version of these components to start a TiDB cluster that consists of one TiKV instance, one TiDB instance, one PD instance, and one TiFlash instance.

This command actually performs the following operations:

- Because this command does not specify the version of the playground component, TiUP first checks the latest version of the installed playground component. Assume that the latest version is v1.12.3, then this command works the same as `tiup playground:v1.12.3`.
- If you have not used TiUP playground to install the TiDB, TiKV, and PD components, the playground component installs the latest stable version of these components, and then start these instances.
- Because this command does not specify the version of the TiDB, PD, and TiKV component, TiUP playground uses the latest version of each component by default. Assume that the latest version is v8.5.0, then this command works the same as `tiup playground:v1.12.3 v8.5.0`.
- Because this command does not specify the number of each component, TiUP playground, by default, starts a smallest cluster that consists of one TiDB instance, one TiKV instance, one PD instance, and one TiFlash instance.
- After starting each TiDB component, TiUP playground reminds you that the cluster is successfully started and provides you some useful information, such as how to connect to the TiDB cluster through the MySQL client and how to access the [TiDB Dashboard](/dashboard/dashboard-intro.md).

You can use the following command to view the command-line flags of the playground component:

```shell
tiup playground --help
```

## Examples

### Check available TiDB versions

```shell
tiup list tidb
```

### Start a TiDB cluster of a specific version

```shell
tiup playground ${version}
```

Replace `${version}` with the target version number.

### Start a TiDB cluster of the nightly version

```shell
tiup playground nightly
```

In the command above, `nightly` indicates the latest development version of TiDB.

### Override PD's default configuration

First, you need to copy the [PD configuration template](https://github.com/pingcap/pd/blob/master/conf/config.toml). Assume you place the copied file to `~/config/pd.toml` and make some changes according to your need, then you can execute the following command to override PD's default configuration:

```shell
tiup playground --pd.config ~/config/pd.toml
```

### Replace the default binary files

By default, when playground is started, each component is started using the binary files from the official mirror. If you want to put a temporarily compiled local binary file into the cluster for testing, you can use the `--{comp}.binpath` flag for replacement. For example, execute the following command to replace the binary file of TiDB:

```shell
tiup playground --db.binpath /xx/tidb-server
```

### Start multiple component instances

By default, only one instance is started for each TiDB, TiKV, and PD component. To start multiple instances for each component, add the following flag:

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### Specify a tag when starting the TiDB cluster to store the data

After you stop a TiDB cluster started using TiUP playground, all cluster data is cleaned up as well. To start a TiDB cluster using TiUP playground and ensure that the cluster data is not cleaned up automatically, you can specify a tag when starting the cluster. After specifying the tag, you can find the cluster data in the `~/.tiup/data` directory. Run the following command to specify a tag:

```shell
tiup playground --tag ${tag_name}
```

For a cluster started in this way, the data files are retained after the cluster is stopped. You can use this tag to start the cluster next time so that you can use the data kept since the cluster was stopped.

## Quickly connect to the TiDB cluster started by playground

TiUP provides the `client` component, which is used to automatically find and connect to a local TiDB cluster started by playground. The usage is as follows:

```shell
tiup client
```

This command provides a list of TiDB clusters that are started by playground on the current machine on the console. Select the TiDB cluster to be connected. After clicking <kbd>Enter</kbd>, a built-in MySQL client is opened to connect to TiDB.

## View information of the started cluster

```shell
tiup playground display
```

The command above returns the following results:

```
Pid    Role     Uptime
---    ----     ------
84518  pd       35m22.929404512s
84519  tikv     35m22.927757153s
86189  tidb     exited
86526  tidb     34m28.293148663s
```

## Scale out a cluster

The command-line parameter for scaling out a cluster is similar to that for starting a cluster. You can scale out two TiDB instances by executing the following command:

```shell
tiup playground scale-out --db 2
```

## Scale in a cluster

You can specify a `pid` in the `tiup playground scale-in` command to scale in the corresponding instance. To view the `pid`, execute `tiup playground display`.

```shell
tiup playground scale-in --pid 86526
```

## Deploy TiProxy

[TiProxy](/tiproxy/tiproxy-overview.md) is the official proxy component from PingCAP, placed between the client and the TiDB server to provide load balancing, connection persistence, service discovery, and other features for TiDB.

Starting from TiUP v1.15.0, you can deploy TiProxy for your cluster using TiUP Playground.

1. Create a `tidb.toml` file and add the following configuration:

    ```
    graceful-wait-before-shutdown=15
    ```

    This configuration item controls the number of seconds TiDB waits before shutting down the server, avoiding client disconnections during cluster scaling-in operations.

2. Start the TiDB cluster:

    ```shell
    tiup playground v8.5.0 --tiproxy 1 --db.config tidb.toml
    ```

    In the playground component, TiProxy-related command-line flags are as follows:

    ```bash
    Flags:
          --tiproxy int                  The number of TiProxy nodes in the cluster. If not specified, TiProxy is not deployed.
          --tiproxy.binpath string       TiProxy instance binary path.
          --tiproxy.config string        TiProxy instance configuration file.
          --tiproxy.host host            Playground TiProxy host. If not provided, TiProxy will still use host flag as its host.
          --tiproxy.port int             Playground TiProxy port. If not provided, TiProxy will use 6000 as its port.
          --tiproxy.timeout int          TiProxy maximum wait time in seconds for starting. 0 means no limit (default 60).
          --tiproxy.version string       The version of TiProxy. If not specified, the latest version of TiProxy is deployed.
    ```

For more information about deploying and using TiProxy, see [TiProxy installation and usage](/tiproxy/tiproxy-overview.md#installation-and-usage).

To use the TiProxy client program `tiproxyctl`, see [Install TiProxy Control](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control).

## Deploy PD microservices

Starting from v8.2.0, [PD microservice mode](/pd-microservices.md) (experimental) can be deployed using TiUP. You can deploy the `tso` microservice and `scheduling` microservice for your cluster using TiUP Playground as follows:

```shell
tiup playground v8.5.0 --pd.mode ms --pd 3 --tso 2 --scheduling 2
```

- `--pd.mode`: setting it to `ms` means enabling the microservice mode for PD.
- `--pd <num>`: specifies the number of APIs for PD microservices. It must be at least `1`.
- `--tso <num>`: specifies the number of instances to be deployed for the `tso` microservice.
- `--scheduling <num>`: specifies the number of instances to be deployed for the `scheduling` microservice.