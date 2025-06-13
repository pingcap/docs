---
title: TiDB Cloud Serverless Database Audit Logging
summary: Learn about how to audit a serverless cluster in TiDB Cloud.
---

# TiDB Cloud Serverless Database Audit Logging (Beta)

TiDB Cloud Serverless provides you with a database audit logging feature to record a history of user access details (such as any SQL statements executed) in logs.

> **Note:**
>
> Currently, the database audit logging feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Serverless database audit logging" in the **Description** field and click **Submit**.

To assess the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to conduct a periodic analysis of the database audit logs.

The audit logging feature is disabled by default. To audit a cluster, you need to enable the audit logging.

## Enable audit logging

To enable audit logging for a TiDB Cloud Serverless cluster, use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md).

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

To disable audit logging for a TiDB Cloud Serverless cluster, use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md).

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

> **Note:**
>
> Only enabling audit logging will not generate audit logs. You need to configure filters to specify what events to log. See [Manage audit logging filter rules](#manage-audit-logging-filter-rules) for more details.

## Manage audit logging filter rules

To filter the audit logging, you need to create a filter rule to specify which events to log. You can use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-filter-create.md) to manage the filter rules.

The filter rule contains the following fields:

- `users`: A list of user names to filter audit events. You can use the wildcard `%` to match any user name.
- `filters`: A list of filter objects. Each filter object can contain the following fields:

  - `classes`: A list of event classes to filter audit events. For example, `["QUERY", "EXECUTE"]`.
  - `tables`: A list of table filters. See [Table filters](https://docs.pingcap.com/tidb/stable/table-filter/) for more details.
  - `statusCodes`: A list of status codes to filter audit events. 1 means success, 0 means failure.

The classes of events that can be filtered include:

- `CONNECTION`: Events related to client connection lifecycle
- `CONNECT`: Connection establishment events
- `DISCONNECT`: Connection termination events
- `CHANGE_USER`: User change events within a connection
- `QUERY`: General query events
- `TRANSACTION`: Transaction management events
- `EXECUTE`: Statement execution events
- `QUERY_DML`: Data manipulation language events
- `INSERT`: Row insertion events
- `REPLACE`: Row replacement events
- `UPDATE`: Row update events
- `DELETE`: Row deletion events
- `LOAD_DATA`: Bulk data loading events
- `SELECT`: Data selection events
- `QUERY_DDL`: Data definition language events
- `AUDIT`: Audit-specific events
- `AUDIT_SET_SYS_VAR`: System variable changes in auditing
- `AUDIT_FUNC_CALL`: Function call events in auditing
- `AUDIT_ENABLE`: Audit enabling events
- `AUDIT_DISABLE`: Audit disabling events

### Create a filter rule

To create a filter rule that filters all audit logs, you can run the following command:

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

To create a filter rule that filters ALL EXECUTE events, you can run the following command:

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["EXECUTE"]]}'
```

### Update a filter rule

To disable a filter rule, you can run the following command:

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --enabled=false
```

To update a filter rule, you can run the following command:

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

Note that you need to pass the complete `--rule` field when updating.

### Delete a filter rule

To delete a filter rule, you can run the following command:

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --name <rule-name>
```

## Configure audit logging

### Data redaction

TiDB Cloud Serverless redacts sensitive data in the audit logs by default. For example, the following SQL statement:

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

is redacted as follows:

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

If you want to disable redaction, use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md).

```shell
ticloud serverless audit-log config --cluster-id <cluster-id> --unredacted
```

### Rotation

TiDB Cloud Serverless generates a new audit log file when one of the following conditions is met:

- The audit log file reaches 100 MB.
- The time interval reaches 1 hour. Note that audit log file generation may be delayed for a few minutes depending on the underlying schedule.

> **Note:**
>
> The rotation cannot be configured at present. TiDB Cloud Serverless automatically rotates the audit log files based on the above conditions.

## Access audit logging

TiDB Cloud Serverless audit logs are stored as readable text files named `YYYY-MM-DD-<uuid>.log`.

Currently, audit logs are stored within TiDB Cloud for 365 days. After this period, logs are automatically deleted.

To view and download audit logs, use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-download.md):

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

> **Note:**
>
> Support for external storage options (such as AWS S3, Azure Blob Storage, and Google Cloud Storage) will be available in the future.

## Audit logging limitations

- Audit logging is only available via TiDB Cloud CLI; support for TiDB Cloud Console will be available soon.
- Audit logs can only be stored in TiDB Cloud at present; support for external storage will be available soon.
- TiDB Cloud Serverless does not guarantee the sequential order of the audit logs, which means you might have to review all log files to see the latest events. To order the logs, you can use the `TIME` field in the event records.
