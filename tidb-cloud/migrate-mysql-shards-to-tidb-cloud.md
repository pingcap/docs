---
title: Migrate and Merge MySQL Shards to TiDB Cloud
summary: Learn how to migrate and merge MySQL shards to TiDB Cloud.
---

# 分库分表合并迁移到 TiDB Cloud

本文档介绍了如何完成上游的 MySQL 存量数据迁移和增量数据同步，并要将分库分表数据合并至 TiDB Cloud 集群的单库单表中。

本文档中的示例使用了较为复杂的跨多个实例之间的分库分表迁移，同时涉及到自增主键冲突处理。本案例中的方案也适用于单实例内的分库分表迁移的场景。

## 环境信息

### 上游集群

上游集群的版本为 MySQL v5.7.18。具体信息如下：

1. MySQL 实例 1:
库 store_01，表 [sale_01, sale_02]
库 store_02，表 [sale_01, sale_02]
2. MySQL 实例 2：
库 store_01，表 [sale_01, sale_02]
库 store_02，表 [sale_01, sale_02]
3. 表结构：
CREATE TABLE sale_01 (
 id bigint(20) NOT NULL auto_increment,
 uid varchar(40) NOT NULL,
 sale_num bigint DEFAULT NULL,
 PRIMARY KEY (id),
 UNIQUE KEY ind_uid (uid)
);

### DM 

DM 的版本为 v5.3.0。具体信息如下：

![storage-architecture](/media/xxx.png)

## 存量数据迁移

## 从多个 MySQL 源导出存量数据

**特别注意**：

* **只导出表数据**，必须导出为 **CSV** 格式，DBaaS 平台合库合表的限制
* 在 AWS S3 Bucket 内创建**一级子目录** `store`（对应库级别），**二级子目录** `sales`（对应表级别），在目录 `sales` 中为每个 MySQL 实例创建一个**三级子目录**（对应实例级别），即：
    * 将 MySQL 实例 1 数据导出至 `s3://dumpling-s3/store/sales/instance01/`
    * 将 MySQL 实例 2 数据导出至 `s3://dumpling-s3/store/sales/instance02/`
* 若存在多实例上的多种分库分表规则，则建议在 s3 bucket 中为分库建一个一级子目录，为分表创建一个二级子目录，在二级子目录下按照实例数创建多个三级子目录，方便管理和一次性导入数据。示例：
    * 将 MySQL 实例 1 和实例 2 中的多个库表 `stock_N.product_N` 合表至 TiDB Cloud 中的表 `stock.products`，则创建 `s3://dumpling-s3/stock/products/instance01/`和 `s3://dumpling-s3/stock/products/instance02/`

**设置 AWS S3 Bucket  目录层级**

<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image2.png "image_tooltip")

**使用 Dumpling  导数至 AWS S3**

**说明**： 

