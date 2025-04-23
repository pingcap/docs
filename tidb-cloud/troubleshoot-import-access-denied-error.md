---
title: Troubleshoot Access Denied Errors during Data Import from Amazon S3
summary: Amazon S3 からTiDB Cloudにデータをインポートするときに発生するアクセス拒否エラーのトラブルシューティング方法を説明します。
---

# Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

このドキュメントでは、Amazon S3 からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーのトラブルシューティング方法について説明します。

TiDB Cloudコンソールの「**データインポート」**ページで**「次へ」**をクリックし、インポートプロセスを確認すると、 TiDB Cloudは指定されたバケットURI内のデータにアクセスできるかどうかの検証を開始します。キーワード「 `AccessDenied`を含むエラーメッセージが表示された場合は、アクセス拒否エラーが発生しています。

アクセス拒否エラーのトラブルシューティングを行うには、AWS マネジメントコンソールで次のチェックを実行します。

## 指定された役割を引き受けることができません {#cannot-assume-the-provided-role}

このセクションでは、 TiDB Cloud が指定されたバケットにアクセスするために提供されたロールを引き受けることができない問題のトラブルシューティング方法について説明します。

### 信頼エンティティを確認する {#check-the-trust-entity}

1.  AWS マネジメントコンソールで、 **IAM** &gt;**アクセス管理**&gt;**ロール**に移動します。
2.  ロールのリストで、ターゲットTiDBクラスター用に作成したロールを見つけてクリックします。ロールの概要ページが表示されます。
3.  ロールの概要ページで、 **「信頼関係」**タブをクリックすると、信頼されたエンティティが表示されます。

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

サンプルの信頼エンティティでは次のようになります。

-   `380838443567`はTiDB CloudアカウントIDです。信頼エンティティのこのフィールドがTiDB CloudアカウントIDと一致していることを確認してください。
-   `696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe`はTiDB Cloud外部IDです。信頼できるエンティティのこのフィールドがTiDB Cloud外部IDと一致していることを確認してください。

### IAMロールが存在するかどうかを確認する {#check-whether-the-iam-role-exists}

IAMロールが存在しない場合は、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)手順に従ってロールを作成します。

### 外部IDが正しく設定されているか確認してください {#check-whether-the-external-id-is-set-correctly}

