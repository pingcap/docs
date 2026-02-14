---
title: Encryption at Rest Using Customer-Managed Encryption Keys on AWS
summary: AWS でホストされているTiDB Cloudクラスター内のデータをカスタマー管理暗号化キー (CMEK) を使用して暗号化する方法を学びます。
aliases: ['/ja/tidbcloud/tidb-cloud-encrypt-cmek']
---

# AWS での顧客管理の暗号化キーを使用した保存時の暗号化 {#encryption-at-rest-using-customer-managed-encryption-keys-on-aws}

顧客管理暗号鍵（CMEK）を使用すると、完全に管理可能な対称暗号鍵を利用して、 TiDB Cloud Dedicated クラスタ内の静的データを保護できます。この鍵はCMEK鍵と呼ばれます。

プロジェクトでCMEKを有効にすると、そのプロジェクト内で作成されるすべてのクラスタは、CMEK鍵を使用して静的データを暗号化します。さらに、これらのクラスタによって生成されるバックアップデータも同じ鍵を使用して暗号化されます。CMEKが有効になっていない場合、 TiDB Cloudはエスクロー鍵を使用して、クラスタ内のすべての保存データを暗号化します。

> **注記：**
>
> CMEKはBring Your Own Key（BYOK）に似ています。BYOKでは通常、ローカルで鍵を生成してアップロードします。しかし、 TiDB Cloudは[AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html)以内に生成された鍵をサポートします。

## 制限 {#restrictions}

-   現在、 TiDB Cloud はCMEK を提供するために AWS KMS と Azure Key Vault の使用のみをサポートしています。
-   CMEK を使用するには、プロジェクトの作成時に CMEK を有効にし、クラスタを作成する前に CMEK 関連の設定を完了する必要があります。既存のプロジェクトでは CMEK を有効にできません。
-   現在、CMEK 対応プロジェクトでは、AWS と Azure でホストされるクラスターを[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)つだけ作成できます。
-   現在、CMEK 対応プロジェクトでは、 [デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore-concepts.md#dual-region-backup)サポートされていません。
-   現在、CMEK 対応プロジェクトでは、AWS と Azure で CMEK を有効化できます。クラウドプロバイダーごとに、リージョンごとに 1 つの固有の暗号化キーを設定できます。選択したクラウドプロバイダーの暗号化キーを設定したリージョンでのみ、クラスタを作成できます。

## CMEKを有効にする {#enable-cmek}

アカウントが所有する KMS を使用してデータを暗号化する場合は、次の手順を実行します。

### ステップ 1. CMEK 対応プロジェクトを作成する {#step-1-create-a-cmek-enabled-project}

組織で`Organization Owner`ロールを担っている場合は、 TiDB Cloudコンソールまたは API を使用して CMEK 対応プロジェクトを作成できます。

<SimpleTab groupId="method">
<div label="Use Console" value="console">

CMEK 対応プロジェクトを作成するには、次の手順に従います。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用して対象の組織に切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト]**をクリックします。
3.  **「プロジェクト」**ページで、右上隅の**「新しいプロジェクトの作成」を**クリックします。
4.  プロジェクト名を入力してください。
5.  プロジェクトの CMEK 機能を有効にすることを選択します。
6.  **「確認」**をクリックしてプロジェクトの作成を完了します。

</div>
<div label="Use API" value="api">

この手順は、TiDB Cloud APIを使用して[CMEK 対応プロジェクトを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject)エンドポイント経由で完了できます。3フィールド`aws_cmek_enabled` `true`に設定されていることを確認してください。

現在、 TiDB Cloud APIはまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)ご覧ください。

</div>
</SimpleTab>

### ステップ2. プロジェクトのCMEK構成を完了する {#step-2-complete-the-cmek-configuration-of-the-project}

TiDB Cloudコンソールまたは API を使用して、プロジェクトの CMEK 構成を完了できます。

