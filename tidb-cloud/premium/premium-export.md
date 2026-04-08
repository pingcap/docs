---
title: Export Data from TiDB Cloud Premium
summary: TiDB Cloud Premiumインスタンスからデータをエクスポートする方法を学びましょう。
---

# TiDB Cloud Premium からデータをエクスポート {#export-data-from-tidb-cloud-premium}

TiDB Cloudを使用すると、 TiDB Cloud Premiumインスタンスから外部storageサービスにデータをエクスポートできます。エクスポートしたデータは、バックアップ、移行、データ分析、その他の目的に使用できます。

[mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)やTiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、 TiDB Cloudが提供するエクスポート機能は、 TiDB Cloud Premiumインスタンスからデータをエクスポートするためのより便利で効率的な方法を提供します。この機能には、次のような利点があります。

-   利便性：エクスポートサービスを利用することで、 TiDB Cloud Premiumインスタンスからデータをエクスポートするためのシンプルで使いやすい方法が実現し、追加のツールやリソースは不要になります。
-   分離性：エクスポートサービスは独立したコンピューティングリソースを使用するため、オンラインサービスで使用されるリソースから確実に分離されます。
-   一貫性：エクスポートサービスは、ロックを発生させることなくエクスポートされたデータの一貫性を保証します。これにより、オンラインサービスに影響はありません。

