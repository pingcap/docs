---
title: CREATE WORKLOAD GROUP
summary: 使用指定的配额设置创建 workload group。workload group 通过绑定到用户来控制资源分配和查询并发。当用户提交查询时，系统会根据该用户所属的组应用 workload group 的限制。
---

# CREATE WORKLOAD GROUP

使用指定的配额设置创建 workload group。workload group 通过绑定到用户来控制资源分配和查询并发。当用户提交查询时，系统会根据该用户所属的组应用 workload group 的限制。

## 语法 {#syntax}

```sql
CREATE WORKLOAD GROUP [IF NOT EXISTS] <group_name>
[WITH cpu_quota = '<percentage>', query_timeout = '<duration>']
```

## 参数 {#parameters}

| 参数                   | 类型     | 必需 | 默认值       | 描述 |
|------------------------|----------|----------|--------------|-----------------------------------------------------------------------------|
| `cpu_quota`            | string   | 否       | （无限制）   | 以百分比字符串表示的 CPU 资源配额（例如 `"20%"`） |
| `query_timeout`        | duration | 否       | （无限制）   | 查询超时时长（单位：`s`/`sec`=秒，`m`/`min`=分钟，`h`/`hour`=小时，`d`/`day`=天，`ms`=毫秒，无单位=秒） |
| `memory_quota`         | string or integer   | 否       | （无限制）   | workload group 的最大内存使用限制（百分比或绝对值） |
| `max_concurrency`      | integer  | 否       | （无限制）   | workload group 的最大并发数 |
| `query_queued_timeout` | duration | 否       | （无限制）   | 当 workload group 超过最大并发时，排队等待的最长时间（单位：`s`/`sec`=秒，`m`/`min`=分钟，`h`/`hour`=小时，`d`/`day`=天，`ms`=毫秒，无单位=秒） |

## 示例 {#examples}

### 基本示例 {#basic-example}

```sql
-- Create workload groups
CREATE WORKLOAD GROUP IF NOT EXISTS interactive_queries
WITH cpu_quota = '30%', memory_quota = '20%', max_concurrency = 2;

CREATE WORKLOAD GROUP IF NOT EXISTS batch_processing
WITH cpu_quota = '70%', memory_quota = '80%', max_concurrency = 10;
```

### 用户分配 {#user-assignment}

必须先将用户分配到 workload group，才能启用资源限制。当用户执行查询时，系统会自动应用该 workload group 的限制。

```sql
-- Create role and grant permissions
CREATE ROLE analytics_role;
GRANT ALL ON *.* TO ROLE analytics_role;
CREATE USER analytics_user IDENTIFIED BY 'password123' WITH DEFAULT_ROLE = 'analytics_role';
GRANT ROLE analytics_role TO analytics_user;

-- Assign user to workload group
ALTER USER analytics_user WITH SET WORKLOAD GROUP = 'interactive_queries';

-- Reassign to different workload group
ALTER USER analytics_user WITH SET WORKLOAD GROUP = 'batch_processing';

-- Remove from workload group (user will use default unlimited resources)
ALTER USER analytics_user WITH UNSET WORKLOAD GROUP;

-- Check user's workload group
DESC USER analytics_user;
```

## 资源配额归一化 {#resource-quota-normalization}

### 配额限制 {#quota-limits}

- 每个 workload group 的 `cpu_quota` 和 `memory_quota` 最多可设置为 `100%`（1.0）
- 所有 workload group 的配额总和可以超过 100%
- 实际资源分配会根据相对比例进行**归一化**

### 配额归一化的工作方式 {#how-quota-normalization-works}

资源会根据每个组的配额占总配额的比例按比例分配：

```
实际分配 = （组配额）/（所有组配额之和）× 100%
```

**示例 1：总配额 = 100%**

- 组 A：30% 配额 → 获得 30% 的资源（30/100）
- 组 B：70% 配额 → 获得 70% 的资源（70/100）

**示例 2：总配额 > 100%**

- 组 A：60% 配额 → 获得 40% 的资源（60/150）
- 组 B：90% 配额 → 获得 60% 的资源（90/150）
- 总配额：150%

**示例 3：总配额 < 100%**

- 组 A：20% 配额 → 获得 67% 的资源（20/30）
- 组 B：10% 配额 → 获得 33% 的资源（10/30）
- 总配额：30%

**特殊情况：**当只存在一个 workload group 时，无论其配置的配额是多少，它都会获得计算集群 (Warehouse) 100% 的资源。