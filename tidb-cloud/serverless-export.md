---
title: Export Data from TiDB Cloud Starter or Essential
summary: TiDB Cloud Starter またはTiDB Cloud Essential クラスターからデータをエクスポートする方法を学習します。
---

# TiDB Cloud StarterまたはEssentialからデータをエクスポートする {#export-data-from-tidb-cloud-starter-or-essential}

TiDB Cloudを使用すると、 TiDB Cloud StarterまたはEssentialクラスターからローカルファイルまたは外部ストレージサービスにデータをエクスポートできます。エクスポートしたデータは、バックアップ、移行、データ分析などの用途に使用できます。

[mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)や TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、 TiDB Cloudが提供するエクスポート機能は、クラスターからデータをエクスポートするためのより便利で効率的な方法を提供します。これには、次のような利点があります。

-   利便性: エクスポート サービスは、クラスターからデータをエクスポートするためのシンプルで使いやすい方法を提供するため、追加のツールやリソースは必要ありません。
-   分離: エクスポート サービスは個別のコンピューティング リソースを使用するため、オンライン サービスで使用されるリソースからの分離が保証されます。
-   一貫性: エクスポート サービスは、ロックを発生させることなくエクスポートされたデータの一貫性を確保するため、オンライン サービスには影響しません。

> **Note:**
>
> 現在、最大エクスポートサイズは1 TiBです。より多くのデータをエクスポートする場合、またはより高速なエクスポートをご希望の場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## エクスポート場所 {#export-locations}

次の場所にデータをエクスポートできます。

-   {{{ .starter }}} の場合:

    -   ローカルファイル
    -   Amazon S3
    -   Google Cloud Storage
    -   Azure Blob Storage
    -   Alibaba Cloud Object Storage Service (OSS)

-   {{{ .essential }}} の場合:

    -   Amazon S3
    -   Azure Blob Storage
    -   Alibaba Cloud Object Storage Service (OSS)

> **Note:**
>
> エクスポートするデータのサイズが大きい場合（100 GiB 以上）は、外部ストレージにエクスポートすることをお勧めします。

### ローカルファイル {#a-local-file}

