---
title: Amazon SQS (S3) - IAM Role (Beta)
summary: Learn how to create an "Amazon SQS (S3) - IAM Role" data source in {{{ .lake }}}.
---

# Amazon SQS (S3) - IAM Role (Beta)

This page describes how to create an `Amazon SQS (S3) - IAM Role` data source. This data source stores the configuration required to access an Amazon SQS queue and the corresponding S3 bucket, and is used for consuming S3 object creation events delivered from Amazon S3 to SQS.

`Amazon SQS (S3) - IAM Role` only stores the connection and authorization information required for SQS (S3) ingestion. It does not consume messages by itself. The actual process of reading SQS messages, parsing S3 ObjectCreated events, and writing data into {{{ .lake }}} is performed by an [Amazon SQS (S3) Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md).

## Use Cases

- Centrally manage the queue URL, Region, IAM Role, and path scope required for SQS (S3) ingestion
- Consume S3 `ObjectCreated` events and write the corresponding object data into {{{ .lake }}}
- Use S3 event notifications to drive data ingestion instead of relying only on polling an S3 path
- Update the IAM Role, queue URL, or path scope in one place when referenced by multiple tasks

## Create Amazon SQS (S3) - IAM Role

1. Navigate to **Data** > **Data Sources**, then click **Create Data Source**.
2. Select **Amazon SQS (S3) - IAM Role** as the service type, then fill in the connection details:

    | Field | Required | Description |
    |-------|----------|-------------|
    | **Name** | Yes | A descriptive name for the data source |
    | **Queue URL** | Yes | SQS standard queue URL, for example `https://sqs.us-east-1.amazonaws.com/123456789012/my-queue` |
    | **Queue Region** | Yes | AWS Region where the SQS queue is located, for example `us-east-1`. The S3 bucket must be in the same Region as the SQS queue |
    | **Role ARN** | Yes | IAM Role ARN in your AWS account that {{{ .lake }}} is allowed to assume |
    | **External ID** | Yes | Organization ID from the {{{ .lake }}} console, used in the IAM Role trust policy |
    | **Bucket** | Yes | Name of the S3 bucket that sends ObjectCreated events |
    | **Object Key Prefix** | No | Prefix filter for S3 object keys. This should match the S3 notification filter |
    | **Object Key Suffix** | No | Suffix filter for S3 object keys. This should match the S3 notification filter |

3. Click **Test Connectivity** to validate the connection. If the test succeeds, click **OK** to save the data source.

    > **Note:**
    >
    > SQS (S3) ingestion uses the AssumeRole model. You do not need to provide AWS Access Key or Secret Key to {{{ .lake }}}. Instead, create an IAM Role in your AWS account and allow {{{ .lake }}} platform roles to obtain temporary credentials through `sts:AssumeRole` in the role trust policy.

## AWS-Side Configuration Overview

Before creating the data source, complete the following configuration in your AWS account:

1. Create or prepare an SQS standard queue.
2. Configure the SQS queue policy to allow the specified S3 bucket to send messages to the queue.
3. Configure S3 bucket notification to send `ObjectCreated` events to the SQS queue.
4. Create an IAM Role that allows {{{ .lake }}} platform roles to access it through `sts:AssumeRole`.
5. Attach S3 read permissions and SQS consume permissions to the IAM Role.
6. Upload a test object and confirm that S3 can deliver the event to SQS.

Prepare the following variables first. `AWS_REGION` must be the Region where both the S3 bucket and SQS queue are located. `EXTERNAL_ID` is the organization ID from the {{{ .lake }}} platform console.

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
> Use the role ARNs provided by Platform: `PLATFORM_SETUP_ROLE_ARN` is the ARN of **Platform setup and validation role**, and `PLATFORM_LOAD_ROLE_ARN` is the ARN of **Platform data loading role**. In most cases, the trust policy of your IAM Role should trust both platform roles.

## Step 1: Create or Get an SQS Standard Queue

Create an SQS standard queue:

```bash
aws sqs create-queue \
  --region "$AWS_REGION" \
  --queue-name "$QUEUE_NAME"
```

Get the queue URL and queue ARN required by later steps:

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

We recommend using a dedicated SQS standard queue for each SQS (S3) data source. Do not reuse the same queue for other buckets, other prefix / suffix scopes, or other business events.

## Step 2: Configure the SQS Queue Policy

Back up the current SQS attributes before making changes:

