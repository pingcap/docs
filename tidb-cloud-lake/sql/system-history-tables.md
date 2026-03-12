---
title: System History Tables
---

import EEFeature from '@site/src/components/EEFeature';
import DetailsWrap from '@site/src/components/DetailsWrap';

<EEFeature featureName='SYSTEM HISTORY'/>

# System History Tables

Databend's system history tables provide **Data Governance** capabilities by automatically tracking database activities for compliance, security monitoring, and performance analysis.

## Available Tables

| Table                                 | Purpose                            | Key Use Cases                                                          |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| [query_history](query-history.md)     | Complete SQL execution audit trail | Performance analysis, compliance tracking, usage monitoring            |
| [access_history](access-history.md)   | Data access and modification logs  | Data lineage, compliance reporting, change management                  |
| [login_history](login-history.md)     | User authentication tracking       | Security auditing, failed login monitoring, access pattern analysis    |
| [profile_history](profile-history.md) | Detailed query execution profiles  | Performance optimization, resource planning, bottleneck identification |
| [log_history](log-history.md)         | Raw system logs and events         | System troubleshooting, error analysis, operational monitoring         |

## Permissions

**Access Restrictions:**

- Only `SELECT` and `DROP` operations are allowed
- ALTER operations are prohibited for all users
- Ownership cannot be transferred

**Required Permissions:**
To query system history tables, users need one of:

- `GRANT SELECT ON *.*` (global access)
- `GRANT SELECT ON system_history.*` (database access)
- `GRANT SELECT ON system_history.table_name` (table-specific access)

**Example:**

```sql
-- Create audit role for compliance team
CREATE ROLE audit_team;
GRANT SELECT ON system_history.* TO ROLE audit_team;
CREATE USER compliance_officer IDENTIFIED BY 'secure_password' WITH DEFAULT_ROLE='audit_team';
GRANT ROLE audit_team TO USER compliance_officer;
```

## Configuration

### Databend Cloud

✅ **Automatically enabled** - All system history tables are ready to use without any configuration.

### Self-Hosted Databend

<DetailsWrap>
<details open>
<summary>📝 **Manual configuration required** - Click to expand configuration details</summary>

#### Minimal Configuration

To enable system history tables, you must configure all 5 tables in your `databend-query.toml`:

```toml
[log.history]
on = true

# All 5 tables must be configured to enable history logging
# retention is optional (default: 168 hours = 7 days)
[[log.history.tables]]
table_name = "query_history"
retention = 168  # Optional: 7 days (default)

[[log.history.tables]]
table_name = "login_history"
retention = 168  # Optional: 7 days (default)

[[log.history.tables]]
table_name = "access_history"
retention = 168  # Optional: 7 days (default)

[[log.history.tables]]
table_name = "profile_history"
retention = 168  # Optional: 7 days (default)

[[log.history.tables]]
table_name = "log_history"
retention = 168  # Optional: 7 days (default)
```

#### Custom Storage (Optional)

By default, history tables use your main database storage. To use separate S3 storage:

```toml
[log.history]
on = true
storage_on = true

[log.history.storage]
type = "s3"

[log.history.storage.s3]
bucket = "your-history-bucket"
root = "history_tables"
endpoint_url = "https://s3.amazonaws.com"
access_key_id = "your-access-key"
secret_access_key = "your-secret-key"


[[log.history.tables]]
table_name = "query_history"

[[log.history.tables]]
table_name = "profile_history"

[[log.history.tables]]
table_name = "login_history"

[[log.history.tables]]
table_name = "access_history"
```

> ⚠️ **Note:** When changing storage configuration, existing history tables will be dropped and recreated.

</details>
</DetailsWrap>

For complete configuration options, see [Query Configuration: [log.history] Section](/guides/self-hosted/references/node-config/query-config#loghistory-section).
