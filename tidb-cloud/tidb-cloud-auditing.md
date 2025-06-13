---
title: Database Audit Logging
summary: Learn about how to audit a cluster in TiDB Cloud.
---

# Database Audit Logging

TiDB Cloud provides you with a database audit logging feature to record a history of user access details (such as any SQL statements executed) in logs.

> **Note:**
>
> Currently, the database audit logging feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for database audit logging" in the **Description** field and click **Submit**.

To assess the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to conduct a periodic analysis of the database audit logs.

The audit logging feature is disabled by default. To audit a cluster, you need to enable the audit logging first, and then specify the auditing filter rules.

> **Note:**
>
> Because audit logging consumes cluster resources, be prudent about whether to audit a cluster.

## Prerequisites

- You are using a TiDB Cloud Dedicated cluster. Audit logging is not available for TiDB Cloud Serverless clusters.
- You are in the `Organization Owner` or `Project Owner` role of your organization. Otherwise, you cannot see the database audit-related options in the TiDB Cloud console. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Enable audit logging

TiDB Cloud supports recording the audit logs of a TiDB Cloud Dedicated cluster to your cloud storage service. Before enabling database audit logging, configure your cloud storage service on the cloud provider where the cluster is located.

> **Note:**
>
> For TiDB clusters deployed on AWS, you can choose to store audit log files in TiDB Cloud when enabling database audit logging. Currently, this feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply to store audit log files in TiDB Cloud" in the **Description** field and click **Submit**.

### Enable audit logging for AWS

To enable audit logging for AWS, take the following steps:

#### Step 1. Create an Amazon S3 bucket

Specify an Amazon S3 bucket in your corporate-owned AWS account as a destination to which TiDB Cloud writes the audit logs.

> Note:
>
> Do not enable object lock on the AWS S3 bucket. Enabling object lock will prevent TiDB Cloud from pushing audit log files to S3.

