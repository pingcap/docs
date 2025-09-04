---
title: 将大型 MySQL 分片数据集迁移并合并到 TiDB Cloud
summary: 了解如何将大型 MySQL 分片数据集迁移并合并到 TiDB Cloud。
---

# 将大型 MySQL 分片数据集迁移并合并到 TiDB Cloud

本文档介绍如何将大型 MySQL 数据集（例如，大于 1 TiB）从不同分区迁移到 TiDB Cloud 并进行合并。在完成全量数据迁移后，你可以根据业务需求使用 [TiDB Data Migration (DM)](https://docs.pingcap.com/tidb/stable/dm-overview) 进行增量迁移。

本文档中的示例使用了跨多个 MySQL 实例的复杂分片迁移任务，并涉及自增主键冲突的处理。本示例场景同样适用于在单个 MySQL 实例内合并不同分片表的数据。

## 示例中的环境信息

本节介绍示例中所用上游集群、DM 及下游集群的基本信息。

### 上游集群

上游集群的环境信息如下：

- MySQL 版本：MySQL v5.7.18
- MySQL instance1：
    - schema `store_01` 和表 `[sale_01, sale_02]`
    - schema `store_02` 和表 `[sale_01, sale_02]`
- MySQL instance2：
    - schema `store_01` 和表 `[sale_01, sale_02]`
    - schema `store_02` 和表 `[sale_01, sale_02]`
- 表结构：

  ```sql
  CREATE TABLE sale_01 (
  id bigint(20) NOT NULL auto_increment,
  uid varchar(40) NOT NULL,
  sale_num bigint DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY ind_uid (uid)
  );
  ```

### DM

DM 的版本为 v5.3.0。你需要手动部署 TiDB DM。详细步骤参见 [使用 TiUP 部署 DM 集群](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

### 外部存储

本文档以 Amazon S3 为例。

### 下游集群

分片的 schema 和表将被合并到表 `store.sales` 中。

## 从 MySQL 到 TiDB Cloud 的全量数据迁移

以下是将 MySQL 分片的全量数据迁移并合并到 TiDB Cloud 的流程。

在以下示例中，你只需将表中的数据导出为 **CSV** 格式。

### 步骤 1. 在 Amazon S3 bucket 中创建目录

在 Amazon S3 bucket 中创建一级目录 `store`（对应数据库级别）和二级目录 `sales`（对应表级别）。在 `sales` 下，为每个 MySQL 实例创建三级目录（对应 MySQL 实例级别）。例如：

- 将 MySQL instance1 的数据迁移到 `s3://dumpling-s3/store/sales/instance01/`
- 将 MySQL instance2 的数据迁移到 `s3://dumpling-s3/store/sales/instance02/`

如果存在跨多个实例的分片，可以为每个数据库创建一个一级目录，为每个分片表创建一个二级目录，然后为每个 MySQL 实例创建一个三级目录以便管理。例如，如果你想将 MySQL instance1 和 MySQL instance2 的 `stock_N.product_N` 表迁移并合并到 TiDB Cloud 的 `stock.products` 表，可以创建如下目录：

- `s3://dumpling-s3/stock/products/instance01/`
- `s3://dumpling-s3/stock/products/instance02/`

### 步骤 2. 使用 Dumpling 导出数据到 Amazon S3

关于如何安装 Dumpling，参见 [Dumpling 简介](https://docs.pingcap.com/tidb/stable/dumpling-overview)。

使用 Dumpling 导出数据到 Amazon S3 时，注意以下事项：

- 为上游集群开启 binlog。
- 选择正确的 Amazon S3 目录和区域。
- 通过配置 `-t` 选项选择合适的并发度，以最小化对上游集群的影响，或直接从备份库导出。关于该参数的更多用法，参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。
- 为 `--filetype csv` 和 `--no-schemas` 设置合适的值。关于这些参数的更多用法，参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。

CSV 文件命名方式如下：

- 如果一个表的数据被分割成多个 CSV 文件，需为这些 CSV 文件添加数字后缀。例如，`${db_name}.${table_name}.000001.csv` 和 `${db_name}.${table_name}.000002.csv`。数字后缀可以不连续，但必须递增。同时需要在数字前补零，保证所有后缀长度一致。

> **Note:**
>
> 如果在某些情况下你无法按照上述规则更新 CSV 文件名（例如，这些 CSV 文件链接也被你的其他程序使用），可以保持文件名不变，并在 [步骤 5](#step-5-perform-the-data-import-task) 的 **Mapping Settings** 中将源数据导入到单一目标表。

导出数据到 Amazon S3 的操作如下：

1. 获取 Amazon S3 bucket 的 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`。

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2. 将 MySQL instance1 的数据导出到 Amazon S3 bucket 的 `s3://dumpling-s3/store/sales/instance01/` 目录。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

    关于参数的详细说明，参见 [Dumpling 参数列表](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)。

3. 将 MySQL instance2 的数据导出到 Amazon S3 bucket 的 `s3://dumpling-s3/store/sales/instance02/` 目录。

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

详细步骤参见 [导出数据到 Amazon S3 云存储](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage)。

### 步骤 3. 在 TiDB Cloud 集群中创建 schema

在 TiDB Cloud 集群中创建 schema，操作如下：

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

在本示例中，上游表 `sale_01` 和 `sale_02` 的 id 列为自增主键。合并分片表到下游数据库时可能会发生冲突。执行以下 SQL，将 id 列设置为普通索引而非主键：

```sql
mysql> CREATE TABLE `sales` (
         `id` bigint(20) NOT NULL ,
         `uid` varchar(40) NOT NULL,
         `sale_num` bigint DEFAULT NULL,
         INDEX (`id`),
         UNIQUE KEY `ind_uid` (`uid`)
        );
Query OK, 0 rows affected (0.17 sec)
```

关于此类冲突的解决方案，参见 [移除列的 PRIMARY KEY 属性](https://docs.pingcap.com/tidb/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column)。

### 步骤 4. 配置 Amazon S3 访问权限

按照 [配置 Amazon S3 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access) 的说明获取访问源数据的 role ARN。

以下示例仅列出关键策略配置。请将 Amazon S3 路径替换为你自己的值。

```yaml
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Sid": "VisualEditor0",
           "Effect": "Allow",
           "Action": [
               "s3:GetObject",
               "s3:GetObjectVersion"
           ],
           "Resource": [
               "arn:aws:s3:::dumpling-s3/*"
           ]
       },
       {
           "Sid": "VisualEditor1",
           "Effect": "Allow",
           "Action": [
               "s3:ListBucket",
               "s3:GetBucketLocation"
           ],

           "Resource": "arn:aws:s3:::dumpling-s3"
       }
   ]
}
```

### 步骤 5. 执行数据导入任务

配置好 Amazon S3 访问权限后，你可以在 TiDB Cloud 控制台执行数据导入任务，操作如下：

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页，然后点击左侧导航栏的 **Data** > **Import**。

2. 选择 **Import data from Cloud Storage**，然后点击 **Amazon S3**。

3. 在 **Import Data from Amazon S3** 页面，填写以下信息：

    - **Import File Count**：对于 TiDB Cloud Starter 或 TiDB Cloud Essential，选择 **Multiple files**。该字段在 TiDB Cloud Dedicated 中不可用。
    - **Included Schema Files**：选择 **No**。
    - **Data Format**：选择 **CSV**。
    - **Folder URI**：填写源数据的 bucket URI。本例中可以使用对应表的二级目录 `s3://dumpling-s3/store/sales/`，这样 TiDB Cloud 可以一次性将所有 MySQL 实例的数据导入并合并到 `store.sales`。
    - **Bucket Access** > **AWS Role ARN**：输入你获取到的 Role-ARN。

    如果 bucket 的位置与集群不同，请确认跨区域合规性。

    TiDB Cloud 会开始验证是否能访问你指定的 bucket URI 中的数据。验证通过后，TiDB Cloud 会尝试使用默认文件命名模式扫描数据源中的所有文件，并在下一页左侧返回扫描摘要结果。如果遇到 `AccessDenied` 错误，参见 [排查 S3 数据导入时的 Access Denied 错误](/tidb-cloud/troubleshoot-import-access-denied-error.md)。

4. 点击 **Connect**。

5. 在 **Destination** 部分，选择目标数据库和表。

    导入多个文件时，可以通过 **Advanced Settings** > **Mapping Settings** 为每个目标表及其对应的 CSV 文件定义自定义映射规则。之后，数据源文件会根据你提供的自定义映射规则重新扫描。

    在 **Source File URIs and Names** 中输入源文件 URI 和名称时，确保格式为 `s3://[bucket_name]/[data_source_folder]/[file_name].csv`。例如，`s3://sampledata/ingest/TableName.01.csv`。

    你也可以使用通配符匹配源文件。例如：

    - `s3://[bucket_name]/[data_source_folder]/my-data?.csv`：该目录下所有以 `my-data` 开头，后跟一个字符的 CSV 文件（如 `my-data1.csv` 和 `my-data2.csv`）都将被导入到同一个目标表。

    - `s3://[bucket_name]/[data_source_folder]/my-data*.csv`：该目录下所有以 `my-data` 开头的 CSV 文件都将被导入到同一个目标表。

    注意仅支持 `?` 和 `*`。

    > **Note:**
    >
    > URI 必须包含数据源文件夹。

6. 如有需要，编辑 CSV 配置。

    你也可以点击 **Edit CSV configuration**，对 Backslash Escape、Separator 和 Delimiter 进行更细粒度的控制。

    > **Note:**
    >
    > 对于分隔符、定界符和 null 的配置，既可以使用字母数字字符，也可以使用部分特殊字符。支持的特殊字符包括 `\t`、`\b`、`\n`、`\r`、`\f` 和 `\u0001`。

7. 点击 **Start Import**。

8. 当导入进度显示 **Completed** 时，检查导入的表。

数据导入完成后，如果你想移除 TiDB Cloud 的 Amazon S3 访问权限，只需删除你添加的策略即可。

## 从 MySQL 到 TiDB Cloud 的增量数据同步

要基于 binlog 将上游集群指定位置的数据变更同步到 TiDB Cloud，可以使用 TiDB Data Migration (DM) 进行增量同步。

### 前置条件

如果你需要迁移增量数据并合并 MySQL 分片到 TiDB Cloud，需要手动部署 TiDB DM，因为 TiDB Cloud 目前尚不支持迁移和合并 MySQL 分片。详细步骤参见 [使用 TiUP 部署 DM 集群](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

### 步骤 1. 添加数据源

1. 新建数据源文件 `dm-source1.yaml`，将上游数据源配置到 DM 中。内容如下：

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-01"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "${host}"           # For example: 192.168.10.101
     user: "user01"
     password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
     port: ${port}             # For example: 3307
    ```

2. 新建另一个数据源文件 `dm-source2.yaml`，内容如下：

    ```yaml
    # MySQL Configuration.
    source-id: "mysql-replica-02"
    # Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
    # The prerequisite is that you have already enabled GTID in the upstream MySQL.
    # If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
    enable-gtid: true
    from:
     host: "192.168.10.102"
     user: "user02"
     password: "${password}"
     port: 3308
    ```

3. 在终端运行以下命令，使用 `tiup dmctl` 将第一个数据源配置加载到 DM 集群：

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
    ```

    上述命令参数说明如下：

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |要连接的集群中任意 DM-master 节点的 `{advertise-addr}`。例如：192.168.11.110:9261|
    |`operate-source create`|将数据源加载到 DM 集群。|

    示例输出如下：

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source1.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262"
           }
       ]
    }

    ```

4. 在终端运行以下命令，使用 `tiup dmctl` 将第二个数据源配置加载到 DM 集群：

    ```shell
    [root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml
    ```

    示例输出如下：

    ```shell
    tiup is checking updates for component dmctl ...

    Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source2.yaml

    {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262"
           }
       ]
    }
    ```

### 步骤 2. 创建同步任务

1. 新建同步任务配置文件 `test-task1.yaml`。

2. 在 Dumpling 导出的 MySQL instance1 的 metadata 文件中找到起始点。例如：

    ```toml
    Started dump at: 2022-05-25 10:16:26
    SHOW MASTER STATUS:
           Log: mysql-bin.000002
           Pos: 246546174
           GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
    Finished dump at: 2022-05-25 10:16:27
    ```

3. 在 Dumpling 导出的 MySQL instance2 的 metadata 文件中找到起始点。例如：

    ```toml
    Started dump at: 2022-05-25 10:20:32
    SHOW MASTER STATUS:
           Log: mysql-bin.000001
           Pos: 1312659
           GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
    Finished dump at: 2022-05-25 10:20:32
    ```

4. 编辑任务配置文件 `test-task1`，为每个数据源配置增量同步模式和同步起始点。

    ```yaml
    ## ********* Task Configuration *********
    name: test-task1
    shard-mode: "pessimistic"
    # Task mode. The "incremental" mode only performs incremental data migration.
    task-mode: incremental
    # timezone: "UTC"

    ## ******** Data Source Configuration **********
    ## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data migration error.
    ##  This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    syncers:           # The running configurations of the sync processing unit.
     global:           # Configuration name.
       safe-mode: false # # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database,
                        # # and changes UPDATE of the data source to DELETE and REPLACE for the target database.
                        # # This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly.
                        # # In the first minute of starting or resuming an incremental migration task, DM automatically enables the safe mode.
    mysql-instances:
    - source-id: "mysql-replica-01"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000002"
         binlog-pos: 246546174
         binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801"
    - source-id: "mysql-replica-02"
       block-allow-list:  "bw-rule-1"
       route-rules: ["store-route-rule", "sale-route-rule"]
       filter-rules: ["store-filter-rule", "sale-filter-rule"]
       syncer-config-name: "global"
       meta:
         binlog-name: "mysql-bin.000001"
         binlog-pos: 1312659
         binlog-gtid: "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036"

    ## ******** Configuration of the target TiDB cluster on TiDB Cloud **********
    target-database:       # The target TiDB cluster on TiDB Cloud
     host: "tidb.xxxxxxx.xxxxxxxxx.ap-northeast-1.prod.aws.tidbcloud.com"
     port: 4000
     user: "root"
     password: "${password}"  # If the password is not empty, it is recommended to use a dmctl-encrypted cipher.

    ## ******** Function Configuration **********
    routes:
     store-route-rule:
       schema-pattern: "store_*"
       target-schema: "store"
     sale-route-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       target-schema: "store"
       target-table:  "sales"
    filters:
     sale-filter-rule:
       schema-pattern: "store_*"
       table-pattern: "sale_*"
       events: ["truncate table", "drop table", "delete"]
       action: Ignore
     store-filter-rule:
       schema-pattern: "store_*"
       events: ["drop database"]
       action: Ignore
    block-allow-list:
     bw-rule-1:
       do-dbs: ["store_*"]

    ## ******** Ignore check items **********
    ignore-checking-items: ["table_schema","auto_increment_ID"]
    ```

关于任务配置的详细说明，参见 [DM 任务配置](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)。

为保证数据同步任务顺利运行，DM 会在任务启动时自动触发预检查并返回检查结果。只有预检查通过后，DM 才会启动同步。你也可以手动触发预检查，命令如下：

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml
```

示例输出如下：

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### 步骤 3. 启动同步任务

使用 `tiup dmctl` 运行以下命令启动数据同步任务：

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr}  start-task dm-task.yaml
```

上述命令参数说明如下：

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |要连接的集群中任意 DM-master 节点的 `{advertise-addr}`。例如：192.168.11.110:9261|
|`start-task`           |启动迁移任务。|

示例输出如下：

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl /root/.tiup/components/dmctl/${tidb_version}/dmctl/dmctl --master-addr 192.168.11.110:9261 start-task dm-task.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-192.168.11.111-9262"
       },

       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-192.168.11.112-9262"
       }
   ],
   "checkResult": ""
}
```

如果任务启动失败，请根据提示信息检查并修正配置，然后重新运行上述命令启动任务。

如遇问题，可参考 [DM 错误处理](https://docs.pingcap.com/tidb/stable/dm-error-handling) 和 [DM FAQ](https://docs.pingcap.com/tidb/stable/dm-faq)。

### 步骤 4. 查看同步任务状态

要了解 DM 集群是否有正在运行的同步任务及其状态，可使用 `tiup dmctl` 运行 `query-status` 命令：

```shell
[root@localhost ~]# tiup dmctl --master-addr 192.168.11.110:9261 query-status test-task1
```

示例输出如下：

```shell
{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-01",
               "worker": "dm-192.168.11.111-9262",
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
                       "totalEvents": "4048",
                       "totalTps": "3",
                       "recentTps": "3",
                       "masterBinlog": "(mysql-bin.000002, 246550002)",
                       "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
                       "syncerBinlog": "(mysql-bin.000002, 246550002)",
                       "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194813",
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
       },
       {
           "result": true,
           "msg": "",
           "sourceStatus": {
               "source": "mysql-replica-02",
               "worker": "dm-192.168.11.112-9262",
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
                       "totalEvents": "33",
                       "totalTps": "0",
                       "recentTps": "0",
                       "masterBinlog": "(mysql-bin.000001, 1316487)",
                       "masterBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
                       "syncerBinlog": "(mysql-bin.000001, 1316487)",
                       "syncerBinlogGtid": "cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4048",
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
       }
   ]
}
```

关于结果的详细解读，参见 [Query Status](https://docs.pingcap.com/tidb/stable/dm-query-status)。