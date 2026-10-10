---
title: CREATE CONNECTION
summary: 外部ストレージへの接続を作成します。
---

# CREATE CONNECTION

外部ストレージへの接続を作成します。

> **Warning:**
>
> 重要: オブジェクト（stage、テーブルなど）が接続を使用する場合、その接続のパラメータはコピーされ、永続的に保存されます。後で `CREATE OR REPLACE CONNECTION` を使用して接続を変更しても、既存のオブジェクトは引き続き古いパラメータを使用します。新しい接続パラメータでオブジェクトを更新するには、それらのオブジェクトを削除して再作成する必要があります。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] CONNECTION [ IF NOT EXISTS ] <connection_name>
    STORAGE_TYPE = '<type>'
    [ <storage_params> ]
```

| パラメータ        | 説明                                                                                                                                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| STORAGE_TYPE     | ストレージサービスの種類です。指定可能な値には `s3`、`azblob`、`gcs`、`oss`、`cos` があります。                                                         |
| storage_params   | ストレージの種類と認証方法によって異なります。完全な一覧については [Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。 |

## 接続パラメータ {#connection-parameters}

接続には、特定のストレージバックエンドに対する認証情報と設定が含まれます。接続を作成する際は、適切な `STORAGE_TYPE` を選択し、必要なパラメータを指定してください。次の表は一般的なオプションを示しています。

| STORAGE_TYPE | 一般的なパラメータ | 説明 |
|--------------|-------------------|-------------|
| `s3`         | `ACCESS_KEY_ID`/`SECRET_ACCESS_KEY`、または `ROLE_ARN`/`EXTERNAL_ID`、任意で `ENDPOINT_URL`、`REGION` | Amazon S3 および S3 互換サービス（MinIO、Cloudflare R2 など）。 |
| `azblob`     | `ACCOUNT_NAME`、`ACCOUNT_KEY`、`ENDPOINT_URL` | Azure Blob Storage。 |
| `gcs`        | `CREDENTIAL`（base64 エンコードされたサービスアカウントキー） | Google Cloud Storage。 |
| `oss`        | `ACCESS_KEY_ID`、`ACCESS_KEY_SECRET`、`ENDPOINT_URL` | Alibaba Cloud Object Storage Service。 |
| `cos`        | `SECRET_ID`、`SECRET_KEY`、`ENDPOINT_URL` | Tencent Cloud Object Storage。 |
| `hf`         | `REPO_TYPE`、`REVISION`、任意で `TOKEN` | Hugging Face Hub のデータセットおよびモデル。 |

パラメータの意味、任意フラグ、追加のストレージタイプについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。以下のタブを展開すると、ストレージ固有の例を確認できます。

<SimpleTab groupId="connection-storage-types">

<div label="Amazon S3" value="s3">

Amazon S3 および S3 互換サービスでは、認証方法を選択してください。

<SimpleTab groupId="s3-auth-methods">

<div label="Access Keys" value="access-keys">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';
```

| パラメータ | 説明 |
|-----------|-------------|
| ACCESS_KEY_ID | AWS access key ID。 |
| SECRET_ACCESS_KEY | AWS secret access key。 |

</div>

<div label="IAM Role" value="iam-role">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ROLE_ARN = '<your-role-arn>';
```

| パラメータ | 説明 |
|-----------|-------------|
| ROLE_ARN  | {{{ .lake }}} が S3 リソースにアクセスするために引き受ける IAM ロールの Amazon Resource Name (ARN)。 |

</div>
</SimpleTab>

</div>

<div label="Azure Blob" value="azblob">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'azblob'
    ACCOUNT_NAME = '<account-name>'
    ACCOUNT_KEY = '<account-key>'
    ENDPOINT_URL = 'https://<account-name>.blob.core.windows.net';
```

</div>

<div label="Google Cloud Storage" value="gcs">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'gcs'
    CREDENTIAL = '<base64-encoded-service-account>';
```

</div>

<div label="Alibaba Cloud OSS" value="oss">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'oss'
    ACCESS_KEY_ID = '<your-ak>'
    ACCESS_KEY_SECRET = '<your-sk>'
    ENDPOINT_URL = 'https://<region-id>[-internal].aliyuncs.com';
```

</div>

<div label="Tencent COS" value="cos">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'cos'
    SECRET_ID = '<your-secret-id>'
    SECRET_KEY = '<your-secret-key>'
    ENDPOINT_URL = '<your-endpoint-url>';
```

</div>

<div label="Hugging Face" value="hf">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'hf'
    REPO_TYPE = 'dataset'
    REVISION = 'main'
    TOKEN = '<optional-access-token>';
```

公開リポジトリでは `TOKEN` を省略し、プライベートまたはレート制限のあるアセットでは含めてください。

</div>
</SimpleTab>

## アクセス制御要件 {#access-control-requirements}

| 権限         | オブジェクトタイプ | 説明           |
|:------------------|:------------|:----------------------|
| CREATE CONNECTION | Global      | 接続を作成します。 |

接続を作成するには、操作を実行するユーザーまたは [current_role](/tidb-cloud-lake/guides/roles.md) が CREATE CONNECTION [privilege](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

## テーブル接続の更新 {#update-table-connections}

既存のテーブルを新しい接続に切り替えるには、[`ALTER TABLE ... CONNECTION`](/tidb-cloud-lake/sql/alter-table.md#external-table-connection) を使用します。このコマンドは、テーブルを再作成せずに外部テーブルを別の接続へ再バインドします。

## 例 {#examples}

### Access Keys を使用する {#using-access-keys}

この例では、`toronto` という名前の Amazon S3 への接続を作成し、その `toronto` 接続を使用して、`s3://lake-toronto` URL にリンクされた `my_s3_stage` という名前の外部 stage を作成します。接続に関するより実践的な例については、[使用例](/tidb-cloud-lake/sql/connection.md#usage-examples) を参照してください。

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (CONNECTION_NAME = 'toronto');
```

### AWS IAM Role を使用する {#using-aws-iam-role}

この例では、IAM ロールを使用して Amazon S3 への接続を作成し、その後この接続を使用する stage を作成します。この方法は、アクセスキーを {{{ .lake }}} に保存する必要がないため、より安全です。

```sql
CREATE CONNECTION lake_test
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test';

CREATE STAGE lake_test
    URL = 's3://test-bucket-123'
    CONNECTION = (CONNECTION_NAME = 'lake_test');

-- You can now query data from your S3 bucket
SELECT * FROM @lake_test/test.parquet LIMIT 1;
```

> **Note:**
>
> {{{ .lake }}} で IAM ロールを使用するには、AWS アカウントと {{{ .lake }}} の間に信頼関係を設定する必要があります。詳細な手順については、[AWS IAM Role による認証](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) を参照してください。