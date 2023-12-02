---
title: Troubleshoot Access Denied Errors during Data Import from Amazon S3
summary: Learn how to troubleshoot access denied errors when importing data from Amazon S3 to TiDB Cloud.
---

# Amazon S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

このドキュメントでは、Amazon S3 からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーのトラブルシューティング方法について説明します。

TiDB Cloudコンソールの**「データ インポート」**ページで**「次へ」**をクリックしてインポート プロセスを確認すると、 TiDB Cloud は指定したバケット URI のデータにアクセスできるかどうかの検証を開始します。キーワード`AccessDenied`を含むエラー メッセージが表示された場合は、アクセス拒否エラーが発生しています。

アクセス拒否エラーのトラブルシューティングを行うには、AWS マネジメント コンソールで次のチェックを実行します。

## 指定された役割を引き受けることはできません {#cannot-assume-the-provided-role}

このセクションでは、 TiDB Cloud が指定されたバケットにアクセスするための指定されたロールを引き受けることができない問題のトラブルシューティング方法について説明します。

### 信託エンティティを確認する {#check-the-trust-entity}

1.  AWS マネジメントコンソールで、 **[IAM]** &gt; **[アクセス管理]** &gt; **[ロール]**に移動します。
2.  ロールのリストで、ターゲット TiDB クラスター用に作成したロールを見つけてクリックします。役割の概要ページが表示されます。
3.  ロールの概要ページで、 **[信頼関係]**タブをクリックすると、信頼されたエンティティが表示されます。

以下は信頼エンティティのサンプルです。

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

サンプルの信頼エンティティでは、次のようになります。

-   `380838443567`はTiDB Cloudアカウント ID です。信頼エンティティのこのフィールドがTiDB Cloudアカウント ID と一致していることを確認してください。
-   `696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe`はTiDB Cloud外部 ID です。信頼できるエンティティのこのフィールドがTiDB Cloud外部 ID と一致していることを確認してください。

### IAMロールが存在するかどうかを確認する {#check-whether-the-iam-role-exists}

IAMロールが存在しない場合は、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)の手順に従ってロールを作成します。

### 外部IDが正しく設定されているか確認する {#check-whether-the-external-id-is-set-correctly}

指定された役割を引き受けることはできません`{role_arn}` 。ロールの信頼関係設定を確認してください。たとえば、信頼エンティティが`TiDB Cloud account ID`に設定されているかどうか、および信頼条件に`TiDB Cloud External ID`が正しく設定されているかどうかを確認します。 [信託エンティティを確認する](#check-the-trust-entity)を参照してください。

## アクセスが拒否されました {#access-denied}

このセクションでは、アクセス問題のトラブルシューティング方法について説明します。

### IAMユーザーのポリシーを確認する {#check-the-policy-of-the-iam-user}

IAMユーザーの AWS アクセス キーを使用して Amazon S3 バケットにアクセスすると、次のエラーが発生する場合があります。

-   「アクセス キー ID &#39;{access_key_id}&#39; とシークレット アクセス キー &#39;{secret_access_key}&#39; を使用したソース &#39;{bucket_uri}&#39; へのアクセスが拒否されました」

これは、権限が不十分なためにTiDB CloudがAmazon S3 バケットにアクセスできなかったことを示しています。 Amazon S3 バケットにアクセスするには、次の権限が必要です。

-   `s3:GetObject`
-   `s3:ListBucket`
-   `s3:GetBucketLocation`

IAMユーザーのポリシーを確認するには、次の手順を実行します。

1.  AWS マネジメントコンソールで、 **[IAM]** &gt; **[アクセス管理]** &gt; **[ユーザー]**に移動します。
2.  ユーザーのリストで、 TiDB Cloudへのデータのインポートに使用したユーザーを見つけてクリックします。ユーザー概要ページが表示されます。
3.  ユーザー概要ページの**権限ポリシー**領域に、ポリシーのリストが表示されます。ポリシーごとに次の手順を実行します。
    1.  ポリシーをクリックして、ポリシーの概要ページに移動します。
    2.  ポリシーの概要ページで、 **[JSON]**タブをクリックして権限ポリシーを確認します。ポリシーの`Resource`フィールドが正しく構成されていることを確認してください。

以下はポリシーの例です。

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
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
    }

