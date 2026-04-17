---
title: Configure External Storage Access
summary: Amazon Simple Storage Service (Amazon S3) などの外部storageへのクロスアカウントアクセスを設定する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-external-storage']
---

# 外部ストレージへのアクセスを構成する {#configure-external-storage-access}

<CustomContent plan="starter,essential">

TiDB Cloud StarterまたはEssentialインスタンスで外部storageからデータをインポートしたり、外部ストレージにデータをエクスポートしたりするには、アカウント間アクセスを設定する必要があります。このドキュメントでは、 TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスで外部storageへのアクセスを設定する方法について説明します。

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud Premiumインスタンスで外部storageからデータをインポートしたり、外部ストレージにデータをエクスポートしたりするには、アカウント間アクセスを設定する必要があります。このドキュメントでは、TiDB Cloud Premiumインスタンスの外部storageへのアクセスを設定する方法について説明します。

</CustomContent>

TiDB Cloud Dedicatedクラスター用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud Dedicatedの外部ストレージアクセスを構成する](/tidb-cloud/dedicated-external-storage.md)参照してください。

## Amazon S3へのアクセスを設定する {#configure-amazon-s3-access}

<CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスが Amazon S3 バケットにアクセスできるようにするには、次のいずれかの方法を使用してインスタンスのバケット アクセスを設定します。

