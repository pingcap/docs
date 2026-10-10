---
title: TiDB データソース (Preview)
summary: TiDB Cloud Lake で TiDB データソースを設定するためのガイド。ストレージおよび認証の設定を含みます。
---

# TiDB データソース (Preview)

**TiDB** データソースには、TiDB クラスターによって stage 済みのデータを TiDB Cloud Lake が読み取るために使用する、オブジェクトストレージの場所、認証情報、およびオプションのイベントキューが保存されます。これは TiDB サーバー自体には接続しません。Dumpling と TiCDC はエクスポートおよび変更イベントをオブジェクトストレージのバケットに書き込み、TiDB Cloud Lake はそのバケットから読み取ります。

## ユースケース {#use-cases}

- 複数の TiDB 同期タスク向けに、stage 用バケット、認証情報、およびオプションの SQS キューを一元管理する
- すべてのタスクで同じバケットと認可設定を毎回入力し直す手間を避ける
- 静的キーの代わりに IAM Role を使用して、TiDB Cloud Lake が有効期限の短い認証情報を取得できるようにする
- 複数のタスクから参照されているバケット、ロール、またはキューを 1 か所で更新する

## 統合のために TiDB を準備する {#prepare-tidb-for-integration}

TiDB Cloud は、完全スナップショット (Dumpling) と増分変更 (TiCDC) をオブジェクトストレージのバケットにエクスポートします。TiDB Cloud の各プランには違いがあるため、設定を最小限に抑えつつデータ互換性を確保できるよう、プランごとに特定のセットアップ手順を推奨します。

