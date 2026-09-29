---
title: Sink to TiDB Cloud Lake
summary: Manual setup guide for building a TiDB Cloud Lake data pipeline on TiDB Cloud Dedicated clusters using Dumpling and a changefeed.
aliases: ['/tidb-cloud/data-pipeline-lake-setup-for-dedicated']
---

# Sink to TiDB Cloud Lake

This guide walks you through the end-to-end setup of a data pipeline from a TiDB Cloud Dedicated cluster to TiDB Cloud Lake: export a full snapshot to Amazon S3 with [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview), create a changefeed to continuously write incremental changes to the same S3 location, and configure TiDB Cloud Lake to load both the snapshot and incremental data. TiDB Cloud Dedicated does not provide the native Data Pipeline setup experience in the TiDB Cloud console, so you need to configure the pipeline manually.

## Restrictions

- The TiDB Cloud Lake warehouse must be in the **same region** as your {{{ .dedicated }}} cluster.
- Only tables with a **primary key** can be replicated incrementally.
- To create the cloud storage changefeed, your {{{ .dedicated }}} cluster must run v7.1.1 or later. For details, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).
- The pipeline requires manual setup and maintenance of AWS IAM resources and credentials, the changefeed, and TiDB Cloud Lake integrations.
- For details on DDL, DML, and column type support, see [Data Pipeline SQL Compatibility for TiDB Cloud Lake](/tidb-cloud/data-pipeline-lake-sql-compatibility.md).

## Prerequisites

Before you begin, make sure that you have:

- A {{{ .dedicated }}} cluster. Note the region in which it is deployed.
- A network connection from the machine that runs Dumpling to your cluster. You can use a public connection, VPC peering, or a private endpoint. This guide uses a public connection as an example.
- A SQL user that can read the source tables. This guide uses `root` as an example. For the required privileges, see [Required privileges](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges).
- An AWS access key that has permission to write to the target S3 bucket. Dumpling uses this access key.
- An Amazon S3 bucket in the same region (for example, `s3://my-datapipeline-bucket`) as your {{{ .dedicated }}} cluster.
- A TiDB Cloud Lake warehouse in the same region as your {{{ .dedicated }}} cluster.

> **Note:**
>
> This guide assumes you already have data in the source TiDB database that you want to replicate. If you need sample data, prepare it before continuing.

## Prepare S3 bucket access

The data pipeline components (Dumpling, the changefeed, and TiDB Cloud Lake) all require access to the same S3 bucket. Create an IAM user and access key, and use the same access key for all three components.

1. Open the [IAM Console](https://console.aws.amazon.com/iam/) and create an IAM user (for example, `tidb-cloud-datapipeline-user`).
2. Attach the following permissions policy to the user. Replace `<your-bucket-name>` and `<your-prefix>` with your actual values:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketAccess",
          "Effect": "Allow",
          "Action": [
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": "arn:aws:s3:::<your-bucket-name>"
        },
        {
          "Sid": "S3ObjectAccess",
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:GetObjectVersion",
            "s3:DeleteObjectVersion"
          ],
          "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
        }
      ]
    }
    ```

3. Create an access key for the user, and record the **Access Key ID** and **Secret Access Key**. You need them when you export the snapshot, create the changefeed, and configure TiDB Cloud Lake.

> **Note:**
>
> This guide uses an access key to access the S3 bucket. The changefeed also supports a Role ARN. For details, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

## Export a full snapshot with Dumpling

TiDB Cloud Dedicated does not provide the Export feature, so export the full snapshot with [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview).

### Prepare the network and SQL user

1. Make sure your {{{ .dedicated }}} cluster is reachable from the machine that runs Dumpling. This guide uses a public connection. If you use a public connection, add the machine's IP address to the IP access list of the cluster. For details, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md) and [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md).
2. In the TiDB Cloud console, click **Connect** on the overview page of your cluster, and record the host and port of the connection. You need them in the Dumpling command.
3. Prepare a SQL user that has the privileges required by Dumpling. This guide uses `root` as an example. To use a dedicated user instead, grant it the [privileges required by Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges).

### Run Dumpling

Run Dumpling on a machine that can connect to your {{{ .dedicated }}} cluster. Pass the AWS access key in the `-o` URI with the `access-key` and `secret-access-key` parameters:

```shell
tiup dumpling \
  -h "<host>" \
  -P <port> \
  -u "<username>" \
  -p "<password>" \
  --filetype csv \
  --csv-output-dialect snowflake \
  --escape-backslash=false \
  -o "s3://<bucket>/<prefix>/snapshot/?access-key=<access-key-id>&secret-access-key=<secret-access-key>" \
  --s3.region "<region>"
