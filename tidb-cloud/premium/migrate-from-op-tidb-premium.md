---
title: Migrate from TiDB Self-Managed to TiDB Cloud Premium
summary: Learn how to migrate data from TiDB Self-Managed to TiDB Cloud Premium.
---

> **Warning:**
>
> TiDB Cloud Premium is currently available in **Private Preview** in select AWS regions.  
>
> If Premium is not yet enabled for your organization, or if you need access in another cloud provider or region, click **Support** in the lower-left corner of the [TiDB Cloud console](https://tidbcloud.com/), or submit a request through the [Contact Us form](https://www.pingcap.com/contact-us) on our website.

# Migrate from TiDB Self-Managed to TiDB Cloud Premium

This document describes how to migrate data from your TiDB Self-Managed clusters to TiDB Cloud Premium (AWS) through Dumpling and TiCDC.

The overall procedure is as follows:

1. Build the environment and prepare the tools.
2. Migrate full data. The process is as follows:
   1. Export data from TiDB Self-Managed to Amazon S3 using Dumpling.
   2. Import data from Amazon S3 to TiDB Cloud Premium.
3. Replicate incremental data by using TiCDC.
4. Verify the migrated data.

## Prerequisites

It is recommended that you put the S3 bucket and the TiDB Cloud Premium cluster in the same region. Cross-region migration might incur additional cost for data conversion.

Before migration, you need to prepare the following:

- An [AWS account](https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-up-s3.html#sign-up-for-aws-gsg) with administrator access
- An [AWS S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- [A TiDB Cloud account](/tidb-cloud/tidb-cloud-quickstart.md) with at least the [`Project Data Access Read-Write`](/tidb-cloud/manage-user-access.md#user-roles) access to your target TiDB Cloud Premium cluster hosted on AWS

## Prepare tools

You need to prepare the following tools:

- Dumpling: a data export tool
- TiCDC: a data replication tool

### Dumpling

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview) is a tool that exports data from TiDB or MySQL into SQL or CSV files. You can use Dumpling to export full data from TiDB Self-Managed.

Before you deploy Dumpling, note the following:

- It is recommended to deploy Dumpling on a new EC2 instance in the same VPC as your target TiDB Cloud Premium cluster.
- The recommended EC2 instance type is **c6g.4xlarge** (16 vCPU and 32 GiB memory). You can choose other EC2 instance types based on your needs. The Amazon Machine Image (AMI) can be Amazon Linux, Ubuntu, or Red Hat.

You can deploy Dumpling by using TiUP or using the installation package.

#### Deploy Dumpling using TiUP

Use [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview) to deploy Dumpling:

```bash
## Deploy TiUP
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source /root/.bash_profile
## Deploy Dumpling and update to the latest version
tiup install dumpling
tiup update --self && tiup update dumpling
```

#### Deploy Dumpling using the installation package

To deploy Dumpling using the installation package:

1. Download the [toolkit package](https://docs.pingcap.com/tidb/stable/download-ecosystem-tools).

2. Extract it to the target machine. You can get Dumpling using TiUP by running `tiup install dumpling`. Then, you can use `tiup dumpling ...` to run Dumpling. For more information, see [Dumpling introduction](https://docs.pingcap.com/tidb/stable/dumpling-overview#dumpling-introduction).

#### Configure privileges for Dumpling

You need the following privileges to export data from the upstream database:

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT
- PROCESS

### Deploy TiCDC

You need to [deploy TiCDC](https://docs.pingcap.com/tidb/dev/deploy-ticdc) to replicate incremental data from the upstream TiDB cluster to TiDB Cloud Premium.

1. Confirm whether the current TiDB version supports TiCDC. TiDB v4.0.8.rc.1 and later versions support TiCDC. You can check the TiDB version by executing `select tidb_version();` in the TiDB cluster. If you need to upgrade it, see [Upgrade TiDB Using TiUP](https://docs.pingcap.com/tidb/dev/deploy-ticdc#upgrade-ticdc-using-tiup).

2. Add the TiCDC component to the TiDB cluster. See [Add or scale out TiCDC to an existing TiDB cluster using TiUP](https://docs.pingcap.com/tidb/dev/deploy-ticdc#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup). Edit the `scale-out.yml` file to add TiCDC:

    ```yaml
    cdc_servers:
    - host: 10.0.1.3
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    - host: 10.0.1.4
      gc-ttl: 86400
      data_dir: /tidb-data/cdc-8300
    ```

3. Add the TiCDC component and check the status.

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    tiup cluster display <cluster-name>
    ```

## Migrate full data

To migrate data from the TiDB Self-Managed cluster to TiDB Cloud Premium, perform a full data migration as follows:

1. Migrate data from the TiDB Self-Managed cluster to Amazon S3.
2. Migrate data from Amazon S3 to TiDB Cloud Premium.

### Migrate data from the TiDB Self-Managed cluster to Amazon S3

You need to migrate data from the TiDB Self-Managed cluster to Amazon S3 using Dumpling.

If your TiDB cluster is in a local IDC, or the network between the Dumpling server and Amazon S3 is not connected, you can export the files to the local storage first, and then upload them to Amazon S3 later.

#### Step 1. Disable the GC mechanism of the upstream TiDB Self-Managed cluster temporarily

To ensure that newly written data is not lost during incremental migration, you need to disable the upstream cluster's garbage collection (GC) mechanism before starting the migration to prevent the system from cleaning up historical data.

Run the following command to verify whether the setting is successful.

```sql
SET GLOBAL tidb_gc_enable = FALSE;
```

The following is an example output, in which `0` indicates that it is disabled.

```sql
SELECT @@global.tidb_gc_enable;
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.01 sec)
```

#### Step 2. Configure access permissions to the Amazon S3 bucket for Dumpling

Create an access key in the AWS console. See [Create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for details.

1. Use your AWS account ID or account alias, your IAM user name, and your password to sign in to [the IAM console](https://console.aws.amazon.com/iam/home#/security_credentials).

2. In the navigation bar on the upper right, choose your user name, and then click **My Security Credentials**.

3. To create an access key, click **Create access key**. Then choose **Download .csv file** to save the access key ID and secret access key to a CSV file on your computer. Store the file in a secure location. You will not have access to the secret access key again after this dialog box closes. After you download the CSV file, choose **Close**. When you create an access key, the key pair is active by default, and you can use the pair right away.

    ![Create access key](/media/tidb-cloud/op-to-cloud-create-access-key01.png)

    ![Download CSV file](/media/tidb-cloud/op-to-cloud-create-access-key02.png)

#### Step 3. Export data from the upstream TiDB cluster to Amazon S3 using Dumpling

Do the following to export data from the upstream TiDB cluster to Amazon S3 using Dumpling:

1. Configure the environment variables for Dumpling.

    ```shell
    export AWS_ACCESS_KEY_ID=${AccessKey}
    export AWS_SECRET_ACCESS_KEY=${SecretKey}
    ```

2. Get the S3 bucket URI and region information from the AWS console. See [Create a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) for details.

    The following screenshot shows how to get the S3 bucket URI information:

    ![Get the S3 URI](/media/tidb-cloud/op-to-cloud-copy-s3-uri.png)

    The following screenshot shows how to get the region information:

    ![Get the region information](/media/tidb-cloud/op-to-cloud-copy-region-info.png)

3. Run Dumpling to export data to the Amazon S3 bucket.

    ```shell
    dumpling \
    -u root \
    -P 4000 \
    -h 127.0.0.1 \
    -r 20000 \
    --filetype sql  \
    -F 256MiB  \
    -t 8 \
    -o "${S3 URI}" \
    --s3.region "${s3.region}"
    ```

    The `-t` option specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and also increases the database's memory consumption. Therefore, do not set this parameter to a very large number.

    For more information, see [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-to-sql-files).

4. Check the export data. Usually the exported data includes the following:

    - `metadata`: this file contains the start time of the export, and the location of the master binary log.
    - `{schema}-schema-create.sql`: the SQL file for creating the schema
    - `{schema}.{table}-schema.sql`: the SQL file for creating the table
    - `{schema}.{table}.{0001}.{sql|csv}`: data files
    - `*-schema-view.sql`, `*-schema-trigger.sql`, `*-schema-post.sql`: other exported SQL files

### Migrate data from Amazon S3 to TiDB Cloud Premium

After you export data from the TiDB Self-Managed cluster to Amazon S3, you need to migrate the data to TiDB Cloud Premium.

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to your TiDB Cloud Premium cluster, click **Data → Import**, and choose **Import data from Cloud Storage** > **Amazon S3**. Make a note of the **Account ID** and **External ID** displayed in the wizard—these values are embedded in the CloudFormation template.

2. In the **Source Connection** dialog, select **AWS Role ARN**, then click **Click here to create a new one with AWS CloudFormation** and follow the on-screen guidance. If your organization cannot launch CloudFormation stacks, see [Manually create the IAM role](#manually-create-the-iam-role-optional).

    - Open the pre-filled CloudFormation template in the AWS console.
    - Provide a role name, review the permissions, and acknowledge the IAM warning.
    - Create the stack and wait for the status to change to **CREATE_COMPLETE**.
    - On the **Outputs** tab, copy the newly generated Role ARN.
    - Return to TiDB Cloud Premium, paste the Role ARN, and click **Confirm**. The wizard stores the ARN for subsequent import jobs.

3. Continue with the remaining steps in the import wizard, using the saved Role ARN when prompted.

#### Manually create the IAM role (optional)

If your organization cannot deploy CloudFormation stacks, create the access policy and IAM role manually:

1. In AWS IAM, create a policy that grants the following actions on your bucket (and KMS key, if applicable):

    - `s3:GetObject`
    - `s3:GetObjectVersion`
    - `s3:ListBucket`
    - `s3:GetBucketLocation`
    - `kms:Decrypt` (only when SSE-KMS encryption is enabled)

    The JSON template below shows the required structure. Replace the placeholders with your bucket path, bucket ARN, and (if needed) KMS key ARN.

    ```json
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
            },
            {
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "<Your AWS KMS ARN>"
            }
        ]
    }
    ```

2. Create an IAM role that trusts TiDB Cloud Premium by supplying the **Account ID** and **External ID** noted in Step 1. Attach the policy from the previous step to this role.

3. Copy the resulting Role ARN and enter it in the TiDB Cloud Premium import wizard.

4. Import data to TiDB Cloud Premium by following [Import data from Amazon S3 into TiDB Cloud Premium](/tidb-cloud/premium/import-from-s3-premium.md).

## Replicate incremental data

To replicate incremental data, do the following:

1. Get the start time of the incremental data migration. For example, you can get it from the metadata file of the full data migration.

    ![Start Time in Metadata](/media/tidb-cloud/start_ts_in_metadata.png)

2. Grant TiCDC to connect to TiDB Cloud Premium.

    1. In the [TiDB Cloud console](https://tidbcloud.com/tidbs), navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Premium cluster to go to its overview page.
    2. In the left navigation pane, click **Settings** > **Networking**.
    3. On the **Networking** page, click **Add IP Address**.
    4. In the displayed dialog, select **Use IP addresses**, click **+**, fill in the public IP address of the TiCDC component in the **IP Address** field, and then click **Confirm**. Now TiCDC can access TiDB Cloud Premium. For more information, see [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md).

3. Get the connection information of the downstream TiDB Cloud Premium cluster.

    1. In the [TiDB Cloud console](https://tidbcloud.com/tidbs), navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Premium cluster to go to its overview page.
    2. Click **Connect** in the upper-right corner.
    3. In the connection dialog, select **Public** from the **Connection Type** drop-down list and select **General** from the **Connect With** drop-down list.
    4. From the connection information, you can get the host IP address and port of the cluster. For more information, see [Connect via public connection](/tidb-cloud/connect-via-standard-connection.md).

4. Create and run the incremental replication task. In the upstream cluster, run the following:

    ```shell
    tiup cdc cli changefeed create \
    --pd=http://172.16.6.122:2379  \
    --sink-uri="tidb://root:123456@172.16.6.125:4000"  \
    --changefeed-id="upstream-to-downstream"  \
    --start-ts="431434047157698561"
    ```

    - `--pd`: the PD address of the upstream cluster. The format is: `[upstream_pd_ip]:[pd_port]`
    - `--sink-uri`: the downstream address of the replication task. Configure `--sink-uri` according to the following format. Currently, the scheme supports `mysql`, `tidb`, `kafka`, `s3`, and `local`.

        ```shell
        [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
        ```

    - `--changefeed-id`: the ID of the replication task. The format must match the ^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$ regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
    - `--start-ts`: specifies the starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.

    For more information, see [CLI and Configuration Parameters of TiCDC Changefeeds](https://docs.pingcap.com/tidb/dev/ticdc-changefeed-config).

5. Enable the GC mechanism again in the upstream cluster. If no error or delay is found in incremental replication, enable the GC mechanism to resume garbage collection of the cluster.

    Run the following command to verify whether the setting works.

    ```sql
    SET GLOBAL tidb_gc_enable = TRUE;
    ```

    The following is an example output, in which `1` indicates that GC is enabled.

    ```sql
    SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.01 sec)
    ```

6. Verify the incremental replication task.

    - If the message "Create changefeed successfully!" is displayed in the output, the replication task is created successfully.
    - If the state is `normal`, the replication task is normal.

        ```shell
         tiup cdc cli changefeed list --pd=http://172.16.6.122:2379
        ```

        ![Update Filter](/media/tidb-cloud/normal_status_in_replication_task.png)

    - Verify the replication. Write a new record to the upstream cluster, and then check whether the record is replicated to the downstream TiDB Cloud Premium cluster.

7. Set the same timezone for the upstream and downstream clusters. By default, TiDB Cloud Premium sets the timezone to UTC. If the timezone is different between the upstream and downstream clusters, you need to set the same timezone for both clusters.

    1. In the upstream cluster, run the following command to check the timezone:

        ```sql
        SELECT @@global.time_zone;
        ```

    2. In the downstream cluster, run the following command to set the timezone:

        ```sql
        SET GLOBAL time_zone = '+08:00';
        ```

    3. Check the timezone again to verify the setting:

        ```sql
        SELECT @@global.time_zone;
        ```

8. Back up the [query bindings](/sql-plan-management.md) in the upstream cluster and restore them in the downstream cluster. You can use the following query to back up the query bindings:

    ```sql
    SELECT DISTINCT(CONCAT('CREATE GLOBAL BINDING FOR ', original_sql,' USING ', bind_sql,';')) FROM mysql.bind_info WHERE status='enabled';
    ```

    If you do not get any output, it means that no query bindings are used in the upstream cluster. In this case, you can skip this step.

    After you get the query bindings, run them in the downstream cluster to restore the query bindings.

9. Back up the user and privilege information in the upstream cluster and restore them in the downstream cluster. You can use the following script to back up the user and privilege information. Note that you need to replace the placeholders with the actual values.

    ```shell
    #!/bin/bash

    export MYSQL_HOST={tidb_op_host}
    export MYSQL_TCP_PORT={tidb_op_port}
    export MYSQL_USER=root
    export MYSQL_PWD={root_password}
    export MYSQL="mysql -u${MYSQL_USER} --default-character-set=utf8mb4"
    
    function backup_user_priv(){
        ret=0
        sql="SELECT CONCAT(user,':',host,':',authentication_string) FROM mysql.user WHERE user NOT IN ('root')"
        for usr in `$MYSQL -se "$sql"`;do
            u=`echo $usr | awk -F ":" '{print $1}'`
            h=`echo $usr | awk -F ":" '{print $2}'`
            p=`echo $usr | awk -F ":" '{print $3}'`
            echo "-- Grants for '${u}'@'${h}';"
            [[ ! -z "${p}" ]] && echo "CREATE USER IF NOT EXISTS '${u}'@'${h}' IDENTIFIED WITH 'mysql_native_password' AS '${p}' ;"
            $MYSQL -se "SHOW GRANTS FOR '${u}'@'${h}';" | sed 's/$/;/g'
            [ $? -ne 0 ] && ret=1 && break
        done
        return $ret
    }
    
    backup_user_priv
    ```
    
    After you get the user and privilege information, run the generated SQL statements in the downstream cluster to restore the user and privilege information.