```bash
aws sqs get-queue-attributes \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names Policy QueueArn \
  > "sqs-attributes.backup.$(date +%Y%m%d-%H%M%S).json"
```

Generate `queue-policy.json`, which only allows the specified S3 bucket to send messages:

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

Apply the policy:

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

## Step 3: Configure S3 Bucket Notification

Back up the current bucket notification before making changes. `put-bucket-notification-configuration` replaces the entire bucket notification configuration. If the bucket already has other notifications, merge them before applying the new configuration.

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  > "bucket-notification.backup.$(date +%Y%m%d-%H%M%S).json"
```

Generate `bucket-notification.json`:

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

Apply the configuration:

```bash
aws s3api put-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME" \
  --notification-configuration file://bucket-notification.json
```

Check the configuration:

```bash
aws s3api get-bucket-notification-configuration \
  --region "$AWS_REGION" \
  --bucket "$BUCKET_NAME"
```

Confirm that `QueueArn` points to the target SQS queue, `Events` includes `s3:ObjectCreated:*`, and `FilterRules` matches the `Object Key Prefix` / `Object Key Suffix` configured in the {{{ .lake }}} data source.

## Step 4: Create an IAM Role for {{{ .lake }}} to Assume

Generate `trust-policy.json`. `ExternalId` is the organization ID from the {{{ .lake }}} (platform) console.

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

Create the IAM Role:

```bash
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://trust-policy.json
```

If the role already exists, back up and update the trust policy:

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

## Step 5: Attach S3/SQS Permissions

Generate `permissions-policy.json`:

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

Apply the permissions:

```bash
aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name platform-s3-sqs-access \
  --policy-document file://permissions-policy.json
```

Permission checklist:

- SQS permissions are scoped to the target queue ARN.
- S3 permissions are scoped to the target bucket and object ARN.
- By default, this policy does not require S3 write or delete permissions.
- If a future SQS (S3) integration task enables **PURGE** or **Clean Up Original Files**, meaning source objects are deleted after successful ingestion, grant `s3:DeleteObject` on the target object path.

## Step 6: Verify S3 to SQS

Upload a test object that matches `PREFIX` / `SUFFIX`:

```bash
echo 'a,b' > /tmp/sqs-s3-local-test.csv

aws s3 cp /tmp/sqs-s3-local-test.csv \
  "s3://$BUCKET_NAME/${PREFIX}sqs-s3-local-test-$(date +%s)$SUFFIX" \
  --region "$AWS_REGION"
```

Receive a message from SQS:

```bash
aws sqs receive-message \
  --region "$AWS_REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  --visibility-timeout 60
```

Confirm that the message contains `Records`, that `eventSource` is `aws:s3`, that `eventName` is `ObjectCreated:*`, and that `Records[].s3.bucket.name` and `Records[].s3.object.key` match the test object.

> **Note:**
>
> `receive-message` does not delete the message automatically. It only hides the message temporarily during the visibility timeout. If you want {{{ .lake }}} to consume this test message later, do not delete it manually. Wait for the visibility timeout to expire before testing data source connectivity.

## Information to Provide to {{{ .lake }}}

After completing the AWS-side configuration, fill in the following information when creating the data source in {{{ .lake }}}:

| Parameter | Description |
|-----------|-------------|
| `role_arn` | IAM Role ARN in your AWS account that {{{ .lake }}} is allowed to assume |
| `external_id` | Organization ID from the {{{ .lake }}} console |
| `queue_url` | SQS standard queue URL |
| `queue_region` | Region where the SQS queue is located |
| `bucket` | S3 bucket name |
| `prefix` / `suffix` | Optional. This should match the S3 notification filter |

Command example for getting `role_arn`:

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query 'Role.Arn' \
  --output text
```

## Configuration Requirements

- The S3 bucket and SQS queue should be in the same AWS Region.
- The SQS queue must be a standard queue. FIFO queues are not supported.
- The SQS queue should be dedicated to one S3 notification rule. Do not reuse it for other buckets, other prefix / suffix scopes, or other business events.
- The bucket, prefix, and suffix in the S3 notification should match the {{{ .lake }}} data source configuration.
- `put-bucket-notification-configuration` replaces the entire bucket notification configuration. Back up and merge existing configurations before applying changes.
- S3 event notifications and SQS standard queues both use at-least-once delivery, so messages may be duplicated.

## Next Steps

After creating this data source, you can use it to create an [Amazon SQS (S3) Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md).
