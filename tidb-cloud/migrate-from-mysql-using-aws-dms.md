---
title: 使用 AWS DMS 将 MySQL 兼容数据库迁移到 TiDB Cloud
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 将数据从 MySQL 兼容数据库迁移到 TiDB Cloud。
---

# 使用 AWS DMS 将 MySQL 兼容数据库迁移到 TiDB Cloud

如果你想将异构数据库（如 PostgreSQL、Oracle 和 SQL Server）迁移到 TiDB Cloud，推荐使用 AWS Database Migration Service (AWS DMS)。

AWS DMS 是一项云服务，可以轻松迁移关系型数据库、数据仓库、NoSQL 数据库以及其他类型的数据存储。你可以使用 AWS DMS 将数据迁移到 TiDB Cloud。

本文档以 Amazon RDS 为例，介绍如何使用 AWS DMS 将数据迁移到 TiDB Cloud。该流程同样适用于将数据从自建 MySQL 数据库或 Amazon Aurora 迁移到 TiDB Cloud。

在本示例中，数据源为 Amazon RDS，数据目标为 TiDB Cloud 中的 TiDB Cloud Dedicated 集群。上下游数据库均位于同一区域。

## 前提条件

在开始迁移之前，请确保你已阅读以下内容：

- 如果源数据库为 Amazon RDS 或 Amazon Aurora，需要将 `binlog_format` 参数设置为 `ROW`。如果数据库使用的是默认参数组，则 `binlog_format` 参数默认为 `MIXED`，且无法修改。此时，你需要[创建一个新的参数组](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params)，例如 `newset`，并将其 `binlog_format` 设置为 `ROW`。然后，[将默认参数组修改为](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#USER_WorkingWithParamGroups.Modifying) `newset`。注意，修改参数组会重启数据库。
- 检查并确保源数据库使用的排序规则（collation）与 TiDB 兼容。TiDB 中 utf8mb4 字符集的默认排序规则为 `utf8mb4_bin`，但在 MySQL 8.0 中，默认排序规则为 `utf8mb4_0900_ai_ci`。如果上游 MySQL 使用默认排序规则，由于 TiDB 不兼容 `utf8mb4_0900_ai_ci`，AWS DMS 无法在 TiDB 中创建目标表，也无法迁移数据。为解决此问题，你需要在迁移前将源数据库的排序规则修改为 `utf8mb4_bin`。TiDB 支持的字符集和排序规则完整列表，参见 [Character Set and Collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation)。
- TiDB 默认包含以下系统数据库：`INFORMATION_SCHEMA`、`PERFORMANCE_SCHEMA`、`mysql`、`sys` 和 `test`。创建 AWS DMS 迁移任务时，需要过滤掉这些系统数据库，不能使用默认的 `%` 选择迁移对象。否则，AWS DMS 会尝试将这些系统数据库从源数据库迁移到目标 TiDB，导致任务失败。为避免此问题，建议填写具体的数据库和表名。
- 将 AWS DMS 的公网和私网 IP 地址添加到源数据库和目标数据库的 IP 访问列表中。否则，在某些场景下网络连接可能会失败。
- 使用 [VPC Peerings](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-on-aws) 或 [Private Endpoint connections](/tidb-cloud/set-up-private-endpoint-connections.md) 连接 AWS DMS 和 TiDB 集群。
- 建议 AWS DMS 和 TiDB 集群使用同一区域，以获得更好的数据写入性能。
- 建议使用 AWS DMS `dms.t3.large`（2 vCPU 和 8 GiB 内存）或更高规格的实例。小规格实例可能会导致内存溢出（OOM）错误。
- AWS DMS 会自动在目标数据库中创建 `awsdms_control` 数据库。

## 限制

- AWS DMS 不支持复制 `DROP TABLE`。
- AWS DMS 支持基础的架构迁移，包括创建表和主键。但 AWS DMS 不会自动在 TiDB Cloud 中创建二级索引、外键或用户账户。你需要在 TiDB 中手动创建这些对象，包括带有二级索引的表（如有需要）。更多信息，参见 [Migration planning for AWS Database Migration Service](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html#CHAP_SettingUp.MigrationPlanning)。

## 第 1 步：创建 AWS DMS 复制实例

1. 进入 AWS DMS 控制台的 [Replication instances](https://console.aws.amazon.com/dms/v2/home#replicationInstances) 页面，并切换到对应区域。建议 AWS DMS 与 TiDB Cloud 使用同一区域。本文档中，上下游数据库及 DMS 实例均在 **us-west-2** 区域。

2. 点击 **Create replication instance**。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3. 填写实例名称、ARN 和描述。

4. 配置实例参数：
    - **Instance class**：选择合适的实例规格。建议使用 `dms.t3.large` 或更高规格以获得更好性能。
    - **Engine version**：使用默认配置。
    - **Multi-AZ**：根据业务需求选择 **Single-AZ** 或 **Multi-AZ**。

5. 在 **Allocated storage (GiB)** 字段配置存储空间。使用默认配置即可。

6. 配置网络和安全性。
    - **Network type - new**：选择 **IPv4**。
    - **Virtual private cloud (VPC) for IPv4**：选择所需的 VPC。建议与上游数据库使用同一个 VPC，以简化网络配置。
    - **Replication subnet group**：为复制实例选择一个子网组。
    - **Public accessible**：使用默认配置。

7. 如有需要，配置 **Advanced settings**、**Maintenance** 和 **Tags**。点击 **Create replication instance** 完成实例创建。

## 第 2 步：创建源数据库端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home) 中，点击刚刚创建的复制实例。复制如下截图所示的公网和私网 IP 地址。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. 配置 Amazon RDS 的安全组规则。本示例中，将 AWS DMS 实例的公网和私网 IP 地址添加到安全组中。

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3. 点击 **Create endpoint** 创建源数据库端点。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4. 本示例中，点击 **Select RDS DB instance**，然后选择源 RDS 实例。如果源数据库为自建 MySQL，可以跳过此步骤，在后续步骤中填写相关信息。

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5. 配置以下信息：
   - **Endpoint identifier**：为源端点创建一个标签，便于后续任务配置时识别。
   - **Descriptive Amazon Resource Name (ARN) - optional**：为默认 DMS ARN 创建一个友好名称。
   - **Source engine**：选择 **MySQL**。
   - **Access to endpoint database**：选择 **Provide access information manually**。
   - **Server name**：填写数据服务器的名称。可从数据库控制台复制。如果上游为 Amazon RDS 或 Amazon Aurora，名称会自动填充。如果是无域名的自建 MySQL，可填写 IP 地址。
   - 填写源数据库的 **Port**、**Username** 和 **Password**。
   - **Secure Socket Layer (SSL) mode**：可根据需要启用 SSL 模式。

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6. **Endpoint settings**、**KMS key** 和 **Tags** 使用默认值。在 **Test endpoint connection (optional)** 部分，建议选择与源数据库相同的 VPC，以简化网络配置。选择对应的复制实例，然后点击 **Run test**。状态需为 **successful**。

7. 点击 **Create endpoint**。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## 第 3 步：创建目标数据库端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home) 中，点击刚刚创建的复制实例。复制如下截图所示的公网和私网 IP 地址。

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. 在 TiDB Cloud 控制台，进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，然后点击右上角的 **Connect** 获取 TiDB Cloud 数据库连接信息。

3. 在弹窗的 **Step 1: Create traffic filter** 下，点击 **Edit**，输入从 AWS DMS 控制台复制的公网和私网 IP 地址，然后点击 **Update Filter**。建议同时将 AWS DMS 复制实例的公网和私网 IP 地址添加到 TiDB 集群流量过滤器，否则在某些场景下 AWS DMS 可能无法连接 TiDB 集群。

4. 点击 **Download CA cert** 下载 CA 证书。在弹窗的 **Step 3: Connect with a SQL client** 下，记录连接字符串中的 `-u`、`-h` 和 `-P` 信息，后续会用到。

5. 点击弹窗中的 **VPC Peering** 标签页，在 **Step 1: Set up VPC** 下点击 **Add**，为 TiDB 集群和 AWS DMS 创建 VPC Peering 连接。

6. 配置相关信息，参见 [Set Up VPC Peering Connections](/tidb-cloud/set-up-vpc-peering-connections.md)。

7. 配置 TiDB 集群的目标端点。
    - **Endpoint type**：选择 **Target endpoint**。
    - **Endpoint identifier**：填写端点名称。
    - **Descriptive Amazon Resource Name (ARN) - optional**：为默认 DMS ARN 创建一个友好名称。
    - **Target engine**：选择 **MySQL**。

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home) 中，点击 **Create endpoint** 创建目标数据库端点，并配置以下信息：
    - **Server name**：填写 TiDB 集群的主机名，即你记录的 `-h` 信息。
    - **Port**：填写 TiDB 集群的端口，即你记录的 `-P` 信息。TiDB 集群默认端口为 4000。
    - **User name**：填写 TiDB 集群的用户名，即你记录的 `-u` 信息。
    - **Password**：填写 TiDB 集群的密码。
    - **Secure Socket Layer (SSL) mode**：选择 **Verify-ca**。
    - 点击 **Add new CA certificate**，导入前面从 TiDB Cloud 控制台下载的 CA 文件。

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9. 导入 CA 文件。

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. **Endpoint settings**、**KMS key** 和 **Tags** 使用默认值。在 **Test endpoint connection (optional)** 部分，选择与源数据库相同的 VPC。选择对应的复制实例，然后点击 **Run test**。状态需为 **successful**。

11. 点击 **Create endpoint**。

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## 第 4 步：创建数据库迁移任务

1. 在 AWS DMS 控制台，进入 [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) 页面。切换到你的区域，然后点击窗口右上角的 **Create task**。

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. 配置以下信息：
    - **Task identifier**：填写任务名称。建议使用易于记忆的名称。
    - **Descriptive Amazon Resource Name (ARN) - optional**：为默认 DMS ARN 创建一个友好名称。
    - **Replication instance**：选择刚刚创建的 AWS DMS 实例。
    - **Source database endpoint**：选择刚刚创建的源数据库端点。
    - **Target database endpoint**：选择刚刚创建的目标数据库端点。
    - **Migration type**：根据需要选择迁移类型。本示例选择 **Migrate existing data and replicate ongoing changes**。

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3. 配置以下信息：
    - **Editing mode**：选择 **Wizard**。
    - **Custom CDC stop mode for source transactions**：使用默认设置。
    - **Target table preparation mode**：选择 **Do nothing** 或其他选项。本示例选择 **Do nothing**。
    - **Stop task after full load completes**：使用默认设置。
    - **Include LOB columns in replication**：选择 **Limited LOB mode**。
    - **Maximum LOB size in (KB)**：使用默认值 **32**。
    - **Turn on validation**：根据需要选择。
    - **Task logs**：选择 **Turn on CloudWatch logs** 以便后续排查问题。相关配置使用默认设置。

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4. 在 **Table mappings** 部分，指定需要迁移的数据库。

    schema 名称即为 Amazon RDS 实例中的数据库名。**Source name** 的默认值为 "%"，表示将 Amazon RDS 中所有数据库迁移到 TiDB。这会导致 Amazon RDS 中的 `mysql`、`sys` 等系统数据库也被迁移到 TiDB 集群，进而导致任务失败。因此，建议填写具体的数据库名，或过滤掉所有系统数据库。例如，按照下图设置，仅会迁移名为 `franktest` 的数据库及其所有表。

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5. 点击右下角的 **Create task**。

6. 返回 [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) 页面，切换到你的区域，可以查看任务的状态和进度。

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

如果在迁移过程中遇到任何问题或失败，可以在 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 中查看日志信息以排查问题。

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 参见

- 如果你想了解更多关于如何将 AWS DMS 连接到 TiDB Cloud 集群的信息，参见 [Connect AWS DMS to TiDB Cloud clusters](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

- 如果你想将 MySQL 兼容数据库（如 Aurora MySQL 和 Amazon Relational Database Service (RDS)）迁移到 TiDB Cloud，推荐使用 [Data Migration on TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

- 如果你想使用 AWS DMS 将 Amazon RDS for Oracle 迁移到 TiDB Cloud，参见 [Migrate from Amazon RDS for Oracle to TiDB Cloud using AWS DMS](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)。