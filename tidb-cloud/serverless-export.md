---
title: Export Data from TiDB Cloud Serverless
summary: TiDB Cloud Serverless クラスターからデータをエクスポートする方法を学習します。
---

# TiDB Cloud Serverlessからデータをエクスポート {#export-data-from-tidb-cloud-serverless}

TiDB Cloud Serverless Export（ベータ版）は、 TiDB Cloud Serverless クラスターからローカルファイルまたは外部storageサービスにデータをエクスポートできるサービスです。エクスポートしたデータは、バックアップ、移行、データ分析などの用途に使用できます。

[mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)や TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、 TiDB Cloud Serverless Export を使用すると、 TiDB Cloud Serverless クラスターからより便利かつ効率的にデータをエクスポートできます。これには以下の利点があります。

-   利便性: エクスポート サービスは、 TiDB Cloud Serverless クラスターからデータをエクスポートするためのシンプルで使いやすい方法を提供するため、追加のツールやリソースは必要ありません。
-   分離: エクスポート サービスは個別のコンピューティング リソースを使用するため、オンライン サービスで使用されるリソースからの分離が確保されます。
-   一貫性: エクスポート サービスは、ロックを発生させることなくエクスポートされたデータの一貫性を確保するため、オンライン サービスには影響しません。

> **注記：**
>
> 現在、最大エクスポートサイズは1TiBです。より多くのデータをエクスポートする場合、またはより高速なエクスポートをご希望の場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## エクスポート場所 {#export-locations}

次の場所にデータをエクスポートできます。

