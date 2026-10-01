---
title: TiDB Cloud Lake へのシンク
summary: Dumpling と changefeed を使用して、TiDB Cloud Dedicated クラスター上に TiDB Cloud Lake データパイプラインを構築するための手動セットアップガイドです。
---

# TiDB Cloud Lake へのシンク

このガイドでは、TiDB Cloud Dedicated クラスターから TiDB Cloud Lake へのデータパイプラインをエンドツーエンドで設定する手順を説明します。[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) を使用して完全スナップショットを Amazon S3 にエクスポートし、[変更フィード](/tidb-cloud/changefeed-overview.md) を作成して増分変更を同じ S3 ロケーションに継続的に書き込み、TiDB Cloud Lake を設定してスナップショットと増分データの両方をロードします。

## 制限事項 {#restrictions}

- TiDB Cloud Lake の Warehouse は、{{{ .dedicated }}} クラスターと**同じリージョン**に存在する必要があります。
- 増分レプリケーションできるのは、**主キー**を持つテーブルのみです。
- クラウドストレージ changefeed を作成するには、{{{ .dedicated }}} クラスターが v7.1.1 以降で動作している必要があります。詳細は、[クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md) を参照してください。
- このパイプラインでは、AWS IAM リソースと認証情報、changefeed、TiDB Cloud Lake 統合の手動セットアップと保守が必要です。
- DDL、DML、およびカラム型のサポートの詳細は、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- {{{ .dedicated }}} クラスター。デプロイされているリージョンを確認しておいてください。
- Dumpling を実行するマシンからクラスターへのネットワーク接続。パブリック接続、VPC ピアリング、またはプライベートエンドポイントを使用できます。このガイドでは例としてパブリック接続を使用します。
- ソーステーブルを読み取れる SQL ユーザー。このガイドでは例として `root` を使用します。必要な権限については、[必要な権限](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges) を参照してください。
- {{{ .dedicated }}} クラスターと同じリージョンにある Amazon S3 バケット（例: `s3://my-datapipeline-bucket`）。
- {{{ .dedicated }}} クラスターと同じリージョンにある TiDB Cloud Lake の Warehouse。

> **Note:**
>
> このガイドでは、レプリケートしたいデータがすでにソース TiDB データベースに存在していることを前提としています。サンプルデータが必要な場合は、先に準備してから続行してください。

## ステップ 1. S3 バケットへのアクセスを準備する {#step-1-prepare-s3-bucket-access}

データパイプラインの各コンポーネント（Dumpling、changefeed、TiDB Cloud Lake）は、すべて同じ S3 バケットへのアクセスが必要です。対象の S3 バケットに必要な権限を持つ IAM ユーザーを作成し、そのユーザーのアクセスキーを作成して、3 つのコンポーネントすべてで同じアクセスキーを使用します。

