---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy the local TiDB cluster using the playground component of TiUP.
category: tools
---

# Quickly Deploy a Local TiDB Cluster

The TiDB cluster is a distributed system that consists of multiple components. A typical TiDB cluster consists of at least three PD nodes, three TiKV nodes, and two TiDB nodes. If you want to try TiDB quickly, it is time-consuming and not easy to manually deploy so many components. This document introduces the playground component of TiUP and how to quickly build a local TiDB test environment using the playground component.

## Overview of playground

The basic usage of the playground component is shown as follows:

```bash
tiup playground [version] [flags]
```

If you directly execute the command above, the locally installed TiDB/TiKV/PD component is used or the stable version of these components start a cluster that consists of one TiKV instance, one TiDB instance, and one PD instance. The following tasks will be performed:

- The version is not specified. In this situation, TiUP uses the latest version of the installed playground component. Assume that the latest version is v0.0.6, this command will work the same as `tiup playground:v0.0.6`.
- If you have not used TiUP to install the TiDB/TiKV/PD component, the playground component uses the latest stable version of these components, and then these instances are started and operated.
- The version of each TiDB/PD/TiKV component is not specified. By default, the latest released version of each component is used. Assume that the latest version is v4.0.0-rc, this command will work the same as `tiup playground:v0.0.6 v4.0.0-rc`.
- The playground component does not specify the number of each component. By default, a cluster that consists of one TiDB instance, one TiKV instance, and one PD instance is started.
- After starting each component, the playground reminds you that the cluster is successfully started and provides you some useful information, such as how to connect to the TiDB cluster through the MySQL client and how to access the dashboard.

The flags of the playground command-line tool are described as follows:

```bash
Flags:
      --db int                   Specifies the number of TiDB instances in the cluster, 1 by default.
      --db.binpath string        Specifies the location of TiDB binary files, for development and debugging. You can ignore this flag.
      --db.config string         Specifies TiDB configuration files, for development and debugging. You can ignore this flag.
  -h, --help                     Prints the help information.
      --host string              Sets the listening address of each component (127.0.0.1 by default). For other computers to access components, you can set the address to 0.0.0.0.
      --kv int                   Specifies the number of TiKV instances in the cluster, 1 by default.
      --kv.binpath string        Specifies the location of TiKV binary files, for development and debugging. You can ignore this flag.
      --kv.config string         Specifies TiKV configuration files, for development and debugging. You can ignore this flag.
      --monitor                  Determines whether to start the monitor.
      --pd int                   Specifies the number of PD instances in the cluster, 1 by default.
      --pd.binpath string        Specifies the location of PD binary files, for development and debugging. You can ignore this flag.
      --pd.config string         Specifies PD configuration files, for development and debugging. You can ignore this flag.
      --tiflash int              Specifies the number of TiFlash instances in the cluster, 0 by default.
      --tiflash.binpath string   Specifies the location of TiFlash binary files, for development and debugging. You can ignore this flag.
      --tiflash.config string    Specifies TiFlash configuration files, for development and debugging. You can ignore this flag.
```

## Examples

### Use the nightly version to start a TiDB cluster

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly
```

In the command above, `nightly` is the version number of the cluster. Similarly, you can replace `nightly` with `v4.0.0-rc`, and the command is `tiup playground v4.0.0-rc`.

### Start a cluster with monitor

{{< copyable "shell-regular" >}}

```shell
tiup playground nightly --monitor
```

This command starts Prometheus on port 9090 to display the time series data in the cluster.

### Override PD's default configuration

Copy the [PD configuration template](https://github.com/pingcap/pd/blob/master/conf/config.toml). If you copy the configuration file to the `~/config/pd.toml` path and make some changes according to your need, execute the following command to override PD's default configuration:

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config ~/config/pd.toml
```

### Replace the default binary files

By default, when playground is started, each component is started using the binary files from the official image package. If you want to put a temporarily compiled local binary file into the cluster for testing, you can use the `--{comp}.binpath` flag for replacement. For example, execute the following command to replace the binary file of TiDB:

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.binpath /xx/tidb-server
```

### Start multiple component instances

By default, only one instance is started for TiDB/TiKV/PD. To start multiple instances for each component, add the following flag:

{{< copyable "shell-regular" >}}

```shell
tiup playground v3.0.10 --db 3 --pd 3 --kv 3
```

## Quickly connect to the started playground cluster

TiUP provides the `client` component, which is used to automatically find and connect to a locally-started playground cluster. The usage is as follows:

{{< copyable "shell-regular" >}}

```shell
tiup client
```

This command provides a list of playground clusters that the current machine has started on the console. Select the playground cluster to connected. After clicking <kbd>Enter</kbd>, a built-in MySQL client is opened to connect to TiDB.
