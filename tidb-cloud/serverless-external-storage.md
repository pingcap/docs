---
title: Configure TiDB Serverless External Storage Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access, Google Cloud Storage (GCS) access and Azure Blob Storage access.
---

# Configure External Storage Access for TiDB Serverless

If you want import data from or export data to external storage in TiDB Serverless, you need to configure cross-account access. This document describes how to configure access to an external storage, including Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS) and Azure Blob Storage for TiDB Serverless.

If you need to configure these external storages for TiDB Dedicated, see [Configure Amazon S3 Access and GCS Access for TiDB Dedicated](/tidb-cloud/config-s3-and-gcs-access.md).

## Configure Amazon S3 access

To allow TiDB Serverless to access your Amazon S3 bucket, you need to configure the bucket access for TiDB Serverless. You can use either of the following methods to configure the bucket access:

- Use an AWS access key: use the access key of an IAM user to access your Amazon S3 bucket.
- Use a Role ARN: use a Role ARN to access your Amazon S3 bucket.

<SimpleTab>
<div label="Role ARN">

</div>
<div label="Access Key">

It is recommended that you use an IAM user (instead of the AWS account root user) to create an access key.

Take the following steps to configure an access key:

1. Create an IAM user. For more information, see [Creating an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).

2. Use your AWS account ID or account alias, and your IAM user name and password to sign in to [the IAM console](https://console.aws.amazon.com/iam).

3. Create an access key. For more details, see [Creating an access key for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).

> **Note:**
>
> TiDB Cloud does not store your access keys. It is recommended that you [delete the access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) after the import is complete.

</div>
</SimpleTab>

## Configure GCS access

To allow TiDB Serverless to access your GCS bucket, you need to configure the GCS access for the bucket. You can use service account key to configure the bucket access:

Take the following steps to configure a service account key:

1. Create a service account with needed permission in the Google Cloud [service account page](https://console.cloud.google.com/iam-admin/serviceaccounts). For more information, see [Creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts).
   1. Enter a service account name.
   2. Enter a description of the service account (Optional). 
   3. Click **CREATE AND CONTINUE** to create the service account and continue the next step.
   4. In the `Grant this service account access to project`, choose the [IAM roles](https://cloud.google.com/iam/docs/understanding-roles) with needed permission. For example, TiDB Serverless export needs a role with `storage.objects.create` permission.
   5. Click **Continue** to the next step.
   6. Optional: In the `Grant users access to this service account`, choose members that need to [attach the service account to other resources](https://cloud.google.com/iam/docs/attach-service-accounts).
   7. Click **Done** to finish creating the service account.

   ![img.png](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2. Click the service account and then click the **ADD KEY** button in the `KEYS` page to create a service account key. 

    ![img.png](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3. Choose the default `JSON` key type and click the **CREATE** button to download the service account key.

4. Open the downloaded JSON file and encode the content with base64. For example, you can use the following command to encode the content in the macOS terminal:

    ```bash
    base64 -i gcp-xxx.json
    ```

## Configure Azure Blob access

To allow TiDB Serverless to access your Azure Blob container, you need to configure the Azure Blob access for the container. You can use service SAS token to configure the container access:

Take the following steps to configure a service SAS token:

1. Click your storage account where the container belongs to in the [Azure storage account](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) page.

2. In your `storage account` page, click the **Security+network** and then click the **Shared access signature**.

    ![img.png](/media/tidb-cloud/serverless-external-storage/azure-sas.png)

3. In the `Shared access signature` page, create a service SAS token with needed permission. For more information, see [Create a service SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview).
   1. Choose the `Blob` service under the `Allowed services` section.
   2. Choose the `Container` and `Object` under the `Allowed Resource types` section.
   3. Choose the permission under the `Allowed permissions` section as you needed. For example: TiDB Serverless exports needs `Read` and `Write` permission.
   4. Adjust the `Start and expiry date/time` as you needed.
   5. You can keep other settings as default.

   ![img.png](/media/tidb-cloud/serverless-external-storage/azure-create-sas.png)

4. Click the **Generate SAS and connection string** button to generate the SAS token.
