---
title: Troubleshoot Permission Errors during Data Import from S3
summary: Learn how to troubleshoot permission errors when importing data from Amazon S3 to TiDB Cloud.
---

# Troubleshoot Permission Errors during Data Import from S3

This document introduces how to troubleshoot permission errors that might occur when you [copy source data files to Amazon S3 and import data into TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-3-copy-source-data-files-to-amazon-s3-and-import-data-into-tidb-cloud).

On the TiDB Cloud console, after clicking **Import** on the **Data Import Task** page, if you see an error message with the keyword `AccessDenied`, a permission-type error has occurred.

To troubleshoot and fix the permission-type error, check the following items in the AWS Management Console one by one.

## Check the storage bucket policy

In the AWS Management Console, go to **IAM** > **Access Management** > **Policies**, find the policy that you have created for the target TiDB cluster. Make sure that the `Resource` field in the policy is correctly configured. The following is a sample policy with **correct `Resource` configuration**:

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

- Pay attention to the line of `"arn:aws:s3:::tidbcloud-samples-sun-encry-kms-bucket/*"`. This is your customized directory that you can customize in your S3 bucket root level for data storage. This directory is expected to end witb `/*`, for example, `"arn:aws:s3:::<bucket>/<sub-dir>/*"`. If you fill in with `"arn:aws:s3:::<bucket-name>"` instead, the `AccessDenied` error will occur.
- The line of `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is the KMS key of the bucket. If the objects on the bucket have been copied from another encrypted bucket, `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is expected to contain the keys of both buckets.

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

In the AWS Management Console, go to **Bucket** > **Permissions**, find the **Object Ownership** panel. Make sure that the "Object Ownership" configuration is "Bucket owner enforced".

If the configuration is not "Bucket owner enforced", the `AccessDenied` error will occur, because your account does not have enough permissions for all objects in this bucket.