---
title: Ingest JSON Logs with Vector (Cloud)
---

In this tutorial, we'll simulate generating logs locally, collect them using [Vector](https://vector.dev/), store them in S3, and automate their ingestion into Databend Cloud using scheduled tasks.

![Automating JSON Log Loading with Vector](@site/static/img/documents/tutorials/vector-tutorial.png)

## Before You Start

Before you start, ensure you have the following prerequisites in place:

- **Amazon S3 Bucket**: An S3 bucket where logs collected by Vector will be stored. [Learn how to create an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).
- **AWS Credentials**: AWS Access Key ID and Secret Access Key with sufficient permissions for accessing your S3 bucket. [Manage your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).
- **AWS CLI**: Ensure that the [AWS CLI](https://aws.amazon.com/cli/) is installed and configured with the necessary permissions to access your S3 bucket.
- **Docker**: Ensure that [Docker](https://www.docker.com/) is installed on your local machine, as it will be used to set up Vector.

## Step 1: Create a Target Folder in S3 Bucket

To store the logs collected by Vector, create a folder named logs in your S3 bucket. In this tutorial, we use `s3://databend-doc/logs/` as the target location. 

This command creates an empty folder named `logs` in the `databend-doc` bucket:

```bash
aws s3api put-object --bucket databend-doc --key logs/
```

## Step 2: Create a Local Log File

Simulate log generation by creating a local log file. In this tutorial, we use `/Users/eric/Documents/logs/app.log` as the file path.

Add the following JSON lines to the file to represent sample log events:

```json title='app.log'
{"user_id": 1, "event": "login", "timestamp": "2024-12-08T10:00:00Z"}
{"user_id": 2, "event": "purchase", "timestamp": "2024-12-08T10:05:00Z"}
```

## Step 3: Configure & Run Vector

1. Create a Vector configuration file named `vector.yaml` on your local machine. In this tutorial, we create it at `/Users/eric/Documents/vector.yaml` with the following content:

```yaml title='vector.yaml'
sources:
  logs:
    type: file
    include:
      - "/logs/app.log"
    read_from: beginning

transforms:
  extract_message:
    type: remap
    inputs:
      - "logs"
    source: |
      . = parse_json(.message) ?? {}

sinks:
  s3:
    type: aws_s3
    inputs:
      - "extract_message"
    bucket: databend-doc
    region: us-east-2
    key_prefix: "logs/" 
    content_type: "text/plain" 
    encoding:
      codec: "native_json" 
    auth:
      access_key_id: "<your-access-key-id>"
      secret_access_key: "<your-secret-access-key>"
```

2. Start Vector using Docker, mapping the configuration file and local logs directory:

```bash
docker run \
  -d \
  -v /Users/eric/Documents/vector.yaml:/etc/vector/vector.yaml:ro \
  -v /Users/eric/Documents/logs:/logs \
  -p 8686:8686 \
  --name vector \
  timberio/vector:nightly-alpine
```

3. Wait for a moment, then check if any logs have been synced to the `logs` folder on S3:

```bash
aws s3 ls s3://databend-doc/logs/
```

If the log file has been successfully synced to S3, you should see output similar to this:

```bash
2024-12-10 15:22:13          0
2024-12-10 17:52:42        112 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz
```

You can now download the synced log file from your bucket:

```bash
aws s3 cp s3://databend-doc/logs/1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz ~/Documents/
```

Compared to the original log, the synced log is in NDJSON format, with each record wrapped in an outer `log` field:

```json
{"log":{"event":"login","timestamp":"2024-12-08T10:00:00Z","user_id":1}}
{"log":{"event":"purchase","timestamp":"2024-12-08T10:05:00Z","user_id":2}}
```

## Step 4: Create a Task in Databend Cloud

1. Open a worksheet, and create an external stage that links to the `logs` folder in your bucket:

```sql
CREATE STAGE mylog 's3://databend-doc/logs/' CONNECTION=(
    ACCESS_KEY_ID = '<your-access-key-id>',
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

Once the stage is successfully created, you can list the files in it:

```sql
LIST @mylog;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          name                          │  size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz │    112 │ "231ddcc590222bfaabd296b151154844" │ 2024-12-10 22:52:42.000 +0000 │ NULL             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

2. Create a table with columns mapped to the fields in the log:

```sql
CREATE TABLE logs (
    event String,
    timestamp Timestamp,
    user_id Int32
);
```

3. Create a scheduled task to load logs from the external stage into the `logs` table:

```sql
CREATE TASK IF NOT EXISTS myvectortask
    WAREHOUSE = 'eric'
    SCHEDULE = 1 MINUTE
    SUSPEND_TASK_AFTER_NUM_FAILURES = 3
AS
COPY INTO logs 
FROM (
    SELECT $1:log:event, $1:log:timestamp, $1:log:user_id
    FROM @mylog/
)
FILE_FORMAT = (TYPE = NDJSON, COMPRESSION = AUTO) 
MAX_FILES = 10000 
PURGE = TRUE;
```

4. Start the task:

```sql
ALTER TASK myvectortask RESUME;
```

Wait for a moment, then check if the logs have been loaded into the table:

```sql
SELECT * FROM logs;

┌──────────────────────────────────────────────────────────┐
│       event      │      timestamp      │     user_id     │
├──────────────────┼─────────────────────┼─────────────────┤
│ login            │ 2024-12-08 10:00:00 │               1 │
│ purchase         │ 2024-12-08 10:05:00 │               2 │
└──────────────────────────────────────────────────────────┘
```

If you run `LIST @mylog;` now, you will see no files listed. This is because the task is configured with `PURGE = TRUE`, which deletes the synced files from S3 after the logs are loaded.

Now, let's simulate generating two more logs in the local log file `app.log`:

```bash
echo '{"user_id": 3, "event": "logout", "timestamp": "2024-12-08T10:10:00Z"}' >> /Users/eric/Documents/logs/app.log
echo '{"user_id": 4, "event": "login", "timestamp": "2024-12-08T10:15:00Z"}' >> /Users/eric/Documents/logs/app.log
```

Wait for a moment for the log to sync to S3 (a new file should appear in the `logs` folder). The scheduled task will then load the new logs into the table. If you query the table again, you will find these logs:

```sql
SELECT * FROM logs;

┌──────────────────────────────────────────────────────────┐
│       event      │      timestamp      │     user_id     │
├──────────────────┼─────────────────────┼─────────────────┤
│ logout           │ 2024-12-08 10:10:00 │               3 │
│ login            │ 2024-12-08 10:15:00 │               4 │
│ login            │ 2024-12-08 10:00:00 │               1 │
│ purchase         │ 2024-12-08 10:05:00 │               2 │
└──────────────────────────────────────────────────────────┘
```
