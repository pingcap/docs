---
title: Database Audit Logging (Beta) for {{{ .essential }}}
summary: Learn about how to audit a {{{ .essential }}} cluster in TiDB Cloud.
aliases: ['/tidbcloud/serverless-audit-logging']
---

# Database Audit Logging (Beta) for {{{ .essential }}}

{{{ .essential }}} provides an audit logging feature that records user access activities of your database, such as executed SQL statements.

> **Note:**
>
> Currently, the database audit logging feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for {{{ .essential }}} database audit logging" in the **Description** field and click **Submit**.

To evaluate the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to periodically analyze database audit logs.

The audit logging feature is **disabled by default**. To audit a TiDB cluster, you need to enable audit logging for it.

## Audit logging configurations

### Data redaction

By default, {{{ .essential }}} redacts sensitive data in audit logs. Take the following SQL statement as an example:

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

It is redacted as follows:

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

### Log file rotation

{{{ .essential }}} generates a new audit log file when either of the following conditions is met:

- The current log file reaches the rotation size (100 MiB by default).
- The rotation interval (one hour by default) has passed since the previous log generation. Depending on the internal scheduling mechanism, log generation might be delayed by a few minutes.

## Audit logging locations

You can store audit logs in the following locations:

- TiDB Cloud
- [Amazon S3](https://aws.amazon.com/s3/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)

### TiDB Cloud

You can store audit logs in TiDB Cloud and download them to your local machine. Audit logs expire and are deleted after 365 days. To request a longer retention period, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### Amazon S3

To store audit logs in Amazon S3, you need to provide the following information:

- URI: `s3://<bucket-name>/<folder-path>/`
- Access credentials: choose one of the following:
    - An [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) with the `s3:PutObject` permission.
    - A [role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) with the `s3:PutObject` permission. Only clusters hosted on AWS support using a role ARN.

For more information, see [Configure Amazon S3 access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access).

### Google Cloud Storage

To store audit logs in Google Cloud Storage, you need to provide the following information:

- URI: `gs://<bucket-name>/<folder-path>/`
- Access credential: a [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) with the `storage.objects.create` and `storage.objects.delete` permissions.

For more information, see [Configure GCS access](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access).

### Azure Blob Storage

To store audit logs in Azure Blob Storage, you need to provide the following information:

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` or `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- Access credential: a [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) with `Read` and `Write` permissions on the `Container` and `Object` resources.

For more information, see [Configure Azure Blob Storage access](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access).

### Alibaba Cloud OSS

To store audit logs in Alibaba Cloud OSS, you need to provide the following information:

- URI: `oss://<bucket-name>/<folder-path>/`
- Access credential: an [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) with the `oss:PutObject` and `oss:GetBucketInfo` permissions to allow data export to the OSS bucket.

For more information, see [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Audit logging filter rules

To filter audit logs, you need to create a filter rule to specify which events to log.

The filter rule contains the following fields:

- `users`: A list of user names to filter audit events. You can use the wildcard `%` to match any user name.
- `filters`: A list of filter objects. Each filter object contains the following fields:

    - `classes`: A list of event classes to filter audit events. For example, `["QUERY", "EXECUTE"]`.
    - `tables`: A list of table filters. For more information, see [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter/).
    - `statusCodes`: A list of status codes to filter audit events. `1` means success, and `0` means failure.

The following table shows all event classes in database audit logging:

| Event class   | Description                                                                                      | Parent-class   |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| `CONNECTION`    | Records all operations related to connections, such as handshaking, connections, disconnections, connection reset, and changing users | -             |
| `CONNECT`       | Records all operations of the handshaking in connections                                          | `CONNECTION`    |
| `DISCONNECT`    | Records all operations of the disconnections                                                      | `CONNECTION`    |
| `CHANGE_USER`   | Records all operations of changing users                                                          | `CONNECTION`    |
| `QUERY`         | Records all operations of SQL statements, including all errors about querying and modifying data  | -               |
| `TRANSACTION`   | Records all operations related to transactions, such as `BEGIN`, `COMMIT`, and `ROLLBACK`         | `QUERY`         |
| `EXECUTE`       | Records all operations of the `EXECUTE` statements                                                | `QUERY`         |
| `QUERY_DML`     | Records all operations of the DML statements, including `INSERT`, `REPLACE`, `UPDATE`, `DELETE`, and `LOAD DATA`    | `QUERY`     |
| `INSERT`        | Records all operations of the `INSERT` statements                                                   | `QUERY_DML`   |
| `REPLACE`       | Records all operations of the `REPLACE` statements                                                  | `QUERY_DML`   |
| `UPDATE`        | Records all operations of the `UPDATE` statements                                                   | `QUERY_DML`   |
| `DELETE`        | Records all operations of the `DELETE` statements                                                   | `QUERY_DML`   |
| `LOAD DATA`     | Records all operations of the `LOAD DATA` statements                                                | `QUERY_DML`   |
| `SELECT`        | Records all operations of the `SELECT` statements                                                   | `QUERY`       |
| `QUERY_DDL`     | Records all operations of the DDL statements                                                        | `QUERY`       |
| `AUDIT`         | Records all operations related to setting TiDB database auditing, including setting system variables and calling system functions | -                   |
| `AUDIT_FUNC_CALL` | Records all operations of calling system functions related to TiDB Cloud database auditing        | `AUDIT`       |
| `AUDIT_SET_SYS_VAR` | Records all operations of setting system variables        | `AUDIT`       |

> **Note:**
>
> The `AUDIT` event class and its subclasses are always recorded in audit logs and cannot be filtered out.

## Configure audit logging

You can enable, edit, and disable audit logging.

### Enable audit logging

You can enable audit logging for a {{{ .essential }}} cluster using the TiDB Cloud console or the TiDB Cloud CLI.

> **Note:**
>
> Enabling audit logging alone does not generate audit logs. You must also configure filters to specify which events to log. For more information, see [Manage audit logging filter rules](#manage-audit-logging-filter-rules).

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Enable**.

4. Select a storage location for the audit logs and fill in the required information. Then click **Test Connection and Next** or **Next**. For more information about available storage locations, see [Audit logging locations](#audit-logging-locations).

5. In the **Database Audit Logging Settings** dialog, fill in the log file rotation and log redaction settings, and then click **Save**.

</div>

<div label="CLI">

Take Amazon S3 storage as an example. To enable audit logging and store audit logs in Amazon S3, run the following command:

```shell
ticloud serverless audit-log config update -c <cluster-id> --enabled --cloud-storage S3 --s3.uri <s3-url> --s3.access-key-id <s3-access-key-id> --s3.secret-access-key <s3-secret-access-key> --rotation-size-mib <size-in-mb> --rotation-interval-minutes <interval-in-minutes> --unredacted=<true|false>
```

The `--rotation-size-mib`, `--rotation-interval-minutes`, and `--unredacted` parameters are optional. If you do not specify them, the default values are used.
 
</div>
</SimpleTab>

### Edit audit logging

You can edit the audit logging for a {{{ .essential }}} cluster after enabling it.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Settings**.

4. In the **Database Audit Logging Settings** dialog, update the log file rotation or log redaction settings, and then click **Save**.

</div>

<div label="CLI">

To update the audit logging settings using the TiDB Cloud CLI, run the following command:

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

4. In the **Disable DB Audit Logging** dialog, click **Disable**.

</div>

<div label="CLI">

To disable audit logging using the TiDB Cloud CLI, run the following command:

```shell
ticloud serverless audit-log config update -c <cluster-id> --disabled=true
```
 
</div>
</SimpleTab>

## Manage audit logging filter rules

You can create, edit, disable, and delete an audit logging filter rule.

### Create a filter rule

To create a filter rule, define which users and events you want to capture in the audit logs. You can specify users, event classes, tables, and status codes to tailor the logging to your needs.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, click **Add Filter Rule**.

4. In the **Add Filter Rule** dialog, fill in the **Filter Name**, **SQL Users**, and **Filter Rule** fields, and then click **Confirm**. For more information about these fields, see [Audit logging filter rules](#audit-logging-filter-rules).

</div>

<div label="CLI">

To create a filter rule using the TiDB Cloud CLI, run the following command:

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

3. On the **DB Audit Logging** page, locate the filter rule you want to edit, click **...** in its row, and then click **Edit**.

4. In the **Edit Filter Rule** dialog, update the **Filter Name** or **Filter Rule** field, and then click **Confirm**.

</div>

<div label="CLI">

To edit a filter rule using the TiDB Cloud CLI, run the following command:

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

3. On the **DB Audit Logging** page, locate the filter rule you want to disable, and turn off the toggle to disable the filter rule.

</div>

<div label="CLI">

To disable a filter rule using the TiDB Cloud CLI, run the following command:

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

3. On the **DB Audit Logging** page, locate the filter rule you want to delete and click **...**.

4. Click **Delete**, and then click **I understand. Delete it** to confirm.

</div>

<div label="CLI">

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --filter-rule-id <rule-id>
```
 
</div>
</SimpleTab>

## Access audit logging with TiDB Cloud Storage

When you store audit logs in TiDB Cloud, {{{ .essential }}} saves them as readable text files named `YYYY-MM-DD-<index>.log`. You can view and download these files from the TiDB Cloud console or using the TiDB Cloud CLI.

> **Note:**
>
> - {{{ .essential }}} does not guarantee that audit logs are stored in sequential order. A log file named `YYYY-MM-DD-<index>.log` might contain entries from earlier dates.
> - To retrieve all logs for a specific date (for example, January 1, 2025), set `--start-date 2025-01-01` and `--end-date 2025-01-02`. In some cases, you might need to download all log files and sort them by the `TIME` field.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

3. On the **DB Audit Logging** page, you can view the list of audit logs under **TiDB Cloud Storage**.

4. To download audit logs, select one or more logs from the list and then click **Download**.

</div>

<div label="CLI">

To download audit logs using the TiDB Cloud CLI, run the following command:

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

- `start-date`: the start date of the audit logs to download, in the format of `YYYY-MM-DD`, for example, `2025-01-01`.
- `end-date`: the end date of the audit logs to download, in the format of `YYYY-MM-DD`, for example, `2025-01-01`.
 
</div>
</SimpleTab>

## Audit logging fields

For each database event record in audit logs, TiDB Cloud provides the following fields:

### General information

All classes of audit logs contain the following information:

| Field         | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| `ID`            | The unique identifier that identifies the audit record of an operation.                        |
| `TIME`          | The timestamp of the audit record.                                                             |
| `EVENT`         | The event classes of the audit record. Multiple event types are separated by commas (`,`).     |
| `USER`          | The username of the audit record.                                                              |
| `ROLES`         | The roles of the user at the time of the operation.                                            |
| `CONNECTION_ID` | The identifier of the user's connection.                                                       |
| `TABLES`        | The accessed tables related to this audit record.                                              |
| `STATUS_CODE`   | The status code of the audit record. `1` means success, and `0` means failure.                |
| `KEYSPACE_NAME` | The keyspace name of the audit record.                                                        |
| `SERVERLESS_TENANT_ID`           | The ID of the serverless tenant that the cluster belongs to.                 |
| `SERVERLESS_PROJECT_ID`          | The ID of the serverless project that the cluster belongs to.                |
| `SERVERLESS_CLUSTER_ID`          | The ID of the serverless cluster that the audit record belongs to.           |
| `REASON`        | The error message of the audit record. Only recorded when an error occurs during the operation.|

### SQL statement information

When the event class is `QUERY` or a subclass of `QUERY`, the audit logs contain the following information:

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `CURRENT_DB`     | The name of the current database.                                                                             |
| `SQL_TEXT`       | The executed SQL statements. If audit log redaction is enabled, the redacted SQL statements are recorded.     |
| `EXECUTE_PARAMS` | The parameters for the `EXECUTE` statements. Recorded only when the event classes include `EXECUTE` and redaction is disabled. |
| `AFFECTED_ROWS`  | The number of affected rows of the SQL statements. Recorded only when the event classes include `QUERY_DML`.  |

### Connection information

When the event class is `CONNECTION` or a subclass of `CONNECTION`, the audit logs contain the following information:

| Field           | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `CURRENT_DB`      | The name of the current database. When the event classes include DISCONNECT, this information is not recorded. |
| `CONNECTION_TYPE` | The type of connection, including Socket, UnixSocket, and SSL/TLS.                                 |
| `PID`             | The process ID of the current connection.                                                          |
| `SERVER_VERSION`  | The current version of the connected TiDB server.                                                  |
| `SSL_VERSION`     | The current version of SSL in use.                                                                 |
| `HOST_IP`         | The current IP address of the connected TiDB server.                                               |
| `HOST_PORT`       | The current port of the connected TiDB server.                                                     |
| `CLIENT_IP`       | The current IP address of the client.                                                              |
| `CLIENT_PORT`     | The current port of the client.                                                                    |

> **Note:**
>
> To improve traffic visibility, `CLIENT_IP` now displays the real client IP address for connections via AWS PrivateLink, instead of the Load Balancer (LB) IP. Currently, this feature is in beta and is available only in the AWS region `Frankfurt (eu-central-1)`.

### Audit operation information

When the event class is `AUDIT` or a subclass of `AUDIT`, the audit logs contain the following information:

| Field          | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| `AUDIT_OP_TARGET`| The objects of the setting related to TiDB Cloud database auditing. |
| `AUDIT_OP_ARGS`  | The arguments of the setting related to TiDB Cloud database auditing. |

## Audit logging limitations

{{{ .essential }}} does not guarantee the sequential order of audit logs, which means that you might have to review all log files find the most recent events. To sort the logs chronologically, you can use the `TIME` field in the audit logs.
