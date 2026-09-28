---
title: Set Up an Alibaba Cloud OSS External Stage for TiDB Cloud Data Pipeline
summary: Learn how to configure an Alibaba Cloud OSS bucket as the external stage for TiDB Cloud Data Pipeline, including the RAM user and access keys.
---

# Set Up an Alibaba Cloud OSS External Stage for TiDB Cloud Data Pipeline

This guide explains how to prepare an Alibaba Cloud Object Storage Service (OSS) bucket as the external stage for the [TiDB Cloud Data Pipeline](/tidb-cloud/data-pipeline-overview.md). An external stage is the intermediate bucket where TiDB Cloud writes exported snapshots and row changes, and TiDB Cloud Lake reads from it to load data into the target warehouse.

TiDB Cloud writes incremental data and snapshots to your OSS bucket, and TiDB Cloud Lake reads the data from it.

> **Restriction:**
>
> - Only **Access Key** authentication is supported. Role ARN is not available for OSS.
> - Event-driven ingestion with SQS is not supported. The pipeline uses polling only.

## Prerequisites

- An Alibaba Cloud account with permissions to manage OSS and RAM resources.
- A TiDB Cloud account with a TiDB Cloud Lake warehouse.

## Step 1. Create an OSS bucket

> **Tip:**
>
> If you already have an OSS bucket ready, skip this step. Using the same region as your TiDB Cloud instance is recommended but not strictly required for OSS.

1. Open the [OSS Console](https://oss.console.aliyun.com/) and create a new bucket.
2. Select a region. Using the same region as your TiDB Cloud instance is recommended.
3. Optionally, create a folder (prefix) inside the bucket to organize TiDB Cloud data (for example, `oss://tidb-cloud-lake-data/my-cluster/`).
4. Record the following values as you will need them in later steps:

    - **Bucket Name:** for example, `tidb-cloud-lake-data`
    - **OSS URI (with prefix):** for example, `oss://tidb-cloud-lake-data/my-cluster/`

## Step 2. Create a RAM user and AccessKey pair

1. Open the [RAM Console](https://ram.console.aliyun.com/) and go to **Users > Create user**.
2. Enter a display name (for example, `tidb-cloud-lake-user`) and select **OpenAPI calling** as the access method.
3. Click **Next**, then copy and save the **AccessKey ID** and **AccessKey Secret**.

    > **Note:**
    >
    > The AccessKey Secret is only shown once at creation time. Make sure to save it immediately.

4. Return to the **Users** page, click the name of the user you just created, go to the **Permissions** tab, and click **Add permissions**.
5. Select **Custom policy**, click **Create policy**, and then select the **Script** tab to create the policy from the following JSON:

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "oss:ListObjects",
            "oss:GetObject",
            "oss:PutObject",
            "oss:DeleteObject"
          ],
          "Resource": [
            "acs:oss:*:*:YOUR_BUCKET_NAME",
            "acs:oss:*:*:YOUR_BUCKET_NAME/*"
          ]
        }
      ]
    }
    ```

    > **Note:** Replace `YOUR_BUCKET_NAME` with the name of your OSS bucket.

6. Enter a policy name (for example, `tidb-cloud-lake-access`) and click **OK**.
7. Attach the policy to the RAM user.
8. Record the following values as you will need them when configuring TiDB Cloud:
    - **Access Key ID:** for example, `LTAI5t...`
    - **Access Key Secret:** saved at creation time

## Step 3. Configure the External Stage in TiDB Cloud

After the bucket, RAM user, and permissions are ready, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) before configuring an OSS external stage because the required OSS endpoint configuration is not yet finalized.

- **Bucket URI**: the OSS URI from Step 1, such as `oss://tidb-cloud-lake-data/my-cluster/`
- **Access Key ID**: the RAM user's AccessKey ID
- **Access Key Secret**: the RAM user's AccessKey Secret

After TiDB Cloud Support confirms the current OSS configuration requirements, enter the required values in the **External Stage** settings and test the connection.

## What's next?

After completing the Alibaba Cloud setup, you have the following resources ready for the TiDB Cloud Lake **External Stage** configuration:

| Resource | Where to find it |
|----------|------------------|
| **OSS URI** | From Step 1, for example, `oss://tidb-cloud-lake-data/my-cluster/` |
| **Access Key ID** | From Step 2, for example, `LTAI5t...` |
| **Access Key Secret** | From Step 2, saved at creation time |

In the [TiDB Cloud console](https://tidbcloud.com), navigate to the Data Pipeline configuration page for your TiDB Cloud instance, and enter these values in the **External Stage** settings to complete the data pipeline setup.
