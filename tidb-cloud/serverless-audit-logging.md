---
title: TiDB Cloud Serverless Database Audit Logging
summary: Learn about how to audit a serverless cluster in TiDB Cloud.
---

# TiDB Cloud Serverless Database Audit Logging

TiDB Cloud Serverless provides you with a database audit logging feature to record a history of user access details (such as any SQL statements executed) in logs.

To assess the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to conduct a periodic analysis of the database audit logs.

The audit logging feature is disabled by default. To audit a cluster, you need to enable the audit logging.

## Enable audit logging

To enable the audit logging for a TiDB Cloud Serverless cluster, using the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md)

```shell
ticloud serverless audit-log enable --cluster-id <cluster-id>
```

To disable the audit logging for a TiDB Cloud Serverless cluster, using the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md)

```shell
ticloud serverless audit-log disable --cluster-id <cluster-id>
```

## Configure audit logging

### Redacted

TiDB Cloud redacts sensitive data in the audit logs by default. For example, the following SQL statement:

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

is redacted as follows:

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

If you want to disable the redaction, using the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md)

```shell
ticloud serverless audit-log config --cluster-id <cluster-id> --unredacted
```

### Rotation

TiDB Cloud will start to generate a new audit log file when one of the following conditions is met:

- The audit log file reaches 100 MB.
- The time interval reaches 1 hour. Note that the audit log files may not be generated exactly at the time interval of 1 hour, it may be delayed for a few minutes depending on the underlying schedule.

## View audit logs

TiDB Cloud audit logs are readable text files named `YYYY-MM-DD-<uuid>.log`. You can download the audit logs by [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) to view them.

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-day <start-day> --end-day <end-day>
```

> **Note:**
> TiDB Cloud will save your audit logs for xx days.

## Audit logging limitations

- The audit logging is only available for TiDB Cloud CLI, the support of TiDB Cloud Console will be available soon.
- The audit logging can only be generated in the TiDB Cloud, the support of external storage will be available soon.
- TiDB Cloud does not guarantee the sequential order of the audit logs, which means you might have to review all log files to see the latest events. To order the logs, you can use the `TIMESTAMP` field in the event records.