---
title: Troubleshoot Access Denied Errors during Data Import from Amazon S3
summary: Learn how to troubleshoot access denied errors when importing data from Amazon S3 to TiDB Cloud.
---

# Troubleshoot Access Denied Errors during Data Import from Amazon S3

This document describes how to troubleshoot access denied errors that might occur when you import data from Amazon S3 into TiDB Cloud.

After you click **Import** on the **Data Import Task** page of the TiDB Cloud console and confirm the import process, TiDB Cloud starts validating whether it can access your data in your specified bucket URL. If you see an error message with the keyword `AccessDenied`, an access denied error has occurred.

To troubleshoot the access denied errors, perform the following checks in the AWS Management Console.

## Check the policy of the IAM role

In the AWS Management Console, go to **IAM** > **Access Management** > **Roles**, find the role you have created for the target TiDB cluster, and check the **Permission policies**. Check each policy and make sure that the `Resource` fields in each policy are correctly configured.

The following is a sample policy.

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
            "Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data"
        },
        {
            "Sid": "AllowKMSkey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
        }
    ]
}
```

In this sample policy, pay attention to the following:

- In `"arn:aws:s3:::tidb-cloud-source-data/mydata/*"`, `"arn:aws:s3:::tidb-cloud-source-data"` is a sample S3 bucket ARN, and `/mydata/*` is a directory that you can customize in your S3 bucket root level for data storage. The directory needs to end with `/*`, for example, `"<Your S3 bucket ARN>/<Directory of your source data>/*"`. If `/*` is not added, the `AccessDenied` error occurs.

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

    If the objects in your bucket have been copied from another encrypted bucket, the KMS key value needs to include the keys of both buckets. For example, `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`.

If your policy is not correctly configured as the preceding example shows, correct the `Resource` fields in your policy and try importing data again.

> **Tip:**
>
> If you have updated the permission policy multiple times and still get the `AccessDenied` error during data import, you can try to revoke active sessions. Go to **IAM** > **Access Management** > **Roles**, find **Revoke active sessions** and click the button to revoke active sessions. Then, retry the data import.
>
> Note that this might affect your other applications.

## Check the bucket policy

In the AWS Management Console, open the Amazon S3 console, go to **Bucket** > **Permissions**, and find the **Bucket policy** page. By default, this page has no policy value. If any denied policy is displayed on this page, the `AccessDenied` error might occur during data import.

If you see a denied policy, check whether the policy relates to the current data import. If yes, delete it from the page and retry the data import.

## Check the trust entity

In the AWS Management Console, go to **IAM** > **Access Management** > **Roles**, click the **Trust relationships** tab, and you will see the trusted entities.

The following is a sample trust entity:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::380838443567:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe"
                }
            }
        }
    ]
}
```

In the sample trust entity:

- `380838443567` is the TiDB Cloud Account ID. Make sure that this field in your trust entity matches your TiDB Cloud Account ID.
- `696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe` is the TiDB Cloud External ID. Make sure that this field in your trusted entity matches your TiDB Cloud External ID.

## Check the Object Ownership

In the AWS Management Console, open the Amazon S3 console, go to **Bucket** > **Permissions**, and find the **Object Ownership** page. Make sure that the "Object Ownership" configuration is "Bucket owner enforced".

If the configuration is not "Bucket owner enforced", the `AccessDenied` error occurs, because your account does not have enough permissions for all objects in this bucket.

To handle the error, click **Edit** in the upper-right corner of the Object Ownership area and change the ownership to "Bucket owner enforced". Note that this might affect your other applications that are using this bucket.

## Check your bucket encryption type

There are more than one way to encrypt an S3 bucket. When you try to access the objects in a bucket, the role you have created must have the permission to access the encryption key for data decryption. Otherwise, the `AccessDenied` error occurs.

To check the encryption type of your bucket, open the Amazon S3 console in the AWS Management console, choose the name of the target bucket, choose **Properties**, and you will see the **Default encryption** page that shows the encryption type of the bucket.

There are two types of server-side encryption: Amazon S3-managed key (SSE-S3) and AWS Key Management Service (SSE-KMS). For SSE-S3, further check is not needed because this encryption type does not cause access denied errors. For SSE-KMS, you need to check the following:

- If the AWS KMS key ARN on the page is displayed in black without an underline, the AWS KMS key is an AWS-managed key (aws/s3).
- If the AWS KMS key ARN on the page is displayed in blue with an underline, click the key ARN to see the specific encryption type. It might be an AWS managed key (aws/s3) or a customer-managed key.

<details>
<summary>For the AWS managed key (aws/s3) in SSE-KMS</summary>

In this situation, if the `AccessDenied` error occurs, the reason might be that the key is read-only and cross-account permission grants are not allowed. See the AWS article [Why are cross-account users getting Access Denied errors when they try to access S3 objects encrypted by a custom AWS KMS key](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/) for details.

To solve the access denied error, click **Edit** in the upper-right corner of the **Default encryption** page, and change the AWS KMS key to "Choose from your AWS KMS keys" or "Enter AWS KMS key ARN", or change the server-side encryption method to "AWS S3 Managed Key (SSE-S3). In addition to this method, you can also create a new bucket and use the custom-managed key or the SSE-S3 encryption method.
</details>

<details>
<summary>For the customer-managed key in SSE-KMS</summary>

To solve the `AccessDenied` error in this situation, click the key ARN or manually find the key in KMS. A **Key users** page is displayed. Click **Add** in the upper-right corner of the page to add the role you have used to import data to TiDB Cloud. Then, try importing data again.

</details>

> **Note:**
>
> If the objects in your bucket have been copied from an existing encrypted bucket, you also need to include the key of the source bucket in the AWS KMS key ARN. This is because the objects in the your bucket use the same encryption method as the source object encryption. For more information, see the AWS document [Using default encryption with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html).

## Check the AWS article for instruction

If you have performed all the checks above and still get the `AccessDenied` error, you can check the AWS article [How do I troubleshoot 403 Access Denied errors from Amazon S3](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/) for more instruction.
