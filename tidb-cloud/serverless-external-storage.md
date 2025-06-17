---
title: Configure TiDB Cloud Serverless External Storage Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access.
---

# Configure External Storage Access for TiDB Cloud Serverless

If you want to import data from or export data to an external storage in a TiDB Cloud Serverless cluster, you need to configure cross-account access. This document describes how to configure access to an external storage for TiDB Cloud Serverless clusters.

If you need to configure these external storages for a TiDB Cloud Dedicated cluster, see [Configure External Storage Access for TiDB Cloud Dedicated](/tidb-cloud/dedicated-external-storage.md).

## Configure Amazon S3 access

To allow a TiDB Cloud Serverless cluster to access the source data in your Amazon S3 bucket, configure the bucket access for the cluster using either of the following methods:

- [Use a Role ARN](#configure-amazon-s3-access-using-a-role-arn): use a Role ARN to access your Amazon S3 bucket.
- [Use an AWS access key](#configure-amazon-s3-access-using-an-aws-access-key): use the access key of an IAM user to access your Amazon S3 bucket.

### Configure Amazon S3 access using a Role ARN

It is recommended that you use [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) to create a role ARN. Take the following steps to create one:

> **Note:**
>
> Role ARN access to Amazon S3 is only supported for clusters with AWS as the cloud provider. If you use a different cloud provider, use an AWS access key instead. For more information, see [Configure Amazon S3 access using an AWS access key](#configure-amazon-s3-access-using-an-aws-access-key).

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Open the **Add New ARN** dialog.

    - If you want to import data from Amazon S3, open the **Add New ARN** dialog as follows:

        1. Click **Import from S3**.
        2. Fill in the **File URI** field.
        3. Choose **AWS Role ARN** and click **Click here to create new one with AWS CloudFormation**.

    - If you want to export data to Amazon S3, open the **Add New ARN** dialog as follows:

        1. Click **Export data to...**  > **Amazon S3**. If your cluster has neither imported nor exported any data before, click **Click here to export data to...** > **Amazon S3** at the bottom of the page.
        2. Fill in the **Folder URI** field.
        3. Choose **AWS Role ARN** and click **Click here to create new one with AWS CloudFormation**.

3. Create a role ARN with an AWS CloudFormation template.

    1. In the **Add New ARN** dialog, click **AWS Console with CloudFormation Template**.

    2. Log in to the [AWS Management Console](https://console.aws.amazon.com) and you will be redirected to the AWS CloudFormation **Quick create stack** page.

    3. Fill in the **Role Name**.

    4. Acknowledge to create a new role and click **Create stack** to create the role ARN.

    5. After the CloudFormation stack is executed, you can click the **Outputs** tab and find the Role ARN value in the **Value** column.

        ![img.png](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

If you have any trouble creating a role ARN with AWS CloudFormation, you can take the following steps to create one manually:

<details>
<summary>Click here to see details</summary>

1. In the **Add New ARN** dialog described in previous instructions, click **Having trouble? Create Role ARN manually**. You will get the **TiDB Cloud Account ID** and **TiDB Cloud External ID**.

2. In the AWS Management Console, create a managed policy for your Amazon S3 bucket.

    1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/) and open the [Amazon S3 console](https://console.aws.amazon.com/s3/).

    2. In the **Buckets** list, choose the name of your bucket with the source data, and then click **Copy ARN** to get your S3 bucket ARN (for example, `arn:aws:s3:::tidb-cloud-source-data`). Take a note of the bucket ARN for later use.

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. Open the [IAM console](https://console.aws.amazon.com/iam/), click **Policies** in the left navigation pane, and then click **Create Policy**.

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. On the **Create policy** page, click the **JSON** tab.

    5. Configure the policy in the policy text field according to your needs. The following is an example that you can use to export data from and import data into a TiDB Cloud Serverless cluster.

        - Exporting data from a TiDB Cloud Serverless cluster needs the **s3:PutObject** and **s3:ListBucket** permissions.
        - Importing data into a TiDB Cloud Serverless cluster needs the **s3:GetObject**, **s3:GetObjectVersion**, and **s3:ListBucket** permissions.

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        In the policy text field, replace the following configurations with your own values.

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`. For example:

            - If your source data is stored in the root directory of the `tidb-cloud-source-data` bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`.
            - If your source data is stored in the `mydata` directory of the bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`.

          Make sure that `/*` is added to the end of the directory so TiDB Cloud can access all files in this directory.

        - `"Resource": "<Your S3 bucket ARN>"`, for example, `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`.

        - If you have enabled AWS Key Management Service key (SSE-KMS) with customer-managed key encryption, make sure the following configuration is included in the policy. `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is a sample KMS key of the bucket.

            ```
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

        - If the objects in your bucket have been copied from another encrypted bucket, the KMS key value needs to include the keys of both buckets. For example, `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`.

    6. Click **Next**.

    7. Set a policy name, add a tag of the policy (optional), and then click **Create policy**.

3. In the AWS Management Console, create an access role for TiDB Cloud and get the role ARN.

    1. In the [IAM console](https://console.aws.amazon.com/iam/), click **Roles** in the left navigation pane, and then click **Create role**.

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. To create a role, fill in the following information:

        - In **Trusted entity type**, select **AWS account**.
        - In **An AWS account**, select **Another AWS account**, and then paste the TiDB Cloud account ID to the **Account ID** field.
        - In **Options**, click **Require external ID (Best practice when a third party will assume this role)**, and then paste the TiDB Cloud External ID to the **External ID** field. If the role is created without a Require external ID, once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project can use the same Role ARN to access your Amazon S3 bucket. If the role is created with the account ID and external ID, only the corresponding TiDB cluster can access the bucket.

    3. Click **Next** to open the policy list, choose the policy you just created, and then click **Next**.

    4. In **Role details**, set a name for the role, and then click **Create role** in the lower-right corner. After the role is created, the list of roles is displayed.

    5. In the list of roles, click the name of the role that you just created to go to its summary page, and then you can get the role ARN.

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### Configure Amazon S3 access using an AWS access key

It is recommended that you use an IAM user (instead of the AWS account root user) to create an access key.

Take the following steps to configure an access key:

1. Create an IAM user. For more information, see [creating an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).

2. Use your AWS account ID or account alias, and your IAM user name and password to sign in to [the IAM console](https://console.aws.amazon.com/iam).

3. Create an access key. For more information, see [creating an access key for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).

> **Note:**
>
> TiDB Cloud does not store your access keys. It is recommended that you [delete the access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) after the import or export is complete.

## Configure GCS access

To allow a TiDB Cloud Serverless cluster to access your GCS bucket, you need to configure the GCS access for the bucket. You can use a service account key to configure the bucket access:

Take the following steps to configure a service account key:

1. On the Google Cloud [service account page](https://console.cloud.google.com/iam-admin/serviceaccounts), click **CREATE SERVICE ACCOUNT** to create a service account. For more information, see [Creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts).

    1. Enter a service account name.
    2. Optional: Enter a description of the service account.
    3. Click **CREATE AND CONTINUE** to create the service account.
    4. In the `Grant this service account access to project`, choose the [IAM roles](https://cloud.google.com/iam/docs/understanding-roles) with the needed permission.

        - Exporting data from a TiDB Cloud Serverless cluster needs a role with `storage.objects.create` permission.
        - Importing data into a TiDB Cloud Serverless cluster needs a role with `storage.buckets.get`, `storage.objects.get`, and `storage.objects.list` permissions.

    5. Click **Continue** to go to the next step.
    6. Optional: In the `Grant users access to this service account`, choose members that need to [attach the service account to other resources](https://cloud.google.com/iam/docs/attach-service-accounts).
    7. Click **Done** to finish creating the service account.

   ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2. Click the service account, and then click **ADD KEY** on the `KEYS` page to create a service account key.

   ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3. Choose the default `JSON` key type, and then click **CREATE** to download the Google Cloud credentials file. The file contains the service account key that you need to use when configuring the GCS access for the TiDB Cloud Serverless cluster.

## Configure Azure Blob Storage access

To allow TiDB Cloud Serverless to access your Azure Blob container, you need to create a service SAS token for the container.

You can create a SAS token either using an [Azure ARM template](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview) (recommended) or manual configuration. 

To create a SAS token using an Azure ARM template, take the following steps:

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Open the **Generate New SAS Token via ARM Template Deployment** dialog.
        
    1. Click **Export data to...**  > **Azure Blob Storage**. If your cluster has neither imported nor exported any data before, click **Click here to export data to...** > **Azure Blob Storage** at the bottom of the page.
   
    2. Scroll down to the **Azure Blob Storage Settings** area, and then click **Click here to create a new one with Azure ARM template** under the SAS Token field. 
   
3. Create a SAS token with the Azure ARM template.

    1. In the **Generate New SAS Token via ARM Template Deployment** dialog, click **Click to open the Azure Portal with the pre-configured ARM template**.
   
    2. After logging in to Azure, you will be redirected to the Azure **Custom deployment** page.

    3. Fill in the **Resource group** and **Storage Account Name** in the **Custom deployment** page. You can get all the information from the storage account overview page where the container is located.

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4. Click **Review + create** or **Next** to review the deployment. Click **Create** to start the deployment.
   
    5. After it completes, you will be redirected to the deployment overview page. Navigate to the **Outputs** section to get the SAS token.

If you have any trouble creating a SAS token with the Azure ARM template, take the following steps to create one manually:

<details>
<summary>Click here to see details</summary>

1. On the [Azure Storage account](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) page, click your storage account to which the container belongs.
   
2. On your **Storage account** page, click the **Security+network**, and then click **Shared access signature**.

   ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3. On the **Shared access signature** page, create a service SAS token with needed permissions as follows. For more information, see [Create a service SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview).

    1. In the **Allowed services** section, choose the **Blob** service.
    2. In the **Allowed Resource types** section, choose **Container** and **Object**.
    3. In the **Allowed permissions** section, choose the permission as needed.

        - Exporting data from a TiDB Cloud Serverless cluster needs the **Read** and **Write** permissions.
        - Importing data into a TiDB Cloud Serverless cluster needs the **Read** and **List** permissions.

    4. Adjust **Start and expiry date/time** as needed.
    5. You can keep the default values for other settings.

   ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4. Click **Generate SAS and connection string** to generate the SAS token.

</details>

## Configure Alibaba Cloud Object Storage Service (OSS) access

To allow TiDB Cloud Serverless to access your Alibaba Cloud OSS bucket, you need to create an AccessKey pair for the bucket.

Take the following steps to configure an AccessKey pair:

1. Create a RAM user and get the AccessKey pair. For more information, see [Create a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user).
    
    In the **Access Mode** section, select **Using permanent AccessKey to access**.

2. Create a custom policy with the required permissions. For more information, see [Create custom policies](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy).
    
    - In the **Effect** section, select **Allow**.
    - In the **Service** section, select **Object Storage Service**.
    - In the **Action** section, select the permissions as needed.
   
        To import data into a TiDB Cloud Serverless cluster, grant **oss:GetObject**, **oss:GetBucketInfo**, and **oss:ListObjects** permissions.

        To export data from a TiDB Cloud Serverless cluster, grant **oss:PutObject**, **oss:GetBucketInfo**, and **oss:ListBuckets** permissions.
        
    - In the **Resource** section, select the bucket and the objects in the bucket.

3. Attach the custom policies to the RAM user. For more information, see [Grant permissions to a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user).
