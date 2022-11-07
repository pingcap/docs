---
title: Migrate from On-Premise TiDB to TiDB Cloud
summary: Learn how to migrate data from on-premise TiDB to TiDB Cloud.
---

# Migrate from On-Premises TiDB to TiDB Cloud

This document describes how to migrate data from your on-premises (OP) TiDB clusters to TiDB Cloud (AWS) through Dumpling and TiCDC.

The overall procedure is as follows:

- Build the environment and prepare the tools
- Full data migration: OP TiDB (Dumpling) --> S3 --> (Import) TiDB Cloud
- Incremental data migration: OP TiDB --> (TiCDC) --> TiDB Cloud
- Data verification

## Prerequisites

It is recommended that you put the S3 bucket and TiDB Cloud in the same region. Cross-region migration might incur additional data conversion cost.

  1. Prepare an [AWS account](https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-up-s3.html#sign-up-for-aws-gsg) with administrator access
  2. Prepare an [AWS S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
  3. [Deploy an on-premises TiDB cluster](https://docs.pingcap.com/zh/tidb/dev/hardware-and-software-requirements)
  4. Prepare [a TiDB Cloud account with administrator access and create a TiDB Cloud (AWS) cluster](/tidb-cloud/tidb-cloud-quickstart.md)

## Prepare tools

### Dumpling

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) is a data export tool that exports data from TiDB/MySQL into SQL or CSV files. You can use Dumpling to export full data from TiDB Cloud.

Before you deploy Dumpling, note the following:

- It is recommended to deploy Dumpling on a new EC2 instance in the same VPC as the TiDB cluster.
- The EC2 instance should have at least 16 cores and 32 GB of memory to guarantee a good export performance.
- The recommended EC2 instance type is c6g.4xlarge. You can choose other EC2 instance types based on your needs. The AMI can be Amazon Linux, Ubuntu, or Red Hat.

You can deploy Dumpling by using TiUP or using the binary package.

#### Deploy Dumpling usig TiUP

Use [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview) to deploy Dumpling:

```bash
## Deploy tiup
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source /root/.bash_profile
## Deploy Dumpling and update to the latest version
tiup install dumpling
tiup update --self && tiup update dumpling
```

#### Deploy Dumpling using the installation package

To deploy Dumpling using the installation package

1. Download the [toolkit package](https://docs.pingcap.com/tidb/stable/download-ecosystem-tools) from the [Dumpling download page].
2. Extract it to the target machine and [install Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#dumpling-introduction).

#### Configure privileges for Dumpling

You need the following previleges to export data from the upstream database:

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT
- PROCESS

#### Deploy TiCDC

  3. 部署增量同步工具 TiCDC
参考文档 - TiCDC 安装部署
    1. 首先需要确认当前 TiDB 版本是否支持 TiCDC，集群版本如低于 4.0.0 rc.1 ，请先升级 TiDB  集群至 4.0.0 rc.1 或更新版本 参考文档 - 升级 TiDB 版本
    2. 【OP TiDB】使用 tiup 在原有 TiDB 集群上新增 TiCDC 组件 参考文档 - 扩容 TICDC 节点 
      1. 编辑扩容文件 scale-out.yaml
cdc_servers:
  - host: 10.0.1.3
    gc-ttl: 86400
    data_dir: /data/deploy/install/data/cdc-8300
  - host: 10.0.1.4
    gc-ttl: 86400
    data_dir: /data/deploy/install/data/cdc-8300

      2. 扩容 TiCDC 组件并检查状态
