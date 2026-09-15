---
title: 故障排查
summary: 本页介绍如何对 TiDB Cloud Lake 中的常见问题进行故障排查。
---

# 故障排查

使用 `system_history` 表诊断慢查询、错误、资源使用情况和登录问题。使用 `profile_history` 进行按操作符的执行分析（CPU 时间、I/O、spill、输出行数）。所有表都按租户隔离。

## 表 {#tables}

### system_history.query_history {#system-history-query-history}

完整的 SQL 执行审计轨迹。每个查询都会生成包含开始/结束状态的记录。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| log_type | TINYINT | 查询状态：1=Start，2=Finish，3=Error，4=Aborted，5=Closed |
| log_type_name | VARCHAR | 字符串名称："Start"、"Finish"、"Error"、"Aborted"、"Closed" |
| handler_type | VARCHAR | 使用的协议（例如 `HTTPQuery`、`MySQL`） |
| tenant_id | VARCHAR | 租户标识符 |
| cluster_id | VARCHAR | 集群标识符 |
| node_id | VARCHAR | 节点标识符 |
| sql_user | VARCHAR | 执行查询的用户 |
| sql_user_quota | VARCHAR | 用户配额信息 |
| sql_user_privileges | VARCHAR | 用户权限 |
| query_id | VARCHAR | 唯一查询标识符 |
| query_kind | VARCHAR | 查询类型（例如 `Query`、`Insert`、`CopyIntoTable`） |
| query_text | VARCHAR | 查询的 SQL 文本 |
| query_hash | VARCHAR | 查询文本的哈希值 |
| query_parameterized_hash | VARCHAR | 忽略字面量值后的哈希值 |
| event_date | DATE | 事件日期 |
| event_time | TIMESTAMP | 事件时间戳 |
| query_start_time | TIMESTAMP | 查询开始时间戳 |
| query_duration_ms | BIGINT | 总耗时（毫秒，包含排队和执行） |
| query_queued_duration_ms | BIGINT | 排队耗时（毫秒） |
| current_database | VARCHAR | 当前使用的数据库 |
| written_rows | BIGINT UNSIGNED | 写入的行数 |
| written_bytes | BIGINT UNSIGNED | 写入的字节数 |
| join_spilled_rows | BIGINT UNSIGNED | Join 期间 spill 的行数 |
| join_spilled_bytes | BIGINT UNSIGNED | Join 期间 spill 的字节数 |
| agg_spilled_rows | BIGINT UNSIGNED | 聚合期间 spill 的行数 |
| agg_spilled_bytes | BIGINT UNSIGNED | 聚合期间 spill 的字节数 |
| group_by_spilled_rows | BIGINT UNSIGNED | Group By 期间 spill 的行数 |
| group_by_spilled_bytes | BIGINT UNSIGNED | Group By 期间 spill 的字节数 |
| written_io_bytes | BIGINT UNSIGNED | 写入到 IO 的字节数 |
| written_io_bytes_cost_ms | BIGINT UNSIGNED | IO 写入耗时（毫秒） |
| scan_rows | BIGINT UNSIGNED | 扫描的行数 |
| scan_bytes | BIGINT UNSIGNED | 扫描的字节数 |
| scan_io_bytes | BIGINT UNSIGNED | 扫描期间读取的 IO 字节数 |
| scan_io_bytes_cost_ms | BIGINT UNSIGNED | IO 扫描耗时（毫秒） |
| scan_partitions | BIGINT UNSIGNED | 扫描的分区数 |
| total_partitions | BIGINT UNSIGNED | 涉及的分区总数 |
| result_rows | BIGINT UNSIGNED | 结果中的行数 |
| result_bytes | BIGINT UNSIGNED | 结果中的字节数 |
| bytes_from_remote_disk | BIGINT UNSIGNED | 从远程磁盘读取的字节数 |
| bytes_from_local_disk | BIGINT UNSIGNED | 从本地磁盘读取的字节数 |
| bytes_from_memory | BIGINT UNSIGNED | 从内存读取的字节数 |
| client_address | VARCHAR | 客户端地址 |
| user_agent | VARCHAR | 客户端 user agent |
| exception_code | INT | 异常代码（0 = 成功） |
| exception_text | VARCHAR | 异常消息 |
| server_version | VARCHAR | 服务器版本 |
| query_tag | VARCHAR | 查询标签 |
| has_profile | BOOLEAN | 查询是否具有执行 profile |
| peek_memory_usage | VARIANT | 峰值内存使用量（JSON） |
| session_id | VARCHAR | 会话标识符 |
| session_settings | VARCHAR | 会话设置 |

