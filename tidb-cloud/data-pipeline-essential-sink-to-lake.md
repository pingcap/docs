---
title: TiDB Cloud Lake へのシンク
summary: エクスポート、changefeed、および TiDB Cloud Lake integration を使用して、TiDB Cloud Essential インスタンス上に TiDB Cloud Lake データパイプラインを構築するための手動セットアップガイドです。
---

# TiDB Cloud Lake へのシンク

このガイドでは、TiDB Cloud Essential インスタンスから TiDB Cloud Lake へのデータパイプラインをエンドツーエンドで設定する方法を説明します。Amazon S3 に完全スナップショットをエクスポートし、同じ S3 ロケーションに増分変更を継続的に書き込むための [変更フィード](/tidb-cloud/changefeed-overview.md) を作成し、スナップショットデータと増分データの両方をロード (load) するように TiDB Cloud Lake を設定します。

## 制限事項 {#restrictions}

- TiDB Cloud Lake の Warehouse は、Essential インスタンスと **同じリージョン**に存在する必要があります。
- 増分レプリケーションできるのは、**主キー**を持つテーブルのみです。
- このパイプラインでは、AWS IAM リソースと認証情報、changefeed、および TiDB Cloud Lake integration の手動セットアップと保守が必要です。
- DDL、DML、およびカラム型のサポートの詳細については、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- 特定のリージョンにデプロイされた TiDB Cloud Essential インスタンス。
- この組織の TiDB Cloud API へのアクセス権。API キーは [TiDB Cloud コンソール](https://tidbcloud.com/) の [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) ページで作成できます。このガイド内のすべての API 呼び出しで必要になるため、**Public Key** と **Private Key** は必ず保存してください。
- TiDB Cloud Essential インスタンスと同じリージョンにある Amazon S3 バケット（例: `s3://my-datapipeline-bucket`）。
- TiDB Cloud Essential インスタンスと同じリージョンにある TiDB Cloud Lake Warehouse。

> **Note:**
>
> このガイドでは、レプリケートしたいデータがすでにソース TiDB データベース内に存在していることを前提としています。サンプルデータが必要な場合は、先に準備してから続行してください。

## ステップ 1. S3 バケットへのアクセスを準備する {#step-1-prepare-s3-bucket-access}

データパイプラインのコンポーネント（エクスポート、changefeed、TiDB Cloud Lake）はすべて、同じ S3 バケットへのアクセスを必要とします。S3 バケットにアクセスするには、次のいずれかの方法を選択してください。

- **Role ARN**（AWS でホストされている TiDB Cloud Essential インスタンス向け）: 3 つのコンポーネントすべてで共有する単一の IAM ロールです。この方法では長期間有効な認証情報を使わずに済み、セキュリティも高まります。
- **Access Key**: セットアップがより簡単で、Role ARN を利用できない場合に必要です。ただし、認証情報の手動管理とローテーションが必要になります。

### 方法 1: Role ARN を使用する {#method-1-use-a-role-arn}

この方法では、まず TiDB Cloud console の Export 機能が提供する CloudFormation スタックを使用して、Export 用に設定された IAM ロールを作成します。次に、その同じロールの信頼ポリシーと権限を拡張し、changefeed と TiDB Cloud Lake もそのロールを使用して S3 バケットにアクセスできるようにします。

#### 1. Export CloudFormation でロールを作成する {#1-create-the-role-with-export-cloudformation}

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で、TiDB Cloud Essential インスタンスの概要ページに移動します。
2. 左側のナビゲーションペインで **Data > Import** をクリックし、右上の **Export Data to** をクリックします。
3. **Amazon S3** を選択します。**Role ARN** 認証で S3 の宛先を設定すると、TiDB Cloud から CloudFormation リンクが提供されます。これを使用して IAM ロールを作成します。

スタックの作成後、スタックの **Outputs** から **Role ARN**（例: `arn:aws:iam::<account-id>:role/<role-name>`）を記録してください。

#### 2. 信頼関係を統合する {#2-consolidate-trust-relationships}

前の手順で作成した IAM ロールは、最初は TiDB Cloud Essential から S3 へデータをエクスポートするために設定されています。同じロールは changefeed と TiDB Cloud Lake による S3 バケットアクセスにも使用されるため、これらのコンポーネントもロールを引き受けられるように信頼ポリシーを更新します。

追加の信頼関係に必要な以下の値を収集し、その後ロールの信頼ポリシーを更新します。AWS Console で [1. Export CloudFormation でロールを作成する](#1-create-the-role-with-export-cloudformation) で作成したロールに移動し、**Trust relationships** タブを開いて **Edit trust policy** をクリックします。

- **Export**: 信頼ポリシーを置き換える前に、既存の Export 用の AWS アカウント ID と外部 ID を記録し、この信頼関係を統合ポリシー内に保持できるようにします。
- **Changefeed**: 必要な値を取得するために TiDB Cloud API を呼び出します。

    ```shell
    curl -L -X GET 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds:getCloudStorageAuthConfig' \
      -u '<Public Key>:<Private Key>' --digest
    ```

    レスポンスから `tidbCloudAccountId` と `tidbCloudAccountExternalId` を記録します。

- **TiDB Cloud Lake**: [TiDB Cloud Lake console](https://lake.tidbcloud.com/) で **Data > Data Sources > Create** に移動します。**Basic Info** セクションで **Service: TiDB** を選択し、**Trust Cloud Platform roles** の下に表示される以下の値を記録します。
    - Lake Setup & Validation Role ARN
    - Lake Data Loading Role ARN
    - Lake External ID

以下の統合ポリシーでロールの信頼ポリシーを **置き換えて**ください。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExportAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Export_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Export_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowChangefeedAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Changefeed_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Changefeed_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeSetupAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Setup_and_Validation_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeLoadAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Data_Loading_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    }
  ]
}
```

#### 3. パイプライン全体のプレフィックスを対象とするように権限を拡張する {#3-expand-permissions-to-cover-the-full-pipeline-prefix}

CloudFormation で作成された権限ポリシーは、スナップショットのエクスポート先パスのみを対象としています。changefeed は `{prefix}/incremental/` に書き込み、TiDB Cloud Lake は `{prefix}/snapshot/` と `{prefix}/incremental/` の両方から読み取るため、ポリシーの対象に親プレフィックスを含める必要があります。

AWS Console でステップ 1 で作成したロールに移動し、**Permissions** タブでポリシー名をクリックして、リソーススコープを置き換えるようにポリシーを編集します。

以下の内容でロールのインライン権限ポリシーを **置き換えて**ください。

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

> **Note:**
>
> CloudFormation で作成されたポリシーでは、`arn:aws:s3:::bucket/prefix/snapshot/*` のような、より限定的なリソースが使用されます。changefeed（`prefix/incremental/` に書き込む）と TiDB Cloud Lake（両方のサブパスから読み取る）の両方が十分なアクセス権を持てるように、これを `arn:aws:s3:::bucket/prefix/*` に変更する必要があります。

### 方法 2: Access Key を使用する {#method-2-use-an-access-key}

> **Note:**
>
> Access Key と Secret Key (AK/SK) を使用する場合、認証情報の管理とローテーションを手動で行う必要があり、セキュリティリスクが高まります。より強固なセキュリティのため、代わりに **Role ARN** を使用してください。

Access Key 認証を使用する場合は、以下の権限を持つ IAM ユーザーを作成し、Export、changefeed、TiDB Cloud Lake の設定時にその認証情報を指定してください。

**権限ポリシー:**

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

後続の手順で使用するため、**Access Key ID** と **Secret Access Key** を記録しておいてください。

## ステップ 2. Amazon S3 に完全スナップショットをエクスポートする {#step-2-export-full-snapshot-to-amazon-s3}

TiDB Cloud コンソールで **Data > Import** に移動し、右上の **Export Data to** をクリックして **Amazon S3** を選択し、新しいエクスポートタスクを作成します。

**設定:**

- **Selected Data**: エクスポートするデータベースとテーブルを選択します。
- **Data Format**: `CSV`
    - **Edit CSV Configuration** をクリックし、以下を設定します。
        - **Dialect**: `Snowflake`
        - **Escape backslash**: `false`
- **Compression**: `None`
- **Amazon S3 Settings**:
    - **Bucket URI**: `s3://<bucket>/<prefix>/snapshot/`（推奨される snapshot サブパスを使用）
    - **Role ARN** または **Access Key**: [ステップ 1. S3 バケットへのアクセスを準備する](#step-1-prepare-s3-bucket-access) の認証情報を使用します。

エクスポートタスクの完了後、タスク詳細を開いて **Snapshot TSO** の値を記録してください。この TSO は changefeed の作成時に必要です。

## ステップ 3. 増分データ用の changefeed を作成する {#step-3-create-a-changefeed-for-incremental-data}

現在、TiDB Cloud Essential では TiDB Cloud コンソールからクラウドストレージシンクを作成できないため、TiDB Cloud API を使用する必要があります。

以下の必須フィールドを指定して changefeed 作成 API を呼び出します。

| フィールド | 必須の値 |
|-------|---------------|
| `sink.cloudStorage.dataFormat.protocol` | `CANAL_JSON` |
| `sink.cloudStorage.dataFormat.canalJsonConfig.enableTidbExtension` | `true` |
| `sink.cloudStorage.dataFormat.contentCompatible` | `true` |
| `startPosition.mode` | `FROM_TSO` |
| `startPosition.tso` | `<snapshot_tso from the export step>` |

**リクエスト例:**

```shell
curl -L -X POST 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds' \
  -H 'Content-Type: application/json' \
  -u '<Public Key>:<Private Key>' --digest \
  -d '{
    "displayName": "<changefeed-name>",
    "sink": {
      "type": "CLOUD_STORAGE",
      "cloudStorage": {
        "storage": {
          "type": "S3",
          "s3": {
            "uri": "s3://<bucket>/<prefix>/incremental/",
            "authType": "ROLE_ARN",
            "roleArn": "<role-arn>"
          }
        },
        "dataFormat": {
          "protocol": "CANAL_JSON",
          "contentCompatible": true,
          "canalJsonConfig": {
            "enableTidbExtension": true
          }
        }
      }
    },
    "filter": {
      "mode": "IGNORE_NOT_SUPPORT_TABLE",
      "filterRule": ["*.*"]
    },
    "startPosition": {
      "mode": "FROM_TSO",
      "tso": "<snapshot_tso>"
    },
    "rcu": 2
  }'
```

> **Note:**
>
> changefeed の URI では、エクスポートスナップショットと同じプレフィックス配下の `incremental/` サブパスを使用する必要があります。IAM ロールの権限（[3. パイプライン全体のプレフィックスを対象とするように権限を拡張する](#3-expand-permissions-to-cover-the-full-pipeline-prefix) を参照）は、このパスを対象に含めている必要があります。
>
> **Access Key** を Role ARN の代わりに使用する場合は、リクエストボディ内の `s3` ブロックを次の内容に置き換えてください。
>
> ```json
> "s3": {
>   "uri": "s3://<bucket>/<prefix>/incremental/",
>   "authType": "ACCESS_KEY",
>   "accessKey": {
>     "id": "<access-key-id>",
>     "secret": "<access-key-secret>"
>   }
> }
> ```
>

## ステップ 4. TiDB Cloud Lake を設定する {#step-4-configure-tidb-cloud-lake}

TiDB Cloud Lake では、S3 バケットからデータをロード (load) するために、データソースと integration を作成する必要があります。

### 1. データソースを作成する {#1-create-a-data-source}

1. [TiDB Cloud Lake console](https://lake.tidbcloud.com/) で **Data > Data Sources > Create** に移動します。
2. **Service: TiDB** を選択します。
3. **Role ARN** または **Access Key** 認証を選択し、以下を入力します。
    - **Role ARN**: [1. Export CloudFormation でロールを作成する](#1-create-the-role-with-export-cloudformation) の ARN、または [方法 2: Access Key を使用する](#method-2-use-an-access-key) の **Access Key ID** / **Secret Access Key**。
    - **S3 Bucket Name**: バケット名のみ（例: `my-datapipeline-bucket`。完全な URI ではありません）。
    - **S3 Region**: Essential インスタンスと同じリージョン。
4. **SQS Queue URL** は任意です。イベント駆動の取り込みを有効にする場合は、先に SQS キューをセットアップし、S3 バケット通知を設定してください。詳細は [TiDB Cloud Lake 用の Amazon SQS および S3 IAM Role](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/) を参照してください。
5. **Trust Cloud Platform roles** で、TiDB Cloud Lake のプラットフォームロールと外部 ID が、[2. 信頼関係を統合する](#2-consolidate-trust-relationships) の統合済み信頼ポリシーに追加した値と一致していることを確認します。

### 2. integration を作成する {#2-create-an-integration}

1. [TiDB Cloud Lake console](https://lake.tidbcloud.com/) で **Data > Integration > Create** に移動します。
2. 以下のフィールドを入力します。
    - **Data Source**: 上で作成したデータソースを選択します。
    - **Name**: この integration タスクの名前。
    - **Sync Mode**: `Snapshot + CDC` を選択して、最初に完全スナップショットをロードし、その後増分変更を継続的に適用します。
    - **Table Rules**: エクスポートしたすべてのテーブルを同期するには `*.*` を指定します。
    - **Changefeed S3 Prefix**: `<prefix>/incremental/`。
    - **Dumpling S3 Prefix**: `<prefix>/snapshot/`。
    - **Poll Interval**: TiDB Cloud Lake が外部 stage をスキャンして新しいデータを検出する間隔です。デフォルト値は 60 秒です。間隔を短くするとデータレイテンシーは減少しますが、TiDB Cloud Lake のホスティングコストは増加します。
    - **Merge Interval**: TiDB Cloud Lake が増分データを Warehouse にマージする間隔です。デフォルト値は 30 秒です。間隔を短くするとデータレイテンシーは減少しますが、TiDB Cloud Lake のホスティングコストは増加します。
    - **Warehouse**: 対象の Warehouse を選択します。
3. **Create** をクリックします。
4. 作成後、integration はデフォルトで **Stopped** です。integration のアクションボタンをクリックし、**Start** を選択してデータロードを開始します。

## See also {#see-also}

- DDL、DML、およびカラム型のサポートの詳細については、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。
