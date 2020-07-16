---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
aliases: ['/docs/dev/pd-recover/','/docs/dev/reference/tools/pd-recover/']
---

# PD Recover User Guide

PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally.

## Compile from source code

1. [Go](https://golang.org/) Version 1.13 or later because the Go modules are used.
2. In the root directory of the [PD project](https://github.com/pingcap/pd), use the `make pd-recover` command to compile and generate `bin/pd-recover`

> **Note:**
>
> Generally, you do not need to compile source code because the PD Control tool already exists in the released Binary or Docker. However, developer users can refer to the above instruction for compiling source code.

## Download TiDB installation package

If you want to download the latest version of `pd-recover`, directly download the TiDB package, because `pd-recover` is included in the TiDB package.
| Package download link | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (pd-recover) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |
> **Note:**
>
> `{version}` indicates the version number of TiDB. For example, if `{version}` is `v4.0.0`, the package download link is `https://download.pingcap.org/tidb-v4.0.0-linux-amd64.tar.gz`. You can also download the latest unpublished version by replacing `{version}` with `latest`.

## Quick Start

This section describes how to use PD Recover to recover a PD cluster.

### Get cluster ID

The cluster ID can be obtained from the log of PD, TiKV or TiDB. To get the cluster ID, you can view the log directly on the server.

#### Get cluster ID from PD log (recommended)

To get the cluster ID from the PD log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd.log | grep "init cluster id"
```

```bash
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
...
```

#### Get cluster ID from TiDB log

To get the cluster ID from the TiDB log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tidb.log | grep "init cluster id"
```

```bash
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
...
```

#### Get cluster ID from TiKV log

To get the cluster ID from the TiKV log, run the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/tikv.log | grep "connect to PD cluster"
```

```bash
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
...
```

### Get allocate ID

The allocate ID value you specify must be larger than the currently largest allocate ID value. To get allocate ID you can either get it from Monitor, or view the log directly on the server.

#### Get allocate ID from the monitor (recommended)

To get allocate ID from the monitor, you need to make sure that the metrics you are viewing is **the last PD leader**, and you can get the max allocate ID from `Current ID allocation` panel in PD dashboard.
 
#### Get allocate ID from PD log

To get the allocate ID from the PD log, you need to make sure that the log you are viewing is **the last PD leader**, and you can get the max allocate ID by running the following command:

{{< copyable "shell-regular" >}}

```bash
cat {{/path/to}}/pd*.log | grep "idAllocator allocates a new id" |  awk -F'=' '{print $2}' | awk -F']' '{print $1}' | sort -r | head -n 1
```

```bash
4000
...
```

Or you can simply run the above command in all pd servers to find the largest one.

### Deploy a new PD cluster

The existed PD cluster should be stopped at first. Before deploying a new PD cluster, you need to delete the old data directory which specified by `--data-dir`.

### Use pd-recover

{{< copyable "shell-regular" >}}

```bash
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### Restart the whole cluster

When the recovery success information is prompted, restart the whole cluster.

## FAQ

### Multiple cluster IDs are found when getting the cluster ID

When a PD cluster is created, a new cluster ID is generated. You can determine the cluster ID of the old cluster by viewing the log.

### The error `dial tcp 10.0.1.13:2379: connect: connection refused` is returned when executing `pd-recover`

The PD service is required when you execute `pd-recover`. Deploy and start the PD cluster before you use PD Recover.
