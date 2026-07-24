---
title: TiDB Cloud Dedicated Database Audit Logging
summary: Learn about how to audit a cluster in TiDB Cloud.
---

# TiDB Cloud Dedicated Database Audit Logging

TiDB Cloud provides an audit logging feature that records user access activities of your database, such as executed SQL statements.

> **Note:**
>
> Database audit logging is now in Public Preview for eligible clusters.
>
> - TiDB version: v7.5.6 or later, or v8.5.2 or later.
> - For Azure clusters, the cluster must have been created after April 15, 2026.
> For all other versions or configurations, the feature remains available upon request.
>
> To request access for an ineligible cluster, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, fill in "Apply for database audit logging" in the **Description** field, and then click **Submit**.

For documentation of the earlier audit logging version, see [TiDB Cloud Database Audit Logging (Legacy)](/tidb-cloud/tidb-cloud-auditing-legacy.md).

To evaluate the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to periodically analyze database audit logs.

The audit logging feature is **disabled by default**. To audit a cluster, you must first enable the audit logging, and then specify the auditing filter rules.

> **Note:**
>
> Because audit logging consumes cluster resources, be prudent about whether to audit a cluster.

## Prerequisites

- You are using a TiDB Cloud Dedicated cluster.

    > **Note:**
    >
    > - Database audit logging is not available for {{{ .starter }}}.
    > - For {{{ .essential }}}, see [Database Audit Logging (PREVIEW) for {{{ .essential }}}](/tidb-cloud/essential-database-audit-logging.md).

- You are in the `Organization Owner` or `Project Owner` role of your organization. Otherwise, you cannot see the database audit-related options in the TiDB Cloud console. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Enable audit logging

TiDB Cloud supports recording the audit logs of a TiDB Cloud Dedicated cluster to your cloud storage service. Before enabling database audit logging, configure your cloud storage service on the cloud provider where the cluster is located.

> **Note:**
>
> For TiDB clusters deployed on AWS, you can choose to store audit log files in TiDB Cloud when enabling database audit logging. Currently, this feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, fill in "Apply to store audit log files in TiDB Cloud" in the **Description** field, and then click **Submit**.

### Enable audit logging for AWS

To enable audit logging for AWS, take the following steps:

#### Step 1. Create an Amazon S3 bucket

Specify an Amazon S3 bucket in your organization-owned AWS account as a destination to which TiDB Cloud writes the audit logs.

> **Note:**
>
> Do not enable object lock on the AWS S3 bucket. Enabling object lock will prevent TiDB Cloud from pushing audit log files to S3.

