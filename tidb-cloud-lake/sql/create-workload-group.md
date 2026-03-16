---
title: CREATE WORKLOAD GROUP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.743"/>

Creates a workload group with specified quota settings. Workload groups control resource allocation and query concurrency by binding to users. When a user submits queries, the workload group limits are applied based on the user's assigned group.

## Syntax

```sql
CREATE WORKLOAD GROUP [IF NOT EXISTS] <group_name>
[WITH cpu_quota = '<percentage>', query_timeout = '<duration>']
```

## Parameters

| Parameter              | Type     | Required | Default      | Description                                                                 |
|------------------------|----------|----------|--------------|-----------------------------------------------------------------------------|
| `cpu_quota`            | string   | No       | (unlimited)  | CPU resource quota as percentage string (e.g. `"20%"`)                      |
| `query_timeout`        | duration | No       | (unlimited)  | Query timeout duration (units: `s`/`sec`=seconds, `m`/`min`=minutes, `h`/`hour`=hours, `d`/`day`=days, `ms`=milliseconds, unitless=seconds) |
| `memory_quota`         | string or integer   | No       | (unlimited)  | Maximum memory usage limit for workload group (percentage or absolute value) |
| `max_concurrency`      | integer  | No       | (unlimited)  | Maximum concurrency number for workload group                               |
| `query_queued_timeout` | duration | No       | (unlimited)  | Maximum queuing wait time when workload group exceeds max concurrency (units: `s`/`sec`=seconds, `m`/`min`=minutes, `h`/`hour`=hours, `d`/`day`=days, `ms`=milliseconds, unitless=seconds)      |

## Examples

### Basic Example

```sql
-- Create workload groups
CREATE WORKLOAD GROUP IF NOT EXISTS interactive_queries 
WITH cpu_quota = '30%', memory_quota = '20%', max_concurrency = 2;

CREATE WORKLOAD GROUP IF NOT EXISTS batch_processing 
WITH cpu_quota = '70%', memory_quota = '80%', max_concurrency = 10;
```

### User Assignment

Users must be assigned to workload groups to enable resource limiting. When users execute queries, the system applies the workload group's restrictions automatically.

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

## Resource Quota Normalization

### Quota Limits
- Each workload group's `cpu_quota` and `memory_quota` can be set up to `100%` (1.0)
- The total sum of all quotas across workload groups can exceed 100%
- Actual resource allocation is **normalized** based on relative proportions

### How Quota Normalization Works

Resources are allocated proportionally based on each group's quota relative to the total:

```
Actual Allocation = (Group Quota) / (Sum of All Group Quotas) × 100%
```

**Example 1: Total quotas = 100%**
- Group A: 30% quota → Gets 30% of resources (30/100)
- Group B: 70% quota → Gets 70% of resources (70/100)

**Example 2: Total quotas > 100%**
- Group A: 60% quota → Gets 40% of resources (60/150)
- Group B: 90% quota → Gets 60% of resources (90/150)
- Total quotas: 150%

**Example 3: Total quotas < 100%**
- Group A: 20% quota → Gets 67% of resources (20/30)
- Group B: 10% quota → Gets 33% of resources (10/30)
- Total quotas: 30%

**Special Case:** When only one workload group exists, it gets 100% of warehouse resources regardless of its configured quota.
