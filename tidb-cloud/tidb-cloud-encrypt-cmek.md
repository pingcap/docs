---
title: Encryption at Rest using Customer-Managemented Encryption Keys
summary: Learn about how to use CMEK in TiDB Cloud.
---

# Encryption at Rest using Customer-Managemented Encryption Keys

Customer-Managed Encryption Key (CMEK) allows you to protect your static data in a TiDB Cloud Dedicated Tier using a cryptographic key that is completely controlled by you. This key is called a CMEK key.

After you configure the CMEK capability for a project, the static data in all clusters created in this project will be encrypted using this CMEK. At the same time, the backup data created by these clusters will also be encrypted using the same key. If you do not enable CMEK, TiDB Cloud will use an escrow key to encrypt all data of your cluster at rest.

> **Note:**
>
> Currently this feature is only available upon request. If you need to try out this feature, contact [support](/tidb-cloud/tidb-cloud-support.md).

## Restrictions

- Currently, TiDB Cloud only supports using AWS KMS to provide CMEK.
- To use the CMEK capability, you need to determine whether to enable the CMEK key during project creation and complete CMEK-related configurations before creating a cluster. Enabling CMEK capabilities in existing projects is not supported.
- Currently, in CMEK-enabled projects, you can only create [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters hosted on AWS. Dedicated Tier clusters hosted on GCP and [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters are not supported.
- Currently, for a particular project, CMEK can only be configured for one AWS region. Once configured, you cannot create clusters in other regions in the same project.

## Enable CMEK

If you want to encrypt your data using the KMS owned in your own account, take the following steps.

### Step 1. Provision KMS and IAM in your cloud provider

1. Create your CMEK Key on the AWS Key Management Service (KMS) console. Copy the KMS Key ARN. To learn how to create a key, see [Creating Keys](http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk) in the AWS documentation.
2. Create an IAM role and configure the role's access policy to CMEK.

    To make the TiDB cluster function as expected, you need to grant certain permissions to the TiDB account for accessing KMS. Note that this feature is in the development stage and the policy requirement could be subject to change as future features might require more permissions. Here’re the required permissions for supported features at present:

    ```json
    {
        "Version": "2012-10-17",
        "Id": "cmek-policy",
        "Statement": [
            // EBS-related policy
            {
                "Sid": "Allow access through EBS for all principals in the account that are authorized to use EBS",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:CreateGrant",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": "<pingcap-account>",
                        "kms:ViaService": "ec2.us-west-2.amazonaws.com"
                    }
                }
            },
            {
                "Sid": "Allow TiDB cloud role to use KMS to store encrypted backup to S3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<pingcap-account>:root"
                },
                "Action": [
                    "kms:Decrypt",
                    "kms:GenerateDataKey"
                ],
                "Resource": "*"
            },
            ... // user's own admin access to KMS
        ]
    }
    ```

> **Note:**
>
> - <pingcap-account> will be provided separately through documentation or by other means, which is the account where customer clusters run in.
> - For EBS related policy in the first block, please refer to [aws doc](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account) for reference.
> - For S3 related policy in the second block, please refer to [aws blog](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption) for reference.

### Step 2. Create a new project and enable CMEK

1. Using TiDB Cloud Open API, create a new project and enable AWS CMEK. 
2. Configure the KMS Key ARN for the specified region (e.g., us-east-1) under this project using TiDB Cloud Open API.

> **Note:**
>
> Currently the configuration is not available on UI, user can configure the project using TiDB cloud’s OpenAPI restful interface.

### Step 3. Create a cluster

Create an AWS Dedicated Cluster under the project created in step 1. You need to ensure that the region where the cluster is located is the same as that in step 2.

> **Note:**
>
> When CMEK is enabled, the EBS volumes used by the nodes of the cluster and the S3 used for the cluster backups are encrypted using CMEK.

## Rotate your CMEK

You can configure [automatic CMEK rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) on AWS KMS. AWS automatic CMEK rotation does not require you to update the TiDB Cloud Encryption at Rest project settings, including the CMEK ID.

## Revoke and restore CMEK

In the case PingCAP’s access to the CMEK needs to be temporarily revoked, the user needs to follow these steps:

1. The user needs to revoke the corresponding permissions and update the KMS Key policy on the AWS KMS console.
2. Pause all the clusters under the project on the TiDB Cloud console.

> **Note:**
>
> If you are just revoking the CMEK on AWS KMS, this will not affect the running cluster. If you have revoked the CMEK, when you pause the cluster and then restore the cluster, the cluster will not be able to restore normally because it can not access the CMEK.

Steps to restore CMEK

1. You need to restore the CMEK access policy on the AWS KMS console.
2. You need to restore all clusters under the project on the TiDB cloud console.
