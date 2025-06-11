---
title: Configure TiDB Cloud Serverless External Storage Access
summary: Amazon Simple Storage Service (Amazon S3) アクセスを構成する方法を学習します。
---

# TiDB Cloud Serverless の外部ストレージアクセスを構成する {#configure-external-storage-access-for-tidb-cloud-serverless}

TiDB Cloud Serverless クラスター内の外部storageからデータをインポートまたはエクスポートする場合は、クロスアカウントアクセスを設定する必要があります。このドキュメントでは、 TiDB Cloud Serverless クラスターの外部storageへのアクセスを設定する方法について説明します。

TiDB Cloud Dedicated クラスター用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud Dedicatedの外部ストレージアクセスを構成する](/tidb-cloud/dedicated-external-storage.md)参照してください。

## Amazon S3 アクセスを構成する {#configure-amazon-s3-access}

TiDB Cloud Serverless クラスターが Amazon S3 バケット内のソースデータにアクセスできるようにするには、次のいずれかの方法を使用してクラスターのバケットアクセスを設定します。

-   [ロールARNを使用する](#configure-amazon-s3-access-using-a-role-arn) : ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   [AWSアクセスキーを使用する](#configure-amazon-s3-access-using-an-aws-access-key) : IAMユーザーのアクセスキーを使用して Amazon S3 バケットにアクセスします。

### ロール ARN を使用して Amazon S3 アクセスを構成する {#configure-amazon-s3-access-using-a-role-arn}

ロールARNを作成するには、 [AWS クラウドフォーメーション](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)使用することをお勧めします。作成するには、以下の手順に従ってください。

> **注記：**
>
> Amazon S3へのロールARNアクセスは、クラウドプロバイダーとしてAWSを使用しているクラスターでのみサポートされます。別のクラウドプロバイダーを使用している場合は、代わりにAWSアクセスキーを使用してください。詳細については、 [AWS アクセスキーを使用して Amazon S3 アクセスを構成する](#configure-amazon-s3-access-using-an-aws-access-key)ご覧ください。

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **新しい ARN の追加**ダイアログを開きます。

    -   Amazon S3 からデータをインポートする場合は、次のようにして**[新しい ARN の追加]**ダイアログを開きます。

        1.  **S3 からインポート**をクリックします。
        2.  **ファイル URI**フィールドに入力します。
        3.  **AWS ロール ARN**を選択し、[**ここをクリックして AWS CloudFormation で新規作成] を**クリックします。

    -   データを Amazon S3 にエクスポートする場合は、次のようにして**[新しい ARN の追加]**ダイアログを開きます。

        1.  **「データをエクスポート...」** &gt; **「Amazon S3」**をクリックします。クラスターでこれまでデータのインポートもエクスポートもしたことがない場合は、ページ下部の**「データをエクスポートするにはここをクリック...** 」 &gt; **「Amazon S3」**をクリックします。
        2.  **フォルダー URI**フィールドに入力します。
        3.  **AWS ロール ARN**を選択し、[**ここをクリックして AWS CloudFormation で新規作成] を**クリックします。

3.  AWS CloudFormation テンプレートを使用してロール ARN を作成します。

    1.  [**新しい ARN の追加]**ダイアログで、 **[AWS コンソールと CloudFormation テンプレート]**をクリックします。

    2.  [AWS マネジメントコンソール](https://console.aws.amazon.com)にログインすると、AWS CloudFormation の**クイック作成スタック**ページにリダイレクトされます。

    3.  **ロール名**を入力します。

    4.  新しいロールを作成することを確認し、 **「スタックの作成」**をクリックしてロール ARN を作成します。

    5.  CloudFormation スタックが実行された後、 **[出力]**タブをクリックし、 **[値]**列でロール ARN 値を見つけることができます。

        ![img.png](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

AWS CloudFormation でロール ARN を作成するときに問題が発生した場合は、次の手順に従って手動で作成できます。

<details><summary>詳細はこちらをクリック</summary>

1.  前の手順で説明した**「新しいARNを追加」**ダイアログで、 **「問題が発生した場合は、ロールARNを手動で作成してください」**をクリックします。TiDB **TiDB CloudアカウントID**と**TiDB Cloud外部ID**が表示されます。

2.  AWS マネジメントコンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)にサインインして[Amazon S3 コンソール](https://console.aws.amazon.com/s3/)開きます。

    2.  **「バケット」**リストで、ソースデータがあるバケットの名前を選択し、 **「ARNをコピー」**をクリックしてS3バケットのARN（例： `arn:aws:s3:::tidb-cloud-source-data` ）を取得します。後で使用するために、バケットのARNをメモしておいてください。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [IAMコンソール](https://console.aws.amazon.com/iam/)開き、左側のナビゲーション ペインで**[ポリシー]**をクリックして、 **[ポリシーの作成] を**クリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **[ポリシーの作成]**ページで、 **[JSON]**タブをクリックします。

    5.  必要に応じて、ポリシーテキストフィールドでポリシーを設定します。以下は、 TiDB Cloud Serverless クラスターとの間でデータのエクスポートとインポートを行う例です。

        -   TiDB Cloud Serverless クラスターからデータをエクスポートするには**、s3:PutObject**および**s3:ListBucket**権限が必要です。
        -   TiDB Cloud Serverless クラスターにデータをインポートするには**、 s3:GetObject** 、 **s3:GetObjectVersion** 、および**s3:ListBucket**権限が必要です。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        ポリシー テキスト フィールドで、次の構成を独自の値に置き換えます。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"` 。例えば:

            -   ソース データが`tidb-cloud-source-data`バケットのルート ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`使用します。
            -   ソース データがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`使用します。

            TiDB Cloud がこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの末尾に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"` 、たとえば`"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

        -   カスタマー管理のキー暗号化で AWS Key Management Service キー (SSE-KMS) を有効にしている場合は、次の設定がポリシーに含まれていることを確認してください。1 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`バケットのサンプル KMS キーです。

                {
                    "Sid": "AllowKMSkey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:Decrypt"
                    ],
                    "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
                }

        -   バケット内のオブジェクトが別の暗号化バケットからコピーされた場合、KMSキーの値には両方のバケットのキーを含める必要があります。例： `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]` 。

    6.  **「次へ」**をクリックします。

    7.  ポリシー名を設定し、ポリシーのタグ（オプション）を追加して、 **「ポリシーの作成」を**クリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  [IAMコンソール](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインの**[ロール]**をクリックし、 **[ロールの作成] を**クリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   **信頼されたエンティティタイプ**で、 **AWS アカウント**を選択します。
        -   **「AWS アカウント」**で**「別の AWS アカウント」**を選択し、 TiDB Cloudアカウント ID を**「アカウント ID」**フィールドに貼り付けます。
        -   **オプション**で、 **「外部IDが必要（サードパーティがこのロールを引き受ける場合のベストプラクティス）」**をクリックし、 TiDB Cloudの外部IDを**「外部ID」**フィールドに貼り付けます。「外部IDが必要」を指定せずにロールを作成した場合、プロジェクト内の1つのTiDBクラスターの設定が完了すると、そのプロジェクト内のすべてのTiDBクラスターが同じロールARNを使用してAmazon S3バケットにアクセスできるようになります。アカウントIDと外部IDを指定してロールを作成した場合、対応するTiDBクラスターのみがバケットにアクセスできます。

    3.  **[次へ]**をクリックしてポリシー リストを開き、作成したポリシーを選択して、 **[次へ]**をクリックします。

    4.  **ロールの詳細**でロールの名前を設定し、右下にある**「ロールの作成」**をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロール ARN を取得できます。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### AWS アクセスキーを使用して Amazon S3 アクセスを構成する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成するには、AWS アカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  IAMユーザーを作成します。詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWS アカウント ID またはアカウントエイリアス、 IAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

> **注記：**
>
> TiDB Cloudはアクセスキーを保存しません。インポートまたはエクスポートが完了したら、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)実行することをお勧めします。

## GCS アクセスを構成する {#configure-gcs-access}

TiDB Cloud Serverless クラスタが GCS バケットにアクセスできるようにするには、バケットの GCS アクセスを設定する必要があります。バケットアクセスの設定には、サービスアカウントキーを使用できます。

サービス アカウント キーを構成するには、次の手順を実行します。

1.  Google Cloud [サービスアカウントページ](https://console.cloud.google.com/iam-admin/serviceaccounts)で、 **「サービスアカウントを作成」**をクリックしてサービスアカウントを作成します。詳細については、 [サービスアカウントの作成](https://cloud.google.com/iam/docs/creating-managing-service-accounts)ご覧ください。

    1.  サービス アカウント名を入力します。

    2.  オプション: サービス アカウントの説明を入力します。

    3.  **[作成して続行]**をクリックして、サービス アカウントを作成します。

    4.  `Grant this service account access to project`で、必要な権限を持つ[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)選択します。

        -   TiDB Cloud Serverless クラスターからデータをエクスポートするには、 `storage.objects.create`権限を持つロールが必要です。
        -   TiDB Cloud Serverless クラスターにデータをインポートするには、 `storage.buckets.get` 、 `storage.objects.get` 、 `storage.objects.list`権限を持つロールが必要です。

    5.  **「続行」**をクリックして次のステップに進みます。

    6.  オプション: `Grant users access to this service account`で、 [サービスアカウントを他のリソースに接続する](https://cloud.google.com/iam/docs/attach-service-accounts)必要なメンバーを選択します。

    7.  **[完了] を**クリックして、サービス アカウントの作成を完了します。

    ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2.  サービス アカウントをクリックし、 `KEYS`ページで**[キーの追加]**をクリックしてサービス アカウント キーを作成します。

    ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3.  デフォルトのキータイプ`JSON`を選択し、 **「作成」**をクリックしてGoogle Cloud認証情報ファイルをダウンロードします。このファイルには、TiDB Cloud ServerlessクラスタのGCSアクセスを構成する際に必要なサービスアカウントキーが含まれています。

## Azure Blob Storage アクセスを構成する {#configure-azure-blob-storage-access}

TiDB Cloud Serverless が Azure Blob コンテナーにアクセスできるようにするには、コンテナーのサービス SAS トークンを作成する必要があります。

SAS トークンは、 [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview) (推奨) または手動構成を使用して作成できます。

Azure ARM テンプレートを使用して SAS トークンを作成するには、次の手順を実行します。

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **ARM テンプレートの展開による新しい SAS トークンの生成**ダイアログを開きます。

    1.  **「データのエクスポート先...」** &gt; **「Azure Blob Storage」**をクリックします。クラスターでこれまでにデータのインポートもエクスポートもしたことがない場合は、ページの下部にある**「データのエクスポート先...」** &gt; **「Azure Blob Storage」**をクリックします。

    2.  **Azure Blob Storage 設定**領域まで下にスクロールし、SAS トークン フィールドの下に**ある Azure ARM テンプレートを使用して新規作成するには、ここをクリック**します。をクリックします。

3.  Azure ARM テンプレートを使用して SAS トークンを作成します。

    1.  **[ARM テンプレートのデプロイによる新しい SAS トークンの生成]**ダイアログで、[クリックして**、事前構成された ARM テンプレートを含む Azure Portal を開く] をクリックします**。

    2.  Azure にログインすると、Azure**カスタム デプロイメント**ページにリダイレクトされます。

    3.  **カスタムデプロイ**ページで、**リソースグループ**と**ストレージアカウント名**を入力します。コンテナが配置されているstorageアカウントの概要ページからすべての情報を取得できます。

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4.  **「確認と作成」**または**「次へ」**をクリックして、デプロイ内容を確認します。 **「作成」**をクリックしてデプロイを開始します。

    5.  完了すると、デプロイの概要ページにリダイレクトされます。 **「出力」**セクションに移動して、SAS トークンを取得してください。

Azure ARM テンプレートを使用して SAS トークンを作成するときに問題が発生した場合は、次の手順に従って手動で作成してください。

<details><summary>詳細はこちらをクリック</summary>

1.  [Azure ストレージ アカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するstorageアカウントをクリックします。

2.  **ストレージ アカウント**ページで、[**Security+ ネットワーク]**をクリックし、 **[Shared access signature]**をクリックします。

    ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3.  **Shared Access Signature**ページで、必要な権限を持つサービスSASトークンを以下のように作成します。詳細については、 [サービスSASトークンを作成する](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)参照してください。

    1.  **[許可されたサービス]**セクションで、 **Blob**サービスを選択します。

    2.  **許可されたリソース タイプ**セクションで、**コンテナー**と**オブジェクト**を選択します。

    3.  **「許可された権限」**セクションで、必要に応じて権限を選択します。

        -   TiDB Cloud Serverless クラスターからデータをエクスポートするには、**読み取り**権限と**書き込み**権限が必要です。
        -   TiDB Cloud Serverless クラスターにデータをインポートするには、**読み取り**権限と**リスト**権限が必要です。

    4.  必要に応じて**開始日時と有効期限**を調整します。

    5.  その他の設定はデフォルト値のままにしておきます。

    ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4.  SAS トークンを生成するには、 **「SAS と接続文字列の生成」を**クリックします。

</details>

## Alibaba Cloud Object Storage Service (OSS) アクセスを構成する {#configure-alibaba-cloud-object-storage-service-oss-access}

TiDB Cloud Serverless が Alibaba Cloud OSS バケットにアクセスできるようにするには、バケットの AccessKey ペアを作成する必要があります。

AccessKey ペアを構成するには、次の手順を実行します。

1.  RAMユーザーを作成し、AccessKeyペアを取得します。詳細については、 [RAMユーザーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)参照してください。

    **[アクセス モード]**セクションで、 **[永続的な AccessKey を使用してアクセスする] を**選択します。

2.  必要な権限を持つカスタムポリシーを作成します。詳細については、 [カスタムポリシーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)参照してください。

    -   **[効果]**セクションで、 **[許可]**を選択します。

    -   **[サービス]**セクションで、 **[オブジェクト ストレージ サービス]**を選択します。

    -   **「アクション」**セクションで、必要に応じて権限を選択します。

        TiDB Cloud Serverless クラスターにデータをインポートするには、 **oss:GetObject** 、 **oss:GetBucketInfo** 、および**oss:ListObjects**権限を付与します。

        TiDB Cloud Serverless クラスターからデータをエクスポートするには、 **oss:PutObject** 、 **oss:GetBucketInfo** 、および**oss:ListBuckets**権限を付与します。

    -   **リソース**セクションで、バケットとバケット内のオブジェクトを選択します。

3.  カスタムポリシーをRAMユーザーにアタッチします。詳細については、 [RAMユーザーに権限を付与する](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)参照してください。
