---
title: TiDB Cloud Essential 数据库审计日志（Beta）
summary: 了解如何在 TiDB Cloud 中对 TiDB Cloud Essential 集群进行审计。
aliases: ['/tidbcloud/serverless-audit-logging']
---

# TiDB Cloud Essential 数据库审计日志（Beta）

TiDB Cloud Essential 提供了审计日志功能，用于记录数据库的用户访问活动，例如执行的 SQL 语句。

> **注意：**
>
> 目前，数据库审计日志功能仅支持按需开通。如需申请该功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写“Apply for TiDB Cloud Essential database audit logging”，并点击 **Submit**。

为了评估你所在组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能**默认关闭**。如需对 TiDB 集群进行审计，需为其启用审计日志。

## 审计日志配置

### 数据脱敏

默认情况下，TiDB Cloud Essential 会对审计日志中的敏感数据进行脱敏。以下 SQL 语句为例：

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

脱敏后如下所示：

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

### 日志文件轮转

当满足以下任一条件时，TiDB Cloud Essential 会生成新的审计日志文件：

- 当前日志文件达到轮转大小（默认 100 MiB）。
- 距离上一次日志生成已过轮转间隔（默认一小时）。根据内部调度机制，日志生成可能会延迟几分钟。

## 审计日志存储位置

你可以将审计日志存储在以下位置：