指定されたロール`{role_arn}`を引き受けることができません。ロールの信頼関係の設定を確認してください。例えば、信頼エンティティが`TiDB Cloud account ID`に設定されているか、信頼条件の`TiDB Cloud External ID`正しく設定されているかを確認してください[信頼エンティティを確認する](#check-the-trust-entity)参照してください。

## アクセスが拒否されました {#access-denied}

このセクションでは、アクセスの問題をトラブルシューティングする方法について説明します。

### IAMユーザーのポリシーを確認する {#check-the-policy-of-the-iam-user}

IAMユーザーの AWS アクセスキーを使用して Amazon S3 バケットにアクセスすると、次のエラーが発生する場合があります。

-   アクセスキーID「{access_key_id}」とシークレットアクセスキー「{secret_access_key}」を使用したソース「{bucket_uri}」へのアクセスが拒否されました。

これは、権限不足のため、 TiDB Cloud がAmazon S3 バケットにアクセスできなかったことを示しています。Amazon S3 バケットにアクセスするには、以下の権限が必要です。

-   `s3:GetObject`
-   `s3:ListBucket`
-   `s3:GetBucketLocation`

IAMユーザーのポリシーを確認するには、次の手順を実行します。

1.  AWS マネジメントコンソールで、 **IAM** &gt;**アクセス管理**&gt;**ユーザー**に移動します。
2.  ユーザーリストで、 TiDB Cloudへのデータのインポートに使用したユーザーを見つけてクリックします。ユーザーの概要ページが表示されます。
3.  ユーザー概要ページの**「権限ポリシー」**領域に、ポリシーの一覧が表示されます。各ポリシーごとに以下の手順を実行してください。
    1.  ポリシーをクリックすると、ポリシーの概要ページが表示されます。
    2.  ポリシーの概要ページで、 **{}JSON**タブをクリックして権限ポリシーを確認します。ポリシー内の`Resource`フィールドが正しく設定されていることを確認してください。

以下にサンプルポリシーを示します。

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

ユーザーに権限を付与してテストする方法の詳細については、 [ユーザーポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)参照してください。

### IAMロールのポリシーを確認する {#check-the-policy-of-the-iam-role}

1.  AWS マネジメントコンソールで、 **IAM** &gt;**アクセス管理**&gt;**ロール**に移動します。
2.  ロールのリストで、ターゲットTiDBクラスター用に作成したロールを見つけてクリックします。ロールの概要ページが表示されます。
3.  ロールの概要ページの**「権限ポリシー」**領域に、ポリシーの一覧が表示されます。各ポリシーごとに以下の手順を実行してください。
    1.  ポリシーをクリックすると、ポリシーの概要ページが表示されます。
    2.  ポリシーの概要ページで、 **{}JSON**タブをクリックして権限ポリシーを確認します。ポリシー内の`Resource`フィールドが正しく設定されていることを確認してください。

以下はサンプルポリシーです。

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

-   `"arn:aws:s3:::tidb-cloud-source-data/mydata/*"`の`"arn:aws:s3:::tidb-cloud-source-data"`はサンプルの S3 バケット ARN で、 `/mydata/*`データstorage用に S3 バケットのルートレベルでカスタマイズできるディレクトリです。ディレクトリの末尾は`/*` （例： `"<Your S3 bucket ARN>/<Directory of your source data>/*"` ）でなければなりません。 `/*`追加されていない場合、 `AccessDenied`エラーが発生します。

-   カスタマー管理のキー暗号化で AWS Key Management Service キー (SSE-KMS) を有効にしている場合は、次の設定がポリシーに含まれていることを確認してください。1 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`バケットのサンプル KMS キーです。

            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }

    バケット内のオブジェクトが別の暗号化バケットからコピーされた場合、KMSキーの値には両方のバケットのキーを含める必要があります。例： `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]` 。

前の例のようにポリシーが正しく構成されていない場合は、ポリシー内の`Resource`フィールドを修正して、再度データのインポートを試みてください。

> **ヒント：**
>
> 権限ポリシーを複数回更新してもデータのインポート中にエラー`AccessDenied`が発生する場合は、アクティブなセッションを取り消してみてください。 **「IAM」** &gt; **「アクセス管理」** &gt; **「ロール」**に移動し、対象のロールをクリックしてロールの概要ページに進みます。ロールの概要ページで**「アクティブなセッションを取り消す」**を見つけ、ボタンをクリックしてアクティブなセッションを取り消します。その後、データのインポートを再試行してください。
>
> 他のアプリケーションに影響する可能性があることに注意してください。

### バケットポリシーを確認する {#check-the-bucket-policy}

1.  AWS マネジメントコンソールで Amazon S3 コンソールを開き、 **「バケット」**ページに移動します。バケットのリストが表示されます。
2.  リストで対象のバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  **「権限」**タブをクリックし、 **「バケットポリシー」**領域までスクロールダウンします。デフォルトでは、この領域にはポリシー値がありません。この領域に拒否されたポリシーが表示されている場合、データのインポート中にエラー`AccessDenied`が発生する可能性があります。

拒否されたポリシーが表示された場合は、そのポリシーが現在のデータインポートに関連しているかどうかを確認してください。関連している場合は、そのポリシーをエリアから削除し、データインポートを再試行してください。

### オブジェクトの所有権を確認する {#check-the-object-ownership}

1.  AWS マネジメントコンソールで Amazon S3 コンソールを開き、 **「バケット」**ページに移動します。バケットのリストが表示されます。
2.  バケットのリストで、対象のバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  バケット情報ページで「**権限」**タブをクリックし、 **「オブジェクトの所有権」**領域までスクロールダウンします。「オブジェクトの所有権」設定が「バケット所有者による適用」になっていることを確認してください。

    設定が「バケット所有者による強制」ではない場合、アカウントにこのバケット内のすべてのオブジェクトに対する十分な権限がないため、エラー`AccessDenied`が発生します。

このエラーに対処するには、「オブジェクト所有権」領域の右上にある**「編集」**をクリックし、所有権を「バケット所有者を強制」に変更してください。ただし、このバケットを使用している他のアプリケーションに影響する可能性がありますのでご注意ください。

### バケットの暗号化タイプを確認してください {#check-your-bucket-encryption-type}

S3バケットを暗号化する方法は複数あります。バケット内のオブジェクトにアクセスするには、作成したロールに、データの復号に必要な暗号化キーへのアクセス権限が付与されている必要があります。権限がない場合、エラー`AccessDenied`が発生します。

バケットの暗号化タイプを確認するには、次の手順を実行します。

1.  AWS マネジメントコンソールで Amazon S3 コンソールを開き、 **「バケット」**ページに移動します。バケットのリストが表示されます。
2.  バケットのリストで、対象のバケットを見つけてクリックします。バケット情報ページが表示されます。
3.  バケット情報ページで、 **[プロパティ]**タブをクリックし、 **[デフォルトの暗号化]**領域まで下にスクロールして、この領域の設定を確認します。

サーバー側暗号化には、Amazon S3 マネージドキー (SSE-S3) と AWS Key Management Service (SSE-KMS) の 2 種類があります。SSE-S3 の場合、アクセス拒否エラーが発生しないため、これ以上の確認は不要です。SSE-KMS の場合は、以下の点を確認する必要があります。

-   当該エリア内の AWS KMS キー ARN が下線なしの黒色で表示されている場合、その AWS KMS キーは AWS 管理キー (aws/s3) です。
-   該当エリアのAWS KMSキーARNが青色でリンク付きで表示されている場合は、そのキーARNをクリックしてキー情報ページを開きます。左側のナビゲーションバーで具体的な暗号化タイプを確認してください。AWS管理キー（aws/s3）またはカスタマー管理キーのいずれかです。

<details><summary>SSE-KMSのAWS管理キー（aws/s3）の場合</summary>

この状況でエラー`AccessDenied`が発生した場合、キーが読み取り専用であり、アカウント間の権限付与が許可されていないことが原因である可能性があります。詳細については、AWSの記事[クロスアカウントユーザーがカスタム AWS KMS キーで暗号化された S3 オブジェクトにアクセスしようとすると、アクセス拒否エラーが発生するのはなぜですか?](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/)ご覧ください。

アクセス拒否エラーを解決するには、 **「デフォルトの暗号化」**領域の右上隅にある**「編集」**をクリックし、AWS KMS キーを「AWS KMS キーから選択」または「AWS KMS キー ARN を入力」に変更するか、サーバー側の暗号化タイプを「AWS S3 マネージドキー（SSE-S3）」に変更します。この方法に加えて、新しいバケットを作成し、カスタムマネージドキーまたは SSE-S3 暗号化方式を使用することもできます。

</details>

<details><summary>SSE-KMSの顧客管理キーの場合</summary>

この状況でエラー`AccessDenied`を解決するには、キーのARNをクリックするか、KMSでキーを手動で検索してください。**キーユーザー**ページが表示されます。ページの右上隅にある**「追加」**をクリックして、 TiDB Cloudへのデータインポートに使用したロールを追加します。その後、データのインポートを再度お試しください。

</details>

> **注記：**
>
> バケット内のオブジェクトが既存の暗号化バケットからコピーされた場合は、AWS KMS キー ARN にソースバケットのキーも含める必要があります。これは、バケット内のオブジェクトがソースオブジェクトの暗号化と同じ暗号化方式を使用しているためです。詳細については、AWS ドキュメント[レプリケーションでのデフォルトの暗号化の使用](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)ご覧ください。

### 手順についてはAWSの記事を確認してください {#check-the-aws-article-for-instruction}

上記のすべてのチェックを実行してもエラー`AccessDenied`が発生する場合は、詳細な手順については AWS の記事[Amazon S3 からの 403 アクセス拒否エラーをトラブルシューティングするにはどうすればいいですか?](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/)確認してください。
