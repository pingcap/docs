---
title: Configure Amazon S3 Access and GCS Access
summary: Amazon Simple Storage Service (Amazon S3) アクセスと Google Cloud Storage (GCS) アクセスを構成する方法を学習します。
---

# Amazon S3 アクセスと GCS アクセスを構成する {#configure-amazon-s3-access-and-gcs-access}

ソースデータが Amazon S3 または Google Cloud Storage (GCS) バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのクロスアカウントアクセスを構成する必要があります。このドキュメントでは、その方法について説明します。

## Amazon S3 アクセスを構成する {#configure-amazon-s3-access}

TiDB Cloud がAmazon S3 バケット内のソースデータにアクセスできるようにするには、 TiDB Cloudのバケットアクセスを設定する必要があります。バケットアクセスを設定するには、次のいずれかの方法を使用できます。

-   AWS アクセスキーを使用する: IAMユーザーのアクセスキーを使用して Amazon S3 バケットにアクセスします。
-   ロール ARN を使用する: ロール ARN を使用して Amazon S3 バケットにアクセスします。

<SimpleTab>
<div label="Role ARN">

次のように、 TiDB Cloudのバケット アクセスを設定し、ロール ARN を取得します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、ターゲット TiDB クラスターのTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

    3.  **「インポート」**ページで、右上隅の**「データのインポート」**をクリックし、 **「S3 から」**を選択します。

    4.  **S3 からのインポート**ページで、**必要なロール ARN を取得するためのガイド**をクリックして、 TiDB Cloudアカウント ID とTiDB Cloud外部 ID を取得します。後で使用するためにこれらの ID をメモしておきます。

