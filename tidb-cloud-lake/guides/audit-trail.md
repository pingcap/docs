---
title: 审计追踪
summary: "{{{ .lake }}} system history tables 会自动捕获数据库活动的详细记录，为合规性和安全监控提供完整的审计追踪。"
---

# 审计追踪

{{{ .lake }}} system history tables 会自动捕获数据库活动的详细记录，为合规性和安全监控提供完整的审计追踪。

支持对以下用户活动进行审计：

- **Query execution** - 完整的 SQL 执行审计追踪（`query_history`）
- **Data access** - 数据库对象访问和修改（`access_history`）
- **Authentication** - 登录尝试和会话跟踪（`login_history`）

## 可用的审计表 {#available-audit-tables}

{{{ .lake }}} 提供了三个 system history tables，用于捕获数据库活动的不同方面：

| Table | Purpose | Key Use Cases |
|-------|---------|---------------|
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md) | 完整的 SQL 执行审计追踪 | 性能监控、安全审计、合规报告 |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md) | 数据库对象访问和修改 | 数据血缘跟踪、合规审计、变更管理 |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md) | 身份验证尝试和会话 | 安全监控、失败登录检测、访问模式分析 |

## 审计使用场景和示例 {#audit-use-cases-examples}

### 安全监控 {#security-monitoring}

**监控失败的登录尝试**

跟踪身份验证失败事件，以识别潜在的安全威胁和未授权的访问尝试。

```sql
-- Check for failed login attempts (security audit)
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
ORDER BY event_time DESC;
```

示例输出：

```
event_time: 2025-06-03 06:07:32.512021
user_name: root1
client_ip: 127.0.0.1:62050
error_message: UnknownUser. Code: 2201, Text = User 'root1'@'%' does not exist.
```

### 合规报告 {#compliance-reporting}

**跟踪数据库模式变更**

监控 DDL 操作，以满足合规和变更管理要求。

```sql
-- Audit DDL operations (compliance tracking)
SELECT query_id, query_start, user_name, object_modified_by_ddl
FROM system_history.access_history
WHERE object_modified_by_ddl != '[]'
ORDER BY query_start DESC;
```

`CREATE TABLE` 操作示例：

```
query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
query_start: 2025-06-12 03:31:19.042128
user_name: root
object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create"}]
```

**审计数据访问模式**

跟踪谁在何时访问了哪些数据，以满足合规和数据治理要求。

```sql
-- Track data access for compliance
SELECT query_id, query_start, user_name, base_objects_accessed
FROM system_history.access_history
WHERE base_objects_accessed != '[]'
ORDER BY query_start DESC;
```

### 运维监控 {#operational-monitoring}

**完整的查询执行审计**

维护所有 SQL 操作的完整记录，包括用户和时间信息。

```sql
-- Complete query audit with user and timing information
SELECT query_id, sql_user, query_text, query_start_time, query_duration_ms, client_address
FROM system_history.query_history
WHERE event_date >= TODAY() - INTERVAL 7 DAY
ORDER BY query_start_time DESC;
```

示例输出：

```
query_id: 4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43
sql_user: root
query_text: SELECT * FROM t
query_start_time: 2025-06-12 03:31:35.041725
query_duration_ms: 94
client_address: 127.0.0.1
```

<!--
For detailed information about each audit table and their specific fields, see the [System History Tables](/tidb-cloud-lake/sql/system-history-tables.md) reference documentation.
-->