```

The options map to the TiDB Cloud export configuration as follows:

- `--filetype csv` with `--csv-output-dialect snowflake`: export data in CSV format, equivalent to the **CSV** data format with the **Snowflake** dialect.
- `--escape-backslash=false`: disable backslash escaping, equivalent to clearing **Escape backslash**.
- Compression is disabled by default, which matches the **None** compression option.
- `-o` and `--s3.region`: write the exported files to your S3 bucket. The `access-key` and `secret-access-key` parameters in the `-o` URI provide the credentials for the bucket.

> **Note:**
>
> If your secret access key contains URI special characters such as `+`, `/`, or `=`, URL-encode them first. Alternatively, set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables, or use a `~/.aws/credentials` file, and omit the `access-key` and `secret-access-key` parameters from the `-o` URI.

After the export completes successfully, the command output includes a JSON summary. Find the `SessionParams.tidb_snapshot` field in the output, and record its value. This value is the **snapshot TSO**, which you need when you create the changefeed so that incremental replication continues from the exported snapshot.

## Create a changefeed for incremental data

TiDB Cloud Dedicated supports creating a cloud storage changefeed in the console. For the full procedure, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md). When you configure the changefeed, pay attention to the following settings:

- **S3 URI**: use the `incremental/` sub-path under the same prefix as the snapshot, for example, `s3://<bucket>/<prefix>/incremental/`.
- **Bucket Access**: select **AWS Access Key**, and enter the access key from [Prepare S3 bucket access](#prepare-s3-bucket-access). Make sure the permissions cover the `incremental/` path.
- **Start Replication Position**: select **Start replication from a specific TSO**, and enter the snapshot TSO recorded in [Run Dumpling](#run-dumpling).
- **Data Format**: select **Canal-JSON**, and enable both **Enable TiDB Extension** and **Enable Canal Content Compatibility**. These settings produce data in a format that is compatible with the TiDB Cloud Lake integration.

## Configure TiDB Cloud Lake

> **Note:**
>
> The TiDB Cloud Lake production environment does not yet support the TiDB data source. Use the **staging** environment for now.

### Create a data source

1. In the Lake staging console, navigate to **Data > Data Sources > Create**.
2. Select **Service: TiDB**.
3. Select the access key authentication and fill in:
    - **Access Key ID** and **Secret Access Key**: the credentials from [Prepare S3 bucket access](#prepare-s3-bucket-access).
    - **S3 Bucket Name**: the bucket name only (for example, `my-datapipeline-bucket`, not the full URI).
    - **S3 Region**: the same region as your {{{ .dedicated }}} cluster.
4. **SQS Queue URL** is optional. If you want to enable event-driven ingestion, set up an SQS queue and configure the S3 bucket notification first. For details, see [Amazon SQS and S3 IAM Role for TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/).

### Create an integration

1. In the Lake staging console, navigate to **Data > Integration > Create**.
2. Fill in the following fields:
    - **Data Source**: select the data source created above.
    - **Name**: a name for this integration task.
    - **Sync Mode**: select `Snapshot + CDC` to load the full snapshot first and then continuously apply incremental changes.
    - **Table Rules**: `*.*` to sync all exported tables.
    - **Changefeed S3 Prefix**: `<prefix>/incremental/`.
    - **Dumpling S3 Prefix**: `<prefix>/snapshot/`.
    - **Poll Interval**: the interval at which TiDB Cloud Lake scans the external stage for new data. The default value is 60 seconds. A shorter interval reduces data latency but increases TiDB Cloud Lake hosting cost.
    - **Merge Interval**: the interval at which TiDB Cloud Lake merges incremental data into the warehouse. The default value is 30 seconds. A shorter interval reduces data latency but increases TiDB Cloud Lake hosting cost.
    - **Warehouse**: select the target warehouse.
3. Click **Create**.
4. After creation, the integration is **Stopped** by default. Click the integration action button > **Start** to begin data loading.

## See also

- For frequently asked questions about Data Pipeline, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).
- For details on DDL, DML, and column type support, see [Data Pipeline SQL Compatibility for TiDB Cloud Lake](/tidb-cloud/data-pipeline-lake-sql-compatibility.md).
