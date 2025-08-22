---
title: TiDB Cloud Serverless 数据库审计日志
summary: 了解如何在 TiDB Cloud 中对 TiDB Cloud Serverless 集群进行审计。
---

# TiDB Cloud Serverless 数据库审计日志（Beta）

TiDB Cloud Serverless 为你提供了数据库审计日志功能，用于在日志中记录用户访问的详细历史（如执行的所有 SQL 语句）。

> **Note:**
>
> 目前，数据库审计日志功能仅支持按需申请。若需申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写 “Apply for TiDB Cloud Serverless database audit logging”，并点击 **Submit**。

为了评估你所在组织的用户访问策略及其他信息安全措施的有效性，定期分析数据库审计日志是一项安全最佳实践。

审计日志功能默认处于关闭状态。若需对集群进行审计，你需要为其启用审计日志。

## 启用审计日志

要为 TiDB Cloud Serverless 集群启用审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

要为 TiDB Cloud Serverless 集群禁用审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

> **Note:**
>
> 仅启用审计日志功能不会生成审计日志。你还需要配置过滤器以指定需要记录的事件。更多信息，参见 [管理审计日志过滤规则](#manage-audit-logging-filter-rules)。

## 管理审计日志过滤规则

要对审计日志进行过滤，你需要创建过滤规则以指定需要记录哪些事件。你可以使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-filter-create.md) 管理过滤规则。

过滤规则包含以下字段：

- `users`：用于过滤审计事件的用户名列表。你可以使用通配符 `%` 匹配任意用户名。
- `filters`：过滤对象的列表。每个过滤对象可以包含以下字段：

    - `classes`：用于过滤审计事件的事件类别列表。例如，`["QUERY", "EXECUTE"]`。
    - `tables`：表过滤器列表。更多信息，参见 [Table filters]。
    - `statusCodes`：用于过滤审计事件的状态码列表。`1` 表示成功，`0` 表示失败。

以下是数据库审计日志中所有事件类别的汇总：

| Event Class   | Description                                                                                      | Parent-class   |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| CONNECTION    | 记录所有与连接相关的操作，如握手、连接、断开连接、连接重置和切换用户 | -             |
| CONNECT       | 记录所有连接握手操作                                          | CONNECTION    |
| DISCONNECT    | 记录所有断开连接的操作                                                      | CONNECTION    |
| CHANGE_USER   | 记录所有切换用户的操作                                                          | CONNECTION    |
| QUERY         | 记录所有 SQL 语句的操作，包括所有查询和数据修改的错误  | -             |
| TRANSACTION   | 记录所有与事务相关的操作，如 `BEGIN`、`COMMIT` 和 `ROLLBACK`               | QUERY         |
| EXECUTE       | 记录所有 `EXECUTE` 语句的操作                                                  | QUERY         |
| QUERY_DML     | 记录所有 DML 语句的操作，包括 `INSERT`、`REPLACE`、`UPDATE`、`DELETE` 和 `LOAD DATA` | QUERY     |
| INSERT        | 记录所有 `INSERT` 语句的操作                                                   | QUERY_DML     |
| REPLACE       | 记录所有 `REPLACE` 语句的操作                                                  | QUERY_DML     |
| UPDATE        | 记录所有 `UPDATE` 语句的操作                                                   | QUERY_DML     |
| DELETE        | 记录所有 `DELETE` 语句的操作                                                   | QUERY_DML     |
| LOAD DATA     | 记录所有 `LOAD DATA` 语句的操作                                                | QUERY_DML     |
| SELECT        | 记录所有 `SELECT` 语句的操作                                                   | QUERY         |
| QUERY_DDL          | 记录所有 DDL 语句的操作                                                      | QUERY               |
| AUDIT              | 记录所有与 TiDB 数据库审计设置相关的操作，包括设置系统变量和调用系统函数 | -                   |
| AUDIT_FUNC_CALL    | 记录所有与 TiDB 数据库审计相关的系统函数调用操作               | AUDIT               |

### 创建过滤规则

要创建捕获所有审计日志的过滤规则，请运行以下命令：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

要创建过滤所有 EXECUTE 事件的过滤规则，请运行以下命令：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["EXECUTE"]]}'
```

### 更新过滤规则

要禁用某个过滤规则，请运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --enabled=false
```

要更新某个过滤规则，请运行以下命令：

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

注意，更新时需要传递完整的 `--rule` 字段。

### 删除过滤规则

