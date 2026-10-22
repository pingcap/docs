---
title: 系统历史表
summary: "{{{ .lake }}} 的系统历史表通过自动跟踪数据库活动，为合规、安全监控和性能分析提供 **Data Governance** 能力。"
---

# 系统历史表

{{{ .lake }}} 的系统历史表通过自动跟踪数据库活动，为合规、安全监控和性能分析提供 **Data Governance** 能力。

## 可用表 {#available-tables}

| 表 | 用途 | 关键使用场景 |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md)     | 完整的 SQL 执行审计轨迹 | 性能分析、合规跟踪、使用情况监控 |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md)   | 数据访问和修改日志 | 数据血缘、合规报告、变更管理 |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md)     | 用户身份验证跟踪 | 安全审计、失败登录监控、访问模式分析 |
| [profile_history](/tidb-cloud-lake/sql/system-history-profile-history.md) | 详细的查询执行配置（Profile） | 性能优化、资源规划、瓶颈识别 |
| [log_history](/tidb-cloud-lake/sql/system-history-log-history.md)         | 原始系统日志和事件 | 系统故障排查、错误分析、运维监控 |

## 权限 {#permissions}

**访问限制：**

- 仅允许 `SELECT` 和 `DROP` 操作
- 所有用户都禁止执行 ALTER 操作
- 所有权不可转移

**所需权限：**

要查询系统历史表，用户需要具备以下权限之一：

- `GRANT SELECT ON *.*`（全局访问）
- `GRANT SELECT ON system_history.*`（数据库访问）
- `GRANT SELECT ON system_history.table_name`（特定表访问）

**示例：**

```sql
-- Create audit role for compliance team
CREATE ROLE audit_team;
GRANT SELECT ON system_history.* TO ROLE audit_team;
CREATE USER compliance_officer IDENTIFIED BY 'secure_password' WITH DEFAULT_ROLE='audit_team';
GRANT ROLE audit_team TO USER compliance_officer;
```

## 配置 {#configuration}

### {{{ .lake }}} {#lake}

✅ **自动启用** - 所有系统历史表默认即可使用，无需任何配置。