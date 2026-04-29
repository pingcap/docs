---
title: Worker Examples
summary: "Comprehensive examples of using WORKER commands to manage UDF execution environments in {{{ .lake }}}."
---

# Worker Examples

> **Note:**
>
> Introduced in v1.3.0.

This page provides comprehensive examples of using WORKER commands to manage UDF execution environments in {{{ .lake }}}.

## Basic Worker Lifecycle

### 1. Create a Worker

Create a basic worker for a UDF named `read_env`:

```sql
CREATE WORKER read_env;
```

Create a worker with `IF NOT EXISTS` to avoid errors:

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

Create a worker with custom configuration:

```sql
CREATE WORKER read_env
    WITH size = 'small',
         auto_suspend = '300',
         auto_resume = 'true',
         max_cluster_count = '3',
         min_cluster_count = '1';
```

### 2. List Workers

View all workers in the current tenant:

```sql
SHOW WORKERS;
```

### 3. Modify Worker Settings

Change worker size and auto-suspend settings:

```sql
ALTER WORKER read_env SET size = 'medium', auto_suspend = '600';
```

Reset specific options to defaults:

```sql
ALTER WORKER read_env UNSET size, auto_suspend;
```

### 4. Manage Worker Tags

Add tags to categorize workers:

```sql
ALTER WORKER read_env SET TAG purpose = 'sandbox', owner = 'ci';
```

Remove tags when no longer needed:

```sql
ALTER WORKER read_env UNSET TAG purpose, owner;
```

### 5. Control Worker State

Suspend a worker (stop its execution environment):

```sql
ALTER WORKER read_env SUSPEND;
```

Resume a suspended worker:

```sql
ALTER WORKER read_env RESUME;
```

### 6. Remove a Worker

Remove a worker when no longer needed:

```sql
DROP WORKER read_env;
```

Safely remove a worker (no error if it doesn't exist):

```sql
DROP WORKER IF EXISTS read_env;
```

## Advanced Examples

### Worker for Different Environments

Create workers with environment-specific configurations, then tag them separately:

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

### Dynamic Worker Management

Script to ensure a worker exists with specific configuration:

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

## Best Practices

### 1. Naming Conventions

- Use descriptive names that indicate the UDF's purpose
- Include environment suffix (e.g., `_dev`, `_prod`, `_staging`)
- Consider team/project prefixes for multi-team environments

### 2. Resource Sizing

- Start with `size='small'` for development and testing
- Use `auto_suspend` to save costs for infrequently used workers
- Set appropriate `min_cluster_count` based on expected load

### 3. Tag Strategy

- Use tags for cost allocation and resource tracking
- Include environment, team, and project information
- Add creation date and owner for audit purposes

### 4. Lifecycle Management

- Use `IF NOT EXISTS` and `IF EXISTS` for idempotent scripts
- Monitor worker usage with `SHOW WORKERS`
- Clean up unused workers to reduce costs

## Common Use Cases

### 1. UDF Development

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

### 2. Batch Processing

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

### 3. Multi-tenant Environments

```sql
-- Workers for different teams
CREATE WORKER team_a_processor WITH
    size = 'medium';

ALTER WORKER team_a_processor SET TAG team = 'team-a', billing_code = 'TA-2024';

CREATE WORKER team_b_processor WITH
    size = 'small';

ALTER WORKER team_b_processor SET TAG team = 'team-b', billing_code = 'TB-2024';
```

## Troubleshooting

### Worker Not Starting

If a worker doesn't start as expected:

1. Check if the UDF exists and is properly configured
2. Verify environment variables are set in the cloud console
3. Review the current worker metadata and resume it if needed:

```sql
-- Inspect current worker metadata
SHOW WORKERS;

-- Resume the worker
ALTER WORKER my_worker RESUME;
```

### Permission Issues

Ensure you have the necessary privileges:

```sql
-- Check your privileges
SHOW GRANTS;
```

### Resource Constraints

If experiencing performance issues:

```sql
-- Increase worker size
ALTER WORKER my_worker SET size = 'large';

-- Adjust cluster counts
ALTER WORKER my_worker SET
    max_cluster_count = '5',
    min_cluster_count = '2';
```

## Related Topics

- [User-Defined Functions (UDFs)](/tidb-cloud-lake/sql/user-defined-function.md) - Learn about creating and using UDFs
- [Warehouse Management](/tidb-cloud-lake/sql/warehouse-overview.md) - Manage compute resources for query execution
- [Workload Groups](/tidb-cloud-lake/sql/workload-group.md) - Control resource allocation and priorities
