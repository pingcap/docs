---
title: Worker 示例
summary: "在 {{{ .lake }}} 中使用 WORKER 命令管理 UDF 执行环境的完整示例。"
---

# Worker 示例

> **注意：**
>
> 于 v1.3.0 中引入。

本页提供了在 {{{ .lake }}} 中使用 WORKER 命令管理 UDF 执行环境的完整示例。

## 基本 Worker 生命周期 {#basic-worker-lifecycle}

### 1. 创建 Worker {#1-create-a-worker}

为名为 `read_env` 的 UDF 创建一个基础 worker：

```sql
CREATE WORKER read_env;
```

使用 `IF NOT EXISTS` 创建 worker 以避免报错：

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

使用自定义配置创建 worker：

```sql
CREATE WORKER read_env
    WITH size = 'small',
         auto_suspend = '300',
         auto_resume = 'true',
         max_cluster_count = '3',
         min_cluster_count = '1';
```

### 2. 列出 Workers {#2-list-workers}

查看当前租户中的所有 workers：

```sql
SHOW WORKERS;
```

### 3. 修改 Worker 设置 {#3-modify-worker-settings}

修改 worker 的 size 和 auto-suspend 设置：

```sql
ALTER WORKER read_env SET size = 'medium', auto_suspend = '600';
```

将特定选项重置为默认值：

```sql
ALTER WORKER read_env UNSET size, auto_suspend;
```

### 4. 管理 Worker 标签 {#4-manage-worker-tags}

添加标签以对 workers 进行分类：

```sql
ALTER WORKER read_env SET TAG purpose = 'sandbox', owner = 'ci';
```

在不再需要时移除标签：

```sql
ALTER WORKER read_env UNSET TAG purpose, owner;
```

### 5. 控制 Worker 状态 {#5-control-worker-state}

暂停 worker（下线其执行环境）：

```sql
ALTER WORKER read_env SUSPEND;
```

恢复已暂停的 worker：

```sql
ALTER WORKER read_env RESUME;
```

### 6. 删除 Worker {#6-remove-a-worker}

在不再需要时删除 worker：

```sql
DROP WORKER read_env;
```

安全地删除 worker（如果不存在则不报错）：

```sql
DROP WORKER IF EXISTS read_env;
```

## 高级示例 {#advanced-examples}

### 用于不同环境的 Worker {#worker-for-different-environments}

创建具有特定环境配置的 workers，然后分别为它们打标签：

```sql
-- Development worker
CREATE WORKER dev_processor WITH
    size = 'small',
    auto_suspend = '60',
    auto_resume = 'true',
    max_cluster_count = '1',
    min_cluster_count = '1';

ALTER WORKER dev_processor SET TAG environment = 'development', purpose = 'testing';

-- Production worker
CREATE WORKER prod_processor WITH
    size = 'large',
    auto_suspend = '1800',
    auto_resume = 'true',
    max_cluster_count = '5',
    min_cluster_count = '2';

ALTER WORKER prod_processor SET TAG environment = 'production', team = 'data-engineering';
```

### 动态 Worker 管理 {#dynamic-worker-management}

用于确保某个 worker 以特定配置存在的脚本：

```sql
-- Create worker if it doesn't exist
CREATE WORKER IF NOT EXISTS my_worker WITH
    size = 'small',
    auto_suspend = '300';

-- Update tags
ALTER WORKER my_worker SET TAG
    environment = 'staging',
    owner = 'ci';

-- Tune options later
ALTER WORKER my_worker SET auto_resume = 'true', max_cluster_count = '2';

-- Show current configuration
SHOW WORKERS;
```

## 最佳实践 {#best-practices}

### 1. 命名约定 {#1-naming-conventions}

- 使用能够表明 UDF 用途的描述性名称
- 包含环境后缀（例如 `_dev`、`_prod`、`_staging`）
- 在多团队环境中，考虑使用团队/项目前缀

### 2. 资源规格选择 {#2-resource-sizing}

- 在开发和测试阶段，从 `size='small'` 开始
- 对于不经常使用的 workers，使用 `auto_suspend` 以节省成本
- 根据预期负载设置合适的 `min_cluster_count`

### 3. 标签策略 {#3-tag-strategy}

- 使用标签进行成本分摊和资源跟踪
- 包含环境、团队和项目信息
- 为审计目的添加创建日期和所有者信息

### 4. 生命周期管理 {#4-lifecycle-management}

- 在幂等脚本中使用 `IF NOT EXISTS` 和 `IF EXISTS`
- 使用 `SHOW WORKERS` 监控 worker 使用情况
- 清理未使用的 workers 以降低成本

## 常见使用场景 {#common-use-cases}

### 1. UDF 开发 {#1-udf-development}

```sql
-- Create a worker for UDF development
CREATE WORKER dev_transform WITH
    size = 'small',
    auto_suspend = '60';

ALTER WORKER dev_transform SET TAG environment = 'development', purpose = 'testing';

-- After UDF is developed and tested
ALTER WORKER dev_transform SET
    size = 'medium',
    auto_suspend = '300';

ALTER WORKER dev_transform SET TAG purpose = 'production-ready';
```

### 2. 批处理 {#2-batch-processing}

```sql
-- Worker for nightly batch jobs
CREATE WORKER nightly_etl WITH
    size = 'large',
    auto_suspend = '3600',  -- Suspend after 1 hour of inactivity
    auto_resume = 'false';  -- Don't auto-resume (manual control)

ALTER WORKER nightly_etl SET TAG
    schedule = 'nightly',
    job_type = 'etl',
    criticality = 'high';
```

### 3. 多租户环境 {#3-multi-tenant-environments}

```sql
-- Workers for different teams
CREATE WORKER team_a_processor WITH
    size = 'medium';

ALTER WORKER team_a_processor SET TAG team = 'team-a', billing_code = 'TA-2024';

CREATE WORKER team_b_processor WITH
    size = 'small';

ALTER WORKER team_b_processor SET TAG team = 'team-b', billing_code = 'TB-2024';
```

## 故障排查 {#troubleshooting}

### Worker 无法启动 {#worker-not-starting}

如果 Worker 没有按预期启动，请执行以下检查：

1. 检查 UDF 是否存在并已正确配置
2. 验证环境变量是否已在云控制台中设置
3. 查看当前 Worker 元信息，并在需要时恢复它：

```sql
-- Inspect current worker metadata
SHOW WORKERS;

-- Resume the worker
ALTER WORKER my_worker RESUME;
```

### 权限问题 {#permission-issues}

请确保你具有所需的权限：

```sql
-- Check your privileges
SHOW GRANTS;
```

### 资源约束 {#resource-constraints}

如果遇到性能问题：

```sql
-- Increase worker size
ALTER WORKER my_worker SET size = 'large';

-- Adjust cluster counts
ALTER WORKER my_worker SET
    max_cluster_count = '5',
    min_cluster_count = '2';
```

## 相关主题 {#related-topics}

- [用户定义函数 (UDFs)](/tidb-cloud-lake/sql/user-defined-function.md) - 了解如何创建和使用 UDFs
- [计算集群管理](/tidb-cloud-lake/sql/warehouse-overview.md) - 管理用于执行查询的计算资源
- [工作负载组](/tidb-cloud-lake/sql/workload-group.md) - 控制资源分配和优先级