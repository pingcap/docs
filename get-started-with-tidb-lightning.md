---
title: TiDB Lightning Tutorial
summary: Learn how to deploy TiDB Lightning and import full backup data to TiDB.
aliases: ['/docs/dev/get-started-with-tidb-lightning/','/docs/dev/how-to/get-started/tidb-lightning/']
---

# TiDB Lightning Tutorial

[TiDB Lightning](https://github.com/pingcap/tidb-lightning) is a tool used for fast full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Mydumper or CSV data source. You can use it in the following two scenarios:

+ Import **large amounts** of **new** data **quickly**
+ Back up and restore all the data

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

## Prerequisites

This tutorial assumes you use several new and clean CentOS 7 instances. You can use VMware, VirtualBox or other tools to deploy a virtual machine locally or a small cloud virtual machine on a vendor-supplied platform. Because TiDB Lightning consumes a large amount of computer resources, it is recommended that you allocate at least 16 GB memory and CPU of 32 cores for running it with the best performance.

> **Warning:**
>
> The deployment method in this tutorial is only recommended for test and trial. **Do not apply it in the production or development environment.**

## Prepare full backup data

First, use [`mydumper`](/mydumper-overview.md) to export data from MySQL:

{{< copyable "shell-regular" >}}

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

In the above command:

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 256`: means a table is partitioned into chunks and one chunk is 256 MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

After executing this command, the full backup data is exported to the `/data/my_database` directory.

## Deploy TiDB Lightning

### Step 1: Deploy TiDB cluster

Before the data import, you need to deploy a TiDB cluster (later than v2.0.9). In this tutorial, TiDB v4.0.3 is used. For the deployment method, refer to [TiDB Introduction](/overview.md).

### Step 2: Download TiDB Lightning installation package

Download the TiDB Lightning installation package from the following link:

- **v4.0.3**: [tidb-toolkit-v4.0.3-linux-amd64.tar.gz](https://download.pingcap.org/tidb-toolkit-v4.0.3-linux-amd64.tar.gz)

> **Note:**
>
> Choose the same version of TiDB Lightning as that of the TiDB cluster.

### Step 3: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` in the package to the server where TiDB Lightning is deployed.
2. Upload the [prepared data source](#prepare-full-backup-data) to the server.
3. Configure `tidb-lightning.toml` as follows:

    ```toml
    [lightning]
    # logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Uses the Local-backend
    backend = "local"
    # Sets the directory for temporarily storing the sorted key-value pairs.
    # The target directory must be empty.
    "sorted-kv-dir" = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Mydumper local source data directory
    data-source-dir = "/data/my_datasource/"

    [tidb]
    # Information of the target cluster
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # The PD address of the cluster
    pd-addr = "172.16.31.3:2379"
    ```

4. After configuring the parameters properly, use a `nohup` command to start the `tidb-lightning` process. If you directly run the command in the command-line, the process might exit because of the SIGHUP signal received. Instead, it's preferable to run a bash script that contains the `nohup` command:

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

### Step 4: Check data integrity

After the import is completed, TiDB Lightning exits automatically. If the import is successful, you can find `tidb lightning exit` in the last line of the log file.

If any error occurs, refer to [TiDB Lightning Troubleshooting](/troubleshoot-tidb-lightning.md).

## Summary

This tutorial briefly introduces what TiDB Lightning is and how to quickly deploy a TiDB Lightning cluster to import full backup data to the TiDB cluster.

For detailed features and usage about TiDB Lightning, refer to [TiDB Lightning Overview](/tidb-lightning/tidb-lightning-overview.md).
