---
title: Amazon SQS (S3) - IAM Role (Preview)
summary: {{{ .lake }}} で "Amazon SQS (S3) - IAM Role" データソースを作成する方法を説明します。
---

# Amazon SQS (S3) - IAM Role (Preview)

このページでは、`Amazon SQS (S3) - IAM Role` データソースを作成する方法について説明します。このデータソースには、Amazon SQS キューおよび対応する S3 バケットにアクセスするために必要な設定が保存され、Amazon S3 から SQS に配信される S3 オブジェクト作成イベントを消費するために使用されます。

`Amazon SQS (S3) - IAM Role` は、SQS (S3) 取り込みに必要な接続情報と認可情報のみを保存します。メッセージ自体を消費することはありません。SQS メッセージの読み取り、S3 ObjectCreated イベントの解析、およびデータの {{{ .lake }}} への書き込みという実際の処理は、[Amazon SQS (S3) Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) によって実行されます。

## ユースケース {#use-cases}

- SQS (S3) 取り込みに必要な queue URL、リージョン、IAM Role、パススコープを一元管理する
- S3 `ObjectCreated` イベントを消費し、対応するオブジェクトデータを {{{ .lake }}} に書き込む
- S3 パスのポーリングのみに依存せず、S3 イベント通知を使用してデータ取り込みを駆動する
- 複数のタスクから参照されている場合に、IAM Role、queue URL、またはパススコープを 1 か所で更新する

## Amazon SQS (S3) - IAM Role を作成する {#create-amazon-sqs-s3-iam-role}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **Amazon SQS (S3) - IAM Role** を選択し、接続の詳細を入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | Yes | データソースを識別するための説明的な名前 |
    | **Queue URL** | Yes | SQS 標準キューの URL。例: `https://sqs.us-east-1.amazonaws.com/123456789012/my-queue` |
    | **Queue Region** | Yes | SQS キューが配置されている AWS リージョン。例: `us-east-1`。S3 バケットは SQS キューと同じリージョンに存在する必要があります |
    | **Role ARN** | Yes | {{{ .lake }}} が引き受けることを許可された、AWS アカウント内の IAM Role ARN |
    | **External ID** | Yes | {{{ .lake }}} コンソールの Organization ID。IAM Role の信頼ポリシーで使用されます |
    | **Bucket** | Yes | ObjectCreated イベントを送信する S3 バケットの名前 |
    | **Object Key Prefix** | No | S3 オブジェクトキーのプレフィックスフィルター。S3 通知フィルターと一致している必要があります |
    | **Object Key Suffix** | No | S3 オブジェクトキーのサフィックスフィルター。S3 通知フィルターと一致している必要があります |

3. **Test Connectivity** をクリックして接続を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

    > **Note:**
    >
    > SQS (S3) 取り込みでは AssumeRole モデルを使用します。AWS Access Key や Secret Key を {{{ .lake }}} に提供する必要はありません。代わりに、AWS アカウント内に IAM Role を作成し、ロールの信頼ポリシーで `sts:AssumeRole` を通じて {{{ .lake }}} プラットフォームロールが一時的な認証情報を取得できるようにしてください。

## AWS 側の設定概要 {#aws-side-configuration-overview}

データソースを作成する前に、AWS アカウントで以下の設定を完了してください。

1. SQS 標準キューを作成するか、既存のものを準備します。
2. 指定した S3 バケットがキューにメッセージを送信できるように、SQS キューポリシーを設定します。
3. `ObjectCreated` イベントを SQS キューに送信するように、S3 バケット通知を設定します。
4. `sts:AssumeRole` を通じて {{{ .lake }}} プラットフォームロールがアクセスできる IAM Role を作成します。
5. IAM Role に S3 読み取り権限と SQS 消費権限を付与します。
6. テスト用オブジェクトをアップロードし、S3 がイベントを SQS に配信できることを確認します。

まず、以下の変数を準備してください。`AWS_REGION` は、S3 バケットと SQS キューの両方が配置されているリージョンである必要があります。`EXTERNAL_ID` は {{{ .lake }}} プラットフォームコンソールの Organization ID です。

```bash
export AWS_REGION="<bucket-and-sqs-region>"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

export BUCKET_NAME="<your-bucket-name>"
export BUCKET_ARN="arn:aws:s3:::$BUCKET_NAME"

export QUEUE_NAME="<your-sqs-standard-queue-name>"
export ROLE_NAME="platform-s3-sqs-consumer-role"

export PREFIX="<object-key-prefix>"
export SUFFIX="<object-key-suffix>"

export PLATFORM_SETUP_ROLE_ARN="<platform-setup-role-arn>"
export PLATFORM_LOAD_ROLE_ARN="<platform-load-role-arn>"
export EXTERNAL_ID="<platform-org-id>"
```

> **Tip:**
>
> Platform から提供されたロール ARN を使用してください。`PLATFORM_SETUP_ROLE_ARN` は **Platform setup and validation role** の ARN、`PLATFORM_LOAD_ROLE_ARN` は **Platform data loading role** の ARN です。ほとんどの場合、IAM Role の信頼ポリシーでは両方のプラットフォームロールを信頼する必要があります。

