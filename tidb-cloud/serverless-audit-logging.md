---
title: Database Audit Logging for {{{ .essential }}}
summary: Learn about how to audit a {{{ .essential }}} cluster in TiDB Cloud.
---

# Database Audit Logging (Beta) for {{{ .essential }}}

{{{ .essential }}} provide you with a database audit logging feature to record a history of user access details (such as any SQL statements executed) in logs.

> **Note:**
>
> Currently, the database audit logging feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for {{{ .essential }}} database audit logging" in the **Description** field and click **Submit**.

To assess the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to conduct a periodic analysis of the database audit logs.

The audit logging feature is disabled by default. To audit a cluster, you need to enable audit logging for it.

## Audit logging configurations

### Data redaction

{{{ .essential }}} redact sensitive data in the audit logs by default. Take the following SQL statement as an example:

```sql 
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

It is redacted as follows:

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

### Log file rotation

{{{ .essential }}} generate a new audit log file when either of the following conditions is met:

- The size of the current log file reaches rotation size (100 MB by default).
- Rotation interval (one hour by default) has passed since the previous log generation. Depending on the internal scheduling mechanism, log generation might be delayed by a few minutes.

## Audit logging locations

You can store the audit logs to the following locations:

- TiDB Cloud
- [Amazon S3](https://aws.amazon.com/s3/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)

### TiDB Cloud

You can store audit logs in TiDB Cloud and download them to your local machine. The audit logs will be expired and deleted after 365 days. To request longer storage duration, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### Amazon S3

To store audit logs to Amazon S3, you need to provide the following information:

- URI: `s3://<bucket-name>/<folder-path>/`
- One of the following access credentials:
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): make sure the access key has the `s3:PutObject` and `s3:ListBucket` permissions.
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): make sure the role ARN (Amazon Resource Name) has the `s3:PutObject` permissions. Note that only clusters hosted on AWS support the role ARN.

For more information, see [Configure Amazon S3 access](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).

### Google Cloud Storage

To store audit logs to Google Cloud Storage, you need to provide the following information:

