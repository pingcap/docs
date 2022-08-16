---
title: Migrate and Merge MySQL Shards to TiDB Cloud
summary: Learn how to migrate and merge MySQL shards to TiDB Cloud.
---

# Migrate and Merge MySQL Shards to TiDB Cloud

This document describes how to migrate and merge MySQL shards from different partitions into TiDB Cloud. After migration, you can use TiDB DM to perform incremental replication according to your business needs.

The example in this document uses a complex shard migration task across multiple MySQL instances, and involves handling conflicts in self-incremental primary keys. The scenario in this example is also applicable to the scenario of merging data from different sharded tables within a single instance.

## Environment information in the example

This section describes the basic information of the upstream cluster, DM, and downstream cluster used in the example.

### Upstream cluster

The version of the upstream cluster is MySQL v5.7.18. The specific information is as follows.

- MySQL instance1:
  - schema `store_01` and table `[sale_01, sale_02]`
  - schema `store_02` and table `[sale_01, sale_02]`
- MySQL instance2:
  - schema `store_01`and table `[sale_01, sale_02]`
  - schema `store_02`and table `[sale_01, sale_02]`
- Table structure：
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

The version of DM is v5.3.0. The details are as follows:

![DM Details](/media/tidb-cloud/shard-dm-details.png)

### Downstream cluster

采用的 TiDB Cloud 上集群的版本为 v6.0.0，合库合表至表 store.sales。
The version of TiDB Cloud cluster is v6.0.0, and the combined library and tables are merged to the table `store.sales`.

## Perform full data migration from MySQL to TiDB Cloud

The following is the procedure to migrate and merge MySQL shards to TiDB Cloud.

Note that in this example, you only need to export tables and they must be in the **CSV** format.

### Step 1. Create directories in the Amazon S3 bucket

Create a first level directory `store` (corresponding to the level of schemas)and a second level directory `sales` (corresponding to the level of tables) in the Amazon S3 bucket. In `sales`, create a third level directory for each MySQL instance (corresponding to the level of instances). For example:

- Migrate the data in MySQL instance1 to `s3://dumpling-s3/store/sales/instance01/`
- Migrate the data in MySQL instance2 to `s3://dumpling-s3/store/sales/instance02/`

If there are shards across multiple instances, you can create a first level directory for each schema and create a second level directory for each sharded table. Then create a third level directory for each MySQL instance for easy management. For example, if you want to migrate and merge tables `stock_N.product_N` from MySQL instance1 and MySQL instance2 into the table `stock.products` in TiDB Cloud, you can create the following directories:

- `s3://dumpling-s3/stock/products/instance01/`
- `s3://dumpling-s3/stock/products/instance02/`

### Step 2. Use Dumpling to export data to Amazon S3

When you use Dumpling to export data to Amazon S3, note the following:

- Enable binlog for upstream clusters.
- Choose the correct Amazon S3 directory and Region zone.
- Choose the appropriate concurrency by configuring `-t` to minimize the impact on the upstream cluster, or export directly from the backup database.
- Set appropriate values for `--filetype csv` and `--no-schemas`.

To export data to Amazon S3, do the following:

1. Get the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` on the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}
    [root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}
    ```

2. Export data from MySQL instance1 to the `s3://dumpling-s3/store/sales/instance01/` directory in the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1"
    ```

3. Export data from MySQL instance2 to the `s3://dumpling-s3/store/sales/instance02/` directory in the Amazon S3 bucket.

    ```shell
    [root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"
    ```

<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image3.png "image_tooltip")

<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image4.png "image_tooltip")

For detailed steps, see [Export data to Amazon S3 cloud storage](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage).

### Step 3. Create a schema in TiDB Cloud cluster

Create a schema in the TiDB Cloud cluster as follows:

```sql
mysql> CREATE DATABASE store;
Query OK, 0 rows affected (0.16 sec)
mysql> use store;
Database changed
```