要删除某个过滤规则，请运行以下命令：

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --name <rule-name>
```

## 配置审计日志

### 数据脱敏

TiDB Cloud Serverless 默认会对审计日志中的敏感数据进行脱敏。以下 SQL 语句为例：

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

脱敏后如下所示：

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

如果你希望关闭脱敏功能，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md)。

```shell
ticloud serverless audit-log config --cluster-id <cluster-id> --unredacted
```

### 日志文件轮转

当满足以下任一条件时，TiDB Cloud Serverless 会生成新的审计日志文件：

- 当前日志文件大小达到 100 MiB。
- 距离上一次日志生成已过去 1 小时。根据内部调度机制，日志生成可能会延迟几分钟。

> **Note:**
>
> 目前，日志文件轮转设置不可配置。TiDB Cloud Serverless 会根据上述条件自动轮转审计日志文件。

## 访问审计日志

TiDB Cloud Serverless 审计日志以可读文本文件的形式存储，文件名为 `YYYY-MM-DD-<index>.log`。

目前，审计日志会在 TiDB Cloud 内部保存 365 天。超过此期限后，日志会被自动删除。

> **Note:**
>
> 如果你需要将审计日志保存到外部存储（如 AWS S3、Azure Blob Storage 和 Google Cloud Storage），请联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

要查看和下载审计日志，请使用 [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-download.md)：

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- `start-date`：你希望下载的审计日志的起始日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。
- `end-date`：你希望下载的审计日志的结束日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。

> **Note:**
>
> TiDB Cloud Serverless 不保证审计日志的顺序性。名为 `YYYY-MM-DD-<index>.log` 的日志文件可能包含前几天的审计日志。
> 如果你希望获取某一天（如 2025 年 1 月 1 日）的所有日志，通常指定 `--start-date 2025-01-01` 和 `--end-date 2025-01-02` 即可。但在极端情况下，你可能需要下载所有日志文件并根据 `TIME` 字段进行排序。

## 审计日志字段

对于审计日志中的每条数据库事件记录，TiDB 提供了以下字段：

### 通用信息

所有类别的审计日志都包含以下信息：

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| ID            | 标识某次操作审计记录的唯一标识符                        |
| TIME          | 审计记录的时间戳                        |
| EVENT         | 审计记录的事件类别。多个事件类型以逗号（`,`）分隔        |
| USER          | 审计记录的用户名                                                              |
| ROLES         | 操作时用户的角色                                            |
| CONNECTION_ID | 用户连接的标识符                                                       |
| TABLES        | 与本次审计记录相关的访问表                                              |
| STATUS_CODE   | 审计记录的状态码。`1` 表示成功，`0` 表示失败。                       |
| KEYSPACE_NAME | 审计记录的 keyspace 名称。 |
| SERVERLESS_TENANT_ID           | 集群所属的 serverless tenant ID。 |
| SERVERLESS_TSERVERLESS_PROJECT_ID         | 集群所属的 serverless 项目 ID。 |
| SERVERLESS_CLUSTER_ID          | 审计记录所属的 serverless 集群 ID。 |
| REASON        | 审计记录的错误信息。仅在操作发生错误时记录。 |

### SQL 语句信息

当事件类别为 `QUERY` 或其子类时，审计日志包含以下信息：

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| CURRENT_DB     | 当前数据库名称。                                                                              |
| SQL_TEXT       | 执行的 SQL 语句。如果启用了审计日志脱敏，则记录脱敏后的 SQL 语句。     |
| EXECUTE_PARAMS | `EXECUTE` 语句的参数。仅当事件类别包含 `EXECUTE` 且未启用脱敏时记录。 |
| AFFECTED_ROWS  | SQL 语句影响的行数。仅当事件类别包含 `QUERY_DML` 时记录。    |

### 连接信息

当事件类别为 `CONNECTION` 或其子类时，审计日志包含以下信息：

| Field           | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| CURRENT_DB      | 当前数据库名称。当事件类别包含 DISCONNECT 时不记录此信息。 |
| CONNECTION_TYPE | 连接类型，包括 Socket、UnixSocket 和 SSL/TLS。                                 |
| PID             | 当前连接的进程 ID。                                                          |
| SERVER_VERSION  | 当前连接的 TiDB 服务器版本。                                                  |
| SSL_VERSION     | 当前使用的 SSL 版本。                                                                 |
| HOST_IP         | 当前连接的 TiDB 服务器 IP 地址。                                              |
| HOST_PORT       | 当前连接的 TiDB 服务器端口。                                                     |
| CLIENT_IP       | 客户端的 IP 地址。                                                             |
| CLIENT_PORT     | 客户端的端口。                                                                    |

### 审计操作信息

当事件类别为 `AUDIT` 或其子类时，审计日志包含以下信息：

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| AUDIT_OP_TARGET| 与 TiDB 数据库审计设置相关的对象。 |
| AUDIT_OP_ARGS  | 与 TiDB 数据库审计设置相关的参数。 |

## 审计日志限制

- 目前仅可通过 TiDB Cloud CLI 获取审计日志。
- 目前审计日志只能存储在 TiDB Cloud 内部。
- TiDB Cloud Serverless 不保证审计日志的顺序性，这意味着你可能需要查看所有日志文件以获取最新事件。若需按时间顺序排序日志，可以使用审计日志中的 `TIME` 字段。