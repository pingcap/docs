---
title: Troubleshoot Access Denied Errors during Data Import from Amazon S3
summary: Learn how to troubleshoot access denied errors when importing data from Amazon S3 to TiDB Cloud.
---

# AmazonS3からのデータインポート中のアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

このドキュメントでは、AmazonS3からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーのトラブルシューティング方法について説明します。

TiDB Cloudコンソールの**[データインポートタスク**]ページで[<strong>検証</strong>]をクリックした後、キーワード`AccessDenied`のエラーメッセージが表示された場合は、アクセス拒否エラーが発生しています。

アクセス拒否エラーのトラブルシューティングを行うには、AWSマネジメントコンソールで次のチェックを実行します。

## IAMロールのポリシーを確認してください {#check-the-policy-of-the-iam-role}

AWSマネジメントコンソールで、[ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[ロール]に移動し、ターゲットTiDBクラスタ用に作成した<strong>ロール</strong>を見つけて、<strong>パーミッションポリシー</strong>を確認します。各ポリシーをチェックし、各ポリシーの`Resource`のフィールドが正しく構成されていることを確認します。

以下はサンプルポリシーです。

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data"
        },
        {
            "Sid": "AllowKMSkey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
        }
    ]
}
```

このサンプルポリシーでは、次の点に注意してください。

-   `"arn:aws:s3:::tidb-cloud-source-data/mydata/*"`では、 `"arn:aws:s3:::tidb-cloud-source-data"`はサンプルのS3バケットARNであり、 `/mydata/*`はデータストレージ用にS3バケットルートレベルでカスタマイズできるディレクトリです。ディレクトリは`/*`で終わる必要があります（例： `"<Your S3 bucket ARN>/<Directory of your source data>/*"` ）。 `/*`を追加しないと、 `AccessDenied`エラーが発生します。

-   お客様が管理するキー暗号化を使用してAWSキー管理サービスキー（SSE-KMS）を有効にしている場合は、次の構成がポリシーに含まれていることを確認してください。 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`はバケットのサンプルKMSキーです。

    ```
        {
            "Sid": "AllowKMSkey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
        }
    ```

    バケット内のオブジェクトが別の暗号化されたバケットからコピーされている場合、KMSキー値には両方のバケットのキーが含まれている必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]` 。

前の例に示すようにポリシーが正しく構成されていない場合は、ポリシーの`Resource`のフィールドを修正して、データのインポートを再試行してください。

> **ヒント：**
>
> アクセス許可ポリシーを複数回更新しても、データのインポート中に`AccessDenied`エラーが発生する場合は、アクティブなセッションを取り消すことができます。 [ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[<strong>ロール</strong>]に移動し、[<strong>アクティブ</strong>なセッションを取り消す]を見つけ、ボタンをクリックしてアクティブなセッションを取り消します。その後、データのインポートを再試行してください。
>
> これは他のアプリケーションに影響を与える可能性があることに注意してください。

## バケットポリシーを確認する {#check-the-bucket-policy}

AWSマネジメントコンソールで、Amazon S3コンソールを開き、[ **Bucket]** &gt; [ <strong>Permissions</strong> ]に移動して、[ <strong>Bucketポリシー]</strong>ページを見つけます。デフォルトでは、このページにはポリシー値がありません。このページに拒否されたポリシーが表示されている場合は、データのインポート中に`AccessDenied`エラーが発生する可能性があります。

拒否されたポリシーが表示された場合は、そのポリシーが現在のデータインポートに関連しているかどうかを確認してください。はいの場合は、ページから削除して、データのインポートを再試行してください。

## 信頼エンティティを確認してください {#check-the-trust-entity}

AWSマネジメントコンソールで、[ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[<strong>ロール</strong>]に移動し、[<strong>信頼関係</strong>]タブをクリックすると、信頼できるエンティティが表示されます。

以下は、信頼エンティティの例です。

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::380838443567:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe"
                }
            }
        }
    ]
}
```

サンプルの信頼エンティティ：

-   `380838443567`はTiDB CloudアカウントIDです。信頼エンティティのこのフィールドがTiDB CloudアカウントIDと一致することを確認してください。
-   `696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe`はTiDB Cloud外部IDです。信頼できるエンティティのこのフィールドがTiDB Cloud外部IDと一致することを確認してください。

## オブジェクトの所有権を確認してください {#check-the-object-ownership}

AWSマネジメントコンソールで、Amazon S3コンソールを開き、[ **Bucket]** &gt; [ <strong>Permissions</strong> ]に移動して、[ <strong>ObjectOwnership]</strong>ページを見つけます。 「オブジェクト所有権」構成が「バケット所有者強制」であることを確認してください。

構成が「バケット所有者の強制」でない場合、アカウントにこのバケット内のすべてのオブジェクトに対する十分な権限がないため、 `AccessDenied`エラーが発生します。

エラーを処理するには、[オブジェクトの所有権]領域の右上隅にある[**編集**]をクリックし、所有権を[バケットの所有者を強制]に変更します。これは、このバケットを使用している他のアプリケーションに影響を与える可能性があることに注意してください。

## バケットの暗号化タイプを確認してください {#check-your-bucket-encryption-type}

S3バケットを暗号化する方法は複数あります。バケット内のオブジェクトにアクセスしようとする場合、作成したロールには、データ復号化用の暗号化キーにアクセスするためのアクセス許可が必要です。そうしないと、 `AccessDenied`エラーが発生します。

バケットの暗号化タイプを確認するには、AWSマネジメントコンソールでAmazon S3コンソールを開き、ターゲットバケットの名前を選択し、[**プロパティ**]を選択すると、バケットの暗号化タイプを示す[<strong>デフォルトの暗号化]</strong>ページが表示されます。

サーバー側の暗号化には、Amazon S3管理キー（SSE-S3）とAWSキー管理サービス（SSE-KMS）の2種類があります。 SSE-S3の場合、この暗号化タイプではアクセス拒否エラーが発生しないため、これ以上のチェックは必要ありません。 SSE-KMSの場合、以下を確認する必要があります。

-   ページ上のAWSKMSキーARNが下線なしで黒で表示されている場合、AWS KMSキーはAWS管理のキー（aws / s3）です。
-   ページ上のAWSKMSキーARNが青色で下線付きで表示されている場合は、キーARNをクリックして特定の暗号化タイプを確認します。 AWS管理キー（aws / s3）または顧客管理キーの場合があります。

<details><summary>SSE-KMSのAWSマネージドキー（aws / s3）の場合</summary>

この状況で`AccessDenied`エラーが発生した場合は、キーが読み取り専用であり、アカウント間のアクセス許可の付与が許可されていないことが原因である可能性があります。詳細については、AWSの記事[クロスアカウントユーザーがカスタムAWSKMSキーで暗号化されたS3オブジェクトにアクセスしようとすると、アクセス拒否エラーが発生するのはなぜですか](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/)を参照してください。

アクセス拒否エラーを解決するには、[**デフォルトの暗号化**]ページの右上隅にある[<strong>編集</strong>]をクリックし、AWSKMSキーを[AWSKMSキーから選択]または[AWSKMSキーARNを入力]に変更するか、サーバーを変更します- 「AWSS3マネージドキー（SSE-S3）」へのサイド暗号化方式。この方式に加えて、新しいバケットを作成し、カスタムマネージドキーまたはSSE-S3暗号化方式を使用することもできます。

</details>

<details><summary>SSE-KMSの顧客管理キーの場合</summary>

この状況で`AccessDenied`のエラーを解決するには、キーARNをクリックするか、KMSでキーを手動で見つけます。**キーユーザー**ページが表示されます。ページの右上隅にある[<strong>追加</strong>]をクリックして、データをTiDB Cloudにインポートするために使用した役割を追加します。その後、データのインポートを再試行してください。

</details>

> **ノート：**
>
> バケット内のオブジェクトが既存の暗号化されたバケットからコピーされている場合は、ソースバケットのキーもAWSKMSキーARNに含める必要があります。これは、バケット内のオブジェクトがソースオブジェクトの暗号化と同じ暗号化方式を使用しているためです。詳細については、AWSドキュメント[レプリケーションでデフォルトの暗号化を使用する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)を参照してください。

## 手順については、AWSの記事を確認してください {#check-the-aws-article-for-instruction}

上記のすべてのチェックを実行しても`AccessDenied`のエラーが発生する場合は、AWSの記事[AmazonS3からの403AccessDeniedエラーのトラブルシューティング方法を教えてください](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/)で詳細を確認できます。
