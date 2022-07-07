---
title: Troubleshoot Permission Errors during Data Import from S3
summary: Learn how to troubleshoot permission errors when importing data from Amazon S3 to TiDB Cloud.
---

# Troubleshoot Permission Errors during Data Import from S3

This document introduces how to troubleshoot permission errors that might occur when you [import data from Amazon S3 into TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-3-copy-source-data-files-to-amazon-s3-and-import-data-into-tidb-cloud).

After clicking **Import** on the **Data Import Task** page on the TiDB Cloud console, if you see an error message with the keyword `AccessDenied`, a permission error has occurred.

To troubleshoot the permission error, perform the following checks in the AWS Management Console.

## Check the policy of the IAM role

In the AWS Management Console, go to **IAM** > **Access Management** > **Roles**, find the role you have created for the target TiDB cluster, and check the **Permission policies**. Check each policy and make sure that the `Resource` fields in each policy is correctly configured. The following is a sample policy:

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

- Pay attention to the line of `"arn:aws:s3:::tidbcloud-samples-sun-encry-kms-bucket/*"`. This is your customized directory that you can customize in your S3 bucket root level for data storage. This directory need to end with `/*`, for example, `"arn:aws:s3:::<bucket>/<sub-dir>/*"`. If you fill in with `"arn:aws:s3:::<bucket-name>"`, the `AccessDenied` error occurs.
- The line of `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is the KMS key of the bucket.
    - If you have enabled AWS Key Management Service key (SSE-KMS) with customer-managed key encryption, make sure that you have granted the `kms:Decrypt` permission to the role you have used to import data to TiDB Cloud.
    - If the objects in your bucket have been copied from another encrypted bucket, the KMS key value need to include the keys of both buckets. For example, `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`.

If your policy is not correctly configured as the preceding example shows, correct the `Resource` fields in your policy and try to import data again.

> **Tip:**
>
> If you have updated the permission policy multiple times and still get the `AccessDenied` error during data import, you can try to revoke active sessions. Go to **IAM** > **Access Management** > **Roles**, find **Revoke active sessions** and click the button to revoke active sessions. Then, retry the data import.
>
> Note that this might affect your other applications.

## Check the bucket policy

In the AWS Management Console, open the Amazon S3 console, go to **Bucket** > **Permissions**, and find the **Bucket policy** page. By default, this page has no policy value. If any denied policy is displayed, the `AccessDenied` error might occur.

If you see a denied policy, check whether the policy relates to the current data import. If yes, delete it on the page and retry the data import.

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

To handle the error, click **edit** on the upper right corner of the page and change the ownership to "Bucket owner enforced". Note that this might affect your other applications that are using this bucket.

## Check your bucket encryption type

There are more than one way to encrypt an S3 bucket. When you try to access the objects in a bucket, the role you have created must have the permission to access the encryption key for data decryption. Otherwise, the `AccessDenied` error occurs.

To check the encryption type of your bucket, open the Amazon S3 console in the AWS Management console, choose the name of the target bucket, choose **Properties**, and you will see the **Default encryption** page that shows the encryption type of the bucket.

There are two types of server-side encryption: Amazon S3-managed key (SSE-S3) and AWS Key Management Service (SSE-KMS). For SSE-S3, further check is not needed because this encryption type does not cause permission errors. For SSE-KMS, you need to check the following:

- If the AWS KMS key ARN on the page is in black color without underline, the AWS KMS key is an AWS-managed key (aws/s3).
- If the AWS KMS key ARN on the page is in blue color with underline, click the key ARN to see the specific encryption type. It might be an AWS managed key (aws/s3) or a customer-managed key.

<details>
<summary>For the AWS managed key (aws/s3) in SSE-KMS</summary>
<br />

In this situation, if the `AccessDenied` error occurs, the reason might be that the key is read-only and cross-account permission grants is not allowed. See the AWS article [Why are cross-account users getting Access Denied errors when they try to access S3 objects encrypted by a custom AWS KMS key](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/) for details.

To handle the permission error, click **edit** on the upper right corner of the **Default encryption** page, and change the AWS KMS key to "Choose from your AWS KMS keys" or "Enter AWS KMS key ARN", or change the server-side encryption method to "AWS S3 Managed Key (SSE-S3). In addition to this method, you can also create a new bucket and use the custom-managed key or the SSE-S3 encryption method.
</details>

<details>
<summary>For the customer-managed key in SSE-KMS</summary>
<br />

To handle the `AccessDenied` error in this situation, click the key ARN or manually find the key in KMS. A **Key users** page is displayed. Click **Add** on the upper right corner of the page to add the role you have used to import data to TiDB Cloud. Then, try to import data again.

</details>

> **Note:**
>
> If the objects in your bucket have been copied from an existing encrypted bucket, you also need to include the key of the source bucket in the AWS KMS key ARN. This is because the objects in the your bucket use the same encryption method as the source object encryption. For more information, see the AWS document [Using default encryption with replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html).

## Check the AWS article for instruction

If you have performed all the checks above and still get the `AccessDenied` error, you can check the AWS article [How do I troubleshoot 403 Access Denied errors from Amazon S3](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/) for instruction.
