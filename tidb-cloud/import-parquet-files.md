---
title:  Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# AmazonS3またはGCSからTiDB CloudにApacheParquetファイルをインポートします {#import-apache-parquet-files-from-amazon-s3-or-gcs-into-tidb-cloud}

非圧縮データファイルとSnappy圧縮[アパッチパーケット](https://parquet.apache.org/)形式データファイルの両方をTiDB Cloudにインポートできます。このドキュメントでは、ParquetファイルをAmazon Simple Storage Service（Amazon S3）またはGoogle Cloud Storage（GCS）からTiDB Cloudにインポートする方法について説明します。

> **ノート：**
>
> TiDB Cloudは、Parquetファイルの空のテーブルへのインポートのみをサポートします。すでにデータが含まれている既存のテーブルにデータをインポートするには、 TiDB Cloudを使用して、このドキュメントに従って一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。

## ステップ1.寄木細工のファイルを準備します {#step-1-prepare-the-parquet-files}

> **ノート：**
>
> 現在、 TiDB Cloudは、次のデータ型のいずれかを含むParquetファイルのインポートをサポートしていません。インポートするParquetファイルにそのようなデータ型が含まれている場合は、最初に[サポートされているデータ型](#supported-data-types) （たとえば、 `STRING` ）を使用してParquetファイルを再生成する必要があります。または、AWS Glueなどのサービスを使用して、データ型を簡単に変換することもできます。
>
> -   `LIST`
> -   `NEST STRUCT`
> -   `BOOL`
> -   `ARRAY`
> -   `MAP`

1.  Parquetファイルが256MBより大きい場合は、ファイルをそれぞれ256MB前後のサイズの小さなファイルに分割することを検討してください。

    TiDB Cloudは、非常に大きなParquetファイルのインポートをサポートしていますが、サイズが約256MBの複数の入力ファイルで最高のパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並行して処理できるため、インポート速度が大幅に向上するためです。

2.  バケット内の既存のオブジェクトの命名規則に従って、インポートする寄木細工のファイルの名前と一致するテキストパターンを特定します。

    たとえば、バケット内のすべてのデータファイルをインポートするには、ワイルドカード記号`*`または`*.parquet`をパターンとして使用できます。同様に、パーティション`station=402260`にデータファイルのサブセットをインポートするには、 `*station=402260*`をパターンとして使用できます。 [ステップ4](#step-4-import-parquet-files-to-tidb-cloud)でTiDB Cloudに提供する必要があるため、このパターンをメモしてください。

## 手順2.ターゲットデータベースとテーブルスキーマを作成します {#step-2-create-the-target-database-and-table-schema}

ParquetファイルをTiDB Cloudにインポートする前に、ターゲットデータベースとテーブルを作成する必要があります。または、次のようにターゲットデータベースとテーブルスキーマを指定すると、 TiDB Cloudはインポートプロセスの一部としてこれらのオブジェクトを作成できます。

1.  寄木細工のファイルが配置されているAmazonS3またはGCSディレクトリに、 `CREATE DATABASE`ステートメントを含む`${db_name}-schema-create.sql`ファイルを作成します。

    たとえば、次のステートメントを含む`mydb-scehma-create.sql`のファイルを作成できます。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE mydb;
    ```

2.  寄木細工のファイルが配置されているAmazonS3またはGCSディレクトリに、 `CREATE TABLE`ステートメントを含む`${db_name}.${table_name}-schema.sql`ファイルを作成します。

    たとえば、次のステートメントを含む`mydb.mytable-schema.sql`のファイルを作成できます。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE mytable (
    ID INT,
    REGION VARCHAR(20),
    COUNT INT );
    ```

    > **ノート：**
    >
    > `${db_name}.${table_name}-schema.sql`のファイルには、1つのDDLステートメントのみを含める必要があります。ファイルに複数のDDLステートメントが含まれている場合、最初のステートメントのみが有効になります。

## 手順3.クロスアカウントアクセスを構成する {#step-3-configure-cross-account-access}

TiDBCloudがTiDB CloudまたはGCSバケット内のParquetファイルにアクセスできるようにするには、次のいずれかを実行します。

-   ParquetファイルがAmazonS3にある場合、 [AmazonS3へのクロスアカウントアクセスを設定します](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access) 。

    終了したら、 [ステップ4](#step-4-import-parquet-files-to-tidb-cloud)で必要になるため、役割ARN値をメモします。

-   ParquetファイルがGCSにある場合は、 [GCSへのクロスアカウントアクセスを構成する](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-gcs-access) 。

## ステップ4.ParquetファイルをTiDB Cloudにインポートする {#step-4-import-parquet-files-to-tidb-cloud}

ParquetファイルをTiDB Cloudにインポートするには、次の手順を実行します。

1.  [TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックします。ターゲットクラスタの概要ページが表示されます。

2.  左側のクラスタ情報ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。

3.  [**データインポートタスク]**ページで、次の情報を入力します。

    -   **データソースタイプ**：データソースのタイプを選択します。
    -   **バケットURL** ：Parquetファイルが配置されているバケットURLを選択します。
    -   **データ形式**：<strong>寄木細工</strong>を選択します。
    -   **クレデンシャルのセットアップ**（このフィールドはAWS S3でのみ表示されます）： <strong>Role-ARNの</strong>RoleARN値を入力します。
    -   **ターゲットデータベース**： <strong>[ユーザー名]</strong>フィールドと[<strong>パスワード</strong>]フィールドに入力します。
    -   **DB /テーブルフィルター**：必要に応じて、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter#cli)を指定できます。
    -   **オブジェクト名パターン**：インポートするParquetファイルの名前と一致するパターンを入力します。たとえば、 `my-data.parquet` 。
    -   **ターゲットテーブル名**：ターゲットテーブルの名前を入力します。たとえば、 `mydb.mytable` 。

4.  [**インポート]**をクリックします。

    データベースリソースの消費に関する警告メッセージが表示されます。

5.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケットURLのデータにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポートタスクが自動的に開始されます。 `AccessDenied`エラーが発生した場合は、 [S3からのデータインポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

6.  インポートの進行状況が成功を示したら、TotalFilesの後の数を確認し**ます**。

    数値がゼロの場合は、[**オブジェクト名パターン]**フィールドに入力した値と一致するデータファイルがないことを意味します。この場合、「<strong>オブジェクト名パターン」</strong>フィールドにタイプミスがあるかどうかを確認して、再試行してください。

インポートタスクの実行時に、サポートされていない変換または無効な変換が検出されると、 TiDB Cloudはインポートジョブを自動的に終了し、インポートエラーを報告します。

インポートエラーが発生した場合は、次の手順を実行してください。

1.  部分的にインポートされたテーブルを削除します。

2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。

3.  Parquetファイルのデータ型を確認してください。

    Parquetファイルにサポートされていないデータ型（たとえば、 `NEST STRUCT` 、または`ARRAY` ）が含まれている場合は、 `MAP` （たとえば、 [サポートされているデータ型](#supported-data-types) ）を使用して`STRING`ファイルを再生成する必要があります。

4.  インポートタスクを再試行してください。

## サポートされているデータ型 {#supported-data-types}

次の表に、TiDBCloudにインポートできるサポートされているTiDB Cloudデータ型を示します。

| 寄木細工のプリミティブタイプ          | 寄木細工の論理タイプ       | TiDBまたはMySQLのタイプ                                                                                                                                                                               |
| ----------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ダブル                     | ダブル              | ダブル<br/>浮く                                                                                                                                                                                     |
| FIXED_LEN_BYTE_ARRAY（9） | DECIMAL（20,0）    | BIGINT UNSIGNED                                                                                                                                                                                |
| FIXED_LEN_BYTE_ARRAY（N） | DECIMAL（p、s）     | 10進数<br/>数値                                                                                                                                                                                    |
| INT32                   | DECIMAL（p、s）     | 10進数<br/>数値                                                                                                                                                                                    |
| INT32                   | 該当なし             | INT<br/> MEDIUMINT<br/>年                                                                                                                                                                       |
| INT64                   | DECIMAL（p、s）     | 10進数<br/>数値                                                                                                                                                                                    |
| INT64                   | 該当なし             | BIGINT<br/> INT UNSIGNED<br/> MEDIUMINT UNSIGNED                                                                                                                                               |
| INT64                   | TIMESTAMP_MICROS | 日付時刻<br/>タイムスタンプ                                                                                                                                                                               |
| BYTE_ARRAY              | 該当なし             | バイナリ<br/>少し<br/>BLOB<br/> CHAR<br/> LINESTRING<br/> LONGBLOB<br/> MEDIUMBLOB<br/> MULTILINESTRING<br/> TINYBLOB<br/> VARBINARY                                                                 |
| BYTE_ARRAY              | ストリング            | ENUM<br/>日にち<br/>10進数<br/>幾何学<br/>GEOMETRYCOLLECTION<br/> JSON<br/> LONGTEXT<br/> MEDIUMTEXT<br/>マルチポイント<br/>MULTIPOLYGON<br/>数値<br/>点<br/>ポリゴン<br/>設定<br/>文章<br/>時間<br/>TINYTEXT<br/> VARCHAR |
| SMALLINT                | 該当なし             | INT32                                                                                                                                                                                          |
| SMALLINT UNSIGNED       | 該当なし             | INT32                                                                                                                                                                                          |
| TINYINT                 | 該当なし             | INT32                                                                                                                                                                                          |
| TINYINT UNSIGNED        | 該当なし             | INT32                                                                                                                                                                                          |