> **注記：**
>
> キーのポリシーが要件を満たしており、権限不足やアカウントの問題などのエラーがないことを確認してください。これらのエラーがあると、このキーを使用してクラスターが誤って作成される可能性があります。

<SimpleTab groupId="method">
<div label="Use Console" value="console">

プロジェクトの CMEK 構成を完了するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[暗号化アクセス]**をクリックします。
3.  **「暗号化アクセス」**ページで、 **「暗号化キーの作成」**をクリックして、キー作成ページに入ります。
4.  キープロバイダーはAWS KMSのみをサポートしています。暗号化キーを使用できるリージョンを選択できます。
5.  JSONファイルをコピーして`ROLE-TRUST-POLICY.JSON`として保存します。このファイルは信頼関係を記述します。
6.  この信頼関係をAWS KMSのキーポリシーに追加します。詳細については、 [AWS KMS のキーポリシー](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)を参照してください。
7.  TiDB Cloudコンソールで、キー作成ページの一番下までスクロールし、AWS KMS から取得した**KMS キー ARN**を入力します。
8.  **「作成」**をクリックしてキーを作成します。

</div>
<div label="Use API" value="api">

1.  AWS KMS でキーポリシーを設定し、キーポリシーに次の情報を追加します。

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

    -   `<pingcap-account>`はクラスターが実行されるアカウントです。アカウントがわからない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)問い合わせてください。
    -   `<region>`はクラスターを作成するリージョンです（例： `us-west-2` ）。リージョンを指定したくない場合は、 `<region>`ワイルドカード`*`に置き換え、 `StringLike`ブロックに入力します。
    -   前のブロックの EBS 関連のポリシーについては、 [AWSドキュメント](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account)を参照してください。
    -   前のブロックの S3 関連のポリシーについては、 [AWSブログ](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption)を参照してください。

2.  TiDB Cloud API の[AWS CMEK を構成する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)のエンドポイントを呼び出します。

    現在、 TiDB Cloud APIはまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)ご覧ください。

</div>
</SimpleTab>

> **注記：**
>
> この機能は今後さらに強化される予定であり、今後の機能には追加の権限が必要になる可能性があります。そのため、このポリシー要件は変更される可能性があります。

### ステップ3. クラスターを作成する {#step-3-create-a-cluster}

[ステップ1](#step-1-create-a-cmek-enabled-project)で作成したプロジェクトの下に、AWS でホストされるTiDB Cloud Dedicated クラスターを作成します。詳細な手順については[TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。クラスターが配置されているリージョンが[ステップ2](#step-2-complete-the-cmek-configuration-of-the-project)と同じであることを確認してください。

> **注記：**
>
> CMEK を有効にすると、クラスターのノードで使用される EBS ボリュームとクラスターのバックアップに使用される S3 が CMEK を使用して暗号化されます。

## CMEKを回転させる {#rotate-cmek}

AWS KMS で[自動CMEKローテーション](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)設定できます。このローテーションを有効にすると、 TiDB Cloudのプロジェクト設定で CMEK ID を含む**暗号化アクセス**を更新する必要はありません。

## CMEK を取り消して復元する {#revoke-and-restore-cmek}

TiDB Cloud の CMEK へのアクセスを一時的に取り消す必要がある場合は、次の手順に従います。

1.  AWS KMS コンソールで、対応する権限を取り消し、KMS キーポリシーを更新します。
2.  TiDB Cloudコンソールで、プロジェクト内のすべてのクラスターを一時停止します。

> **注記：**
>
> AWS KMS で CMEK を取り消しても、実行中のクラスターには影響しません。ただし、クラスターを一時停止してから復元すると、クラスターは CMEK にアクセスできないため、正常に復元できなくなります。

TiDB Cloud の CMEK へのアクセスを取り消した後、アクセスを復元する必要がある場合は、次の手順に従います。

1.  AWS KMS コンソールで、CMEK アクセスポリシーを復元します。
2.  TiDB Cloudコンソールで、プロジェクト内のすべてのクラスターを復元します。
