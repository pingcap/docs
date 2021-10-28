---
title: Incrementally synchronize data From Aurora MySQL to TiDB
summary: Incrementally synchronize data From Aurora MySQL to TiDB
---

# Incrementally Replicate Data From Aurora MySQL to TiDB

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform. It supports the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. DM helps you reduce the operation cost of data migration and simplify the troubleshooting process.

This document describes how to use DM for incremental replication.

## Prerequisites

- [Deploy DM using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)

***

## Step 1. Precheck

DM relies on the `ROW`-formatted binlog for incremental replication, so you need to enable the binary logging for an Aurora MySQL cluster. For the configuration instructions, refer to Amazon's document [Enable binary for an Aurora Cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls).

It is recommmend to  migrate data based on GTIDs (global transaction identifiers). For how to enable it, refer to Amazon's document [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora).

## Step 2. Configure the data source

Create a configuration file describing the upstream library information `source1.yaml`:

```yaml
# Unique name for database
source-id: "aurora-replica-01"

# To migrate data based on GTID, you need to set this item to true.
enable-gtid: false

from:
  host: "${host}" # eg: test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com
  user: "root"
  password: "${password}"  # It is recommended to use database passwords encrypted by `dmctl encrypt`.
  port: 3306
```

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source1.yaml
```

| Parameter | Description |
| :--------| :------------|
| `--master-addr`                     | Master API server addr. |
| `operate-source`                    | `create`/`update`/`stop`/`show` upstream MySQL/MariaDB source. |

Usage of `dmctl encrypt`: [Encrypt the database password using dmctl](https://docs.pingcap.com/tidb-data-migration/stable/manage-source#encrypt-the-database-password)

All avaiable command of `dmctl` could be found in [Maintain DM Clusters Using dmctl](https://docs.pingcap.com/tidb-data-migration/stable/dmctl-introduction)

When the data sources are successfully added, the return information of each data source includes a DM-worker bound to it.

```bash
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        }
    ]
}
```

## Step 3. Configure the task

> **Note:**
>
> Because Aurora does not support flushing tables with read lock (FTWRL), when you only perform the full data migration to export data, write operations have to be paused. See [AWS document](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls) for details. In the following example, both full data migration and incremental replication are performed, and DM automatically enables the `safe mode` to solve the pause issue. To ensure data consistency in other task modes, refer to [AWS document](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls).

This following example migrates the data in Aurora and incrementally replicates the data to TiDB in real time, which is the **full data migration plus incremental replication** mode. According to the TiDB cluster information above, the added `source-id`, and the table to be migrated, you can save the following task configuration file `task.yaml`:

```yaml
# The task name. You need to use a different name for each of the multiple tasks that run simultaneously.
name: "test"
# Description: the task mode that can be used to specify the data migration task to be executed.
# 1. `full`: only makes a full backup of the upstream database and then imports the full data to the downstream database.
# 2. `incremental`: Only replicates the incremental data of the upstream database to the downstream database using the binlog. You can set the meta configuration item of the instance configuration # # to specify the starting position of incremental replication.
# 3. `all`: full + incremental. Makes a full backup of the upstream database, imports the full data to the downstream database, and then uses the binlog to make an incremental replication to the downstream database starting from the exported position during the full backup process (binlog position).
task-mode: "incremental"
# The downstream TiDB configuration information.
target-database:
  host: "${host}"
  port: ${port}
  user: "${user_name}"
  password: "${password}"

# Configuration of all the upstream MySQL instances required by the current data migration task.
mysql-instances:
- source-id: "aurora-replica-01"
     # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used.
  meta:
    binlog-name: binlog.000001
    binlog-pos: 4
    binlog-gtid: "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"  # You need to set this argument if you specify `enable-gtid: true` for the source of the incremental task.

  # The configuration items of the block and allow lists of the schema or table to be migrated, used to quote the global block and allow lists configuration. For global configuration, see the `block-allow-list` below.
  block-allow-list: "listA"
  mydumper-config-name: "configA"


# The configuration of block and allow lists.
block-allow-list:
  listA:                             # Quoted by block-allow-list: "listA" above
    do-dbs: ["dbname"]            # The allow list of the upstream table to be migrated. Database tables that are not in the allow list will not be migrated.

# The configuration of the dump unit.
mydumpers:
   configA:                            # Quoted by mydumper-config-name: "configA" above
    extra-args: "--consistency none"  # Aurora does not support FTWRL, you need to configure this option to bypass FTWRL.
```

## Step 4. Start the task

Start the task using `dmctl` through TiUP.

> **Note:**
>
> Currently, when using `dmctl` in TiUP, you need to use the absolute path of `task.yaml`. TiUP will support the relative path in later versions.

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 start-task /absolute/path/to/task.yaml --remove-meta
```

If the task is successfully started, the following information is returned:

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        }
    ]
}
```

If `source db replication privilege checker` and `source db dump privilege checker` errors are in the returned information, check whether unrecognized privileges exsit in the `errorMsg` field. For example:

```
line 1 column 287 near \"INVOKE LAMBDA ON *.* TO...
```

The returned information above shows that the `INVOKE LAMBDA` privilege causes an error. If the privilege is Aurora-specific, add the following content to the configuration file to skip the check. 

```
ignore-checking-items: ["replication_privilege","dump_privilege"]
```

## Step 5. Query the task and validate the data

Check the information of the on-going migration task and the task status using `dmctl` through TiUP.

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status
```

If the task is running normally, the following information is returned.

```
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "test",
            "taskStatus": "Running",
            "sources": [
                "aurora-replica-01",
                "aurora-replica-02"
            ]
        }
    ]
}
```

You can query data in the downstream, modify data in Aurora, and validate the data migrated to TiDB.

*** 

## Helpful Topics  

- [DM Administration Guide](/data-migration/todo.md)
- [How to filter binlog event](/data-migration/advanced-migration/binlog-filter.md)
- [How to work with GH-ost and PT-osc](/data-migration/advanced-migration/ghost-ptosc.md)
- [How to merge multiple tables with multiple databases](/data-migration/advanced-migration/merge-db-table.md)
- [How to deal with the situation where there are multiple tables downstream](https://docs.pingcap.com/tidb-data-migration/stable/usage-scenario-downstream-more-columns)