-   ローカルファイル
-   外部storageには以下が含まれます:

    -   [アマゾンS3](https://aws.amazon.com/s3/)
    -   [Googleクラウドストレージ](https://cloud.google.com/storage)
    -   [Azure BLOB ストレージ](https://azure.microsoft.com/en-us/services/storage/blobs/)
    -   [Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/product/oss)

> **注記：**
>
> エクスポートするデータのサイズが大きい場合（100GiBを超える場合）は、外部storageにエクスポートすることをお勧めします。

### ローカルファイル {#a-local-file}

TiDB Cloud Serverless クラスターからローカル ファイルにデータをエクスポートするには、データ[TiDB Cloudコンソールを使用する](#export-data-to-a-local-file)または[TiDB Cloud CLIを使用する](/tidb-cloud/ticloud-serverless-export-create.md)エクスポートし、エクスポートしたデータをTiDB Cloud CLI を使用してダウンロードする必要があります。

データをローカル ファイルにエクスポートする場合、次の制限があります。

-   TiDB Cloudコンソールを使用してエクスポートされたデータをダウンロードすることはサポートされていません。
-   エクスポートされたデータはTiDB Cloudのスタッシングエリアに保存され、2日後に有効期限が切れます。エクスポートしたデータは期限内にダウンロードする必要があります。
-   スタッシング領域のstorageスペースがいっぱいの場合、データをローカル ファイルにエクスポートすることはできません。

### アマゾンS3 {#amazon-s3}

データを Amazon S3 にエクスポートするには、次の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   次のアクセス資格情報のいずれか:
    -   [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) : アクセス キーに`s3:PutObject`および`s3:ListBucket`権限があることを確認します。
    -   [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) : ロールARN（Amazonリソースネーム）に`s3:PutObject`と`s3:ListBucket`権限があることを確認してください。このロールARNはAWSでホストされているクラスターでのみサポートされることに注意してください。

詳細については[Amazon S3 アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)参照してください。

### Googleクラウドストレージ {#google-cloud-storage}

Google Cloud Storage にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `gs://<bucket-name>/<folder-path>/`
-   アクセス認証情報：バケットの**Base64エンコードされた**[サービスアカウントキー](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)サービスアカウントキーに`storage.objects.create`権限があることを確認してください。

詳細については[GCS アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-gcs-access)参照してください。

### Azure BLOB ストレージ {#azure-blob-storage}

Azure Blob Storage にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   アクセス資格情報: Azure Blob Storage コンテナーの[共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) 。SAS トークンに、 `Container`と`Object`リソースに対する`Read`と`Write`権限があることを確認してください。

詳細については[Azure Blob Storage アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSS にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `oss://<bucket-name>/<folder-path>/`
-   アクセス認証情報：Alibaba Cloudアカウントの[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)バケットへのデータエクスポートを許可するために、AccessKeyペア`oss:GetBucketInfo` `oss:PutObject` `oss:ListBuckets`権限があることを確認してください。

For more information, see [Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

## エクスポートオプション {#export-options}

### データフィルタリング {#data-filtering}

-   TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。
-   TiDB Cloud CLI は、SQL ステートメントと[テーブルフィルター](/table-filter.md)使用したデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

次の形式でデータをエクスポートできます。

-   `SQL` : SQL 形式でデータをエクスポートします。
-   `CSV` : CSV形式でデータをエクスポートします。以下のオプションを指定できます。
    -   `delimiter` : エクスポートデータで使用する区切り文字を指定します。デフォルトの区切り文字は`"`です。
    -   `separator` : エクスポートデータのフィールド区切りに使用する文字を指定します。デフォルトの区切り文字は`,`です。
    -   `header` : エクスポートデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    -   `null-value` : エクスポートデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。
-   `Parquet` : Parquet 形式でデータをエクスポートします。

スキーマとデータは、次の命名規則に従ってエクスポートされます。

| アイテム       | 圧縮されていない                                 | 圧縮                                                                                   |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------ |
| データベーススキーマ | {データベース}-schema-create.sql               | {データベース}-schema-create.sql.{圧縮タイプ}                                                   |
| テーブルスキーマ   | {データベース}.{テーブル}-schema.sql               | {データベース}.{テーブル}-schema.sql.{圧縮タイプ}                                                   |
| データ        | {データベース}.{テーブル}.{0001}.{csv|parquet|sql} | {データベース}.{テーブル}.{0001}.{csv|sql}.{圧縮タイプ}<br/> {データベース}.{テーブル}.{0001}.{圧縮タイプ}.parquet |

### データ圧縮 {#data-compression}

次のアルゴリズムを使用して、エクスポートされた CSV および SQL データを圧縮できます。

-   `gzip` (デフォルト): エクスポートされたデータを`gzip`で圧縮します。
-   `snappy` : エクスポートされたデータを`snappy`で圧縮します。
-   `zstd` : エクスポートされたデータを`zstd`で圧縮します。
-   `none` : エクスポートした`data`を圧縮しません。

次のアルゴリズムを使用して、エクスポートされた Parquet データを圧縮できます。

-   `zstd` (デフォルト): Parquet ファイルを`zstd`で圧縮します。
-   `gzip` : Parquet ファイルを`gzip`で圧縮します。
-   `snappy` : Parquet ファイルを`snappy`で圧縮します。
-   `none` : Parquet ファイルを圧縮しません。

### データ変換 {#data-conversion}

データを Parquet 形式にエクスポートする場合、 TiDB Cloud Serverless と Parquet 間のデータ変換は次のようになります。

| TiDB Cloudサーバーレス タイプ | Parquestプリミティブ型 | Parquet論理型                                 |
| -------------------- | --------------- | ------------------------------------------ |
| 可変長文字                | バイト配列           | 文字列(UTF8)                                  |
| 時間                   | バイト配列           | String(UTF8)                               |
| 小さなテキスト              | バイト配列           | 文字列(UTF8)                                  |
| 中テキスト                | バイト配列           | 文字列(UTF8)                                  |
| TEXT                 | バイト配列           | 文字列(UTF8)                                  |
| LONGTEXT             | バイト配列           | 文字列(UTF8)                                  |
| セット                  | バイト配列           | 文字列(UTF8)                                  |
| JSON                 | バイト配列           | 文字列(UTF8)                                  |
| 日付                   | バイト配列           | 文字列(UTF8)                                  |
| チャー                  | バイト配列           | 文字列(UTF8)                                  |
| ベクター                 | バイト配列           | 文字列(UTF8)                                  |
| 小数点(1&lt;=p&lt;=9)   | INT32           | DECIMAL(p,s)                               |
| 小数点(10&lt;=p&lt;=18) | INT64           | DECIMAL(p,s)                               |
| 小数点(p&gt;=19)        | バイト配列           | 文字列(UTF8)                                  |
| ENUM                 | バイト配列           | 文字列(UTF8)                                  |
| タイムスタンプ              | INT64           | TIMESTAMP(単位=MICROS、isAdjustedToUTC=false) |
| 日時                   | INT64           | TIMESTAMP(単位=MICROS、isAdjustedToUTC=false) |
| 年                    | INT32           | /                                          |
| タイニーイント              | INT32           | /                                          |
| 符号なし TINYINT         | INT32           | /                                          |
| スモールイント              | INT32           | /                                          |
| 符号なしスモール整数           | INT32           | /                                          |
| ミディアムミント             | INT32           | /                                          |
| 署名なしのメディアミント         | INT32           | /                                          |
| INT                  | INT32           | /                                          |
| 符号なし整数               | 固定長バイト配列(9)     | 10進数(20,0)                                 |
| ビッグイント               | 固定長バイト配列(9)     | 10進数(20,0)                                 |
| 符号なしBIGINT           | バイト配列           | 文字列(UTF8)                                  |
| フロート                 | フロート            | /                                          |
| ダブル                  | ダブル             | /                                          |
| ブロブ                  | バイト配列           | /                                          |
| タイニーブロブ              | バイト配列           | /                                          |
| ミディアムブロブ             | バイト配列           | /                                          |
| LONGBLOB             | バイト配列           | /                                          |
| バイナリ                 | バイト配列           | /                                          |
| VARBINARY            | バイト配列           | /                                          |
| 少し                   | バイト配列           | /                                          |

## 例 {#examples}

### データをローカルファイルにエクスポートする {#export-data-to-a-local-file}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「ローカルファイル」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。

    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。

    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。

    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。

    > **ヒント：**
    >
    > クラスターでこれまでにデータのインポートもエクスポートもしたことがない場合は、ページの下部にある**[データをエクスポートするにはここをクリックします...]**をクリックしてデータをエクスポートする必要があります。

4.  **［エクスポート］**をクリックします。

5.  エクスポート タスクが成功したら、エクスポート タスクの詳細に表示されるダウンロード コマンドをコピーし、 [TiDB CloudCLI](/tidb-cloud/cli-reference.md)でコマンドを実行してエクスポートされたデータをダウンロードできます。

</div>

<div label="CLI">

1.  エクスポート タスクを作成します。

    ```shell
    ticloud serverless export create -c <cluster-id>
    ```

    出力からエクスポート ID が取得されます。

2.  After the export task is successful, download the exported data to your local file:

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

    ダウンロード コマンドの詳細については、 [ticloud サーバーレスエクスポートのダウンロード](/tidb-cloud/ticloud-serverless-export-download.md)参照してください。

</div>
</SimpleTab>

### Amazon S3にデータをエクスポートする {#export-data-to-amazon-s3}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Amazon S3」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **フォルダー URI** : `s3://<bucket-name>/<folder-path>/`形式で Amazon S3 の URI を入力します。
    -   **バケット アクセス**: 次のアクセス資格情報のいずれかを選択し、資格情報を入力します。
        -   **AWS ロール ARN** : バケットへのアクセス権を持つロール ARN を入力します。AWS CloudFormation を使用してロール ARN を作成することをお勧めします。詳細については、 [TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)参照してください。
        -   **AWS アクセスキー**: バケットにアクセスする権限を持つアクセスキー ID とアクセスキーシークレットを入力します。

4.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

-   `s3.uri` : `s3://<bucket-name>/<folder-path>/`形式の Amazon S3 URI。
-   `s3.access-key-id`: the access key ID of the user who has the permission to access the bucket.
-   `s3.secret-access-key` : バケットにアクセスする権限を持つユーザーのアクセスキーシークレット。
-   `s3.role-arn` : バケットにアクセスする権限を持つロール ARN。

</div>
</SimpleTab>

### Export data to Google Cloud Storage {#export-data-to-google-cloud-storage}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  On the **Import** page, click **Export Data to** in the upper-right corner, and then choose **Google Cloud Storage** from the drop-down list. Fill in the following parameters:

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **フォルダ URI** : Google Cloud Storage の URI を`gs://<bucket-name>/<folder-path>/`形式で入力します。
    -   **バケット アクセス**: バケットにアクセスする権限を持つ Google Cloud 認証情報ファイルをアップロードします。

4.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type GCS --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter "database.table"
```

-   `gcs.uri` : `gs://<bucket-name>/<folder-path>/`形式の Google Cloud Storage バケットの URI。
-   `gcs.service-account-key` : base64 でエンコードされたサービス アカウント キー。

</div>
</SimpleTab>

### Azure Blob Storage にデータをエクスポートする {#export-data-to-azure-blob-storage}

<SimpleTab>
<div label="Console">

1.  Log in to the [TiDB Cloudコンソール](https://tidbcloud.com/) and navigate to the [**クラスター**](https://tidbcloud.com/project/clusters) page of your project.

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Azure Blob Storage」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **Folder URI**: enter the URI of Azure Blob Storage with the `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` format.
    -   **SASトークン**: コンテナへのアクセス権を持つSASトークンを入力します[Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/)でSASトークンを作成することをお勧めします。詳細については、 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)参照してください。

4.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

-   `azblob.uri` : `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式の Azure Blob Storage の URI。
-   `azblob.sas-token`: the account SAS token of the Azure Blob Storage.

</div>
</SimpleTab>

### Alibaba Cloud OSSへのデータのエクスポート {#export-data-to-alibaba-cloud-oss}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  **「インポート」**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Alibaba Cloud OSS」**を選択します。

4.  次のパラメータを入力してください。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **Folder URI**: enter the Alibaba Cloud OSS URI where you want to export the data, in the `oss://<bucket-name>/<folder-path>/` format.
    -   **AccessKey ID**と**AccessKey Secret** : バケットにアクセスする権限を持つ AccessKey ID と AccessKey Secret を入力します。

5.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type OSS --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter "database.table"
```

-   `oss.uri` : データをエクスポートする Alibaba Cloud OSS URI ( `oss://<bucket-name>/<folder-path>/`形式)。
-   `oss.access-key-id` : バケットにアクセスする権限を持つユーザーの AccessKey ID。
-   `oss.access-key-secret`: the AccessKey secret of the user who has the permission to access the bucket.

</div>
</SimpleTab>

### Cancel an export task {#cancel-an-export-task}

進行中のエクスポート タスクをキャンセルするには、次の手順を実行します。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**Clusters**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

3.  **[インポート]**ページで**[エクスポート]**をクリックして、エクスポート タスク リストを表示します。

4.  キャンセルするエクスポート タスクを選択し、 **[アクション]**をクリックします。

5.  ドロップダウンリストから**「キャンセル」**を選択します。キャンセルできるのは、**実行**中のエクスポートタスクのみです。

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## エクスポート速度 {#export-speed}

エクスポート速度は[クラスタープラン](/tidb-cloud/select-cluster-tier.md#cluster-plans)によって異なります。詳細については、次の表をご覧ください。

| プラン                   | エクスポート速度    |
| :-------------------- | :---------- |
| 無料クラスタープラン            | 最大25 MiB/秒  |
| Scalable cluster plan | 最大100 MiB/秒 |

## 価格 {#pricing}

The export service is free during the beta period. You only need to pay for the [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process of successful or canceled tasks. For failed export tasks, you will not be charged.
