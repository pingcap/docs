---
title: Troubleshoot Permission Errors during Data Import from S3
summary: Learn how to troubleshoot permission errors when importing data from Amazon S3 to TiDB Cloud.
---

# Troubleshoot Permission Errors during Data Import from S3

This document introduces how to troubleshoot permission-type errors that might occur when you [import data from Amazon S3 into TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-3-copy-source-data-files-to-amazon-s3-and-import-data-into-tidb-cloud).

If you see an error message with the keyword `AccessDenied` after clicking **Import** on the **Data Import Task** page on the TiDB Cloud console, a permission-type error has occurred.

To troubleshoot and fix the permission-type error, perform the following checks in the AWS Management Console one by one.

## Check the permission policy

In the AWS Management Console, go to **IAM** > **Access Management** > **Policies**, find the permission policy that you have created for the target TiDB cluster. Make sure that the `Resource` fields in the policy is correctly configured. The following is a sample policy with **correct `Resource` configuration**:

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
            "Resource": [
                "arn:aws:s3:::tidbcloud-samples-sun-encry-kms-bucket/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::tidbcloud-samples-sun-encry-kms-bucket"
            ]
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

In this sample policy:

- Pay attention to the line of `"arn:aws:s3:::tidbcloud-samples-sun-encry-kms-bucket/*"`. This is your customized directory that you can customize in your S3 bucket root level for data storage. This directory is expected to end with `/*`, for example, `"arn:aws:s3:::<bucket>/<sub-dir>/*"`. If you fill in with `"arn:aws:s3:::<bucket-name>"` instead, the `AccessDenied` error will occur.
- The line of `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is the KMS key of the bucket. If the objects on the bucket have been copied from another encrypted bucket, `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is expected to contain the keys of both buckets.

If your policy is not correctly configured as the preceding example shows, correct the `Resource` fields in your policy and try the data import again.

> **Tip:**
>
> If you have updated the permission policy for multiple times and still get the `AccessDenied` error during data import, you can try to revoke active sessions. Go to **IAM** > **Access Management** > **Roles**, find **Revoke active sessions** and click the button to revoke active sessions. Then, retry the data import.
>
> Note that this might affect your other applications.

## Check the bucket policy

In the AWS Management Console, open the Amazon S3 console, go to **Bucket** > **Permissions**, and find the **Bucket policy** panel. By default, this panel has no policy value. If any denied policy is displayed in the panel, the `AccessDenied` error might occur.

If you see a denied policy, delete it in the panel and retry the data import.

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

In the AWS Management Console, open the Amazon S3 console, go to **Bucket** > **Permissions**, and find the **Object Ownership** panel. Make sure that the "Object Ownership" configuration is "Bucket owner enforced".

If the configuration is not "Bucket owner enforced", the `AccessDenied` error will occur, because your account does not have enough permissions for all objects in this bucket.

To handle the error, click **edit** on the upper right corner of the panel and change the ownership to "Bucket owner enforced". Note that this might affect your other applications that are using this bucket.

## Check your bucket encryption type

There are multiple ways to encrypt an S3 bucket. When you try to access the objects in a bucket, the role you have created must have the permission to access the encryption key for data decryption. Otherwise, the `AccessDenied` error will occur.

To check the encryption type of your bucket, open the Amazon S3 console in the AWS Management console, choose the name of the target bucket, choose **Properties**, and you will see the **Default encryption** panel that shows the encryption type of the bucket.

On the **Default encryption** panel:

<details>
<summary>If the server-side encryption is "AWS Key Management Service key (SSE-KMS)" and the AWS KMS key is "AWS managed key (aws/s3)"</summary>
<br />

In this situation, if the `AccessDenied` error occurs, the reason might be that the key is read-only and cross-account permission grants is not allowed. See [Why are cross-account users getting Access Denied errors when they try to access S3 objects encrypted by a custom AWS KMS key](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/) for details.

To handle the permission error, click **edit** at the upper right corner of the **Default encryption** panel, and change the AWS KMS key to "Choose from your AWS KMS keys" or "Enter AWS KMS key ARN", or change the server-side encryption method to "AWS S3 Managed Key (SSE-S3).
</details>

<details>
<summary>If the server-side encryption is "AWS Key Management Service key (SSE-KMS)" and the AWS KMS key is "Enter AWS KMS key ARN" (customer-managed key)</summary>
<br />

To handle the `AccessDenied` error in this situation, click the key ARN or manually find the key in KMS. A **Key users** panel is displayed. Click **Add** at the upper right corner of the panel to add the role you have used to import data to TiDB Cloud. Then, restry the data import.
</details>

## Check the AWS article for instruction

If you have performed all the checks above and still get the `AccessDenied` error, you can check the AWS article [How do I troubleshoot 403 Access Denied errors from Amazon S3?](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/) for instruction.
