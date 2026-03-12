---
title: Backup & Restore with BendSave
---

This tutorial walks you through how to back up and restore data using BendSave. We'll use a local MinIO instance as both the S3-compatible storage backend for Databend and the destination for storing backups.

## Before You Start

Before you start, ensure you have the following prerequisites in place:

- A Linux machine (x86_64 or aarch64 architecture): In this tutorial, we'll deploy Databend on a Linux machine. You can use a local machine, a virtual machine, or a cloud instance such as AWS EC2.
    - [Docker](https://www.docker.com/): Used to deploy a local MinIO instance. 
    - [AWS CLI](https://aws.amazon.com/cli/): Used to manage buckets in MinIO.
    - If you are on AWS EC2, make sure your security group allows inbound traffic on port `8000`, as this is required for BendSQL to connect to Databend.

- BendSQL is installed on your local machine. See [Installing BendSQL](/guides/connect/sql-clients/bendsql/#installing-bendsql) for instructions on how to install BendSQL using various package managers.

- The Databend release package: Download the release from the [Databend GitHub Releases page](https://github.com/databendlabs/databend/releases). The package contains the `databend-bendsave` binary in the `bin` directory, which is the tool we'll use for backup and restore operations in this tutorial.
```bash
databend-v1.2.725-nightly-x86_64-unknown-linux-gnu/
├── bin
│   ├── bendsql
│   ├── databend-bendsave  # The BendSave binary used in this tutorial
│   ├── databend-meta
│   ├── databend-metactl
│   └── databend-query
├── configs
│   ├── databend-meta.toml
│   └── databend-query.toml
└── ...
```

## Step 1: Launch MinIO in Docker

1. Start a MinIO container on your Linux machine. The following command launches a MinIO container named **minio**, with ports `9000` (for the API) and `9001` (for the web console) exposed:

```bash
docker run -d --name minio \
  -e "MINIO_ACCESS_KEY=minioadmin" \
  -e "MINIO_SECRET_KEY=minioadmin" \
  -p 9000:9000 \
  -p 9001:9001 \
  minio/minio server /data \
    --address :9000 \
    --console-address :9001
```

2. Set your MinIO credentials as environment variables, then use the AWS CLI to create two buckets: one for storing backups (**backupbucket**) and another for Databend data (**databend**):

```bash
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

aws --endpoint-url http://127.0.0.1:9000/ s3 mb s3://backupbucket
aws --endpoint-url http://127.0.0.1:9000/ s3 mb s3://databend
```

## Step 2: Set up Databend

1. Download the latest Databend release and extract it to get the necessary binaries:

```bash
wget https://github.com/databendlabs/databend/releases/download/v1.2.25-nightly/databend-dbg-v1.2.725-nightly-x86_64-unknown-linux-gnu.tar.gz

tar -xzvf databend-dbg-v1.2.725-nightly-x86_64-unknown-linux-gnu.tar.gz
```

2. Configure the **databend-query.toml** configuration file in the **configs** folder. 

```bash
vi configs/databend-query.toml
```

The following shows the key configuration required for this tutorial:

```toml
...
[[query.users]]
name = "root"
auth_type = "no_password"
...
# Storage config.
[storage]
# fs | s3 | azblob | gcs | oss | cos
type = "s3"
...
# To use an Amazon S3-like storage service, uncomment this block and set your values.
[storage.s3]
bucket = "databend"
endpoint_url = "http://127.0.0.1:9000"
access_key_id = "minioadmin"
secret_access_key = "minioadmin"
enable_virtual_host_style = false
```

3. Use the following commands to start the Meta and Query services:

```bash
./databend-meta -c ../configs/databend-meta.toml > meta.log 2>&1 &
```

```bash
./databend-query -c ../configs/databend-query.toml > query.log 2>&1 &
```

After launching the services, verify they are running by checking their health endpoints. A successful response should return HTTP status 200 OK.

```bash
curl -I  http://127.0.0.1:28002/v1/health

curl -I  http://127.0.0.1:8080/v1/health
```

4. Connect to your Databend instance from your local machine with BendSQL, then apply your Databend Enterprise license, create a table, and insert some sample data.

```bash
bendsql -h <your-linux-host>
```

```sql
SET GLOBAL enterprise_license='<your-license-key>';
```

```sql
CREATE TABLE books (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
);

INSERT INTO books(id, title) VALUES(1, 'Invisible Stars');
```

5. Back on your Linux machine, verify that the table data has been stored in your Databend bucket:

```bash
aws --endpoint-url http://127.0.0.1:9000 s3 ls s3://databend/ --recursive
```

```bash
2025-04-07 15:27:06        748 1/169/_b/h0196160323247b1cab49be6060d42df8_v2.parquet
2025-04-07 15:27:06        646 1/169/_sg/h0196160323247c5eb0a1a860a6442c70_v4.mpk
2025-04-07 15:27:06        550 1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk
2025-04-07 15:27:06        143 1/169/last_snapshot_location_hint_v2
```

## Step 3: Back up with BendSave

1. Run the following command to back up your Databend data to the **backupbucket** in MinIO:

```bash
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

./databend-bendsave backup \
  --from ../configs/databend-query.toml \
  --to 's3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1'
<jemalloc>: Number of CPUs detected is not deterministic. Per-CPU arena disabled.
Backing up from ../configs/databend-query.toml to s3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1
```

2. After the backup completes, you can verify that the files were written to the backupbucket by listing its contents:

```bash
aws --endpoint-url http://127.0.0.1:9000 s3 ls s3://backupbucket/ --recursive
```

```bash
2025-04-07 15:44:29        748 1/169/_b/h0196160323247b1cab49be6060d42df8_v2.parquet
2025-04-07 15:44:29        646 1/169/_sg/h0196160323247c5eb0a1a860a6442c70_v4.mpk
2025-04-07 15:44:29        550 1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk
2025-04-07 15:44:29        143 1/169/last_snapshot_location_hint_v2
2025-04-07 15:44:29     344781 databend_meta.db
```

## Step 4: Restore with BendSave

1. Remove all the file in the **databend** bucket:

```bash
aws --endpoint-url http://127.0.0.1:9000 s3 rm s3://databend/ --recursive
```

2. After the removal, you can verify using BendSQL that querying the table in Databend fails:

```sql
SELECT * FROM books;
```

```bash
error: APIError: QueryFailed: [3001]NotFound (persistent) at read, context: { uri: http://127.0.0.1:9000/databend/1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk, response: Parts { status: 404, version: HTTP/1.1, headers: {"accept-ranges": "bytes", "content-length": "423", "content-type": "application/xml", "server": "MinIO", "strict-transport-security": "max-age=31536000; includeSubDomains", "vary": "Origin", "vary": "Accept-Encoding", "x-amz-id-2": "dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8", "x-amz-request-id": "18342C51C209C7E9", "x-content-type-options": "nosniff", "x-ratelimit-limit": "144", "x-ratelimit-remaining": "144", "x-xss-protection": "1; mode=block", "date": "Mon, 07 Apr 2025 23:14:45 GMT"} }, service: s3, path: 1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk, range: 0- } => S3Error { code: "NoSuchKey", message: "The specified key does not exist.", resource: "/databend/1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk", request_id: "18342C51C209C7E9" }
```

3. Run the following command to restore your Databend data to the **databend** bucket in MinIO:

```bash
./databend-bendsave restore \
  --from "s3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1" \
  --to-query ../configs/databend-query.toml \
  --to-meta ../configs/databend-meta.toml \
  --confirm
<jemalloc>: Number of CPUs detected is not deterministic. Per-CPU arena disabled.
Restoring from s3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1 to query ../configs/databend-query.toml and meta ../configs/databend-meta.toml with confirmation
```

4. After the restore completes, you can verify that the files were written back to the **databend** bucket by listing its contents:

```bash
aws --endpoint-url http://127.0.0.1:9000 s3 ls s3://databend/ --recursive
```

```bash
2025-04-07 23:21:39        748 1/169/_b/h0196160323247b1cab49be6060d42df8_v2.parquet
2025-04-07 23:21:39        646 1/169/_sg/h0196160323247c5eb0a1a860a6442c70_v4.mpk
2025-04-07 23:21:39        550 1/169/_ss/h019610dcc72474adb32ef43698db2a09_v4.mpk
2025-04-07 23:21:39        143 1/169/last_snapshot_location_hint_v2
2025-04-07 23:21:39     344781 databend_meta.db
```

5. Query the table again using BendSQL, and you will see that the query now succeeds:

```sql
SELECT * FROM books;
```

```sql
┌────────────────────────────────────────────────────────┐
│        id        │       title      │       genre      │
├──────────────────┼──────────────────┼──────────────────┤
│                1 │ Invisible Stars  │ General          │
└────────────────────────────────────────────────────────┘
```
