---
title: Migrate Data from MySQL SQL File
summary: Learn how to migrate data from MySQL SQL files to TiDB using TiDB Lightning.
category: how-to
---

# Migrate Data from MySQL SQL File

This document describes how to migrate data from MySQL SQL files to TiDB using TiDB Lightning. For details on how to generate MySQL SQL files, see [Mydumper](/mydumper-overview.md) or [Dumpling](/export-or-backup-using-dumpling.md).

## Deploy TiDB Lightning

The data migration process described in this document uses TiDB Lightning. Before you start the migration, [deploy TiDB Lightning](/tidb-lightning/deploy-tidb-lightning.md).

> **Note:**
>
> - If you choose the importer backend, you need to deploy tikv-importer along with TiDB Lightning. During the import process, the TiDB cluster cannot provide services. This mode imports data quickly, which is suitable for importing a large amount of data (above the TB level).
> - If you choose the TiDB backend, only TiDB Lightning is required. The cluster can provide services normally during the import.
> - For detailed differences between the two backend mode, see [TiDB Lightning Backend](/tidb-lightning/tidb-lightning-tidb-backend.md).

## Configure data source of TiDB Lightning

This document takes the TiDB backend as an example. Add the `tidb-lightning.toml` configuration file and add the following major configurations in the file:

1. Set the `data-source-dir` under `[mydumper]` to the path of the MySQL SQL file.

    ```
    [mydumper]
    # data source directory
    data-source-dir = "/data/export"
    ```

    > **Note:**
    >
    > If a corresponding schema already exists in the downstream, set `no-schema=true` to skip the creation of schema.

2. Add the TiDB configurations of the target cluster.

    ```
    [tidb]
    # the target cluster information. Fill in one address of tidb-server
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    ```

For other configurations, see [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Run TiDB Lightning to import data

Run TiDB Lightning to start the import operation. If you start TiDB Lightning by using `nohup` directly in the command line, the program might exit because of the `SIGHUP` signal. Therefore, it is recommended to write `nohup` in a script. For example:

```
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

When the import operation is started, you can view the progress by the following two ways:

- `grep` the keyword `progress` in logs, which is updated every 5 minutes by default.
- Access the monitoring dashboard. See [Monitor TiDB Lightning](/tidb-lightning/monitor-tidb-lightning.md) for details.
