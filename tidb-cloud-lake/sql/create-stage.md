---
title: CREATE STAGE
summary: 内部または外部の stage を作成します。
---

# CREATE STAGE

内部または外部の stage を作成します。

## 構文 {#syntax}

```sql
-- Internal stage
CREATE [ OR REPLACE ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]

-- External stage
CREATE STAGE [ IF NOT EXISTS ] <external_stage_name>
    externalStageParams
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]
```

### externalStageParams {#externalstageparams}

> **Tip:**
>
> 外部 stage では、インライン認証情報の代わりに、事前設定済みの接続オブジェクトを参照する `CONNECTION` パラメータの使用を推奨します。この方法により、セキュリティと管理性が向上します。

```sql
externalStageParams ::=
  '<protocol>://<location>'
  CONNECTION = (
        <connection_parameters>
  )
|
  CONNECTION = (
        CONNECTION_NAME = '<your-connection-name>'
  );
```

異なるストレージサービスで使用可能な接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

`CONNECTION_NAME` の詳細については、[CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) を参照してください。

### FILE_FORMAT {#file-format}

詳細は [入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

## アクセス制御要件 {#access-control-requirements}

| 権限 | オブジェクトタイプ | 説明 |
|:----------|:--------------|:--------------------------------------------------------------------------|
| SUPER     | グローバル、テーブル | stage（stage の一覧表示、作成、削除）、catalog、または share を操作します。 |

stage を作成するには、操作を実行するユーザーまたは [current_role](/tidb-cloud-lake/guides/roles.md) が SUPER [privilege](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

## 例 {#examples}

### 例 1: 内部 stage を作成する {#example-1-create-internal-stage}

この例では、*my_internal_stage* という名前の内部 stage を作成します。

```sql
CREATE STAGE my_internal_stage;

DESC STAGE my_internal_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│       name        │ stage_type │ storage_type │ url  │ endpoint │ has_credentials │ has_encryption_key │ storage_params │ file_format_options │  creator │         created_on         │ comment │     owner     │
├───────────────────┼────────────┼──────────────┼──────┼──────────┼─────────────────┼────────────────────┼────────────────┼─────────────────────┼──────────┼────────────────────────────┼─────────┼───────────────┤
│ my_internal_stage │ Internal   │ NULL         │ NULL │ NULL     │ false           │ false              │ NULL           │ {"compression":...} │ root@%   │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 例 2: Connection を使用して外部 stage を作成する {#example-2-create-external-stage-with-connection}

この例では、connection を使用して Amazon S3 上に *my_s3_stage* という名前の外部 stage を作成します。

```sql
-- First create a connection
CREATE CONNECTION my_s3_connection
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE my_s3_stage
  URL='s3://load/files/'
  CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

DESC STAGE my_s3_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│    name     │ stage_type │ storage_type │       url        │ endpoint │ has_credentials │ has_encryption_key │   storage_params      │ file_format_options │ creator │         created_on         │ comment │     owner     │
├─────────────┼────────────┼──────────────┼──────────────────┼──────────┼─────────────────┼────────────────────┼───────────────────────┼─────────────────────┼─────────┼────────────────────────────┼─────────┼───────────────┤
│ my_s3_stage │ External   │ s3           │ s3://load/files/ │ NULL     │ true            │ false              │ {"bucket":"load",...} │ {"compression":...} │ root@%  │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 例 3: AWS IAM User を使用して外部 stage を作成する {#example-3-create-external-stage-with-aws-iam-user}

この例では、AWS Identity and Access Management (IAM) user を使用して、Amazon S3 上に *iam_external_stage* という名前の外部 stage を作成します。

#### ステップ 1: S3 バケットのアクセスポリシーを作成する {#step-1-create-access-policy-for-s3-bucket}

以下の手順では、Amazon S3 上のバケット *lake-toronto* に対して *lake-access* という名前のアクセスポリシーを作成します。

1. AWS Management Console にログインし、**Services** > **Security, Identity, & Compliance** > **IAM** を選択します。
2. 左側のナビゲーションペインで **Account settings** を選択し、右側のページで **Security Token Service (STS)** セクションに移動します。アカウントが属する AWS リージョンのステータスが **Active** であることを確認してください。
3. 左側のナビゲーションペインで **Policies** を選択し、右側のページで **Create policy** を選択します。
4. **JSON** タブをクリックし、次のコードをエディタにコピー＆ペーストして、ポリシーを *lake_access* として保存します。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllObjectActions",
      "Effect": "Allow",
      "Action": ["s3:*Object"],
      "Resource": "arn:aws:s3:::lake-toronto/*"
    },
    {
      "Sid": "ListObjectsInBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::lake-toronto"
    }
  ]
}
```

#### ステップ 2: IAM User を作成する {#step-2-create-iam-user}

以下の手順では、*lake* という名前の IAM user を作成し、その user にアクセスポリシー *lake-access* をアタッチします。

1. 左側のナビゲーションペインで **Users** を選択し、右側のページで **Add users** を選択します。
2. user を設定します。
    - user 名を *lake* に設定します。
    - user の権限を設定する際に、**Attach policies directly** をクリックし、アクセスポリシー *lake-access* を検索して選択します。
3. user の作成後、user 名をクリックして詳細ページを開き、**Security credentials** タブを選択します。
4. **Access keys** セクションで、**Create access key** をクリックします。
5. ユースケースとして **Third-party service** を選択し、その下のチェックボックスをオンにして access key の作成を確認します。
6. 生成された access key と secret access key をコピーし、安全な場所に保存します。

#### ステップ 3: 外部 stage を作成する {#step-3-create-external-stage}

より高いセキュリティのために、IAM role を使用して外部 stage を作成します。

```sql
-- First create a connection using IAM role
CREATE CONNECTION iam_s3_connection
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-access'
  EXTERNAL_ID = 'my-external-id-123';

