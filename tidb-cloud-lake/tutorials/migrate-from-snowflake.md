---
title: Snowflake から TiDB Cloud Lake へ移行する
summary: データを Amazon S3 にエクスポートし、それを TiDB Cloud Lake のテーブルにロードすることで、Snowflake から TiDB Cloud Lake にデータを移行します。
---

# Snowflake から TiDB Cloud Lake へ移行する

> **Capabilities**: Full Load

このチュートリアルでは、Snowflake から {{{ .lake }}} にデータを移行する手順を説明します。移行では、Snowflake から Amazon S3 バケットにデータをエクスポートし、その後 {{{ .lake }}} にロードします。プロセスは次の 3 つの主要なステップに分かれています。

![alt text](/media/tidb-cloud-lake/migrate-from-snowflake.png)

このチュートリアルでは、Snowflake から Parquet 形式で Amazon S3 バケットにデータをエクスポートし、その後 {{{ .lake }}} にロードする手順を説明します。

## 開始前に {#before-you-start}

開始する前に、次の前提条件を満たしていることを確認してください。

- **Amazon S3 Bucket**: エクスポートしたデータを保存するための S3 バケットと、ファイルをアップロードするために必要な権限が必要です。[S3 バケットの作成方法](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。このチュートリアルでは、エクスポートしたデータを stage する場所として `s3://lake-doc/snowflake/` を使用します。
- **AWS Credentials**: S3 バケットにアクセスするための十分な権限を持つ AWS Access Key ID と Secret Access Key が必要です。[AWS 認証情報の管理](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)を参照してください。
- **IAM Roles と Policies を管理する権限**: Snowflake と Amazon S3 間のアクセスを設定するために必要な IAM roles と policies を作成および管理する権限があることを確認してください。[IAM roles と policies について](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を参照してください。

## Step 1: Amazon S3 用の Snowflake Storage Integration を設定する {#step-1-configuring-snowflake-storage-integration-for-amazon-s3}

このステップでは、IAM roles を使用して Snowflake が Amazon S3 にアクセスできるように設定します。まず IAM role を作成し、その後その role を使用して、安全なデータアクセスのための Snowflake Storage Integration を確立します。

1. AWS Management Console にサインインし、**IAM** > **Policies** で次の JSON コードを使って policy を作成します。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:PutObject",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:DeleteObject",
            "s3:DeleteObjectVersion"
          ],
          "Resource": "arn:aws:s3:::lake-doc/snowflake/*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
          "Resource": "arn:aws:s3:::lake-doc",
          "Condition": {
            "StringLike": {
              "s3:prefix": ["snowflake/*"]
            }
          }
        }
      ]
    }
    ```

    この policy は、`lake-doc` という名前の S3 バケットと、そのバケット内の `snowflake` フォルダに対して適用されます。

    - `s3:PutObject`, `s3:GetObject`, `s3:GetObjectVersion`, `s3:DeleteObject`, `s3:DeleteObjectVersion`: snowflake フォルダ内のオブジェクト（例: `s3://lake-doc/snowflake/`）に対する操作を許可します。このフォルダ内でオブジェクトのアップロード、読み取り、削除ができます。
    - `s3:ListBucket`, `s3:GetBucketLocation`: `lake-doc` バケットの内容一覧の取得と、そのロケーションの取得を許可します。`Condition` 要素により、一覧取得は `snowflake` フォルダ内のオブジェクトに制限されます。

2. **IAM** > **Roles** で `lake-doc-role` という名前の role を作成し、先ほど作成した policy をアタッチします。
    - role 作成の最初のステップで、**Trusted entity type** に **AWS account**、**An AWS account** に **This account (xxxxx)** を選択します。

    ![alt text](/media/tidb-cloud-lake/trusted-entity.png)

    - role の作成後、role ARN をコピーして安全な場所に保存します。例: `arn:aws:iam::123456789012:role/lake-doc-role`
    - Snowflake アカウントの IAM user ARN を取得した後で、この role の **Trust Relationships** を更新します。

3. Snowflake で SQL worksheet を開き、role ARN を使用して `my_s3_integration` という名前の storage integration を作成します。

    ```sql
    CREATE OR REPLACE STORAGE INTEGRATION my_s3_integration
      TYPE = EXTERNAL_STAGE
      STORAGE_PROVIDER = 'S3'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-doc-role'
      STORAGE_ALLOWED_LOCATIONS = ('s3://lake-doc/snowflake/')
      ENABLED = TRUE;
    ```

4. storage integration の詳細を表示し、結果内の `STORAGE_AWS_IAM_USER_ARN` プロパティの値を取得します。例: `arn:aws:iam::123456789012:user/example`。この値は、次のステップで role `lake-doc-role` の **Trust Relationships** を更新するために使用します。

    ```sql
    DESCRIBE INTEGRATION my_s3_integration;
    ```

5. AWS Management Console に戻り、role `lake-doc-role` を開いて **Trust relationships** > **Edit trust policy** に移動します。次のコードをエディタにコピーします。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::123456789012:user/example"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    ```

    `arn:aws:iam::123456789012:user/example` という ARN は、前のステップで取得した Snowflake アカウントの IAM user ARN です。

## Step 2: Amazon S3 へのデータの準備とエクスポート {#step-2-preparing-and-exporting-data-to-amazon-s3}

1. Snowflake で、Snowflake storage integration `my_s3_integration` を使用して external stage を作成します。

    ```sql
    CREATE OR REPLACE STAGE my_external_stage
        URL = 's3://lake-doc/snowflake/'
        STORAGE_INTEGRATION = my_s3_integration
        FILE_FORMAT = (TYPE = 'PARQUET');
    ```

    `URL = 's3://lake-doc/snowflake/'` は、データを stage する S3 バケットとフォルダを指定します。パス `s3://lake-doc/snowflake/` は、S3 バケット `lake-doc` と、そのバケット内の `snowflake` フォルダに対応します。

2. エクスポートするデータを準備します。

    ```sql
    CREATE DATABASE doc;
    USE DATABASE doc;

    CREATE TABLE my_table (
        id INT,
        name STRING,
        age INT
    );

    INSERT INTO my_table (id, name, age) VALUES
    (1, 'Alice', 30),
    (2, 'Bob', 25),
    (3, 'Charlie', 35);
    ```

3. `COPY INTO` を使用して、テーブルデータを external stage にエクスポートします。

    ```sql
    COPY INTO @my_external_stage/my_table_data_
    FROM my_table
    FILE_FORMAT = (TYPE = 'PARQUET') HEADER=true;
    ```

    `lake-doc` バケットを開くと、`snowflake` フォルダ内に Parquet ファイルが表示されます。

## Step 3: {{{ .lake }}} へのデータのロード (load) {#step-3-loading-data-into-lake}

1. {{{ .lake }}} にターゲットテーブルを作成します。

    ```sql
    CREATE DATABASE doc;
    USE DATABASE doc;

    CREATE TABLE my_target_table (
        id INT,
        name STRING,
        age INT
    );
    ```

2. [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) を使用して、バケット内のエクスポート済みデータをロードします。

    ```sql
    COPY INTO my_target_table
    FROM 's3://lake-doc/snowflake'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    )
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (
        TYPE = 'PARQUET'
    );
    ```

3. ロードしたデータを確認します。

```sql
SELECT * FROM my_target_table;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │       age       │
├─────────────────┼──────────────────┼─────────────────┤
│               1 │ Alice            │              30 │
│               2 │ Bob              │              25 │
│               3 │ Charlie          │              35 │
└──────────────────────────────────────────────────────┘
```