In this example, the column IDs of  `sale_01` and `sale_02` are auto-increment primary keys.  conflicts might occur when you merge sharded tables in the downstream database. For solutoins to solve conflicts, see [Remove the PRIMARY KEY attribute from the column](https://docs.pingcap.com/tidb-data-migration/v5.3/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column).

Execute the following SQL statement to modify the PRIMARY KEY attribute of the ID column to normal index.

```sql
mysql> CREATE TABLE `sales` (
   ->   `id` bigint(20) NOT NULL ,
   ->   `uid` varchar(40) NOT NULL,
   ->   `sale_num` bigint DEFAULT NULL,
   ->   INDEX (`id`),
   ->   UNIQUE KEY `ind_uid` (`uid`)
   -> );
Query OK, 0 rows affected (0.17 sec)
```

### Step 4. Configure Amazon S3 access

To configure Amazon S3 access, follow the instructions in [Configure Amazon S3 access](/tidbcloud/config-s3-and-gcs-access#configure-amazon-s3-access).

This document uses the Amazon S3 as an example. The following example only lists key policy configurations. Replace the Amazon S3 path with your own values.

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

### Step 5. Perform the data import task

After configuring the IAM Role, you can perform the data import task on the [TiDB Cloud console](https://tidbcloud.com/console/clusters). You need to fill in the following information:

- Data Source Type: AWS S3.
- Bucket URL: fill in the bucket URL of your source data. you can use the second level directory corresponding to tables, `s3://dumpling-s3/store/sales` in this example. The data in all MySQL instances that is to be merged into `store.sales` can be imported in one go.
- Data Format: choose the format of your data.
- Target Cluster: fill in the Username and Password fields.
- DB/Tables Filter: if necessary, you can specify a table filter. If you want to configure multiple filter rules, use , to separate the rules.

## 增量数据同步

TiDB Cloud 尚未提供增量数据同步功能，需要手动搭建 DM 进行。安装步骤请参考[ Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

### 创建数据源

```shell
[root@localhost ~]# cat dm-source1.yaml
```

```yaml
# MySQL Configuration.
source-id: "mysql-replica-01"
# DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是在上游 MySQL 已开启 GTID 模式。
enable-gtid: true
from:
 host: "172.16.5.138"
 user: "lzy"
 password: "mZMkdjbRztSag6qEgoh8UkDY6X13H48="
 port: 3307
[root@localhost ~]# cat dm-source2.yaml
```

```yaml
# MySQL Configuration.
source-id: "mysql-replica-02"
# DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是在上游 MySQL 已开启 GTID 模式。
enable-gtid: true
from:
 host: "172.16.5.138"
 user: "lzy"
 password: "3O8fCPEnwO87cIal32bpO0AuTsJyBJ0="
 port: 3308 
```

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source1.yaml
```

```shell
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

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source2.yaml
```

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source2.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-172.16.7.214-9262"
       }
   ]
}

### 配置同步任务

增量同步任务需要显式指定起始位置，可以从 Dumpling 导出文件的 metadata 文件中找到。

获取 MySQL 实例 1 Dumpling 导出文件 metadata 内容，用于配置增量同步起始点

```shell
Started dump at: 2022-05-25 10:16:26
SHOW MASTER STATUS:
       Log: mysql-bin.000002
       Pos: 246546174
       GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801
Finished dump at: 2022-05-25 10:16:27
```

获取 MySQL 实例 2 Dumpling 导出文件 metadata 内容，用于配置增量同步起始点

```shell
Started dump at: 2022-05-25 10:20:32
SHOW MASTER STATUS:
       Log: mysql-bin.000001
       Pos: 1312659
       GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036
Finished dump at: 2022-05-25 10:20:32
```

根据 metadata 文件中的位点信息，创建增量同步任务

```shell
[root@localhost ~]# cat dm-task.yaml
```

```yaml
## ********* 任务信息配置 *********
name: test-task1
shard-mode: "pessimistic"
# 任务模式，可设为 "full" - "只进行全量数据迁移"、"incremental" - "Binlog 实时同步"、"all" - "全量 + Binlog 迁移"
task-mode: incremental
# timezone: "UTC"

## ******** 数据源配置 **********
## 【可选配置】如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错
## 该场景多见于，全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据
syncers:            # sync 处理单元的运行配置参数
 global:           # 配置名称
   safe-mode: true # 设置为 true，则将来自数据源的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE`；在增量同步稳定后可以关闭 safe-mode
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

## ******** 目标 TiDB 配置 **********
target-database:       # 目标 TiDB Cloud 配置
 host: "tidb.70593805.b973b556.ap-northeast-1.prod.aws.tidbcloud.com"
 port: 4000
 user: "root"
 password: "oSWRLvR3F5GDIgm+l+9h3kB72VFWBUwzOw=="         # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

## ******** 功能配置 **********
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

##  ******** 忽略检查项 **********
ignore-checking-items: ["table_schema","auto_increment_ID"]
```

### 检查同步任务配置

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 check-task dm-task.yaml
```

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 check-task dm-task.yaml

{
   "result": true,
   "msg": "check pass!!!"
}
```

### 启动任务

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 start-task dm-task.yaml
```

```shell
tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 start-task dm-task.yaml

{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-172.16.7.154-9262"
       },

       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-02",
           "worker": "dm-172.16.7.214-9262"
       }
   ],
   "checkResult": ""
}
```

```shell
[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 query-status test-task1
```

```shell
{
   "result": true,
   "msg": "",
   "sources": [
       {
           "result": true,
           "msg": "",
           "source": "mysql-replica-01",
           "worker": "dm-
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
               "worker": "dm-172.16.7.214-9262",
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
