---
title: 接続パラメータ
summary: 接続パラメータは、`CREATE CONNECTION` を使用して再利用可能な接続を作成する際に指定するキーと値のペアです。接続を作成した後は、`CONNECTION = (CONNECTION_NAME = '<connection-name>')` を使用して、stage、`COPY` コマンド、およびその他の SQL 機能からその接続を参照できます。完全な構文と使用方法については、`CREATE CONNECTION` を参照してください。
---

# Connection Parameters

接続パラメータは、`CREATE CONNECTION` を使用して再利用可能な接続を作成する際に指定するキーと値のペアです。接続を作成した後は、`CONNECTION = (CONNECTION_NAME = '<connection-name>')` を使用して、stage、COPY コマンド、およびその他の SQL 機能からその接続を参照できます。完全な構文と使用方法については、[CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) を参照してください。

ストレージ固有の接続詳細については、以下の表を参照してください。

<SimpleTab groupId="operating-systems">

<div label="Amazon S3" value="Amazon S3">

以下の表は、Amazon S3 互換ストレージサービスにアクセスするための接続パラメータを示しています。

| パラメーター                | 必須?      | 説明                                                          |
|--------------------------- |----------- |-------------------------------------------------------------- |
| endpoint_url               | Yes        | Amazon S3 互換ストレージサービスのエンドポイント URL。              |
| access_key_id              | Yes        | リクエスタを識別するためのアクセスキー ID。                         |
| secret_access_key          | Yes        | 認証用のシークレットアクセスキー。                                 |
| enable_virtual_host_style  | No         | 仮想ホスト形式 URL を使用するかどうか。デフォルトは *false*。        |
| master_key                 | No         | 高度なデータ暗号化のためのオプションのマスターキー。                 |
| region                     | No         | バケットが配置されている AWS リージョン。                          |
| security_token             | No         | 一時的な認証情報のためのセキュリティトークン。                      |

> **Note:**
>
> - コマンドで **endpoint_url** パラメータが指定されていない場合、{{{ .lake }}} はデフォルトで Amazon S3 上に stage を作成します。そのため、S3 互換オブジェクトストレージやその他のオブジェクトストレージソリューション上に外部 stage を作成する場合は、必ず **endpoint_url** パラメータを含めてください。
>
> - **region** パラメータは、{{{ .lake }}} がリージョン情報を自動検出できるため必須ではありません。通常、このパラメータの値を手動で指定する必要はありません。自動検出に失敗した場合、{{{ .lake }}} はデフォルトで 'us-east-1' をリージョンとして使用します。MinIO とともに {{{ .lake }}} をデプロイし、リージョン情報を設定していない場合も、自動的に 'us-east-1' が使用され、正常に動作します。ただし、"region is missing" や "The bucket you are trying to access requires a specific endpoint. Please direct all future requests to this particular endpoint" のようなエラーメッセージが表示された場合は、リージョン名を確認し、**region** パラメータに明示的に設定する必要があります。

```sql title='Examples'
-- Create a reusable connection for Amazon S3
CREATE CONNECTION my_s3_conn
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-ak>'
  SECRET_ACCESS_KEY = '<your-sk>';

-- Use the connection when creating a stage
CREATE STAGE my_s3_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_s3_conn');

-- Create a reusable connection for an S3-compatible service such as MinIO
CREATE CONNECTION my_minio_conn
  STORAGE_TYPE = 's3'
  ENDPOINT_URL = 'http://localhost:9000'
  ACCESS_KEY_ID = 'ROOTUSER'
  SECRET_ACCESS_KEY = 'CHANGEME123';

CREATE STAGE my_minio_stage
  URL = 's3://lake'
  CONNECTION = (CONNECTION_NAME = 'my_minio_conn');
```

Amazon S3 バケットにアクセスするために、認証用の AWS IAM ロールと external ID を指定することもできます。AWS IAM ロールと external ID を指定することで、ユーザーがアクセスできる S3 バケットをより細かく制御できます。つまり、IAM ロールに特定の S3 バケットへのアクセス権限のみが付与されている場合、ユーザーはそのバケットにのみアクセスできます。external ID は、追加の検証レイヤーを提供することで、さらにセキュリティを強化できます。詳細については、<https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html> を参照してください。

以下の表は、AWS IAM ロール認証を使用して Amazon S3 ストレージサービスにアクセスするための接続パラメータを示しています。

| パラメーター   | 必須?      | 説明                                                   |
|-------------- |----------- |------------------------------------------------------- |
| endpoint_url  | No         | Amazon S3 のエンドポイント URL。                        |
| role_arn      | Yes        | S3 への認可に使用する AWS IAM ロールの ARN。             |
| external_id   | No         | ロール引き受け時のセキュリティを強化するための external ID。  |

```sql title='Examples'
-- Create the connection using IAM role authentication
CREATE CONNECTION my_iam_conn
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/my-role'
  EXTERNAL_ID = 'my-external-id';

-- Reference the connection when creating a stage
CREATE STAGE my_iam_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_iam_conn');
```

</div>

<div label="Azure Blob" value="Azure Blob">

以下の表は、Azure Blob Storage にアクセスするための接続パラメータを示しています。

