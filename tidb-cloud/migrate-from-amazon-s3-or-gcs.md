---
title: Import or Migrate from Amazon S3 or GCS to TiDB Cloud
summary: Learn how to import or migrate data from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) to TiDB Cloud.
---

# AmazonS3またはGCSからTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-amazon-s3-or-gcs-to-tidb-cloud}

このドキュメントでは、データをTiDB Cloudにインポートまたは移行するためのステージング領域として、Amazon Simple Storage Service（Amazon S3）またはGoogle Cloud Storage（GCS）を使用する方法について説明します。

> **ノート：**
>
> アップストリームデータベースがAuroraの場合は、このドキュメントを参照する代わりに、 [AuroraからTiDB Cloudに一括で移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## AmazonS3からTiDB Cloudにインポートまたは移行します {#import-or-migrate-from-amazon-s3-to-tidb-cloud}

組織がAWS上のサービスとしてTiDB Cloudを使用している場合は、データをTiDB Cloudにインポートまたは移行するためのステージングエリアとしてAmazonS3を使用できます。

### 前提条件 {#prerequisites}

AmazonS3からTiDB Cloudにデータを移行する前に、企業所有のAWSアカウントへの管理者アクセス権があることを確認してください。

### ステップ1.AmazonS3バケットを作成し、ソースデータファイルを準備します {#step-1-create-an-amazon-s3-bucket-and-prepare-source-data-files}

1.  企業所有のAWSアカウントにAmazonS3バケットを作成します。

    詳細については、AWSユーザーガイドの[バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

    > **ノート：**
    >
    > 出力料金とレイテンシーを最小限に抑えるには、AmazonS3バケットとTiDB Cloudデータベースクラスタを同じリージョンに作成します。

2.  アップストリームデータベースからデータを移行する場合は、最初にソースデータをエクスポートする必要があります。

    詳細については、 [MySQL互換データベースからデータを移行する](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

3.  ソースデータがローカルファイルにある場合は、AmazonS3コンソールまたはAWSCLIのいずれかを使用してファイルをAmazonS3バケットにアップロードできます。

    -   Amazon S3コンソールを使用してファイルをアップロードするには、AWSユーザーガイドの[オブジェクトのアップロード](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html)を参照してください。
    -   AWS CLIを使用してファイルをアップロードするには、次のコマンドを使用します。

        ```shell
        aws s3 sync <Local path> <Amazon S3 bucket URL>
        ```

        例えば：

        ```shell
        aws s3 sync ./tidbcloud-samples-us-west-2/ s3://tidb-cloud-source-data
        ```

> **ノート：**
>
> -   ソースデータをTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、Dumpling、 Auroraバックアップスナップショットが含まれます。ソースファイルがCSV形式の場合は、 [TiDBでサポートされている命名規則](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能で適用可能な場合は、大きなソースファイルを最大サイズ256MBの小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudはスレッド間でファイルを並行して読み取ることができるため、インポートのパフォーマンスが向上する可能性があります。

### ステップ2.AmazonS3アクセスを設定します {#step-2-configure-amazon-s3-access}

TiDBCloudがTiDB Cloudバケットのソースデータにアクセスできるようにするには、次の手順を実行してTiDB Cloudのバケットアクセスを設定し、Role-ARNを取得します。プロジェクト内の1つのTiDBクラスタの設定が完了すると、そのプロジェクト内のすべてのTiDBクラスターが同じRole-ARNを使用してAmazonS3バケットにアクセスできるようになります。

1.  TiDB Cloud Consoleで、ターゲットTiDBクラスタのTiDB CloudアカウントIDと外部IDを取得します。

    1.  TiDB Cloud Consoleで、ターゲットプロジェクトを選択し、ターゲットクラスタの名前をクリックして概要ページに移動します。
    2.  左側のクラスタ概要ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。
    3.  [**データインポートタスク**]ページで、[ <strong>AWS IAMポリシー設定の表示</strong>]をクリックして、 TiDB CloudアカウントIDとTiDB Cloud外部IDを取得します。後で使用するために、これらのIDをメモしてください。

2.  AWSマネジメントコンソールで、AmazonS3バケットのマネージドポリシーを作成します。

    1.  AWSマネジメントコンソールにサインインし、AmazonS3コンソールを[https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)で開きます。

    2.  [**バケット**]リストで、ソースデータを含むバケットの名前を選択し、[ARNの<strong>コピー</strong>]をクリックしてS3バケットのARNを取得します（たとえば、 `arn:aws:s3:::tidb-cloud-source-data` ）。後で使用するために、バケットARNをメモしておきます。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)でIAMコンソールを開き、左側のナビゲーションペインで[**ポリシー**]をクリックしてから、[ポリシーの<strong>作成</strong>]をクリックします。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4.  [**ポリシーの作成**]ページで、[ <strong>JSON</strong> ]タブをクリックします。

    5.  次のアクセスポリシーテンプレートをコピーして、ポリシーテキストフィールドに貼り付けます。

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

        ポリシーテキストフィールドで、次の構成を独自の値に更新します。

        -   `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            たとえば、ソースデータが`tidb-cloud-source-data`バケットのルートディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`を使用します。ソースデータがバケットの`mydata`ディレクトリに保存されている場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`を使用します。 TiDB Cloudがこのディレクトリ内のすべてのファイルにアクセスできるように、ディレクトリの最後に`/*`が追加されていることを確認してください。

        -   `"Resource": "<Your S3 bucket ARN>"`

            たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-source-data"` 。

    6.  [**次へ：タグ**]をクリックし、ポリシーのタグを追加して（オプション）、[<strong>次へ：レビュー</strong>]をクリックします。

    7.  ポリシー名を設定し、[**ポリシーの作成**]をクリックします。

3.  AWSマネジメントコンソールで、 TiDB Cloudのアクセスロールを作成し、ロールARNを取得します。

    1.  [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)のIAMコンソールで、左側のナビゲーションペインで[**役割**]をクリックし、[役割の<strong>作成</strong>]をクリックします。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2.  ロールを作成するには、次の情報を入力します。

        -   [**信頼できるエンティティタイプ**]で、[ <strong>AWSアカウント]</strong>を選択します。
        -   [ **AWSアカウント**]で、[<strong>別のAWSアカウント</strong>]を選択し、 TiDB CloudアカウントIDを[<strong>アカウントID]</strong>フィールドに貼り付けます。
        -   [**オプション**]で、[外部IDが必要] <strong>（サードパーティがこの役割を引き受ける場合のベストプラクティス）を</strong>クリックし、 TiDB Cloud外部IDを[<strong>外部ID</strong> ]フィールドに貼り付けます。

    3.  [**次へ**]をクリックしてポリシーリストを開き、作成したポリシーを選択して、[<strong>次へ</strong>]をクリックします。

    4.  [**役割の詳細**]で、役割の名前を設定し、右下隅にある[<strong>役割の作成</strong>]をクリックします。ロールが作成されると、ロールのリストが表示されます。

    5.  ロールのリストで、作成したロールの名前をクリックして概要ページに移動し、ロールARNをコピーします。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4.  TiDB Cloudコンソールで、 TiDB CloudアカウントIDと外部IDを取得する**[データインポートタスク**]ページに移動し、ロールARNを[<strong>ロールARN]</strong>フィールドに貼り付けます。

### ステップTiDB Cloudにデータをインポートする {#step-3-import-data-into-tidb-cloud}

1.  [**データインポートタスク**]ページで、[<strong>役割ARN]</strong>フィールドに加えて、次の情報も入力する必要があります。

    -   **データソースタイプ**： `AWS S3` 。
    -   **バケットURL** ：ソースデータのバケットURLを入力します。
    -   **データ形式**：データの形式を選択します。
    -   **ターゲットクラスター**： <strong>[ユーザー名]</strong>フィールドと[<strong>パスワード</strong>]フィールドに入力します。
    -   **DB /テーブルフィルター**：必要に応じて、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter#cli)を指定できます。

2.  [**インポート]**をクリックします。

    データベースリソースの消費に関する警告メッセージが表示されます。

3.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケットURLのデータにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポートタスクが自動的に開始されます。 `AccessDenied`エラーが発生した場合は、 [S3からのデータインポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

データがインポートされた後、 TiDB CloudのAmazon S3アクセスを削除する場合は、 [ステップ2.AmazonS3アクセスを設定します](#step-2-configure-amazon-s3-access)で追加したポリシーを削除するだけです。

## GCSからTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-gcs-to-tidb-cloud}

組織でTiDB CloudをGoogleCloudPlatform（GCP）のサービスとして使用している場合は、Google Cloud Storage（GCS）をTiDB Cloudにデータをインポートまたは移行するためのステージング領域として使用できます。

### 前提条件 {#prerequisites}

GCSからTiDB Cloudにデータを移行する前に、次のことを確認してください。

-   企業所有のGCPアカウントへの管理者アクセス権があります。
-   TiDB Cloud管理ポータルへの管理者アクセス権があります。

### 手順1.GCSバケットを作成し、ソースデータファイルを準備します {#step-1-create-a-gcs-bucket-and-prepare-source-data-files}

1.  企業所有のGCPアカウントにGCSバケットを作成します。

    詳細については、GoogleCloudStorageのドキュメントの[ストレージバケットの作成](https://cloud.google.com/storage/docs/creating-buckets)を参照してください。

2.  アップストリームデータベースからデータを移行する場合は、最初にソースデータをエクスポートする必要があります。

    詳細については、 [TiUPをインストールします](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup)および[MySQL互換データベースからデータをエクスポートする](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases)を参照してください。

> **ノート：**
>
> -   ソースデータをTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、Dumpling、 Auroraバックアップスナップショットが含まれます。ソースファイルがCSV形式の場合は、 [TiDBでサポートされている命名規則](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能で適用可能な場合は、大きなソースファイルを最大サイズ256 MBの小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudがスレッド間でファイルを並列に読み取ることができ、インポートのパフォーマンスが向上します。

### 手順2.GCSアクセスを構成する {#step-2-configure-gcs-access}

TiDBクラウドがGCSバケット内のソースデータにアクセスできるようにするには、各TiDB CloudのGCSアクセスをGCPプロジェクトとGCSバケットペアのサービスとして構成する必要があります。プロジェクト内の1つのクラスタの構成が完了すると、そのプロジェクト内のすべてのデータベースクラスターがGCSバケットにアクセスできるようになります。

1.  ターゲットTiDBクラスタのGoogleCloudServiceアカウントIDを取得します。

    1.  TiDB Cloud Adminコンソールで、Google Cloud Platformにデプロイされているターゲットプロジェクトとターゲットクラスタを選択し、[**インポート**]をクリックします。
    2.  [ **Google CloudサービスアカウントIDを表示]**をクリックして、サービスアカウントIDをコピーします。

2.  Google Cloud Platform（GCP）管理コンソールで、[ **IAMと管理**]&gt; [<strong>役割</strong>]に移動し、ストレージコンテナの次の読み取り専用権限を持つ役割が存在するかどうかを確認します。

    -   storage.buckets.get
    -   storage.objects.get
    -   storage.objects。リスト

    はいの場合、次の手順でターゲットTiDBクラスタに一致する役割を使用できます。そうでない場合は、[ **IAMと管理**]&gt;[<strong>ロール</strong>]&gt;[ <strong>CREATE ROLE</strong> ]に移動して、ターゲットTiDBクラスタのロールを定義します。

3.  [**クラウドストレージ**]&gt;[<strong>ブラウザ</strong>]に移動し、 TiDB CloudがアクセスするGCSバケットを選択して、[<strong>情報</strong>パネルの表示]をクリックします。

    パネルが表示されます。

4.  パネルで、[ **PRINCIPAL**の追加]をクリックします。

    プリンシパルを追加するためのダイアログボックスが表示されます。

5.  ダイアログボックスで、次の手順を実行します。

    1.  [**新しいプリンシパル**]フィールドに、ターゲットTiDBクラスタのGoogleCloudServiceアカウントIDを貼り付けます。
    2.  [**役割**]ドロップダウンリストで、ターゲットTiDBクラスタの役割を選択します。
    3.  [**保存]**をクリックします。

これで、 TiDB CloudクラスタがGCSバケットにアクセスできるようになりました。

> **ノート：**
>
> TiDB Cloudへのアクセスを削除するには、追加したプリンシパルを削除するだけです。

### 手順3.ソースデータファイルをGCSにコピーし、データをTiDB Cloudにインポートします {#step-3-copy-source-data-files-to-gcs-and-import-data-into-tidb-cloud}

1.  ソースデータファイルをGCSバケットにコピーするには、GoogleCloudConsoleまたはgsutilを使用してデータをGCSバケットにアップロードします。

    -   Google Cloud Consoleを使用してデータをアップロードするには、GoogleCloudStorageのドキュメントの[ストレージバケットの作成](https://cloud.google.com/storage/docs/creating-buckets)を参照してください。
    -   gsutilを使用してデータをアップロードするには、次のコマンドを使用します。

        ```shell
        gsutil rsync -r <Local path> <GCS URL>
        ```

        例えば：

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```

2.  TiDB Cloudコンソールから、[TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックして、独自の概要ページに移動します。左側のクラスタ情報ペインで、[**インポート**]をクリックし、[<strong>データインポートタスク</strong>]ページでインポート関連情報を入力します。

> **ノート：**
>
> 出力料金とレイテンシーを最小限に抑えるには、GCSバケットとTiDB Cloudデータベースクラスタを同じリージョンに配置します。
