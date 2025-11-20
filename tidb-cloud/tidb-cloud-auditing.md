---
title: TiDB Cloud 专属数据库审计日志
summary: 了解如何在 TiDB Cloud 中审计集群。
---

# TiDB Cloud 专属数据库审计日志

TiDB Cloud 提供了审计日志功能，用于记录数据库的用户访问活动，例如执行的 SQL 语句。

> **注意：**
>
> 目前，数据库审计日志功能仅支持按需开通。若需申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写 “Apply for database audit logging”，并点击 **Submit**。

为了评估组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能**默认关闭**。要对集群进行审计，必须先启用审计日志功能，然后指定审计过滤规则。

> **注意：**
>
> 由于审计日志会消耗集群资源，请谨慎决定是否对集群进行审计。

## 前提条件

- 你正在使用 TiDB Cloud 专属集群。

    > **注意：**
    >
    > - TiDB Cloud Starter 不支持数据库审计日志功能。
    > - 对于 TiDB Cloud Essential，请参见 [TiDB Cloud Essential 数据库审计日志（Beta）](/tidb-cloud/essential-database-audit-logging.md)。

- 你在组织中拥有 `Organization Owner` 或 `Project Owner` 角色。否则，你无法在 TiDB Cloud 控制台中看到与数据库审计相关的选项。更多信息请参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

## 启用审计日志

TiDB Cloud 支持将 TiDB Cloud 专属集群的审计日志记录到你的云存储服务。在启用数据库审计日志之前，请在集群所在的云服务商上配置你的云存储服务。

> **注意：**
>
> 对于部署在 AWS 上的 TiDB 集群，在启用数据库审计日志时，你可以选择将审计日志文件存储在 TiDB Cloud。目前，该功能仅支持按需开通。若需申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写 “Apply to store audit log files in TiDB Cloud”，并点击 **Submit**。

### 在 AWS 上启用审计日志

要在 AWS 上启用审计日志，请按照以下步骤操作：

#### 步骤 1. 创建 Amazon S3 存储桶

在你组织拥有的 AWS 账号中指定一个 Amazon S3 存储桶，作为 TiDB Cloud 写入审计日志的目标位置。

> **注意：**
>
> 不要在 AWS S3 存储桶上启用对象锁定。启用对象锁定会阻止 TiDB Cloud 向 S3 推送审计日志文件。