{{{ .starter }}} インスタンスからローカル ファイルにデータをエクスポートするには、データ[TiDB Cloudコンソールを使用する](#export-data-to-a-local-file)または[TiDB Cloud CLIを使用する](/tidb-cloud/ticloud-serverless-export-create.md)エクスポートし、エクスポートしたデータをTiDB Cloud CLI を使用してダウンロードする必要があります。

データをローカル ファイルにエクスポートする場合、次の制限があります。

-   TiDB Cloudコンソールを使用してエクスポートされたデータをダウンロードすることはサポートされていません。
-   エクスポートされたデータはTiDB Cloudのステージングエリアに保存され、2日後に有効期限が切れます。エクスポートしたデータは期限内にダウンロードする必要があります。
-   ステージング領域のストレージスペースがいっぱいの場合、データをローカル ファイルにエクスポートすることはできません。

### アマゾンS3 {#amazon-s3}

Amazon S3 にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   次のいずれかのアクセス資格情報:
    -   [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) : アクセス キーに`s3:PutObject`と`s3:ListBucket`権限があることを確認します。
    -   [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) : ロールARN（Amazonリソースネーム）に`s3:PutObject`と`s3:ListBucket`権限があることを確認してください。このロールARNはAWSでホストされているクラスターでのみサポートされることに注意してください。

詳細については[Amazon S3 アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)を参照してください。

### Googleクラウドストレージ {#google-cloud-storage}

Google Cloud Storage にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `gs://<bucket-name>/<folder-path>/`
-   アクセス認証情報: バケットの**Base64エンコードされた**[サービスアカウントキー](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) 。サービスアカウントキーに`storage.objects.create`権限があることを確認してください。

詳細については[GCS アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)を参照してください。

### Azure BLOB ストレージ {#azure-blob-storage}

Azure Blob Storage にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   アクセス資格情報: Azure Blob Storage コンテナーの[共有アクセス署名（SAS）トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) 。SAS トークンに、 `Container`と`Object`リソースに対する`Read`と`Write`権限があることを確認してください。

詳細については[Azure Blob Storage アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)を参照してください。

### アリババクラウドOSS {#alibaba-cloud-oss}

Alibaba Cloud OSS にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `oss://<bucket-name>/<folder-path>/`
-   アクセス資格情報：Alibaba Cloudアカウントの[アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)ペアに`oss:PutObject`と`oss:GetBucketInfo`権限があることを確認してください。

詳細については[Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)を参照してください。

## エクスポートオプション {#export-options}

### データフィルタリング {#data-filtering}

-   TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。
-   TiDB Cloud CLI は、SQL ステートメントと[テーブルフィルター](/table-filter.md)を使用したデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

次の形式でデータをエクスポートできます。

-   `SQL` : SQL 形式でデータをエクスポートします。
-   `CSV` : CSV形式でデータをエクスポートします。以下のオプションを指定できます。
    -   `delimiter` : エクスポートデータで使用する区切り文字を指定します。デフォルトの区切り文字は`"`です。
    -   `separator` : エクスポートデータのフィールド区切りに使用する文字を指定します。デフォルトの区切り文字は`,`です。
    -   `header` : エクスポートデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    -   `null-value` : エクスポートデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。
-   `Parquet` : Parquet 形式でデータをエクスポートします。これは {{{ .starter }}} データのエクスポートにのみ適用されます。

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

データを Parquet 形式にエクスポートする場合、TiDB と Parquet 間のデータ変換は次のようになります。

| TiDB Cloud Serverlessの型 | Parquet プリミティブ型 | Parquet 論理型                              |
|----------------------------|------------------------|--------------------------------------------|
| VARCHAR                    | BYTE_ARRAY             | String(UTF8)                               |
| TIME                       | BYTE_ARRAY             | String(UTF8)                               |
| TINYTEXT                   | BYTE_ARRAY             | String(UTF8)                               |
| MEDIUMTEXT                 | BYTE_ARRAY             | String(UTF8)                               |
| TEXT                       | BYTE_ARRAY             | String(UTF8)                               |
| LONGTEXT                   | BYTE_ARRAY             | String(UTF8)                               |
| SET                        | BYTE_ARRAY             | String(UTF8)                               |
| JSON                       | BYTE_ARRAY             | String(UTF8)                               |
| DATE                       | BYTE_ARRAY             | String(UTF8)                               |
| CHAR                       | BYTE_ARRAY             | String(UTF8)                               |
| VECTOR                     | BYTE_ARRAY             | String(UTF8)                               |
| DECIMAL(1<=p<=9)           | INT32                  | DECIMAL(p,s)                               |
| DECIMAL(10<=p<=18)         | INT64                  | DECIMAL(p,s)                               |
| DECIMAL(p>=19)             | BYTE_ARRAY             | String(UTF8)                               |
| ENUM                       | BYTE_ARRAY             | String(UTF8)                               |
| TIMESTAMP                  | INT64                  | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| DATETIME                   | INT64                  | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| YEAR                       | INT32                  | /                                          |
| TINYINT                    | INT32                  | /                                          |
| UNSIGNED TINYINT           | INT32                  | /                                          |
| SMALLINT                   | INT32                  | /                                          |
| UNSIGNED SMALLINT          | INT32                  | /                                          |
| MEDIUMINT                  | INT32                  | /                                          |
| UNSIGNED MEDIUMINT         | INT32                  | /                                          |
| INT                        | INT32                  | /                                          |
| UNSIGNED INT               | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                              |
| BIGINT                     | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                              |
| UNSIGNED BIGINT            | BYTE_ARRAY             | String(UTF8)                               |
| FLOAT                      | FLOAT                  | /                                          |
| DOUBLE                     | DOUBLE                 | /                                          |
| BLOB                       | BYTE_ARRAY             | /                                          |
| TINYBLOB                   | BYTE_ARRAY             | /                                          |
| MEDIUMBLOB                 | BYTE_ARRAY             | /                                          |
| LONGBLOB                   | BYTE_ARRAY             | /                                          |
| BINARY                     | BYTE_ARRAY             | /                                          |
| VARBINARY                  | BYTE_ARRAY             | /                                          |
| BIT                        | BYTE_ARRAY             | /                                          |

## 例 {#examples}

### データをローカルファイルにエクスポートする {#export-data-to-a-local-file}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット {{{ .starter }}} インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「ローカルファイル」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。

    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。

    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。

    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択します。

    > **Tip:**
    >
    > {{{ .starter }}} インスタンスでこれまでにデータのインポートもエクスポートもしたことがない場合は、ページの下部にある**[ここをクリックしてデータをエクスポートします...]**をクリックしてデータをエクスポートする必要があります。

4.  **［エクスポート］**をクリックします。

5.  エクスポート タスクが成功したら、エクスポート タスクの詳細に表示されるダウンロード コマンドをコピーし、 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md)でコマンドを実行してエクスポートされたデータをダウンロードできます。