-   [ロールARNを使用する](#configure-amazon-s3-access-using-a-role-arn): ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   [AWSアクセスキーを使用する](#configure-amazon-s3-access-using-an-aws-access-key): IAMユーザーのアクセスキーを使用して、Amazon S3 バケットにアクセスします。

### ロールARNを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-a-role-arn}

ロールARNの作成には[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)使用することをお勧めします。作成するには、以下の手順に従ってください。

> **注記：**
>
> Amazon S3 へのロール ARN アクセスは、ターゲット<CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスのクラウドプロバイダーが AWS である場合にのみサポートされます。別のクラウドプロバイダーを使用する場合は、代わりに AWS アクセスキーを使用してください。詳細については、 [AWSアクセスキーを使用してAmazon S3へのアクセスを設定する](#configure-amazon-s3-access-using-an-aws-access-key)参照してください。

1.  ターゲットの<CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。
    2.  ターゲットの<CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **「新しいARNの追加」**ダイアログを開きます。

    -   Amazon S3からデータをインポートする場合は、次のようにして**「新しいARNの追加」**ダイアログを開きます。

        1.  **「S3からインポート」を**クリックします。
        2.  **ファイルURI**欄に入力してください。
        3.  **AWS ロール ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    <CustomContent plan="starter,essential">

    -   データをAmazon S3にエクスポートする場合は、次のように**「新しいARNの追加」**ダイアログを開きます。

        1.  **「データのエクスポート先...」** &gt; **「Amazon S3」**をクリックします。TiDB Cloud StarterまたはEssentialインスタンスでこれまでデータのインポートまたはエクスポートが行われていない場合は、ページ下部の**「ここをクリックしてデータをエクスポート...」** &gt; **「Amazon S3」**をクリックしてください。
        2.  **フォルダURI**欄に入力してください。
        3.  **AWS ロール ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    </CustomContent>

    <CustomContent plan="premium">

    -   データをAmazon S3にエクスポートする場合は、次のように**「新しいARNの追加」**ダイアログを開きます。

        1.  **「データのエクスポート」を**クリックします。
        2.  **ターゲット接続**で**Amazon S3を**選択してください。
        3.  **フォルダURI**欄に入力してください。
        4.  **AWS ロール ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    </CustomContent>

3.  AWS CloudFormationテンプレートを使用してロールARNを作成します。

    1.  **「新しい ARN の追加」**ダイアログで、 **「CloudFormation テンプレートを使用した AWS コンソール」**をクリックします。

    2.  [AWS マネジメントコンソール](https://console.aws.amazon.com)コンソールにログインすると、AWS CloudFormation の**クイック作成スタック**ページにリダイレクトされます。

    3.  **役割名**を入力してください。

    4.  新しいロールを作成することに同意し、 **「スタックの作成」**をクリックしてロールARNを作成します。

    5.  CloudFormationスタックの実行後、 **[出力]**タブをクリックすると、 **[値]**列にロールARNの値が表示されます。

        ![Role ARN](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

AWS CloudFormationでロールARNを作成する際に問題が発生した場合は、以下の手順で手動で作成できます。

<details><summary>詳細はこちらをクリックしてください</summary>

1.  前の手順で説明した**「新しい ARN を追加」**ダイアログで、 **「問題が発生しましたか？ロール ARN を手動で作成します」**をクリックします。TiDB **TiDB Cloudアカウント ID**と**TiDB Cloud外部 ID**が取得されます。

2.  AWS マネジメントコンソールで、Amazon S3 バケット用のマネージドポリシーを作成します。

    1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)コンソールにサインインし、 [Amazon S3コンソール](https://console.aws.amazon.com/s3/)を開きます。

    2.  **バケット**一覧から対象バケットの名前を選択し、 **「ARNをコピー」**をクリックしてS3バケットのARNを取得します（例： `arn:aws:s3:::tidb-cloud-source-data` ）。後で使用するために、バケットのARNをメモしておいてください。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [IAMコンソール](https://console.aws.amazon.com/iam/)を開き、左側のナビゲーションペインで**「ポリシー」**をクリックし、 **「ポリシーの作成」を**クリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **ポリシー作成**ページで、 **「JSON」**タブをクリックします。

    5.  ポリシーテキストフィールドで、必要に応じてポリシーを設定してください。以下は、 <CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>。

        -   <CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスからデータをエクスポートするには、 **s3:PutObject**および**s3:ListBucket**権限が必要です。
        -   <CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスにデータをインポートするには、 **s3:GetObject** 、 **s3:GetObjectVersion** 、および**s3:ListBucket**権限が必要です。

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
                    "Resource": "<Your S3 bucket ARN>/<Your data directory>/*"
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

        ポリシーテキストフィールドで、以下の設定を独自の値に置き換えてください。

        -   `"Resource": "<Your S3 bucket ARN>/<Your data directory>/*"` 、ここで`<Your data directory>`はエクスポートされたデータのターゲットディレクトリ、またはインポートされたデータのソースディレクトリです。例:

            -   インポートまたはエクスポートするデータが`tidb-cloud-source-data`バケットのルート ディレクトリにある場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`を使用してください。
            -   インポートまたはエクスポートするデータがバケットの`mydata`ディレクトリにある場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`を使用します。

            TiDB Cloud がこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの末尾に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"` 、例えば`"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

        -   AWS Key Management Service キー (SSE-KMS) を顧客管理キー暗号化で有効にしている場合は、ポリシーに次の設定が含まれていることを確認してください。 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`は、バケットの KMS キーの例です。

                {
                    "Sid": "AllowKMSkey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:Decrypt"
                    ],
                    "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
                }

        -   バケット内のオブジェクトが別の暗号化されたバケットからコピーされた場合、KMS キー値には両方のバケットのキーを含める必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`のようになります。

    6.  **「次へ」**をクリックしてください。

    7.  ポリシー名を設定し、ポリシーのタグを追加（任意）してから、 **「ポリシーの作成」を**クリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  [IAMコンソール](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインの**[ロール]**をクリックし、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  役割を作成するには、以下の情報を入力してください。

        -   **「信頼済みエンティティタイプ」**で**「AWSアカウント」**を選択します。
        -   **「AWSアカウント」**で**「別のAWSアカウント」**を選択し、 TiDB CloudアカウントIDを**「アカウントID」**フィールドに貼り付けます。
        -   **[オプション]**で、 **[外部 ID が必要 (サードパーティがこの役割を引き受ける場合のベスト プラクティス)]**をクリックし、 TiDB Cloud外部 ID を**[外部 ID]**フィールドに貼り付けます。<CustomContent plan="starter,essential">ロールが外部IDを必須とせずに作成された場合、プロジェクト内のいずれかのTiDB Cloud StarterまたはEssentialインスタンスの設定が完了すると、そのプロジェクト内のすべてのTiDB Cloud StarterおよびEssentialインスタンスは同じロールARNを使用してAmazon S3バケットにアクセスできます。ロールがアカウントIDと外部IDの両方を使用して作成された場合、対応するTiDB Cloud StarterまたはEssentialインスタンスのみがバケットにアクセスできます。</CustomContent>

    3.  **「次へ」**をクリックしてポリシー一覧を開き、先ほど作成したポリシーを選択してから**「次へ」**をクリックします。

    4.  **「役割の詳細」**で役割の名前を設定し、右下隅の**「役割の作成」**をクリックします。役割が作成されると、役割の一覧が表示されます。

    5.  役割の一覧から、先ほど作成した役割の名前をクリックして概要ページに移動すると、役割のARNを取得できます。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### AWSアクセスキーを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成する際には、AWSアカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセスキーを設定するには、以下の手順に従ってください。

1.  IAMユーザーを作成します。詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWSアカウントIDまたはアカウントエイリアス、およびIAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインしてください。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

> **注記：**
>
> TiDB Cloudはアクセス キーを保存しません。インポートまたはエクスポートが完了したら[アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)ことをお勧めします。

<CustomContent plan="starter,essential">

## GCSへのアクセスを設定する {#configure-gcs-access}

TiDB Cloud StarterまたはEssentialインスタンスがGCSバケットにアクセスできるようにするには、バケットのGCSアクセスを設定する必要があります。サービスアカウントキーを使用してバケットアクセスを設定できます。

サービスアカウントキーを設定するには、以下の手順に従ってください。

1.  Google Cloud サービス[サービスアカウントページ](https://console.cloud.google.com/iam-admin/serviceaccounts)ページで、 **[サービス アカウントの作成]**をクリックしてサービス アカウントを作成します。詳細については、 [サービスアカウントの作成](https://cloud.google.com/iam/docs/creating-managing-service-accounts)参照してください。

    1.  サービスアカウント名を入力してください。

    2.  任意：サービスアカウントの説明を入力してください。

    3.  サービスアカウントを作成するには、 **「作成して続行」**をクリックしてください。

    4.  `Grant this service account access to project`で、必要な権限を持つ[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)を選択します。

        -   TiDB Cloud StarterまたはEssentialインスタンスからデータをエクスポートするには`storage.objects.create`権限を持つロールが必要です。
        -   TiDB Cloud StarterまたはEssentialインスタンスにデータをインポートするには`storage.buckets.get` 、 `storage.objects.get` 、および`storage.objects.list`権限を持つロールが必要です。

    5.  次のステップに進むには、 **「続行」**をクリックしてください。

    6.  オプション: `Grant users access to this service account`で、 [サービスアカウントを他のリソースにアタッチする](https://cloud.google.com/iam/docs/attach-service-accounts)必要があるメンバーを選択します。

    7.  **「完了」**をクリックして、サービスアカウントの作成を完了してください。

    ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2.  サービスアカウントをクリックし、 `KEYS`ページで**[キーの追加]**をクリックして、サービスアカウントキーを作成します。

    ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3.  デフォルトのキータイプ`JSON`を選択し、 **[作成]**をクリックして Google Cloud 認証情報ファイルをダウンロードします。このファイルには、TiDB Cloud StarterまたはEssentialインスタンスの GCS アクセスを設定する際に使用する必要のあるサービス アカウント キーが含まれています。

</CustomContent>

<CustomContent plan="starter,essential,premium">

## Azure Blob Storageへのアクセスを構成する {#configure-azure-blob-storage-access}

TiDB CloudがAzure Blobコンテナにアクセスできるようにするには、コンテナ用のサービスSASトークンを作成する必要があります。

SAS トークンは、 [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)(推奨) または手動構成を使用して作成できます。

Azure ARMテンプレートを使用してSASトークンを作成するには、次の手順を実行します。

1.  対象のTiDB Cloudリソースの**インポート**または**エクスポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    2.  対象のTiDB Cloudリソースの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート**」または**「データ」** &gt; **「エクスポート」**をクリックします。

2.  **「ARMテンプレート展開による新しいSASトークンの生成」**ダイアログを開きます。

    -   Azure Blob Storage からデータをインポートする場合：

        1.  **「Azure Blob Storage からインポート」を**クリックします。
        2.  **フォルダURI**欄に入力してください。
        3.  **SASトークン**フィールドで、 **[Azure ARMテンプレートを使用して新しいトークンを作成するには、ここをクリックしてください]をクリックします**。

    <CustomContent plan="starter,essential">

    -   データをAzure Blob Storageにエクスポートする場合：

        1.  **「データのエクスポート先...」** &gt; **「Azure Blob Storage」**をクリックします。TiDB Cloud StarterまたはEssentialインスタンスでこれまでデータのインポートまたはエクスポートが行われていない場合は、ページ下部の**「データのエクスポート先...」** &gt; **「Azure Blob Storage」を**クリックしてください。
        2.  **Azure Blob Storage 設定**エリアまでスクロールダウンし、SAS トークンフィールドの下にある**[ここをクリックして、Azure ARM テンプレートを使用して新しいものを作成する] をクリックします**。

    </CustomContent>

    <CustomContent plan="premium">

    -   データをAzure Blob Storageにエクスポートする場合：

        1.  **「データのエクスポート」を**クリックします。
        2.  **ターゲット接続**で**Azure Blob Storageを**選択してください。
        3.  SASトークンフィールドの下にある**「ここをクリックして、Azure ARMテンプレートを使用して新しいものを作成してください」をクリックしてください**。

    </CustomContent>

3.  Azure ARMテンプレートを使用してSASトークンを作成します。

    1.  **「ARM テンプレート展開による新しい SAS トークンの生成」**ダイアログで、[クリック**] をクリックして、事前構成済みの ARM テンプレートを含む Azure ポータルを開きます**。

    2.  Azureにログインすると、Azure**カスタムデプロイ**ページにリダイレクトされます。

    3.  **カスタムデプロイメント**ページで、**リソースグループ**と**ストレージアカウント名**を入力してください。コンテナが配置されているstorageアカウントの概要ページから、すべての情報を取得できます。

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4.  デプロイメントを確認するには、 **「レビュー + 作成」**または**「次へ」**をクリックします。デプロイメントを開始するには、 **「作成」**をクリックします。

    5.  処理が完了すると、デプロイメント概要ページにリダイレクトされます。 **「出力」**セクションに移動して、SASトークンを取得してください。

Azure ARMテンプレートを使用してSASトークンを作成する際に問題が発生した場合は、以下の手順に従って手動で作成してください。

<details><summary>詳細はこちらをクリックしてください</summary>

1.  [Azureストレージアカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するstorageアカウントをクリックします。

2.  **ストレージアカウントの**ページで、[**Security]+ [ネットワーク]**をクリックし、 **[共有アクセス署名]**をクリックします。

    ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3.  **[共有アクセス署名]**ページで、次のように必要なアクセス許可を持つサービス SAS トークンを作成します。詳細については、 [サービスSASトークンを作成します](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)参照してください。

    1.  **「許可されたサービス」**セクションで、 **「Blob」**サービスを選択します。

    2.  **「許可されたリソースの種類」**セクションで、 **「コンテナ」**と**「オブジェクト」**を選択します。

    3.  **「許可された権限」**セクションで、必要に応じて権限を選択してください。

        -   TiDB Cloud StarterまたはEssentialインスタンスからデータをエクスポートするには、**読み取り**権限と**書き込み**権限が必要です。
        -   TiDB Cloud StarterまたはEssentialインスタンスにデータをインポートするには、**読み取り**権限と**一覧表示**権限が必要です。

    4.  必要に応じて**開始日時と終了日時**を調整してください。

    5.  その他の設定については、デフォルト値をそのまま使用できます。

    ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4.  SASトークンを生成するには、 **「SASと接続文字列の生成」を**クリックしてください。

</details>

</CustomContent>

## Alibaba Cloudオブジェクトストレージサービス（OSS）へのアクセスを設定する {#configure-alibaba-cloud-object-storage-service-oss-access}

TiDB CloudがAlibaba Cloud OSSバケットにアクセスできるようにするには、そのバケットのアクセスキーペアを作成する必要があります。

アクセスキーペアを設定するには、以下の手順に従ってください。

1.  RAM ユーザーを作成し、AccessKey ペアを取得します。詳細については、 [RAMユーザーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)参照してください。

    **アクセスモードの**セクションで、 **「永続的なアクセスキーを使用してアクセスする」を**選択します。

2.  必要な権限を持つカスタム ポリシーを作成します。詳細については、 [カスタムポリシーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)参照してください。

    -   **「効果」**セクションで**「許可」**を選択します。

    -   「**サービス」**セクションで、 **「オブジェクトストレージサービス」**を選択します。

    -   「**アクション」**セクションで、必要に応じて権限を選択してください。

        <CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスにデータをインポートするには、 **oss:GetObject** 、 **oss:GetBucketInfo** 、および**oss:ListObjects**権限を付与します。

        <CustomContent plan="starter,essential">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスからデータをエクスポートするには、 `oss:PutObject`および`oss:GetBucketInfo`権限を付与してください。

    -   **リソース**セクションで、バケットとバケット内のオブジェクトを選択します。

3.  カスタム ポリシーを RAM ユーザーにアタッチします。詳細については、 [RAMユーザーに権限を付与する](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)参照してください。