- TiDB Cloud
- [Amazon S3](https://aws.amazon.com/s3/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [阿里云对象存储 OSS](https://www.alibabacloud.com/product/oss)

### TiDB Cloud

你可以将审计日志存储在 TiDB Cloud，并下载到本地。审计日志在 365 天后过期并被删除。如需更长的保留时间，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

### Amazon S3

如需将审计日志存储在 Amazon S3，你需要提供以下信息：

- URI: `s3://<bucket-name>/<folder-path>/`
- 访问凭证：选择以下任一方式：
    - 具有 `s3:PutObject` 权限的 [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)。
    - 具有 `s3:PutObject` 权限的 [role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)。仅托管在 AWS 上的集群支持使用 role ARN。

更多信息，参见 [配置 Amazon S3 访问](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

### Google Cloud Storage

如需将审计日志存储在 Google Cloud Storage，你需要提供以下信息：

- URI: `gs://<bucket-name>/<folder-path>/`
- 访问凭证：具有 `storage.objects.create` 和 `storage.objects.delete` 权限的 [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)。

更多信息，参见 [配置 GCS 访问](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)。

### Azure Blob Storage

如需将审计日志存储在 Azure Blob Storage，你需要提供以下信息：

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` 或 `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- 访问凭证：具有 `Container` 和 `Object` 资源 `Read` 和 `Write` 权限的 [SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。

更多信息，参见 [配置 Azure Blob Storage 访问](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。

### 阿里云 OSS

如需将审计日志存储在阿里云 OSS，你需要提供以下信息：

- URI: `oss://<bucket-name>/<folder-path>/`
- 访问凭证：具有 `oss:PutObject` 和 `oss:GetBucketInfo` 权限的 [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)，以允许将数据导出到 OSS bucket。

更多信息，参见 [配置阿里云对象存储 OSS 访问](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## 审计日志过滤规则

如需过滤审计日志，你需要创建过滤规则以指定哪些事件需要记录。

过滤规则包含以下字段：

- `users`：用于过滤审计事件的用户名列表。你可以使用通配符 `%` 匹配任意用户名。
- `filters`：过滤对象列表。每个过滤对象包含以下字段：

    - `classes`：用于过滤审计事件的事件类列表。例如，`["QUERY", "EXECUTE"]`。
    - `tables`：表过滤器列表。更多信息，参见 [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter/)。
    - `statusCodes`：用于过滤审计事件的状态码列表。`1` 表示成功，`0` 表示失败。

下表展示了数据库审计日志中的所有事件类：

| Event class   | 描述                                                                                      | 父类   |
|---------------|------------------------------------------------------------------------------------------|--------|
| `CONNECTION`    | 记录所有与连接相关的操作，如握手、连接、断开连接、重置连接和切换用户 | -      |
| `CONNECT`       | 记录所有连接握手操作                                          | `CONNECTION`    |
| `DISCONNECT`    | 记录所有断开连接操作                                         | `CONNECTION`    |
| `CHANGE_USER`   | 记录所有切换用户操作                                         | `CONNECTION`    |
| `QUERY`         | 记录所有 SQL 语句操作，包括所有查询和数据修改的错误  | -      |
| `TRANSACTION`   | 记录所有与事务相关的操作，如 `BEGIN`、`COMMIT` 和 `ROLLBACK`         | `QUERY`         |
| `EXECUTE`       | 记录所有 `EXECUTE` 语句的操作                                                | `QUERY`         |
| `QUERY_DML`     | 记录所有 DML 语句操作，包括 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 和 `LOAD DATA`    | `QUERY`     |
| `INSERT`        | 记录所有 `INSERT` 语句的操作                                                   | `QUERY_DML`   |
| `REPLACE`       | 记录所有 `REPLACE` 语句的操作                                                  | `QUERY_DML`   |
| `UPDATE`        | 记录所有 `UPDATE` 语句的操作                                                   | `QUERY_DML`   |
| `DELETE`        | 记录所有 `DELETE` 语句的操作                                                   | `QUERY_DML`   |
| `LOAD DATA`     | 记录所有 `LOAD DATA` 语句的操作                                                | `QUERY_DML`   |
| `SELECT`        | 记录所有 `SELECT` 语句的操作                                                   | `QUERY`       |
| `QUERY_DDL`     | 记录所有 DDL 语句的操作                                                        | `QUERY`       |
| `AUDIT`         | 记录所有与 TiDB 数据库审计设置相关的操作，包括设置系统变量和调用系统函数 | -                   |
| `AUDIT_FUNC_CALL` | 记录所有与 TiDB Cloud 数据库审计相关的系统函数调用操作        | `AUDIT`       |
| `AUDIT_SET_SYS_VAR` | 记录所有系统变量设置操作        | `AUDIT`       |

> **注意：**
>
> `AUDIT` 事件类及其子类始终会被记录在审计日志中，无法被过滤。

## 配置审计日志

你可以启用、编辑和禁用审计日志。

### 启用审计日志

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 为 TiDB Cloud Essential 集群启用审计日志。

> **注意：**
>
> 仅启用审计日志不会生成审计日志。你还必须配置过滤规则以指定需要记录的事件。更多信息，参见 [管理审计日志过滤规则](#manage-audit-logging-filter-rules)。

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，点击 **Enable**。

4. 选择审计日志的存储位置并填写所需信息。然后点击 **Test Connection and Next** 或 **Next**。关于可用存储位置的更多信息，参见 [审计日志存储位置](#audit-logging-locations)。

5. 在 **Database Audit Logging Settings** 对话框中，填写日志文件轮转和日志脱敏设置，然后点击 **Save**。

</div>

<div label="CLI">

以 Amazon S3 存储为例。如需启用审计日志并将日志存储在 Amazon S3，运行以下命令：

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-url> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

`--rotation-size-mib`、`--rotation-interval-minutes` 和 `--unredacted` 参数为可选项。如未指定，则使用默认值。
 
</div>
</SimpleTab>

### 编辑审计日志

启用后，你可以编辑 TiDB Cloud Essential 集群的审计日志配置。

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，点击 **Settings**。

4. 在 **Database Audit Logging Settings** 对话框中，更新日志文件轮转或日志脱敏设置，然后点击 **Save**。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 更新审计日志设置，运行以下命令：

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```
 
</div>
</SimpleTab>

### 禁用审计日志

你可以为 TiDB Cloud Essential 集群禁用审计日志。

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，点击右上角的 **...**，然后点击 **Disable**。

4. 在 **Disable DB Audit Logging** 对话框中，点击 **Disable**。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 禁用审计日志，运行以下命令：

```shell
ticloud serverless audit-log config update -c <cluster-id> --disabled=true
```
 
</div>
</SimpleTab>

## 管理审计日志过滤规则

你可以创建、编辑、禁用和删除审计日志过滤规则。

### 创建过滤规则

如需创建过滤规则，请定义你希望在审计日志中捕获的用户和事件。你可以根据需要指定用户、事件类、表和状态码。

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，点击 **Add Filter Rule**。

4. 在 **Add Filter Rule** 对话框中，填写 **Filter Name**、**SQL Users** 和 **Filter Rule** 字段，然后点击 **Confirm**。关于这些字段的更多信息，参见 [审计日志过滤规则](#audit-logging-filter-rules)。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 创建过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```
 
</div>
</SimpleTab>

### 编辑过滤规则

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，找到你要编辑的过滤规则，点击其所在行的 **...**，然后点击 **Edit**。

4. 在 **Edit Filter Rule** 对话框中，更新 **Filter Name** 或 **Filter Rule** 字段，然后点击 **Confirm**。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 编辑过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```
 
</div>
</SimpleTab>

### 禁用过滤规则

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，找到你要禁用的过滤规则，关闭开关以禁用该规则。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 禁用过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```
 
</div>
</SimpleTab>

### 删除过滤规则

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，找到你要删除的过滤规则并点击 **...**。

4. 点击 **Delete**，然后点击 **I understand. Delete it** 以确认删除。

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```
 
</div>
</SimpleTab>

## 通过 TiDB Cloud 存储访问审计日志

当你将审计日志存储在 TiDB Cloud 时，TiDB Cloud Essential 会将其保存为可读的文本文件，命名为 `YYYY-MM-DD-<index>.log`。你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 查看和下载这些文件。

> **注意：**
>
> - TiDB Cloud Essential 不保证审计日志的存储顺序。名为 `YYYY-MM-DD-<index>.log` 的日志文件可能包含更早日期的日志条目。
> - 如需获取某一天（如 2025 年 1 月 1 日）的所有日志，请设置 `--start-date 2025-01-01` 和 `--end-date 2025-01-02`。在某些情况下，你可能需要下载所有日志文件并根据 `TIME` 字段进行排序。

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **DB Audit Logging**。

3. 在 **DB Audit Logging** 页面，你可以在 **TiDB Cloud Storage** 下查看审计日志列表。

4. 如需下载审计日志，从列表中选择一个或多个日志，然后点击 **Download**。

</div>

<div label="CLI">

如需通过 TiDB Cloud CLI 下载审计日志，运行以下命令：

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- `start-date`：要下载的审计日志起始日期，格式为 `YYYY-MM-DD`，如 `2025-01-01`。
- `end-date`：要下载的审计日志结束日期，格式为 `YYYY-MM-DD`，如 `2025-01-01`。
 
</div>
</SimpleTab>

## 审计日志字段

对于审计日志中的每条数据库事件记录，TiDB Cloud 提供以下字段：

### 通用信息

所有类型的审计日志均包含以下信息：

| 字段         | 描述                                                                                   |
|---------------|---------------------------------------------------------------------------------------|
| `ID`            | 标识操作审计记录的唯一标识符。                        |
| `TIME`          | 审计记录的时间戳。                                                             |
| `EVENT`         | 审计记录的事件类。多个事件类型以逗号（`,`）分隔。     |
| `USER`          | 审计记录的用户名。                                                              |
| `ROLES`         | 操作时用户的角色。                                            |
| `CONNECTION_ID` | 用户连接的标识符。                                                       |
| `TABLES`        | 与该审计记录相关的访问表。                                              |
| `STATUS_CODE`   | 审计记录的状态码。`1` 表示成功，`0` 表示失败。                |
| `KEYSPACE_NAME` | 审计记录的 keyspace 名称。                                                        |
| `SERVERLESS_TENANT_ID`           | 集群所属的 serverless 租户 ID。                 |
| `SERVERLESS_PROJECT_ID`          | 集群所属的 serverless 项目 ID。                |
| `SERVERLESS_CLUSTER_ID`          | 审计记录所属的 serverless 集群 ID。           |
| `REASON`        | 审计记录的错误信息。仅在操作发生错误时记录。|

### SQL 语句信息

当事件类为 `QUERY` 或其子类时，审计日志包含以下信息：

| 字段          | 描述                                                                                                   |
|----------------|-------------------------------------------------------------------------------------------------------|
| `CURRENT_DB`     | 当前数据库名称。                                                                             |
| `SQL_TEXT`       | 执行的 SQL 语句。如果启用了审计日志脱敏，则记录脱敏后的 SQL 语句。     |
| `EXECUTE_PARAMS` | `EXECUTE` 语句的参数。仅当事件类包含 `EXECUTE` 且未启用脱敏时记录。 |
| `AFFECTED_ROWS`  | SQL 语句影响的行数。仅当事件类包含 `QUERY_DML` 时记录。  |

### 连接信息

当事件类为 `CONNECTION` 或其子类时，审计日志包含以下信息：

| 字段           | 描述                                                                                   |
|-----------------|---------------------------------------------------------------------------------------|
| `CURRENT_DB`      | 当前数据库名称。当事件类包含 DISCONNECT 时不记录该信息。 |
| `CONNECTION_TYPE` | 连接类型，包括 Socket、UnixSocket 和 SSL/TLS。                                 |
| `PID`             | 当前连接的进程 ID。                                                          |
| `SERVER_VERSION`  | 当前连接的 TiDB 服务器版本。                                                  |
| `SSL_VERSION`     | 当前使用的 SSL 版本。                                                                 |
| `HOST_IP`         | 当前连接的 TiDB 服务器 IP 地址。                                               |
| `HOST_PORT`       | 当前连接的 TiDB 服务器端口。                                                     |
| `CLIENT_IP`       | 当前客户端 IP 地址。                                                              |
| `CLIENT_PORT`     | 当前客户端端口。                                                                    |

> **注意：**
>
> 为提升流量可见性，`CLIENT_IP` 现已支持通过 AWS PrivateLink 连接时显示真实客户端 IP，而非负载均衡（LB）IP。该功能目前为 Beta，仅在 AWS 区域 `Frankfurt (eu-central-1)` 可用。

### 审计操作信息

当事件类为 `AUDIT` 或其子类时，审计日志包含以下信息：

| 字段          | 描述                                                                                                   |
|----------------|-------------------------------------------------------------------------------------------------------|
| `AUDIT_OP_TARGET`| 与 TiDB Cloud 数据库审计设置相关的对象。 |
| `AUDIT_OP_ARGS`  | 与 TiDB Cloud 数据库审计设置相关的参数。 |

## 审计日志限制

TiDB Cloud Essential 不保证审计日志的顺序，这意味着你可能需要检查所有日志文件以查找最新事件。如需按时间顺序排序日志，可以使用审计日志中的 `TIME` 字段。