For more information, see [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

#### Step 2. Configure Amazon S3 access

1. Get the TiDB Cloud Account ID and the External ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
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

In the TiDB Cloud console, go back to the **Enable Database Audit Logging** dialog box where you got the TiDB Cloud account ID and the External ID values, and then take the following steps:

1. In the **Bucket URI** field, enter the URI of your S3 bucket where the audit log files are to be written.
2. In the **Bucket Region** drop-down list, select the AWS region where the bucket locates.
3. In the **Role ARN** field, fill in the Role ARN value that you copied in [Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access).
4. Click **Test Connection** to verify whether TiDB Cloud can access and write to the bucket.

    If it is successful, **The connection is successfully** is displayed. Otherwise, check your access configuration.

5. Click **Enable** to enable audit logging for the cluster.

    TiDB Cloud is ready to write audit logs for the specified cluster to your Amazon S3 bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI, location, or ARN, you must click **Test Connection** again to verify that TiDB Cloud can connect to the bucket. Then, click **Enable** to apply the changes.
> - To remove TiDB Cloud's access to your Amazon S3, simply delete the trust policy granted to this cluster in the AWS Management Console.

### Enable audit logging for Google Cloud

To enable audit logging for Google Cloud, take the following steps:

#### Step 1. Create a GCS bucket

Specify a Google Cloud Storage (GCS) bucket in your corporate-owned Google Cloud account as a destination to which TiDB Cloud writes audit logs.

For more information, see [Creating storage buckets](https://cloud.google.com/storage/docs/creating-buckets) in the Google Cloud Storage documentation.

#### Step 2. Configure GCS access

1. Get the Google Cloud Service Account ID of the TiDB cluster that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
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
3. Click **Test Connection** to verify whether TiDB Cloud can access and write to the bucket.

    If it is successful, **The connection is successfully** is displayed. Otherwise, check your access configuration.

4. Click **Enable** to enable audit logging for the cluster.

    TiDB Cloud is ready to write audit logs for the specified cluster to your GCS bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI or location, you must click **Test Connection** again to verify that TiDB Cloud can connect to the bucket. Then, click **Enable** to apply the changes.
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

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.
4. In the **Enable Database Audit Logging** dialog, provide the blob URL and SAS token that you obtained from [Step 2. Configure Azure Blob access](#step-2-configure-azure-blob-storage-access):

    - In the **Blob URL** field, enter the URL of the container where audit logs will be stored.
    - In the **SAS Token** field, enter the SAS token for accessing the container.

5. Click **Test Connection** to verify whether TiDB Cloud can access and write to the container.

    If it is successful, **The connection is successfully** is displayed. Otherwise, check your access configuration.

6. Click **Enable** to enable audit logging for the cluster.

    TiDB Cloud is ready to write audit logs for the specified cluster to your Azure blob container.

> **Note:**
>
> After enabling audit logging, if you make new changes to the **Blob URL** or **SAS Token** fields, you must click **Test Connection** again to verify that TiDB Cloud can connect to the container. Then, click **Enable** to apply the changes.

## Specify auditing filter rules

After enabling audit logging, you must specify auditing filter rules to control which user access events to capture and write to audit logs. If no filter rules are specified, TiDB Cloud does not log anything.

To specify auditing filter rules for a cluster, take the following steps:

1. On the **DB Audit Logging** page, click **Add Filter Rule** in the **Log Filter Rules** section to add an audit filter rule.

    You can add one audit rule at a time. Each rule specifies a user expression, database expression, table expression, and access type. You can add multiple audit rules to meet your auditing requirements.

2.In the **Log Filter Rules** section, click **>** to expand and view the list of audit rules you have added.

> **Note:**
>
> - The filter rules are regular expressions and case-sensitive. If you use the wildcard rule `.*`, all users, databases, or table events in the cluster are logged.
> - Because audit logging consumes cluster resources, be prudent when specifying filter rules. To minimize the consumption, it is recommended that you specify filter rules to limit the scope of audit logging to specific database objects, users, and actions, where possible.

## View audit logs

By default, TiDB Cloud stores database audit log files in your storage service, so you need to read the audit log information from your storage service.

> **Note:**
>
> If you have requested and chosen to store audit log files in TiDB Cloud, you can download them from the **Audit Log Access** section on the **Database Audit Logging** page.

TiDB Cloud audit logs are readable text files with the cluster ID, Pod ID, and log creation date incorporated into the fully qualified filenames.

For example, `13796619446086334065/tidb-0/tidb-audit-2022-04-21T18-16-29.529.log`. In this example, `13796619446086334065` indicates the cluster ID and `tidb-0` indicates the Pod ID.

## Disable audit logging

If you no longer want to audit a cluster, go to the page of the cluster, click **Settings** > **Audit Settings**, and then toggle the audit setting in the upper-right corner to **Off**.

> **Note:**
>
> Each time the size of the log file reaches 10 MiB, the log file will be pushed to the cloud storage bucket. Therefore, after the audit log is disabled, the log file whose size is smaller than 10 MiB will not be automatically pushed to the cloud storage bucket. To get the log file in this situation, contact [PingCAP support](/tidb-cloud/tidb-cloud-support.md).

## Audit log fields

For each database event record in audit logs, TiDB provides the following fields:

> **Note:**
>
> In the following tables, the empty maximum length of a field means that the data type of this field has a well-defined constant length (for example, 4 bytes for INTEGER).

| Col # | Field name | TiDB data type | Maximum length | Description |
|---|---|---|---|---|
| 1 | N/A | N/A | N/A | Reserved for internal use |
| 2 | N/A | N/A | N/A | Reserved for internal use |
| 3 | N/A | N/A | N/A | Reserved for internal use |
| 4 | ID       | INTEGER |  | Unique event ID  |
| 5 | TIMESTAMP | TIMESTAMP |  | Time of event   |
| 6 | EVENT_CLASS | VARCHAR | 15 | Event type     |
| 7 | EVENT_SUBCLASS     | VARCHAR | 15 | Event subtype |
| 8 | STATUS_CODE | INTEGER |  | Response status of the statement   |
| 9 | COST_TIME | FLOAT |  | Time consumed by the statement    |
| 10 | HOST | VARCHAR | 16 | Server IP    |
| 11 | CLIENT_IP         | VARCHAR | 16 | Client IP   |
| 12 | USER | VARCHAR | 17 | Login username    |
| 13 | DATABASE | VARCHAR | 64 | Event-related database      |
| 14 | TABLES | VARCHAR | 64 | Event-related table name          |
| 15 | SQL_TEXT | VARCHAR | 64 KB | Masked SQL statement   |
| 16 | ROWS | INTEGER |  | Number of affected rows (`0` indicates that no rows are affected)      |

Depending on the EVENT_CLASS field value set by TiDB, database event records in audit logs also contain additional fields as follows:

- If the EVENT_CLASS value is `CONNECTION`, database event records also contain the following fields:

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CLIENT_PORT | INTEGER |  | Client port number |
    | 18 | CONNECTION_ID | INTEGER |  | Connection ID |
    | 19 | CONNECTION_TYPE  | VARCHAR | 12 | Connection via `socket` or `unix-socket` |
    | 20 | SERVER_ID | INTEGER |  | TiDB server ID |
    | 21 | SERVER_PORT | INTEGER |  | The port that the TiDB server uses to listen to client communicating via the MySQL protocol |
    | 22 | SERVER_OS_LOGIN_USER | VARCHAR | 17 | The username of the TiDB process startup system  |
    | 23 | OS_VERSION | VARCHAR | N/A | The version of the operating system where the TiDB server is located  |
    | 24 | SSL_VERSION | VARCHAR | 6 | The current SSL version of TiDB |
    | 25 | PID | INTEGER |  | The PID of the TiDB process |

- If the EVENT_CLASS value is `TABLE_ACCESS` or `GENERAL`, database event records also contain the following fields:

    | Col # | Field name | TiDB data type | Maximum length | Description |
    |---|---|---|---|---|
    | 17 | CONNECTION_ID | INTEGER |  | Connection ID   |
    | 18 | COMMAND | VARCHAR | 14 | The command type of the MySQL protocol |
    | 19 | SQL_STATEMENT  | VARCHAR | 17 | The SQL statement type |
    | 20 | PID | INTEGER |  | The PID of the TiDB process  |
