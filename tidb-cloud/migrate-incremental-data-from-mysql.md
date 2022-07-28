---
title: Migrate Incremental Data from MySQL
summary: Learn how to migrate incremental data from MySQL to TiDB Cloud.
---

# Migrate Incremental Data from MySQL

TiDB Cloud does not provide incremental data migration feature yet. You need to deploy TiDB Data Migration (DM) manually to perform incremental migration to TiDB Cloud. For installation steps, see [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup).

## Step 1. Create the data source

You need to create a data source first. The data source is a MySQL instance that you want to migrate data from. The following is an example of creating a data source. You need to replace the values of MySQL IP, Port, user name and password with your own values.

```shell
# Encrypt MySQL password
[root@localhost ~]# tiup dmctl encrypt {mysq-user-password}
mZMkdjbRztSag6qEgoh8UkDY6X13H48=

[root@localhost ~]# cat dm-source1.yaml
```

```yaml
# MySQL Configuration.
source-id: "mysql-replica-01"

# Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs.
# To enable this mode, the upstream MySQL must also enable GTID.
# If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
enable-gtid: true

from:
  host: "172.16.5.138"
  user: "lzy"
  password: "mZMkdjbRztSag6qEgoh8UkDY6X13H48="
  port: 3307
```

Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source1.yaml
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source1.yaml
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-172.16.7.154-9262"
        }
    ]
}
```

The parameters used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
|`operate-source create`|Loads the data source to the DM cluster.|

## Step 2. Crate a migration task

Edit the `task.yaml` file. Configure the incremental migration mode and the starting point of the data source. You can find the starting point in the metadata file in the file exported by Dumpling.

```toml
# Get the contents of the metadata in the file exported by Dumpling
# Use it to configure the incremental migration starting point
# cat metadata
Started dump at: 2022-05-24 11:19:37
SHOW MASTER STATUS:
    Log: mysql-bin.000001
    Pos: 77092852
    GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-640

Finished dump at: 2022-05-24 11:19:53
```

Based on the above starting point information, create a migration task as follows.

```toml
## ********* Task Configuration *********
name: test-task1
# shard-mode: "pessimistic"
# Task mode. The "incremental" mode only performs incremental data migration.
task-mode: incremental
# timezone: "UTC"

## ******** Data Source Configuration **********
## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data migration error.
##  This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
syncers:         # The running configurations of the sync processing unit.
  global:        # Configuration name.
  safe-mode: false   # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental migration task, DM automatically enables the safe mode.

mysql-instances:
  - source-id: "mysql-replica-01"
    block-allow-list:  "bw-rule-1"
    route-rules: ["route-rule-1"]
    filter-rules: ["tpcc-filter-rule"]
    syncer-config-name: "global"                   # You can use the syncers incremental data configuration above.
    meta:                                          # When task-mode is "incremental" and the target database does not have a checkpoint, DM uses the binlog position as the starting point. If the target database has a checkpoint, DM uses the checkpoint as the starting point.
    binlog-name: "mysql-bin.000001"
    binlog-pos: 77092852
    binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-640"

## ******** Configuration of the Target TiDB on TiDB Cloud **********
target-database:    # the Target TiDB on TiDB Cloud
  host: "tidb.70593805.b973b556.ap-northeast-1.prod.aws.tidbcloud.com"
  port: 4000
  user: "root"
  password: "oSWRLvR3F5GDIgm+l+9h3kB72VFWBUwzOw=="     # If the password is not empty, it is recommended to use a dmctl-encrypted cipher

## ******** Function Configuration **********
block-allow-list:
  bw-rule-1:
    do-dbs: ["~^tpcc.*"]

routes:                       # Table renaming rules ('routes') from upstream to downstream tables, in order to support merging different tables into a single target table.
  route-rule-1:               # Rule name.
    schema-pattern: "tpcc"    # Rule for matching upstream schema names. It supports the wildcards "*" and "?".
    target-schema: "tpdd"     # Name of the target schema.

filters:
  tpcc-filter-rule:
    schema-pattern: "tpcc"
    events: ["drop database"]
    action: Ignore

##  ******** Ignore check items **********
ignore-checking-items: ["table_schema"]
```

For detailed task configurations, see [DM Task Configurations](https://docs.pingcap.com/tidb/stable/task-configuration-file-full).

## Step 3. Check the migration task configuration

Run the following command to check the migration task configuration:

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 check-task dm-task1.yaml
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 check-task dm-task1.yaml
{
    "result": true,
    "msg": "check pass!!!"
}
```

## Step 4. Start the migration task

Run the following command to start the migration task:

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 start-task dm-task1.yaml
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 start-task dm-task1.yaml
{
    "result": true,
    "msg": "",
    "sources": [
        {
           "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-172.16.7.154-9262"
        }
    ],
    "checkResult": ""
}
```

The parameters used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
|`start-task`           |Starts the migration task.|

If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

If you encounter any problem, refer to [DM error handling](https://docs.pingcap.com/tidb/stable/dm-error-handling) and [DM FAQ](https://docs.pingcap.com/tidb/stable/dm-faq).

## Check the migration task status

To learn whether the DM cluster has an ongoing migration task and view the task status, run the `query-status` command using `tiup dmctl`:

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 query-status test-task1
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 query-status test-task1
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "dm-172.16.7.154-9262",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test-task1",
                    "stage": "Running",
                    "unit": "Sync",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "sync": {
                        "totalEvents": "3",
                        "totalTps": "0",
                        "recentTps": "0",
                        "masterBinlog": "(mysql-bin.000001, 77093211)",
                        "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-641",
                        "syncerBinlog": "(mysql-bin.000001, 77093211)",
                        "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-641",
                        "blockingDDLs": [
                        ],
                       "unresolvedGroups": [
                        ],
                        "synced": true,
                        "binlogType": "remote",
                        "secondsBehindMaster": "0",
                        "blockDDLOwner": "",
                     "conflictMsg": ""
                    }
                }
            ]
        ]
}
```

For a detailed interpretation of the results, see [Query Status](https://docs.pingcap.com/tidb/stable/dm-query-status).

## Step 5. Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl print the related information in logs. The log directories of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.
