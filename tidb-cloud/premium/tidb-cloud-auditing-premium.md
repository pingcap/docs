---
title: "{{{ .premium }}} 数据库审计日志"
summary: 了解如何在 {{{ .premium }}} 中审计实例。
---

# {{{ .premium }}} 数据库审计日志

TiDB Cloud 提供审计日志功能，用于记录数据库的用户访问活动，例如已执行的 SQL 语句。

为了评估组织中用户访问策略及其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能**默认处于禁用状态**。要审计一个 {{{ .premium }}} 实例，你必须先启用审计日志，然后配置审计过滤规则。

> **注意：**
>
> 由于审计日志会消耗实例资源，请谨慎评估是否需要对实例启用审计。

## 前提条件 {#prerequisites}

- 你正在使用 {{{ .premium }}} 实例。

    > **注意：**
    >
    > - {{{ .starter }}} 不支持数据库审计日志。
    > - 对于 {{{ .essential }}}，请参见 [{{{ .essential }}} 的数据库审计日志（Beta）](/tidb-cloud/essential-database-audit-logging.md)。
    > - 对于 {{{ .dedicated }}}，请参见 [{{{ .dedicated }}} 数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

- 你必须在组织中拥有 `Organization Owner` 角色。否则，你将无法在 TiDB Cloud 控制台中看到与数据库审计相关的选项。

## 启用审计日志 {#enable-audit-logging}

TiDB Cloud 支持将 {{{ .premium }}} 实例的审计日志记录到你的云存储服务中。在启用数据库审计日志之前，请先在实例所在的云服务提供商上配置你的云存储服务。

### 为 AWS 上的 TiDB 启用审计日志 {#enable-audit-logging-for-tidb-on-aws}

要为 AWS 启用审计日志，请执行以下步骤：

#### 第 1 步：创建 Amazon S3 bucket {#step-1-create-an-amazon-s3-bucket}

在你组织拥有的 AWS 账户中指定一个 Amazon S3 bucket，作为 TiDB Cloud 写入审计日志的目标位置。

> **注意：**
>
> 不要在 AWS S3 bucket 上启用 object lock。启用 object lock 会阻止 TiDB Cloud 将审计日志文件推送到 S3。

更多信息，请参见 AWS 用户指南中的 [Creating a general purpose bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。

#### 第 2 步：配置 Amazon S3 访问权限 {#step-2-configure-amazon-s3-access}

1. 获取你要启用审计日志的 {{{ .premium }}} 实例的 TiDB Cloud Account ID 和 External ID。

    1. 在 TiDB Cloud 控制台中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    2. 点击目标实例名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。

    3. 在 **DB Audit Logging** 页面右上角点击 **Enable**。

    4. 在 **Database Audit Log Storage Configuration** 对话框中，找到 **AWS IAM Policy Settings** 部分，并记录 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID** 以供后续使用。

2. 在 AWS Management Console 中，进入 **IAM** > **Access Management** > **Policies**，然后检查是否存在一个具有 `s3:PutObject` 只写权限的存储 bucket policy。

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

        在该模板中，`<Your S3 bucket ARN>` 是你的 S3 bucket 的 Amazon Resource Name (ARN)，即审计日志文件将被写入的目标 bucket。你可以进入 S3 bucket 的 **Properties** 标签页，并在 **Bucket Overview** 区域获取 ARN 值。在 `"Resource"` 字段中，你需要在 ARN 后添加 `/*`。例如，如果 ARN 是 `arn:aws:s3:::tidb-cloud-test`，则需要将 `"Resource"` 字段的值配置为 `"arn:aws:s3:::tidb-cloud-test/*"`。

3. 进入 **IAM** > **Access Management** > **Roles**，然后检查是否已存在一个角色，其信任实体与之前记录的 TiDB Cloud Account ID 和 External ID 对应。

    - 如果存在，记录匹配的角色以供后续使用。
    - 如果不存在，点击 **Create role**，选择 **Another AWS account** 作为信任实体类型，然后在 **Account ID** 字段中输入 TiDB Cloud Account ID 的值。接着，选择 **Require External ID** 选项，并在 **External ID** 字段中输入 TiDB Cloud External ID 的值。

4. 在 **IAM** > **Access Management** > **Roles** 中，点击上一步中的角色名称进入 **Summary** 页面，然后执行以下步骤：

    1. 在 **Permissions** 标签页下，检查之前记录的具有 `s3:PutObject` 只写权限的 policy 是否已附加到该角色。如果没有，选择 **Attach Policies**，搜索所需 policy，然后点击 **Attach Policy**。
    2. 返回 **Summary** 页面，并将 **Role ARN** 的值复制到剪贴板。

#### 第 3 步：启用审计日志 {#step-3-enable-audit-logging}

在 TiDB Cloud 控制台中，返回你获取 TiDB Cloud account ID 和 External ID 值时所在的 **Database Audit Log Storage Configuration** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入将写入审计日志文件的 S3 bucket 的 URI。
2. 在 **Bucket Region** 下拉列表中，选择 bucket 所在的 AWS 区域。
3. 在 **Role ARN** 字段中，填写你在 [第 2 步：配置 Amazon S3 访问权限](#step-2-configure-amazon-s3-access) 中复制的 Role ARN 值。
4. 点击 **Test Connection and Next**，验证 TiDB Cloud 是否可以访问并写入该 bucket。

    如果成功，将显示 **The connection is successful**。否则，请检查你的访问配置。

5. 点击 **Enable**，为该实例启用审计日志。

    TiDB Cloud 现已准备好将指定实例的审计日志写入你的 Amazon S3 bucket。

> **注意：**
>
> - 启用审计日志后，如果你对 bucket URI、位置或 ARN 做了任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 是否可以连接到该 bucket。然后，点击 **Enable** 以应用更改。
> - 若要移除 TiDB Cloud 对你的 Amazon S3 的访问权限，只需在 AWS Management Console 中删除授予该实例的 trust policy。

<CustomContent language="en,zh">

### 为 Alibaba Cloud 上的 TiDB 启用审计日志 {#enable-audit-logging-for-tidb-on-alibaba-cloud}

要为 Alibaba Cloud 上的 TiDB Cloud 启用数据库审计日志，请执行以下步骤：

#### 第 1 步：创建 OSS bucket {#step-1-create-an-oss-bucket}

在你组织拥有的 Alibaba Cloud 账户中创建一个 Object Storage Service (OSS) bucket，作为 TiDB Cloud 写入审计日志的目标位置。

更多信息，请参见 Alibaba Cloud Storage 文档中的 [Create a bucket](https://www.alibabacloud.com/help/en/oss/user-guide/create-a-bucket-4)。

#### 第 2 步：配置 OSS 访问权限 {#step-2-configure-oss-access}

1. 获取你要启用审计日志的 {{{ .premium }}} 实例的 Alibaba Cloud Service Account ID。

    1. 在 TiDB Cloud 控制台中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。
    2. 点击目标实例名称进入其概览页面，然后在左侧导航栏中点击 **Settings** > **DB Audit Logging**。
    3. 在 **DB Audit Logging** 页面右上角点击 **Enable**。
    4. 在 **Database Audit Log Storage Configuration** 对话框中，找到 **Alibaba Cloud RAM Policy Settings** 部分，并记录 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID** 以供后续使用。

2. 在 Alibaba Cloud 控制台中，进入 **RAM** > **Permissions** > **Policies**，然后检查是否已存在一个 policy，具有针对你的审计日志 OSS bucket 的 `oss:PutObject` 只写权限。

    - 如果存在，记录该 policy 名称以供后续使用。

    - 如果不存在，点击 **Create Policy**，并使用以下 policy 模板定义该 policy。

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": [
                "oss:PutObject"
            ],
            "Resource": "acs:oss:*:*:<Your-Bucket-Name>/*"
            }
        ]
        }
        ```

    将 `<Your-Bucket-Name>` 替换为 TiDB Cloud 将写入审计日志的 OSS bucket 名称。例如，如果你的 bucket 名称是 `auditlog-bucket`，则使用：`"Resource": "acs:oss:*:*:auditlog-bucket/*"`。

3. 在 Alibaba Cloud 控制台中，进入 **RAM** > **Identities** > **Roles**，然后检查是否已存在一个角色，其 **trusted entity** 与你之前记录的 TiDB Cloud Account ID 和 External ID 相匹配。

    - 如果存在，记录该角色名称以供后续使用。

    - 如果不存在，点击 **Create Role**，并按以下步骤操作。

        1. 在角色创建页面，点击 **Switch to Policy Editor**。
        2. 在 **Principal** 下，选择 **Cloud Account**，并在字段中输入 **TiDB Cloud Account Id**。
        3. 在 **Action** 下，从下拉列表中选择 **sts:AssumeRole**。
        4. 点击 **Add condition**，然后按如下方式配置条件：
            - 将 **Key** 设置为 ``sts:ExternalId``。
            - 将 **Operator** 设置为 ``StringEquals``。
            - 将 **Value** 设置为 **TiDB Cloud External ID**。
        5. 点击 **OK** 打开 **Create Role** 对话框。
        6. 在 **Role Name** 字段中输入角色名称，然后点击 **OK** 创建角色。

4. 创建角色后，进入 **Permissions** 标签页并点击 **Grant Permission**。

    在对话框中，配置以下设置：

    - 对于 **Resource Scope**，选择 **Account**。
    - 在 **Policy** 字段中，选择之前创建的 OSS 写入 policy。
    - 点击 **Grant Permissions**。

5. 复制 **Role ARN**（例如：`acs:ram::<Your-Account-ID>:role/tidb-cloud-audit-role`）以供后续使用。

#### Step 3. 启用审计日志 {#step-3-enable-audit-logging}

在 TiDB Cloud 控制台中，返回到你获取 TiDB Cloud account ID 时所在的 **Database Audit Log Storage Configuration** 对话框，然后执行以下步骤：

1. 在 **Bucket URI** 字段中，输入你的 OSS bucket 的 URI。例如，`oss://tidb-cloud-audit-log`。
2. 在 **Bucket Region** 字段中，选择 bucket 所在的 Alibaba Cloud 区域（建议与 {{{ .premium }}} 实例所在区域保持一致）。
3. 在 **Role ARN** 字段中，粘贴在[步骤 2. 配置 OSS 访问](#step-2-configure-oss-access)中复制的 Role ARN 值。
4. 点击 **Test Connection** 以验证 TiDB Cloud 是否可以访问并写入 OSS bucket。

    - 如果成功，将显示 **The connection is successful**。
    - 如果失败，请检查 OSS bucket 权限、RAM role 配置和 policy。

5. 点击 **Enable** 以为该实例启用审计日志。

    TiDB Cloud 现已准备好将指定实例的审计日志写入你的 OSS bucket。

> **Note:**
>
> - 启用审计日志后，如果你对 bucket URI 或位置进行了任何新的更改，必须再次点击 **Test Connection** 以验证 TiDB Cloud 能够连接到该 bucket。然后，点击 **Enable** 以应用更改。
> - 若要移除 TiDB Cloud 对你的 OSS bucket 的访问权限，请在 Alibaba Cloud 控制台中删除授予该实例的 trust policy。

</CustomContent>

## 指定审计过滤规则 {#specify-auditing-filter-rules}

启用审计日志后，你必须指定审计过滤规则，以控制要捕获并写入审计日志的用户访问事件。如果未指定过滤规则，TiDB Cloud 不会记录任何内容。

要为实例指定审计过滤规则，请执行以下步骤：

1. 在 **DB Audit Logging** 页面中，点击 **Log Filter Rules** 部分中的 **Add Filter Rule** 以添加审计过滤规则。

    你一次只能添加一条审计规则。每条规则指定一个用户表达式、数据库表达式、表表达式和访问类型。你可以添加多条审计规则以满足你的审计需求。

2. 在 **Log Filter Rules** 部分中，点击 **>** 以展开并查看你已添加的审计规则列表。

> **Note:**
>
> - 过滤规则是正则表达式，并且区分大小写。如果你使用通配规则 `.*`，则会记录该实例中的所有用户、数据库或表事件。
> - 由于审计日志会消耗实例资源，因此在指定过滤规则时请谨慎。为尽量减少资源消耗，建议尽可能通过过滤规则将审计日志的范围限制为特定数据库对象、用户和操作。

## 查看审计日志 {#view-audit-logs}

默认情况下，TiDB Cloud 会将数据库审计日志文件存储在你的存储服务中，因此你需要从你的存储服务中读取审计日志信息。

TiDB Cloud 审计日志是可读的文本文件，其完整文件名中包含实例 ID、内部 ID 和日志创建日期。

例如，`13796619446086334065/tidb-5m5z34/tidb-audit-2022-04-21T18-16-29.529.log`。在此示例中，`13796619446086334065` 表示实例 ID，`tidb-5m5z34` 表示内部 ID。

## 禁用审计日志 {#disable-audit-logging}

如果你不再希望对某个实例进行审计，请进入该实例页面，点击 **Settings** > **Audit Settings**，然后将右上角的审计设置切换为 **Disable**。

> **Note:**
>
> 每当日志文件大小达到 10 MiB 时，该日志文件就会被推送到云存储 bucket。因此，在禁用审计日志后，大小小于 10 MiB 的日志文件不会自动推送到云存储 bucket。若要获取这种情况下的日志文件，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 审计日志字段 {#audit-logging-fields}

对于审计日志中的每条数据库事件记录，TiDB Cloud 提供以下字段。

### 通用信息 {#general-information}

所有审计日志记录都包含以下字段：

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| `ID`            | 审计记录的唯一标识符。 |
| `EVENT`         | 审计记录的事件类别。多个事件类别以逗号（`,`）分隔。  |
| `USER`          | 执行该操作的用户名称。                                             |
| `ROLES`         | 用户在执行该操作时被分配的角色。                                  |
| `CONNECTION_ID` | 用户连接的标识符。                                                      |
| `TABLES`        | 操作期间访问的表。                                              |
| `STATUS_CODE`   | 操作的状态码。`1` 表示成功，`0` 表示失败。           |
| `REASON`        | 操作的错误消息。仅在发生错误时记录。 |

### SQL 语句信息 {#sql-statement-information}

当事件类别为 `QUERY` 或 `QUERY` 的子类时，审计日志包含以下字段：

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `CURRENT_DB`     | 当前数据库的名称。                                                                             |
| `SQL_TEXT`       | 已执行的 SQL 语句。如果启用了审计日志脱敏，则记录脱敏后的语句。     |
| `EXECUTE_PARAMS` | 传递给 `EXECUTE` 语句的参数。仅当事件类别包含 `EXECUTE` 且未启用脱敏时记录。 |
| `AFFECTED_ROWS`  | SQL 语句影响的行数。仅当事件类别包含 `QUERY_DML` 时记录。  |

### 连接信息 {#connection-information}

当事件类别为 `CONNECTION` 或 `CONNECTION` 的子类时，审计日志包含以下字段：

| Field           | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `CURRENT_DB`      | 当前数据库的名称。当事件类别包含 `DISCONNECT` 时不记录。  |
| `CONNECTION_TYPE` | 连接类型，例如 Socket、UnixSocket 或 SSL/TLS。                          |
| `PID`             | 当前连接的进程 ID。                                                    |
| `SERVER_VERSION`  | 已连接的 TiDB server 的版本。                                                  |
| `SSL_VERSION`     | 正在使用的 SSL 版本。                                                                 |
| `HOST_IP`         | 已连接的 TiDB server 的 IP 地址。                                               |
| `HOST_PORT`       | 已连接的 TiDB server 的端口。                                                     |
| `CLIENT_IP`       | 客户端的 IP 地址。                                                              |
| `CLIENT_PORT`     | 客户端的端口。                                                                    |

> **Note:**
>
> 为了提高流量可见性，对于通过 AWS PrivateLink 建立的连接，`CLIENT_IP` 显示实际客户端 IP 地址，而不是负载均衡器 IP。此功能目前为 beta，仅在 AWS 区域 `Frankfurt (eu-central-1)` 中可用。

### 审计操作信息 {#audit-operation-information}

当事件类别为 `AUDIT` 或 `AUDIT` 的子类时，审计日志包含以下字段：

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `AUDIT_OP_TARGET`| TiDB Cloud 数据库审计设置变更的目标对象。 |
| `AUDIT_OP_ARGS`  | TiDB Cloud 数据库审计设置变更中使用的参数。 |

## 审计日志限制 {#audit-logging-limitations}

{{{ .premium }}} 不保证审计日志按时间顺序写入。要查找最新事件，你可能需要查看所有日志文件。若要按时间顺序对日志进行排序，请使用每条审计记录中的 `TIME` 字段。