### system_history.profile_history {#system-history-profile-history}

每个查询的详细执行 profile。使用 `jq()` 提取按操作符统计的信息。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| timestamp | TIMESTAMP | 记录 profile 的时间 |
| query_id | VARCHAR | 查询 ID |
| profiles | VARIANT | 操作符的 JSON 数组，每个元素包含 `id`、`name`、`statistics[]` |
| statistics_desc | VARIANT | 描述统计信息格式的 JSON |

统计数组索引：`[0]`=OutputRows，`[1]`=OutputBytes，`[2]`=InputRows，`[3]`=InputBytes，`[4]`=CpuTime(ns)。

### system_history.log_history {#system-history-log-history}

来自所有 {{{ .lake }}} 节点和组件的原始日志条目。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| timestamp | TIMESTAMP | 日志条目的时间戳 |
| path | VARCHAR | 源文件路径和行号 |
| target | VARCHAR | 目标模块或组件 |
| log_level | VARCHAR | 日志等级（`INFO`、`ERROR`、`WARN` 等） |
| cluster_id | VARCHAR | 集群标识符 |
| node_id | VARCHAR | 节点标识符 |
| warehouse_id | VARCHAR | 计算集群 (Warehouse) 标识符 |
| query_id | VARCHAR | 关联的查询 ID |
| message | VARCHAR | 日志消息（纯文本） |
| fields | VARIANT | 附加字段（JSON） |
| batch_number | BIGINT | 内部使用 |

### system_history.access_history {#system-history-access-history}

数据血缘和访问控制审计。跟踪所有被访问或修改的对象。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| query_id | VARCHAR | 查询 ID |
| query_start | TIMESTAMP | 查询开始时间 |
| user_name | VARCHAR | 执行查询的用户 |
| base_objects_accessed | VARIANT | 被访问的对象（JSON 数组） |
| direct_objects_accessed | VARIANT | 预留供未来使用 |
| objects_modified | VARIANT | 被 DML 修改的对象（JSON 数组） |
| object_modified_by_ddl | VARIANT | 被 DDL 修改的对象（JSON 数组） |

JSON 对象字段：`object_domain`（Database/Table/Stage）、`object_name`、`columns[]`、`stage_type`、`operation_type`（Create/Alter/Drop/Undrop）、`properties`。

### system_history.login_history {#system-history-login-history}

所有登录尝试的身份验证审计轨迹。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| event_time | TIMESTAMP | 登录事件时间戳 |
| handler | VARCHAR | 协议（例如 `HTTP`、`MySQL`） |
| event_type | VARCHAR | `LoginSuccess` 或 `LoginFailed` |
| connection_uri | VARCHAR | 连接 URI |
| auth_type | VARCHAR | 身份验证方法（例如 Password） |
| user_name | VARCHAR | 尝试登录的用户 |
| client_ip | VARCHAR | 客户端 IP 地址 |
| user_agent | VARCHAR | 客户端用户代理 |
| session_id | VARCHAR | 会话 ID |
| node_id | VARCHAR | 节点 ID |
| error_message | VARCHAR | 失败时的错误消息 |

## 快速示例 {#quick-examples}

查找最近一小时内的慢查询（>5s）：

```sql
SELECT query_id, sql_user, query_duration_ms, query_text
FROM system_history.query_history
WHERE query_duration_ms > 5000
  AND event_time > now() - INTERVAL 1 HOUR
  AND log_type = 2
ORDER BY query_duration_ms DESC
LIMIT 20;
```

查找失败的查询：

```sql
SELECT query_id, sql_user, exception_code, exception_text, query_text
FROM system_history.query_history
WHERE exception_code != 0
  AND event_time > now() - INTERVAL 1 HOUR
ORDER BY event_time DESC;
```

检查登录失败：

```sql
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
  AND event_time > now() - INTERVAL 24 HOUR
ORDER BY event_time DESC;
```
