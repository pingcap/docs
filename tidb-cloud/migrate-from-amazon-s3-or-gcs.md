---
title: Import or Migrate from Amazon S3 or GCS to TiDB Cloud
summary: Learn how to import or migrate data from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) to TiDB Cloud.
---

# AmazonS3またはGCSからTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-amazon-s3-or-gcs-to-tidb-cloud}

このドキュメントでは、データをTiDB Cloudにインポートまたは移行するためのステージング領域としてAmazon Simple Storage Service（Amazon S3）またはGoogle Cloud Storage（GCS）を使用する方法について説明します。

> **ノート：**
>
> アップストリームデータベースがAuroraの場合は、このドキュメントを参照する代わりに、 [AuroraからTiDB Cloudに一括で移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## AmazonS3からTiDB Cloudにインポートまたは移行します {#import-or-migrate-from-amazon-s3-to-tidb-cloud}

組織がAWSでサービスとしてTiDB Cloudを使用している場合は、データをTiDB Cloudにインポートまたは移行するためのステージングエリアとしてAmazonS3を使用できます。

### 前提条件 {#prerequisites}

AmazonS3からTiDB Cloudにデータを移行する前に、次のことを確認してください。

-   企業所有のAWSアカウントへの管理者アクセス権があります。
-   管理者はTiDB Cloud管理ポータルにアクセスできます。

### ステップ1.AmazonS3バケットを作成し、ソースデータファイルを準備します {#step-1-create-an-amazon-s3-bucket-and-prepare-source-data-files}

1.  企業所有のAWSアカウントにAmazonS3バケットを作成します。

    詳細については、AWSユーザーガイドの[バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

2.  アップストリームデータベースからデータを移行する場合は、最初にソースデータをエクスポートする必要があります。

    詳細については、 [TiUPをインストールします](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup)および[MySQL互換データベースからデータをエクスポートする](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases)を参照してください。

> **ノート：**
>
> -   ソースデータをTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、Dumpling、 Auroraバックアップスナップショットが含まれます。ソースファイルがCSV形式の場合は、 [TiDBでサポートされている命名規則](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能で適用可能な場合は、大きなソースファイルを最大サイズ256 MBの小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudがスレッド間でファイルを並列に読み取ることができ、インポートパフォーマンスが向上する可能性があります。

### ステップ2.AmazonS3アクセスを設定します {#step-2-configure-amazon-s3-access}

TiDBクラウドがAmazonS3バケットのソースデータにアクセスできるようにするには、各TiDB CloudのAmazonS3をAWSプロジェクトとAmazonS3バケットペアのサービスとして設定する必要があります。プロジェクト内の1つのクラスタの設定が完了すると、そのプロジェクト内のすべてのデータベースクラスターがAmazonS3バケットにアクセスできるようになります。

1.  ターゲットTiDBクラスタのTiDB CloudアカウントIDと外部IDを取得します。

    1.  TiDB Cloud管理コンソールで、AWSにデプロイされているターゲットプロジェクトとターゲットクラスタを選択し、[**インポート**]をクリックします。
    2.  [ **AWSIAMポリシー設定の表示]を**クリックします。ターゲットTiDBクラスタの対応するTiDB CloudアカウントIDとTiDB Cloud外部IDが表示されます。
    3.  次の手順で使用されるため、 TiDB CloudアカウントIDと外部IDをメモしてください。

2.  AWSマネジメントコンソールで、[ **IAM]** &gt; [<strong>アクセス管理</strong>]&gt;[<strong>ポリシー</strong>]に移動し、次の読み取り専用アクセス許可を持つストレージバケットポリシーが存在するかどうかを確認します。

    -   s3：GetObject
    -   s3：GetObjectVersion
    -   s3：ListBucket
    -   s3：GetBucketLocation

    上記の権限を持つストレージバケットポリシーが存在するかどうかに応じて、次のいずれかを実行します。

    -   はいの場合、次の手順で、ターゲットTiDBクラスタに一致するストレージバケットポリシーを使用できます。
    -   そうでない場合は、[ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[<strong>ポリシー</strong>]&gt;[ポリシーの<strong>作成</strong>]に移動し、次のポリシーテンプレートに従ってターゲットTiDBクラスタのバケットポリシーを定義します。

    {{< copyable "" >}}

    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<Your customized directory>"
            },
            {
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

    テンプレートでは、次の2つのフィールドを独自のリソース値に更新する必要があります。

    -   `"Resource": "<Your S3 bucket ARN>"` ： `<Your S3 bucket ARN>`はS3バケットのARNです。 S3バケットの[**プロパティ**]タブに移動し、[<strong>バケットの概要</strong>]領域でAmazonリソース名（ARN）の値を取得できます。たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-test"` 。
    -   `"Resource": "arn:aws:s3:::<Your customized directory>"` ： `<Your customized directory>`は、データストレージ用にS3バケットルートレベルでカスタマイズできるディレクトリです。たとえば、 `"Resource": "arn:aws:s3:::tidb-cloud-test/mydata/*"` 。データをS3バケットルートディレクトリに保存する場合は、 `"Resource": "arn:aws:s3:::tidb-cloud-test/*"`を使用します。

3.  [ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[<strong>ロール</strong>]に移動し、信頼エンティティがターゲットTiDBクラスタのTiDB CloudアカウントIDに対応するロールが存在するかどうかを確認します。

    -   はいの場合、次の手順でターゲットTiDBクラスタに一致する役割を使用できます。
    -   そうでない場合は、[ **Create role** ]をクリックし、信頼エンティティタイプとして[ <strong>Another AWSアカウント</strong>]を選択してから、[AccountID <strong>]</strong>フィールドにターゲットTiDBクラスタのTiDB CloudアカウントIDを入力します。

4.  [ **IAM** ]&gt;[<strong>アクセス管理</strong>]&gt;[<strong>ロール</strong>]で、前の手順のロール名をクリックして<strong>[概要</strong>]ページに移動し、次の手順を実行します。

    1.  [**権限**]タブで、ターゲットTiDBクラスタのストレージバケットポリシーがロールにアタッチされているかどうかを確認します。

        そうでない場合は、[ポリシーの添付]を選択し、必要な**ポリシー**を検索して、[<strong>ポリシーの添付</strong>]をクリックします。

    2.  [**信頼関係**]タブをクリックし、[<strong>信頼関係の編集</strong>]をクリックして、 <strong>Condition sts：ExternalId</strong>属性の値がターゲットTiDBクラスタのTiDB Cloud外部IDであるかどうかを確認します。

        そうでない場合は、JSONテキストエディターで**Condition sts：ExternalId**属性を更新し、[<strong>信頼ポリシーの更新</strong>]をクリックします。

        以下は、 **Condition sts：ExternalId**属性の構成例です。

        {{< copyable "" >}}

        ```
        "Condition": {
            "StringEquals": {
            "sts:ExternalId": "696e6672612d61706993147c163238a8a7005caaf40e0338fc"
            }
        }
        ```

    3.  **[概要**]ページに戻り、<strong>ロールARN</strong>値をクリップボードにコピーします。

5.  TiDB Cloud管理コンソールで、ターゲットTiDBクラスタのTiDB CloudアカウントIDと外部IDを取得する画面に移動し、前の手順のロール値を使用して[**ロールARN** ]フィールドを更新します。

これで、 TiDB CloudクラスタがAmazonS3バケットにアクセスできるようになりました。

> **ノート：**
>
> TiDB Cloudへのアクセスを削除するには、追加した信頼ポリシーを削除するだけです。

### ステップ3.ソースデータファイルをAmazonS3にコピーし、データをTiDB Cloudにインポートします {#step-3-copy-source-data-files-to-amazon-s3-and-import-data-into-tidb-cloud}

1.  ソースデータファイルをAmazonS3バケットにコピーするには、AWSWebコンソールまたはAWSCLIのいずれかを使用してデータをAmazonS3バケットにアップロードできます。

    -   AWS Webコンソールを使用してデータをアップロードするには、AWSユーザーガイドの[オブジェクトのアップロード](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html)を参照してください。
    -   AWS CLIを使用してデータをアップロードするには、次のコマンドを使用します。

        {{< copyable "" >}}

        ```shell
        aws s3 sync <Local path> <S3 URL> 
        ```

        例えば：

        {{< copyable "" >}}

        ```shell
        aws s3 sync ./tidbcloud-samples-us-west-2/ s3://target-url-in-s3
        ```

2.  TiDB Cloudコンソールから、[TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックして、独自の概要ページに移動します。左側のクラスタ情報ペインで、[**インポート**]をクリックし、[<strong>データインポートタスク</strong>]ページでインポート関連情報を入力します。

> **ノート：**
>
> 出力料金とレイテンシーを最小限に抑えるには、AmazonS3バケットとTiDB Cloudデータベースクラスタを同じリージョンに配置します。

## GCSからTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-gcs-to-tidb-cloud}

組織でTiDB CloudをGoogleCloudPlatform（GCP）のサービスとして使用している場合は、データをTiDB Cloudにインポートまたは移行するためのステージング領域としてGoogleCloud Storage（GCS）を使用できます。

### 前提条件 {#prerequisites}

GCSからTiDB Cloudにデータを移行する前に、次のことを確認してください。

-   管理者は、会社所有のGCPアカウントにアクセスできます。
-   管理者はTiDB Cloud管理ポータルにアクセスできます。

### 手順1.GCSバケットを作成し、ソースデータファイルを準備します {#step-1-create-a-gcs-bucket-and-prepare-source-data-files}

1.  企業所有のGCPアカウントにGCSバケットを作成します。

    詳細については、GoogleCloudStorageのドキュメントの[ストレージバケットの作成](https://cloud.google.com/storage/docs/creating-buckets)をご覧ください。

2.  アップストリームデータベースからデータを移行する場合は、最初にソースデータをエクスポートする必要があります。

    詳細については、 [TiUPをインストールします](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup)および[MySQL互換データベースからデータをエクスポートする](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases)を参照してください。

> **ノート：**
>
> -   ソースデータをTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、Dumpling、 Auroraバックアップスナップショットが含まれます。ソースファイルがCSV形式の場合は、 [TiDBでサポートされている命名規則](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能で適用可能な場合は、大きなソースファイルを最大サイズ256 MBの小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudがスレッド間でファイルを並列に読み取ることができ、インポートのパフォーマンスが向上します。

### ステップ2.GCSアクセスを構成する {#step-2-configure-gcs-access}

TiDBクラウドがGCSバケット内のソースデータにアクセスできるようにするには、各TiDB CloudのGCSアクセスをGCPプロジェクトとGCSバケットペアのサービスとして構成する必要があります。プロジェクト内の1つのクラスタの構成が完了すると、そのプロジェクト内のすべてのデータベースクラスターがGCSバケットにアクセスできるようになります。

1.  ターゲットTiDBクラスタのGoogleCloudServiceアカウントIDを取得します。

    1.  TiDB Cloud管理コンソールで、Google Cloud Platformにデプロイされているターゲットプロジェクトとターゲットクラスタを選択し、[**インポート**]をクリックします。
    2.  [ **Google Cloud ServiceアカウントIDを表示]**をクリックして、サービスアカウントIDをコピーします。

2.  Google Cloud Platform（GCP）管理コンソールで、[ **IAMと管理**]&gt; [<strong>ロール</strong>]に移動し、ストレージコンテナの次の読み取り専用権限を持つロールが存在するかどうかを確認します。

    -   storage.buckets.get
    -   storage.objects.get
    -   storage.objects。リスト

    はいの場合、次の手順でターゲットTiDBクラスタに一致する役割を使用できます。そうでない場合は、[ **IAMと管理**]&gt;[<strong>ロール</strong>]&gt;[ <strong>CREATE ROLE</strong> ]に移動して、ターゲットTiDBクラスタのロールを定義します。

3.  **Cloud Storage** &gt; <strong>Browser</strong>に移動し、 TiDB CloudがアクセスするGCSバケットを選択して、 <strong>SHOWINFOPANEL</strong>をクリックします。

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

### ステップ3.ソースデータファイルをGCSにコピーし、データをTiDB Cloudにインポートします {#step-3-copy-source-data-files-to-gcs-and-import-data-into-tidb-cloud}

1.  ソースデータファイルをGCSバケットにコピーするには、GoogleCloudConsoleまたはgsutilを使用してデータをGCSバケットにアップロードします。

    -   Google Cloud Consoleを使用してデータをアップロードするには、GoogleCloudStorageのドキュメントの[ストレージバケットの作成](https://cloud.google.com/storage/docs/creating-buckets)をご覧ください。
    -   gsutilを使用してデータをアップロードするには、次のコマンドを使用します。

        {{< copyable "" >}}

        ```shell
        gsutil rsync -r <Local path> <GCS URL> 
        ```

        例えば：

        {{< copyable "" >}}

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```

2.  TiDB Cloudコンソールから、[TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックして、独自の概要ページに移動します。左側のクラスタ情報ペインで、[**インポート**]をクリックし、[<strong>データインポートタスク</strong>]ページでインポート関連情報を入力します。

> **ノート：**
>
> 出力料金とレイテンシーを最小限に抑えるには、GCSバケットとTiDB Cloudデータベースクラスタを同じリージョンに配置します。
