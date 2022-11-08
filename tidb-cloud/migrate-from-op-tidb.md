---
title: Migrate from On-Premise TiDB to TiDB Cloud
summary: Learn how to migrate data from on-premise TiDB to TiDB Cloud.
---

# Migrate from On-Premises TiDB to TiDB Cloud

This document describes how to migrate data from your on-premises (OP) TiDB clusters to TiDB Cloud (AWS) through Dumpling and TiCDC.

The overall procedure is as follows:

- Build the environment and prepare the tools
- Full data migration: OP TiDB (Dumpling) --> S3 --> (Import) TiDB Cloud
- Incremental data migration: OP TiDB --> (TiCDC) --> TiDB Cloud
- Data verification

## Prerequisites

It is recommended that you put the S3 bucket and TiDB Cloud in the same region. Cross-region migration might incur additional data conversion cost.

  1. Prepare an [AWS account](https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-up-s3.html#sign-up-for-aws-gsg) with administrator access
  2. Prepare an [AWS S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
  3. [Deploy an on-premises TiDB cluster](https://docs.pingcap.com/zh/tidb/dev/hardware-and-software-requirements)
  4. Prepare [a TiDB Cloud account with administrator access and create a TiDB Cloud (AWS) cluster](/tidb-cloud/tidb-cloud-quickstart.md)

## Prepare tools

### Dumpling

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) is a data export tool that exports data from TiDB/MySQL into SQL or CSV files. You can use Dumpling to export full data from TiDB Cloud.

Before you deploy Dumpling, note the following:

- It is recommended to deploy Dumpling on a new EC2 instance in the same VPC as the TiDB cluster.
- The EC2 instance should have at least 16 cores and 32 GB of memory to guarantee a good export performance.
- The recommended EC2 instance type is c6g.4xlarge. You can choose other EC2 instance types based on your needs. The AMI can be Amazon Linux, Ubuntu, or Red Hat.

You can deploy Dumpling by using TiUP or using the binary package.

#### Deploy Dumpling usig TiUP

Use [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview) to deploy Dumpling:

```bash
## Deploy tiup
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source /root/.bash_profile
## Deploy Dumpling and update to the latest version
tiup install dumpling
tiup update --self && tiup update dumpling
```

#### Deploy Dumpling using the installation package

To deploy Dumpling using the installation package

1. Download the [toolkit package](https://docs.pingcap.com/tidb/stable/download-ecosystem-tools) from the [Dumpling download page].
2. Extract it to the target machine and [install Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#dumpling-introduction).

#### Configure privileges for Dumpling

You need the following previleges to export data from the upstream database:

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT
- PROCESS

### Deploy TiCDC

You need to [deploy TiCDC](https://docs.pingcap.com/tidb/dev/deploy-ticdc) to replicate incremental data from the upstream TiDB cluster to TiDB Cloud.

- First you need to confirm whether the current TiDB version supports TiCDC. You can check the TiDB version by executing `select tidb_version();` in the TiDB cluster. If the TiDB version is earlier than v4.0.8.rc.1, you need to upgrade first. See [Upgrade TiDB Using TiUP](https://docs.pingcap.com/tidb/dev/upgrade-tidb-using-tiup).

- Add the TiCDC component to the TiDB cluster. See [Scale a TiDB Cluster Using TiUP](https://docs.pingcap.com/tidb/dev/scale-tidb-using-tiup).

  1. Edit the `scale-out.yaml` file to add TiCDC:

      ```yaml
      cdc_servers:
      - host: 10.0.1.3
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
      - host: 10.0.1.4
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
      ```

  2. Add the TiCDC component and check the status.

        ```shell
        tiup cluster scale-out <cluster-name> scale-out.yaml
        tiup cluster display <cluster-name>
        ```

## Perform full data migration

To migrate data from the on-premises TiDB cluster to TiDB Cloud, you need to perform a full data migration as follows:

1. Migrate data from the on-premises TiDB cluster to Amazon S3.
2. Migrate data from Amazon S3 to TiDB Cloud.

### Migrate data from the on-premises TiDB cluster to Amazon S3

You need to migrate data from the on-premises TiDB cluster to Amazon S3 using Dumpling.

If your TiDB cluster is in a local IDC, or the network between the Dumpling server and Amazon S3 is not connected, you can export the files to the local storage first, and then upload them to S3 later.

#### Step 1: Disable the GC mechanism of the upstream OP TiDB cluster temporarily

To ensure that newly written data is not lost during incremental migration, you need to disable the upstream cluster's garbage collection (GC) mechanism before starting the backup to ensure that the system does not clean up historical data.

```sql
mysql > SET GLOBAL tidb_gc_enable = FALSE;
## Verify whether the setting is successful. 0 means it is disabled.
mysql > SELECT @@global.tidb_gc_enable;
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.01 sec)
```

#### Step 2: Configure access permissions to the Amazon S3 bucket for Dumpling

Create an access key on the AWS console. See [Create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for details.

#### Step 3: Export data from the upstream TiDB cluster to Amazon S3 using Dumpling

1. Configure environment variables for Dumpling.

    ```shell
    export AWS_ACCESS_KEY_ID=${AccessKey}
    export AWS_SECRET_ACCESS_KEY=${SecretKey}
    ```

2. Get the S3 bucket URI and Region information from the AWS console. See [Create a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) for details.

3. Run Dumpling to export data to the Amazon S3 bucket.

    ```ymal
    dumpling \
    -u root \
    -P 4000 \
    -h 127.0.0.1 \
    -r 20000 \
    --filetype {sql|csv}  \
    -F 256MiB  \
    -o "${S3 URI}" \
    --s3.region "${s3.region}"
    ```

    The `-t` option specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and also increases the database's memory consumption. Therefore, it is not recommended to set the number too large.

    For mor information, see [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview).

4. Check the export data. Usually the exported data includes the following:

    - metadata: this file contains the start time of the export, and the location of the master binary log.
    - {schema}-schema-create.sql: the SQL file for creating the schema
    - {schema}.{table}-schema.sql: the SQL file for creating the table
    - {schema}.{table}.{0001}.{sql|csv}: data files
    - \*-schema-view.sql, \*-schema-trigger.sql, \*-schema-post.sql: other exported SQL files

### Migrate data from Amazon S3 to TiDB Cloud

After you export data from the on-premises TiDB cluster to Amazon S3, you need to migrate the data to TiDB Cloud.

If your TiDB cluster is in a local IDC, or the network between the Dumpling server and Amazon S3 is not connected, you can export the files to the local storage first, and then upload them to S3 later.

1. Get the Account ID and External ID of the cluster on the TiDB Cloud Console. For more information, see [Step 2. Configure Amazon S3 access](/tidb-cloud/tidb-cloud-auditing.md#step-2-configure-amazon-s3-access).

2. Configure access permissions for Amazon s3. Usually you need the following read-only permissions:
    - s3:GetObject
    - s3:GetObjectVersion
    - s3:ListBucket
    - s3:GetBucketLocation
    If the S3 bucket uses server-side encryption SSE-KMS, you also need to add KMS permissions:
    - kms:Decrypt

3. Configure the access policy. Go to the AWS Console > IAM > Access Management > Policies to check if the access policy for TiDB Cloud exists already. If it does not exist, create a policy following [Creating policies on the JSON tab](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html). The following is an example template for the json policy.

    ```json
    ## Create a json policy template
    ##<Your customized directory>: fill in the path to the folder in the S3 bucket where the data files to be imported are located
    ##<Your S3 bucket ARN>: fill in the ARN of S3 bucket. You can click the Copy ARN button on the S3 Bucket Overview page to get it.
    ##<Your AWS KMS ARN>: Fill ARN for the S3 bucket KMS key. You can get it from S3 bucket > Properties > Default encryption > AWS KMS Key ARN. For more informaiton, see https://docs.aws.amazon.com/AmazonS3/latest/userguide/viewing-bucket-key-settings.html

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<Your customized directory>"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": "<Your S3 bucket ARN>"
            }
            // If you have enabled SSE-KMS for the S3 bucket, add the following permissions.
            {
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "<Your AWS KMS ARN>"
            }
            ,
            {
                "Effect": "Allow",
                "Action": "kms:Decrypt",
                "Resource": "<Your AWS KMS ARN>"
            }
        ]
    }
    ```

4. Configure the role. See [Creating an IAM role (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html). In the Account ID field, enter the TiDB Cloud Account ID and  TiDB Cloud External ID you have noted down in Step 1.

5. Get the Role-ARN. Go to IAM > Access Management > Roles. Click the role you have created, and note down the ARN. You will use it when importing data into TiDB Cloud.

6. Import data to TiDB Cloud. See [Step 3. Import data into TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-3-import-data-into-tidb-cloud).

## Perform incremental data migration

