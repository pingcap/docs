---
title: Vector を使用した JSON ログの取り込み (Cloud)
summary: このチュートリアルでは、ローカルでのログ生成をシミュレートし、[Vector](https://vector.dev/) を使用して収集し、S3 に保存し、スケジュールされたタスクを使用して {{{ .lake }}} への取り込みを自動化します。
---

# Vector を使用した JSON ログの取り込み (Cloud)

このチュートリアルでは、ローカルでのログ生成をシミュレートし、[Vector](https://vector.dev/) を使用して収集し、S3 に保存し、スケジュールされたタスクを使用して {{{ .lake }}} への取り込みを自動化します。

![Vector による JSON ログのロード自動化](/media/tidb-cloud-lake/vector-tutorial.png)

## 始める前に {#before-you-start}

開始する前に、次の前提条件を満たしていることを確認してください。

- **Amazon S3 Bucket**: Vector が収集したログを保存する S3 バケット。[S3 バケットの作成方法](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。
- **AWS Credentials**: S3 バケットにアクセスするための十分な権限を持つ AWS Access Key ID と Secret Access Key。[AWS 認証情報の管理](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)を参照してください。
- **AWS CLI**: [AWS CLI](https://aws.amazon.com/cli/) がインストールされており、S3 バケットにアクセスするために必要な権限で設定されていることを確認してください。
- **Docker**: Vector のセットアップに使用するため、ローカルマシンに [Docker](https://www.docker.com/) がインストールされていることを確認してください。

## ステップ 1: S3 バケットに対象フォルダを作成する {#step-1-create-a-target-folder-in-s3-bucket}

Vector が収集したログを保存するために、S3 バケットに `logs` という名前のフォルダを作成します。このチュートリアルでは、対象の保存先として `s3://lake-doc/logs/` を使用します。

このコマンドは、`lake-doc` バケットに `logs` という名前の空のフォルダを作成します。

```bash
aws s3api put-object --bucket lake-doc --key logs/
```

## ステップ 2: ローカルログファイルを作成する {#step-2-create-a-local-log-file}

ローカルログファイルを作成して、ログ生成をシミュレートします。このチュートリアルでは、ファイルパスとして `/Users/eric/Documents/logs/app.log` を使用します。

サンプルのログイベントを表すために、次の JSON Lines をファイルに追加します。

```json title='app.log'
{"user_id": 1, "event": "login", "timestamp": "2024-12-08T10:00:00Z"}
{"user_id": 2, "event": "purchase", "timestamp": "2024-12-08T10:05:00Z"}
```

## ステップ 3: Vector を設定して実行する {#step-3-configure-run-vector}

1. ローカルマシンに `vector.yaml` という名前の Vector 設定ファイルを作成します。このチュートリアルでは、`/Users/eric/Documents/vector.yaml` に次の内容で作成します。

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

2. 設定ファイルとローカルのログディレクトリをマウントして、Docker を使用して Vector を起動します。

    ```bash
    docker run \
      -d \
      -v /Users/eric/Documents/vector.yaml:/etc/vector/vector.yaml:ro \
      -v /Users/eric/Documents/logs:/logs \
      -p 8686:8686 \
      --name vector \
      timberio/vector:nightly-alpine
    ```

3. 少し待ってから、ログが S3 上の `logs` フォルダに同期されているか確認します。

```bash
aws s3 ls s3://lake-doc/logs/
```

ログファイルが S3 に正常に同期されていれば、次のような出力が表示されます。

```bash
2024-12-10 15:22:13          0
2024-12-10 17:52:42        112 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz
```

これで、同期されたログファイルをバケットからダウンロードできます。

```bash
aws s3 cp s3://lake-doc/logs/1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz ~/Documents/
```

元のログと比較すると、同期されたログは NDJSON 形式になっており、各レコードは外側の `log` フィールドでラップされています。

```json
{"log":{"event":"login","timestamp":"2024-12-08T10:00:00Z","user_id":1}}
{"log":{"event":"purchase","timestamp":"2024-12-08T10:05:00Z","user_id":2}}
```

## Step 4: {{{ .lake }}} でタスクを作成する {#step-4-create-a-task-in-lake}

1. Worksheet を開き、バケット内の `logs` フォルダにリンクする外部 stage を作成します。

    ```sql
    CREATE STAGE mylog 's3://lake-doc/logs/' CONNECTION=(
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );
    ```

    stage の作成に成功すると、その中のファイルを一覧表示できます。

    ```sql
    LIST @mylog;
    
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                          name                          │  size  │                 md5                │         last_modified         │      creator     │
    ├────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
    │ 1733871161-7b89e50a-6eb4-4531-8479-dd46981e4674.log.gz │    112 │ "231ddcc590222bfaabd296b151154844" │ 2024-12-10 22:52:42.000 +0000 │ NULL             │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

2. ログ内のフィールドに対応するカラムを持つテーブルを作成します。

    ```sql
    CREATE TABLE logs (
        event String,
        timestamp Timestamp,
        user_id Int32
    );
    ```

3. 外部 stage から `logs` テーブルにログをロードするスケジュールタスクを作成します。

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

4. タスクを開始します。

```sql
ALTER TASK myvectortask RESUME;
```

少し待ってから、ログがテーブルにロードされているか確認します。

```sql
SELECT * FROM logs;

┌──────────────────────────────────────────────────────────┐
│       event      │      timestamp      │     user_id     │
├──────────────────┼─────────────────────┼─────────────────┤
│ login            │ 2024-12-08 10:00:00 │               1 │
│ purchase         │ 2024-12-08 10:05:00 │               2 │
└──────────────────────────────────────────────────────────┘
```

この時点で `LIST @mylog;` を実行すると、ファイルは何も表示されません。これは、タスクが `PURGE = TRUE` で設定されており、ログのロード後に同期済みファイルが S3 から削除されるためです。

次に、ローカルのログファイル `app.log` にさらに 2 件のログを生成することをシミュレートします。

```bash
echo '{"user_id": 3, "event": "logout", "timestamp": "2024-12-08T10:10:00Z"}' >> /Users/eric/Documents/logs/app.log
echo '{"user_id": 4, "event": "login", "timestamp": "2024-12-08T10:15:00Z"}' >> /Users/eric/Documents/logs/app.log
```

ログが S3 に同期されるまで少し待ちます（`logs` フォルダに新しいファイルが表示されるはずです）。その後、スケジュールタスクによって新しいログがテーブルにロードされます。再度テーブルをクエリすると、次のログを確認できます。

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