---
title: Data Migration from AWS Aurora MySQL to TiDB
summary: Using DM to migrate from AWS Aurora MySQL to TiDB
category: tools
---

# Data Migration from AWS Aurora MySQL to TiDB

This document describes how to use DM to migrate from [AWS Aurora MySQL](https://aws.amazon.com/cn/rds/aurora/details/mysql-details/) to TiDB。

## Step 1: Start binlog in Aurora cluster

This document assumes you'll migrate data from two Aurora clusters to  TiDB. The information list of Aurora clusters is as belowed. It indicates Aurora-1 has a single built-in reader endpoint. 

| Cluster | Endpoint | Port | Role |
|:-------- |:--- | :--- | :--- |
| Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Writer |
| Aurora-1 | pingcap-1-us-east-2a.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Reader |
| Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Writer |

During the incremental backup process, you need to set the binglog format as `ROW`. Inactive binlog or incorrect binlog format will hinder data migration using DM. See [Checking items](https://www.pingcap.com/docs-cn/tools/dm/precheck/#%E6%A3%80%E6%9F%A5%E5%86%85%E5%AE%B9) for more information.

> **Warning:** 
>
> Aurora reader cannot start binlog, so it cannot be the upstream master server when using DM to migrate data.

If you need to use GTID for replication, enable GTID for Aurora cluster. 

> **Warning:**
>
> GTID-based data migration requires MySQL 5.7 (Aurora 2.04.1) version or later. 

### Modify binlog relevent parameters in the Aurora cluster 

In Aurora cluster, binlog relevant parameters are in the **cluster parameter group**. See [Enable Binary Logging on the Replication Master](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.html) for more information about enabling binlog. You need to set the `binlog_format` in `ROW` when using DM for migration. 

If GTID is required for migration, set both `gtid-mode` and `enforce_gtid_consistency` as `ON`. See [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora) for more information about enabling GTID-based migration for Aurora cluster. 

> **Warning**: 
>
> In Aurora back-end management system, `gtid_mode` means `gtid-mode`.

## Step 2: Deploy DM cluster

Up to now we recommend using DM-Ansible to deploy DM cluster. See [Deploy Data Migration Using DM-Ansible](https://pingcap.com/docs/dev/how-to/deploy/data-migration-with-ansible/) for more information. 

> **Warning**: 
> 
> - In all the DM config files, use encrypted password generated with dmctl. If the database password is empty, you can pass the encryption. About how to use dmctl to encrypt cleartext password, see [Encrypt the upstream MySQL user password using dmctl](https://pingcap.com/docs/dev/how-to/deploy/data-migration-with-ansible/#encrypt-the-upstream-mysql-user-password-using-dmctl) for more information. 
> - Both the upstream and downstream users need to have the corresponded read-write access permission.

## Step 3: Check the cluster informtaion

The config information is as follows after using DM-Ansible to deploy DM cluster. 

- DM cluster components

    | Component | Host | Port |
    |:------|:---- |:---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master | 172.16.10.71 | 8261 |

- Upstream and Downstream database instance

    | Database instance | Host | Port | Username | Encrypted password |
    |:-------- |:--- | :--- | :--- | :--- |
    | Upstream Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | Upstream Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | Downstream TiDB | 172.16.10.83 | 4000 | root | |

- Configuration in dm-master process config file `{ansible deploy}/conf/dm-master.toml`

    ```toml
    # Master Configuration

    [[deploy]]
    source-id = "mysql-replica-01"
    dm-worker = "172.16.10.72:8262"

    [[deploy]]
    source-id = "mysql-replica-02"
    dm-worker = "172.16.10.73:8262"
    ```

## Step 4: Configurate the task

This document assumes that you need to use both incremental backup and full backup of `test_table` table in `test_db` in Aurora-1 and Aurora-2 instance, and replicate to the `test_table` table of `test_db` in downstream TiDB.

Copy and edit `{ansible deploy}/conf/task.yaml.example` to generate the following config file `task.yaml`: 

```yaml
# The task name. You need to use a different name for each of the multiple tasks that run simultaneously.
name: "test"
# The full backup plus incremental backup for data replication.
task-mode: "all"
# The downstream TiDB config information.
target-database:
  host: "172.16.10.83"
  port: 4000
  user: "root"
  password: ""

# Configuration of all the upstream MySQL instances required by the current data replication task.
mysql-instances:
-
  # The ID of upstream instances or the replication group. You can refer to the configuration of `source_id` in the "inventory.ini" file or in the "dm-master.toml" file.
  source-id: "mysql-replica-01"
  # The configuration item name of the black and white lists of the name of the database/table to be replicated, used to quote the global black and white lists configuration that is set in the global black-white-list below.
  black-white-list: "global"
  # The configuration item name of mydumper, used to quote the global mydumper configuration. 
  mydumper-config-name: "global"

-
  source-id: "mysql-replica-02"
  black-white-list: "global"
  mydumper-config-name: "global"

# The global configuration of black and white lists. Each instance can quote it by the configuration item name.
black-white-list:
  global:
    do-tables:                        # The white list of the upstream table to be replicated
    - db-name: "test_db"              # The database name of the table to be replicated 
      tbl-name: "test_table"          # The name of the table to be replicated 

# mydumper global configuration. Each instance can quote with the configuration item name. 
mydumpers:
  global:
    extra-args: "-B test_db -T test_table"  # It can only output the `test_table` of `test_db` and configure the parameter of mydumper. 
```

## Step 5: Start the task

1. Go to dmctl directory `/home/tidb/dm-ansible/resources/bin/`

2. Start dmctl using:

    ```bash
    ./dmctl --master-addr 172.16.10.71:8261
    ```

3. Start data replication task using:

    ```bash
    # `task.yaml` is the previous edited config file 
    start-task ./task.yaml
    ```
    
    - The task has been started successfully if the returned results do not report any error. 
    - The permission of upstream Aurora user may not be supported by TiDB if the returned results report the following errors:  
        
        ```json
        {
            "id": 4,
            "name": "source db dump privilege chcker",
            "desc": "check dump privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        },
        {
            "id": 5,
            "name": "source db replication privilege chcker",
            "desc": "check replication privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        }
        ```
        
        Using either of the following solutions, you can use `start-task` to restart the task:
        1. Remove the unnecessary permission not supported by TiDB for Aurora user when migrating data 
        2. If Aurora user is ensured to have the permission that DM needs, then add the following configuration item in `task.yaml` config file to skip the permission precheck when start the task. 
            ```yaml
            ignore-checking-items: ["dump_privilege", "replication_privilege"]
            ```

## Step 6: Query the task

If you want to know whether there is a on-going data replication in DM cluster or the information about the task status, execute the following command to query:

```bash
query-status
```

> **Warning**: 
>
> If the returned results of the command report the following error, it means the lock cannot be acquired when dumping in full backup. 
>   ```bash
>   Couldn't acquire global lock, snapshots will not be consistent: Access denied for user 'root'@'%' (using password: YES)
>   ```
>If the consistency between dump file and metadata is allowed not to be ensured by FTML, or the writing process in upstream can be paused, you can skip the error by adding `--no-locks` in `extra-args` under the `mydumpers`. The procedure is as follows: 
> 1. Use `stop-task` to stop the paused task caused by irregular dumping 
> 2. Update the `extra-args: "-B test_db -T test_table"` in task.yaml to `extra-args: "-B test_db -T test_table --no-locks"`
> 3. Use `start-task` to restart the task
