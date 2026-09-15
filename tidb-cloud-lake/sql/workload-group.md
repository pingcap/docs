---
title: Workload Group
summary: Workload group 通过为不同用户组分配 CPU、内存配额并限制并发查询数，在 {{{ .lake }}} 中实现资源管理和查询并发控制。
---

# Workload Group

Workload group 通过为不同用户组分配 CPU、内存配额并限制并发查询数，在 {{{ .lake }}} 中实现资源管理和查询并发控制。

## 工作原理 {#how-it-works}

1. 使用特定资源配额（CPU、内存、并发限制）**创建 workload group**
2. 使用 `ALTER USER` 将**用户分配**到 workload group
3. **查询执行**时会根据用户自动应用其 workload group 的资源限制

## 快速示例 {#quick-example}

```sql
-- Create workload group
CREATE WORKLOAD GROUP analytics WITH cpu_quota = '50%', memory_quota = '30%', max_concurrency = 5;

-- Create role and grant permissions
CREATE ROLE analyst_role;
GRANT ALL ON *.* TO ROLE analyst_role;
CREATE USER analyst IDENTIFIED BY 'password' WITH DEFAULT_ROLE = 'analyst_role';
GRANT ROLE analyst_role TO analyst;

-- Assign user to workload group
ALTER USER analyst WITH SET WORKLOAD GROUP = 'analytics';

-- Remove user from workload group (user will use default unlimited resources)
ALTER USER analyst WITH UNSET WORKLOAD GROUP;
```

## 命令参考 {#command-reference}

### 管理 {#management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE WORKLOAD GROUP](/tidb-cloud-lake/sql/create-workload-group.md) | 创建带有资源配额的新 workload group |
| [ALTER WORKLOAD GROUP](/tidb-cloud-lake/sql/alter-workload-group.md) | 修改 workload group 配置 |
| [DROP WORKLOAD GROUP](/tidb-cloud-lake/sql/drop-workload-group.md) | 删除 workload group |
| [RENAME WORKLOAD GROUP](/tidb-cloud-lake/sql/rename-workload-group.md) | 重命名 workload group |

### 信息 {#information}

| 命令 | 描述 |
|---------|-------------|
| [SHOW WORKLOAD GROUPS](/tidb-cloud-lake/sql/show-workload-groups.md) | 列出所有 workload group 及其设置 |

> **提示：**
>
> 资源配额会在同一个计算集群 (Warehouse) 中的所有 workload group 之间进行归一化。例如，如果两个组的 CPU 配额分别为 60% 和 40%，则它们将分别获得实际资源的 60% 和 40%。