ユーザーに権限を付与してテストする方法の詳細については、 [ユーザーポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)を参照してください。

### IAMロールのポリシーを確認する {#check-the-policy-of-the-iam-role}

1.  AWS マネジメントコンソールで、 **[IAM]** &gt; **[アクセス管理]** &gt; **[ロール]**に移動します。
2.  ロールのリストで、ターゲット TiDB クラスター用に作成したロールを見つけてクリックします。役割の概要ページが表示されます。
3.  役割の概要ページの**権限ポリシー**領域に、ポリシーのリストが表示されます。ポリシーごとに次の手順を実行します。
    1.  ポリシーをクリックして、ポリシーの概要ページに移動します。
    2.  ポリシーの概要ページで、 **[JSON]**タブをクリックして権限ポリシーを確認します。ポリシーの`Resource`フィールドが正しく構成されていることを確認してください。

以下はポリシーの例です。

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

このサンプル ポリシーでは、次の点に注意してください。

-   `"arn:aws:s3:::tidb-cloud-source-data/mydata/*"`の`"arn:aws:s3:::tidb-cloud-source-data"`はサンプル S3 バケット ARN で、 `/mydata/*`はデータstorage用に S3 バケットのルート レベルでカスタマイズできるディレクトリです。ディレクトリは`/*`で終わる必要があります (例: `"<Your S3 bucket ARN>/<Directory of your source data>/*"` 。 `/*`を追加しないと、 `AccessDenied`エラーが発生します。

-   顧客管理のキー暗号化を使用して AWS Key Management Service キー (SSE-KMS) を有効にしている場合は、次の設定がポリシーに含まれていることを確認してください。 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`はバケットのサンプル KMS キーです。

            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }

    バケット内のオブジェクトが別の暗号化されたバケットからコピーされた場合、KMS キーの値には両方のバケットのキーが含まれている必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]` 。

前の例に示すようにポリシーが正しく構成されていない場合は、ポリシーの`Resource`フィールドを修正し、データのインポートを再試行します。

> **ヒント：**
>
> アクセス許可ポリシーを複数回更新しても、データのインポート中に`AccessDenied`エラーが発生する場合は、アクティブなセッションを取り消してみることができます。 **[IAM]** &gt; **[アクセス管理]** &gt; **[ロール]**に移動し、ターゲット ロールをクリックしてロールの概要ページに入ります。役割の概要ページで、 **「アクティブなセッションを取り消す」を**見つけてボタンをクリックし、アクティブなセッションを取り消します。その後、データのインポートを再試行します。
>
> これは他のアプリケーションに影響を与える可能性があることに注意してください。

### バケットポリシーを確認してください {#check-the-bucket-policy}

1.  AWS マネジメントコンソールで、Amazon S3 コンソールを開き、 **[バケット]**ページに移動します。バケットのリストが表示されます。
2.  リストでターゲットのバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  **[権限]**タブをクリックし、 **[バケット ポリシー]**領域まで下にスクロールします。デフォルトでは、この領域にはポリシー値はありません。この領域に拒否されたポリシーが表示されている場合、データのインポート中に`AccessDenied`エラーが発生する可能性があります。

拒否されたポリシーが表示された場合は、そのポリシーが現在のデータ インポートに関連しているかどうかを確認してください。 「はい」の場合は、エリアから削除し、データのインポートを再試行します。

### オブジェクトの所有権を確認する {#check-the-object-ownership}

1.  AWS マネジメントコンソールで、Amazon S3 コンソールを開き、 **[バケット]**ページに移動します。バケットのリストが表示されます。
2.  バケットのリストで、ターゲットのバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  バケット情報ページで、 **「権限」**タブをクリックし、 **「オブジェクト所有権」**領域まで下にスクロールします。 「オブジェクトの所有権」設定が「バケット所有者を強制」であることを確認してください。

    構成が「バケット所有者強制」ではない場合、アカウントにこのバケット内のすべてのオブジェクトに対する十分な権限がないため、エラー`AccessDenied`が発生します。

このエラーを処理するには、「オブジェクト所有権」領域の右上隅にある**「編集」**をクリックし、所有権を「バケット所有者強制」に変更します。これは、このバケットを使用している他のアプリケーションに影響を与える可能性があることに注意してください。

### バケットの暗号化タイプを確認してください {#check-your-bucket-encryption-type}

S3 バケットを暗号化する方法は複数あります。バケット内のオブジェクトにアクセスしようとする場合、作成したロールには、データ復号化のための暗号化キーにアクセスする権限が必要です。それ以外の場合は、 `AccessDenied`エラーが発生します。

バケットの暗号化タイプを確認するには、次の手順を実行します。

1.  AWS マネジメントコンソールで、Amazon S3 コンソールを開き、 **[バケット]**ページに移動します。バケットのリストが表示されます。
2.  バケットのリストで、ターゲットのバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  バケット情報ページで、 **「プロパティ」**タブをクリックし、 **「デフォルトの暗号化」**領域まで下にスクロールして、この領域の構成を確認します。

サーバー側の暗号化には、Amazon S3 管理キー (SSE-S3) と AWS Key Management Service (SSE-KMS) の 2 種類があります。 SSE-S3 の場合、この暗号化タイプではアクセス拒否エラーが発生しないため、さらに確認する必要はありません。 SSE-KMS の場合は、次のことを確認する必要があります。

-   この領域の AWS KMS キー ARN が下線なしの黒色で表示されている場合、その AWS KMS キーは AWS 管理のキー (aws/s3) です。
-   エリア内の AWS KMS キー ARN がリンクとともに青色で表示されている場合は、キー ARN をクリックしてキー情報ページを開きます。左側のナビゲーション バーをチェックして、特定の暗号化タイプを確認してください。 AWS 管理キー (aws/s3) または顧客管理キーである可能性があります。

<details><summary>SSE-KMS の AWS 管理キー (aws/s3) の場合</summary>

この状況で`AccessDenied`エラーが発生した場合、キーが読み取り専用であり、クロスアカウントのアクセス許可の付与が許可されていないことが原因である可能性があります。詳細については、AWS の記事[クロスアカウントユーザーがカスタム AWS KMS キーで暗号化された S3 オブジェクトにアクセスしようとすると、アクセス拒否エラーが発生するのはなぜですか](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/)を参照してください。

アクセス拒否エラーを解決するには、 **[デフォルト暗号化]**領域の右上隅にある**[編集]**をクリックし、AWS KMS キーを [AWS KMS キーから選択] または [AWS KMS キー ARN を入力] に変更するか、サーバーを変更します。側の暗号化タイプを「AWS S3 マネージド キー (SSE-S3)」に設定します。この方法に加えて、新しいバケットを作成してカスタム マネージド キーまたは SSE-S3 暗号化方法を使用することもできます。

</details>

<details><summary>SSE-KMS のカスタマー マネージド キーの場合</summary>

この状況で`AccessDenied`エラーを解決するには、キー ARN をクリックするか、KMS でキーを手動で見つけます。 **「主要ユーザー」**ページが表示されます。領域の右上隅にある**[追加]**をクリックして、データをTiDB Cloudにインポートするために使用したロールを追加します。その後、データを再度インポートしてみてください。

</details>

> **注記：**
>
> バケット内のオブジェクトが既存の暗号化されたバケットからコピーされている場合は、ソース バケットのキーを AWS KMS キー ARN に含める必要もあります。これは、バケット内のオブジェクトがソース オブジェクトの暗号化と同じ暗号化方式を使用しているためです。詳細については、AWS ドキュメント[レプリケーションでのデフォルトの暗号化の使用](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)を参照してください。

### 手順については AWS の記事を確認してください {#check-the-aws-article-for-instruction}

上記のチェックをすべて実行してもエラー`AccessDenied`が発生する場合は、AWS の記事[Amazon S3 からの 403 アクセス拒否エラーをトラブルシューティングするにはどうすればよいですか](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/)で詳細な手順を確認してください。
