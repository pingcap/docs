---
title:  Import CSV Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import CSV files from Amazon S3 or GCS into TiDB Cloud.
---

# AmazonS3またはGCSからTiDB CloudにCSVファイルをインポートする {#import-csv-files-from-amazon-s3-or-gcs-into-tidb-cloud}

このドキュメントでは、圧縮されていないCSVファイルをAmazon Simple Storage Service（Amazon S3）またはGoogle Cloud Storage（GCS）からTiDB Cloudにインポートする方法について説明します。

> **ノート：**
>
> -   CSVソースファイルが圧縮されている場合は、インポートする前にまずファイルを解凍する必要があります。
> -   データの一貫性を確保するために、 TiDB CloudではCSVファイルを空のテーブルにのみインポートできます。すでにデータが含まれている既存のテーブルにデータをインポートするには、 TiDB Cloudを使用して、このドキュメントに従って一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。

## 手順1.CSVファイルを準備します {#step-1-prepare-the-csv-files}

1.  CSVファイルが256MBより大きい場合は、ファイルをそれぞれ256MB前後のサイズの小さなファイルに分割することを検討してください。

    TiDB Cloudは、非常に大きなCSVファイルのインポートをサポートしていますが、サイズが約256MBの複数の入力ファイルで最高のパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並行して処理できるため、インポート速度が大幅に向上するためです。

2.  バケット内の既存のオブジェクトの命名規則に従って、インポートするCSVファイルの名前と一致するテキストパターンを特定します。

    たとえば、バケット内のすべてのデータファイルをインポートするには、ワイルドカード記号`*`または`*.csv`をパターンとして使用できます。同様に、パーティション`station=402260`にデータファイルのサブセットをインポートするには、 `*station=402260*`をパターンとして使用できます。 [ステップ4](#step-4-import-csv-files-to-tidb-cloud)でTiDB Cloudに提供する必要があるため、このパターンをメモしてください。

## 手順2.ターゲットテーブルスキーマを作成します {#step-2-create-the-target-table-schema}

CSVファイルをTiDB Cloudにインポートする前に、ターゲットデータベースとテーブルを作成する必要があります。または、次のようにターゲットデータベースとテーブルスキーマを指定すると、 TiDB Cloudはインポートプロセスの一部としてこれらのオブジェクトを作成できます。

1.  CSVファイルが配置されているAmazonS3またはGCSディレクトリに、 `CREATE DATABASE`ステートメントを含む`${db_name}-schema-create.sql`ファイルを作成します。

    たとえば、次のステートメントを含む`mydb-scehma-create.sql`のファイルを作成できます。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE mydb;
    ```

2.  CSVファイルが配置されているAmazonS3またはGCSディレクトリに、 `CREATE TABLE`ステートメントを含む`${db_name}.${table_name}-schema.sql`ファイルを作成します。

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

TiDBCloudがTiDB CloudまたはGCSバケット内のCSVファイルにアクセスできるようにするには、次のいずれかを実行します。

-   CSVファイルがAmazonS3にある場合、 [AmazonS3へのクロスアカウントアクセスを設定します](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access) 。

    終了したら、 [ステップ4](#step-4-import-csv-files-to-tidb-cloud)で必要になるため、役割ARN値をメモします。

-   CSVファイルがGCSにある場合は、 [GCSへのクロスアカウントアクセスを構成する](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-gcs-access) 。

## ステップ4.CSVファイルをTiDB Cloudにインポートする {#step-4-import-csv-files-to-tidb-cloud}

CSVファイルをTiDB Cloudにインポートするには、次の手順を実行します。

1.  [TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックします。ターゲットクラスタの概要ページが表示されます。

2.  左側のクラスタ情報ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。

3.  [**データインポートタスク]**ページで、次の情報を入力します。

    -   **データソースタイプ**：データソースのタイプを選択します。

    -   **バケットURL** ：CSVファイルが配置されているバケットURLを選択します。

    -   **データ形式**： <strong>CSV</strong>を選択します。

    -   **クレデンシャルのセットアップ**（このフィールドはAWS S3でのみ表示されます）： <strong>Role-ARNの</strong>RoleARN値を入力します。

    -   **CSVConfiguration / コンフィグレーション**：セパレーター、区切り文字、ヘッダー、非ヌル、ヌル、バックスラッシュエスケープ、トリムラストセパレーターなど、CSV固有の構成を確認して更新します。これらのフィールドのすぐ横に、各CSV構成の説明があります。

        > **ノート：**
        >
        > 区切り文字、区切り文字、およびnullの構成では、英数字と特定の特殊文字の両方を使用できます。サポートされている特殊文字には、 `\t` 、 `\r` `\n`が`\f` `\u0001` `\b` 。

    -   **ターゲットデータベース**： <strong>[ユーザー名]</strong>フィールドと[<strong>パスワード</strong>]フィールドに入力します。

    -   **DB /テーブルフィルター**：必要に応じて、 [テーブルフィルター](https://docs.pingcap.com/tidb/stable/table-filter#cli)を指定できます。

    -   **オブジェクト名パターン**：インポートするCSVファイルの名前と一致するパターンを入力します。たとえば、 `my-data.csv` 。

    -   **ターゲットテーブル名**：ターゲットテーブルの名前を入力します。たとえば、 `mydb.mytable` 。

4.  [**インポート]**をクリックします。

    データベースリソースの消費に関する警告メッセージが表示されます。

5.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケットURLのデータにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポートタスクが自動的に開始されます。 `AccessDenied`エラーが発生した場合は、 [S3からのデータインポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

6.  インポートの進行状況が成功を示したら、TotalFilesの後の数を確認し**ます**。

    数値がゼロの場合は、[**オブジェクト名パターン]**フィールドに入力した値と一致するデータファイルがないことを意味します。この場合、「<strong>オブジェクト名パターン」</strong>フィールドにタイプミスがないことを確認して、再試行してください。

インポートタスクの実行時に、サポートされていない変換または無効な変換が検出されると、 TiDB Cloudはインポートジョブを自動的に終了し、インポートエラーを報告します。

インポートエラーが発生した場合は、次の手順を実行してください。

1.  部分的にインポートされたテーブルを削除します。
2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。
3.  CSVファイルのデータ型を確認してください。
4.  インポートタスクを再試行してください。
