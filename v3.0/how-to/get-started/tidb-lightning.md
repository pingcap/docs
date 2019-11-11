---
title: TiDB Lightning Tutorial
summary: Learn how to deploy TiDB Lightning and import full backup data to TiDB.
category: how-to
---

# TiDB Lightning Tutorial

[TiDB Lightning](https://github.com/pingcap/tidb-lightning) is a tool used for fast full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Mydumper or CSV data source. You can use it in the following two scenarios:

+ Import **large amounts** of **new** data **quickly**
+ Back up and restore all the data

The TiDB Lightning tool set consists of two components:

- **`tidb-lightning`** (the "front end") reads the data source and imports the database structure into the TiDB cluster, and also transforms the data into Key-Value (KV) pairs and sends them to `tikv-importer`.

- **`tikv-importer`** (the "back end") combines and sorts the KV pairs and then imports these sorted pairs as a whole into the TiKV cluster.

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

## Prerequisite

The operations in this tutorial requires several new and clean instances on the CentOS 7 system. You can use VMware, VirtualBox and other tools to deploy a virtual host locally or to deploy a small cloud virtual host on a vendor-supplied platform. Because TiDB Lightning consumes a large amount of computer resources, it is recommended that you allocate at least 4 GB for the memory.

> **Warning:**
>
> The deployment method in this tutorial is only for test and trial, not for the production or development environment.

## Prepare full backup data

Use [`mydumper`](/v3.0/reference/tools/mydumper.md) to export data from MySQL:

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

Before the data import, first you need to deploy a TiDB cluster (later than version v2.0.9). In this tutorial, TiDB v3.0.4 is used. For the deployment method, refer to [TiDB Introduction](/v3.0/overview.md).

### Step 2: Download TiDB Lightning installation package

Download the TiDB Lightning installation package from the following link:

- **v3.0.4**: [tidb-toolkit-v3.0.4-linux-amd64.tar.gz](http://download.pingcap.org/tidb-toolkit-v3.0.0-linux-amd64.tar.gz)

> **Note:**
>
> Choose the same version as the TiDB cluster.

### Step 3: Start `tikv-importer`

1. Upload `bin/tikv-importer` in the package to the server where TiDB Lightning is deployed.

2. Configure `tikv-importer.toml`.

    ```toml
    # The template for the TiKV Importer configuration file

    # Log file
    log-file = "tikv-importer.log"
    # Log level: "trace", "debug", "info", "warn", "error" or "off"
    log-level = "info"

    [server]
    # The listening address of tikv-importer. tidb-lightning connects to this address for data write.
    addr = "0.0.0.0:8287"

    [import]
    # The file path in which the engine file is stored.
    import-dir = "/mnt/ssd/data.import/"
    ```

3. Operate `tikv-importer`:

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

### Step 4: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` in the installation package to the server where TiDB Lightning is deployed.
2. Upload the [prepared data source](#prepare-full-backup-data) to the server.
3. Configure the parameters for `tidb-lightning` and operate `tidb-lightning`. If you directly use the `nohup` command in the command-line to start the `tidb-lightning` process, the process might exit because of the SIGHUP signal received. It is recommended that you use the `nohup` command in the script. For example:

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning \
                --importer 172.16.31.10:8287 \
                -d /data/my_database/ \
                --tidb-server 172.16.31.2 \
                --tidb-user root \
                --log-file tidb-lightning.log \
            > nohup.out &
    ```

### Step 5: Check data

After the import is completed, TiDB Lightning exits automatically. If the import is successful, `tidb lightning exit` is displayed in the last line of the log.

If any error occurs, refer to [TiDB Lightning Troubleshooting](/v3.0/how-to/troubleshoot/tidb-lightning.md)

## Summary

This tutorial briefly introduces TiDB Lightning, and describes how to deploy a set of TiDB Lightning cluster and imports the full backup data to the TiDB cluster.

For more details about the features and usage of TiDB Lightning, refer to [TiDB Lightning Overview](/v3.0/reference/tools/tidb-lightning/overview.md).