-- Create stage using the connection
CREATE STAGE iam_external_stage
  URL = 's3://lake-toronto'
  CONNECTION = (CONNECTION_NAME = 'iam_s3_connection');
```

### 例 4: Cloudflare R2 上に外部 stage を作成する {#example-4-create-external-stage-on-cloudflare-r2}

[Cloudflare R2](https://www.cloudflare.com/en-ca/products/r2/) は、Cloudflare が提供するオブジェクトストレージサービスであり、Amazon の AWS S3 サービスと完全な互換性があります。この例では、Cloudflare R2 上に *r2_stage* という名前の外部 stage を作成します。

#### ステップ 1: バケットを作成する {#step-1-create-bucket}

以下の手順では、Cloudflare R2 上に *lake* という名前のバケットを作成します。

1. Cloudflare ダッシュボードにログインし、左側のナビゲーションペインで **R2** を選択します。
2. **Create bucket** をクリックしてバケットを作成し、バケット名を *lake* に設定します。バケットの作成に成功すると、バケット詳細ページでバケット名のすぐ下にバケット endpoint が表示されます。

#### ステップ 2: R2 API Token を作成する {#step-2-create-r2-api-token}

以下の手順では、Access Key ID と Secret Access Key を含む R2 API token を作成します。

1. **R2** > **Overview** で **Manage R2 API Tokens** をクリックします。
2. **Create API token** をクリックして API token を作成します。
3. API token を設定する際に、必要な権限を選択し、必要に応じて **TTL** を設定します。
4. **Create API Token** をクリックして Access Key ID と Secret Access Key を取得します。これらをコピーし、安全な場所に保存します。

#### Step 3: 外部 stage を作成する {#step-3-create-external-stage}

作成した Access Key ID と Secret Access Key を使用して、*r2_stage* という名前の外部 stage を作成します。

```sql
-- First create a connection
CREATE CONNECTION r2_connection
  STORAGE_TYPE = 's3'
  REGION = 'auto'
  ENDPOINT_URL = '<your-bucket-endpoint>'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE r2_stage
  URL='s3://lake/'
  CONNECTION = (CONNECTION_NAME = 'r2_connection');
```