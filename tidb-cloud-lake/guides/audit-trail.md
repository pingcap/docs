---
title: Audit Trail
summary: Databend system history tables automatically capture detailed records of database activities, providing a complete audit trail for compliance and security monitoring.
---

# Audit Trail

Databend system history tables automatically capture detailed records of database activities, providing a complete audit trail for compliance and security monitoring.

Allows the auditing of the user:
- **Query execution** - Complete SQL execution audit trail (`query_history`)
- **Data access** - Database object access and modifications (`access_history`)
- **Authentication** - Login attempts and session tracking (`login_history`)

## Available Audit Tables

Databend provides five system history tables that capture different aspects of database activity:

| Table | Purpose | Key Use Cases |
|-------|---------|---------------|
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md) | Complete SQL execution audit trail | Performance monitoring, security auditing, compliance reporting |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md) | Database object access and modifications | Data lineage tracking, compliance auditing, change management |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md) | Authentication attempts and sessions | Security monitoring, failed login detection, access pattern analysis |

## Audit Use Cases & Examples

### Security Monitoring

**Monitor Failed Login Attempts**

Track authentication failures to identify potential security threats and unauthorized access attempts.

```sql
-- Check for failed login attempts (security audit)
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
ORDER BY event_time DESC;
```

Example output:
```
event_time: 2025-06-03 06:07:32.512021
user_name: root1
client_ip: 127.0.0.1:62050
error_message: UnknownUser. Code: 2201, Text = User 'root1'@'%' does not exist.
```

### Compliance Reporting

**Track Database Schema Changes**

Monitor DDL operations for compliance and change management requirements.

```sql
-- Audit DDL operations (compliance tracking)
SELECT query_id, query_start, user_name, object_modified_by_ddl
FROM system_history.access_history
WHERE object_modified_by_ddl != '[]'
ORDER BY query_start DESC;
```

Example for `CREATE TABLE` operation:
```
query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
query_start: 2025-06-12 03:31:19.042128
user_name: root
object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create"}]
```

**Audit Data Access Patterns**

Track who accessed what data and when for compliance and data governance.

```sql
-- Track data access for compliance
SELECT query_id, query_start, user_name, base_objects_accessed
FROM system_history.access_history
WHERE base_objects_accessed != '[]'
ORDER BY query_start DESC;
```

### Operational Monitoring

**Complete Query Execution Audit**

Maintain comprehensive records of all SQL operations with user and timing information.

```sql
-- Complete query audit with user and timing information
SELECT query_id, sql_user, query_text, query_start_time, query_duration_ms, client_address
FROM system_history.query_history
WHERE event_date >= TODAY() - INTERVAL 7 DAY
ORDER BY query_start_time DESC;
```

Example output:
```
query_id: 4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43
sql_user: root
query_text: SELECT * FROM t
query_start_time: 2025-06-12 03:31:35.041725
query_duration_ms: 94
client_address: 127.0.0.1
```

For detailed information about each audit table and their specific fields, see the [System History Tables](/tidb-cloud-lake/sql/system-history-tables.md) reference documentation.
