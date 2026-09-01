---
title: Use Plan Replayer to Troubleshoot SQL Performance
summary: Learn how to generate a Plan Replayer file from your instance for troubleshooting SQL performance, and how to authorize TiDB Cloud Support to access it for a limited period.
---

# Use Plan Replayer to Troubleshoot SQL Performance

Plan Replayer helps you package the information required to investigate a SQL execution plan into a file. The file can include the TiDB version and configuration, session variables, SQL bindings, table schemas, table statistics, the output of `EXPLAIN` or `EXPLAIN ANALYZE`, and internal optimizer information.

When troubleshooting SQL performance issues on a TiDB Cloud Essential or Premium instance, you can use `PLAN REPLAYER DUMP` to generate a Plan Replayer file for a specific SQL statement and download the file from the returned URL. The Plan Replayer file is useful for investigating issues such as unexpected execution plans, plan regressions, inaccurate statistics, or problematic plans that occur only occasionally.

If you need assistance from TiDB Cloud Support to troubleshoot the SQL performance issue, you can temporarily authorize TiDB Cloud Support to access Plan Replayer files for a limited period.

> **Note:**
>
> Plan Replayer files do not contain actual table row data, but they can contain SQL text, table definitions, optimizer statistics, and other potentially sensitive information. Review the file contents and your organization's data-sharing requirements before authorizing Support access.

## Before you start

- Connect to the target TiDB Cloud Essential or Premium instance using a SQL client that supports Plan Replayer statements.
- Use an account with permission to execute the required SQL statements.
- Identify the SQL statement, SQL digest, or plan digest that you want to investigate.
- Remove or mask sensitive literals in SQL text where possible. Plan Replayer does not include table rows, but SQL text and schema names might still contain sensitive information.

## Generate a Plan Replayer file

This section describes how to generate a Plan Replayer file for a specific SQL statement.

### Generate a file for a statement

Run `PLAN REPLAYER DUMP` with the statement you want to investigate. Use `EXPLAIN` to capture the optimizer's estimated execution plan.

```sql
PLAN REPLAYER DUMP EXPLAIN
SELECT * FROM orders WHERE customer_id = 1001;
```

The statement returns a pre-signed S3 download URL in the `File_token` column. The URL is temporary. Save it securely and download the Plan Replayer ZIP file before it expires.

### Include runtime information

When the performance issue involves actual execution behavior, use `EXPLAIN ANALYZE` to include runtime execution information in addition to the execution plan.

```sql
PLAN REPLAYER DUMP EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 1001;
```

### Use historical statistics

If historical statistics are enabled and the performance issue occurred at a specific time, use `WITH STATS AS OF TIMESTAMP` to request the statistics available at that time. TiDB uses the latest historical statistics available before the specified timestamp.

```sql
PLAN REPLAYER DUMP WITH STATS AS OF TIMESTAMP
'2026-08-31 12:00:00'
EXPLAIN SELECT * FROM orders WHERE customer_id = 1001;
```

You can also provide a Unix timestamp if required for your investigation. If no historical statistics are available before the specified time, TiDB uses the latest available statistics and records the relevant error information in the package.

## Manage access from TiDB Cloud Support

Support access is controlled at the instance level. The authorization allows TiDB Cloud Support engineers to access generated Plan Replayer files for SQL performance troubleshooting during a limited period.

### Authorize TiDB Cloud Support

To authorize TiDB Cloud Support to temporarily access Plan Replayer files generated for SQL performance troubleshooting, take the following steps:

1. In the TiDB Cloud console, navigate to the Overview page of the target TiDB Cloud Essential or Premium instance.
2. In the left navigation pane, click **Settings** > **Security**.
3. On the **Security** page, click **Authorize** in the **SQL Plan Replayer Files Access Authorization** section.
4. Select an access duration that covers the expected troubleshooting window from the drop-down list.
5. Review the authorization statement and select the confirmation checkbox.
6. Click **Authorize** to grant temporary access.

Access starts immediately and is automatically revoked when the selected expiration time is reached.

### Extend the authorization period

If the authorization period is about to expire and the issue is still being investigated, go to the **Security** page of the target TiDB Cloud Essential or Premium instance, and then click **Extend Access** to update the expiration time.

The new expiration time takes effect after you confirm the update.

### Revoke access

When troubleshooting is complete, or whenever you no longer want TiDB Cloud Support to access the Plan Replayer files, go to the **Security** page of the target TiDB Cloud Essential or Premium instance, and then click **Revoke Access** and confirm the action.

Revocation takes effect immediately. Files associated with the diagnostic access flow might also be deleted according to the product's retention policy.

## Best practices

To help protect sensitive information, minimize unnecessary access, and improve support efficiency, follow these best practices:

- Generate the Plan Replayer file close to the time of the investigation.
- Authorize TiDB Cloud Support for the shortest practical period.
- Include the Plan Replayer file identifier in the related support ticket.
- Revoke access when the issue is resolved.

## Security and retention

Plan Replayer is designed to share optimizer and execution-plan context without exporting actual table rows. However, SQL text, object names, table definitions, configuration, bindings, and statistics can contain business-sensitive information. If you need to share the Plan Replayer file with TiDB Cloud Support, use the minimum necessary access duration and revoke access after the investigation.

Plan Replayer files are temporary diagnostic artifacts. TiDB might automatically remove generated files after their retention period. Generate a new file if the previous file has expired or is no longer available.

## Related documentation

[TiDB: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster](https://docs.pingcap.com/tidb/stable/sql-plan-replayer/)
