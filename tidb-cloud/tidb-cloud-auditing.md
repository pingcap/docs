---
title: TiDB Cloud Dedicated Database Audit Logging
summary: 了解如何在 TiDB Cloud 中进行集群审计日志记录。
---

# TiDB Cloud Dedicated Database Audit Logging

TiDB Cloud 为你提供了数据库审计日志功能，用于记录用户访问详情的历史（例如执行的任何 SQL 语句）到日志中。

> **Note:**
>
> 目前，数据库审计日志功能仅在请求后提供。若要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。接着，在 **Description** 字段中填写“Apply for database audit logging”并点击 **Submit**。

为了评估你组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能默认是关闭的。要对集群进行审计，你需要先启用审计日志，然后指定审计过滤规则。

> **Note:**
>
> 由于审计日志会消耗集群资源，因此在是否审计集群时应谨慎。

## 前提条件

- 你使用的是 TiDB Cloud Dedicated 集群。TiDB Cloud Serverless 集群不支持审计日志。
- 你在你的组织中拥有 **Organization Owner** 或 **Project Owner** 角色。否则，你在 TiDB Cloud 控制台中看不到与数据库审计相关的选项。更多信息请参见 [User roles](/tidb-cloud/manage-user-access.md#user-roles)。

## 启用审计日志

TiDB Cloud 支持将 TiDB Cloud Dedicated 集群的审计日志记录到你的云存储服务。在启用数据库审计日志之前，请在集群所在的云提供商上配置你的云存储服务。

> **Note:**
>
> 对于部署在 AWS 上的 TiDB 集群，你可以选择在启用数据库审计日志时将审计日志文件存储在 TiDB Cloud 中。此功能目前仅在请求后提供。若要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。接着，在 **Description** 字段中填写“Apply to store audit log files in TiDB Cloud”并点击 **Submit**。

### 为 AWS 启用审计日志

要为 AWS 启用审计日志，请按照以下步骤操作：

#### Step 1. 创建 Amazon S3 存储桶

在你的企业拥有的 AWS 账户中指定一个 Amazon S3 存储桶，作为 TiDB Cloud 写入审计日志的目标。

> 注意：
>
> 不要在 S3 存储桶上启用对象锁定。启用对象锁定会阻止 TiDB Cloud 将审计日志文件推送到 S3。

更多信息请参见 [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)（AWS 用户指南）。

#### Step 2. 配置 Amazon S3 访问权限

1. 获取你想启用审计日志的 TiDB 集群的 TiDB Cloud 账户 ID 和 External ID。

    1. 在 TiDB Cloud 控制台，导航到你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **AWS IAM Policy Settings** 部分，记录 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID** 以备后续使用。

2. 在 AWS 管理控制台中，进入 **IAM** > **Access Management** > **Policies**，检查是否存在具有 `s3:PutObject` 写入权限的存储桶策略。

    - 如果存在，记录匹配的存储桶策略以备后用。
    - 如果不存在，进入 **IAM** > **Access Management** > **Policies** > **Create Policy**，根据以下策略模板定义存储桶策略。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "<Your S3 bucket ARN>/*"
                }
            ]
        }
        ```

        其中 `<Your S3 bucket ARN>` 是你要写入审计日志文件的 S3 存储桶的 Amazon 资源名称（ARN）。你可以在存储桶的 **Properties** 标签页的 **Bucket Overview** 区域获取 ARN 值。在 `"Resource"` 字段中，需在 ARN 后添加 `/*`。例如，如果 ARN 是 `arn:aws:s3:::tidb-cloud-test`，则配置为 `"arn:aws:s3:::tidb-cloud-test/*"`。

3. 进入 **IAM** > **Access Management** > **Roles**，检查是否已存在信任实体对应之前记录的 TiDB Cloud 账户 ID 和 External ID 的角色。

    - 如果存在，记录该角色以备后用。
    - 如果不存在，点击 **Create role**，选择 **Another AWS account** 作为信任实体类型，然后在 **Account ID** 字段中输入 TiDB Cloud 账户 ID。勾选 **Require External ID**，并在 **External ID** 字段中填写之前记录的 External ID。

4. 在 **IAM** > **Access Management** > **Roles** 中，点击上一步中创建或选择的角色，进入 **Summary** 页面，执行以下操作：

    1. 在 **Permissions** 标签页，确认是否已附加具有 `s3:PutObject` 写入权限的策略。如果没有，选择 **Attach Policies**，搜索所需策略，然后点击 **Attach Policy**。
    2. 返回 **Summary** 页面，复制 **Role ARN** 的值备用。

#### Step 3. 启用审计日志

在 TiDB Cloud 控制台中，返回到之前获取 TiDB Cloud 账户 ID 和 External ID 的 **Enable Database Audit Logging** 对话框，执行以下步骤：

1. 在 **Bucket URI** 字段中，输入你的 S3 存储桶的 URI。
2. 在 **Bucket Region** 下拉列表中，选择存储桶所在的 AWS 区域。
3. 在 **Role ARN** 字段中，填写在 [Step 2. 配置 Amazon S3 访问](#step-2-configure-amazon-s3-access) 中复制的 Role ARN。
4. 点击 **Test Connection**，验证 TiDB Cloud 是否能访问并写入存储桶。

    如果成功，会显示 **The connection is successfully**。否则，请检查你的访问配置。

5. 点击 **Enable**，启用该集群的审计日志。

    TiDB Cloud 现已准备好将指定集群的审计日志写入你的 Amazon S3 存储桶。

> **Note:**
>
> - 启用审计日志后，如果你对存储桶 URI、位置或 ARN 进行了任何新更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否能连接到存储桶。然后，点击 **Enable** 以应用更改。
> - 若要撤销 TiDB Cloud 对你的 Amazon S3 的访问权限，只需在 AWS 管理控制台中删除授予此集群的信任策略。

### 为 Google Cloud 启用审计日志

要为 Google Cloud 启用审计日志，请按照以下步骤操作：

#### Step 1. 创建 GCS 存储桶

在你的企业拥有的 Google Cloud 账户中指定一个 Google Cloud Storage (GCS) 存储桶，作为 TiDB Cloud 写入审计日志的目标。

更多信息请参见 [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets)（Google Cloud Storage 文档）。

#### Step 2. 配置 GCS 访问权限

1. 获取你想启用审计日志的 TiDB 集群的 Google Cloud Service Account ID。

    1. 在 TiDB Cloud 控制台，导航到你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **Google Cloud Server Account ID** 部分，记录 **Service Account ID** 以备后用。

2. 在 Google Cloud 控制台中，进入 **IAM & Admin** > **Roles**，检查是否存在具有以下写入权限的角色：

    - storage.objects.create
    - storage.objects.delete

    如果存在，记录匹配的角色以备后用。如果不存在，进入 **IAM & Admin** > **Roles** > **CREATE ROLE**，为 TiDB 集群定义一个角色。

3. 进入 **Cloud Storage** > **Browser**，选择你希望 TiDB Cloud 访问的 GCS 存储桶，然后点击 **SHOW INFO PANEL**。

    信息面板会显示。

4. 在信息面板中，点击 **ADD PRINCIPAL**。

    将显示添加主体的对话框。

5. 在对话框中，执行以下操作：

    1. 在 **New Principals** 字段中，粘贴 TiDB 集群的 Google Cloud Service Account ID。
    2. 在 **Role** 下拉列表中，选择目标 TiDB 集群的角色。
    3. 点击 **SAVE**。

#### Step 3. 启用审计日志

在 TiDB Cloud 控制台中，返回到之前获取 TiDB Cloud 账户 ID 的 **Enable Database Audit Logging** 对话框，执行以下步骤：

1. 在 **Bucket URI** 字段中，输入你的完整 GCS 存储桶名称。
2. 在 **Bucket Region** 字段中，选择存储桶所在的 GCS 区域。
3. 点击 **Test Connection**，验证 TiDB Cloud 是否能访问并写入存储桶。

    如果成功，会显示 **The connection is successfully**。否则，请检查你的访问配置。

4. 点击 **Enable**，启用该集群的审计日志。

    TiDB Cloud 现已准备好将审计日志写入你的 GCS 存储桶。

> **Note:**
>
> - 启用审计日志后，如果你对存储桶 URI 或位置进行了任何新更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否能连接到存储桶。然后，点击 **Enable** 以应用更改。
> - 若要撤销 TiDB Cloud 对你的 GCS 存储桶的访问权限，只需在 Google Cloud 控制台中删除授予此集群的信任策略。

### 为 Azure 启用审计日志

要为 Azure 启用审计日志，请按照以下步骤操作：

#### Step 1. 创建 Azure 存储账户

在你组织的 Azure 订阅中创建一个 Azure 存储账户，作为 TiDB Cloud 写入数据库审计日志的目标。

更多信息请参见 [Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)（Azure 文档）。

#### Step 2. 配置 Azure Blob 存储访问权限

1. 在 [Azure 门户](https://portal.azure.com/) 中，创建用于存储数据库审计日志的容器。

    1. 在左侧导航栏中，点击 **Storage Accounts**，然后选择用于存储数据库审计日志的存储账户。

        > **Tip:**
        >
        > 如果左侧导航栏隐藏，点击左上角的菜单按钮切换显示。

    2. 在所选存储账户的导航栏中，点击 **Data storage > Containers**，然后点击 **+ Container** 打开 **New container** 面板。

    3. 在 **New container** 面板中，为你的新容器输入名称，设置匿名访问级别（建议选择 **Private**，即无匿名访问），然后点击 **Create**。几秒钟后，新容器会创建并显示在容器列表中。

2. 获取目标容器的 URL。

    1. 在容器列表中，选择目标容器，点击容器旁的 **...**，然后选择 **Container properties**。
    2. 在显示的属性页面中，复制 **URL** 值备用，然后返回容器列表。

3. 生成目标容器的 SAS 令牌。

    1. 在容器列表中，选择目标容器，点击容器旁的 **...**，然后选择 **Generate SAS**。
    2. 在显示的 **Generate SAS** 面板中，选择 **Account key** 作为 **Signing method**。
    3. 在 **Permissions** 下拉列表中，选择 **Read**、**Write** 和 **Create**，以允许写入审计日志文件。
    4. 在 **Start** 和 **Expiry** 字段中，指定 SAS 令牌的有效期。

        > **Note:**
        >
        > - 审计功能需要持续向存储账户写入审计日志，因此 SAS 令牌必须具有足够长的有效期。但有效期越长，泄露风险越大。出于安全考虑，建议每六到十二个月更换一次 SAS 令牌。
        > - 生成的 SAS 令牌无法撤销，因此需要谨慎设置其有效期。
        > - 确保在 SAS 令牌到期前重新生成并更新，以保证审计日志的持续可用。

    5. 在 **Allowed protocols** 中，选择 **HTTPS only**，确保安全访问。
    6. 点击 **Generate SAS token and URL**，复制显示的 **Blob SAS token** 备用。

#### Step 3. 启用审计日志

1. 在 TiDB Cloud 控制台中，导航到你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **Tip:**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
4. 在 **Enable Database Audit Logging** 对话框中，提供你从 [Step 2. 配置 Azure Blob 存储访问](#step-2-configure-azure-blob-storage-access) 获取的 **Blob URL** 和 **SAS Token**：

    - 在 **Blob URL** 字段中，输入存储审计日志的容器 URL。
    - 在 **SAS Token** 字段中，输入访问容器的 SAS 令牌。

5. 点击 **Test Connection**，验证 TiDB Cloud 是否能访问并写入容器。

    如果成功，会显示 **The connection is successfully**。否则，请检查你的访问配置。

6. 点击 **Enable**，启用该集群的审计日志。

    TiDB Cloud 现已准备好将审计日志写入你的 Azure Blob 容器。

> **Note:**
>
> 在启用审计日志后，如果你对 **Blob URL** 或 **SAS Token** 字段进行了任何新更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否能连接到容器。然后，点击 **Enable** 以应用更改。

## 指定审计过滤规则

启用审计日志后，你必须指定审计过滤规则，以控制捕获和写入审计日志的用户访问事件。如果没有指定过滤规则，TiDB Cloud 不会记录任何内容。

要为集群指定审计过滤规则，请执行以下步骤：

1. 在 **DB Audit Logging** 页面，点击 **Add Filter Rule**，添加审计过滤规则。

    你可以一次添加一条规则。每条规则指定用户表达式、数据库表达式、表表达式和访问类型。可以添加多条规则以满足你的审计需求。

2. 在 **Log Filter Rules** 区域，点击 **>** 展开并查看已添加的审计规则列表。

> **Note:**
>
> - 过滤规则是正则表达式，区分大小写。如果使用通配符规则 `.*`，则会记录集群中所有用户、数据库或表的事件。
> - 由于审计日志会消耗集群资源，建议谨慎设置过滤规则。为了减少资源消耗，建议限制过滤范围，仅对特定数据库对象、用户和操作设置过滤规则。

## 查看审计日志

默认情况下，TiDB Cloud 会将数据库审计日志文件存储在你的存储服务中，因此你需要从存储服务中读取审计日志信息。

> **Note:**
>
> 如果你已请求并选择将审计日志文件存储在 TiDB Cloud 中，可以在 **Database Audit Logging** 页面中的 **Audit Log Access** 部分下载。

TiDB Cloud 的审计日志是可读文本文件，文件名中包含集群 ID、Pod ID 和日志创建日期。

例如：`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示集群 ID，`tidb-0` 表示 Pod ID。

## 禁用审计日志

如果你不再需要对某个集群进行审计，可以进入该集群的页面，点击 **Settings** > **Audit Settings**，然后在右上角切换审计设置为 **Off**。

> **Note:**
>
> 每当日志文件大小达到 10 MiB 时，日志文件会被推送到云存储桶。因此，禁用审计日志后，大小小于 10 MiB 的日志文件不会自动推送到云存储桶。如需获取此类日志文件，请联系 [PingCAP support](/tidb-cloud/tidb-cloud-support.md)。

## 审计日志字段

对于审计日志中的每个数据库事件记录，TiDB 提供以下字段：

> **Note:**
>
> 在下表中，字段的最大长度为空表示该字段的数据类型具有明确的常量长度（例如，INTEGER 为 4 字节）。

| Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | 保留供内部使用 |
| 2 | N/A | N/A | N/A | 保留供内部使用 |
| 3 | N/A | N/A | N/A | 保留供内部使用 |
| 4 | ID       | INTEGER |  | 唯一事件ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | 事件时间   |
| 6 | EVENT_CLASS | VARCHAR | 15 | 事件类型     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | 事件子类型 |
| 8 | STATUS_CODE | INTEGER |  | 语句响应状态   |
| 9 | COST_TIME | FLOAT |  | 语句耗时    |
| 10 | HOST | VARCHAR | 16 | 服务器IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | 客户端IP   |
| 12 | USER | VARCHAR | 17 | 登录用户名    |
| 13 | DATABASE | VARCHAR | 64 | 事件相关数据库      |
| 14 | TABLES | VARCHAR | 64 | 事件相关表名          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | 掩码SQL语句   |
| 16 | ROWS | INTEGER |  | 影响的行数（`0` 表示无影响行）      |

根据 TiDB 设置的 EVENT_CLASS 字段值，审计日志中的数据库事件记录还包含以下附加字段：

- 如果 EVENT_CLASS 值为 `CONNECTION`，数据库事件记录还包含以下字段：

    | Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | 客户端端口号 |
    | 18 | CONNECTION_ID | INTEGER |  | 连接ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | 连接类型（`socket` 或 `unix-socket`） |
    | 20 | SERVER_ID | INTEGER |  | TiDB 服务器ID |
    | 21 | SERVER_PORT | INTEGER |  | TiDB 服务器监听的端口（MySQL协议） |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | TiDB 进程启动系统的用户名 |
    | 23 | OS_VERSION | VARCHAR | N/A | TiDB 服务器所在操作系统版本 |
    | 24 | SSL_VERSION | VARCHAR | 6 | 当前 TiDB 的 SSL 版本 |
    | 25 | PID | INTEGER |  | TiDB 进程的PID |

- 如果 EVENT_CLASS 值为 `TABLE_ACCESS` 或 `GENERAL`，数据库事件记录还包含以下字段：

    | Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | 连接ID   |
    | 18 | COMMAND | VARCHAR | 14 | MySQL 协议的命令类型 |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | SQL语句类型 |
    | 20 | PID | INTEGER |  | TiDB 进程的PID  |