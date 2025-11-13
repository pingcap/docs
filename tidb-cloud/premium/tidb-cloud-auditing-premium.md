---
title: "{{{ .premium }}} Database Audit Logging"
summary: Learn how to audit an instance in {{{ .premium }}}.
---

# {{{ .premium }}} Database Audit Logging

TiDB Cloud provides an audit logging feature that records user access activities of your database, such as executed SQL statements.

To evaluate the effectiveness of user access policies and other information security measures of your organization, it is a security best practice to periodically analyze database audit logs.

The audit logging feature is **disabled by default**. To audit a TiDB instance, you must first enable audit logging, and then configure auditing filter rules.

> **Note:**
>
> Because audit logging consumes instance resources, be prudent about whether to audit an instance.

## Prerequisites

- You are using a {{{ .premium }}} instance.

    > **Note:**
    >
    > - Database audit logging is not available for {{{ .starter }}}.
    > - For {{{ .essential }}}, see [Database Audit Logging (Beta) for {{{ .essential }}}](/tidb-cloud/essential-database-audit-logging.md).
    > - For {{{ .dedicated }}}, see [{{{ .dedicated }}} Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md).

- You must have the `Organization Owner` role in your organization. Otherwise, you cannot see the database audit-related options in the TiDB Cloud console.

## Enable audit logging

TiDB Cloud supports recording the audit logs of a {{{ .premium }}} instance to your cloud storage service. Before enabling database audit logging, configure your cloud storage service on the cloud provider where the instance is located.

### Enable audit logging for TiDB on AWS

To enable audit logging for AWS, take the following steps:

#### Step 1. Create an Amazon S3 bucket

Specify an Amazon S3 bucket in your organization-owned AWS account as the destination to which TiDB Cloud writes audit logs.

> **Note:**
>
> Do not enable object lock on the AWS S3 bucket. Enabling object lock will prevent TiDB Cloud from pushing audit log files to S3.

For more information, see [Creating a general purpose bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) in the AWS User Guide.

#### Step 2. Configure Amazon S3 access

