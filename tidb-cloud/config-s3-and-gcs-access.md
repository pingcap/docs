---
title: Configure Amazon S3 Access and GCS Access
summary: Learn how to configure Amazon Simple Storage Service (Amazon S3) access and Google Cloud Storage (GCS) access.
---

# Amazon S3 アクセスと GCS アクセスの設定 {#configure-amazon-s3-access-and-gcs-access}

ソース データが Amazon S3 または Google Cloud Storage (GCS) バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのクロスアカウント アクセスを構成する必要があります。このドキュメントでは、これを行う方法について説明します。

## Amazon S3 アクセスの構成 {#configure-amazon-s3-access}

TiDB Cloud がAmazon S3 バケットのソース データにアクセスできるようにするには、 TiDB Cloudのバケット アクセスを構成する必要があります。次のいずれかの方法を使用して、バケット アクセスを構成できます。

-   AWS アクセス キーを使用する: IAMユーザーのアクセス キーを使用して、Amazon S3 バケットにアクセスします。
-   ロール ARN を使用する: ロール ARN を使用して、Amazon S3 バケットにアクセスします。

<SimpleTab>
<div label="Access Key">

アクセス キーの作成には、(AWS アカウントのルート ユーザーではなく) IAMユーザーを使用することをお勧めします。

アクセス キーを構成するには、次の手順を実行します。

