---
title: Encryption at Rest Using Customer-Managed Encryption Keys
summary: Learn about how to use Customer-Managed Encryption Key (CMEK) in TiDB Cloud.
---

# 顧客管理の暗号化キーを使用した保存時の暗号化 {#encryption-at-rest-using-customer-managed-encryption-keys}

顧客管理の暗号化キー (CMEK) を使用すると、お客様が完全に管理する暗号化キーを使用して、TiDB Dedicatedクラスター内の静的データを保護できます。このキーは CMEK キーとして知られています。

プロジェクトで CMEK を有効にすると、このプロジェクト内で作成されたすべてのクラスターは、この CMEK キーを使用して静的データを暗号化し、これらのクラスターによって生成されるバックアップ データも同じキーを使用して暗号化されます。 CMEK を有効にしない場合、 TiDB Cloud はエスクロー キーを使用して、クラスター内の保存中のすべてのデータを暗号化します。

> **ノート：**
>
> 現在、この機能はリクエストがあった場合にのみ利用可能です。この機能を試す必要がある場合は、 [<a href="/tidb-cloud/tidb-cloud-support.md">サポート</a>](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 制限 {#restrictions}

-   現在、 TiDB Cloudは、CMEK を提供するための AWS KMS の使用のみをサポートしています。
-   CMEK を使用するには、プロジェクトの作成時に CMEK を有効にし、クラスターを作成する前に CMEK 関連の構成を完了する必要があります。既存のプロジェクトに対して CMEK を有効にすることはできません。
-   現在、CMEK 対応プロジェクトでは、AWS でホストされるクラスターを[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB Dedicatededicated</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)だけ作成できます。 GCP でホストされる TiDB Dedicatedクラスターおよび[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターはサポートされていません。
-   現在、特定のプロジェクトでは、1 つの AWS リージョンに対してのみ CMEK を有効にすることができます。構成後は、同じプロジェクト内の他のリージョンにクラスターを作成することはできません。

## CMEKを有効にする {#enable-cmek}

アカウントが所有する KMS を使用してデータを暗号化する場合は、次の手順を実行します。

### ステップ 1. クラウドプロバイダーで KMS とIAMをプロビジョニングする {#step-1-provision-kms-and-iam-in-your-cloud-provider}

1.  AWS Key Management Service (KMS) コンソールで CMEK キーを作成します。 KMS キー ARN をコピーします。キーの作成方法については、AWS ドキュメントの[<a href="http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk">キーの作成</a>](http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk)を参照してください。

2.  IAMロールを作成し、ロールのアクセス ポリシーを CMEK に設定します。

    TiDB クラスターを期待どおりに機能させるには、KMS にアクセスするための特定の権限を TiDB アカウントに付与する必要があります。この機能は開発段階にあり、将来の機能ではさらに多くの権限が必要になる可能性があるため、ポリシー要件は変更される可能性があることに注意してください。現在サポートされている機能に必要な権限は次のとおりです。

    ```json
    {
        "Version": "2012-10-17",
        "Id": "cmek-policy",
        "Statement": [
            // EBS-related policy
            {
                "Sid": "Allow access through EBS for all principals in the account that are authorized to use EBS",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:CreateGrant",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": "<pingcap-account>",
                        "kms:ViaService": "ec2.<region>.amazonaws.com"
                    }
                }
            },
            // S3-related policy
            {
                "Sid": "Allow TiDB cloud role to use KMS to store encrypted backup to S3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<pingcap-account>:root"
                },
                "Action": [
                    "kms:Decrypt",
                    "kms:GenerateDataKey"
                ],
                "Resource": "*"
            },
            ... // user's own admin access to KMS
        ]
    }
    ```

> **ノート：**
>
> -   `<pingcap-account>`は、クラスターが実行されるアカウントです。アカウントがわからない場合は、 [<a href="/tidb-cloud/tidb-cloud-support.md">サポート</a>](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
> -   `<region>`はクラスターを作成するリージョンです (例: `us-west-2` )。地域を指定したくない場合は、 `<region>`ワイルドカード`*`に置き換えて、 `StringLike`ブロックに置きます。
> -   前のブロックの EBS 関連のポリシーについては、 [<a href="https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account">AWS ドキュメント</a>](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account)を参照してください。
> -   前のブロックの S3 関連のポリシーについては、 [<a href="https://repost.aws/knowledge-center/s3-bucket-access-default-encryption">AWS ブログ</a>](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption)を参照してください。

### ステップ 2. 新しいプロジェクトを作成し、CMEK を有効にする {#step-2-create-a-new-project-and-enable-cmek}

> **ノート：**
>
> 現在、CMEK 構成はTiDB Cloudコンソールでは利用できません。プロジェクトは、 TiDB Cloud API を使用してのみ構成できます。

1.  新しいプロジェクトを作成し、 TiDB Cloud API の[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject">プロジェクトを作成する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject)エンドポイントを使用して AWS CMEK を有効にします。

    `aws_cmek_enabled`フィールドが`true`に設定されていることを確認してください。

2.  TiDB CloudAPI の[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek">AWS CMEK の構成</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)エンドポイントを使用して、このプロジェクトの指定されたリージョン (us-east-1 など) の KMS キー ARN を構成します。

### ステップ 3. クラスターを作成する {#step-3-create-a-cluster}

ステップ 1 で作成したプロジェクトの下に、AWS でホストされる TiDB Dedicatedクラスターを作成します。クラスターが配置されているリージョンがステップ 2 のリージョンと同じであることを確認します。

> **ノート：**
>
> CMEK が有効な場合、クラスターのノードによって使用される EBS ボリュームとクラスターのバックアップに使用される S3 は、CMEK を使用して暗号化されます。

## CMEKを回転 {#rotate-cmek}

[<a href="http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html">自動 CMEK ローテーション</a>](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) AWS KMS で設定できます。このローテーションを有効にすると、CMEK ID を含むTiDB Cloudの保存時の暗号化プロジェクト設定を更新する必要がなくなります。

## CMEK を取り消して復元する {#revoke-and-restore-cmek}

TiDB Cloud の CMEK へのアクセスを一時的に取り消す必要がある場合は、次の手順に従ってください。

1.  AWS KMS コンソールで、対応するアクセス許可を取り消し、KMS キー ポリシーを更新します。
2.  TiDB Cloudコンソールで、プロジェクト内のすべてのクラスターを一時停止します。

> **ノート：**
>
> AWS KMS で CMEK を取り消しても、実行中のクラスターは影響を受けません。ただし、クラスターを一時停止してからクラスターを復元すると、クラスターは CMEK にアクセスできないため、正常に復元できなくなります。

TiDB Cloud の CMEK へのアクセスを取り消した後、アクセスを復元する必要がある場合は、次の手順に従います。

1.  AWS KMS コンソールで、CMEK アクセス ポリシーを復元します。
2.  TiDB Cloudコンソールで、プロジェクト内のすべてのクラスターを復元します。
