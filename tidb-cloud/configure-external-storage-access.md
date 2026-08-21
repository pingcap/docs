---
title: Configure External Storage Access
summary: Amazon Simple Storage Service (Amazon S3) などの外部ストレージへのクロスアカウントアクセスを設定する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-external-storage']
---

# 外部ストレージへのアクセスを構成する {#configure-external-storage-access}

TiDB Cloud Starter、 Essential 、またはPremiumインスタンスで外部ストレージからデータをインポートしたり、外部ストレージにデータをエクスポートしたりするには、アカウント間アクセスを設定する必要があります。このドキュメントでは、TiDB Cloud Starter、 TiDB Cloud Essential、およびTiDB Cloud Premiumインスタンスで外部ストレージへのアクセスを設定する方法について説明します。

TiDB Cloud Dedicatedクラスター用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud Dedicatedの外部ストレージアクセスを構成する](/tidb-cloud/dedicated-external-storage.md)を参照してください。

## Amazon S3へのアクセスを設定する {#configure-amazon-s3-access}

TiDB Cloud Starter、 Essential、またはPremiumインスタンスがAmazon S3バケットにアクセスできるようにするには、以下のいずれかの方法を使用して、インスタンスのバケットアクセスを設定します。

-   [ロールARNを使用する](#configure-amazon-s3-access-using-a-role-arn): ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   [AWSアクセスキーを使用する](#configure-amazon-s3-access-using-an-aws-access-key): IAMユーザーのアクセスキーを使用して、Amazon S3 バケットにアクセスします。

### ロールARNを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-a-role-arn}

ロールARNの作成には[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)を使用することをお勧めします。作成するには、以下の手順に従ってください。

> **Note:**
>
> Amazon S3 へのロール ARN アクセスは、ターゲットTiDB Cloud Starter、 Essential、または Premium インスタンスのクラウドプロバイダーが AWS である場合にのみサポートされます。別のクラウドプロバイダーを使用する場合は、代わりに AWS アクセスキーを使用してください。詳細については、 [AWSアクセスキーを使用してAmazon S3へのアクセスを設定する](#configure-amazon-s3-access-using-an-aws-access-key)を参照してください。

1.  対象のTiDB Cloud Starter、 Essential、またはPremiumインスタンスの**Import**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。
    2.  対象のTiDB Cloud Starter、 Essential、または Premium インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**Data** &gt; **Import**をクリックします。

2.  **Add New ARN**ダイアログを開きます。

    -   Amazon S3からデータをインポートする場合は、次のようにして**Add New ARN**ダイアログを開きます。

        1.  **Import from S3**をクリックします。
        2.  **File URI**欄に入力してください。
        3.  **AWS Role ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    <CustomContent plan="starter,essential">

    -   データをAmazon S3にエクスポートする場合は、次のように**Add New ARN**ダイアログを開きます。

        1.  **Export data to...** &gt; **Amazon S3**をクリックします。TiDB Cloud StarterまたはEssentialインスタンスでこれまでデータのインポートまたはエクスポートが行われていない場合は、ページ下部の**Click here to export data to...** &gt; **Amazon S3**をクリックしてください。
        2.  **Folder URI**欄に入力してください。
        3.  **AWS Role ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    </CustomContent>

    <CustomContent plan="premium">

    -   データをAmazon S3にエクスポートする場合は、次のように**Add New ARN**ダイアログを開きます。

        1.  **Export Data**をクリックします。
        2.  **Target Connection**で**Amazon S3**を選択してください。
        3.  **Folder URI**欄に入力してください。
        4.  **AWS Role ARN**を選択し、[**ここをクリックして AWS CloudFormation を使用して新しいロールを作成します] をクリックします**。

    </CustomContent>

3.  AWS CloudFormationテンプレートを使用してロールARNを作成します。

    1.  **Add New ARN**ダイアログで、 **AWS Console with CloudFormation Template**をクリックします。

    2.  [AWS マネジメントコンソール](https://console.aws.amazon.com)コンソールにログインすると、AWS CloudFormation の**Quick create stack**ページにリダイレクトされます。

    3.  **Role Name**を入力してください。

    4.  新しいロールを作成することに同意し、 **Create stack**をクリックしてロールARNを作成します。

    5.  CloudFormationスタックの実行後、 **Outputs**タブをクリックすると、 **Value**列にロールARNの値が表示されます。

        ![Role ARN](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

AWS CloudFormationでロールARNを作成する際に問題が発生した場合は、以下の手順で手動で作成できます。

<details><summary>詳細はこちらをクリックしてください</summary>

1.  前の手順で説明した**Add New ARN**ダイアログで、 **Having trouble? Create Role ARN manually**をクリックします。**TiDB Cloud Account ID**と**TiDB Cloud External ID**が取得されます。

2.  AWS マネジメントコンソールで、Amazon S3 バケット用のマネージドポリシーを作成します。

    1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)コンソールにサインインし、 [Amazon S3コンソール](https://console.aws.amazon.com/s3/)を開きます。

    2.  **バケット**一覧から対象バケットの名前を選択し、 **Copy ARN**をクリックしてS3バケットのARNを取得します（例： `arn:aws:s3:::tidb-cloud-source-data` ）。後で使用するために、バケットのARNをメモしておいてください。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [IAMコンソール](https://console.aws.amazon.com/iam/)を開き、左側のナビゲーションペインで**Policies**をクリックし、 **Create Policy**をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **Create policy**ページで、 **JSON**タブをクリックします。

    5.  ポリシーテキストフィールドで、必要に応じてポリシーを設定してください。以下は、 TiDB Cloud Starter、 Essential、またはPremiumインスタンスからデータをエクスポートしたり、これらのインスタンスにデータをインポートしたりする際に使用できる例です。

        -   TiDB Cloud Starter、 Essential、またはPremiumインスタンスからデータをエクスポートするには**、s3:PutObject**および**s3:ListBucketの**権限が必要です。
        -   TiDB Cloud Starter、 Essential、またはPremiumインスタンスにデータをインポートするには**、s3:GetObject** 、 **s3:GetObjectVersion** 、および**s3:ListBucketの**権限が必要です。

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

        -   バケット内のオブジェクトが別の暗号化されたバケットからコピーされた場合、KMS キー値には両方のバケットのキーを含める必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`のようになります。

    6.  **Next**をクリックしてください。

    7.  ポリシー名を設定し、ポリシーのタグを追加（任意）してから、 **Create policy**をクリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  [IAMコンソール](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインの**Roles**をクリックし、 **Create role**をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  役割を作成するには、以下の情報を入力してください。

        -   **Trusted entity type**で**AWS account**を選択します。
        -   **An AWS account**で**Another AWS account**を選択し、 TiDB CloudアカウントIDを**Account ID**フィールドに貼り付けます。
        -   **[オプション]**で、 **[外部 ID が必要 (サードパーティがこの役割を引き受ける場合のベスト プラクティス)]**をクリックし、 TiDB Cloud外部 ID を**External ID**フィールドに貼り付けます。<CustomContent plan="starter,essential">ロールが外部IDを必須とせずに作成された場合、プロジェクト内のいずれかのTiDB Cloud StarterまたはEssentialインスタンスの設定が完了すると、そのプロジェクト内のすべてのTiDB Cloud StarterおよびEssentialインスタンスは同じロールARNを使用してAmazon S3バケットにアクセスできます。ロールがアカウントIDと外部IDの両方を使用して作成された場合、対応するTiDB Cloud StarterまたはEssentialインスタンスのみがバケットにアクセスできます。</CustomContent>

    3.  **Next**をクリックしてポリシー一覧を開き、先ほど作成したポリシーを選択してから**Next**をクリックします。

    4.  **Role details**で役割の名前を設定し、右下隅の**Create role**をクリックします。役割が作成されると、役割の一覧が表示されます。

    5.  役割の一覧から、先ほど作成した役割の名前をクリックして概要ページに移動すると、役割のARNを取得できます。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### AWSアクセスキーを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成する際には、AWSアカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセスキーを設定するには、以下の手順に従ってください。

1.  IAMユーザーを作成します。詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)を参照してください。

2.  AWSアカウントIDまたはアカウントエイリアス、およびIAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインしてください。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)を参照してください。

> **Note:**
>
> TiDB Cloudはアクセス キーを保存しません。インポートまたはエクスポートが完了したら[アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)ことをお勧めします。

<CustomContent plan="starter,essential">

## GCSへのアクセスを設定する {#configure-gcs-access}

TiDB Cloud StarterまたはEssentialインスタンスがGCSバケットにアクセスできるようにするには、バケットのGCSアクセスを設定する必要があります。サービスアカウントキーを使用してバケットアクセスを設定できます。

サービスアカウントキーを設定するには、以下の手順に従ってください。

1.  Google Cloud サービス[サービスアカウントページ](https://console.cloud.google.com/iam-admin/serviceaccounts)ページで、 **CREATE SERVICE ACCOUNT**をクリックしてサービス アカウントを作成します。詳細については、 [サービスアカウントの作成](https://cloud.google.com/iam/docs/creating-managing-service-accounts)を参照してください。

    1.  サービスアカウント名を入力してください。

    2.  任意：サービスアカウントの説明を入力してください。

    3.  サービスアカウントを作成するには、 **CREATE AND CONTINUE**をクリックしてください。

    4.  `Grant this service account access to project`で、必要な権限を持つ[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)を選択します。

        -   TiDB Cloud StarterまたはEssentialインスタンスからデータをエクスポートするには`storage.objects.create`権限を持つロールが必要です。
        -   TiDB Cloud StarterまたはEssentialインスタンスにデータをインポートするには`storage.buckets.get` 、 `storage.objects.get` 、および`storage.objects.list`権限を持つロールが必要です。

    5.  次のステップに進むには、 **Continue**をクリックしてください。

    6.  オプション: `Grant users access to this service account`で、 [サービスアカウントを他のリソースにアタッチする](https://cloud.google.com/iam/docs/attach-service-accounts)必要があるメンバーを選択します。

    7.  **Done**をクリックして、サービスアカウントの作成を完了してください。

    ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2.  サービスアカウントをクリックし、 `KEYS`ページで**ADD KEY**をクリックして、サービスアカウントキーを作成します。

    ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3.  デフォルトのキータイプ`JSON`を選択し、 **[作成]**をクリックして Google Cloud 認証情報ファイルをダウンロードします。このファイルには、TiDB Cloud StarterまたはEssentialインスタンスの GCS アクセスを設定する際に使用する必要のあるサービス アカウント キーが含まれています。

</CustomContent>

<CustomContent plan="starter,essential,premium">

## Azure Blob Storageへのアクセスを構成する {#configure-azure-blob-storage-access}

TiDB CloudがAzure Blobコンテナにアクセスできるようにするには、コンテナ用のサービスSASトークンを作成する必要があります。

SAS トークンは、 [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)(推奨) または手動構成を使用して作成できます。

Azure ARMテンプレートを使用してSASトークンを作成するには、次の手順を実行します。

1.  対象のTiDB Cloudリソースの**Import**または**Export**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    2.  対象のTiDB Cloudリソースの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Data** &gt; **Import**または**Data** &gt; **Export**をクリックします。

2.  **Generate New SAS Token via ARM Template Deployment**ダイアログを開きます。

    -   Azure Blob Storage からデータをインポートする場合：

        1.  **Import from Azure Blob Storage**をクリックします。
        2.  **Folder URI**欄に入力してください。
        3.  **SAS Token**フィールドで、 **Click here to create a new one with Azure ARM template**をクリックします。

    <CustomContent plan="starter,essential">

    -   データをAzure Blob Storageにエクスポートする場合：

        1.  **Export data to...** &gt; **Azure Blob Storage**をクリックします。TiDB Cloud StarterまたはEssentialインスタンスでこれまでデータのインポートまたはエクスポートが行われていない場合は、ページ下部の**Click here to export data to...** &gt; **Azure Blob Storage**をクリックしてください。
        2.  **Azure Blob Storage Settings**エリアまでスクロールダウンし、SASトークンフィールドの下にある**Click here to create a new one with Azure ARM template**をクリックします。

    </CustomContent>

    <CustomContent plan="premium">

    -   データをAzure Blob Storageにエクスポートする場合：

        1.  **Export Data**をクリックします。
        2.  **Target Connection**で**Azure Blob Storage**を選択してください。
        3.  SASトークンフィールドの下にある**Click here to create a new one with Azure ARM template**をクリックしてください。

    </CustomContent>

3.  Azure ARMテンプレートを使用してSASトークンを作成します。

    1.  **Generate New SAS Token via ARM Template Deployment**ダイアログで、 **Click to open the Azure Portal with the pre-configured ARM template**をクリックします。

    2.  Azureにログインすると、Azure**Custom deployment**ページにリダイレクトされます。

    3.  **Resource group**ページで、**リソースグループ**と**ストレージアカウント名**を入力してください。コンテナが配置されているストレージアカウントの概要ページから、すべての情報を取得できます。

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4.  デプロイメントを確認するには、 **Review + create**または**Next**をクリックします。デプロイメントを開始するには、 **Create**をクリックします。

    5.  処理が完了すると、デプロイメント概要ページにリダイレクトされます。 **Outputs**セクションに移動して、SASトークンを取得してください。

Azure ARMテンプレートを使用してSASトークンを作成する際に問題が発生した場合は、以下の手順に従って手動で作成してください。

<details><summary>詳細はこちらをクリックしてください</summary>

1.  [Azureストレージアカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するストレージアカウントをクリックします。

2.  **Storage account**ページで、**[セキュリティ + ネットワーク]**をクリックし、 **Shared access signature**をクリックします。

    ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3.  **Shared access signature**ページで、次のように必要なアクセス許可を持つサービス SAS トークンを作成します。詳細については、 [サービスSASトークンを作成します](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)を参照してください。

    1.  **Allowed services**セクションで、 **Blob**サービスを選択します。

    2.  **Allowed Resource types**セクションで、 **Container**と**Object**を選択します。

    3.  **Allowed permissions**セクションで、必要に応じて権限を選択してください。

        -   TiDB Cloud StarterまたはEssentialインスタンスからデータをエクスポートするには、**Read**権限と**Write**権限が必要です。
        -   TiDB Cloud StarterまたはEssentialインスタンスにデータをインポートするには、**Read**権限と**一覧表示**権限が必要です。

    4.  必要に応じて**Start and expiry date/time**を調整してください。

    5.  その他の設定については、デフォルト値をそのまま使用できます。

    ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4.  SASトークンを生成するには、 **Generate SAS and connection string**をクリックしてください。

</details>

</CustomContent>

## Alibaba Cloudオブジェクトストレージサービス（OSS）へのアクセスを設定する {#configure-alibaba-cloud-object-storage-service-oss-access}

TiDB CloudがAlibaba Cloud OSSバケットにアクセスできるようにするには、そのバケットのアクセスキーペアを作成する必要があります。

アクセスキーペアを設定するには、以下の手順に従ってください。

1.  RAM ユーザーを作成し、AccessKey ペアを取得します。詳細については、 [RAMユーザーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)を参照してください。

    **Access Mode**セクションで、 **Using permanent AccessKey to access**を選択します。

2.  必要な権限を持つカスタム ポリシーを作成します。詳細については、 [カスタムポリシーを作成する](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)を参照してください。

    -   **Effect**セクションで**Allow**を選択します。

    -   **Service**セクションで、 **Object Storage Service**を選択します。

    -   **Action**セクションで、必要に応じて権限を選択してください。

        TiDB Cloud Starter、 Essential、またはPremiumインスタンスにデータをインポートするには、 **oss:GetObject** 、 **oss:GetBucketInfo** 、および**oss:ListObjectsの**権限を付与してください。

        TiDB Cloud Starter、 Essential、またはPremiumインスタンスからデータをエクスポートするには、 `oss:PutObject`と`oss:GetBucketInfo`の権限を付与してください。

    -   **Resource**セクションで、バケットとバケット内のオブジェクトを選択します。

3.  カスタム ポリシーを RAM ユーザーにアタッチします。詳細については、 [RAMユーザーに権限を付与する](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)を参照してください。
