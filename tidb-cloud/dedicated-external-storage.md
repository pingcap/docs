---
title: Configure External Storage Access for TiDB Cloud Dedicated
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS), and Azure Blob Storage access.
aliases: ['/tidb-cloud/config-s3-and-gcs-access']
---

# Configure External Storage Access for TiDB Cloud Dedicated

If your source data is stored in Amazon S3 buckets, Azure Blob Storage containers, or Google Cloud Storage (GCS) buckets, before importing or migrating the data to TiDB Cloud, you need to configure cross-account access to the buckets. This document describes how to do this for TiDB Cloud Dedicated clusters.

If you need to configure these external storages for TiDB Cloud Serverless clusters, see [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md).

## Configure Amazon S3 access

To allow a TiDB Cloud Dedicated cluster to access the source data in your Amazon S3 bucket, configure the bucket access for the cluster using either of the following methods:

- [Use a Role ARN](#configure-amazon-s3-access-using-a-role-arn) (recommended): use a Role ARN to access your Amazon S3 bucket.
- [Use an AWS access key](#configure-amazon-s3-access-using-an-aws-access-key): use the access key of an IAM user to access your Amazon S3 bucket.

### Configure Amazon S3 access using a Role ARN

Configure the bucket access for TiDB Cloud and get the Role ARN as follows:

1. In the [TiDB Cloud console](https://tidbcloud.com/), get the corresponding TiDB Cloud account ID and external ID of the target TiDB cluster.

    1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

    3. Select **Import data from Cloud Storage**, and then click **Amazon S3**.

    4. On the **Import Data from Amazon S3** page, click the link under **Role ARN**. The **Add New Role ARN** dialog is displayed.

    5. Expand **Create Role ARN manually** to get the TiDB Cloud Account ID and TiDB Cloud External ID. Take a note of these IDs for later use.

2. In the AWS Management Console, create a managed policy for your Amazon S3 bucket.

    1. Sign in to the AWS Management Console and open the Amazon S3 console at [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/).
    2. In the **Buckets** list, choose the name of your bucket with the source data, and then click **Copy ARN** to get your S3 bucket ARN (for example, `arn:aws:s3:::tidb-cloud-source-data`). Take a note of the bucket ARN for later use.

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. Open the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/), click **Policies** in the navigation pane on the left, and then click **Create Policy**.

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. On the **Create policy** page, click the **JSON** tab.
    5. Copy the following access policy template and paste it into the policy text field.

        ````json
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

        - If you have enabled AWS Key Management Service key (SSE-KMS) with customer-managed key encryption, make sure the following configuration is included in the policy. `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is a sample KMS key of the bucket.

            ```json
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

            If the objects in your bucket have been copied from another encrypted bucket, the KMS key value needs to include the keys of both buckets. For example, `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`.

    6. Click **Next**.
    7. Set a policy name, add a tag of the policy (optional), and then click **Create policy**.

3. In the AWS Management Console, create an access role for TiDB Cloud and get the role ARN.

    1. In the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/), click **Roles** in the navigation pane on the left, and then click **Create role**.

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. To create a role, fill in the following information:

        - Under **Trusted entity type**, select **AWS account**.
        - Under **An AWS account**, select **Another AWS account**, and then paste the TiDB Cloud account ID to the **Account ID** field.
        - Under **Options**, click **Require external ID** to avoid the [confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html), and then paste the TiDB Cloud External ID to the **External ID** field. If the role is created without "Require external ID", anyone with your S3 bucket URI and IAM role ARN might be able to access your Amazon S3 bucket. If the role is created with both the account ID and external ID, only TiDB clusters running in the same project and the same region can access the bucket.

    3. Click **Next** to open the policy list, choose the policy you just created, and then click **Next**.
    4. Under **Role details**, set a name for the role, and then click **Create role** in the lower-right corner. After the role is created, the list of roles is displayed.
    5. In the list of roles, click the name of the role that you just created to go to its summary page, and then copy the role ARN.

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4. In the TiDB Cloud console, go to the **Data Import** page where you get the TiDB Cloud account ID and external ID, and then paste the role ARN to the **Role ARN** field.

### Configure Amazon S3 access using an AWS access key

It is recommended that you use an IAM user (instead of the AWS account root user) to create an access key.

Take the following steps to configure an access key:

1. Create an IAM user with the following policies:

   - `AmazonS3ReadOnlyAccess`
   - [`CreateOwnAccessKeys` (required) and `ManageOwnAccessKeys` (optional)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

   It is recommended that these policies only work for your bucket that stores the source data.

   For more information, see [Creating an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).

2. Use your AWS account ID or account alias, and your IAM user name and password to sign in to [the IAM console](https://console.aws.amazon.com/iam).

3. Create an access key. For more details, see [Creating an access key for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).

> **Note:**
>
> TiDB Cloud does not store your access keys. It is recommended that you [delete the access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) after the import is complete.

## Configure GCS access

To allow TiDB Cloud to access the source data in your GCS bucket, you need to configure the GCS access for the bucket. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can access the GCS bucket.

1. In the TiDB Cloud console, get the Google Cloud Service Account ID of the target TiDB cluster.

    1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

    3. Select **Import data from Cloud Storage**, and then click **Google Cloud Storage**.

    4. Click **Show Google Cloud Server Account ID**, and then copy the Service Account ID for later use.

2. In the Google Cloud console, create an IAM role for your GCS bucket.

    1. Sign in to the [Google Cloud console](https://console.cloud.google.com/).
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

    If you want to use a folder's gsutil URI, open the folder, and then click the copy button following the folder name to copy the folder name. After that, you need to add `gs://` to the beginning and `/` to the end of the name to get the correct URI for the folder.

    For example, if the folder name is `tidb-cloud-source-data`, you need to use `gs://tidb-cloud-source-data/` as the URI.

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7. In the TiDB Cloud console, go to the **Data Import** page where you get the Google Cloud Service Account ID, and then paste the GCS bucket gsutil URI to the **Bucket gsutil URI** field. For example, paste `gs://tidb-cloud-source-data/`.

## Configure Azure Blob Storage access

To allow TiDB Cloud Dedicated to access your Azure Blob container, you need to configure the Azure Blob access for the container. You can use an account SAS token to configure the container access:

1. On the [Azure Storage account](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) page, click your storage account to which the container belongs.

2. In the navigation pane for your storage account, click **Security + networking** > **Shared access signature**.

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3. On the **Shared access signature** page, create an [account SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) with the necessary permissions as follows:

    1. Under **Allowed services**, select **Blob**.
    2. Under **Allowed resource types**, select **Container** and **Object**.
    3. Under **Allowed permissions**, select the required permissions. For example, importing data to TiDB Cloud Dedicated requires **Read** and **List**.
    4. Adjust **Start and expiry date/time** as needed. For security reasons, it is recommended to set an expiration date that aligns with your data import timeline.
    5. Keep the default values for other settings.

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4. Click **Generate SAS and connection string** to generate the SAS token.

5. Copy the generated **SAS Token**. You will need this token string when configuring the data import in TiDB Cloud.

> **Note:**
>
> Before starting data import, test the connection and permissions to ensure TiDB Cloud Dedicated can access the specified Azure Blob container and files.
