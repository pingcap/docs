---
title: 使用 Vector 导入 JSON 日志（Cloud）
summary: 在本教程中，我们将模拟在本地生成日志，使用 Vector 收集日志，将其存储到 S3，并通过定时任务自动将其导入到 {{{ .lake }}}。
---

# 使用 Vector 导入 JSON 日志（Cloud）

在本教程中，我们将模拟在本地生成日志，使用 [Vector](https://vector.dev/) 收集日志，将其存储到 S3，并通过定时任务自动将其导入到 {{{ .lake }}}。

![使用 Vector 自动加载 JSON 日志](/media/tidb-cloud-lake/vector-tutorial.png)

## 开始之前 {#before-you-start}

开始之前，请确保已满足以下前提条件：

- **Amazon S3 Bucket**：一个用于存储 Vector 收集到的日志的 S3 bucket。[了解如何创建 S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。
- **AWS Credentials**：具有足够权限以访问 S3 bucket 的 AWS Access Key ID 和 Secret Access Key。[管理你的 AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)。
- **AWS CLI**：确保已安装 [AWS CLI](https://aws.amazon.com/cli/)，并已配置访问 S3 bucket 所需的权限。
- **Docker**：确保你的本地机器上已安装 [Docker](https://www.docker.com/)，因为后续将使用它来部署 Vector。

## 步骤 1：在 S3 Bucket 中创建目标文件夹 {#step-1-create-a-target-folder-in-s3-bucket}

为了存储 Vector 收集到的日志，请在 S3 bucket 中创建一个名为 logs 的文件夹。在本教程中，我们使用 `s3://lake-doc/logs/` 作为目标位置。

以下命令会在 `lake-doc` bucket 中创建一个名为 `logs` 的空文件夹：

```bash
aws s3api put-object --bucket lake-doc --key logs/
```

## 步骤 2：创建本地日志文件 {#step-2-create-a-local-log-file}

通过创建本地日志文件来模拟日志生成。在本教程中，我们使用 `/Users/eric/Documents/logs/app.log` 作为文件路径。

向该文件中添加以下 JSON 行，作为示例日志事件：

```json title='app.log'
{"user_id": 1, "event": "login", "timestamp": "2024-12-08T10:00:00Z"}
{"user_id": 2, "event": "purchase", "timestamp": "2024-12-08T10:05:00Z"}
```

## 步骤 3：配置并运行 Vector {#step-3-configure-run-vector}

1. 在本地机器上创建一个名为 `vector.yaml` 的 Vector 配置文件。在本教程中，我们在 `/Users/eric/Documents/vector.yaml` 创建该文件，内容如下：

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
        bucket: lake-doc
        region: us-east-2
        key_prefix: "logs/"
        content_type: "text/plain"
        encoding:
          codec: "native_json"
        auth:
          access_key_id: "<your-access-key-id>"
          secret_access_key: "<your-secret-access-key>"
    ```

2. 使用 Docker 启动 Vector，并映射配置文件和本地日志目录：

    ```bash
    docker run \
      -d \
      -v /Users/eric/Documents/vector.yaml:/etc/vector/vector.yaml:ro \
      -v /Users/eric/Documents/logs:/logs \
      -p 8686:8686 \
      --name vector \
      timberio/vector:nightly-alpine
    ```

3. 稍等片刻，然后检查是否已有日志同步到 S3 上的 `logs` 文件夹：

```bash
aws s3 ls s3://lake-doc/logs/
```

如果日志文件已成功同步到 S3，你将看到类似如下的输出：

```bash
2024-12-10 15:22:13          0
2024-12-10 17:52:42        112 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz
```

现在，你可以从 bucket 中下载已同步的日志文件：

```bash
aws s3 cp s3://lake-doc/logs/1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz ~/Documents/
```

与原始日志相比，同步后的日志采用 NDJSON 格式，并且每条记录都包装在外层的 `log` 字段中：

```json
{"log":{"event":"login","timestamp":"2024-12-08T10:00:00Z","user_id":1}}
{"log":{"event":"purchase","timestamp":"2024-12-08T10:05:00Z","user_id":2}}
```

## 步骤 4：在 {{{ .lake }}} 中创建任务 {#step-4-create-a-task-in-lake}

1. 打开一个工作区 (Worksheet)，并创建一个外部 stage，将其链接到存储桶中的 `logs` 文件夹：

    ```sql
    CREATE STAGE mylog 's3://lake-doc/logs/' CONNECTION=(
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );
    ```

    stage 创建成功后，你可以列出其中的文件：

    ```sql
    LIST @mylog;
    
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                          name                          │  size  │                 md5                │         last_modified         │      creator     │
    ├────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
    │ 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz │    112 │ "231ddcc590222bfaabd296b151154844" │ 2024-12-10 22:52:42.000 +0000 │ NULL             │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

2. 创建一个表，并将其列映射到日志中的字段：

    ```sql
    CREATE TABLE logs (
        event String,
        timestamp Timestamp,
        user_id Int32
    );
    ```

3. 创建一个调度任务，将外部 stage 中的日志加载到 `logs` 表中：

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

4. 启动该任务：

```sql
ALTER TASK myvectortask RESUME;
```

稍等片刻，然后检查日志是否已加载到表中：

```sql
SELECT * FROM logs;

┌──────────────────────────────────────────────────────────┐
│       event      │      timestamp      │     user_id     │
├──────────────────┼─────────────────────┼─────────────────┤
│ login            │ 2024-12-08 10:00:00 │               1 │
│ purchase         │ 2024-12-08 10:05:00 │               2 │
└──────────────────────────────────────────────────────────┘
```

如果你现在运行 `LIST @mylog;`，将不会看到任何文件。这是因为该任务配置了 `PURGE = TRUE`，在日志加载完成后会从 S3 中删除已同步的文件。

现在，让我们模拟在本地日志文件 `app.log` 中再生成两条日志：

```bash
echo '{"user_id": 3, "event": "logout", "timestamp": "2024-12-08T10:10:00Z"}' >> /Users/eric/Documents/logs/app.log
echo '{"user_id": 4, "event": "login", "timestamp": "2024-12-08T10:15:00Z"}' >> /Users/eric/Documents/logs/app.log
```

稍等片刻，让日志同步到 S3（`logs` 文件夹中应会出现一个新文件）。随后，调度任务会将新的日志加载到表中。如果你再次查询该表，将会看到这些日志：

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