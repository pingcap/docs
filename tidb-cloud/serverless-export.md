---
title: Export Data from TiDB Cloud Serverless
summary: TiDB Cloud Serverless クラスターからデータをエクスポートする方法を学びます。
---

# TiDB Cloud Serverless からデータをエクスポート {#export-data-from-tidb-cloud-serverless}

TiDB Cloud Serverless Export (ベータ版) は、 TiDB Cloud Serverless クラスターからローカル ファイルまたは外部storageサービスにデータをエクスポートできるサービスです。エクスポートされたデータは、バックアップ、移行、データ分析などの目的で使用できます。

[mysqlダンプ](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)や TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、 TiDB Cloud Serverless Export を使用すると、 TiDB Cloud Serverless クラスターからデータをエクスポートするより便利で効率的な方法が提供されます。これには次の利点があります。

-   利便性: エクスポート サービスは、 TiDB Cloud Serverless クラスターからデータをエクスポートするためのシンプルで使いやすい方法を提供するため、追加のツールやリソースは必要ありません。
-   分離: エクスポート サービスは個別のコンピューティング リソースを使用するため、オンライン サービスで使用されるリソースからの分離が保証されます。
-   一貫性: エクスポート サービスは、ロックを発生させることなくエクスポートされたデータの一貫性を確保するため、オンライン サービスには影響しません。

## エクスポート場所 {#export-locations}

次の場所にデータをエクスポートできます。

