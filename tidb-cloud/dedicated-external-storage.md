---
title: Configure External Storage Access for TiDB Cloud Dedicated
summary: Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、Azure Blob Storage アクセスを構成する方法を学習します。
aliases: ['/tidb-cloud/config-s3-and-gcs-access']
---

# TiDB Cloud Dedicatedの外部ストレージアクセスを構成する {#configure-external-storage-access-for-tidb-cloud-dedicated}

ソースデータがAmazon S3バケット、Azure Blob Storageコンテナ、またはGoogle Cloud Storage（GCS）バケットに保存されている場合、 TiDB Cloudにデータをインポートまたは移行する前に、バケットへのクロスアカウントアクセスを設定する必要があります。このドキュメントでは、 TiDB Cloud Dedicatedクラスターでこれを行う方法について説明します。

TiDB Cloud Serverless クラスター用にこれらの外部ストレージを構成する必要がある場合は、 [TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/serverless-external-storage.md)参照してください。

## Amazon S3 アクセスを構成する {#configure-amazon-s3-access}

TiDB Cloud Dedicated クラスターが Amazon S3 バケット内のソースデータにアクセスできるようにするには、次のいずれかの方法を使用してクラスターのバケットアクセスを設定します。

-   [ロールARNを使用する](#configure-amazon-s3-access-using-a-role-arn) (推奨): ロール ARN を使用して Amazon S3 バケットにアクセスします。
-   [AWSアクセスキーを使用する](#configure-amazon-s3-access-using-an-aws-access-key) : IAMユーザーのアクセスキーを使用して Amazon S3 バケットにアクセスします。

### ロール ARN を使用して Amazon S3 アクセスを構成する {#configure-amazon-s3-access-using-a-role-arn}

次のように、 TiDB Cloudのバケット アクセスを設定し、ロール ARN を取得します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、対象の TiDB クラスターの対応するTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

    3.  **「Cloud Storage からデータをインポート」**を選択し、 **「Amazon S3」**をクリックします。

    4.  **Amazon S3からデータをインポートする**ページで、 **「ロールARN」**の下のリンクをクリックします。 **「新しいロールARNを追加」**ダイアログが表示されます。

    5.  **「ロールARNの作成」を手動で**展開し、 TiDB CloudアカウントIDとTiDB Cloud外部IDを取得します。これらのIDは後で使用するため、メモしておいてください。

2.  AWS マネジメントコンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  AWS マネジメントコンソールにサインインし、 [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で Amazon S3 コンソールを開きます。

    2.  **「バケット」**リストで、ソースデータがあるバケットの名前を選択し、 **「ARNをコピー」**をクリックしてS3バケットのARN（例： `arn:aws:s3:::tidb-cloud-source-data` ）を取得します。後で使用するために、バケットのARNをメモしておいてください。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーション ペインで**[ポリシー]**をクリックして、 **[ポリシーの作成] を**クリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **[ポリシーの作成]**ページで、 **[JSON]**タブをクリックします。

    5.  次のアクセス ポリシー テンプレートをコピーし、ポリシー テキスト フィールドに貼り付けます。

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
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
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

    6.  **「次へ」**をクリックします。

    7.  ポリシー名を設定し、ポリシーのタグ（オプション）を追加して、 **「ポリシーの作成」を**クリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  IAMコンソールの[https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインの**[ロール]**をクリックし、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   **[信頼されたエンティティ タイプ]**で、 **[AWS アカウント]**を選択します。
        -   **[AWS アカウント]**の下で**[別の AWS アカウント]**を選択し、 TiDB Cloudアカウント ID を**[アカウント ID]**フィールドに貼り付けます。
        -   **「オプション」**で**「外部IDが必要」**をクリックして[混乱した副官の問題](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)を回避し、「**外部ID」**フィールドにTiDB Cloudの外部IDを貼り付けます。「外部IDが必要」を選択せず​​にロールを作成した場合、S3バケットURIとIAMロールARNを持つすべてのユーザーがAmazon S3バケットにアクセスできる可能性があります。アカウントIDと外部IDの両方を使用してロールを作成した場合、同じプロジェクトおよび同じリージョンで実行されているTiDBクラスターのみがバケットにアクセスできます。

    3.  **[次へ]**をクリックしてポリシー リストを開き、作成したポリシーを選択して、 **[次へ]**をクリックします。

    4.  **「ロールの詳細」**でロールの名前を設定し、右下にある**「ロールの作成」**をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロール ARN をコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、**データ インポート**ページに移動し、 TiDB Cloudアカウント ID と外部 ID を取得して、ロール ARN を**ロール ARN**フィールドに貼り付けます。

### AWS アクセスキーを使用して Amazon S3 アクセスを構成する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成するには、AWS アカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  次のポリシーを持つIAMユーザーを作成します。

    -   `AmazonS3ReadOnlyAccess`
    -   [`CreateOwnAccessKeys` （必須）と`ManageOwnAccessKeys` （オプション）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

    これらのポリシーは、ソース データを保存するバケットに対してのみ機能することをお勧めします。

    詳細については[IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWS アカウント ID またはアカウントエイリアス、 IAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)参照してください。

> **注記：**
>
> TiDB Cloud はアクセスキーを保存しません。インポートが完了したら、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)実行することをお勧めします。

## GCS アクセスを構成する {#configure-gcs-access}

TiDB Cloud がGCS バケット内のソースデータにアクセスできるようにするには、バケットの GCS アクセスを設定する必要があります。プロジェクト内の 1 つの TiDB クラスタに対して設定が完了すると、そのプロジェクト内のすべての TiDB クラスタが GCS バケットにアクセスできるようになります。

1.  TiDB Cloudコンソールで、ターゲット TiDB クラスタの Google Cloud サービス アカウント ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

    3.  **「Cloud Storage からデータをインポート」**を選択し、 **「Google Cloud Storage」**をクリックします。

    4.  **[Google Cloud Server アカウント ID を表示]**をクリックし、後で使用するためにサービス アカウント ID をコピーします。

2.  Google Cloud コンソールで、GCS バケットのIAMロールを作成します。

    1.  [Google Cloud コンソール](https://console.cloud.google.com/)にサインインします。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、 **[ロールの作成]**をクリックします。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3.  ロールの名前、説明、ID、およびロール開始ステージを入力します。ロールの作成後は、ロール名を変更できません。

    4.  **[権限の追加]を**クリックします。

    5.  次の読み取り専用権限をロールに追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.objects.get
        -   storage.objects.list

        権限名を**「プロパティ名または値を入力」**フィールドにフィルタークエリとしてコピーし、フィルター結果でその名前を選択できます。3つの権限を追加するには、権限名の間に**OR**を使用します。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB Cloud がアクセスする GCS バケットの名前をクリックします。

4.  **バケットの詳細**ページで、 **[権限]**タブをクリックし、 **[アクセスの許可]**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5.  バケットへのアクセスを許可するには次の情報を入力し、 **「保存」**をクリックします。

    -   **[新しいプリンシパル]**フィールドに、ターゲット TiDB クラスタの Google Cloud サービス アカウント ID を貼り付けます。

    -   **[ロールの選択]**ドロップダウン リストに、作成したIAMロールの名前を入力し、フィルター結果から名前を選択します。

    > **注記：**
    >
    > TiDB Cloudへのアクセスを削除するには、許可したアクセスを削除するだけです。

6.  **バケットの詳細**ページで、 **[オブジェクト]**タブをクリックします。

    ファイルの gsutil URI をコピーする場合は、ファイルを選択し、 **[オブジェクト オーバーフロー メニューを開く]**をクリックして、 **[gsutil URI をコピー] を**クリックします。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    フォルダのgsutil URIを使用する場合は、フォルダを開き、フォルダ名の横にあるコピーボタンをクリックしてフォルダ名をコピーします。その後、フォルダ名の先頭に`gs://` 、末尾に`/`追加して、正しいフォルダURIを取得してください。

    たとえば、フォルダー名が`tidb-cloud-source-data`場合、URI として`gs://tidb-cloud-source-data/`使用する必要があります。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7.  TiDB Cloudコンソールで、**データインポート**ページに移動し、Google Cloud サービスアカウント ID を取得し、GCS バケットの gsutil URI を**「バケット gsutil URI」**フィールドに貼り付けます。例えば、 `gs://tidb-cloud-source-data/`と入力します。

## Azure Blob Storage アクセスを構成する {#configure-azure-blob-storage-access}

TiDB Cloud Dedicated が Azure BLOB コンテナーにアクセスできるようにするには、コンテナーの Azure BLOB アクセスを構成する必要があります。コンテナーへのアクセスを構成するには、アカウントの SAS トークンを使用します。

1.  [Azure ストレージ アカウント](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)ページで、コンテナーが属するstorageアカウントをクリックします。

2.  storageアカウントのナビゲーション ウィンドウで、 **[Security+ ネットワーク]** &gt; **[Shared access signature] を**クリックします。

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3.  **Shared access signature**ページで、次のように必要な権限を持つ[アカウントSASトークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)作成します。

    1.  **[許可されたサービス]**の下で、 **[Blob]**を選択します。
    2.  **許可されたリソースの種類**の下で、**コンテナー**と**オブジェクト**を選択します。
    3.  **「許可された権限」**で、必要な権限を選択します。たとえば、 TiDB Cloud Dedicated にデータをインポートするには、 **「読み取り」**と**「一覧表示」の**権限が必要です。
    4.  必要に応じて**開始日時と有効期限**を調整してください。セキュリティ上の理由から、データのインポートスケジュールに合わせて有効期限を設定することをお勧めします。
    5.  その他の設定はデフォルト値のままにしておきます。

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4.  SAS トークンを生成するには、 **「SAS と接続文字列の生成」を**クリックします。

5.  生成された**SASトークン**をコピーします。このトークン文字列は、 TiDB Cloudでデータのインポートを設定する際に必要になります。

> **注記：**
>
> データのインポートを開始する前に、接続とアクセス許可をテストして、 TiDB Cloud Dedicated が指定された Azure Blob コンテナーとファイルにアクセスできることを確認します。
