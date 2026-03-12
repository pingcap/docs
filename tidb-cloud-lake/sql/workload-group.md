---
title: Workload Group
---

Workload groups enable resource management and query concurrency control in Databend by allocating CPU, memory quotas and limiting concurrent queries for different user groups.

## How It Works

1. **Create workload groups** with specific resource quotas (CPU, memory, concurrency limits)
2. **Assign users** to workload groups using `ALTER USER`
3. **Query execution** automatically applies the workload group's resource limits based on the user

## Quick Example

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

## Command Reference

### Management
| Command | Description |
|---------|-------------|
| [CREATE WORKLOAD GROUP](create-workload-group.md) | Creates a new workload group with resource quotas |
| [ALTER WORKLOAD GROUP](alter-workload-group.md) | Modifies workload group configuration |
| [DROP WORKLOAD GROUP](drop-workload-group.md) | Removes a workload group |
| [RENAME WORKLOAD GROUP](rename-workload-group.md) | Renames a workload group |

### Information
| Command | Description |
|---------|-------------|
| [SHOW WORKLOAD GROUPS](show-workload-groups.md) | Lists all workload groups and their settings |

:::tip
Resource quotas are normalized across all workload groups in a warehouse. For example, if two groups have 60% and 40% CPU quotas, they get 60% and 40% of actual resources respectively.
:::