2.  AWS マネジメントコンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  AWS マネジメントコンソールにサインインし、 [詳しくはこちら](https://console.aws.amazon.com/s3/)で Amazon S3 コンソールを開きます。

    2.  **[バケット**] リストで、ソース データを含むバケットの名前を選択し、 **[ARN のコピー]**をクリックして S3 バケット ARN (例: `arn:aws:s3:::tidb-cloud-source-data` ) を取得します。後で使用するために、バケット ARN をメモしておきます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [詳しくはこちら](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーション ペインで**[ポリシー]**をクリックして、 **[ポリシーの作成] を**クリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **[ポリシーの作成]**ページで、 **[JSON]**タブをクリックします。

    5.  次のアクセス ポリシー テンプレートをコピーし、ポリシー テキスト フィールドに貼り付けます。

        ```json
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

        ポリシー テキスト フィールドで、次の構成を独自の値に更新します。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            たとえば、ソース データが`tidb-cloud-source-data`バケットのルート ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`を使用します。ソース データがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`使用します。TiDB TiDB Cloud がこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの末尾に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"`

            たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

        -   カスタマー管理のキー暗号化で AWS Key Management Service キー (SSE-KMS) を有効にしている場合は、ポリシーに次の設定が含まれていることを確認してください。1 `"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"`バケットのサンプル KMS キーです。

                {
                    "Sid": "AllowKMSkey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:Decrypt"
                    ],
                    "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
                }

            バケット内のオブジェクトが別の暗号化されたバケットからコピーされた場合、KMS キー値には両方のバケットのキーを含める必要があります。たとえば、 `"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]` 。

    6.  **[次へ: タグ]**をクリックし、ポリシーのタグ (オプション) を追加して、 **[次へ: レビュー]**をクリックします。

    7.  ポリシー名を設定し、 **「ポリシーの作成」を**クリックします。

3.  AWS マネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロール ARN を取得します。

    1.  IAMコンソールの[詳しくはこちら](https://console.aws.amazon.com/iam/)で、左側のナビゲーション ペインの**[ロール]**をクリックし、 **[ロールの作成] を**クリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   **信頼されたエンティティタイプ**で、 **AWS アカウント**を選択します。
        -   **[AWS アカウント]**の下で**[別の AWS アカウント]**を選択し、 TiDB Cloudアカウント ID を**[アカウント ID]**フィールドに貼り付けます。
        -   **オプション**で、**外部 ID が必要 (サードパーティがこのロールを引き受ける場合のベストプラクティス)**をクリックし、 TiDB Cloud外部 ID を**外部 ID**フィールドに貼り付けます。ロールが「外部 ID が必要」なしで作成された場合、プロジェクト内の 1 つの TiDB クラスターの設定が完了すると、そのプロジェクト内のすべての TiDB クラスターが同じロール ARN を使用して Amazon S3 バケットにアクセスできます。ロールがアカウント ID と外部 ID を使用して作成された場合、対応する TiDB クラスターのみがバケットにアクセスできます。

    3.  [**次へ]**をクリックしてポリシー リストを開き、作成したポリシーを選択して、 **[次へ]**をクリックします。

    4.  **[ロールの詳細]**でロールの名前を設定し、右下隅の**[ロールの作成]**をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロール ARN をコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、**データ インポート**ページに移動し、 TiDB Cloudアカウント ID と外部 ID を取得して、ロール ARN を**ロール ARN**フィールドに貼り付けます。

</div>
<div label="Access Key">

アクセスキーを作成するには、AWS アカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  次のポリシーを持つIAMユーザーを作成します。

    -   `AmazonS3ReadOnlyAccess`
    -   [`CreateOwnAccessKeys` (必須) および`ManageOwnAccessKeys` (オプション)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

    これらのポリシーは、ソース データを保存するバケットに対してのみ機能することをお勧めします。

    詳細については[IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)参照してください。

2.  AWS アカウント ID またはアカウントエイリアスと、 IAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)を参照してください。

> **注記：**
>
> TiDB Cloud はアクセス キーを保存しません。インポートが完了したら、 [アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)実行することをお勧めします。

</div>
</SimpleTab>

## GCS アクセスを構成する {#configure-gcs-access}

TiDB Cloud がGCS バケット内のソース データにアクセスできるようにするには、バケットの GCS アクセスを構成する必要があります。プロジェクト内の 1 つの TiDB クラスターの構成が完了すると、そのプロジェクト内のすべての TiDB クラスターが GCS バケットにアクセスできるようになります。

1.  TiDB Cloudコンソールで、ターゲット TiDB クラスタの Google Cloud サービス アカウント ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

    3.  右上隅の**「データのインポート」**をクリックし、 **「Google Cloud サービス アカウント ID を表示」**をクリックして、後で使用するためにサービス アカウント ID をコピーします。

2.  Google Cloud コンソールで、GCS バケットのIAMロールを作成します。

    1.  [Google Cloud コンソール](https://console.cloud.google.com/)にサインインします。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、 **[ロールの作成] を**クリックします。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3.  ロールの名前、説明、ID、およびロール起動ステージを入力します。ロールの作成後は、ロール名を変更できません。

    4.  **「権限の追加」**をクリックします。

    5.  次の読み取り専用権限をロールに追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.objects.get
        -   storage.objects.list

        権限名をフィルター クエリとして**[プロパティ名または値の入力**] フィールドにコピーし、フィルター結果で名前を選択できます。3 つの権限を追加するには、権限名の間に**OR**を使用できます。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB Cloudがアクセスする GCS バケットの名前をクリックします。

4.  **バケットの詳細**ページで、 **「権限」**タブをクリックし、 **「アクセスの許可」**をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5.  バケットへのアクセスを許可するには次の情報を入力し、 **「保存」**をクリックします。

    -   **[新しいプリンシパル]**フィールドに、ターゲット TiDB クラスタの Google Cloud サービス アカウント ID を貼り付けます。

    -   **[ロールの選択]**ドロップダウン リストに、作成したIAMロールの名前を入力し、フィルター結果から名前を選択します。

    > **注記：**
    >
    > TiDB Cloudへのアクセスを削除するには、許可したアクセスを削除するだけです。

6.  **バケットの詳細**ページで、 **「オブジェクト」**タブをクリックします。

    ファイルの gsutil URI をコピーする場合は、ファイルを選択し、 **[オブジェクト オーバーフロー メニューを開く]**をクリックして、 **[gsutil URI をコピー]**をクリックします。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    フォルダの gsutil URI を使用する場合は、フォルダを開き、フォルダ名の後の [コピー] ボタンをクリックしてフォルダ名をコピーします。その後、フォルダの正しい URI を取得するには、名前の先頭に`gs://` 、末尾に`/`追加する必要があります。

    たとえば、フォルダー名が`tidb-cloud-source-data`の場合、URI として`gs://tidb-cloud-source-data/`を使用する必要があります。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7.  TiDB Cloudコンソールで、Google Cloud サービス アカウント ID を取得する**データ インポート**ページに移動し、GCS バケットの gsutil URI を**Bucket gsutil URI**フィールドに貼り付けます。たとえば、 `gs://tidb-cloud-source-data/`貼り付けます。
