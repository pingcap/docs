---
title: Import or Migrate from Amazon S3 or GCS to TiDB Cloud
summary: Learn how to import or migrate data from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) to TiDB Cloud.
---

# Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-amazon-s3-or-gcs-to-tidb-cloud}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Google Cloud Storage (GCS) をTiDB Cloudにデータをインポートまたは移行するためのステージング領域として使用する方法について説明します。

> **ノート：**
>
> アップストリーム データベースが Amazon Aurora MySQL の場合は、このドキュメントを参照する代わりに、 [<a href="/tidb-cloud/migrate-from-aurora-bulk-import.md">Amazon Aurora MySQL からTiDB Cloudへ一括移行</a>](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## Amazon S3 からTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-amazon-s3-to-tidb-cloud}

組織が AWS のサービスとしてTiDB Cloudを使用している場合は、 TiDB Cloudにデータをインポートまたは移行するためのステージング領域として Amazon S3 を使用できます。

### 前提条件 {#prerequisites}

データを Amazon S3 からTiDB Cloudに移行する前に、企業所有の AWS アカウントへの管理者アクセス権があることを確認してください。

### ステップ 1. Amazon S3 バケットを作成し、ソースデータファイルを準備する {#step-1-create-an-amazon-s3-bucket-and-prepare-source-data-files}

1.  企業所有の AWS アカウントに Amazon S3 バケットを作成します。

    詳細については、AWS ユーザーガイドの[<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html">バケットの作成</a>](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してください。

    > **ノート：**
    >
    > 下り料金とレイテンシーを最小限に抑えるには、Amazon S3 バケットとTiDB Cloudデータベース クラスターを同じリージョンに作成します。

2.  アップストリーム データベースからデータを移行する場合は、最初にソース データをエクスポートする必要があります。

    詳細については、 [<a href="/tidb-cloud/migrate-data-into-tidb.md">MySQL 互換データベースからのデータの移行</a>](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

3.  ソースデータがローカル ファイルにある場合は、Amazon S3 コンソールまたは AWS CLI を使用してファイルを Amazon S3 バケットにアップロードできます。

    -   Amazon S3 コンソールを使用してファイルをアップロードするには、AWS ユーザーガイドの[<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html">オブジェクトのアップロード</a>](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html)を参照してください。
    -   AWS CLI を使用してファイルをアップロードするには、次のコマンドを使用します。

        ```shell
        aws s3 sync <Local path> <Amazon S3 bucket URI>
        ```

        例えば：

        ```shell
        aws s3 sync ./tidbcloud-samples-us-west-2/ s3://tidb-cloud-source-data
        ```

> **ノート：**
>
> -   ソース データがTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、 Dumpling、 Aurora Backup Snapshot が含まれます。ソース ファイルが CSV 形式の場合は、 [<a href="https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name">TiDB がサポートする命名規則</a>](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能かつ該当する場合は、大きなソース ファイルを最大サイズ 256 MB の小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudはスレッド間で並行してファイルを読み取ることができるため、インポートのパフォーマンスが向上する可能性があります。

### ステップ 2. Amazon S3 アクセスを構成する {#step-2-configure-amazon-s3-access}

TiDB Cloud がAmazon S3 バケット内のソース データにアクセスできるようにするには、 TiDB Cloudのバケット アクセスを設定し、Role-ARN を取得する必要があります。プロジェクト内の 1 つの TiDB クラスターの設定が完了すると、そのプロジェクト内のすべての TiDB クラスターが同じロール ARN を使用して Amazon S3 バケットにアクセスできるようになります。

詳細な手順については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

### ステップ 3. データをTiDB Cloudにインポートする {#step-3-import-data-into-tidb-cloud}

1.  ターゲットクラスターの**インポート**ページを開きます。

    1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **[インポート]**ページで、右上隅にある**[データのインポート]**をクリックし、 **[S3 から] を**選択して、次のパラメーターを入力します。

    -   **データ形式**: データの形式を選択します。
    -   **バケット URI** : ソース データのバケット URI を入力します。
    -   **ロール ARN** : [<a href="#step-2-configure-amazon-s3-access">ステップ2</a>](#step-2-configure-amazon-s3-access)で取得したロール ARN を入力します。

    バケットのリージョンがクラスターと異なる場合は、クロスリージョンのコンプライアンスを確認してください。 **「次へ」**をクリックします。

    TiDB Cloudは、指定されたバケット URI 内のデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloudはデフォルトのファイル命名パターンを使用してデータ ソース内のすべてのファイルのスキャンを試行し、次のページの左側にスキャンの概要結果を返します。 `AccessDenied`エラーが発生した場合は、 [<a href="/tidb-cloud/troubleshoot-import-access-denied-error.md">S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング</a>](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

3.  必要に応じて、ファイル パターンを変更し、テーブル フィルター ルールを追加します。

4.  **「次へ」**をクリックします。

5.  **[プレビュー]**ページで、インポートするデータを確認し、 **[インポートの開始]**をクリックします。

データのインポート後、 TiDB Cloudの Amazon S3 アクセスを削除する場合は、 [<a href="#step-2-configure-amazon-s3-access">ステップ 2. Amazon S3 アクセスを構成する</a>](#step-2-configure-amazon-s3-access)で追加したポリシーを削除するだけです。

## GCS からTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-gcs-to-tidb-cloud}

組織が Google Cloud Platform (GCP) 上のサービスとしてTiDB Cloudを使用している場合は、 TiDB Cloudにデータをインポートまたは移行するためのステージング領域として Google Cloud Storage (GCS) を使用できます。

### 前提条件 {#prerequisites}

データを GCS からTiDB Cloudに移行する前に、次のことを確認してください。

-   企業所有の GCP アカウントへの管理者アクセス権を持っています。
-   TiDB Cloud管理ポータルへの管理者アクセス権を持っています。

### ステップ 1. GCS バケットを作成し、ソース データ ファイルを準備する {#step-1-create-a-gcs-bucket-and-prepare-source-data-files}

1.  企業所有の GCP アカウントに GCS バケットを作成します。

    詳細については、Google Cloud Storage ドキュメントの[<a href="https://cloud.google.com/storage/docs/creating-buckets">storageバケットの作成</a>](https://cloud.google.com/storage/docs/creating-buckets)を参照してください。

2.  アップストリーム データベースからデータを移行する場合は、最初にソース データをエクスポートする必要があります。

    詳細については、 [<a href="/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup">TiUPをインストールする</a>](/tidb-cloud/migrate-data-into-tidb.md#step-1-install-tiup)および[<a href="/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases">MySQL互換データベースからデータをエクスポート</a>](/tidb-cloud/migrate-data-into-tidb.md#step-2-export-data-from-mysql-compatible-databases)を参照してください。

> **ノート：**
>
> -   ソース データがTiDB Cloudでサポートされているファイル形式にコピーできることを確認してください。サポートされている形式には、CSV、 Dumpling、 Aurora Backup Snapshot が含まれます。ソース ファイルが CSV 形式の場合は、 [<a href="https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name">TiDB がサポートする命名規則</a>](https://docs.pingcap.com/tidb/stable/migrate-from-csv-using-tidb-lightning#file-name)に従う必要があります。
> -   可能かつ該当する場合は、大きなソース ファイルを最大サイズ 256 MB の小さなファイルに分割することをお勧めします。これにより、 TiDB Cloudがスレッド間で並行してファイルを読み取ることができ、インポートのパフォーマンスが向上します。

### ステップ 2. GCS アクセスを構成する {#step-2-configure-gcs-access}

TiDB クラウドが GCS バケット内のソース データにアクセスできるようにするには、GCP プロジェクトと GCS バケットのペア上のサービスとして、各TiDB Cloudの GCS アクセスを構成する必要があります。プロジェクト内の 1 つのクラスターの構成が完了すると、そのプロジェクト内のすべてのデータベース クラスターが GCS バケットにアクセスできるようになります。

詳細な手順については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access">GCS アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access)を参照してください。

### ステップ 3. ソース データ ファイルを GCS にコピーし、データをTiDB Cloudにインポートする {#step-3-copy-source-data-files-to-gcs-and-import-data-into-tidb-cloud}

1.  ソース データ ファイルを GCS バケットにコピーするには、Google Cloud コンソールまたは gsutil を使用してデータを GCS バケットにアップロードします。

    -   Google Cloud コンソールを使用してデータをアップロードするには、Google Cloud Storage ドキュメントの[<a href="https://cloud.google.com/storage/docs/creating-buckets">storageバケットの作成</a>](https://cloud.google.com/storage/docs/creating-buckets)を参照してください。
    -   gsutil を使用してデータをアップロードするには、次のコマンドを使用します。

        ```shell
        gsutil rsync -r <Local path> <GCS URI>
        ```

        例えば：

        ```shell
        gsutil rsync -r ./tidbcloud-samples-us-west-2/ gs://target-url-in-gcs
        ```

2.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

3.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

4.  **[インポート]**ページで、右上隅の**[データのインポート]**をクリックし、インポート関連情報を入力します。

> **ノート：**
>
> 下り料金とレイテンシーを最小限に抑えるには、GCS バケットとTiDB Cloudデータベース クラスターを同じリージョンに配置します。
