---
title: Incrementally synchronize data From Aurora MySQL to TiDB
summary: Incrementally synchronize data From Aurora MySQL to TiDB
---

# Incrementally synchronize data From Aurora MySQL to TiDB

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. It can help to reduce the operation cost of data migration and simplify the troubleshooting process.

This article only introduces how to use DM for incremental synchronization

## Complete the following tasks before start

- [Deploy DM using TiUP](/data-migration/quick_install_tools.md)

***

## Step 1. Precheck

DM relies on the `ROW`-formatted binlog for incremental replication. See [Enable binary for an Aurora Cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls) for the configuration instruction.

If GTID is enabled in Aurora, you can migrate data based on GTID. For how to enable it, see [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora). To migrate data based on GTID, you need to set `enable-gtid` to `true` in the configuration file of data source in [Configure the data source](#configure-the-data-source).

> **Note:**
>
> + GTID-based data migration requires MySQL 5.7 (Aurora 2.04) version or later.

## Step 2. Configure the data source

> **Note:**
>
> The configuration file used by DM supports database passwords in plaintext or ciphertext. It is recommended to use password encrypted using dmctl. To obtain the ciphertext password, see Encrypt the database password using dmctl.

Save the following configuration files of data source according to the example, in which the value of `source-id` will be used in the task configuration in step 3.

The content of `source1.yaml`:

```yaml
# Aurora-1
source-id: "aurora-replica-01"

# To migrate data based on GTID, you need to set this item to true.
enable-gtid: false

from:
  host: "test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com"
  user: "root"
  password: "OiG90CGm3CEbXan6ZSd/SUAsofxJAZo="
  port: 3306
```

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source1.yaml
```

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
> Because Aurora does not support FTWRL, write operations have to be paused when you only perform the full data migration to export data. See [AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls) for details. In this example, both full data migration and incremental replication are performed, and DM automatically enables the `safe mode`to solve this pause issue. To ensure data consistency in other combinations of task mode, see [AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls).

This example migrates the existing data in Aurora and replicates incremental data to TiDB in real time, which is the **full data migration plus incremental replication** mode. According to the TiDB cluster information above, the added `source-id`, and the table to be migrated, save the following task configuration file `task.yaml`:

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
  port: 4000
  user: "root"
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

The returned information above shows that the `INVOKE LAMBDA` privilege causes an error. If the privilege is Aurora-specific, add the following content to the configuration file to skip the check. DM will improve the automatic handling of Aurora privileges in later versions.

```
ignore-checking-items: ["replication_privilege","dump_privilege"]
```

## Step 5: Query the task and validate the data

Use `dmctl` through TiUP to query information of the on-going migration task and the task status.

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