-   ローカルファイル
-   外部storageには以下が含まれます:

    -   [アマゾンS3](https://aws.amazon.com/s3/)
    -   [Google クラウド ストレージ](https://cloud.google.com/storage)
    -   [Azure BLOB ストレージ](https://azure.microsoft.com/en-us/services/storage/blobs/)

> **注記：**
>
> エクスポートするデータのサイズが大きい場合（100 GiB 以上）は、外部storageにエクスポートすることをお勧めします。

### ローカルファイル {#a-local-file}

TiDB Cloud Serverless クラスターからローカル ファイルにデータをエクスポートするには、データ[TiDB Cloudコンソールを使用する](#export-data-to-a-local-file)または[TiDB CloudCLIを使用する](/tidb-cloud/ticloud-serverless-export-create.md)エクスポートし、 TiDB Cloud CLI を使用してエクスポートしたデータをダウンロードする必要があります。

データをローカル ファイルにエクスポートする場合、次の制限があります。

-   TiDB Cloudコンソールを使用してエクスポートされたデータをダウンロードすることはサポートされていません。
-   エクスポートされたデータはTiDB Cloudの保管領域に保存され、2 日後に期限切れになります。エクスポートされたデータは時間内にダウンロードする必要があります。
-   スタッシング領域のstorageスペースがいっぱいの場合、データをローカル ファイルにエクスポートすることはできません。

### アマゾンS3 {#amazon-s3}

データを Amazon S3 にエクスポートするには、次の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<folder-path>/`
-   次のアクセス資格情報のいずれか:
    -   [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) : アクセス キーに`s3:PutObject`および`s3:ListBucket`権限があることを確認します。
    -   [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) : ロール ARN (Amazon リソース名) に`s3:PutObject`と`s3:ListBucket`権限があることを確認します。

詳細については[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)参照してください。

### Google クラウド ストレージ {#google-cloud-storage}

データを Google Cloud Storage にエクスポートするには、次の情報を提供する必要があります。

-   URI: `gs://<bucket-name>/<folder-path>/`
-   アクセス認証情報: バケットの**base64 エンコードされた**[サービスアカウントキー](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)サービス アカウント キーに`storage.objects.create`権限があることを確認してください。

詳細については[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-gcs-access)参照してください。

### Azure BLOB ストレージ {#azure-blob-storage}

Azure Blob Storage にデータをエクスポートするには、次の情報を提供する必要があります。

-   URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`または`https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
-   アクセス資格情報: Azure Blob Storage コンテナーの場合は[共有アクセス署名 (SAS) トークン](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)トークンに、 `Container`および`Object`リソースに対する`Read`および`Write`アクセス許可があることを確認します。

詳細については[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)参照してください。

## エクスポートオプション {#export-options}

### データのフィルタリング {#data-filtering}

-   TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。
-   TiDB Cloud CLI は、SQL ステートメントと[テーブルフィルター](/table-filter.md)使用したデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

次の形式でデータをエクスポートできます。

-   `SQL` : SQL 形式でデータをエクスポートします。
-   `CSV` : CSV 形式でデータをエクスポートします。次のオプションを指定できます。
    -   `delimiter` : エクスポートされたデータで使用する区切り文字を指定します。デフォルトの区切り文字は`"`です。
    -   `separator` : エクスポートされたデータ内のフィールドを区切るために使用される文字を指定します。デフォルトの区切り文字は`,`です。
    -   `header` : エクスポートされたデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    -   `null-value` : エクスポートされたデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。
-   `Parquet` : データを Parquet 形式でエクスポートします。

スキーマとデータは、次の命名規則に従ってエクスポートされます。

| アイテム       | 圧縮されていない                                 | 圧縮                                                                                   |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------------------------ |
| データベーススキーマ | {データベース}-スキーマ作成.sql                      | {データベース}-schema-create.sql.{圧縮タイプ}                                                   |
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

| TiDB Cloudサーバーレスタイプ  | Parquest プリミティブ型 | Parquet 論理型                                |
| -------------------- | ---------------- | ------------------------------------------ |
| バルチャー                | バイト配列            | 文字列(UTF8)                                  |
| 時間                   | バイト配列            | 文字列(UTF8)                                  |
| 小さなテキスト              | バイト配列            | 文字列(UTF8)                                  |
| 中テキスト                | バイト配列            | 文字列(UTF8)                                  |
| TEXT                 | バイト配列            | 文字列(UTF8)                                  |
| 長文                   | バイト配列            | 文字列(UTF8)                                  |
| セット                  | バイト配列            | 文字列(UTF8)                                  |
| 翻訳                   | バイト配列            | 文字列(UTF8)                                  |
| 日付                   | バイト配列            | 文字列(UTF8)                                  |
| 文字                   | バイト配列            | 文字列(UTF8)                                  |
| ベクター                 | バイト配列            | 文字列(UTF8)                                  |
| 小数点(1&lt;=p&lt;=9)   | INT32            | 10進数(p,s)                                  |
| 小数点(10&lt;=p&lt;=18) | INT64            | 10進数(p,s)                                  |
| 小数点(p&gt;=19)        | バイト配列            | 文字列(UTF8)                                  |
| 列挙                   | バイト配列            | 文字列(UTF8)                                  |
| タイムスタンプ              | INT64            | TIMESTAMP(単位=MICROS、isAdjustedToUTC=false) |
| 日時                   | INT64            | TIMESTAMP(単位=MICROS、isAdjustedToUTC=false) |
| 年                    | INT32            | /                                          |
| 小さな                  | INT32            | /                                          |
| 符号なし TINYINT         | INT32            | /                                          |
| スモールイント              | INT32            | /                                          |
| 符号なし小整数              | INT32            | /                                          |
| ミディアムミント             | INT32            | /                                          |
| 未署名のメディアミント          | INT32            | /                                          |
| 内部                   | INT32            | /                                          |
| 符号なし整数               | 固定長バイト配列(9)      | 10進数(20,0)                                 |
| ビッグイント               | 固定長バイト配列(9)      | 10進数(20,0)                                 |
| 符号なしBIGINT           | バイト配列            | 文字列(UTF8)                                  |
| フロート                 | フロート             | /                                          |
| ダブル                  | ダブル              | /                                          |
| ブロブ                  | バイト配列            | /                                          |
| タイニーブロブ              | バイト配列            | /                                          |
| ミディアムブロブ             | バイト配列            | /                                          |
| ロングロブ                | バイト配列            | /                                          |
| バイナリ                 | バイト配列            | /                                          |
| バイナリ                 | バイト配列            | /                                          |
| 少し                   | バイト配列            | /                                          |

## 例 {#examples}

### データをローカルファイルにエクスポートする {#export-data-to-a-local-file}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

3.  **インポート**ページで、右上隅の**[データのエクスポート先]**をクリックし、ドロップダウン リストから**[ローカル ファイル]**を選択します。次のパラメータを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。

    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。

    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。

    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。

    > **ヒント：**
    >
    > クラスターでこれまでにデータをインポートまたはエクスポートしたことがない場合は、ページの下部にある**[ここをクリックしてデータをエクスポート...]**をクリックしてデータをエクスポートする必要があります。

4.  **[エクスポート]**をクリックします。

5.  エクスポート タスクが成功したら、エクスポート タスクの詳細に表示されるダウンロード コマンドをコピーし、 [TiDB CloudCLI](/tidb-cloud/cli-reference.md)でコマンドを実行してエクスポートされたデータをダウンロードできます。

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

    ダウンロードコマンドの詳細については、 [ticloud サーバーレス エクスポート ダウンロード](/tidb-cloud/ticloud-serverless-export-download.md)参照してください。

</div>
</SimpleTab>

### Amazon S3にデータをエクスポートする {#export-data-to-amazon-s3}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

3.  **インポート**ページで、右上隅の**[データのエクスポート先]**をクリックし、ドロップダウン リストから**[Amazon S3]**を選択します。次のパラメータを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **フォルダー URI** : `s3://<bucket-name>/<folder-path>/`形式で Amazon S3 の URI を入力します。
    -   **バケット アクセス**: 次のアクセス資格情報のいずれかを選択し、資格情報を入力します。
        -   **AWS ロール ARN** : バケットにアクセスする権限を持つロール ARN を入力します。AWS CloudFormation を使用してロール ARN を作成することをお勧めします。詳細については、 [TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)参照してください。
        -   **AWS アクセスキー**: バケットにアクセスする権限を持つアクセスキー ID とアクセスキーシークレットを入力します。

4.  **[エクスポート]**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

-   `s3.uri` : `s3://<bucket-name>/<folder-path>/`形式の Amazon S3 URI。
-   `s3.access-key-id` : バケットにアクセスする権限を持つユーザーのアクセスキー ID。
-   `s3.secret-access-key` : バケットにアクセスする権限を持つユーザーのアクセスキーシークレット。
-   `s3.role-arn` : バケットにアクセスする権限を持つロール ARN。

</div>
</SimpleTab>

### Google Cloud Storage にデータをエクスポートする {#export-data-to-google-cloud-storage}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

3.  **[インポート]**ページで、右上隅の**[データのエクスポート**先] をクリックし、ドロップダウン リストから**[Google Cloud Storage]**を選択します。次のパラメータを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **フォルダ URI** : `gs://<bucket-name>/<folder-path>/`形式で Google Cloud Storage の URI を入力します。
    -   **バケット アクセス**: バケットにアクセスする権限を持つ Google Cloud 認証情報ファイルをアップロードします。

4.  **[エクスポート]**をクリックします。

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

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

3.  **[インポート]**ページで、右上隅の**[データのエクスポート**先] をクリックし、ドロップダウン リストから**[Azure Blob Storage]**を選択します。次のパラメーターを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL** 、 **CSV** 、または**Parquet を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなし**を選択します。
    -   **フォルダー URI** : `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式で Azure Blob Storage の URI を入力します。
    -   **SAS トークン**: コンテナーへのアクセス許可を持つ SAS トークンを入力します。 [Azure ARM テンプレート](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/)を使用して SAS トークンを作成することをお勧めします。詳細については、 [TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)参照してください。

4.  **[エクスポート]**をクリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

-   `azblob.uri` : `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`形式の Azure Blob Storage の URI。
-   `azblob.sas-token` : Azure Blob Storage のアカウント SAS トークン。

</div>
</SimpleTab>

### エクスポートタスクをキャンセルする {#cancel-an-export-task}

進行中のエクスポート タスクをキャンセルするには、次の手順を実行します。

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

3.  **[インポート]**ページで**[エクスポート]**をクリックして、エクスポート タスク リストを表示します。

4.  キャンセルするエクスポート タスクを選択し、 **[アクション]**をクリックします。

5.  ドロップダウン リストで**[キャンセル]**を選択します。**実行中**ステータスのエクスポート タスクのみをキャンセルできることに注意してください。

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## 価格 {#pricing}

ベータ期間中、エクスポート サービスは無料です。成功したタスクまたはキャンセルされたタスクのエクスポート プロセス中に生成された[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)に対してのみお支払いいただく必要があります。失敗したエクスポート タスクについては、料金は発生しません。
