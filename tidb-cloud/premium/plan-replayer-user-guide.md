# Use Plan Replayer to Troubleshoot SQL Performance

Plan Replayer helps you package the information required to investigate an SQL execution plan. In TiDB Cloud, you can generate a Plan Replayer file from your instance and temporarily authorize TiDB Cloud Support to access it when you need help troubleshooting SQL performance.

> **Important:** Plan Replayer files contain SQL text, table definitions, optimizer statistics, and related plan information. They do not contain actual table row data. Review the file contents and your organization's data-sharing requirements before authorizing Support access.

## Overview

Use Plan Replayer when you need to share enough optimizer context for a performance investigation without exporting the underlying table data. A Plan Replayer package can include the TiDB version and configuration, session variables, SQL bindings, table schemas, table statistics, the result of `EXPLAIN` or `EXPLAIN ANALYZE`, and internal optimizer information.

The package is useful for investigating issues such as an unexpected execution plan, a plan regression, inaccurate statistics, or an SQL statement whose problematic plan appears only occasionally.

## Before You Start

- Connect to the target TiDB Cloud instance with a SQL client that supports sending Plan Replayer statements.
- Use an account with permission to execute the required SQL statements.
- Identify the SQL statement, SQL digest, or plan digest that you want to investigate.
- Remove or mask sensitive literals in SQL text where possible. Plan Replayer does not include table rows, but SQL text and schema names may still be sensitive.

## Generate a Plan Replayer File

### Generate a file for a statement

Run `PLAN REPLAYER DUMP` with the statement you want to investigate. Use `EXPLAIN` to capture the optimizer's estimated plan.

```sql
PLAN REPLAYER DUMP EXPLAIN
SELECT * FROM orders WHERE customer_id = 1001;
```

The SQL result returns a pre-signed S3 download URL in the `File_token` column.The URL is temporary. Save it securely and download the Plan Replayer ZIP file before it expires.

### Include runtime information

When the issue involves actual execution behavior, use `EXPLAIN ANALYZE`. This includes runtime execution information in addition to the plan.

```sql
PLAN REPLAYER DUMP EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 1001;
```

### Use historical statistics

If historical statistics are enabled and the issue occurred at a particular time, request the statistics available at that time. TiDB uses the latest historical statistics before the specified timestamp.

```sql
PLAN REPLAYER DUMP WITH STATS AS OF TIMESTAMP
'2026-08-31 12:00:00'
EXPLAIN SELECT * FROM orders WHERE customer_id = 1001;
```

You can also provide a Unix timestamp when required by your investigation. If no historical statistics are available before the specified time, TiDB uses the latest available statistics and records the relevant error information in the package.

## Capture an Intermittent Plan

Use `PLAN REPLAYER CAPTURE` when the target SQL statement or problematic execution plan appears only occasionally and cannot be reproduced directly. Capture matches a SQL digest and a plan digest, then creates a Plan Replayer file when a matching execution is observed.

### Enable capture

```sql
SET GLOBAL tidb_enable_plan_replayer_capture = ON;
```

### Register a capture task

Register the SQL digest and plan digest that you want to capture.

```sql
PLAN REPLAYER CAPTURE
'sql_digest'
'plan_digest';
```

To capture any plan used by the target SQL digest, use `*` as the plan digest.

```sql
PLAN REPLAYER CAPTURE
'sql_digest'
'*';
```

### Check capture results

Query `mysql.plan_replayer_status` to view active capture tasks, generated file tokens, update times, and failure reasons.

```sql
SELECT * FROM mysql.plan_replayer_status;
```

When the target execution is captured successfully, use the returned token or file identifier as the reference for your Support request.

## Authorize TiDB Cloud Support

Support access is controlled at the instance level. The authorization allows TiDB Cloud Support engineers to access generated Plan Replayer diagnostic files for SQL performance troubleshooting during a temporary window.

1. Open the target instance in the TiDB Cloud console.
2. Go to **Security**.
3. Find **SQL Plan Replayer Files Access Authorization**.
4. Click **Authorize**.
5. Select an access duration from the dropdown list.
6. Review the authorization statement and select the confirmation checkbox.
7. Click **Authorize** to grant temporary access.

Choose an authorization period that covers the expected troubleshooting window. The access starts immediately and is automatically revoked when the selected expiration time is reached.

## Manage Support Access

### Extend the authorization period

If the issue is still being investigated, update the expiration time from the authorization section in **Settings > Security**. The new expiration time applies automatically after you confirm the update.

### Revoke access

When troubleshooting is complete, or whenever you no longer want Support to access the files, click **Revoke Access** and confirm the action. Revocation takes effect immediately. Files associated with the diagnostic access flow may also be deleted according to the product's retention policy.

> **Recommended workflow:** Generate the Plan Replayer file close to the time of the investigation, authorize Support for the shortest practical period, include the file identifier and the related support ticket, and revoke access when the issue is resolved.

## Security and Retention

Plan Replayer is designed to share optimizer and execution-plan context without exporting actual table rows. Nevertheless, SQL text, object names, table definitions, configuration, bindings, and statistics can contain business-sensitive information. Use the minimum necessary access duration and revoke access after the investigation.

Plan Replayer files are temporary diagnostic artifacts. TiDB may remove generated files automatically after their retention period. Generate a new file if the previous identifier has expired or is no longer available.

## Related Documentation

[TiDB: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster](https://docs.pingcap.com/tidb/stable/sql-plan-replayer/)