更多信息请参见 AWS 用户指南中的 [创建存储桶](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。

#### 步骤 2. 配置 Amazon S3 访问权限

1. 获取你要启用审计日志的 TiDB 集群的 TiDB Cloud Account ID 和 External ID。

    1. 在 TiDB Cloud 控制台，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **AWS IAM Policy Settings** 部分，记录下 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID**，以备后用。

2. 在 AWS 管理控制台，进入 **IAM** > **Access Management** > **Policies**，检查是否已有具备 `s3:PutObject` 写入权限的存储桶策略。

    - 如果有，记录该存储桶策略以备后用。
    - 如果没有，进入 **IAM** > **Access Management** > **Policies** > **Create Policy**，并根据以下策略模板定义存储桶策略。

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

        其中，`<Your S3 bucket ARN>` 是你 S3 存储桶的 Amazon 资源名称（ARN），即审计日志文件将被写入的存储桶。你可以在 S3 存储桶的 **Properties** 标签页的 **Bucket Overview** 区域获取 ARN 值。在 `"Resource"` 字段中，需要在 ARN 后加上 `/*`。例如，如果 ARN 是 `arn:aws:s3:::tidb-cloud-test`，则 `"Resource"` 字段的值应为 `"arn:aws:s3:::tidb-cloud-test/*"`。

3. 进入 **IAM** > **Access Management** > **Roles**，检查是否已存在信任实体为你之前记录的 TiDB Cloud Account ID 和 External ID 的角色。

    - 如果有，记录该角色以备后用。
    - 如果没有，点击 **Create role**，选择 **Another AWS account** 作为信任实体类型，在 **Account ID** 字段输入 TiDB Cloud Account ID。然后，选择 **Require External ID** 选项，并在 **External ID** 字段输入 TiDB Cloud External ID。

4. 在 **IAM** > **Access Management** > **Roles**，点击上一步的角色名称进入 **Summary** 页面，然后按以下步骤操作：

    1. 在 **Permissions** 标签页，检查该角色是否已附加具备 `s3:PutObject` 写入权限的策略。如果没有，选择 **Attach Policies**，搜索所需策略，然后点击 **Attach Policy**。
    2. 返回 **Summary** 页面，复制 **Role ARN** 的值到剪贴板。

#### 步骤 3. 启用审计日志

在 TiDB Cloud 控制台，返回你获取 TiDB Cloud Account ID 和 External ID 的 **Enable Database Audit Logging** 对话框，然后按以下步骤操作：

1. 在 **Bucket URI** 字段，输入你 S3 存储桶的 URI，即审计日志文件将被写入的位置。
2. 在 **Bucket Region** 下拉列表中，选择存储桶所在的 AWS 区域。
3. 在 **Role ARN** 字段，填写你在 [步骤 2. 配置 Amazon S3 访问权限](#step-2-configure-amazon-s3-access) 中复制的 Role ARN。
4. 点击 **Test Connection**，验证 TiDB Cloud 是否可以访问并写入该存储桶。

    如果连接成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

5. 点击 **Enable**，为该集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 Amazon S3 存储桶。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI、位置或 ARN 做了任何更改，必须再次点击 **Test Connection** 验证 TiDB Cloud 是否可以连接到存储桶。然后点击 **Enable** 应用更改。
> - 若要移除 TiDB Cloud 对你 Amazon S3 的访问权限，只需在 AWS 管理控制台中删除授予该集群的信任策略。

### 在 Google Cloud 上启用审计日志

要在 Google Cloud 上启用审计日志，请按照以下步骤操作：

#### 步骤 1. 创建 GCS 存储桶

在你组织拥有的 Google Cloud 账号中指定一个 Google Cloud Storage (GCS) 存储桶，作为 TiDB Cloud 写入审计日志的目标位置。

更多信息请参见 Google Cloud Storage 文档中的 [创建存储桶](https://cloud.google.com/storage/docs/creating-buckets)。

#### 步骤 2. 配置 GCS 访问权限

1. 获取你要启用审计日志的 TiDB 集群的 Google Cloud Service Account ID。

    1. 在 TiDB Cloud 控制台，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **Google Cloud Server Account ID** 部分，记录下 **Service Account ID**，以备后用。

2. 在 Google Cloud 控制台，进入 **IAM & Admin** > **Roles**，检查是否存在具备以下存储容器写入权限的角色。

    - storage.objects.create
    - storage.objects.delete

    如果有，记录该角色以备后用。如果没有，进入 **IAM & Admin** > **Roles** > **CREATE ROLE**，为 TiDB 集群定义一个角色。

3. 进入 **Cloud Storage** > **Browser**，选择你希望 TiDB Cloud 访问的 GCS 存储桶，然后点击 **SHOW INFO PANEL**。

    信息面板将显示。

4. 在面板中，点击 **ADD PRINCIPAL**。

    将弹出添加主体的对话框。

5. 在对话框中，按以下步骤操作：

    1. 在 **New Principals** 字段，粘贴 TiDB 集群的 Google Cloud Service Account ID。
    2. 在 **Role** 下拉列表中，选择目标 TiDB 集群的角色。
    3. 点击 **SAVE**。

#### 步骤 3. 启用审计日志

在 TiDB Cloud 控制台，返回你获取 TiDB Cloud 账号 ID 的 **Enable Database Audit Logging** 对话框，然后按以下步骤操作：

1. 在 **Bucket URI** 字段，输入你的完整 GCS 存储桶名称。
2. 在 **Bucket Region** 字段，选择存储桶所在的 GCS 区域。
3. 点击 **Test Connection**，验证 TiDB Cloud 是否可以访问并写入该存储桶。

    如果连接成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

4. 点击 **Enable**，为该集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 GCS 存储桶。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI 或位置做了任何更改，必须再次点击 **Test Connection** 验证 TiDB Cloud 是否可以连接到存储桶。然后点击 **Enable** 应用更改。
> - 若要移除 TiDB Cloud 对你 GCS 存储桶的访问权限，请在 Google Cloud 控制台中删除授予该集群的信任策略。

### 在 Azure 上启用审计日志

要在 Azure 上启用审计日志，请按照以下步骤操作：

#### 步骤 1. 创建 Azure 存储账户

在你组织的 Azure 订阅下创建一个 Azure 存储账户，作为 TiDB Cloud 写入数据库审计日志的目标位置。

更多信息请参见 Azure 文档中的 [创建 Azure 存储账户](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)。

#### 步骤 2. 配置 Azure Blob Storage 访问权限

1. 在 [Azure 门户](https://portal.azure.com/) 中，创建用于存储数据库审计日志的容器。

    1. 在 Azure 门户左侧导航栏点击 **Storage Accounts**，然后点击用于存储数据库审计日志的存储账户。

        > **提示：**
        >
        > 如果左侧导航栏被隐藏，可点击左上角菜单按钮切换其显示状态。

    2. 在所选存储账户的导航栏中，点击 **Data storage > Containers**，然后点击 **+ Container** 打开 **New container** 面板。

    3. 在 **New container** 面板中，为新容器输入名称，设置匿名访问级别（推荐级别为 **Private**，即不允许匿名访问），然后点击 **Create**。几秒钟后，新容器会被创建并显示在容器列表中。

2. 获取目标容器的 URL。

    1. 在容器列表中，选中目标容器，点击容器的 **...**，然后选择 **Container properties**。
    2. 在显示的属性页面，复制 **URL** 的值以备后用，然后返回容器列表。

3. 为目标容器生成 SAS token。

    1. 在容器列表中，选中目标容器，点击容器的 **...**，然后选择 **Generate SAS**。
    2. 在显示的 **Generate SAS** 面板中，**Signing method** 选择 **Account key**。
    3. 在 **Permissions** 下拉列表中，选择 **Read**、**Write** 和 **Create**，以允许写入审计日志文件。
    4. 在 **Start** 和 **Expiry** 字段，指定 SAS token 的有效期。

        > **注意：**
        >
        > - 审计功能需要持续向存储账户写入审计日志，因此 SAS token 必须有足够长的有效期。但有效期越长，token 泄露的风险越高。为安全起见，建议每 6 到 12 个月更换一次 SAS token。
        > - 生成的 SAS token 无法撤销，因此需要谨慎设置其有效期。
        > - 请确保在 SAS token 过期前重新生成并更新 token，以保证审计日志的持续可用性。

    5. **Allowed protocols** 选择 **HTTPS only**，以确保安全访问。
    6. 点击 **Generate SAS token and URL**，然后复制显示的 **Blob SAS token** 以备后用。

#### 步骤 3. 启用审计日志

1. 在 TiDB Cloud 控制台，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
4. 在 **Enable Database Audit Logging** 对话框中，填写你在 [步骤 2. 配置 Azure Blob 访问权限](#step-2-configure-azure-blob-storage-access) 获取的 blob URL 和 SAS token：

    - 在 **Blob URL** 字段，输入存储审计日志的容器 URL。
    - 在 **SAS Token** 字段，输入访问该容器的 SAS token。

5. 点击 **Test Connection**，验证 TiDB Cloud 是否可以访问并写入该容器。

    如果连接成功，将显示 **The connection is successfully**。否则，请检查你的访问配置。

6. 点击 **Enable**，为该集群启用审计日志。

    TiDB Cloud 已准备好将指定集群的审计日志写入你的 Azure blob 容器。

> **注意：**
>
> 启用审计日志后，如果你对 **Blob URL** 或 **SAS Token** 字段做了新的更改，必须再次点击 **Test Connection** 验证 TiDB Cloud 是否可以连接到容器。然后点击 **Enable** 应用更改。

## 指定审计过滤规则

启用审计日志后，必须指定审计过滤规则，以控制捕获和写入哪些用户访问事件到审计日志。如果未指定过滤规则，TiDB Cloud 不会记录任何日志。

要为集群指定审计过滤规则，请按以下步骤操作：

1. 在 **DB Audit Logging** 页面，点击 **Log Filter Rules** 区域的 **Add Filter Rule**，添加一条审计过滤规则。

    每次只能添加一条审计规则。每条规则需指定用户表达式、数据库表达式、表表达式和访问类型。你可以添加多条审计规则，以满足你的审计需求。

2. 在 **Log Filter Rules** 区域，点击 **>** 展开并查看你已添加的审计规则列表。

> **注意：**
>
> - 过滤规则为正则表达式，且区分大小写。如果使用通配规则 `.*`，则集群中所有用户、数据库或表的事件都会被记录。
> - 由于审计日志会消耗集群资源，指定过滤规则时请谨慎。为最小化资源消耗，建议尽量指定过滤规则，将审计日志范围限定在特定的数据库对象、用户和操作上。

## 查看审计日志

默认情况下，TiDB Cloud 会将数据库审计日志文件存储在你的存储服务中，因此你需要从存储服务中读取审计日志信息。

> **注意：**
>
> 如果你已申请并选择将审计日志文件存储在 TiDB Cloud，可以在 **Database Audit Logging** 页面的 **Audit Log Access** 区域下载日志文件。

TiDB Cloud 审计日志为可读的文本文件，文件名中包含集群 ID、节点 ID 和日志创建日期。

例如：`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示集群 ID，`tidb-0` 表示节点 ID。

## 禁用审计日志

如果你不再需要对集群进行审计，可进入该集群页面，点击 **Settings** > **Audit Settings**，然后将右上角的审计开关切换为 **Off**。

> **注意：**
>
> 每当日志文件大小达到 10 MiB 时，日志文件会被推送到云存储桶。因此，禁用审计日志后，文件大小小于 10 MiB 的日志不会自动推送到云存储桶。如需获取此类日志文件，请联系 [PingCAP 支持](/tidb-cloud/tidb-cloud-support.md)。

## 审计日志字段

对于审计日志中的每条数据库事件记录，TiDB 提供以下字段：

> **注意：**
>
> 下表中，字段的最大长度为空表示该字段的数据类型有固定的常量长度（例如 INTEGER 为 4 字节）。

| Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | 预留给内部使用 |
| 2 | N/A | N/A | N/A | 预留给内部使用 |
| 3 | N/A | N/A | N/A | 预留给内部使用 |
| 4 | ID       | INTEGER |  | 唯一事件 ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | 事件发生时间   |
| 6 | EVENT_CLASS | VARCHAR | 15 | 事件类型     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | 事件子类型 |
| 8 | STATUS_CODE | INTEGER |  | 语句响应状态   |
| 9 | COST_TIME | FLOAT |  | 语句消耗时间    |
| 10 | HOST | VARCHAR | 16 | 服务器 IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | 客户端 IP   |
| 12 | USER | VARCHAR | 17 | 登录用户名    |
| 13 | DATABASE | VARCHAR | 64 | 事件相关数据库      |
| 14 | TABLES | VARCHAR | 64 | 事件相关表名          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | 脱敏后的 SQL 语句   |
| 16 | ROWS | INTEGER |  | 受影响的行数（`0` 表示未影响任何行）      |

根据 TiDB 设置的 EVENT_CLASS 字段值，审计日志中的数据库事件记录还包含以下附加字段：

- 如果 EVENT_CLASS 的值为 `CONNECTION`，数据库事件记录还包含以下字段：

    | Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | 客户端端口号 |
    | 18 | CONNECTION_ID | INTEGER |  | 连接 ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | 通过 `socket` 或 `unix-socket` 连接 |
    | 20 | SERVER_ID | INTEGER |  | TiDB 服务器 ID |
    | 21 | SERVER_PORT | INTEGER |  | TiDB 服务器监听 MySQL 协议客户端的端口 |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | TiDB 进程启动系统的用户名  |
    | 23 | OS_VERSION | VARCHAR | N/A | TiDB 服务器所在操作系统的版本  |
    | 24 | SSL_VERSION | VARCHAR | 6 | TiDB 当前的 SSL 版本 |
    | 25 | PID | INTEGER |  | TiDB 进程的 PID |

- 如果 EVENT_CLASS 的值为 `TABLE_ACCESS` 或 `GENERAL`，数据库事件记录还包含以下字段：

    | Col # | 字段名 | TiDB 数据类型 | 最大长度 | 描述 |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | 连接 ID   |
    | 18 | COMMAND | VARCHAR | 14 | MySQL 协议的命令类型 |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | SQL 语句类型 |
    | 20 | PID | INTEGER |  | TiDB 进程的 PID  |