> **注記：**
>
> エクスポートの最大サイズは1 TiBです。この制限を超えるエクスポートは失敗する可能性があります。より多くのデータをエクスポートする場合、またはエクスポート速度の向上を希望する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 輸出先 {#export-locations}

データを以下の外部storage場所にエクスポートできます。

-   [Amazon S3](https://aws.amazon.com/s3/)
-   [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
-   [Alibaba Cloudオブジェクトストレージサービス（OSS）](https://www.alibabacloud.com/product/oss)

### Amazon S3 {#amazon-s3}

データをAmazon S3にエクスポートするには、以下の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   以下のいずれかのアクセス認証情報：
    -   [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): アクセスキーに`s3:PutObject`権限があることを確認してください。
    -   [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) ：ロールARN（Amazonリソースネーム）に`s3:PutObject`権限が付与されていることを確認してください。なお、ロールARNはAWS上でホストされているTiDB Cloud Premiumインスタンスのみがサポートしています。

詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。

### Azure Blob Storage {#azure-blob-storage}

Azure Blob Storage にデータをエクスポートするには、以下の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   アクセス資格情報: Azure Blob Storage コンテナーの[共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。 SAS トークンに、 `Container`および`Object`リソースに対する`Read`および`Write`アクセス許可があることを確認してください。

詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSSにデータをエクスポートするには、以下の情報を提供する必要があります。

-   URI: `oss://<bucket-name>/<folder-path>/`
-   アクセス資格情報: Alibaba Cloud アカウントの[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)。 AccessKey ペアに`oss:PutObject`と`oss:GetBucketInfo`権限があることを確認してください。

詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)参照してください。

## エクスポートオプション {#export-options}

### データフィルタリング {#data-filtering}

TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

データを以下の形式でエクスポートできます。

-   `SQL` ：データをSQL形式でエクスポートします。
-   `CSV` ：データをCSV形式でエクスポートします。以下のオプションを指定できます。
    -   `delimiter` : エクスポートされたデータで使用される区切り文字を指定します。デフォルトの区切り文字は`"`です。
    -   `separator` : エクスポートされたデータ内のフィールドを区切るために使用される文字を指定します。デフォルトの区切り文字は`,`です。
    -   `header` ：エクスポートされたデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    -   `null-value` : エクスポートされたデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。

スキーマとデータは、以下の命名規則に従ってエクスポートされます。

| アイテム       | 圧縮されていない                      | 圧縮                                 |
| ---------- | ----------------------------- | ---------------------------------- |
| データベーススキーマ | {database}-schema-create.sql  | {データベース}-スキーマ作成.sql.{圧縮タイプ}        |
| テーブルスキーマ   | {データベース}.{テーブル}-スキーマ.sql      | {データベース}.{テーブル}-スキーマ.sql.{圧縮タイプ}   |
| データ        | {database}.{table}.{0001}.csv | {データベース}.{テーブル}.{0001}.csv.{圧縮タイプ} |
| データ        | {データベース}.{テーブル}.{0001}.sql    | {データベース}.{テーブル}.{0001}.sql.{圧縮タイプ} |

### データ圧縮 {#data-compression}

エクスポートされたCSVデータとSQLデータは、以下のアルゴリズムを使用して圧縮できます。

-   `gzip` (デフォルト): エクスポートされたデータを`gzip`で圧縮します。
-   `snappy` : エクスポートされたデータを`snappy`で圧縮します。
-   `zstd` : エクスポートされたデータを`zstd`で圧縮します。
-   `none` ：エクスポートされたデータを圧縮しない。

## 例 {#examples}

### データをAmazon S3にエクスポートする {#export-data-to-amazon-s3}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 左上隅にあるコンボボックスを使用して、組織、プロジェクト、インスタンスを切り替えることができます。

2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「エクスポート」**をクリックします。

3.  **エクスポート**ページで、右上隅にある**「データのエクスポート」**をクリックします。次に、以下の設定を行います。

    -   **タスク名**：エクスポートタスクの名前を入力してください。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **ソース接続**： TiDB Cloud Premiumインスタンスの**ユーザー名**と**パスワード**を入力し、 **「接続テスト」**をクリックして認証情報を確認します。
    -   **ターゲット接続**：
        -   **ストレージプロバイダー**：Amazon S3を選択してください。
        -   **フォルダURI** ：Amazon S3のURIを`s3://<bucket-name>/<folder-path>/`形式で入力してください。
        -   **バケットへのアクセス**：以下のアクセス認証情報から1つを選択し、認証情報を入力してください。
            -   **AWS ロール ARN** : バケットにアクセスする権限を持つロール ARN を入力します。 AWS CloudFormation を使用してロール ARN を作成することをお勧めします。詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。
            -   **AWSアクセスキー**：バケットへのアクセス権限を持つアクセスキーIDとアクセスキーシークレットを入力してください。
    -   **エクスポートするデータ**：エクスポートするデータベースまたはテーブルを選択してください。
    -   **データ形式**： **SQL**または**CSV**を選択してください。
    -   **圧縮**： **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択してください。

4.  **「エクスポート」**をクリックします。

### データをAzure Blob Storageにエクスポートする {#export-data-to-azure-blob-storage}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 左上隅にあるコンボボックスを使用して、組織、プロジェクト、インスタンスを切り替えることができます。

2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「エクスポート」**をクリックします。

3.  **エクスポート**ページで、右上隅にある**「データのエクスポート」**をクリックします。次に、以下の設定を行います。

    -   **タスク名**：エクスポートタスクの名前を入力してください。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **ソース接続**： TiDB Cloud Premiumインスタンスの**ユーザー名**と**パスワード**を入力し、 **「接続テスト」**をクリックして認証情報を確認します。
    -   **ターゲット接続**：
        -   **ストレージプロバイダー**：Azure Blob Storageを選択してください。
        -   **フォルダー URI** : Azure Blob Storage の URI を`azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式で入力します。
        -   **SAS トークン**: コンテナーへのアクセス権限を持つ SAS トークンを入力します。 [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/)を使用して SAS トークンを作成することをお勧めします。詳細については、 [外部ストレージへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)参照してください。
    -   **エクスポートするデータ**：エクスポートするデータベースまたはテーブルを選択してください。
    -   **データ形式**： **SQL**または**CSV**を選択してください。
    -   **圧縮**： **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択してください。

4.  **「エクスポート」**をクリックします。

### データをAlibaba Cloud OSSにエクスポート {#export-data-to-alibaba-cloud-oss}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 左上隅にあるコンボボックスを使用して、組織、プロジェクト、インスタンスを切り替えることができます。

2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「エクスポート」**をクリックします。

3.  **エクスポート**ページで、右上隅にある**「データのエクスポート」を**クリックします。

    -   **タスク名**：エクスポートタスクの名前を入力してください。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **ソース接続**： TiDB Cloud Premiumインスタンスの**ユーザー名**と**パスワード**を入力し、 **「接続テスト」**をクリックして認証情報を確認します。
    -   **ターゲット接続**：
        -   **ストレージプロバイダー**：Alibaba Cloud OSSを選択してください。
        -   **フォルダーURI** ：データをエクスポートするAlibaba Cloud OSS URIを`oss://<bucket-name>/<folder-path>/`形式で入力します。
        -   **アクセスキーID**と**アクセスキーシークレット**：バケットへのアクセス権限を持つアクセスキーIDとアクセスキーシークレットを入力してください。
    -   **エクスポートするデータ**：エクスポートするデータベースまたはテーブルを選択してください。
    -   **データ形式**： **SQL**または**CSV**を選択してください。
    -   **圧縮**： **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択してください。

4.  **「エクスポート」**をクリックします。

### エクスポートタスクをキャンセルする {#cancel-an-export-task}

進行中のエクスポートタスクをキャンセルするには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 左上隅にあるコンボボックスを使用して、組織、プロジェクト、インスタンスを切り替えることができます。

2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「エクスポート」**をクリックします。

3.  **エクスポート**ページで、エクスポートタスク一覧を表示します。

4.  キャンセルしたいエクスポートタスクを選択し、 **[アクション]**をクリックします。

5.  ドロップダウンリストから**「キャンセル」**を選択してください。なお、キャンセルできるのは「**実行中」**ステータスのエクスポートタスクのみです。
