---
title: Configure External Storage Access for TiDB Cloud Dedicated
summary: Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、およびAzure Blob Storageへのアクセス設定方法を学びましょう。
aliases: ['/ja/tidb-cloud/config-s3-and-gcs-access']
---

# TiDB Cloud Dedicatedの外部ストレージアクセスを構成する {#configure-external-storage-access-for-tidb-cloud-dedicated}

ソースデータがAmazon S3バケット、Azure Blob Storageコンテナ、またはGoogle Cloud Storage（GCS）バケットに保存されている場合、データをTiDB Cloudにインポートまたは移行する前に、バケットへのクロスアカウントアクセスを設定する必要があります。このドキュメントでは、TiDB Cloud Dedicatedクラスターでこの設定を行う方法について説明します。

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud StarterまたはEssentialの外部ストレージアクセスを設定する](/tidb-cloud/configure-external-storage-access.md)を参照してください。

## Amazon S3へのアクセスを設定する {#configure-amazon-s3-access}

TiDB Cloud Dedicatedクラスターが Amazon S3 バケット内のソースデータにアクセスできるようにするには、以下のいずれかの方法を使用してクラスターのバケットアクセスを設定します。

-   [ロールARNを使用する](#configure-amazon-s3-access-using-a-role-arn)(推奨): ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   [AWSアクセスキーを使用する](#configure-amazon-s3-access-using-an-aws-access-key): IAMユーザーのアクセスキーを使用して、Amazon S3 バケットにアクセスします。

### ロールARNを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-a-role-arn}

TiDB Cloudのバケットアクセスを設定し、以下の手順でロールARNを取得します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、対象の TiDB クラスターに対応するTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

    3.  **「クラウドストレージからデータをインポート」**をクリックします。

    4.  **「クラウドストレージからデータをインポート」**ページで、**ストレージプロバイダーを****「Amazon S3」**に設定し、 **「認証情報**」で**「AWS ロール ARN」**が選択されていることを確認してから、 **「ロール ARN」**フィールドの下にある**「ここをクリックして AWS CloudFormation で新しいロール ARN を作成」をクリックします**。 **「新しいロール ARN を追加」**ダイアログが表示されます。

    5.  **問題が発生しましたか？ロールARNを手動で作成して**、このクラスターの**TiDB CloudアカウントID**と**TiDB Cloud外部ID**を取得してください。これらのIDは後で使用するため、メモしておいてください。

2.  AWS マネジメントコンソールで、Amazon S3 バケット用のマネージドポリシーを作成します。

    1.  AWS マネジメント コンソールにサインインし、 [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で Amazon S3 コンソールを開きます。

    2.  **バケット**一覧から、ソースデータが入っているバケットの名前を選択し、 **「ARNをコピー」**をクリックしてS3バケットのARNを取得します（例： `arn:aws:s3:::tidb-cloud-source-data` ）。後で使用するために、バケットのARNをメモしておいてください。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーション ペインで**[ポリシー]**をクリックし、 **[ポリシーの作成] を**クリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **ポリシー作成**ページで、 **「JSON」**タブをクリックします。

    5.  以下のアクセス ポリシー テンプレートをコピーして、ポリシー テキスト フィールドに貼り付けてください。

        ````json
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

        In the policy text field, update the following configurations to your own values.

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            For example, if your source data is stored in the root directory of the `tidb-cloud-source-data` bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`. If your source data is stored in the `mydata` directory of the bucket, use `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`. Make sure that `/*` is added to the end of the directory so TiDB Cloud can access all files in this directory.

        - `"Resource": "<Your S3 bucket ARN>"`

            For example, `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`.

        - If you have enabled AWS Key Management Service key (SSE-KMS) with customer-managed key encryption, make sure the following configuration is included in the policy. `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` is a sample KMS key of the bucket.

            ```json
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

            If the objects in your bucket have been copied from another encrypted bucket, the KMS key value needs to include the keys of both buckets. For example, `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`.

        ````

    6.  **「次へ」**をクリックしてください。

    7.  ポリシー名を設定し、ポリシーのタグを追加（任意）してから、 **「ポリシーの作成」を**クリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)のIAMコンソールで、左側のナビゲーション ペインの**[ロール]**をクリックし、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  役割を作成するには、以下の情報を入力してください。

        -   **「信頼できるエンティティの種類」**で**「AWS アカウント」**を選択します。
        -   **「AWSアカウント」**の下にある**「別のAWSアカウント」**を選択し、 TiDB CloudアカウントIDを**「アカウントID」**フィールドに貼り付けます。
        -   **「オプション」**で**「外部IDを必須にする」**をクリックして[混乱した副官の問題](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)回避し、 TiDB Cloud外部IDを「**外部ID」**フィールドに貼り付けます。「外部IDを必須にする」を選択せず​​にロールを作成すると、S3バケットURIとIAMロールARNを持つユーザーであれば誰でもAmazon S3バケットにアクセスできる可能性があります。アカウントIDと外部IDの両方を使用してロールを作成すると、同じプロジェクトおよび同じリージョンで実行されているTiDBクラスタのみがバケットにアクセスできます。

    3.  **「次へ」**をクリックしてポリシー一覧を開き、先ほど作成したポリシーを選択してから**「次へ」**をクリックします。

    4.  **「役割の詳細」**で役割の名前を設定し、右下隅の**「役割の作成」**をクリックします。役割が作成されると、役割の一覧が表示されます。

    5.  役割の一覧から、先ほど作成した役割の名前をクリックして概要ページに移動し、役割のARNをコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、 TiDB CloudアカウントIDと外部IDを取得する**データインポート**ページに移動し、ロールARNを**ロールARN**フィールドに貼り付けます。

### AWSアクセスキーを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成する際には、AWSアカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセスキーを設定するには、以下の手順に従ってください。

1.  以下のポリシーを持つIAMユーザーを作成します。

    -   `AmazonS3ReadOnlyAccess`
    -   [`CreateOwnAccessKeys` （必須）および`ManageOwnAccessKeys` （オプション）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

    これらのポリシーは、ソースデータが保存されているバケットにのみ適用されるようにすることをお勧めします。

    詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWSアカウントIDまたはアカウントエイリアス、およびIAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインしてください。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

> **注記：**
>
> TiDB Cloudはアクセス キーを保存しません。インポートが完了したら、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)ことをお勧めします。

## GCSへのアクセスを設定する {#configure-gcs-access}

TiDB CloudがGCSバケット内のソースデータにアクセスできるようにするには、バケットのGCSアクセスを設定する必要があります。プロジェクト内の1つのTiDBクラスタの設定が完了すると、そのプロジェクト内のすべてのTiDBクラスタがGCSバケットにアクセスできるようになります。

1.  TiDB Cloudコンソールで、対象のTiDBクラスターのGoogle CloudサービスアカウントIDを取得します。

    1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

    3.  **「クラウドストレージからデータをインポート」**をクリックします。

    4.  **「クラウドストレージからデータをインポート」**ページで、 **「ストレージプロバイダー」を****「Google Cloud Storage」**に設定し、後で使用するためにGoogle CloudサービスアカウントIDをコピーしてください。

2.  Google Cloud コンソールで、GCS バケット用のIAMロールを作成します。

    1.  [Google Cloud Console](https://console.cloud.google.com/)にサインインしてください。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、「役割**の作成」**をクリックしてください。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3.  役割の名前、説明、ID、および役割の起動ステージを入力してください。役割名は、作成後に変更することはできません。

    4.  **「権限を追加」を**クリックしてください。

    5.  ロールに以下の読み取り専用権限を追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.get
        -   storage.オブジェクトリスト

        権限名をフィルタークエリとして**「プロパティ名または値を入力」**フィールドにコピーし、フィルター結果からその名前を選択できます。3つの権限を追加するには、権限名の間に**OR演算子**を使用します。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB CloudがアクセスするGCSバケットの名前をクリックします。

4.  **バケットの詳細**ページで、 **[権限]**タブをクリックし、 **[アクセス権の付与]**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5.  バケットへのアクセス権を付与するには、以下の情報を入力し、 **「保存」**をクリックしてください。

    -   **「新しいプリンシパル」**フィールドに、対象のTiDBクラスターのGoogle Cloud ServiceアカウントIDを貼り付けます。

    -   **「役割を選択」ドロップ**ダウンリストに、先ほど作成したIAMロールの名前を入力し、フィルター結果からその名前を選択します。

    > **注記：**
    >
    > TiDB Cloudへのアクセス権を削除するには、付与したアクセス権を削除するだけで済みます。

6.  **バケットの詳細**ページで、「**オブジェクト」**タブをクリックします。

    ファイルの gsutil URI をコピーするには、ファイルを選択し、 **[オブジェクトを開く] オーバーフロー メニュー**をクリックして、 **[gsutil URI をコピー] を**クリックします。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    フォルダのgsutil URIを使用する場合は、フォルダを開き、フォルダ名の横にあるコピーボタンをクリックしてフォルダ名をコピーします。その後、フォルダ名の先頭に`gs://` 、末尾に`/`を追加して、フォルダの正しいURIを取得する必要があります。

    例えば、フォルダ名が`tidb-cloud-source-data`の場合、URI としては`gs://tidb-cloud-source-data/`を使用する必要があります。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7.  TiDB Cloudコンソールで、Google Cloud Service アカウント ID を取得する**データインポート**ページに移動し、GCS バケットの gsutil URI を**バケット gsutil URI**フィールドに貼り付けます。たとえば、 `gs://tidb-cloud-source-data/`を貼り付けます。

## Azure Blob Storageへのアクセスを構成する {#configure-azure-blob-storage-access}

TiDB Cloud DedicatedがAzure Blobコンテナにアクセスできるようにするには、コンテナのAzure Blobアクセスを設定する必要があります。アカウントSASトークンを使用してコンテナアクセスを設定できます。

1.  [Azureストレージアカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するstorageアカウントをクリックします。

2.  storageアカウントのナビゲーション ペインで、 **[Security+ ネットワーク]** &gt; **[共有アクセス 署名]**をクリックします。

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3.  **[共有アクセス署名]**ページで、次のように必要な権限を持つ[アカウントSASトークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)を作成します。

    1.  **「許可されたサービス」**で**「Blob」**を選択します。
    2.  **「許可されるリソースの種類」**で、 **「コンテナ」**と**「オブジェクト」**を選択します。
    3.  **「許可された権限」**で、必要な権限を選択します。たとえば、 TiDB Cloud Dedicatedにデータをインポートするには、 **「読み取り」**と**「一覧表示」の**権限が必要です。
    4.  必要に応じて**開始日時と有効期限日時**を調整してください。セキュリティ上の理由から、有効期限はデータインポートのスケジュールに合わせて設定することをお勧めします。
    5.  その他の設定については、デフォルト値を維持してください。

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4.  SASトークンを生成するには、 **「SASと接続文字列の生成」を**クリックしてください。

5.  生成された**SASトークン**をコピーしてください。このトークン文字列は、TiDB Cloudでデータインポートを設定する際に必要になります。

> **注記：**
>
> データインポートを開始する前に、接続とアクセス許可をテストして、 TiDB Cloud Dedicatedが指定されたAzure Blobコンテナとファイルにアクセスできることを確認してください。