- **Premium** または **BYOC**: [TiDB Cloud コンソールの **Data Pipeline**](https://docs.pingcap.com/tidbcloud/data-pipeline-sink-to-lake/?plan=premium) UI を使用して、エクスポートとインポートを 1 か所で設定および管理します。
- **Essential**: コンソールの **Export** および **Changefeed** 機能を使用して、[TiDB Cloud Lake へのデータパイプラインを手動で設定](https://docs.pingcap.com/tidbcloud/data-pipeline-essential-sink-to-lake/?plan=essential)します。
- **Dedicated**: [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) とコンソールの **Changefeed** 機能を使用して、[TiDB Cloud Lake へのデータパイプラインを手動で設定](https://docs.pingcap.com/tidbcloud/data-pipeline-dedicated-sink-to-lake/)します。

## TiDB データソースを作成する {#create-tidb-data-source}

1. **Data** > **Data Sources** に移動し、**Create** をクリックします。
2. サービスとして **TiDB** を選択し、データソースの **Name** を入力します。
3. **Storage Provider** と **Authentication Method** を選択し、接続の詳細を入力します。表示されるフィールドは、選択した組み合わせによって異なります。詳細は以下の [Amazon S3](#amazon-s3) または [Alibaba Cloud OSS](#alibaba-cloud-oss) を参照してください。

    > **Note:**
    >
    > 可能であれば、TiDB Cloud Lake のデプロイと同じストレージプロバイダーおよびリージョンを使用してください。

4. **Test Connectivity** をクリックして、バケットと認証情報を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## Amazon S3 {#amazon-s3}

ストレージプロバイダーが **Amazon S3** の場合は、以下のいずれかの認証方式を選択します。

### 認証方式: Role ARN (推奨) {#authentication-method-role-arn-recommended}

Role ARN は AssumeRole モデルを使用します。TiDB Cloud Lake は AWS アカウント内の IAM Role を引き受けて一時的な認証情報を取得するため、静的キーを TiDB Cloud Lake に渡す必要がありません。

データソースを保存する前に、IAM Role の信頼ポリシーで 2 つのプラットフォームロール (TiDB Cloud Lake のセットアップおよび検証ロール、ならびに TiDB Cloud Lake のデータロード用ロール) を信頼し、`sts:ExternalId` 条件に対応する External ID を指定する必要があります。完全な信頼ポリシー設定については、[AWS IAM Role による認証](https://docs.pingcap.com/tidbcloudlake/authenticate-with-aws-iam-role/) を参照してください。

| フィールド | 必須 | 説明 |
| ------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**                  | はい      | このデータソースを識別するための説明的な名前                                                                                                      |
| **Storage Provider**      | はい      | **Amazon S3** を選択                                                                                                                         |
| **Authentication Method** | はい      | **Role ARN** を選択                                                                                                                          |
| **Role ARN**              | はい      | TiDB Cloud Lake が引き受けを許可されている AWS アカウント内の IAM Role ARN。例: `arn:aws:iam::123456789012:role/tidbcloud-lake-tidb` |
| **S3 Bucket Name**        | はい      | TiCDC / Dumpling が TiDB Cloud Lake によってロードされるデータを stage するバケット                                                                     |
| **S3 Region**             | はい      | バケットの AWS リージョン。例: `us-east-1`                                                                                            |
| **S3 Endpoint**           | いいえ       | MinIO などの S3 互換ストレージでのみ使用します。例: `http://localhost:9000`。Amazon S3 の場合は空のままにします                                 |
| **SQS Queue URL**         | いいえ       | イベント駆動モード用のオプションの SQS 標準キュー URL。[オプションの SQS キュー](#optional-sqs-queue) を参照してください                                         |

### 認証方式: Access Key / Secret Key {#authentication-method-access-key-secret-key}

この方式は、たとえばロール引き受けをサポートしない S3 互換ストアなど、静的認証情報を使用したい場合に利用します。

詳細は、[Amazon S3 - Credentials](https://docs.pingcap.com/tidbcloudlake/aws-credentials/) を参照してください。

| フィールド | 必須 | 説明 |
|-------|----------|-------------|
| **Name** | はい | このデータソースを識別するための説明的な名前 |
| **Storage Provider** | はい | **Amazon S3** を選択 |
| **Authentication Method** | はい | **Access Key / Secret Key** を選択 |
| **S3 Access Key** | はい | stage 用バケットにアクセスできるアクセスキー ID |
| **S3 Secret Key** | はい | アクセスキー ID に対応するシークレットアクセスキー |
| **S3 Bucket Name** | はい | TiCDC / Dumpling が TiDB Cloud Lake がロードするデータを stage するバケット |
| **S3 Region** | はい | バケットの AWS リージョン |
| **S3 Endpoint** | いいえ | S3 互換ストレージでのみ使用します。Amazon S3 の場合は空のままにします |
| **SQS Queue URL** | いいえ | イベント駆動モード用のオプションの SQS 標準キュー URL |

## Alibaba Cloud OSS {#alibaba-cloud-oss}

ストレージプロバイダーが **Alibaba Cloud OSS** の場合、TiDB Cloud Lake は Alibaba Cloud から stage 用バケットを読み取ります。OSS では **Access Key / Secret Key** 認証のみサポートされます。

| フィールド | 必須 | 説明 |
|-------|----------|-------------|
| **Name** | はい | このデータソースを識別するための説明的な名前 |
| **Storage Provider** | はい | **Alibaba Cloud OSS** を選択 |
| **OSS Access Key ID** | はい | OSS AccessKey ID |
| **OSS AccessKey Secret** | はい | OSS AccessKey secret |
| **OSS Bucket** | はい | TiCDC / Dumpling がデータを stage する OSS バケット |
| **OSS Region** | 読み取り専用 | Lake のデプロイリージョンです。自動的に表示され、変更できません |

## オプションの SQS キュー {#optional-sqs-queue}

**SQS Queue URL** フィールドはオプションであり、Amazon S3 にのみ適用されます。stage 用バケットに対する S3 `ObjectCreated` イベントを受信する標準 SQS キューを指定すると、TiDB Cloud Lake は次回のポーリングを待つ代わりに、そのキューから新しく書き込まれた changefeed / export オブジェクトを検出できます。

- キューは **standard** キューである必要があります。FIFO キューはサポートされません。S3 のイベント通知をそれらに配信できないためです。
- S3 バケットと SQS キューは同じリージョンに配置することを推奨します。
- バケットのポーリングは引き続き正式な検出経路であり、SQS は置き換えではなくレイテンシー最適化です。
- このフィールドを空のままにすると、タスクはポーリングによってオブジェクトを検出します。

キュー、バケット通知、および信頼ポリシーの設定については、[Amazon SQS (S3) - IAM Role](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md) を参照してください。

## 次のステップ {#next-steps}

このデータソースを作成した後、それを使用して [TiDB Integration Task](/tidb-cloud-lake/guides/integrate-with-tidb.md) を作成できます。