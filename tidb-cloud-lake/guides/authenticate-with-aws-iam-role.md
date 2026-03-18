---
title: Authenticate with AWS IAM Role
summary: Cloud-native identity delegation (AWS IAM Role, Azure Managed Identity, Google Service Account federation, etc.) lets Databend Cloud obtain short-lived credentials to your object storage without ever handling raw access keys. That keeps data plane access inside your cloud provider's control plane while you retain ownership of every permission.
---
# Authenticate with AWS IAM Role

Cloud-native identity delegation (AWS IAM Role, Azure Managed Identity, Google Service Account federation, etc.) lets Databend Cloud obtain short-lived credentials to your object storage without ever handling raw access keys. That keeps data plane access inside your cloud provider's control plane while you retain ownership of every permission.

## IAM role benefits

- No static keys: temporary credentials eliminate long-lived secrets to rotate or leak.
- Least privilege: fine-grained policies restrict Databend Cloud to only the buckets and actions you approve.
- Central governance: continue auditing and revoking access through your existing IAM workflows.
- Automated rotation: the cloud provider refreshes tokens, so integrations keep working when teams change.

## How it works

After Databend Cloud support shares the trusted principal information for your organization, you create an IAM role/identity in your cloud account, attach a policy that allows the object storage operations you need (for example reading a set of buckets), and configure the trust policy so only Databend Cloud can assume the role with a unique external ID. Databend Cloud then assumes that role on demand, uses the temporary credentials to access your storage, and automatically logs out when the session expires.

## Use IAM role

1. Raise a support ticket to get the IAM role ARN for your Databend Cloud organization:

   For example: `arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg`

2. Goto AWS Console:

   https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/policies

   Click `Create policy`, and select `Custom trust policy`, and input the policy document for S3 bucket access:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:ListBucket",
         "Resource": "arn:aws:s3:::test-bucket-123"
       },
       {
         "Effect": "Allow",
         "Action": "s3:*Object",
         "Resource": "arn:aws:s3:::test-bucket-123/*"
       }
     ]
   }
   ```

   Click `Next`, and input the policy name: `databend-test`, and click `Create policy`

3. Goto AWS Console:

   https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/roles

   Click `Create role`, and select `Custom trust policy` in `Trusted entity type`:

   ![Create Role](/media/tidb-cloud-lake/create-role.png)

   Input the the trust policy document:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg"
         },
         "Condition": {
           "StringEquals": {
             "sts:ExternalId": "my-external-id-123"
           }
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

   Click `Next`, and select the previously created policy: `databend-test`

   Click `Next`, and input the role name: `databend-test`

   Click `View Role`, and record the role ARN: `arn:aws:iam::987654321987:role/databend-test`

4. Run the following SQL statement in Databend Cloud cloud worksheet or `BendSQL`:

   ```sql
   CREATE CONNECTION databend_test STORAGE_TYPE = 's3' ROLE_ARN = 'arn:aws:iam::987654321987:role/databend-test' EXTERNAL_ID = 'my-external-id-123';

   CREATE STAGE databend_test URL = 's3://test-bucket-123' CONNECTION = (CONNECTION_NAME = 'databend_test');

   SELECT * FROM @databend_test/test.parquet LIMIT 1;
   ```

> **Note:**
>
> Congratulations! You could now access your own AWS S3 buckets in Databend Cloud with IAM Role.