1. [IAM Console](https://console.aws.amazon.com/iam/) を開き、IAM ユーザー（例: `tidb-cloud-datapipeline-user`）を作成します。
2. 次の権限ポリシーをユーザーにアタッチします。`<your-bucket-name>` と `<your-prefix>` は実際の値に置き換えてください。

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

3. ユーザーのアクセスキーを作成し、**Access Key ID** と **Secret Access Key** を記録します。これらは、スナップショットのエクスポート、changefeed の作成、TiDB Cloud Lake の設定時に必要です。

> **Note:**
>
> このガイドでは、S3 バケットへのアクセスにアクセスキーを使用します。changefeed は Role ARN もサポートしています。詳細は、[クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md#step-1-configure-destination) を参照してください。

## ステップ 2. Dumpling で完全スナップショットをエクスポートする {#step-2-export-a-full-snapshot-with-dumpling}

TiDB Cloud Dedicated では TiDB Cloud コンソールでエクスポート機能が提供されていないため、[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) を使用して完全スナップショットをエクスポートします。

### 1. ネットワークと SQL ユーザーを準備する {#1-prepare-the-network-and-sql-user}

1. {{{ .dedicated }}} クラスターに、Dumpling を実行するマシンから到達できることを確認します。このガイドではパブリック接続を使用します。パブリック接続を使用する場合は、そのマシンの IP アドレスをクラスターの IP アクセスリストに追加してください。詳細は、[パブリック接続経由でTiDB Cloud Dedicatedに接続します](/tidb-cloud/connect-via-standard-connection.md) および [IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md) を参照してください。
2. [TiDB Cloud コンソール](https://tidbcloud.com/) で、クラスターの概要ページにある **Connect** をクリックし、接続先のホストとポートを記録します。これらは Dumpling コマンドで必要です。
3. Dumpling に必要な権限を持つ SQL ユーザーを準備します。このガイドでは例として `root` を使用します。専用ユーザーを使用する場合は、そのユーザーに [Dumpling に必要な権限](https://docs.pingcap.com/tidb/stable/dumpling-overview#required-privileges) を付与してください。

### 2. Dumpling でスナップショットをエクスポートする {#2-export-the-snapshot-with-dumpling}

{{{ .dedicated }}} クラスターに接続できるマシンで Dumpling を実行します。AWS アクセスキーは、`access-key` および `secret-access-key` パラメータを使って `-o` URI に渡します。

```shell
tiup dumpling \
  -h "<host>" \
  -P <port> \
  -u "<username>" \
  -p "<password>" \
  --filetype csv \
  --csv-output-dialect snowflake \
  --escape-backslash=false \
  -o "s3://<bucket>/<prefix>/snapshot/?access-key=<access-key-id>&secret-access-key=<secret-access-key>" \
  --s3.region "<region>"
```

パラメータの説明:

- `--filetype csv` と `--csv-output-dialect snowflake`: データを **Snowflake** 方言の CSV 形式でエクスポートします。
- `--escape-backslash=false`: バックスラッシュのエスケープを無効にします。
- 圧縮はデフォルトで無効です。
- `-o` と `--s3.region`: エクスポートしたファイルを S3 バケットに書き込みます。`-o` URI 内の `access-key` および `secret-access-key` パラメータは、バケット用の認証情報を提供します。

> **Note:**
>
> Secret Access Key に `+`、`/`、`=` などの URI 特殊文字が含まれている場合は、先に URL エンコードしてください。あるいは、`AWS_ACCESS_KEY_ID` と `AWS_SECRET_ACCESS_KEY` 環境変数を設定するか、`~/.aws/credentials` ファイルを使用し、`-o` URI から `access-key` と `secret-access-key` パラメータを省略することもできます。

エクスポートが正常に完了すると、コマンド出力に JSON サマリーが含まれます。出力内の `SessionParams.tidb_snapshot` フィールドを見つけ、その値を記録してください。この値は **snapshot TSO** です。エクスポートしたスナップショットの続きから増分レプリケーションを開始するため、changefeed の作成時に必要になります。

## ステップ 3. 増分データ用の changefeed を作成する {#step-3-create-a-changefeed-for-incremental-data}

TiDB Cloud コンソールでは、TiDB Cloud Dedicated クラスター用のクラウドストレージ changefeed を作成できます。完全な手順については、[クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md) を参照してください。changefeed を設定する際は、次の設定に注意してください。

- **S3 URI**: スナップショットと同じプレフィックス配下の `incremental/` サブパスを使用します。たとえば `s3://<bucket>/<prefix>/incremental/` です。
- **Bucket Access**: **AWS Access Key** を選択し、[ステップ 1. S3 バケットへのアクセスを準備する](#step-1-prepare-s3-bucket-access) のアクセスキーを入力します。権限の対象に `incremental/` パスが含まれていることを確認してください。
- **Start Replication Position**: **Start replication from a specific TSO** を選択し、[ステップ 2. Dumpling で完全スナップショットをエクスポートする](#step-2-export-a-full-snapshot-with-dumpling) で記録した snapshot TSO を入力します。
- **Data Format**: **Canal-JSON** を選択し、**Enable TiDB Extension** と **Enable Canal Content Compatibility** の両方を有効にします。これらの設定により、TiDB Cloud Lake 統合と互換性のある形式でデータが生成されます。

## ステップ 4. TiDB Cloud Lake を設定する {#step-4-configure-tidb-cloud-lake}

TiDB Cloud Lake では、S3 バケットからデータをロードするために、データソースと統合を作成する必要があります。

### 1. データソースを作成する {#1-create-a-data-source}

1. [TiDB Cloud Lake console](https://lake.tidbcloud.com/) で、**Data > Data Sources > Create** に移動します。
2. **Service: TiDB** を選択します。
3. アクセスキー認証を選択し、以下を入力します。
    - **Access Key ID** と **Secret Access Key**: [ステップ 1. S3 バケットへのアクセスを準備する](#step-1-prepare-s3-bucket-access) の認証情報。
    - **S3 Bucket Name**: バケット名のみ（例: `my-datapipeline-bucket`。完全な URI ではありません）。
    - **S3 Region**: {{{ .dedicated }}} クラスターと同じリージョン。
4. **SQS Queue URL** は任意です。イベント駆動の取り込みを有効にしたい場合は、SQS キューをセットアップし、S3 バケット通知を設定し、IAM ユーザーに必要な SQS 権限を付与してください。詳細は、[TiDB Cloud Lake 用の Amazon SQS および S3 IAM Role](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/) を参照してください。

### 2. 統合を作成する {#2-create-an-integration}

1. [TiDB Cloud Lake console](https://lake.tidbcloud.com/) で、**Data > Integration > Create** に移動します。
2. 次のフィールドを入力します。
    - **Data Source**: 上で作成したデータソースを選択します。
    - **Name**: この統合タスクの名前。
    - **Sync Mode**: `Snapshot + CDC` を選択して、最初に完全スナップショットをロードし、その後に増分変更を継続的に適用します。
    - **Table Rules**: エクスポートしたすべてのテーブルを同期するには `*.*` を指定します。
    - **Changefeed S3 Prefix**: `<prefix>/incremental/`。
    - **Dumpling S3 Prefix**: `<prefix>/snapshot/`。
    - **Poll Interval**: TiDB Cloud Lake が外部 stage をスキャンして新しいデータを検出する間隔です。デフォルト値は 60 秒です。間隔を短くするとデータレイテンシーは減少しますが、TiDB Cloud Lake のホスティングコストは増加します。
    - **Merge Interval**: TiDB Cloud Lake が増分データを Warehouse にマージする間隔です。デフォルト値は 30 秒です。間隔を短くするとデータレイテンシーは減少しますが、TiDB Cloud Lake のホスティングコストは増加します。
    - **Warehouse**: 対象の Warehouse を選択します。
3. **Create** をクリックします。
4. 作成後、統合はデフォルトで **Stopped** です。統合のアクションボタン > **Start** をクリックして、データロードを開始します。

## 関連情報 {#see-also}

- DDL、DML、およびカラム型のサポートの詳細は、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。