## Step 1: SQS 標準キューを作成または取得する {#step-1-create-or-get-an-sqs-standard-queue}

SQS 標準キューを作成します。

```bash
aws sqs create-queue \
  --region "$AWS_REGION" \
  --queue-name "$QUEUE_NAME"
```

後続の手順で必要になる queue URL と queue ARN を取得します。

```bash
export QUEUE_URL=$(
  aws sqs get-queue-url \
    --region "$AWS_REGION" \
    --queue-name "$QUEUE_NAME" \
    --query 'QueueUrl' \
    --output text
)

export QUEUE_ARN=$(
  aws sqs get-queue-attributes \
    --region "$AWS_REGION" \
    --queue-url "$QUEUE_URL" \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text
)
```

各 SQS (S3) データソースごとに専用の SQS 標準キューを使用することを推奨します。同じキューを、他のバケット、他の prefix / suffix スコープ、または他の業務イベントに再利用しないでください。

## Step 2: SQS キューポリシーを設定する {#step-2-configure-the-sqs-queue-policy}

変更を加える前に、現在の SQS 属性をバックアップします。

```bash
aws sqs get-queue-attributes \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names Policy QueueArn \
  > "sqs-attributes.backup.$(date +%Y%m%d-%H%M%S).json"
```

指定した S3 バケットのみにメッセージ送信を許可する `queue-policy.json` を生成します。

```bash
jq -n \
  --arg policyId "$QUEUE_NAME-policy" \
  --arg queueArn "$QUEUE_ARN" \
  --arg bucketArn "$BUCKET_ARN" \
  --arg accountId "$AWS_ACCOUNT_ID" \
  '{
    Version: "2012-10-17",
    Id: $policyId,
    Statement: [
      {
        Sid: "AllowS3ToSendMessage",
        Effect: "Allow",
        Principal: {
          Service: "s3.amazonaws.com"
        },
        Action: "sqs:SendMessage",
        Resource: $queueArn,
        Condition: {
          ArnLike: {
            "aws:SourceArn": $bucketArn
          },
          StringEquals: {
            "aws:SourceAccount": $accountId
          }
        }
      }
    ]
  }' \
  > queue-policy.json
```

ポリシーを適用します。

```bash
jq -n \
  --arg policy "$(jq -c . queue-policy.json)" \
  '{Policy: $policy}' \
  > set-queue-attributes.json

aws sqs set-queue-attributes \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --attributes file://set-queue-attributes.json
```

## Step 3: S3 バケット通知を設定する {#step-3-configure-s3-bucket-notification}

変更を加える前に、現在のバケット通知をバックアップしてください。`put-bucket-notification-configuration` はバケット通知の設定全体を置き換えます。バケットにすでに他の通知がある場合は、新しい設定を適用する前にそれらをマージしてください。

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  > "bucket-notification.backup.$(date +%Y%m%d-%H%M%S).json"
```

`bucket-notification.json` を生成します。

```bash
jq -n \
  --arg id "$QUEUE_NAME" \
  --arg queueArn "$QUEUE_ARN" \
  --arg prefix "$PREFIX" \
  --arg suffix "$SUFFIX" \
  '{
    QueueConfigurations: [
      (
        {
          Id: $id,
          QueueArn: $queueArn,
          Events: [
            "s3:ObjectCreated:*"
          ]
        }
        +
        (
          [
            if $prefix != "" then {Name: "prefix", Value: $prefix} else empty end,
            if $suffix != "" then {Name: "suffix", Value: $suffix} else empty end
          ] as $rules
          | if ($rules | length) > 0
            then {Filter: {Key: {FilterRules: $rules}}}
            else {}
            end
        )
      )
    ]
  }' \
  > bucket-notification.json
```

設定を適用します。

```bash
aws s3api put-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  --notification-configuration file://bucket-notification.json
```

設定を確認します。

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME"
```

`QueueArn` が対象の SQS キューを指していること、`Events` に `s3:ObjectCreated:*` が含まれていること、`FilterRules` が {{{ .lake }}} データソースで設定した `Object Key Prefix` / `Object Key Suffix` と一致していることを確認してください。

## Step 4: {{{ .lake }}} が引き受ける IAM ロールを作成する {#step-4-create-an-iam-role-for-lake-to-assume}

`trust-policy.json` を生成します。`ExternalId` は {{{ .lake }}} (platform) コンソールの organization ID です。

```bash
jq -n \
  --arg platformSetupRoleArn "$PLATFORM_SETUP_ROLE_ARN" \
  --arg platformLoadRoleArn "$PLATFORM_LOAD_ROLE_ARN" \
  --arg externalId "$EXTERNAL_ID" \
  '{
    Version: "2012-10-17",
    Statement: [
      {
        Sid: "AllowPlatformSetupAssumeRole",
        Effect: "Allow",
        Principal: {
          AWS: $platformSetupRoleArn
        },
        Action: "sts:AssumeRole",
        Condition: {
          StringEquals: {
            "sts:ExternalId": $externalId
          }
        }
      },
      {
        Sid: "AllowPlatformLoadAssumeRole",
        Effect: "Allow",
        Principal: {
          AWS: $platformLoadRoleArn
        },
        Action: "sts:AssumeRole",
        Condition: {
          StringEquals: {
            "sts:ExternalId": $externalId
          }
        }
      }
    ]
  }' \
  > trust-policy.json
```