- URI: `gs://<bucket-name>/<folder-path>/`
- Access credential: a **base64 encoded** [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your bucket. Make sure the service account key has the `storage.objects.create` and `storage.objects.delete` permissions.

For more information, see [Configure GCS access](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

### Azure Blob Storage

To store audit logs to Azure Blob Storage, you need to provide the following information:

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` or `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- Access credential: a [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) for your Azure Blob Storage container. Make sure the SAS token has the `Read` and `Write` permissions on the `Container` and `Object` resources.

For more information, see [Configure Azure Blob Storage access](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

### Alibaba Cloud OSS

To store audit logs to Alibaba Cloud OSS, you need to provide the following information:

- URI: `oss://<bucket-name>/<folder-path>/`
- Access credential: An [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) for your Alibaba Cloud account. Make sure the AccessKey pair has the `oss:PutObject` and `oss:GetBucketInfo` permissions to allow data export to the OSS bucket.

For more information, see [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Audit logging filter rules

To filter the audit logging, you need to create a filter rule to specify which events to log.

The filter rule contains the following fields:

- `users`: A list of user names to filter audit events. You can use the wildcard `%` to match any user name.
- `filters`: A list of filter objects. Each filter object can contain the following fields:

    - `classes`: A list of event classes to filter audit events. For example, `["QUERY", "EXECUTE"]`.
    - `tables`: A list of table filters. For more information, see [Table filters].
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
| AUDIT_FUNC_CALL    | Record all operations of calling system functions related to TiDB database auditing               | AUDIT |

## Configure audit logging

### Enable audit logging

You can enable audit logging for a {{{ .essential }}} cluster.

> **Note:**
>
> Only enabling audit logging will not generate audit logs. You need to configure filters to specify what events to log. For more information, see [Manage audit logging filter rules](#manage-audit-logging-filter-rules).

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Enable**.

4. Select the storage location of the audit logs and fill in the necessary information, then click **Test Connection and Next** or **Next**. For more information about the available storage locations, see [Audit logging locations](#audit-logging-locations).

5. In the **Database Audit Logging Setting** pop-up, fill the log file rotation and log redaction settings, and then click **Save**.

</div>

<div label="CLI">

Take s3 storage as an example. Run the following command to enable audit logging and store the audit logs to Amazon S3:

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-url> --s3.access-key-id <s3-access-key-id>  --s3.secret-access-key <s3-secret-access-key> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

`--rotation-size-mib`, `--rotation-interval-minutes`, and `--unredacted` are optional parameters. If you do not specify them, the default values are used.
 
</div>
</SimpleTab>

### Edit audit logging

You can Edit the audit logging for a {{{ .essential }}} cluster after enabling it.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Settings**.

4. In the **Database Audit Logging Setting** pop-up, fill the log file rotation and log redaction settings, and then click **Save**.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log config update -c <cluster-id> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```
 
</div>
</SimpleTab>

### Disable audit logging

You can disable audit logging for a {{{ .essential }}} cluster.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **...** in the upper-right corner, and then click **Disable**.

4. Click **Disable** in the pop-up dialog to disable audit logging.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log config update -c <cluster-id> --disabled=true
```
 
</div>
</SimpleTab>

## Manage audit logging filter rules

You can manage audit logging filter rules in the [TiDB Cloud console](https://tidbcloud.com/) or by using the [TiDB Cloud CLI](/tidb-cloud/ticloud-auditlog-config.md).

### Create a filter rule

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Add Filter Rule**.

4. Fill in the `Filter Name`, `SQL Users`, and `Filter Rules` fields in the **Add Filter Rule** pop-up dialog, and then click **Confirm**. For more information about the fields, see [Audit logging filter rules](#audit-logging-filter-rules).

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```
 
</div>
</SimpleTab>

### Edit a filter rule

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, find the filter rule you want to edit, click **...** in its row, and then click **Edit**.

4. Fill in the `Filter Name` and `Filter Rules` fields in the **Edit Filter Rule** pop-up dialog, and then click **Confirm**.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```
 
</div>
</SimpleTab>

### Disable a filter rule

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, choose the filter rule you want to disable.

4. switch the slider to disable the filter rule.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```
 
</div>
</SimpleTab>

### Delete a filter rule

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, choose the filter rule you want to delete and click **...**.

4. Click **Delete** and then click **I understand. Delete it** in the pop-up dialog to delete the filter rule.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```
 
</div>
</SimpleTab>

## Access audit logging with TiDB Cloud Storage

{{{ .essential }}} audit logs are stored as readable text files named `YYYY-MM-DD-<index>.log`. When you store audit logs in TiDB Cloud, you can access and download them.

> **Note:**
>
> {{{ .essential }}} do not guarantee sequential ordering of audit logs. The log file named `YYYY-MM-DD-<index>.log` might contain the audit logs in previous days.
> If you want to retrieve all logs from a specific date (for example, January 1, 2025), specifying `--start-date 2025-01-01` and `--end-date 2025-01-02` usually works. But under extreme conditions, you might need to download all log files and order them by the `TIME` field.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, you can view the list of audit logs under `TiDB Cloud Storage`.

4. To download audit logs, select one or more logs from the list and then click **Download**.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- `start-date`: The start date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.
- `end-date`: The end date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.
 
</div>
</SimpleTab>

## Audit logging fields

For each database event record in audit logs, TiDB provides the following fields:

### General information

All classes of audit logs contain the following information:

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| ID            | The unique identifier that identifies the audit record of an operation                        |
| TIME          | The timestamp of the audit record                        |
| EVENT         | The event classes of the audit record. Multiple event types are separated by commas (`,`)        |
| USER          | The username of the audit record                                                              |
| ROLES         | The roles of the user at the time of the operation                                            |
| CONNECTION_ID | The identifier of the user's connection                                                       |
| TABLES        | The accessed tables related to this audit record                                              |
| STATUS_CODE   | The status code of the audit record. `1` means success, and `0` means failure.                       |
| KEYSPACE_NAME | The keyspace name of the audit record. |
| SERVERLESS_TENANT_ID           | The ID of the serverless tenant that the cluster belongs to. |
| SERVERLESS_TSERVERLESS_PROJECT_ID         | The ID of the serverless project that the cluster belongs to. |
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
| CURRENT_DB      | The name of the current database. When the event classes include DISCONNECT, this information is not recorded. |
| CONNECTION_TYPE | The type of connection, including Socket, UnixSocket, and SSL/TLS.                                 |
| PID             | The process ID of the current connection.                                                          |
| SERVER_VERSION  | The current version of the connected TiDB server.                                                  |
| SSL_VERSION     | The current version of SSL in use.                                                                 |
| HOST_IP         | The current IP address of the connected TiDB server.                                              |
| HOST_PORT       | The current port of the connected TiDB server.                                                     |
| CLIENT_IP       | The current IP address of the client.                                                             |
| CLIENT_PORT     | The current port of the client.                                                                    |

### Audit operation information

When the event class is `AUDIT` or a subclass of `AUDIT`, the audit logs contain the following information:

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| AUDIT_OP_TARGET| The objects of the setting related to TiDB database auditing. |
| AUDIT_OP_ARGS  | The arguments of the setting related to TiDB database auditing. |

## Audit logging limitations

- Do not guarantee the sequential order of audit logs, which means you might have to review all log files to view the latest events. To sort the logs chronologically, you can use the `TIME` field in the audit logs.
