---
title: Configure Amazon S3 Access and GCS Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access and Google Cloud Storage (GCS) access.
---

# Configure Amazon S3 Access and GCS Access

If your source data is stored in Amazon S3 or Google Cloud Storage (GCS) buckets, before importing or migrating the data to TiDB Cloud, you need to configure cross-account access to the buckets. This document describes how to do this.

## Configure Amazon S3 access

To allow TiDB Cloud to access the source data in your Amazon S3 bucket, take the following steps to configure the bucket access for TiDB Cloud and get the Role-ARN.

1. In the [TiDB Cloud console](https://tidbcloud.com/), get the TiDB Cloud account ID and external ID of the target TiDB cluster.

    1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

    3. On the **Import** page, click **Import Data** in the upper-right corner and select **From S3**.

    4. On the **Import from S3** page, click **Guide for getting the required Role ARN** to get the TiDB Cloud Account ID and TiDB Cloud External ID. Take a note of these IDs for later use.

2. In the AWS Management Console, create a managed policy for your Amazon S3 bucket.

    1. Sign in to the AWS Management Console and open the Amazon S3 console at <https://console.aws.amazon.com/s3/>.
    2. In the **Buckets** list, choose the name of your bucket with the source data, and then click **Copy ARN** to get your S3 bucket ARN (for example, `arn:aws:s3:::tidb-cloud-source-data`). Take a note of the bucket ARN for later use.

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. Open the IAM console at <https://console.aws.amazon.com/iam/>, click **Policies** in the navigation pane on the left, and then click **Create Policy**.

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. On the **Create policy** page, click the **JSON** tab.
    5. Copy the following access policy template and paste it to the policy text field.

        ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        In the policy text field, update the following configurations to your own values.

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            For example, if your source data is stored in the root directory of the `tidb-cloud-source-data` bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`. If your source data is stored in the `mydata` directory of the bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`. Make sure that `/*` is added to the end of the directory so TiDB Cloud can access all files in this directory.

        - `"Resource": "<Your S3 bucket ARN>"`

            For example, `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`.

    6. Click **Next: Tags**, add a tag of the policy (optional), and then click **Next:Review**.

    7. Set a policy name, and then click **Create policy**.

3. In the AWS Management Console, create an access role for TiDB Cloud and get the role ARN.

    1. In the IAM console at <https://console.aws.amazon.com/iam/>, click **Roles** in the navigation pane on the left, and then click **Create role**.

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. To create a role, fill in the following information:

        - Under **Trusted entity type**, select **AWS account**.
        - Under **An AWS account**, select **Another AWS account**, and then paste the TiDB Cloud account ID to the **Account ID** field.
        - Under **Options**, click **Require external ID (Best practice when a third party will assume this role)**, and then paste the TiDB Cloud External ID to the **External ID** field. If the role is created without "Require external ID", once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can use the same Role-ARN to access your Amazon S3 bucket. If the role is created with the account ID and external ID, only the corresponding TiDB cluster can access the bucket.

    3. Click **Next** to open the policy list, choose the policy you just created, and then click **Next**.
    4. Under **Role details**, set a name for the role, and then click **Create role** in the lower-right corner. After the role is created, the list of roles is displayed.
    5. In the list of roles, click the name of the role that you just created to go to its summary page, and then copy the role ARN.

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4. In the TiDB Cloud console, go to the **Data Import** page where you get the TiDB Cloud account ID and external ID, and then paste the role ARN to the **Role ARN** field.

## Configure GCS access

To allow TiDB Cloud to access the source data in your GCS bucket, you need to configure the GCS access for the bucket. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can access the GCS bucket.

1. In the TiDB Cloud console, get the Google Cloud Service Account ID of the target TiDB cluster.

    1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

    3. Click **Import Data** in the upper-right corner, click **Show Google Cloud Service Account ID**, and then copy the Service Account ID for later use.

2. In the Google Cloud Platform (GCP) Management Console, create an IAM role for your GCS bucket.

    1. Sign in to the [GCP Management Console](https://console.cloud.google.com/).
    2. Go to the [Roles](https://console.cloud.google.com/iam-admin/roles) page, and then click **CREATE ROLE**.

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3. Enter a name, description, ID, and role launch stage for the role. The role name cannot be changed after the role is created.
    4. Click **ADD PERMISSIONS**.
    5. Add the following read-only permissions to the role, and then click **Add**.

        - storage.buckets.get
        - storage.objects.get
        - storage.objects.list

        You can copy a permission name to the **Enter property name or value** field as a filter query, and choose the name in the filter result. To add the three permissions, you can use **OR** between the permission names.

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3. Go to the [Bucket](https://console.cloud.google.com/storage/browser) page, and click the name of the GCS bucket you want TiDB Cloud to access.

4. On the **Bucket details** page, click the **PERMISSIONS** tab, and then click **GRANT ACCESS**.

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5. Fill in the following information to grant access to your bucket, and then click **SAVE**.

    - In the **New Principals** field, paste the Google Cloud Service Account ID of the target TiDB cluster.
    - In the **Select a role** drop-down list, type the name of the IAM role you just created, and then choose the name from the filter result.

    > **Note:**
    >
    > To remove the access to TiDB Cloud, you can simply remove the access that you have granted.

6. On the **Bucket details** page, click the **OBJECTS** tab.

    If you want to copy a file's gsutil URI, select the file, click **Open object overflow menu**, and then click **Copy gsutil URI**.

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    If you want to use a folder's gsutil URI, open the folder, and then click the copy button following the folder name to copy the folder name. After that, you need to add `gs://` to the beginning and `/` to the end of the name to get a correct URI of the folder.

    For example, if the folder name is `tidb-cloud-source-data`, you need to use `gs://tidb-cloud-source-data/` as the URI.

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7. In the TiDB Cloud console, go to the **Data Import** page where you get the Google Cloud Service Account ID, and then paste the GCS bucket gsutil URI to the **Bucket gsutil URI** field. For example, paste `gs://tidb-cloud-source-data/`.