* 详细操作方法如下：
    * 通过 AWS S3 方式参考：[Dumpling 导数至 AWS S3 操作步骤](https://pingcap.feishu.cn/docs/doccnunXi04QOo0A8rbOn06vXXd)
    * 通过 GCS 方式参考：[ Dumling 导数至 Google Cloud Storage 操作步骤](https://pingcap.feishu.cn/docs/doccntzVHCWTM8tv0iilQSgd2yg#)
* 常见 Dumpling 导出问题，参考：[各 RDS For MySQL 常见 Dumpling 导出问题](https://pingcap.feishu.cn/docs/doccnvJ6S5TJ6A8va3oW2X9jVcb#)

# 上游集群需要开启 binlog

# 注意选择正确的 S3 目录和 region 区域

# 选择合适的 dumpling 并发度 -t，尽量减少对上游集群的影响，或者直接从备库导出

# 注意设置选项 --filetype csv 和 --no-schemas 

[root@localhost ~]# export AWS_ACCESS_KEY_ID={your_aws_access_key_id}

[root@localhost ~]# export AWS_SECRET_ACCESS_KEY= {your_aws_secret_access_key}

# 导出 MySQL 实例 1 数据

[root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql01-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance01/" --s3.region "ap-northeast-1" 

# 导出 MySQL 实例 2 数据

[root@localhost ~]# tiup dumpling -u {username} -p {password} -P {port} -h {mysql02-ip} -B store_01,store_02 -r 20000 --filetype csv --no-schemas -o "s3://dumpling-s3/store/sales/instance02/" --s3.region "ap-northeast-1"  

<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image3.png "image_tooltip")

<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image4.png "image_tooltip")

**将 AWS S3 (GCS) 数据导入至 TiDB Cloud **

**预先在 TiDB Cloud  创建 Schema**

说明：示例中表 `sale_01` 和 `sale_02` 的列 id 为主键（假设业务不依赖于该列），且具有自增属性，在同步下游进行合表时会发生主键冲突，参考[去掉自增主键属性进行处理](https://docs.pingcap.com/zh/tidb-data-migration/v5.3/shard-merge-best-practices#%E5%8E%BB%E6%8E%89%E8%87%AA%E5%A2%9E%E4%B8%BB%E9%94%AE%E7%9A%84%E4%B8%BB%E9%94%AE%E5%B1%9E%E6%80%A7)

mysql> CREATE DATABASE store;

Query OK, 0 rows affected (0.16 sec)

mysql> use store;

Database changed

# 去掉 id 自增属性，并设置为普通索引

mysql> CREATE TABLE `sales` (

   ->   `id` bigint(20) NOT NULL ,

   ->   `uid` varchar(40) NOT NULL,

   ->   `sale_num` bigint DEFAULT NULL,

   ->   INDEX (`id`),

   ->   UNIQUE KEY `ind_uid` (`uid`)

   -> );

Query OK, 0 rows affected (0.17 sec)

**设置导入权限**

**说明**：

* 操作方法如下：
    * 若通过 AWS S3 导入，可参考[ AWS S3 导入 TiDB Cloud 集群操作手册](https://pingcap.feishu.cn/docs/doccnaE2au5qdHUh6ayjNozZ86c)
    * 若通过 GCS 导入，可参考[ GCS 导入 TiDB Cloud 集群操作手册](https://pingcap.feishu.cn/docs/doccn4Mewev7pgQa0pyfKRgQu5b)
* 本文档以 AWS S3 方式为示例做说明，这里仅列出最关键的 AWS S3 策略配置（请根据实际情况替换 S3 路径）：

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

**执行数据导入**

**确认 IAM Role 配置无误后，在 TiDB Cloud 集群页面执行数据导入**

填写内容：

* Bucket URL： Dumpling 数据导出的位置
* Data Format：选择 TiDB Dumpling
* Role-ARN：填写创建好的 IAM Role，请确认已经具备正确的访问权限
* Target Database Username：建议使用 root
* Object Name Pattern：填写文件匹配规则，例如 *store*.sale*
* Target Table Name：填写目标 schema 名称，所有匹配的文件都将导入该表。例如 store.sales

执行导入即可

<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image5.png "image_tooltip")

注意：

* Bucket URL 建议写到表级别对应的二级目录（这里为 `s3://dumpling-s3/store/sales`），这样合表 `store.sales` 所需要的全部 MySQL 实例数据都被包含在内，并可以一次性导入

<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image6.png "image_tooltip")

注意：Object Name Pattern 格式为： *{schema 前缀}*.{table 前缀}*，例如 *store*.sale*

<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image7.png "image_tooltip")

**增量数据同步**

TiDB Cloud 尚未提供增量数据同步功能，需要手动搭建 DM 进行。安装步骤请参考[ Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)。

**创建数据源**

[root@localhost ~]# cat dm-source1.yaml

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

# MySQL Configuration.

source-id: "mysql-replica-02"

# DM-worker 是否使用全局事务标识符 (GTID) 拉取 binlog。使用前提是在上游 MySQL 已开启 GTID 模式。

enable-gtid: true

from:

 host: "172.16.5.138"

 user: "lzy"

 password: "3O8fCPEnwO87cIal32bpO0AuTsJyBJ0="

 port: 3308
 
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

[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 operate-source create dm-source2.yaml

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

**配置同步任务**

增量同步任务需要显式指定起始位置，可以从 Dumpling 导出文件的 metadata 文件中找到。

# 获取 MySQL 实例 1 Dumpling 导出文件 metadata 内容，用于配置增量同步起始点

Started dump at: 2022-05-25 10:16:26

SHOW MASTER STATUS:

       Log: mysql-bin.000002

       Pos: 246546174

       GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-194801

Finished dump at: 2022-05-25 10:16:27

# 获取 MySQL 实例 2 Dumpling 导出文件 metadata 内容，用于配置增量同步起始点

Started dump at: 2022-05-25 10:20:32

SHOW MASTER STATUS:

       Log: mysql-bin.000001

       Pos: 1312659

       GTID:cd21245e-bb10-11ec-ae16-fec83cf2b903:1-4036

Finished dump at: 2022-05-25 10:20:32

根据 metadata 文件中的位点信息，创建增量同步任务

[root@localhost ~]# cat dm-task.yaml

---

## ********* 任务信息配置 *********

name: test-task1

shard-mode: "pessimistic"

# 任务模式，可设为 "full" - "只进行全量数据迁移"、"incremental" - "Binlog 实时同步"、"all" - "全量 + Binlog 迁移"

task-mode: incremental

# timezone: "UTC"

## ******** 数据源配置 **********

## 【可选配置】如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错

##  该场景多见于，全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据

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

**检查同步任务配置**

[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 check-task dm-task.yaml

tiup is checking updates for component dmctl ...

Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 172.16.7.140:9261 check-task dm-task.yaml

{

   "result": true,

   "msg": "check pass!!!"

}

**启动任务**

[root@localhost ~]# tiup dmctl --master-addr 172.16.7.140:9261 start-task dm-task.yaml

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

---
