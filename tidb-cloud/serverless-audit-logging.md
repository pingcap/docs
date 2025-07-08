---
title: TiDB Cloud Serverless 数据库审计日志
summary: 了解如何在 TiDB Cloud 中对 TiDB Cloud Serverless 集群进行审计。
---

# TiDB Cloud Serverless 数据库审计日志（Beta）

TiDB Cloud Serverless 为你提供了数据库审计日志功能，用于记录用户访问的历史详情（例如执行的任何 SQL 语句）到日志中。

> **Note:**
>
> 目前，数据库审计日志功能仅在请求后提供。若要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。接着，在 **Description** 字段中填写“申请 TiDB Cloud Serverless 数据库审计日志”，并点击 **Submit**。

为了评估你组织的用户访问策略和其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能默认未启用。若要对集群进行审计，你需要为其启用审计日志。

## 启用审计日志

要为 TiDB Cloud Serverless 集群启用审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

若要禁用 TiDB Cloud Serverless 集群的审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

> **Note:**
>
> 仅启用审计日志不会生成审计日志。你还需要配置过滤规则以指定哪些事件需要记录。更多信息请参见 [管理审计日志过滤规则](#manage-audit-logging-filter-rules)。

## 管理审计日志过滤规则

要过滤审计日志，你需要创建过滤规则，指定哪些事件需要记录。你可以使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-filter-create.md) 来管理过滤规则。

过滤规则包含以下字段：

- `users`: 用户名列表，用于过滤审计事件。可以使用通配符 `%` 来匹配任何用户名。
- `filters`: 过滤对象列表。每个过滤对象可以包含以下字段：

    - `classes`: 事件类别列表，用于过滤审计事件。例如，`["QUERY", "EXECUTE"]`。
    - `tables`: 表过滤列表。更多信息请参见 [Table filters]。
    - `statusCodes`: 状态码列表，用于过滤审计事件。`1` 表示成功，`0` 表示失败。

以下是数据库审计日志中所有事件类别的总结：

| Event Class   | 描述                                                                                          | Parent-class   |
|---------------|------------------------------------------------------------------------------------------------|----------------|
| CONNECTION    | 记录所有与连接相关的操作，如握手、连接、断开连接、连接重置和切换用户                         | -              |
| CONNECT       | 记录所有连接中的握手操作                                                                       | CONNECTION     |
| DISCONNECT    | 记录所有断开连接的操作                                                                         | CONNECTION     |
| CHANGE_USER   | 记录所有切换用户的操作                                                                         | CONNECTION     |
| QUERY         | 记录所有 SQL 语句的操作，包括查询和数据修改的所有错误                                              | -              |
| TRANSACTION   | 记录所有与事务相关的操作，如 `BEGIN`、`COMMIT` 和 `ROLLBACK`                                | QUERY          |
| EXECUTE       | 记录所有 `EXECUTE` 语句的操作                                                                  | QUERY          |
| QUERY_DML     | 记录所有 DML 语句的操作，包括 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 和 `LOAD DATA`             | QUERY          |
| INSERT        | 记录所有 `INSERT` 语句的操作                                                                   | QUERY_DML      |
| REPLACE       | 记录所有 `REPLACE` 语句的操作                                                                  | QUERY_DML      |
| UPDATE        | 记录所有 `UPDATE` 语句的操作                                                                   | QUERY_DML      |
| DELETE        | 记录所有 `DELETE` 语句的操作                                                                   | QUERY_DML      |
| LOAD DATA     | 记录所有 `LOAD DATA` 语句的操作                                                                | QUERY_DML      |
| SELECT        | 记录所有 `SELECT` 语句的操作                                                                   | QUERY          |
| QUERY_DDL     | 记录所有 DDL 语句的操作                                                                         | QUERY          |
| AUDIT         | 记录所有与设置 TiDB 数据库审计相关的操作，包括设置系统变量和调用系统函数                         | -              |
| AUDIT_FUNC_CALL | 记录所有调用与 TiDB 数据库审计相关的系统函数的操作                                              | AUDIT          |

### 创建过滤规则

要创建捕获所有审计日志的过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

要创建只过滤所有 `EXECUTE` 事件的过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["EXECUTE"]}]}'
```

### 更新过滤规则

要禁用某个过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --enabled=false
```

要更新过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

注意，在更新时需要传递完整的 `--rule` 字段。

### 删除过滤规则

要删除过滤规则，运行以下命令：

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --name <rule-name>
```

## 配置审计日志

### 数据脱敏

TiDB Cloud Serverless 默认会对审计日志中的敏感数据进行脱敏。例如，以下 SQL 语句：

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

会被脱敏为：

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

如果你想禁用脱敏功能，可以使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config --cluster-id <cluster-id> --unredacted
```

### 日志文件轮转

TiDB Cloud Serverless 在满足以下任一条件时会生成新的审计日志文件：