| パラメーター      | 必須?   | 説明                                           |
|----------------|-------------|-------------------------------------------------------|
| endpoint_url   | はい         | Azure Blob Storage のエンドポイント URL。               |
| account_key    | はい         | 認証用の Azure Blob Storage アカウントキー。            |
| account_name   | はい         | 識別用の Azure Blob Storage アカウント名。              |

```sql title='Examples'
-- Create a connection for Azure Blob Storage
CREATE CONNECTION my_azure_conn
  STORAGE_TYPE = 'azblob'
  ACCOUNT_NAME = 'myaccount'
  ACCOUNT_KEY = 'myaccountkey'
  ENDPOINT_URL = 'https://<your-storage-account-name>.blob.core.windows.net';

-- Create a stage that uses the connection
CREATE STAGE my_azure_stage
  URL = 'azblob://my-container'
  CONNECTION = (CONNECTION_NAME = 'my_azure_conn');
```

</div>

<div label="Google GCS" value="Google GCS">

以下の表は、Google Cloud Storage にアクセスするための接続パラメータを示しています。

| パラメータ      | 必須?   | 説明                                           |
|----------------|-------------|-------------------------------------------------------|
| credential     | はい         | 認証用の Google Cloud Storage 認証情報。               |

`credential` を取得するには、Google のドキュメントにある [Create a service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating) の手順に従ってサービスアカウントキーファイルを作成し、ダウンロードできます。サービスアカウントキーファイルをダウンロードした後、次のコマンドで base64 文字列に変換できます。

```
base64 -i -o ~/Desktop/base64-encoded-key.txt
```

```sql title='Examples'
-- Create the connection with the base64-encoded credential
CREATE CONNECTION my_gcs_conn
  STORAGE_TYPE = 'gcs'
  CREDENTIAL = '<your-base64-encoded-credential>';

-- Use the connection when creating a stage
CREATE STAGE my_gcs_stage
  URL = 'gcs://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_gcs_conn');
```

</div>

<div label="Alibaba Cloud OSS" value="Alibaba OSS">

以下の表は、Alibaba Cloud OSS にアクセスするための接続パラメータを示しています。

| パラメーター          | 必須?      | 説明                                                     |
|---------------------- |----------- |--------------------------------------------------------- |
| access_key_id         | Yes        | 認証用の Alibaba Cloud OSS access key ID。                |
| access_key_secret     | Yes        | 認証用の Alibaba Cloud OSS access key secret。            |
| endpoint_url          | Yes        | Alibaba Cloud OSS のエンドポイント URL。                  |
| presign_endpoint_url  | No         | Alibaba Cloud OSS URL の事前署名に使用するエンドポイント URL。 |

```sql title='Examples'
-- Create a connection for Alibaba Cloud OSS
CREATE CONNECTION my_oss_conn
  STORAGE_TYPE = 'oss'
  ACCESS_KEY_ID = '<your-ak>'
  ACCESS_KEY_SECRET = '<your-sk>'
  ENDPOINT_URL = 'https://<bucket-name>.<region-id>[-internal].aliyuncs.com';

-- Create a stage using the connection
CREATE STAGE my_oss_stage
  URL = 'oss://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_oss_conn');
```

</div>

<div label="Tencent COS" value="Tencent COS">

以下の表は、Tencent Cloud Object Storage (COS) にアクセスするための接続パラメータを示しています。

| パラメーター     | 必須?  | 説明                                                  |
|-------------- |----------- |------------------------------------------------------------- |
| endpoint_url  | Yes        | Tencent Cloud Object Storage のエンドポイント URL。            |
| secret_id     | Yes        | 認証用の Tencent Cloud Object Storage secret ID。             |
| secret_key    | Yes        | 認証用の Tencent Cloud Object Storage secret key。            |

```sql title='Examples'
-- Create a connection for Tencent COS
CREATE CONNECTION my_cos_conn
  STORAGE_TYPE = 'cos'
  SECRET_ID = '<your-secret-id>'
  SECRET_KEY = '<your-secret-key>'
  ENDPOINT_URL = '<your-endpoint-url>';

-- Create a stage that uses the connection
CREATE STAGE my_cos_stage
  URL = 'cos://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_cos_conn');
```

</div>

<div label="HuggingFace" value="Hugging Face">

以下の表は、Hugging Face にアクセスするための接続パラメータを示しています。

| パラメーター | 必須?             | 説明                                                                                                     |
|-----------|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| repo_type | No (default: dataset) | Hugging Face リポジトリのタイプ。`dataset` または `model` を指定できます。                                      |
| revision  | No (default: main)    | Hugging Face URI のリビジョン。リポジトリのブランチ、タグ、またはコミットを指定できます。                       |
| token     | No                    | Hugging Face の API トークン。プライベートリポジトリや特定のリソースへのアクセスに必要な場合があります。         |

```sql title='Examples'
-- Create a connection for Hugging Face
CREATE CONNECTION my_hf_conn
  STORAGE_TYPE = 'hf'
  REPO_TYPE = 'dataset'
  REVISION = 'main';

-- Create a stage that uses the connection
CREATE STAGE my_huggingface_stage
  URL = 'hf://opendal/huggingface-testdata/'
  CONNECTION = (CONNECTION_NAME = 'my_hf_conn');
```

</div>
</SimpleTab>