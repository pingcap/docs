---
title:  使用 AWS DMS 将 Amazon RDS for Oracle 迁移到 TiDB Cloud
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 将数据从 Amazon RDS for Oracle 迁移到 TiDB Cloud Serverless。
---

# 使用 AWS DMS 将 Amazon RDS for Oracle 迁移到 TiDB Cloud

本文档描述了如何使用 AWS Database Migration Service (AWS DMS) 将数据从 Amazon RDS for Oracle 迁移到 [TiDB Cloud Serverless](https://tidbcloud.com/clusters/create-cluster) 的分步示例。

如果你想了解更多关于 TiDB Cloud 和 AWS DMS 的信息，请参阅以下内容：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
- [TiDB Developer Guide](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
- [AWS DMS Documentation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## 为什么使用 AWS DMS？

AWS DMS 是一项云服务，可以实现关系型数据库、数据仓库、NoSQL 数据库以及其他类型数据存储的迁移。

如果你希望将数据从异构数据库（如 PostgreSQL、Oracle 和 SQL Server）迁移到 TiDB Cloud，推荐使用 AWS DMS。

## 部署架构

总体上，按照以下步骤操作：

1. 搭建源端 Amazon RDS for Oracle。
2. 搭建目标端 [TiDB Cloud Serverless](https://tidbcloud.com/project/clusters/create-cluster)。
3. 使用 AWS DMS 设置数据迁移（全量加载）。

下图展示了高层次的架构。

![Architecture](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## 前置条件

在开始之前，请阅读以下前置条件：

- [AWS DMS 前置条件](/tidb-cloud/migrate-from-mysql-using-aws-dms.md#prerequisites)
- [AWS 云账号](https://aws.amazon.com)
- [TiDB Cloud 账号](https://tidbcloud.com)
- [DBeaver](https://dbeaver.io/)

接下来，你将学习如何使用 AWS DMS 将数据从 Amazon RDS for Oracle 迁移到 TiDB Cloud。

## 步骤 1. 创建 VPC

登录 [AWS 控制台](https://console.aws.amazon.com/vpc/home#vpcs:) 并创建一个 AWS VPC。你需要在该 VPC 中后续创建 Oracle RDS 和 DMS 实例。

关于如何创建 VPC 的详细说明，请参阅 [创建 VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC)。

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## 步骤 2. 创建 Oracle 数据库实例

在你刚刚创建的 VPC 中创建一个 Oracle 数据库实例，并记住密码，同时授予其公网访问权限。你必须启用公网访问以使用 AWS Schema Conversion Tool。注意，在生产环境中不推荐授予公网访问权限。

关于如何创建 Oracle 数据库实例的详细说明，请参阅 [创建 Oracle 数据库实例并连接数据库](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html)。

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## 步骤 3. 在 Oracle 中准备表数据

使用以下脚本在 github_events 表中创建并填充 10000 行数据。你可以使用 github event 数据集，并从 [GH Archive](https://gharchive.org/) 下载。该数据集包含 10000 行数据。使用以下 SQL 脚本在 Oracle 中执行。

- [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
- [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

执行完 SQL 脚本后，在 Oracle 中检查数据。以下示例使用 [DBeaver](https://dbeaver.io/) 查询数据：

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## 步骤 4. 创建 TiDB Cloud Serverless 集群

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)。

2. [创建 TiDB Cloud Serverless 集群](/tidb-cloud/tidb-cloud-quickstart.md)。

3. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。

4. 在右上角点击 **Connect**。

5. 点击 **Generate Password** 生成密码，并复制生成的密码。

## 步骤 5. 创建 AWS DMS 复制实例

1. 进入 AWS DMS 控制台的 [Replication instances](https://console.aws.amazon.com/dms/v2/home#replicationInstances) 页面，并切换到对应区域。

2. 在 VPC 中创建一个 `dms.t3.large` 的 AWS DMS 复制实例。

    ![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

> **Note:**
>
> 关于创建可用于 TiDB Cloud Serverless 的 AWS DMS 复制实例的详细步骤，请参阅 [连接 AWS DMS 到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

## 步骤 6. 创建 DMS 端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home) 左侧点击 `Endpoints` 菜单项。

2. 创建 Oracle 源端点和 TiDB 目标端点。

    下图展示了源端点的配置。

    ![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

    下图展示了目标端点的配置。

    ![Create AWS DMS Target endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

> **Note:**
>
> 关于创建 TiDB Cloud Serverless DMS 端点的详细步骤，请参阅 [连接 AWS DMS 到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

## 步骤 7. 迁移表结构

在本示例中，AWS DMS 会自动处理表结构，因为表结构定义较为简单。

如果你决定使用 AWS Schema Conversion Tool 迁移表结构，请参阅 [安装 AWS SCT](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure)。

更多信息请参阅 [使用 AWS SCT 将源表结构迁移到目标数据库](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html)。

## 步骤 8. 创建数据库迁移任务

1. 在 AWS DMS 控制台，进入 [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) 页面。切换到你的区域，然后点击窗口右上角的 **Create task**。

    ![Create task](/media/tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. 创建数据库迁移任务，并指定 **Selection rules**：

    ![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3. 创建任务，启动任务，然后等待任务完成。

4. 点击 **Table statistics** 检查表。表结构名称为 `ADMIN`。

    ![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## 步骤 9. 检查下游 TiDB 集群中的数据

连接到 [TiDB Cloud Serverless 集群](https://tidbcloud.com/clusters/create-cluster)，检查 `admin.github_event` 表中的数据。如下面截图所示，DMS 已成功迁移表 `github_events` 及 10000 行数据。

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## 总结

通过 AWS DMS，你可以按照本文档的示例成功将数据从任意上游 AWS RDS 数据库迁移。

如果在迁移过程中遇到任何问题或失败，可以在 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 中查看日志信息以排查问题。

![Troubleshooting](/media/tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 参见

- [使用 AWS DMS 从 MySQL 兼容数据库迁移](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
- [连接 AWS DMS 到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)
