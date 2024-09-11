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

データをローカル ファイルまたは[アマゾンS3](https://aws.amazon.com/s3/)にエクスポートできます。

> **注記：**
>
> エクスポートするデータのサイズが大きい場合（100 GiB 以上）は、外部storageにエクスポートすることをお勧めします。

### ローカルファイル {#a-local-file}

TiDB Cloud Serverless クラスターからローカル ファイルにデータをエクスポートするには、データ[TiDB Cloudコンソールを使用する](#export-data-to-a-local-file)または[TiDB CloudCLIを使用する](/tidb-cloud/ticloud-serverless-export-create.md)エクスポートし、 TiDB Cloud CLI を使用してエクスポートしたデータをダウンロードする必要があります。

データをローカル ファイルにエクスポートする場合、次の制限があります。

-   TiDB Cloudコンソールを使用してエクスポートされたデータをダウンロードすることはサポートされていません。
-   エクスポートされたデータはTiDB Cloudのスタッシング領域に保存され、2 日後に期限切れになります。エクスポートされたデータは時間内にダウンロードする必要があります。
-   スタッシング領域のstorageスペースがいっぱいの場合、データをローカル ファイルにエクスポートすることはできません。

### アマゾンS3 {#amazon-s3}

データを Amazon S3 にエクスポートするには、次の情報を提供する必要があります。

-   URI: `s3://<bucket-name>/<file-path>`
-   次のアクセス資格情報のいずれか:
    -   [アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) : アクセス キーに`s3:PutObject`および`s3:ListBucket`権限があることを確認します。
    -   [ロールARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) : ロール ARN に`s3:PutObject`および`s3:ListBucket`権限があることを確認します。

詳細については[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)参照してください。

## エクスポートオプション {#export-options}

### データのフィルタリング {#data-filtering}

-   TiDB Cloudコンソールは、選択したデータベースとテーブルを含むデータのエクスポートをサポートしています。

### データ形式 {#data-formats}

次の形式でデータをエクスポートできます。

-   `SQL` : SQL 形式でデータをエクスポートします。
-   `CSV` : CSV 形式でデータをエクスポートします。次のオプションを指定できます。
    -   `delimiter` : エクスポートされたデータで使用する区切り文字を指定します。デフォルトの区切り文字は`"`です。
    -   `separator` : エクスポートされたデータ内のフィールドを区切るために使用される文字を指定します。デフォルトの区切り文字は`,`です。
    -   `header` : エクスポートされたデータにヘッダー行を含めるかどうかを指定します。デフォルト値は`true`です。
    -   `null-value` : エクスポートされたデータ内の NULL 値を表す文字列を指定します。デフォルト値は`\N`です。

スキーマとデータは、次の命名規則に従ってエクスポートされます。

| アイテム       | 圧縮されていない                         | 圧縮                                       |
| ---------- | -------------------------------- | ---------------------------------------- |
| データベーススキーマ | {データベース}-スキーマ作成.sql              | {データベース}-schema-create.sql.{圧縮タイプ}       |
| テーブルスキーマ   | {データベース}.{テーブル}-schema.sql       | {データベース}.{テーブル}-schema.sql.{圧縮タイプ}       |
| データ        | {データベース}.{テーブル}.{0001}.{csv|sql} | {データベース}.{テーブル}.{0001}.{csv|sql}.{圧縮タイプ} |

### データ圧縮 {#data-compression}

次のアルゴリズムを使用して、エクスポートされた CSV および SQL データを圧縮できます。

-   `gzip` (デフォルト): エクスポートされたデータを`gzip`で圧縮します。
-   `snappy` : エクスポートされたデータを`snappy`で圧縮します。
-   `zstd` : エクスポートされたデータを`zstd`で圧縮します。
-   `none` : エクスポートした`data`圧縮しません。

## 手順 {#steps}

### データをローカルファイルにエクスポートする {#export-data-to-a-local-file}

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**[データのエクスポート先] を**クリックし、ドロップダウン リストから**[ローカル ファイル]**を選択します。次のパラメータを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。

    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。

    -   **データ形式**: **SQL ファイル**または**CSV を**選択します。

    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなしを**選択します。

    > **ヒント：**
    >
    > クラスターでこれまでにデータをインポートまたはエクスポートしたことがない場合は、ページの下部にある**[データをエクスポートするには、ここをクリックします...] をクリックしてデータをエクスポートする**必要があります。

4.  **[エクスポート]を**クリックします。

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

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

3.  **インポート**ページで、右上隅の**[データのエクスポート先] を**クリックし、ドロップダウン リストから**[Amazon S3]**を選択します。次のパラメータを入力します。

    -   **タスク名**: エクスポート タスクの名前を入力します。デフォルト値は`SNAPSHOT_{snapshot_time}`です。
    -   **エクスポートされたデータ**: エクスポートするデータベースとテーブルを選択します。
    -   **データ形式**: **SQL ファイル**または**CSV を**選択します。
    -   **圧縮**: **Gzip** 、 **Snappy** 、 **Zstd** 、また**はなしを**選択します。
    -   **フォルダー URI** : `s3://<bucket-name>/<folder-path>/`形式で Amazon S3 の URI を入力します。
    -   **バケット アクセス**: 次のアクセス資格情報のいずれかを選択し、資格情報を入力します。資格情報がない場合は、 [TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)を参照してください。
        -   **AWS ロール ARN** : バケットにアクセスするための`s3:PutObject`および`s3:ListBucket`権限を持つロール ARN を入力します。
        -   **AWS アクセスキー**: バケットにアクセスするための`s3:PutObject`と`s3:ListBucket`の権限を持つアクセスキー ID とアクセスキーシークレットを入力します。

4.  **[エクスポート]を**クリックします。

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --s3.bucket-uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key>
```

-   `s3.bucket-uri` : `s3://<bucket-name>/<file-path>`形式の Amazon S3 URI。
-   `s3.access-key-id` : バケットにアクセスする権限を持つユーザーのアクセスキー ID。
-   `s3.secret-access-key` : バケットにアクセスする権限を持つユーザーのアクセスキーシークレット。

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

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

3.  **[インポート]**ページで**[エクスポート]**をクリックして、エクスポート タスク リストを表示します。

4.  キャンセルするエクスポート タスクを選択し、 **[アクション]**をクリックします。

5.  ドロップダウン リストで**[キャンセル] を**選択します。**実行中**ステータスのエクスポート タスクのみをキャンセルできることに注意してください。

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## 価格 {#pricing}

ベータ期間中、エクスポート サービスは無料です。成功したタスクまたはキャンセルされたタスクのエクスポート プロセス中に生成された[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)に対してのみお支払いいただく必要があります。失敗したエクスポート タスクについては、料金は発生しません。