1.  次のポリシーでIAMユーザーを作成します。

    -   `AmazonS3ReadOnlyAccess`
    -   [`CreateOwnAccessKeys` (必須) および<code>ManageOwnAccessKeys</code> (オプション)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

    これらのポリシーは、ソース データを格納するバケットに対してのみ機能することをお勧めします。

    詳細については、 [IAMユーザーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)を参照してください。

2.  AWS アカウント ID またはアカウント エイリアス、およびIAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインします。

3.  アクセスキーを作成します。詳細については、 [IAMユーザーのアクセス キーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)を参照してください。

> **ノート：**
>
> TiDB Cloud はアクセス キーを保存しません。インポートが完了したら[アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)することをお勧めします。

</div>
<div label="Role ARN">

TiDB Cloudのバケット アクセスを構成し、次のようにロール ARN を取得します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、ターゲットの TiDB クラスターのTiDB Cloudアカウント ID と外部 ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

    3.  **[インポート]**ページで、右上隅にある<strong>[データのインポート]</strong>をクリックし、 <strong>[S3 から]</strong>を選択します。

    4.  **[S3 からのインポート]**ページで、 <strong>[必要なロール ARN を取得するためのガイド]</strong>をクリックして、 TiDB Cloudアカウント ID とTiDB Cloud外部 ID を取得します。後で使用するために、これらの ID をメモしておいてください。

2.  AWS マネジメント コンソールで、Amazon S3 バケットの管理ポリシーを作成します。

    1.  AWS マネジメント コンソールにサインインし、 [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で Amazon S3 コンソールを開きます。

    2.  **[バケット]**リストで、ソース データを含むバケットの名前を選択し、 <strong>[ARN のコピー]</strong>をクリックして S3 バケット ARN を取得します (たとえば、 `arn:aws:s3:::tidb-cloud-source-data` )。後で使用するために、バケット ARN を書き留めます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーション ペインで**[ポリシー]**をクリックし、 <strong>[ポリシーの作成]</strong>をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  **[ポリシーの作成]**ページで、 <strong>[JSON]</strong>タブをクリックします。

    5.  次のアクセス ポリシー テンプレートをコピーして、ポリシー テキスト フィールドに貼り付けます。

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

            たとえば、ソース データが`tidb-cloud-source-data`バケットのルート ディレクトリに格納されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`使用します。ソース データがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`を使用します。 TiDB Cloud がこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの最後に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"`

            たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"`です。

    6.  **[次へ: タグ]**をクリックし、ポリシーのタグを追加して (オプション)、 <strong>[次へ: 確認]</strong>をクリックします。

    7.  ポリシー名を設定し、 **[ポリシーの作成]**をクリックします。

3.  AWS マネジメント コンソールで、 TiDB Cloudのアクセス ロールを作成し、ロール ARN を取得します。

    1.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)のIAMコンソールで、左側のナビゲーション ペインで**[ロール]**をクリックし、 <strong>[ロールの作成]</strong>をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   **[信頼されたエンティティ タイプ]**で、 <strong>[AWS アカウント]</strong>を選択します。
        -   **An AWS account**で、 <strong>Another AWS account</strong>を選択し、 TiDB Cloudアカウント ID を<strong>Account ID</strong>フィールドに貼り付けます。
        -   **[オプション]**で、 <strong>[外部 ID を要求する (サード パーティがこのロールを引き受ける場合のベスト プラクティス)]</strong>をクリックし、 TiDB Cloudの外部 ID を<strong>[外部 ID]</strong>フィールドに貼り付けます。 「外部 ID が必要」なしでロールが作成された場合、プロジェクト内の 1 つの TiDB クラスターの設定が完了すると、そのプロジェクト内のすべての TiDB クラスターは同じロール ARN を使用して Amazon S3 バケットにアクセスできます。アカウント ID と外部 ID を使用してロールが作成された場合、対応する TiDB クラスターのみがバケットにアクセスできます。

    3.  **[次へ]**をクリックしてポリシー リストを開き、作成したポリシーを選択して、 <strong>[次へ]</strong>をクリックします。

    4.  **[ロールの詳細]**で、ロールの名前を設定し、右下隅にある<strong>[ロールの作成]</strong>をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックしてその概要ページに移動し、ロール ARN をコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、 TiDB Cloudアカウント ID と外部 ID を取得する**データ インポート**ページに移動し、ロール ARN を<strong>ロール ARN</strong>フィールドに貼り付けます。

</div>
</SimpleTab>

## GCS アクセスの構成 {#configure-gcs-access}

TiDB Cloud がGCS バケット内のソース データにアクセスできるようにするには、バケットの GCS アクセスを構成する必要があります。プロジェクト内の 1 つの TiDB クラスターの構成が完了すると、そのプロジェクト内のすべての TiDB クラスターが GCS バケットにアクセスできるようになります。

1.  TiDB Cloudコンソールで、ターゲット TiDB クラスターの Google Cloud サービス アカウント ID を取得します。

    1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

    3.  右上隅の**[データのインポート]**をクリックし、 <strong>[Google Cloud サービス アカウント ID を表示]</strong>をクリックして、後で使用できるようにサービス アカウント ID をコピーします。

2.  Google Cloud Platform (GCP) 管理コンソールで、GCS バケットのIAMロールを作成します。

    1.  [GCP 管理コンソール](https://console.cloud.google.com/)にサインインします。

    2.  [役割](https://console.cloud.google.com/iam-admin/roles)ページに移動し、 **[CREATE ROLE]**をクリックします。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3.  役割の名前、説明、ID、および役割の開始段階を入力します。ロールの作成後にロール名を変更することはできません。

    4.  **[権限を追加]**をクリックします。

    5.  次の読み取り専用アクセス許可を役割に追加し、 **[追加]**をクリックします。

        -   storage.buckets.get
        -   storage.objects.get
        -   storage.objects.list

        **アクセス許可名をフィルター クエリとして [プロパティ名または値を入力]**フィールドにコピーし、フィルター結果で名前を選択することができます。 3 つのアクセス許可を追加するには、アクセス許可名の間に<strong>OR</strong>を使用できます。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3.  [バケツ](https://console.cloud.google.com/storage/browser)ページに移動し、 TiDB Cloudにアクセスさせたい GCS バケットの名前をクリックします。

4.  **バケットの詳細**ページで、 <strong>[PERMISSIONS]</strong>タブをクリックし、 <strong>[GRANT ACCESS]</strong>をクリックします。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5.  次の情報を入力してバケットへのアクセスを許可し、 **[保存]**をクリックします。

    -   **[New Principals]**フィールドに、ターゲット TiDB クラスタの Google Cloud サービス アカウント ID を貼り付けます。

    -   **[ロールの選択]**ドロップダウン リストで、作成したばかりのIAMロールの名前を入力し、フィルター結果から名前を選択します。

    > **ノート：**
    >
    > TiDB Cloudへのアクセスを削除するには、付与したアクセスを削除するだけです。

6.  **バケットの詳細**ページで、 <strong>[オブジェクト]</strong>タブをクリックします。

    ファイルの gsutil URI をコピーする場合は、ファイルを選択し、 **[オブジェクト オーバーフロー メニューを開く]**をクリックし、 <strong>[gsutil URI をコピー]</strong>をクリックします。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    フォルダの gsutil URI を使用する場合は、フォルダを開き、フォルダ名に続く [コピー] ボタンをクリックしてフォルダ名をコピーします。その後、フォルダの正しい URI を取得するために、名前の先頭に`gs://` 、末尾に`/`追加する必要があります。

    たとえば、フォルダー名が`tidb-cloud-source-data`の場合、URI として`gs://tidb-cloud-source-data/`使用する必要があります。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7.  TiDB Cloudコンソールで、Google Cloud サービス アカウント ID を取得する**データ インポート**ページに移動し、GCS バケット gsutil URI を<strong>バケット gsutil URI</strong>フィールドに貼り付けます。たとえば、 `gs://tidb-cloud-source-data/`を貼り付けます。