</div>

<div label="CLI">

1.  エクスポート タスクを作成します。

    ```shell
    ticloud serverless export create -c <cluster-id>
    ```

    出力からエクスポート ID が取得されます。

2.  エクスポート タスクが成功したら、エクスポートされたデータをローカル ファイルにダウンロードします。

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

    ダウンロード コマンドの詳細については、 [ticloud サーバーレスエクスポートのダウンロード](/tidb-cloud/ticloud-serverless-export-download.md)を参照してください。

</div>
</SimpleTab>

### Amazon S3にデータをエクスポートする {#export-data-to-amazon-s3}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Amazon S3」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択します。
    -   **フォルダー URI** : `s3://<bucket-name>/<folder-path>/`形式で Amazon S3 の URI を入力します。
    -   **バケット アクセス**: 次のアクセス資格情報のいずれかを選択し、資格情報を入力します。
        -   **AWS ロール ARN** : バケットへのアクセス権を持つロール ARN を入力します。AWS CloudFormation を使用してロール ARN を作成することをお勧めします。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)を参照してください。
        -   **AWS アクセスキー**: バケットにアクセスする権限を持つアクセスキー ID とアクセスキーシークレットを入力します。

4.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

-   `s3.uri` : `s3://<bucket-name>/<folder-path>/`形式の Amazon S3 URI。
-   `s3.access-key-id` : バケットにアクセスする権限を持つユーザーのアクセス キー ID。
-   `s3.secret-access-key` : バケットにアクセスする権限を持つユーザーのアクセス キー シークレット。
-   `s3.role-arn` : バケットにアクセスする権限を持つロール ARN。

</div>
</SimpleTab>

### Google Cloud Storage にデータをエクスポートする {#export-data-to-google-cloud-storage}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット {{{ .starter }}} インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Google Cloud Storage」**を選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択します。
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

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Azure Blob Storage」を**選択します。以下のパラメータを入力します。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択します。
    -   **フォルダー URI** : `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式で Azure Blob Storage の URI を入力します。
    -   **SASトークン**: コンテナへのアクセス権を持つSASトークンを入力します。2でSASトークンを作成することをお勧めします。詳細については、 [Azure Blob Storage アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access) [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/)してください。

4.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

-   `azblob.uri` : `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式の Azure Blob Storage の URI。
-   `azblob.sas-token` : Azure Blob Storage のアカウント SAS トークン。

</div>
</SimpleTab>

### Alibaba Cloud OSSへのデータのエクスポート {#export-data-to-alibaba-cloud-oss}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

3.  **「インポート」**ページで、右上隅の**「データのエクスポート先」**をクリックし、ドロップダウンリストから**「Alibaba Cloud OSS」**を選択します。

4.  次のパラメータを入力してください。

    -   **タスク名**: エクスポートタスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、または**None**を選択します。
    -   **フォルダー URI** : データをエクスポートする Alibaba Cloud OSS URI を`oss://<bucket-name>/<folder-path>/`形式で入力します。
    -   **AccessKey ID**と**AccessKey Secret** : バケットにアクセスする権限を持つ AccessKey ID と AccessKey Secret を入力します。

5.  **［エクスポート］**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type OSS --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter "database.table"
```

-   `oss.uri` : データをエクスポートする Alibaba Cloud OSS URI ( `oss://<bucket-name>/<folder-path>/`形式)。
-   `oss.access-key-id` : バケットにアクセスする権限を持つユーザーの AccessKey ID。
-   `oss.access-key-secret` : バケットにアクセスする権限を持つユーザーの AccessKey シークレット。

</div>
</SimpleTab>

### エクスポートタスクをキャンセルする {#cancel-an-export-task}

進行中のエクスポート タスクをキャンセルするには、次の手順を実行します。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート] を**クリックします。

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

エクスポート速度は[クラスタープラン](/tidb-cloud/select-cluster-tier.md)によって異なります:

-   **TiDB Cloud Starter**:

    -   使用制限を 0 に設定すると、エクスポート速度は最大 25 MiB/s になります。
    -   支出限度額が 0 より大きい場合、エクスポート速度は最大 100 MiB/s になります。

-   **TiDB Cloud Essential** : 最大 100 MiB/秒。