- 当前日志文件的大小达到 100 MiB。
- 自上次生成日志起已过去一小时。根据内部调度机制，日志生成可能会延迟几分钟。

> **Note:**
>
> 目前，日志文件轮转设置不可配置。TiDB Cloud Serverless 会根据上述条件自动轮转审计日志文件。

## 访问审计日志

TiDB Cloud Serverless 审计日志以名为 `YYYY-MM-DD-<index>.log` 的可读文本文件存储。

目前，审计日志在 TiDB Cloud 内存储期限为 365 天。超过此期限后，日志会自动删除。

> **Note:**
>
> 如果你需要将审计日志保存到外部存储（如 AWS S3、Azure Blob 存储和 Google Cloud Storage），请联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

要查看和下载审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-download.md)：

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- `start-date`: 你想下载的审计日志的起始日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。
- `end-date`: 你想下载的审计日志的结束日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。

> **Note:**
>
> TiDB Cloud Serverless 不保证审计日志的顺序性。名为 `YYYY-MM-DD-<index>.log` 的日志文件可能包含之前几天的审计日志。
> 如果你想获取某个特定日期（例如 2025 年 1 月 1 日）的所有日志，通常可以指定 `--start-date 2025-01-01` 和 `--end-date 2025-01-02`。但在极端情况下，你可能需要下载所有日志文件并按 `TIME` 字段排序。

## 审计日志字段

对于审计日志中的每个数据库事件记录，TiDB 提供以下字段：

### 通用信息

所有类别的审计日志都包含以下信息：

| 字段             | 描述                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| ID               | 标识操作审计记录的唯一标识符                                                               |
| TIME             | 审计记录的时间戳                                                                           |
| EVENT            | 审计记录的事件类别。多个事件类型用逗号（`,`）分隔                                              |
| USER             | 审计记录的用户名                                                                           |
| ROLES            | 操作时用户的角色                                                                           |
| CONNECTION_ID    | 用户连接的标识符                                                                           |
| TABLES           | 相关的访问表                                                                               |
| STATUS_CODE      | 审计记录的状态码。`1` 表示成功，`0` 表示失败。                                                 |
| KEYSPACE_NAME    | 审计记录的 keyspace 名称                                                                  |
| SERVERLESS_TENANT_ID           | 所属集群的无服务器租户 ID                                              |
| SERVERLESS_TSERVERLESS_PROJECT_ID         | 所属集群的无服务器项目 ID                                              |
| SERVERLESS_CLUSTER_ID          | 审计记录所属的无服务器集群 ID                                              |
| REASON           | 审计记录的错误信息。仅在操作发生错误时记录。                                                    |

### SQL 语句信息

当事件类别为 `QUERY` 或其子类时，审计日志包含以下信息：

| 字段             | 描述                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| CURRENT_DB       | 当前数据库的名称                                                                           |
| SQL_TEXT         | 执行的 SQL 语句。如果启用了审计日志脱敏，则记录脱敏后的 SQL 语句                                |
| EXECUTE_PARAMS   | `EXECUTE` 语句的参数。仅在事件类别包含 `EXECUTE` 且未启用脱敏时记录                                |
| AFFECTED_ROWS    | SQL 语句影响的行数。仅在事件类别包含 `QUERY_DML` 时记录                                              |

### 连接信息

当事件类别为 `CONNECTION` 或其子类时，审计日志包含以下信息：

| 字段             | 描述                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| CURRENT_DB       | 当前数据库的名称。若事件类别包含 DISCONNECT，则不记录此信息                                    |
| CONNECTION_TYPE  | 连接类型，包括 Socket、UnixSocket 和 SSL/TLS                                              |
| PID              | 当前连接的进程 ID                                                                           |
| SERVER_VERSION   | 连接的 TiDB 服务器的当前版本                                                                |
| SSL_VERSION      | 使用的 SSL 版本                                                                             |
| HOST_IP          | 连接的 TiDB 服务器的当前 IP 地址                                                               |
| HOST_PORT        | 连接的 TiDB 服务器的当前端口                                                                   |
| CLIENT_IP        | 客户端的当前 IP 地址                                                                           |
| CLIENT_PORT      | 客户端的当前端口                                                                             |

### 审计操作信息

当事件类别为 `AUDIT` 或其子类时，审计日志包含以下信息：

| 字段             | 描述                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| AUDIT_OP_TARGET  | 与 TiDB 数据库审计相关的设置对象                                                               |
| AUDIT_OP_ARGS    | 与 TiDB 数据库审计相关的设置参数                                                               |

## 审计日志的限制

- 目前，审计日志仅通过 TiDB Cloud CLI 提供。
- 审计日志目前只能存储在 TiDB Cloud 中。
- TiDB Cloud Serverless 不保证审计日志的顺序性，意味着你可能需要查看所有日志文件以获取最新事件。你可以通过 `TIME` 字段按时间排序审计日志。