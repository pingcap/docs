---
title: Export Data from TiDB Serverless
summary: Learn how to export data from TiDB Serverless clusters.
---

# TiDB Serverless からデータをエクスポート {#export-data-from-tidb-serverless}

TiDB Serverless Export (ベータ版) は、TiDB Serverless クラスターからローカルstorageまたは外部storageサービスにデータをエクスポートできるサービスです。エクスポートされたデータは、バックアップ、移行、データ分析などの目的で使用できます。

[mysqlダンプ](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)や TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)などのツールを使用してデータをエクスポートすることもできますが、TiDB Serverless Export を使用すると、TiDB Serverless クラスターからデータをエクスポートするより便利で効率的な方法が提供されます。これには次の利点があります。

-   利便性: エクスポート サービスは、TiDB Serverless クラスターからデータをエクスポートするためのシンプルで使いやすい方法を提供するため、追加のツールやリソースは必要ありません。
-   分離: エクスポート サービスは個別のコンピューティング リソースを使用するため、オンライン サービスで使用されるリソースからの分離が保証されます。
-   一貫性: エクスポート サービスは、ロックを発生させることなくエクスポートされたデータの一貫性を確保するため、オンライン サービスには影響しません。

## 特徴 {#features}

このセクションでは、TiDB Serverless Export の機能について説明します。

### エクスポート場所 {#export-location}

データをローカルstorageまたは[アマゾンS3](https://aws.amazon.com/s3/)にエクスポートできます。

> **注記：**
>
> エクスポートするデータのサイズが大きい場合 (100 GiB 以上) は、Amazon S3 にエクスポートすることをお勧めします。

**ローカルstorage**

データをローカルstorageにエクスポートする場合、次の制限があります。

-   複数のデータベースを同時にローカルstorageにエクスポートすることはサポートされていません。
-   エクスポートされたデータはスタッシングエリアに保存され、2日後に期限切れになります。エクスポートされたデータは時間内にダウンロードする必要があります。
-   スタッシング領域のstorageスペースがいっぱいの場合、データをローカルstorageにエクスポートすることはできません。

**アマゾンS3**

データを Amazon S3 にエクスポートするには、S3 バケットに[アクセスキー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)指定する必要があります。アクセス キーに S3 バケットの読み取りおよび書き込みアクセス権があり、少なくとも`s3:PutObject`と`s3:ListBucket`の権限が含まれていることを確認してください。

### データのフィルタリング {#data-filtering}

エクスポートするデータベースとテーブルを指定して、データをフィルタリングできます。テーブルを指定せずにデータベースを指定すると、指定したデータベース内のすべてのテーブルがエクスポートされます。Amazon S3 にデータをエクスポートするときにデータベースを指定しないと、クラスター内のすべてのデータベースがエクスポートされます。

> **注記：**
>
> データをローカルstorageにエクスポートする場合は、データベースを指定する必要があります。

### データ形式 {#data-formats}

次の形式でデータをエクスポートできます。

-   `SQL` (デフォルト): データを SQL 形式でエクスポートします。
-   `CSV` : データを CSV 形式でエクスポートします。

スキーマとデータは、次の命名規則に従ってエクスポートされます。

| アイテム       | 圧縮されていない                         | 圧縮                                       |
| ---------- | -------------------------------- | ---------------------------------------- |
| データベーススキーマ | {データベース}-スキーマ作成.sql              | {データベース}-schema-create.sql.{圧縮タイプ}       |
| テーブルスキーマ   | {データベース}.{テーブル}-schema.sql       | {データベース}.{テーブル}-schema.sql.{圧縮タイプ}       |
| データ        | {データベース}.{テーブル}.{0001}.{sql|csv} | {データベース}.{テーブル}.{0001}.{sql|csv}.{圧縮タイプ} |

### データ圧縮 {#data-compression}

次のアルゴリズムを使用してエクスポートされたデータを圧縮できます。

-   `gzip` (デフォルト): エクスポートされたデータを gzip で圧縮します。
-   `snappy` : エクスポートされたデータを snappy で圧縮します。
-   `zstd` : エクスポートされたデータを zstd で圧縮します。
-   `none` : エクスポートされたデータを圧縮しません。

### エクスポートをキャンセル {#cancel-export}

実行状態にあるエクスポート タスクをキャンセルできます。

## 例 {#examples}

現在、 [TiDB CloudCLI](/tidb-cloud/cli-reference.md)を使用してエクスポート タスクを管理できます。

### データをローカルstorageにエクスポートする {#export-data-to-local-storage}

1.  エクスポートするデータベースとテーブルを指定するエクスポート タスクを作成します。

    ```shell
    ticloud serverless export create -c <cluster-id> --database <database> --table <table>
    ```

    出力からエクスポート ID が取得されます。

2.  エクスポートが成功したら、エクスポートしたデータをローカルstorageにダウンロードします。

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

### Amazon S3にデータをエクスポートする {#export-data-to-amazon-s3}

```shell
ticloud serverless export create -c <cluster-id> --bucket-uri <bucket-uri> --access-key-id <access-key-id> --secret-access-key <secret-access-key>
```

### CSV形式でエクスポート {#export-with-the-csv-format}

```shell
ticloud serverless export create -c <cluster-id> --file-type CSV
```

### データベース全体をエクスポートする {#export-the-whole-database}

```shell
ticloud serverless export create -c <cluster-id> --database <database>
```

### スナップ圧縮でエクスポート {#export-with-snappy-compression}

```shell
ticloud serverless export create -c <cluster-id> --compress snappy
```

### エクスポートタスクをキャンセルする {#cancel-an-export-task}

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

## 価格 {#pricing}

ベータ期間中、エクスポート サービスは無料です。成功したタスクまたはキャンセルされたタスクのエクスポート プロセス中に生成された[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)に対してのみお支払いいただく必要があります。失敗したエクスポート タスクについては、料金は発生しません。
