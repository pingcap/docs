---
title: TiDB Cloud Dedicated 数据库审计日志（旧版）
summary: 了解如何在 TiDB Cloud 中审计集群。
---

# TiDB Cloud Dedicated 数据库审计日志（旧版）

TiDB Cloud 提供审计日志功能，用于记录数据库的用户访问活动，例如已执行的 SQL 语句。

> **Note:**
>
> 这是数据库审计日志功能的旧版本。此前，该功能仅对一小部分测试用户开放，目前已进入维护模式。本文档面向这些现有用户。对于新的部署，请参见 [TiDB Cloud Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md)，该功能提供更细粒度的事件类以及更详细的审计日志。

为了评估组织中的用户访问策略及其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能**默认禁用**。要审计集群，你必须先启用审计日志，然后指定审计过滤规则。

> **Note:**
>
> 由于审计日志会消耗集群资源，因此请谨慎评估是否需要对集群启用审计。

## 前提条件 {#prerequisites}

- 你正在使用 TiDB Cloud Dedicated 集群。

    > **Note:**
    >
    > - {{{ .starter }}} 不支持数据库审计日志。
    > - 对于 {{{ .essential }}}，请参见 [Database Audit Logging (Preview) for {{{ .essential }}}](/tidb-cloud/essential-database-audit-logging.md)。