IAM ロールを作成します。

```bash
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://trust-policy.json
```

ロールがすでに存在する場合は、信頼ポリシーをバックアップして更新します。

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json \
  > "trust-policy.backup.$(date +%Y%m%d-%H%M%S).json"

aws iam update-assume-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-document file://trust-policy.json
```

## Step 5: S3/SQS 権限をアタッチする {#step-5-attach-s3-sqs-permissions}

`permissions-policy.json` を生成します。

```bash
jq -n \
  --arg bucketArn "$BUCKET_ARN" \
  --arg objectArn "$BUCKET_ARN/*" \
  --arg queueArn "$QUEUE_ARN" \
  '{
    Version: "2012-10-17",
    Statement: [
      {
        Sid: "S3BucketMetadataAccess",
        Effect: "Allow",
        Action: [
          "s3:GetBucketLocation",
          "s3:ListBucket"
        ],
        Resource: $bucketArn
      },
      {
        Sid: "S3ObjectReadAccess",
        Effect: "Allow",
        Action: [
          "s3:GetObject"
        ],
        Resource: $objectArn
      },
      {
        Sid: "SQSConsumeAccess",
        Effect: "Allow",
        Action: [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility"
        ],
        Resource: $queueArn
      }
    ]
  }' \
  > permissions-policy.json
```

権限を適用します。

```bash
aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name platform-s3-sqs-access \
  --policy-document file://permissions-policy.json
```

権限チェックリスト:

- SQS 権限は対象キューの ARN にスコープされています。
- S3 権限は対象バケットおよびオブジェクト ARN にスコープされています。
- デフォルトでは、このポリシーに S3 の書き込み権限や削除権限は不要です。
- 将来の SQS (S3) 統合タスクで **PURGE** または **Clean Up Original Files** を有効にし、取り込み成功後にソースオブジェクトを削除する場合は、対象オブジェクトパスに対する `s3:DeleteObject` を付与してください。

## Step 6: S3 から SQS への連携を確認する {#step-6-verify-s3-to-sqs}

`PREFIX` / `SUFFIX` に一致するテストオブジェクトをアップロードします。

```bash
echo 'a,b' > /tmp/sqs-s3-local-test.csv

aws s3 cp /tmp/sqs-s3-local-test.csv \
  "s3://$BUCKET_NAME/${PREFIX}sqs-s3-local-test-$(date +%s)$SUFFIX" \
  --region "$AWS_REGION"
```

SQS からメッセージを受信します。

```bash
aws sqs receive-message \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  --visibility-timeout 60
```

メッセージに `Records` が含まれていること、`eventSource` が `aws:s3` であること、`eventName` が `ObjectCreated:*` であること、そして `Records[].s3.bucket.name` と `Records[].s3.object.key` がテストオブジェクトと一致していることを確認します。

> **Note:**
>
> `receive-message` はメッセージを自動的に削除しません。可視性タイムアウトの間、一時的にメッセージを非表示にするだけです。後で {{{ .lake }}} にこのテストメッセージを消費させたい場合は、手動で削除しないでください。データソース接続をテストする前に、可視性タイムアウトが期限切れになるまで待ってください。

## {{{ .lake }}} に提供する情報 {#information-to-provide-to-lake}

AWS 側の設定が完了したら、{{{ .lake }}} でデータソースを作成する際に、以下の情報を入力します。

| パラメータ | 説明 |
|-----------|-------------|
| `role_arn` | {{{ .lake }}} が引き受けることを許可された、AWS アカウント内の IAM Role ARN |
| `external_id` | {{{ .lake }}} コンソールの Organization ID |
| `queue_url` | SQS 標準キューの URL |
| `queue_region` | SQS キューが配置されているリージョン |
| `bucket` | S3 バケット名 |
| `prefix` / `suffix` | 任意。S3 通知フィルターと一致している必要があります |

`role_arn` を取得するコマンド例:

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query 'Role.Arn' \
  --output text
```

## 設定要件 {#configuration-requirements}

- S3 バケットと SQS キューは同じ AWS リージョンに存在している必要があります。
- SQS キューは standard queue である必要があります。FIFO キューはサポートされていません。
- SQS キューは 1 つの S3 notification rule 専用にする必要があります。他のバケット、他の prefix / suffix スコープ、または他の業務イベントに再利用しないでください。
- S3 notification の bucket、prefix、suffix は、{{{ .lake }}} のデータソース設定と一致している必要があります。
- `put-bucket-notification-configuration` は、バケット通知設定全体を置き換えます。変更を適用する前に、既存の設定をバックアップし、マージしてください。
- S3 event notifications と SQS standard queues はどちらも at-least-once 配信を使用するため、メッセージが重複する可能性があります。

## 次のステップ {#next-steps}

このデータソースを作成した後は、これを使用して [Amazon SQS (S3) Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) を作成できます。