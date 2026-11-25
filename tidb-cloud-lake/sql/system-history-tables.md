---
title: System History Tables
summary: "{{{ .lake }}}'s system history tables provide Data Governance capabilities by automatically tracking database activities for compliance, security monitoring, and performance analysis."
---

# System History Tables

{{{ .lake }}}'s system history tables provide **Data Governance** capabilities by automatically tracking database activities for compliance, security monitoring, and performance analysis.

## Available Tables

| Table                                 | Purpose                            | Key Use Cases                                                          |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md)     | Complete SQL execution audit trail | Performance analysis, compliance tracking, usage monitoring            |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md)   | Data access and modification logs  | Data lineage, compliance reporting, change management                  |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md)     | User authentication tracking       | Security auditing, failed login monitoring, access pattern analysis    |
| [profile_history](/tidb-cloud-lake/sql/system-history-profile-history.md) | Detailed query execution profiles  | Performance optimization, resource planning, bottleneck identification |
| [log_history](/tidb-cloud-lake/sql/system-history-log-history.md)         | Raw system logs and events         | System troubleshooting, error analysis, operational monitoring         |

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

### {{{ .lake }}}

✅ **Automatically enabled** - All system history tables are ready to use without any configuration.
