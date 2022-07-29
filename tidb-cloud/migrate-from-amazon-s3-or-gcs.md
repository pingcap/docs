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

TiDB CloudがAmazonS3バケットのソースデータにアクセスできるようにするには、 TiDB Cloudのバケットアクセスを設定し、Role-ARNを取得する必要があります。プロジェクト内の1つのTiDBクラスタの設定が完了すると、そのプロジェクト内のすべてのTiDBクラスターが同じRole-ARNを使用してAmazonS3バケットにアクセスできるようになります。

詳細な手順については、 [AmazonS3アクセスを設定する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

### ステップTiDB Cloudにデータをインポートする {#step-3-import-data-into-tidb-cloud}

1.  [**データインポートタスク**]ページで、[<strong>役割ARN]</strong>フィールドに加えて、次の情報も入力する必要があります。

    -   **データソースタイプ**： `AWS S3` 。
    -   **バケットURL** ：ソースデータのバケットURLを入力します。
    -   **データ形式**：データの形式を選択します。
    -   **ターゲットクラスター**： <strong>[ユーザー名]</strong>フィールドと[<strong>パスワード</strong>]フィールドに入力します。
    -   **DB /テーブルフィルター**：必要に応じて、 [テーブルフィルター](/table-filter.md#syntax)を指定できます。複数のフィルタールールを構成する場合は、 `,`を使用してルールを区切ります。

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

詳細な手順については、 [GCSアクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access)を参照してください。

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