- 你在组织中拥有 `Organization Owner` 或 `Project Owner` 角色。否则，你将无法在 TiDB Cloud 控制台中看到与数据库审计相关的选项。更多信息，请参见 [User roles](/tidb-cloud/manage-user-access.md#user-roles)。

## 启用审计日志 {#enable-audit-logging}

TiDB Cloud 支持将 TiDB Cloud Dedicated 集群的审计日志记录到你的云存储服务中。在启用数据库审计日志之前，请先在集群所在的云服务提供商上配置云存储服务。

> **Note:**
>
> 对于部署在 AWS 上的 TiDB 集群，你可以在启用数据库审计日志时选择将审计日志文件存储在 TiDB Cloud 中。目前，此功能仅可按需申请。如需申请此功能，请点击 [TiDB Cloud console](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 进入 [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段中填写 "Apply to store audit log files in TiDB Cloud"，然后点击 **Submit**。

### 为 AWS 启用审计日志 {#enable-audit-logging-for-aws}

要为 AWS 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 Amazon S3 bucket {#step-1-create-an-amazon-s3-bucket}

在你组织拥有的 AWS 账户中指定一个 Amazon S3 bucket，作为 TiDB Cloud 写入审计日志的目标位置。

> **Note:**
>
> 不要在 AWS S3 bucket 上启用 object lock。启用 object lock 会阻止 TiDB Cloud 将审计日志文件推送到 S3。

更多信息，请参见 AWS User Guide 中的 [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。

#### 步骤 2. 配置 Amazon S3 访问 {#step-2-configure-amazon-s3-access}

1. 获取你要启用审计日志的 TiDB 集群的 TiDB Cloud Account ID 和 External ID。

    1. 在 TiDB Cloud 控制台中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群的名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面右上角点击 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **AWS IAM Policy Settings** 部分，并记录 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID** 以供后续使用。

2. 在 AWS Management Console 中，进入 **IAM** > **Access Management** > **Policies**，然后检查是否存在具有 `s3:PutObject` 只写权限的存储 bucket policy。

    - 如果存在，记录匹配的存储 bucket policy 以供后续使用。
    - 如果不存在，进入 **IAM** > **Access Management** > **Policies** > **Create Policy**，并根据以下 policy 模板定义一个 bucket policy。

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

        在该模板中，`<Your S3 bucket ARN>` 是要写入审计日志文件的 S3 bucket 的 Amazon Resource Name (ARN)。你可以进入 S3 bucket 的 **Properties** 标签页，并在 **Bucket Overview** 区域获取 ARN 值。在 `"Resource"` 字段中，你需要在 ARN 后追加 `/*`。例如，如果 ARN 为 `arn:aws:s3:::tidb-cloud-test`，则需要将 `"Resource"` 字段的值配置为 `"arn:aws:s3:::tidb-cloud-test/*"`。

3. 进入 **IAM** > **Access Management** > **Roles**，然后检查是否已存在一个角色，其信任实体与之前记录的 TiDB Cloud Account ID 和 External ID 对应。

    - 如果存在，记录匹配的角色以供后续使用。
    - 如果不存在，点击 **Create role**，选择 **Another AWS account** 作为信任实体类型，然后在 **Account ID** 字段中输入 TiDB Cloud Account ID 的值。接着，选择 **Require External ID** 选项，并在 **External ID** 字段中输入 TiDB Cloud External ID 的值。

4. 在 **IAM** > **Access Management** > **Roles** 中，点击上一步中的角色名称进入 **Summary** 页面，然后执行以下步骤：

    1. 在 **Permissions** 标签页下，检查之前记录的具有 `s3:PutObject` 只写权限的 policy 是否已附加到该角色。如果没有，请选择 **Attach Policies**，搜索所需 policy，然后点击 **Attach Policy**。
    2. 返回 **Summary** 页面，并将 **Role ARN** 的值复制到剪贴板。

#### 步骤 3. 启用审计日志 {#step-3-enable-audit-logging}

在 TiDB Cloud 控制台中，返回你获取 TiDB Cloud account ID 和 External ID 值时所在的 **Enable Database Audit Logging** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入要写入审计日志文件的 S3 bucket 的 URI。
2. 在 **Bucket Region** 下拉列表中，选择 bucket 所在的 AWS 区域。
3. 在 **Role ARN** 字段中，填写你在[步骤 2. 配置 Amazon S3 访问](#step-2-configure-amazon-s3-access)中复制的 Role ARN 值。
4. 点击 **Test Connection** 以验证 TiDB Cloud 是否可以访问并写入该 bucket。

    如果成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

5. 点击 **Enable** 为集群启用审计日志。

    TiDB Cloud 现已准备好将指定集群的审计日志写入你的 Amazon S3 bucket。

> **Note:**
>
> - 启用审计日志后，如果你对 bucket URI、位置或 ARN 做了任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 能够连接到该 bucket。然后，点击 **Enable** 以应用更改。
> - 若要移除 TiDB Cloud 对 Amazon S3 的访问权限，只需在 AWS Management Console 中删除授予此集群的 trust policy。

### 为 Google Cloud 启用审计日志 {#enable-audit-logging-for-google-cloud}

要为 Google Cloud 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 GCS bucket {#step-1-create-a-gcs-bucket}

在你组织拥有的 Google Cloud 账户中指定一个 Google Cloud Storage (GCS) bucket，作为 TiDB Cloud 写入审计日志的目标位置。

更多信息，请参见 Google Cloud Storage 文档中的 [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets)。

#### 步骤 2. 配置 GCS 访问 {#step-2-configure-gcs-access}

1. 获取你要启用审计日志的 TiDB 集群的 Google Cloud Service Account ID。

    1. 在 TiDB Cloud 控制台中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群的名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面右上角点击 **Enable**。
    4. 在 **Enable Database Audit Logging** 对话框中，找到 **Google Cloud Server Account ID** 部分，并记录 **Service Account ID** 以供后续使用。

2. 在 Google Cloud console 中，进入 **IAM & Admin** > **Roles**，然后检查是否存在一个角色，具有以下存储容器只写权限。

    - storage.objects.create
    - storage.objects.delete

    如果存在，记录与该 TiDB 集群匹配的角色以供后续使用。如果不存在，进入 **IAM & Admin** > **Roles** > **CREATE ROLE**，为该 TiDB 集群定义一个角色。

3. 进入 **Cloud Storage** > **Browser**，选择你希望 TiDB Cloud 访问的 GCS bucket，然后点击 **SHOW INFO PANEL**。

    此时会显示信息面板。

4. 在面板中，点击 **ADD PRINCIPAL**。

    此时会显示添加 principal 的对话框。

5. 在对话框中，执行以下步骤：

    1. 在 **New Principals** 字段中，粘贴 TiDB 集群的 Google Cloud Service Account ID。
    2. 在 **Role** 下拉列表中，选择目标 TiDB 集群的角色。
    3. 点击 **SAVE**。

#### 步骤 3. 启用审计日志 {#step-3-enable-audit-logging}

在 TiDB Cloud 控制台中，返回你获取 TiDB Cloud account ID 时所在的 **Enable Database Audit Logging** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入完整的 GCS bucket 名称。
2. 在 **Bucket Region** 字段中，选择 bucket 所在的 GCS 区域。
3. 点击 **Test Connection** 以验证 TiDB Cloud 是否可以访问并写入该 bucket。

    如果成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

4. 点击 **Enable** 为集群启用审计日志。

    TiDB Cloud 现已准备好将指定集群的审计日志写入你的 GCS bucket。

> **Note:**
>
> - 启用审计日志后，如果你对 bucket URI 或位置做了任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 能够连接到该 bucket。然后，点击 **Enable** 以应用更改。
> - 若要移除 TiDB Cloud 对 GCS bucket 的访问权限，请在 Google Cloud console 中删除授予此集群的 trust policy。

### 为 Azure 启用审计日志 {#enable-audit-logging-for-azure}

要为 Azure 启用审计日志，请执行以下步骤：

#### 步骤 1. 创建 Azure storage account {#step-1-create-an-azure-storage-account}

在你组织的 Azure 订阅中创建一个 Azure storage account，作为 TiDB Cloud 写入数据库审计日志的目标位置。

更多信息，请参见 Azure 文档中的 [Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)。

#### 第 2 步：配置 Azure Blob Storage 访问 {#step-2-configure-azure-blob-storage-access}

1. 在 [Azure portal](https://portal.azure.com/) 中，创建一个用于存储数据库审计日志的容器。

    1. 在 Azure portal 左侧导航窗格中，点击 **Storage Accounts**，然后点击用于存储数据库审计日志的存储账户。

        > **Tip:**
        >
        > 如果左侧导航窗格被隐藏，请点击左上角的菜单按钮以切换其显示状态。

    2. 在所选存储账户的导航窗格中，点击 **Data storage > Containers**，然后点击 **+ Container** 打开 **New container** 窗格。

    3. 在 **New container** 窗格中，为新容器输入名称，设置匿名访问级别（推荐级别为 **Private**，表示不允许匿名访问），然后点击 **Create**。几秒钟后，新容器将被创建并显示在容器列表中。

2. 获取目标容器的 URL。

    1. 在容器列表中，选择目标容器，点击该容器对应的 **...**，然后选择 **Container properties**。
    2. 在显示的属性页面中，复制 **URL** 的值以备后用，然后返回容器列表。

3. 为目标容器生成 SAS token。

    1. 在容器列表中，选择目标容器，点击该容器对应的 **...**，然后选择 **Generate SAS**。
    2. 在显示的 **Generate SAS** 窗格中，在 **Signing method** 中选择 **Account key**。
    3. 在 **Permissions** 下拉列表中，选择 **Read**、**Write** 和 **Create**，以允许写入审计日志文件。
    4. 在 **Start** 和 **Expiry** 字段中，为 SAS token 指定有效期。

        > **Note:**
        >
        > - 审计功能需要持续将审计日志写入存储账户，因此 SAS token 必须具有足够长的有效期。但是，有效期越长，token 泄漏的风险越高。出于安全考虑，建议每六到十二个月更换一次 SAS token。
        > - 已生成的 SAS token 无法被回收，因此你需要谨慎设置其有效期。
        > - 请确保在 SAS token 过期之前重新生成并修改它，以保证审计日志的持续可用性。

    5. 对于 **Allowed protocols**，选择 **HTTPS only** 以确保安全访问。
    6. 点击 **Generate SAS token and URL**，然后复制显示的 **Blob SAS token** 以备后用。

#### 第 3 步：启用审计日志记录 {#step-3-enable-audit-logging}

1. 在 TiDB Cloud 控制台中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 点击目标 TiDB Cloud Dedicated 集群的名称进入其概览页面，然后在左侧导航窗格中点击 **Settings** > **DB Audit Logging**。
3. 在 **DB Audit Logging** 页面右上角，点击 **Enable**。
4. 在 **Enable Database Audit Logging** 对话框中，提供你在[第 2 步：配置 Azure Blob 访问](#step-2-configure-azure-blob-storage-access)中获取的 blob URL 和 SAS token：

    - 在 **Blob URL** 字段中，输入用于存储审计日志的容器 URL。
    - 在 **SAS Token** 字段中，输入用于访问该容器的 SAS token。

5. 点击 **Test Connection**，验证 TiDB Cloud 是否可以访问并写入该容器。

    如果成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

6. 点击 **Enable**，为该集群启用审计日志记录。

    TiDB Cloud 现已准备好将指定集群的审计日志写入你的 Azure blob 容器。

> **Note:**
>
> 启用审计日志记录后，如果你对 **Blob URL** 或 **SAS Token** 字段进行了新的修改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 能够连接到该容器。然后，点击 **Enable** 以应用这些更改。

## 指定审计过滤规则 {#specify-auditing-filter-rules}

启用审计日志记录后，你必须指定审计过滤规则，以控制要捕获并写入审计日志的用户访问事件。如果未指定过滤规则，TiDB Cloud 不会记录任何内容。

如需为集群指定审计过滤规则，请执行以下步骤：

1. 在 **DB Audit Logging** 页面中，点击 **Log Filter Rules** 部分中的 **Add Filter Rule**，添加一条审计过滤规则。

    你一次只能添加一条审计规则。每条规则都指定一个用户表达式、数据库表达式、表表达式和访问类型。你可以添加多条审计规则，以满足你的审计需求。

2. 在 **Log Filter Rules** 部分中，点击 **>** 展开并查看你已添加的审计规则列表。

> **Note:**
>
> - 过滤规则是正则表达式，并且大小写敏感。如果你使用通配符规则 `.*`，则会记录集群中所有用户、数据库或表事件。
> - 由于审计日志记录会消耗集群资源，因此在指定过滤规则时请谨慎。为尽量减少资源消耗，建议尽可能通过过滤规则将审计日志记录的作用域限制为特定的数据库对象、用户和操作。

## 查看审计日志 {#view-audit-logs}

默认情况下，TiDB Cloud 会将数据库审计日志文件存储在你的存储服务中，因此你需要从存储服务中读取审计日志信息。

> **Note:**
>
> 如果你已申请并选择将审计日志文件存储在 TiDB Cloud 中，则可以从 **Database Audit Logging** 页面上的 **Audit Log Access** 部分下载这些文件。

TiDB Cloud 审计日志是可读的文本文件，其完整文件名中包含集群 ID、节点 ID 和日志创建日期。

例如，`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示集群 ID，`tidb-0` 表示节点 ID。

## 禁用审计日志记录 {#disable-audit-logging}

如果你不再希望对某个集群进行审计，请进入该集群的页面，点击 **Settings** > **Audit Settings**，然后将右上角的审计开关切换为 **Off**。

> **Note:**
>
> 每当日志文件大小达到 10 MiB 时，该日志文件就会被推送到云存储 bucket。因此，在禁用审计日志后，大小小于 10 MiB 的日志文件不会被自动推送到云存储 bucket。在这种情况下，如需获取日志文件，请联系 [PingCAP support](/tidb-cloud/tidb-cloud-support.md)。

## 审计日志字段 {#audit-log-fields}

对于审计日志中的每条数据库事件记录，TiDB 提供以下字段：

> **Note:**
>
> 在下表中，字段的最大长度为空表示该字段的数据类型具有明确定义的固定长度常量（例如，INTEGER 为 4 字节）。

| Col # | Field name | TiDB data type | Maximum length | Description |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | 保留供内部使用 |
| 2 | N/A | N/A | N/A | 保留供内部使用 |
| 3 | N/A | N/A | N/A | 保留供内部使用 |
| 4 | ID       | INTEGER |  | 唯一事件 ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | 事件发生时间   |
| 6 | EVENT_CLASS | VARCHAR | 15 | 事件类型     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | 事件子类型 |
| 8 | STATUS_CODE | INTEGER |  | 语句的响应状态   |
| 9 | COST_TIME | FLOAT |  | 语句消耗的时间    |
| 10 | HOST | VARCHAR | 16 | 服务器 IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | 客户端 IP   |
| 12 | USER | VARCHAR | 17 | 登录用户名    |
| 13 | DATABASE | VARCHAR | 64 | 与事件相关的数据库      |
| 14 | TABLES | VARCHAR | 64 | 与事件相关的表名          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | 脱敏后的 SQL 语句   |
| 16 | ROWS | INTEGER |  | 受影响的行数（`0` 表示没有行受影响）      |

根据 TiDB 设置的 EVENT_CLASS 字段值，审计日志中的数据库事件记录还会包含以下附加字段：

- 如果 EVENT_CLASS 的值为 `CONNECTION`，数据库事件记录还会包含以下字段：

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | 客户端端口号 |
    | 18 | CONNECTION_ID | INTEGER |  | 连接 ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | 通过 `socket` 或 `unix-socket` 建立的连接 |
    | 20 | SERVER_ID | INTEGER |  | TiDB server ID |
    | 21 | SERVER_PORT | INTEGER |  | TiDB server 用于监听通过 MySQL 协议与客户端通信的端口 |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | 启动 TiDB 进程的系统用户名  |
    | 23 | OS_VERSION | VARCHAR | N/A | TiDB server 所在操作系统的版本  |
    | 24 | SSL_VERSION | VARCHAR | 6 | TiDB 当前的 SSL 版本 |
    | 25 | PID | INTEGER |  | TiDB 进程的 PID |

- 如果 EVENT_CLASS 的值为 `TABLE_ACCESS` 或 `GENERAL`，数据库事件记录还会包含以下字段：

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | 连接 ID   |
    | 18 | COMMAND | VARCHAR | 14 | MySQL 协议的命令类型 |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | SQL 语句类型 |
    | 20 | PID | INTEGER |  | TiDB 进程的 PID  |