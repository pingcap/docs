---
title: TiDB Cloud Serverless Database Audit Logging
summary: Learn about how to audit a TiDB Cloud Serverless cluster in TiDB Cloud.
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
    - `statusCodes`: A list of status codes to filter audit events. `1` means success, `0` means failure.

Here is the summary of all event classes in database audit logging:

| Event Class   | Description                                                                                      | Parent-class   |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| CONNECTION    | Record all operations related to connections, such as handshaking, connections, disconnections, connection reset, and changing users | -             |
| CONNECT       | Record all operations of the handshaking in connections                                          | CONNECTION    |
| DISCONNECT    | Record all operations of the disconnections                                                      | CONNECTION    |
| CHANGE_USER   | Record all operations of changing users                                                          | CONNECTION    |
| QUERY         | Record all operations of SQL statements, including all errors about querying and modifying data  | -             |
| TRANSACTION   | Record all operations related to transactions, such as `BEGIN`, `COMMIT`, and `ROLLBACK`               | QUERY         |
| EXECUTE       | Record all operations of the `EXECUTE` statements                                                  | QUERY         |
| QUERY_DML     | Record all operations of the DML statements, including `INSERT`, `REPLACE`, `UPDATE`, `DELETE`, and `LOAD DATA` | QUERY     |
| INSERT        | Record all operations of the `INSERT` statements                                                   | QUERY_DML     |
| REPLACE       | Record all operations of the `REPLACE` statements                                                  | QUERY_DML     |
| UPDATE        | Record all operations of the `UPDATE` statements                                                   | QUERY_DML     |
| DELETE        | Record all operations of the `DELETE` statements                                                   | QUERY_DML     |
| LOAD DATA     | Record all operations of the `LOAD DATA` statements                                                | QUERY_DML     |
| SELECT        | Record all operations of the `SELECT` statements                                                   | QUERY         |
| QUERY_DDL          | Record all operations of the DDL statements                                                      | QUERY               |
| AUDIT              | Record all operations related to setting TiDB database auditing, including setting system variables and calling system functions | -                   |
| AUDIT_FUNC_CALL    | Record all operations of calling system functions related to TiDB database auditing               | AUDIT               |

### Create a filter rule

To create a filter rule that filters all audit logs, run the following command:

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

To create a filter rule that filters ALL EXECUTE events, run the following command:

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["EXECUTE"]]}'
```

### Update a filter rule

To disable a filter rule, run the following command:

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --enabled=false
```

To update a filter rule, run the following command:

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

Note that you need to pass the complete `--rule` field when updating.

### Delete a filter rule

To delete a filter rule, run the following command:

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --name <rule-name>
```

## Configure audit logging

### Data redaction

TiDB Cloud Serverless redacts sensitive data in the audit logs by default. For example, the following SQL statement:

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

It is redacted as follows:

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
- The time interval reaches 1 hour. Note that audit log file generation might be delayed for a few minutes depending on the underlying schedule.

> **Note:**
>
> The rotation cannot be configured at present. TiDB Cloud Serverless automatically rotates the audit log files based on the preceding conditions.

## Access audit logging

TiDB Cloud Serverless audit logs are stored as readable text files named `YYYY-MM-DD-<index>.log`.

Currently, audit logs are stored within TiDB Cloudfor 365 days. After this period, logs are automatically deleted.

> **Note:**
>
> Support for external storage options (such as AWS S3, Azure Blob Storage, and Google Cloud Storage) will be available in the future.

To view and download audit logs, use the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-download.md):

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- start-date: The start date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.
- end-date: The end date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.

> **Note:**
>
> TiDB Cloud Serverless does not guarantee sequential ordering of audit logs. The log file named `YYYY-MM-DD-<index>.log` may contains the audit logs in previous days.
> If you want to retrieve all logs from a specific date (for example, January 1, 2025), specify `--start-date 2025-01-01` and `--end-date 2025-01-02` usually works. But under extreme conditions, you may need to download all log files and order by the `TIME` filed.

## Audit logging fields

For each database event record in audit logs, TiDB provides the following fields:

### General information

All classes of audit logs contain the following information:

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| ID            | The unique identifier that identifies the audit record of an operation                        |
| TIME          | The timestamp of the audit record                        |
| EVENT         | The event classes of the audit record. Multiple event types are separated by commas (,)        |
| USER          | The username of the audit record                                                              |
| ROLES         | The roles of the user at the time of the operation                                            |
| CONNECTION_ID | The identifier of the user's connection                                                       |
| TABLES        | The accessed tables related to this audit record                                              |
| STATUS_CODE   | The status code of the audit record. `1` means success, `0` means failure                        |
| KEYSPACE_NAME | The keyspace name of the audit record. |
| SERVERLESS_TENANT_ID           | The ID of the serverless tenant that the cluster belongs to. |
| SERVERLESS_TSERVERLESS_PROJECT_ID         | The name of the serverless project that the cluster belongs to. |
| SERVERLESS_CLUSTER_ID          | The ID of the serverless cluster that the audit record belongs to. |
| REASON        | The error message of the audit record. Only recorded when an error occurs during the operation. |

### SQL statement information

When the event class is `QUERY` or a subclass of `QUERY`, the audit logs contain the following information:

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| CURRENT_DB     | The name of the current database.                                                                              |
| SQL_TEXT       | The executed SQL statements. If audit log redaction is enabled, the redacted SQL statements are recorded.     |
| EXECUTE_PARAMS | The parameters for the `EXECUTE` statements. Recorded only when the event classes include `EXECUTE` and redaction is disabled. |
| AFFECTED_ROWS  | The number of affected rows of the SQL statements. Recorded only when the event classes include `QUERY_DML`.    |

### Connection information

When the event class is `CONNECTION` or a subclass of `CONNECTION`, the audit logs contain the following information:

| Field           | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| CURRENT_DB      | Name of the current database. When the event classes include DISCONNECT, this information is not recorded. |
| CONNECTION_TYPE | Type of connection, including Socket, UnixSocket, and SSL/TLS                                 |
| PID             | Process ID of the current connection                                                          |
| SERVER_VERSION  | Current version of the connected TiDB server                                                  |
| SSL_VERSION     | Current version of SSL in use                                                                 |
| HOST_IP         | Current IP address of the connected TiDB server                                               |
| HOST_PORT       | Current port of the connected TiDB server                                                     |
| CLIENT_IP       | Current IP address of the client                                                              |
| CLIENT_PORT     | Current port of the client                                                                    |

### Audit operation information

When the event class is `AUDIT` or a subclass of `AUDIT`, the audit logs contain the following information:

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| AUDIT_OP_TARGET| The objects of the setting related to TiDB database auditing. |
| AUDIT_OP_ARGS  | The arguments of the setting related to TiDB database auditing. |

## Audit logging limitations

- Audit logging is only available via TiDB Cloud CLI. Support for TiDB Cloud console will be available soon.
- Audit logs can only be stored in TiDB Cloud at present. Support for external storage will be available soon.
- TiDB Cloud Serverless does not guarantee the sequential order of the audit logs, which means you might have to review all log files to see the latest events. To order the logs, you can use the `TIME` field in the audit logs.
