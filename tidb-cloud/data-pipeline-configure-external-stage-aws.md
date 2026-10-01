---
title: TiDB Cloud Data Pipeline 用の外部 stage を設定する (AWS)
summary: Amazon S3 バケットを TiDB Cloud Data Pipeline の外部 stage として設定する方法について、バケットアクセスや SQS による取り込みを含めて説明します。
---

# TiDB Cloud Data Pipeline 用の外部 stage を設定する (AWS)

このガイドでは、[TiDB Cloud Data Pipeline](/tidb-cloud/data-pipeline.md) の外部 stage として Amazon S3 バケットを準備する方法を説明します。外部 stage は、TiDB Cloud がエクスポートしたスナップショットと行変更を書き込む中間バケットであり、TiDB Cloud Lake はそこからデータを読み取って対象の Warehouse にロードします。

TiDB Cloud はデータをお使いの S3 バケットに書き込み、TiDB Cloud Lake はそこからデータを読み取ります。

## 前提条件 {#prerequisites}

- IAM、S3、および必要に応じて SQS リソースを管理する権限を持つ AWS アカウント
- TiDB Cloud Lake Warehouse を持つ TiDB Cloud アカウント
- TiDB Cloud インスタンスと同じリージョンにある S3 バケット。まだない場合は、[S3 バケットを作成する](#step-1-create-an-s3-bucket) で作成してください。

## ステップ 1. S3 バケットを作成する {#step-1-create-an-s3-bucket}

> **Tip:**
>
> すでに S3 バケットを用意している場合は、この手順をスキップし、バケットのリージョンが TiDB Cloud インスタンスのリージョンと一致していることだけ確認してください。

1. [AWS S3 Console](https://console.aws.amazon.com/s3/) を開き、新しいバケットを作成します。
2. リージョンを選択し、そのリージョンが TiDB Cloud インスタンスのリージョンと一致していることを確認します。
3. （任意）バケット内にフォルダ（プレフィックス）を作成して、TiDB Cloud データを整理します（例: `s3://tidb-cloud-lake-data/my-cluster/`）。

## ステップ 2. バケットアクセスを設定する {#step-2-configure-bucket-access}

以下のいずれかのバケットアクセス方法を選択し、対応するセクションの手順を完了してください。

* **オプション 1: ロール ARN によるバケットアクセス (CloudFormation)**（推奨）
* **オプション 2: ロール ARN によるバケットアクセス (手動設定)**
* **オプション 3: アクセスキーによるバケットアクセス (非推奨)**

> **Tip:**
>
> **開始前に、イベント駆動の取り込みを有効にするかどうかを決めてください。**
>
> デフォルトでは、TiDB Cloud Lake はデータパイプライン作成後、新しいデータがないか定期的にバケットをスキャンします。より低いデータレイテンシーが必要な場合は、SQS キューを使ったイベント駆動の取り込みを任意で有効にできます。新しいデータがバケットに書き込まれると、S3 イベント通知が SQS キューに送信され、TiDB Cloud Lake は次回の定期スキャンを待たずに新しいデータを検出してロードできます。changefeed は引き続き、設定された間隔に従ってデータをバケットにフラッシュします。イベント駆動の取り込みにより TiDB Cloud Lake がより頻繁にデータをロードする可能性があるため、TiDB Cloud Lake サービスのホスティングコストが増加する場合があります。
>
> - **オプション 1** では、イベント駆動の取り込みを有効にする場合、スタック作成時に CloudFormation スタックで SQS キューを作成することも、後から手動で SQS キューを追加することもできます。
> - **オプション 2 と 3** では、イベント駆動の取り込みを有効にする場合、SQS キューを手動で作成して設定する必要があります。

### オプション 1. ロール ARN によるバケットアクセス (CloudFormation) {#option-1-bucket-access-with-role-arn-cloudformation}

1 つの IAM ロールを TiDB Cloud（バケットへの書き込み）と TiDB Cloud Lake（バケットからの読み取り）で共有します。このロールの信頼ポリシーにより、両者はそれぞれ独自の外部 ID で保護された状態でロールを引き受けられるため、長期間有効な認証情報を保存する必要がありません。CloudFormation スタックがロール、その信頼関係、その権限、さらに必要に応じて SQS キューとそのポリシーを一括で作成するため、これが推奨される方法です。

#### 1.1 CloudFormation でロールを作成する {#11-create-the-role-with-cloudformation}

1. TiDB Cloud コンソールで **Create Data Pipeline** ページを開き、**External Stage** エリアに移動して **Bucket URI** を入力します。
2. **Bucket Access** で **AWS Role ARN** を選択し、フィールドの下にある CloudFormation リンクをクリックしてダイアログを開きます。
3. **AWS Console with CloudFormation Template** をクリックします。すべてのパラメータが事前入力された状態で、AWS CloudFormation コンソールが新しいブラウザタブで開きます。
4. 新しいタブで **stack name** を入力し、イベント駆動の取り込みが必要な場合は任意で **SQS queue name** を入力します。CloudFormation はキューとその通知ポリシーを自動的に作成します。不要な場合は SQS フィールドを空のままにしてください。
5. スタックを作成し、ステータスが `CREATE_COMPLETE` になるまで待ちます。
6. スタックの **Outputs** タブで、TiDB Cloud コンソールで External Stage を設定する際に必要な以下の値を記録します。

    - **Role ARN**: `RoleARN` の値
    - **SQS queue URL**（SQS を有効にした場合のみ）: `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>` 形式のキュー URL

#### 1.2 （任意）S3 バケット通知を設定する {#12-optional-configure-the-s3-bucket-notification}

[1.1](#11-create-the-role-with-cloudformation) で SQS を有効にした場合、キューとそのポリシーはすでにスタックによって作成されています。残る手順は、既存のバケットに対する通知設定のみです。提供されている CloudFormation スタックは、バケットがすでに存在するためこの設定は行いません。[2.3.2](#232-configure-the-s3-bucket-notification) の手動通知設定手順に従ってください。

### オプション 2. ロール ARN によるバケットアクセス (手動設定) {#option-2-bucket-access-with-role-arn-manual-setup}

CloudFormation を使用できない場合、または組織の要件によりすべての IAM リソースを手動で作成・レビューする必要がある場合は、この方法を使用します。IAM ロール自体はオプション 1 と同じで、異なるのは作成方法だけです。

#### 2.1 必要な値を収集する {#21-collect-the-required-values}

1. TiDB Cloud コンソールで **Create Data Pipeline** ページを開き、**External Stage** エリアに移動して **Bucket URI** を入力します。
2. **Bucket Access** で **AWS Role ARN** を選択し、フィールドの下にある CloudFormation リンクをクリックしてダイアログを開きます。
3. ダイアログの **Having trouble?** エリアから以下の値をコピーします。これらはすべて [2.2](#22-create-the-role-and-attach-the-policies) の信頼ポリシーで必要です。

    - TiDB Cloud account ID
    - TiDB Cloud external ID
    - Lake external ID
    - Lake platform setup & validation role ARN
    - Lake platform data loading role ARN

#### 2.2 ロールを作成し、ポリシーをアタッチする {#22-create-the-role-and-attach-the-policies}

1. [IAM Console](https://console.aws.amazon.com/iam/) を開き、**Roles > Create role** に移動します。
2. **Trusted entity type** で **Custom trust policy** を選択し、以下をポリシードキュメントに貼り付けます。プレースホルダーの値は収集した値に置き換えてください。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowTiDBCloudAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<TiDB Cloud account ID>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<TiDB Cloud external ID>" } }
        },
        {
          "Sid": "AllowLakeSetupAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform setup & validation role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        },
        {
          "Sid": "AllowLakeLoadAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform data loading role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        }
      ]
    }
    ```

3. ロール名を入力し（例: `tidb-cloud-lake-role`）、**Create role** をクリックします。
4. 作成したロールを開き、**Permissions** タブに移動して **Add permissions > Create inline policy** をクリックします。
5. **JSON** タブを選択し、以下を貼り付けます。`YOUR_BUCKET_NAME` と `your-prefix` は実際の値に置き換え、イベント駆動の取り込みが不要な場合は `SQSConsumeAccess` ステートメントを削除してください。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketMetadata",
          "Effect": "Allow",
          "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
        },
        {
          "Sid": "S3ObjectReadWrite",
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
        },
        {
          "Sid": "SQSConsumeAccess",
          "Effect": "Allow",
          "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes", "sqs:ChangeMessageVisibility"],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

6. ポリシー名を入力し（例: `tidb-cloud-lake-access`）、**Create policy** をクリックします。
7. ロール詳細ページから ロール ARN をコピーします。これは TiDB Cloud コンソールで External Stage を設定する際に必要です。例: `arn:aws:iam::123456789012:role/tidb-cloud-lake-role`

#### 2.3 （任意）SQS でイベント駆動の取り込みを有効にする {#23-optional-enable-event-driven-ingestion-with-sqs}

ワークロードで定期スキャンを許容できる場合は、このセクションをスキップしてください。SQS を使用するタイミングの詳細については、[ステップ 2. バケットアクセスを設定する](#step-2-configure-bucket-access) の Tip を参照してください。

##### 2.3.1 SQS キューを作成し、キューポリシーを設定する {#231-create-the-sqs-queue-and-configure-the-queue-policy}

1. [SQS Console](https://console.aws.amazon.com/sqs/) を開き、**Create queue** をクリックして **Standard** タイプを選択し、名前を入力します（例: `tidb-cloud-lake-sqs`）。その後、**Create queue** をクリックします。
2. キューを開き、**Access policy** タブに移動して、ポリシーを以下の内容に置き換えます。これにより、S3 がキューに通知を送信できるようになります。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

    > **Note:** `REGION`、`ACCOUNT_ID`、`YOUR_QUEUE_NAME`、`YOUR_BUCKET_NAME` は実際の値に置き換えてください。

3. [2.2](#22-create-the-role-and-attach-the-policies) の `SQSConsumeAccess` ステートメントがロールの権限ポリシーに含まれていることを確認します。
4. SQS コンソールのキュー詳細ページからキュー URL を記録します。これは TiDB Cloud コンソールで External Stage を設定する際に必要で、形式は `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>` です。

##### 2.3.2 S3 バケット通知を設定する {#232-configure-the-s3-bucket-notification}

S3 イベント通知を設定して、バケットからのオブジェクト作成イベントを SQS キューに送信します。

1. [AWS S3 Console](https://console.aws.amazon.com/s3/) を開き、対象のバケットに移動します。
2. **Properties > Event notifications > Create event notification** に移動します。
3. 以下を設定します。
    - **Event types:** **All object create events** を選択します。
    - **Destination:** **SQS queue** を選択し、先ほど作成したキューを選びます。
4. **Save changes** をクリックします。

### オプション 3. アクセスキーによるバケットアクセス (非推奨) {#option-3-bucket-access-with-access-key-not-recommended}

> **Note:**
>
> Access Key/Secret Key (AK/SK) を使用する場合、認証情報を手動で管理およびローテーションする必要があり、誤って漏洩するリスクも高くなります。管理を簡素化し、セキュリティを高めるため、[オプション 1](#option-1-bucket-access-with-role-arn-cloudformation) または [オプション 2](#option-2-bucket-access-with-role-arn-manual-setup) の手順に従って Role ARN を作成することを推奨します。

この方法では、IAM ユーザーを作成し、その **Access Key ID** と **Secret Access Key** を TiDB Cloud に提供します。TiDB Cloud はこれらの認証情報を使用して、お使いの S3 バケットに直接アクセスします。

#### 3.1 IAM ユーザーとアクセスキーを作成する {#31-create-an-iam-user-and-access-key}

1. [IAM Console](https://console.aws.amazon.com/iam/) を開き、**Users > Create user** に移動します。
2. ユーザー名（例: `tidb-cloud-lake-user`）を入力し、**Next** をクリックします。
3. **Set permissions** ページで、必要な S3 権限と、必要に応じて SQS 権限を付与するポリシーを作成またはアタッチします。`YOUR_BUCKET_NAME` と `your-prefix` は実際の値に置き換えてください。イベント駆動の取り込みが不要な場合は、`SQSConsumerAccess` ステートメントを削除してください。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketAccess",
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": [
            "arn:aws:s3:::YOUR_BUCKET_NAME",
            "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
          ]
        },
        {
          "Sid": "SQSConsumerAccess",
          "Effect": "Allow",
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes",
            "sqs:ChangeMessageVisibility"
          ],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

4. **Next** をクリックします。**Review and create** ページでユーザー設定を確認し、**Create user** をクリックします。
5. **Users** ページで、作成したユーザー名をクリックし、**Security credentials** タブに移動します。
6. **Access keys** セクションで **Create access key** をクリックします。**Access key best practices & alternatives** ページで **Other** を選択し、**Next** をクリックしてアクセスキーを作成します。
7. **Access Key ID** と **Secret Access Key** を保存します。これらは TiDB Cloud コンソールで External Stage を設定するときに必要です。

    > **Note:**
    >
    > Secret Access Key は作成時に一度だけ表示されます。必ずすぐに保存してください。

#### 3.2 （任意）SQS でイベント駆動の取り込みを有効にする {#32-optional-enable-event-driven-ingestion-with-sqs}

ワークロードで定期スキャンを許容できる場合は、このセクションをスキップしてください。

1. [SQS Console](https://console.aws.amazon.com/sqs/) を開き、**Create queue** をクリックして、**Standard** タイプを選択し、名前（例: `tidb-cloud-lake-sqs`）を入力します。**Create queue** をクリックします。
2. キューを開き、**Access policy** タブに移動して、S3 がそのキューに通知を送信できるように、ポリシーを次の内容に置き換えます。プレースホルダーの値は実際の値に置き換えてください。

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

3. バケットで通知を設定します。

    1. [AWS S3 Console](https://console.aws.amazon.com/s3/) を開き、対象のバケットに移動します。
    2. **Properties > Event notifications > Create event notification** に移動します。
    3. 次のように設定します。
        - **Event types:** **All object create events** を選択します。
        - **Destination:** **SQS queue** を選択し、先ほど作成したキューを選びます。
    4. **Save changes** をクリックします。

4. SQS コンソールのキュー詳細ページでキュー URL を記録します。これは TiDB Cloud コンソールで External Stage を設定するときに必要です。形式は `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>` です。

## 次のステップ {#what-s-next}

AWS の設定が完了すると、External Stage の設定に必要な値がすべてそろいます。

- **S3 URI**: **ステップ 1. S3 バケットを作成する** で取得します。
- **Bucket access**: Role ARN（オプション 1 と 2）、または Access Key ID と Secret Access Key（オプション 3）。
- **SQS queue URL**（任意）。

[TiDB Cloud コンソール](https://tidbcloud.com) で TiDB Cloud インスタンスの Data Pipeline 設定ページに移動し、**External Stage** 設定にこれらの値を入力して、データパイプラインのセットアップを完了してください。
