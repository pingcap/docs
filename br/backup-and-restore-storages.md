---
title: Backup Storages
summary: TiDB supports backup storage to Amazon S3, Google Cloud Storage, Azure Blob Storage, and NFS. You can specify the URI and authentication for different storage services. BR sends credentials to TiKV by default when using S3, GCS, or Azure Blob Storage. You can disable this for cloud environments. The URI format for each storage service is specified, along with authentication methods. Server-side encryption is supported for Amazon S3 and Azure Blob Storage. BR v6.3.0 also supports AWS S3 Object Lock.
---

# Backup Storages

TiDB supports storing backup data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, and NFS. Specifically, you can specify the URI of backup storage in the `--storage` or `-s` parameter of `br` commands. This document introduces the [URI format](#uri-format) and [authentication](#authentication) of different external storage services, and [server-side encryption](#server-side-encryption).

## Send credentials to TiKV

| CLI parameter | Description | Default value
|:----------|:-------|:-------|
| `--send-credentials-to-tikv` | Controls whether to send credentials obtained by BR to TiKV. | `true`|

By default, BR sends a credential to each TiKV node when using Amazon S3, GCS, or Azure Blob Storage as the storage system. This behavior simplifies the configuration and is controlled by the parameter `--send-credentials-to-tikv`(or `-c` in short).

Note that this operation is not applicable to cloud environments. If you use IAM Role authorization, each node has its own role and permissions. In this case, you need to configure `--send-credentials-to-tikv=false` (or `-c=0` in short) to disable sending credentials:

```bash
./br backup full -c=0 -u pd-service:2379 --storage 's3://bucket-name/prefix'
```

If you back up or restore data using the [`BACKUP`](/sql-statements/sql-statement-backup.md) and [`RESTORE`](/sql-statements/sql-statement-restore.md) statements, you can add the `SEND_CREDENTIALS_TO_TIKV = FALSE` option:

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

## URI format

### URI format description

The URI format of the external storage service is as follows:

```shell
[scheme]://[host]/[path]?[parameters]
```

For more information about the URI format, see [URI Formats of External Storage Services](/external-storage-uri.md).

### URI examples

This section provides some URI examples by using `external` as the `host` parameter (`bucket name` or `container name` in the preceding sections).

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

**Back up snapshot data to Amazon S3**

```shell
./br backup full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

**Restore snapshot data from Amazon S3**

```shell
./br restore full -u "${PD_IP}:2379" \
--storage "s3://external/backup-20220915?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

</div>
<div label="GCS" value="gcs">

**Back up snapshot data to GCS**

```shell
./br backup full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

**Restore snapshot data from GCS**

```shell
./br restore full --pd "${PD_IP}:2379" \
--storage "gcs://external/backup-20220915?credentials-file=${credentials-file-path}"
```

</div>
<div label="Azure Blob Storage" value="azure">

**Back up snapshot data to Azure Blob Storage**

```shell
./br backup full -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915?account-name=${account-name}&account-key=${account-key}"
```

**Restore the `test` database from snapshot backup data in Azure Blob Storage**

```shell
./br restore db --db test -u "${PD_IP}:2379" \
--storage "azure://external/backup-20220915account-name=${account-name}&account-key=${account-key}"
```

</div>
</SimpleTab>

## Authentication

When storing backup data in a cloud storage system, you need to configure authentication parameters depending on the specific cloud service provider. This section describes the authentication methods used by Amazon S3, GCS, and Azure Blob Storage, and how to configure the accounts used to access the corresponding storage service.

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

Before backup, configure the following privileges to access the backup directory on S3.

- Minimum privileges for TiKV and Backup & Restore (BR) to access the backup directories during backup: `s3:ListBucket`, `s3:GetObject`, `s3:DeleteObject`, `s3:PutObject`, and `s3:AbortMultipartUpload`
- Minimum privileges for TiKV and BR to access the backup directories during restore: `s3:ListBucket`, `s3:GetObject`, `s3:DeleteObject`, and `s3:PutObject`. BR writes checkpoint information to the `./checkpoints` subdirectory under the backup directory. When restoring log backup data, BR writes the table ID mapping relationship of the restored cluster to the `./pitr_id_maps` subdirectory under the backup directory.

If you have not yet created a backup directory, refer to [Create a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) to create an S3 bucket in the specified region. If necessary, you can also create a folder in the bucket by referring to [Create a folder](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html).

> **Note:**
>
> In 2024, AWS changed the default behavior, and newly created instances now only support IMDSv2 by default. For more details, see [Set IMDSv2 as default for all new instance launches in your account](https://aws.amazon.com/about-aws/whats-new/2024/03/set-imdsv2-default-new-instance-launches/). Therefore, starting from v7.5.7, BR supports obtaining IAM role permissions on Amazon EC2 instances with only IMDSv2 enabled. When using BR of an earlier version before v7.5.7, you need to configure the instance to support both IMDSv1 and IMDSv2.

It is recommended that you configure access to S3 using either of the following ways:

- Method 1: Specify the access key

    If you specify an access key and a secret access key in the URI, authentication is performed using the specified access key and secret access key. Besides specifying the key in the URI, the following methods are also supported:

    - BR reads the environment variables `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY`.
    - BR reads the environment variables `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY`.
    - BR reads the shared credentials file in the path specified by the environment variable `$AWS_SHARED_CREDENTIALS_FILE`.
    - BR reads the shared credentials file in the `~/.aws/credentials` path.

- Method 2: Access based on the IAM role

    Associate an IAM role that can access S3 with EC2 instances where the TiKV and BR nodes run. After the association, BR can directly access the backup directories in S3 without additional settings.

    ```shell
    br backup full --pd "${PD_IP}:2379" \
    --storage "s3://${host}/${path}"
    ```

</div>
<div label="GCS" value="gcs">

You can configure the account used to access GCS by specifying the access key. If you specify the `credentials-file` parameter, the authentication is performed using the specified `credentials-file`. Besides specifying the key in the URI, the following methods are also supported:

- BR reads the file in the path specified by the environment variable `$GOOGLE_APPLICATION_CREDENTIALS`
- BR reads the file `~/.config/gcloud/application_default_credentials.json`.
- BR obtains the credentials from the metadata server when the cluster is running in GCE or GAE.

</div>
<div label="Azure Blob Storage" value="azure">

- Method 1: Specify the shared access signature

    If you specify `account-name` and `sas-token` in the URI, the authentication is performed using the specified account name and shared access signature (SAS) token. Note that the SAS token contains the `&` character. You need to encode it as `%26` before appending it to the URI. You can also directly encode the entire `sas-token` using percent-encoding.

- Method 2: Specify the access key

    If you specify `account-name` and `account-key` in the URI, the authentication is performed using the specified account name and account key. Besides the method of specifying the key in the URI, BR can also read the key from the environment variable `$AZURE_STORAGE_KEY`.

- Method 3: Use Azure AD for backup and restore

    Configure the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` on the node where BR is running.

    - When the cluster is started using TiUP, TiKV uses the systemd service. The following example shows how to configure the preceding three environment variables for TiKV:

        > **Note:**
        >
        > If this method is used, you need to restart TiKV in step 3. If your cluster cannot be restarted, use **Method 1: Specify the access key** for backup and restore.

        1. Suppose that the TiKV port on this node is `24000`, that is, the name of the systemd service is `tikv-24000`:

            ```shell
            systemctl edit tikv-24000
            ```

        2. Edit the TiKV configuration file to configure the three environment variables:

            ```
            [Service]
            Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ```

        3. Reload the configuration and restart TiKV:

            ```shell
            systemctl daemon-reload
            systemctl restart tikv-24000
            ```

    - To configure the Azure AD information for TiKV and BR started with command lines, you only need to check whether the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` are configured in the operating environment by running the following commands:

        ```shell
        echo $AZURE_CLIENT_ID
        echo $AZURE_TENANT_ID
        echo $AZURE_CLIENT_SECRET
        ```

    - Use BR to back up data to Azure Blob Storage:

        ```shell
        ./br backup full -u "${PD_IP}:2379" \
        --storage "azure://external/backup-20220915?account-name=${account-name}"
        ```

</div>
</SimpleTab>

## Server-side encryption

### Amazon S3 server-side encryption

BR supports server-side encryption when backing up data to Amazon S3. You can also use an AWS KMS key you create for S3 server-side encryption using BR. For details, see [BR S3 server-side encryption](/encryption-at-rest.md#br-s3-server-side-encryption).

### Azure Blob Storage server-side encryption

BR supports specifying the Azure server-side encryption scope or providing the encryption key when backing up data to Azure Blob Storage. This feature lets you establish a security boundary for different backup data of the same storage account. For details, see [BR Azure Blob Storage server-side encryption](/encryption-at-rest.md#br-azure-blob-storage-server-side-encryption).

## Other features supported by the storage service

BR v6.3.0 supports AWS [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html). You can enable this feature to prevent backup data from being tampered with or deleted.