1. Get the TiDB Cloud Account ID and the External ID of the TiDB instance that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**TiDB Instances**](https://tidbcloud.com/instances) page.

    2. Click the name of your target instance to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.

    3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.

    4. In the **Database Audit Log Storage Configuration** dialog, locate the **AWS IAM Policy Settings** section, and record **TiDB Cloud Account ID** and **TiDB Cloud External ID** for later use.

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

In the TiDB Cloud console, go back to the **Database Audit Log Storage Configuration** dialog where you got the TiDB Cloud account ID and the External ID values, and then take the following steps:

1. In the **Bucket URI** field, enter the URI of your S3 bucket where the audit log files are to be written.
2. In the **Bucket Region** drop-down list, select the AWS region where the bucket is located.
3. In the **Role ARN** field, fill in the Role ARN value that you copied in [Step 2. Configure Amazon S3 access](#step-2-configure-amazon-s3-access).
4. Click **Test Connection and Next** to verify whether TiDB Cloud can access and write to the bucket.

    If it is successful, **The connection is successful** is displayed. Otherwise, check your access configuration.

5. Click **Enable** to enable audit logging for the instance.

    TiDB Cloud is ready to write audit logs for the specified instance to your Amazon S3 bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI, location, or ARN, you must click **Test Connection** again to verify that TiDB Cloud can connect to the bucket. Then, click **Enable** to apply the changes.
> - To remove TiDB Cloud's access to your Amazon S3, simply delete the trust policy granted to this instance in the AWS Management Console.

<CustomContent language="en,zh">

### Enable audit logging for TiDB on Alibaba Cloud

To enable database audit logging for TiDB cloud on Alibaba Cloud, take the following steps:

#### Step 1. Create an OSS bucket

Create an Object Storage Service (OSS) bucket in your organization-owned Alibaba Cloud account as the destination to which TiDB Cloud writes audit logs.

For more information, see [Create a bucket](https://www.alibabacloud.com/help/en/oss/user-guide/create-a-bucket-4) in the Alibaba Cloud Storage documentation.

#### Step 2. Configure OSS access

1. Get the Alibaba Cloud Service Account ID of the TiDB instance that you want to enable audit logging.

    1. In the TiDB Cloud console, navigate to the [**TiDB Instances**](https://tidbcloud.com/instances) page.
    2. Click the name of your target instance to go to its overview page, and then click **Settings** > **DB Audit Logging** in the left navigation pane.
    3. On the **DB Audit Logging** page, click **Enable** in the upper-right corner.
    4. In the **Database Audit Log Storage Configuration** dialog, locate the **Alibaba Cloud RAM Policy Settings** section, and record **TiDB Cloud Account ID** and **TiDB Cloud External ID** for later use.

2. In the Alibaba Cloud console, go to **RAM** > **Permissions** > **Policies**, and then check whether a policy already exists with the `oss:PutObject` write-only permission for your audit log OSS bucket.

    - If yes, record the policy name for later use.

    - If not, click **Create Policy**, and define the policy using the following policy template.

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": [
                "oss:PutObject"
            ],
            "Resource": "acs:oss:*:*:<Your-Bucket-Name>/*"
            }
        ]
        }
        ```

    Replace `<Your-Bucket-Name>` with the name of your OSS bucket where TiDB Cloud will write audit logs. For example, if your bucket name is `auditlog-bucket`, use: `"Resource": "acs:oss:*:*:auditlog-bucket/*"`.

3. In the Alibaba Cloud console, go to **RAM** > **Identities** > **Roles**, and then check whether a role already exists whose **trusted entity** matches the TiDB Cloud Account ID and External ID you recorded earlier.

    - If yes, record the role name for later use.

    - If not, click **Create Role** by taking the following steps.

        1. In the role creation page, click **Switch to Policy Editor**.
        2. Under **Principal**, choose **Cloud Account** and enter the **TiDB Cloud Account Id** in the field.
        3. Under **Action**, select **sts:AssumeRole** from the drop-down list.
        4. Click **Add condition**, and then configure the condition as follows:
            - Set **Key** to ``sts:ExternalId``.
            - Set **Operator** to ``StringEquals``.
            - Set **Value** to the **TiDB Cloud External ID**.
        5. Click **OK** to open the **Create Role** dialog.
        6. Enter the role name in the **Role Name** field, and click **OK** to create the role.

4. After the role is created, go to the **Permissions** tab and click **Grant Permission**.

    In the dialog, configure the following settings:

    - For **Resource Scope**, select **Account**.
    - In the **Policy** field, select the OSS write policy created earlier.
    - Click **Grant Permissions**.

5. Copy the **Role ARN** (for example: `acs:ram::<Your-Account-ID>:role/tidb-cloud-audit-role`) for later use.

#### Step 3. Enable audit logging

In the TiDB Cloud console, go back to the **Database Audit Log Storage Configuration** dialog where you got the TiDB Cloud account ID, and then take the following steps:

1. In the **Bucket URI** field, enter the URI of your OSS bucket. For example, ``oss://tidb-cloud-audit-log``.
2. In the **Bucket Region** field, select the Alibaba Cloud region where the bucket is located (recommended to match your TiDB instance region).
3. In the **Role ARN** field, paste the Role ARN value copied in [Step 2. Configure the OSS access](#step-2-configure-oss-access).
4. Click **Test Connection** to verify whether TiDB Cloud can access and write to the OSS bucket.

    - If it is successful, **The connection is successful** is displayed.
    - If not, check the OSS bucket permissions, RAM role configuration, and policy.

5. Click **Enable** to activate audit logging for the instance.

    TiDB Cloud is ready to write audit logs for the specified instance to your OSS bucket.

> **Note:**
>
> - After enabling audit logging, if you make any new changes to the bucket URI or location, you must click **Test Connection** again to verify that TiDB Cloud can connect to the bucket. Then, click **Enable** to apply the changes.
> - To remove TiDB Cloud's access to your OSS bucket, delete the trust policy granted to this instance in the Alibaba Cloud console.

</CustomContent>

## Specify auditing filter rules

After enabling audit logging, you must specify auditing filter rules to control which user access events to capture and write to audit logs. If no filter rules are specified, TiDB Cloud does not log anything.

To specify auditing filter rules for an instance, take the following steps:

1. On the **DB Audit Logging** page, click **Add Filter Rule** in the **Log Filter Rules** section to add an audit filter rule.

    You can add one audit rule at a time. Each rule specifies a user expression, database expression, table expression, and access type. You can add multiple audit rules to meet your auditing requirements.

2. In the **Log Filter Rules** section, click **>** to expand and view the list of audit rules you have added.

> **Note:**
>
> - The filter rules are regular expressions and case-sensitive. If you use the wildcard rule `.*`, all users, databases, or table events in the instance are logged.
> - Because audit logging consumes instance resources, be prudent when specifying filter rules. To minimize the consumption, it is recommended that you specify filter rules to limit the scope of audit logging to specific database objects, users, and actions, where possible.

## View audit logs

By default, TiDB Cloud stores database audit log files in your storage service, so you need to read the audit log information from your storage service.

TiDB Cloud audit logs are readable text files with the instance ID, internal ID, and log creation date incorporated into the fully qualified filenames.

For example, `13796619446086334065/tidb-5m5z34/tidb-audit-2022-04-21T18-16-29.529.log`. In this example, `13796619446086334065` indicates the instance ID and `tidb-5m5z34` indicates the internal ID.

## Disable audit logging

If you no longer want to audit an instance, go to the page of the instance, click **Settings** > **Audit Settings**, and then toggle the audit setting in the upper-right corner to **Disable**.

> **Note:**
>
> Each time the size of the log file reaches 10 MiB, the log file is pushed to the cloud storage bucket. Therefore, after audit logging is disabled, the log file whose size is smaller than 10 MiB will not be automatically pushed to the cloud storage bucket. To get the log file in this situation, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

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
    | 21 | SERVER_PORT | INTEGER |  | The port that the TiDB server uses to listen to client communication via the MySQL protocol |
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
