---
title: TiDB Cloud Dedicated 数据库审计日志 (公测中)
summary: 了解如何在 TiDB Cloud 中审计集群。
---

# TiDB Cloud Dedicated 数据库审计日志 (公测中)

TiDB Cloud 提供了审计日志功能，用于记录数据库的用户访问活动，例如执行的 SQL 语句。

> **注意：**
>
> 数据库审计日志功能目前面向满足以下条件的 TiDB Cloud Dedicated 集群开放公测：
>
> - 对于部署在 AWS 和 Google Cloud 上的集群：TiDB 版本必须为 v7.5.6 或更高版本，或者 v8.5.2 或更高版本。
> - 对于部署在 Azure 上的集群：TiDB 版本必须为 v7.5.6 或更高版本，或者 v8.5.2 或更高版本，并且集群必须创建于 2026 年 4 月 15 日之后。
>
> 对于其他 TiDB 版本或集群配置，使用数据库审计日志功能需要单独申请。如需为不符合上述条件的集群申请该功能，请在 [TiDB Cloud 控制台](https://tidbcloud.com)右下角点击 **?**，然后点击 **Support Tickets** 进入[帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段中填写“Apply for database audit logging”，然后点击 **Submit**。
>
> 本文档仅适用于数据库审计日志功能的公测版本。如果你使用的是较早版本的数据库审计日志功能，请参阅 [TiDB Cloud 数据库审计日志（旧版）](/tidb-cloud/tidb-cloud-auditing-legacy.md)。

为了评估组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能**默认关闭**。要对集群进行审计，必须先启用审计日志功能，然后指定审计过滤规则。

> **注意：**
>
> 由于审计日志会消耗集群资源，请谨慎决定是否对集群进行审计。

## 前提条件

- 你正在使用 TiDB Cloud Dedicated 集群。

    > **注意：**
    >
    > - TiDB Cloud Starter 不支持数据库审计日志功能。
    > - 对于 TiDB Cloud Essential，请参见 [TiDB Cloud Essential 数据库审计日志（预览版）](/tidb-cloud/essential-database-audit-logging.md)。

- 你在组织中拥有 `Organization Owner` 或 `Project Owner` 角色。否则，你无法在 TiDB Cloud 控制台中看到与数据库审计相关的选项。更多信息请参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

## 启用审计日志

TiDB Cloud 支持将 TiDB Cloud Dedicated 集群的审计日志写入你的云存储服务。在启用数据库审计日志之前，请在集群所在的云服务商上配置你的云存储服务。

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

1. 获取你要为其启用审计日志的 TiDB 集群的 TiDB Cloud Account ID 和 External ID。

    1. 在 TiDB Cloud 控制台，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群的名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Database Audit Log Storage Configuration** 对话框中，找到 **AWS IAM Policy Settings** 部分，记录下 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID**，以备后用。

2. 在 [AWS 管理控制台](https://console.aws.amazon.com/) 中，进入 **IAM** > **Access Management** > **Policies**，检查是否已有具备 `s3:PutObject` 写入权限的 IAM 策略。

    - 如果有，记录该策略以备后用。
    - 如果没有，进入 **IAM** > **Access Management** > **Policies** > **Create Policy**，并根据以下策略模板定义 IAM 策略。

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

在 TiDB Cloud 控制台，返回你获取 TiDB Cloud Account ID 和 External ID 的 **Database Audit Log Storage Configuration** 对话框，然后按以下步骤操作：

1. 在 **Bucket URI** 字段，输入你 S3 存储桶的 URI，即审计日志文件将被写入的位置。
2. 在 **Bucket Region** 下拉列表中，选择存储桶所在的 AWS 区域。
3. 在 **Role ARN** 字段，填写你在 [步骤 2. 配置 Amazon S3 访问权限](#step-2-configure-amazon-s3-access) 中复制的 Role ARN。
4. 点击 **Test Connection and Next**，验证 TiDB Cloud 是否可以访问并写入该存储桶。如果连接成功，对话框将进入数据库审计日志设置的下一步。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI、位置或 ARN 做了任何更改，必须先禁用再重新启用审计日志。
> - 若要移除 TiDB Cloud 对你 Amazon S3 的访问权限，只需在 AWS 管理控制台中删除授予该集群的信任策略。

### 在 Google Cloud 上启用审计日志

要在 Google Cloud 上启用审计日志，请按照以下步骤操作：

#### 步骤 1. 创建 GCS 存储桶

在你组织拥有的 Google Cloud 账号中指定一个 Google Cloud Storage (GCS) 存储桶，作为 TiDB Cloud 写入审计日志的目标位置。

更多信息请参见 Google Cloud Storage 文档中的 [创建存储桶](https://cloud.google.com/storage/docs/creating-buckets)。

#### 步骤 2. 配置 GCS 访问权限

1. 获取你要为其启用审计日志的 TiDB 集群的 Google Cloud Service Account ID。

    1. 在 TiDB Cloud 控制台，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群的名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
    4. 在 **Database Audit Log Storage Configuration** 对话框中，找到 **Google Cloud Service Account ID** 部分，记录下 **Service Account ID**，以备后用。

2. 在 [Google Cloud 控制台](https://console.cloud.google.com/) 中，进入 **IAM & Admin** > **Roles**，检查是否存在具备以下存储桶中对象写入权限的角色。

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

在 TiDB Cloud 控制台，返回你获取 Google Cloud Service Account ID 的 **Database Audit Log Storage Configuration** 对话框，然后按以下步骤操作：

1. 在 **Bucket URI** 字段，输入你的完整 GCS 存储桶名称。
2. 在 **Bucket Region** 字段，选择存储桶所在的 GCS 区域。
3. 点击 **Test Connection and Next**，验证 TiDB Cloud 是否可以访问并写入该存储桶。如果连接成功，对话框将进入数据库审计日志设置的下一步。

> **注意：**
>
> - 启用审计日志后，如果你对存储桶 URI 或位置做了任何更改，必须先禁用再重新启用审计日志。
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
        > - 审计功能需要持续向存储账户写入审计日志，因此 SAS token 必须有足够长的有效期。但有效期越长，token 泄漏的风险越高。为安全起见，建议每 6 到 12 个月更换一次 SAS token。
        > - 生成的 SAS token 无法撤销，因此需要谨慎设置其有效期。
        > - 请确保在 SAS token 过期前重新生成并更新 token，以保证审计日志的持续可用性。

    5. **Allowed protocols** 选择 **HTTPS only**，以确保安全访问。
    6. 点击 **Generate SAS token and URL**，然后复制显示的 **Blob SAS token** 以备后用。

#### 步骤 3. 启用审计日志

1. 在 TiDB Cloud 控制台，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 点击目标 TiDB Cloud Dedicated 集群的名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。
3. 在 **DB Audit Logging** 页面，点击右上角的 **Enable**。
4. 在 **Database Audit Log Storage Configuration** 对话框中，填写你在 [步骤 2. 配置 Azure Blob 访问权限](#step-2-configure-azure-blob-storage-access) 获取的 blob URL 和 SAS token：
    - 在 **Blob URL** 字段，输入存储审计日志的容器 URL。
    - 在 **SAS Token** 字段，输入访问该容器的 SAS token。
5. 点击 **Test Connection and Next**，验证 TiDB Cloud 是否可以访问并写入该容器。如果连接成功，对话框将进入数据库审计日志设置的下一步。

> **注意：**
>
> 启用审计日志后，如果你对 **Blob URL** 或 **SAS Token** 字段做了新的更改，必须禁用并重新启用审计日志。

## 配置数据库审计日志设置

为云服务提供商配置存储后，完成数据库审计日志设置步骤：

1. 设置日志文件轮转策略。

    你可以基于文件大小或时间间隔轮转审计日志文件。当任一条件满足时，TiDB Cloud 会生成新的审计日志文件。

    > **注意：**
    >
    > 基于时间间隔的日志文件轮转仅适用于 TiDB v8.5.2 及以上版本。如果你的 TiDB Cloud Dedicated 集群的 TiDB 版本早于 v8.5.2，则只能基于文件大小轮转审计日志文件。

2. 配置日志脱敏。

    默认启用日志脱敏。启用后，SQL 文本中的敏感信息会在审计日志中被替换为 `?`。

3. 点击 **Save and Enable** 以应用设置并启用审计日志。

> **注意：**
>
> 如果你禁用日志脱敏，写入云存储的审计日志文件可能包含敏感信息。由于存在潜在安全风险，不建议使用此配置。

## 指定审计过滤规则

启用审计日志后，必须指定审计过滤规则，以控制捕获和写入哪些用户访问事件到审计日志。如果未指定过滤规则，TiDB Cloud 不会记录任何日志。

要为集群指定审计过滤规则，请按以下步骤操作：

1. 在 **DB Audit Logging** 页面，点击 **Audit Filters** 区域的 **Add Filter Rule**，添加一条审计过滤规则。

2. 在 **Add Filter Rule** 对话框中，配置以下项：

    - **Filter Name**：输入过滤规则的名称。
    - **SQL User**：以 `<user>@<host>` 格式输入 SQL 用户。用户名和主机名可以使用 `%` 匹配零个或多个字符，或使用 `_` 匹配恰好一个字符。`@` 符号和 `<host>` 为可选项。
    - **Filter Events**：选择要记录的事件。支持的过滤事件，参见[审计过滤事件](#audit-filter-events)。

3. 点击 **Confirm** 添加过滤规则。

> **注意：**
>
> - 由于审计日志会消耗集群资源，指定过滤规则时请谨慎。为最小化资源使用，请尽可能指定过滤规则，将审计日志限制为特定用户和事件。

## 查看审计日志

默认情况下，TiDB Cloud 会将数据库审计日志文件存储在你的存储服务中，因此你需要从存储服务中访问审计日志。

> **注意：**
>
> 如果你已申请并选择将审计日志文件存储在 TiDB Cloud，可以在 **Database Audit Logging** 页面的 **Audit Log Access** 区域下载日志文件。

TiDB Cloud 审计日志为可读的文本文件，完整文件路径中包含集群 ID、节点 ID 和日志创建日期。

例如：`13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示集群 ID，`tidb-0` 表示节点 ID。

## 禁用审计日志

如果你不再需要对集群进行审计，请按以下步骤操作：

1. 在 TiDB Cloud 控制台中进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Dedicated 集群的名称。
2. 在左侧导航栏中，点击 **Settings** > **DB Audit Logging**。
3. 在 **Database Audit Logging** 区域中，点击 **Settings** 旁边的 **...**，然后点击 **Disable**。

> **注意：**
>
> 每当日志文件大小达到 10 MiB 时，日志文件会被推送到云存储桶。因此，禁用审计日志后，文件大小小于 10 MiB 的日志不会自动推送到云存储桶。如需获取此类日志文件，请联系 [PingCAP 支持](/tidb-cloud/tidb-cloud-support.md)。

## 审计过滤事件

下表展示了数据库审计日志中的所有事件类：

| Event class   | Description                                                                                      | Parent-class   |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| `CONNECTION`    | 记录所有与连接相关的操作，例如连接握手、连接、断开连接、连接重置和用户变更 | -             |
| `CONNECT`       | 记录所有连接握手操作                                          | `CONNECTION`    |
| `DISCONNECT`    | 记录所有断开连接操作                                                      | `CONNECTION`    |
| `CHANGE_USER`   | 记录所有变更用户的操作                                                          | `CONNECTION`    |
| `QUERY`         | 记录所有 SQL 语句操作，包括查询或修改数据时发生的错误  | -               |
| `TRANSACTION`   | 记录所有与事务相关的操作，例如 `BEGIN`、`COMMIT` 和 `ROLLBACK`         | `QUERY`         |
| `EXECUTE`       | 记录所有 `EXECUTE` 语句的操作                                                | `QUERY`         |
| `QUERY_DML`     | 记录所有 DML 语句的操作，包括 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 和 `LOAD DATA`    | `QUERY`     |
| `INSERT`        | 记录所有 `INSERT` 语句的操作                                                   | `QUERY_DML`   |
| `REPLACE`       | 记录所有 `REPLACE` 语句的操作                                                  | `QUERY_DML`   |
| `UPDATE`        | 记录所有 `UPDATE` 语句的操作                                                   | `QUERY_DML`   |
| `DELETE`        | 记录所有 `DELETE` 语句的操作                                                   | `QUERY_DML`   |
| `LOAD DATA`     | 记录所有 `LOAD DATA` 语句的操作                                                | `QUERY_DML`   |
| `SELECT`        | 记录所有 `SELECT` 语句的操作                                                   | `QUERY`       |
| `QUERY_DDL`     | 记录所有 DDL 语句的操作                                                        | `QUERY`       |
| `AUDIT`         | 记录所有与配置 TiDB Cloud 数据库审计相关的操作，包括设置系统变量和调用系统函数 | -                   |
| `AUDIT_FUNC_CALL` | 记录所有调用与 TiDB Cloud 数据库审计相关的系统函数的操作        | `AUDIT`       |
| `AUDIT_SET_SYS_VAR` | 记录所有设置系统变量的操作        | `AUDIT`       |

## 审计日志字段

对于审计日志中的每条数据库事件记录，TiDB Cloud 提供以下字段：

### 常规信息

所有类的审计日志都包含以下信息：

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| `ID`            | 操作审计记录的唯一标识符。                        |
| `TIME`          | 审计记录的时间戳。                                                             |
| `EVENT`         | 审计记录的事件类。多个事件类型以逗号（`,`）分隔。     |
| `USER`          | 执行该操作的用户名。                                                              |
| `ROLES`         | 用户在执行该操作时的角色。                                            |
| `CONNECTION_ID` | 用户连接的标识符。                                                       |
| `TABLES`        | 操作期间访问的表。                                              |
| `STATUS_CODE`   | 审计记录的状态码。`1` 表示成功，`0` 表示失败。                |
| `KEYSPACE_NAME` | 审计记录的 keyspace 名称。                                                        |
| `REASON`        | 审计记录的错误信息。仅在操作期间发生错误时记录。|

### SQL 语句信息

当事件类为 `QUERY` 或 `QUERY` 的子类时，审计日志包含以下信息：

| 字段          | 描述                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `CURRENT_DB`     | 当前数据库的名称。                                                                             |
| `SQL_TEXT`       | 已执行的 SQL 语句。如果启用了审计日志脱敏，则记录脱敏后的 SQL 语句。     |
| `EXECUTE_PARAMS` | `EXECUTE` 语句的参数。仅当事件类包含 `EXECUTE` 且禁用脱敏时记录。 |
| `AFFECTED_ROWS`  | SQL 语句影响的行数。仅当事件类包含 `QUERY_DML` 时记录。  |

### 连接信息

当事件类为 `CONNECTION` 或 `CONNECTION` 的子类时，审计日志包含以下信息：

| 字段           | 描述                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `CURRENT_DB`      | 当前数据库的名称。当事件类包含 DISCONNECT 时，不记录此信息。 |
| `CONNECTION_TYPE` | 连接类型，包括 Socket、UnixSocket 和 SSL/TLS。                                 |
| `PID`             | 当前连接的进程 ID。                                                          |
| `SERVER_VERSION`  | 所连接 TiDB 服务器的当前版本。                                                  |
| `SSL_VERSION`     | 当前使用的 SSL 版本。                                                                 |
| `HOST_IP`         | 所连接 TiDB 服务器的当前 IP 地址。                                               |
| `HOST_PORT`       | 所连接 TiDB 服务器的当前端口。                                                     |
| `CLIENT_IP`       | 客户端的当前 IP 地址。                                                              |
| `CLIENT_PORT`     | 客户端的当前端口。                                                                    |

> **注意：**
>
> 为了提高流量可见性，对于通过 AWS PrivateLink 建立的连接，`CLIENT_IP` 现在显示真实客户端 IP 地址，而不是负载均衡器 (LB) IP。当前，此功能处于 beta 阶段，仅在 AWS Region `Frankfurt (eu-central-1)` 可用。

### 审计操作信息

当事件类为 `AUDIT` 或 `AUDIT` 的子类时，审计日志包含以下信息：

| 字段          | 描述                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `AUDIT_OP_TARGET`| TiDB Cloud 数据库审计设置变更的目标对象。 |
| `AUDIT_OP_ARGS`  | TiDB Cloud 数据库审计设置变更中使用的参数。 |

## 审计日志限制

{{{ .dedicated }}} 不保证审计日志按时间顺序写入，这意味着你可能需要检查所有日志文件才能找到最新事件。要按时间顺序对日志进行排序，可以使用审计日志中的 `TIME` 字段。

## 旧版数据库审计日志参考

如果你当前仍依赖旧版审计日志插件，请参阅[数据库审计日志（旧版）](/tidb-cloud/tidb-cloud-auditing-legacy.md)。