For more information, see [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

#### Step 2. Configure Amazon S3 access

1. Get the TiDB Cloud Account ID and the External ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

        > **Tip:**
        >
        > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

    2. Click the name of your target TiDB Cloud Dedicated cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
    3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.
    4. In the **Enable Database Audit Logging** dialog, locate the **AWS IAM Policy Settings** section, and record **TiDB Cloud Account ID** and **TiDB Cloud External ID** for later use.

2. In the AWS Management Console, go to **IAM** > **Access Management** > **Policies**, and then check whether there is a storage bucket policy with the `s3:PutObject` write-only permission.

    - If yes, record the matched storage bucket policy for later use.
    - If not, go to **IAM** > **Access Management** > **Policies** > **Create Policy**, and define a bucket policy according to the following policy template.

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "<Your S3 bucket ARN>/*"
                }
            ]
        }
        ```

        In the template, `<Your S3 bucket ARN>` is the Amazon Resource Name (ARN) of your S3 bucket where the audit log files are to be written. You can go to the **Properties** tab in your S3 bucket and get the ARN value in the **Bucket Overview** area. In the `"Resource"` field, you need to add `/*` after the ARN. For example, if the ARN is `arn:aws:s3:::tidb-cloud-test`, you need to configure the value of the `"Resource"` field as `"arn:aws:s3:::tidb-cloud-test/*"`.

3. Go to **IAM** > **Access Management** > **Roles**, and then check whether a role whose trust entity corresponds to the TiDB Cloud Account ID and the External ID that you recorded earlier already exists.

    - If yes, record the matched role for later use.
    - If not, click **Create role**, select **Another AWS account** as the trust entity type, and then enter the TiDB Cloud Account ID value into the **Account ID** field. Then, choose the **Require External ID** option and enter the TiDB Cloud External ID value into the **External ID** field.

4. In **IAM** > **Access Management** > **Roles**, click the role name from the previous step to go to the **Summary** page, and then take the following steps:

    1. Under the **Permissions** tab, check whether the recorded policy with the `s3:PutObject` write-only permission is attached to the role. If not, choose **Attach Policies**, search for the needed policy, and then click **Attach Policy**.
    2. Return to the **Summary** page and copy the **Role ARN** value to your clipboard.

#### Step 3. Enable audit logging

In the TiDB Cloud console, go back to the **Database Audit Log Storage Configuration** dialog box where you got the TiDB Cloud account ID and the External ID values, and then take the following steps:

1. In the **Bucket URI** field, enter the URI of your S3 bucket where the audit log files are to be written.
2. In the **Bucket Region** drop-down list, select the AWS region where the bucket locates.
3. In the **Role ARN** field, fill in the Role ARN value that you copied in [Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access).
4. Click **Test Connection and Save** to verify whether TiDB Cloud can access and write to the bucket. If the connection is successful, the dialog navigates to the next step for **Database Audit Logging Settings**.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI, location, or ARN, you must disable and re-enable audit logging.
> - To remove TiDB Cloud's access to your Amazon S3, simply delete the trust policy granted to this cluster in the AWS Management Console.

### Enable audit logging for Google Cloud

To enable audit logging for Google Cloud, take the following steps:

#### Step 1. Create a GCS bucket

Specify a Google Cloud Storage (GCS) bucket in your organization-owned Google Cloud account as a destination to which TiDB Cloud writes audit logs.

For more information, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in the Google Cloud Storage documentation.

#### Step 2. Configure GCS access

1. Get the Google Cloud Service Account ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

        > **Tip:**
        >
        > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

    2. Click the name of your target TiDB Cloud Dedicated cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
    3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.
    4. In the **Enable Database Audit Logging** dialog, locate the **Google Cloud Server Account ID** section, and record **Service Account ID** for later use.

2. In the Google Cloud console, go to **IAM & Admin** > **Roles**, and then check whether a role with the following write-only permissions of the storage container exists.

    - storage.objects.create
    - storage.objects.delete

    If yes, record the matched role for the TiDB cluster for later use. If not, go to **IAM & Admin** > **Roles** > **CREATE ROLE** to define a role for the TiDB cluster.

3. Go to **Cloud Storage** > **Browser**, select the GCS bucket you want TiDB Cloud to access, and then click **SHOW INFO PANEL**.

    The panel is displayed.

4. In the panel, click **ADD PRINCIPAL**.

    The dialog box for adding principals is displayed.

5. In the dialog box, take the following steps:

    1. In the **New Principals** field, paste the Google Cloud Service Account ID of the TiDB cluster.
    2. In the **Role** drop-down list, choose the role of the target TiDB cluster.
    3. Click **SAVE**.

#### Step 3. Enable audit logging

In the TiDB Cloud console, go back to the **Enable Database Audit Logging** dialog box where you got the TiDB Cloud account ID, and then take the following steps:

1. In the **Bucket URI** field, enter your full GCS bucket name.
2. In the **Bucket Region** field, select the GCS region where the bucket locates.
3. Click **Test Connection and Save** to verify whether TiDB Cloud can access and write to the bucket. If the connection is successful, the dialog navigates to the next step for **Database Audit Logging Settings**.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI or location, you must disable and re-enable audit logging.
> - To remove TiDB Cloud's access to your GCS bucket, delete the trust policy granted to this cluster in the Google Cloud console.

### Enable audit logging for Azure

To enable audit logging for Azure, take the following steps:

#### Step 1. Create an Azure storage account

Create an Azure storage account in your organization's Azure subscription as the destination to which TiDB Cloud writes the database audit logs.

For more information, see [Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal) in Azure documentation.

#### Step 2. Configure Azure Blob Storage access

1. In the [Azure portal](https://portal.azure.com/), create a container used for storing database audit logs.

    1. In the left navigation pane of the Azure portal, click **Storage Accounts**, and then click the storage account for storing database audit logs.

        > **Tip:**
        >
        > If the left navigation pane is hidden, click the menu button in the upper-left corner to toggle its visibility.

    2. In the navigation pane for the selected storage account, click **Data storage > Containers**, and then click **+ Container** to open the **New container** pane.

    3. In the **New container** pane, enter a name for your new container, set the anonymous access level (the recommended level is **Private**, which means no anonymous access), and then click **Create**. The new container will be created and displayed in the container list in a few seconds.

2. Get the URL of the target container.

    1. In the container list, select the target container, click **...** for the container, and then select **Container properties**.
    2. On the displayed properties page, copy the **URL** value for later use, and then return to the container list.

3. Generate a SAS token for the target container.

    1. In the container list, select the target container, click **...** for the container, and then select **Generate SAS**.
    2. In the displayed **Generate SAS** pane, select **Account key** for **Signing method**.
    3. In the **Permissions** drop-down list, select **Read**, **Write**, and **Create** to allow writing audit log files.
    4. In the **Start** and **Expiry** fields, specify a validity period for the SAS token.

        > **Note:**
        >
        > - The audit feature needs to continuously write audit logs to the storage account, so the SAS token must have a sufficiently long validity period. However, longer validity increases the risk of token leakage. For security, it is recommended to replace your SAS token every six to twelve months.
        > - The generated SAS token cannot be revoked, so you need to set its validity period carefully.
        > - Make sure to re-generate and update the SAS token before it expires to ensure continuous availability of audit logs.

    5. For **Allowed protocols**, select **HTTPS only** to ensure secure access.
    6. Click **Generate SAS token and URL**, and then copy the displayed **Blob SAS token** for later use.

#### Step 3. Enable audit logging

1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target TiDB Cloud Dedicated cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.
4. In the **Enable Database Audit Logging** dialog, provide the blob URL and SAS token that you obtained from [Step 2. Configure Azure Blob access](#step-2-configure-azure-blob-storage-access):
    - In the **Blob URL** field, enter the URL of the container where audit logs will be stored.
    - In the **SAS Token** field, enter the SAS token for accessing the container.
5. Click **Test Connection and Save** to verify whether TiDB Cloud can access and write to the container. If the connection is successful, the dialog navigates to the next step for **Database Audit Logging Settings**.

> **Note:**
>
> After enabling audit logging, if you make new changes to the **Blob URL** or **SAS Token** fields, you must disable and re-enable audit logging.

## Database audit logging settings

After configuring storage for your cloud provider, complete the **Database Audit Logging Settings** step:

1. Set the log file rotation policy.

    You can rotate audit log files based on either file size or time interval. When either condition is met, TiDB Cloud generates a new audit log file.

2. Configure log redaction.

    Log redaction is enabled by default. When enabled, sensitive information in the SQL text is replaced with `?` in audit logs.

3. Click **Save and Enable** to apply the settings and enable the audit logging.

> **Note:**
>
> If you disable log redaction, audit log files written to your cloud storage might contain sensitive information. This configuration is not recommended due to potential security risks.


## Specify auditing filter rules

After enabling audit logging, you must specify auditing filter rules to control which user access events to capture and write to audit logs. If no filter rules are specified, TiDB Cloud does not log anything.

To specify auditing filter rules for a cluster, take the following steps:

1. On the **DB Audit Logging** page, click **Add Filter Rule** in the **Audit Filters** section to add an audit filter rule.

2. In the **Add Filter Rule** dialog, configure the following items:

    - **Filter Name**: Enter a name for the filter rule.
    - **SQL User**: Enter the SQL user in the `<user>@<host>` format. The username and hostname can use `%` to match any value or `_` to match any single character. The `@` symbol and `<host>` are optional.
    - **Filter Events**: Select the events to log. For the supported filter events, see [Audit Filter Events](#audit-filter-events).

3. Click **Confirm** to add the filter rule.

> **Note:**
>
> - Because audit logging consumes cluster resources, be prudent when specifying filter rules. To minimize resource usage, specify filter rules to limit audit logging to specific users and events where possible.

## View audit logs

By default, TiDB Cloud stores database audit log files in your storage service, so you need to read the audit log information from your storage service.

> **Note:**
>
> If you have requested and chosen to store audit log files in TiDB Cloud, you can download them from the **Audit Log Access** section on the **Database Audit Logging** page.

TiDB Cloud audit logs are readable text files with the cluster ID, node ID, and log creation date incorporated into the fully qualified filenames.

For example, `13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`. In this example, `13796619446086334065` indicates the cluster ID and `tidb-0` indicates the node ID.

## Disable audit logging

If you no longer want to audit a cluster, take the following steps:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page in the TiDB Cloud console, and then click the name of your target TiDB Cloud Dedicated cluster.
2. In the left navigation pane, click **Settings** > **DB Audit Logging**.
3. In the **Database Audit Logging** section, click **...** next to **Settings**, and then click **Disable**.

> **Note:**
>
> Each time the size of the log file reaches 10 MiB, the log file will be pushed to the cloud storage bucket. Therefore, after the audit log is disabled, the log file whose size is smaller than 10 MiB will not be automatically pushed to the cloud storage bucket. To get the log file in this situation, contact [PingCAP support](/tidb-cloud/tidb-cloud-support.md).

## Audit filter events

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
| `SERVERLESS_TENANT_ID`           | The ID of the serverless tenant that the {{{ .essential }}} instance belongs to.                 |
| `SERVERLESS_PROJECT_ID`          | The ID of the serverless project that the {{{ .essential }}} instance belongs to.                |
| `SERVERLESS_CLUSTER_ID`          | The ID of the serverless {{{ .essential }}} instance that the audit record belongs to.           |
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

{{{ .dedicated }}} does not guarantee the sequential order of audit logs, which means that you might have to review all log files to find the most recent events. To sort the logs chronologically, you can use the `TIME` field in the audit logs.

## Legacy database audit logging reference

If you are currently relying on the legacy audit logging plugin, see [Database Audit Logging (Legacy)](/tidb-cloud/tidb-cloud-auditing-legacy.md).
