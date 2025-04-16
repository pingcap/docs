---
title: Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless
summary: Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud Object Storage Service (OSS) からTiDB Cloud Serverless に CSV ファイルをインポートする方法を学習します。
---

# Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud OSS から CSV ファイルをTiDB Cloud Serverless にインポートする {#import-csv-files-from-amazon-s3-gcs-azure-blob-storage-or-alibaba-cloud-oss-into-tidb-cloud-serverless}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、Azure Blob Storage、または Alibaba Cloud Object Storage Service (OSS) からTiDB Cloud Serverless に CSV ファイルをインポートする方法について説明します。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB Cloud Serverless では空のテーブルへのCSVファイルのインポートのみが許可されています。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従ってTiDB Cloud Serverless を使用して一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータを対象の既存テーブルにコピーします。

## ステップ1.CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSV ファイルが 256 MB より大きい場合は、サイズがそれぞれ約 256 MB の小さなファイルに分割することを検討してください。

    TiDB Cloud Serverlessは非常に大きなCSVファイルのインポートをサポートしていますが、256MB程度の複数の入力ファイルで最適なパフォーマンスを発揮します。これは、 TiDB Cloud Serverlessが複数のファイルを並列処理できるため、インポート速度が大幅に向上するからです。

2.  CSV ファイルに次のように名前を付けます。

    -   CSV ファイルにテーブル全体のすべてのデータが含まれている場合は、データをインポートするときに`${db_name}.${table_name}`テーブルにマップされる`${db_name}.${table_name}.csv`形式でファイルに名前を付けます。

    -   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値のサフィックスを追加してください。例： `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`数値のサフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さを揃えるため、数値の前にゼロを追加する必要があります。

    -   TiDB Cloud Serverlessは、以下の形式の圧縮ファイルのインポートをサポートしています： `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy` 。圧縮されたCSVファイルをインポートする場合は、ファイル名を`${db_name}.${table_name}.${suffix}.csv.${compress}`形式にしてください。13 `${suffix}`オプションで、「000001」などの任意の整数にすることができます。例えば、 `trips.000001.csv.gz`ファイルを`bikeshare.trips`テーブルにインポートする場合は、ファイル名を`bikeshare.trips.000001.csv.gz`に変更する必要があります。

    > **注記：**
    >
    > -   パフォーマンスを向上させるには、各圧縮ファイルのサイズを 100 MiB に制限することをお勧めします。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。
    > -   非圧縮ファイルの場合、前述のルールに従って CSV ファイル名を更新できないケース (たとえば、CSV ファイル リンクが他のプログラムでも使用されている場合) は、ファイル名を変更せずに、 [ステップ4](#step-4-import-csv-files-to-tidb-cloud-serverless)の**マッピング設定**を使用してソース データを単一のターゲット テーブルにインポートできます。

## ステップ2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schemas}

CSV ファイルにはスキーマ情報が含まれていないため、CSV ファイルからTiDB Cloud Serverless にデータをインポートする前に、次のいずれかの方法でテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloud Serverless で、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: CSV ファイルが保存されている Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud Object Storage Service ディレクトリで、次のようにソース データのターゲット テーブル スキーマ ファイルを作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        CSVファイルが[ステップ1](#step-1-prepare-the-csv-files)の命名規則に従っている場合、データのインポート時にデータベーススキーマファイルはオプションです。それ以外の場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式で、 `CREATE DATABASE` DDLステートメントを含んでいる必要があります。このファイルを使用して、 TiDB Cloud Serverlessはデータをインポートする際に、データを格納するための`${db_name}`データベースを作成します。

        たとえば、次のステートメントを含む`mydb-scehma-create.sql`ファイルを作成すると、 TiDB Cloud Serverless はデータをインポートするときに`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        CSV ファイルが保存されている Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud Object Storage Service ディレクトリにテーブル スキーマ ファイルを含めない場合、 TiDB Cloud Serverless はデータをインポートしたときに対応するテーブルを作成しません。

        各テーブルスキーマファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDLステートメントを含む必要があります。このファイルを使用することで、 TiDB Cloud Serverlessはデータをインポートする際に`${db_name}`データベースに`${db_table}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、 TiDB Cloud Serverless はデータをインポートするときに`mydb`データベースに`mytable`テーブルを作成します。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注記：**
        >
        > `${db_name}.${table_name}-schema.sql`ファイルには1つのDDL文のみを含めることができます。ファイルに複数のDDL文が含まれている場合、最初の文のみが有効になります。

## ステップ3. クロスアカウントアクセスを構成する {#step-3-configure-cross-account-access}

TiDB Cloud Serverless が Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud Object Storage Service バケット内の CSV ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   CSV ファイルが Amazon S3 にある場合は、 [TiDB Cloud Serverless の外部storageアクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access) 。

    バケットにアクセスするには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、アクセスキー（アクセスキー ID とシークレットアクセスキーを含む）またはロール ARN の値をメモしておいてください。これらは[ステップ4](#step-4-import-csv-files-to-tidb-cloud-serverless)で必要になります。

-   CSV ファイルが GCS にある場合は、 [TiDB Cloud Serverless の外部storageアクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-gcs-access) 。

-   CSV ファイルが Azure Blob Storage にある場合は、 [TiDB Cloud Serverless の外部storageアクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access) 。

-   CSV ファイルが Alibaba Cloud Object Storage Service (OSS) にある場合は、 [TiDB Cloud Serverless の外部storageアクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access) 。

## ステップ4. CSVファイルをTiDB Cloud Serverlessにインポートする {#step-4-import-csv-files-to-tidb-cloud-serverless}

CSV ファイルをTiDB Cloud Serverless にインポートするには、次の手順を実行します。

<SimpleTab>
<div label="Amazon S3">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**を選択し、 **「Amazon S3」**をクリックします。

3.  **「Amazon S3 からのデータのインポート」**ページで、ソース CSV ファイルについて次の情報を入力します。

    -   **インポート ファイル数**: 必要に応じて**1 つのファイル**または**複数のファイル**を選択します。
    -   **含まれるスキーマファイル**: このフィールドは複数のファイルをインポートする場合にのみ表示されます。ソースフォルダにターゲットテーブルスキーマが含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **CSV**を選択します。
    -   **ファイルURI**または**フォルダーURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`s3://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `s3://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`s3://[bucket_name]/[data_source_folder]/` 。たとえば、 `s3://sampledata/ingest/` 。
    -   **バケットアクセス**：バケットにアクセスするには、AWSロールARNまたはAWSアクセスキーのいずれかを使用できます。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access)ご覧ください。
        -   **AWS ロール ARN** : AWS ロール ARN 値を入力します。
        -   **AWS アクセスキー**: AWS アクセスキー ID と AWS シークレットアクセスキーを入力します。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、各ターゲットテーブルとそれに対応するCSVファイルに対してカスタムマッピングルールを定義できます。その後、データソースファイルは指定されたカスタムマッピングルールを使用して再スキャンされます。

    ソースファイルのURIと名前を**「ソースファイルのURIと名前」**に入力する際は、必ず次の形式`s3://[bucket_name]/[data_source_folder]/[file_name].csv`に従ってください。例えば、 `s3://sampledata/ingest/TableName.01.csv` 。

    ソースファイルの一致にはワイルドカードも使用できます。例:

    -   `s3://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダー内の`my-data`で始まり、その後に 1 文字 ( `my-data1.csv`や`my-data2.csv`など) が続くすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    -   `s3://[bucket_name]/[data_source_folder]/my-data*.csv` : フォルダー内の`my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    サポートされているのは`?`と`*`のみであることに注意してください。

    > **注記：**
    >
    > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Google Cloud">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**を選択し、 **「Google Cloud Storage」**をクリックします。

3.  **「Google Cloud Storage からデータをインポート」**ページで、ソース CSV ファイルについて次の情報を入力します。

    -   **インポート ファイル数**: 必要に応じて**1 つのファイル**または**複数のファイル**を選択します。
    -   **含まれるスキーマファイル**: このフィールドは複数のファイルをインポートする場合にのみ表示されます。ソースフォルダにターゲットテーブルスキーマが含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **CSV**を選択します。
    -   **ファイルURI**または**フォルダーURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `[gcs|gs]://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`[gcs|gs]://[bucket_name]/[data_source_folder]/` 。たとえば、 `[gcs|gs]://sampledata/ingest/` 。
    -   **バケットアクセス**：サービスアカウントキーを使用してバケットにアクセスできます。詳細については、 [GCS アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-gcs-access)ご覧ください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、各ターゲットテーブルとそれに対応するCSVファイルに対してカスタムマッピングルールを定義できます。その後、データソースファイルは指定されたカスタムマッピングルールを使用して再スキャンされます。

    ソースファイルのURIと名前を**「ソースファイルのURIと名前」**に入力する際は、必ず次の形式`[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`に従ってください。例えば、 `[gcs|gs]://sampledata/ingest/TableName.01.csv` 。

    ソースファイルの一致にはワイルドカードも使用できます。例:

    -   `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダー内の`my-data`で始まり、その後に 1 文字 ( `my-data1.csv`や`my-data2.csv`など) が続くすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    -   `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data*.csv` : フォルダー内の`my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    サポートされているのは`?`と`*`のみであることに注意してください。

    > **注記：**
    >
    > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Azure Blob Storage">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **[Cloud Storage からデータをインポート]**を選択し、 **[Azure Blob Storage]**をクリックします。

3.  **「Azure Blob Storage からのデータのインポート」**ページで、ソース CSV ファイルについて次の情報を入力します。

    -   **インポート ファイル数**: 必要に応じて**1 つのファイル**または**複数のファイル**を選択します。
    -   **含まれるスキーマファイル**: このフィールドは複数のファイルをインポートする場合にのみ表示されます。ソースフォルダにターゲットテーブルスキーマが含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **CSV**を選択します。
    -   **ファイルURI**または**フォルダーURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `[azure|https]://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`[azure|https]://[bucket_name]/[data_source_folder]/` 。たとえば、 `[azure|https]://sampledata/ingest/` 。
    -   **バケットアクセス**：共有アクセス署名（SAS）トークンを使用してバケットにアクセスできます。詳細については、 [Azure Blob Storage アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)ご覧ください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、各ターゲットテーブルとそれに対応するCSVファイルに対してカスタムマッピングルールを定義できます。その後、データソースファイルは指定されたカスタムマッピングルールを使用して再スキャンされます。

    ソースファイルのURIと名前を**「ソースファイルのURIと名前」**に入力する際は、必ず次の形式`[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`に従ってください。例えば、 `[azure|https]://sampledata/ingest/TableName.01.csv` 。

    ソースファイルの一致にはワイルドカードも使用できます。例:

    -   `[azure|https]://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダー内の`my-data`で始まり、その後に 1 文字 ( `my-data1.csv`や`my-data2.csv`など) が続くすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    -   `[azure|https]://[bucket_name]/[data_source_folder]/my-data*.csv` : フォルダー内の`my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    サポートされているのは`?`と`*`のみであることに注意してください。

    > **注記：**
    >
    > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**を選択し、 **「Alibaba Cloud OSS」**をクリックします。

3.  **Alibaba Cloud OSS からのデータのインポート**ページで、ソース CSV ファイルについて次の情報を入力します。

    -   **インポート ファイル数**: 必要に応じて**1 つのファイル**または**複数のファイル**を選択します。
    -   **含まれるスキーマファイル**: このフィールドは複数のファイルをインポートする場合にのみ表示されます。ソースフォルダにターゲットテーブルスキーマが含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **CSV**を選択します。
    -   **ファイルURI**または**フォルダーURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`oss://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `oss://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースファイルのURIと名前を次の形式で入力します`oss://[bucket_name]/[data_source_folder]/` 。たとえば、 `oss://sampledata/ingest/` 。
    -   **バケットアクセス**：アクセスキーペアを使用してバケットにアクセスできます。詳細については、 [Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access)ご覧ください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、各ターゲットテーブルとそれに対応するCSVファイルに対してカスタムマッピングルールを定義できます。その後、データソースファイルは指定されたカスタムマッピングルールを使用して再スキャンされます。

    ソースファイルのURIと名前を**「ソースファイルのURIと名前」**に入力する際は、必ず次の形式`oss://[bucket_name]/[data_source_folder]/[file_name].csv`に従ってください。例えば、 `oss://sampledata/ingest/TableName.01.csv` 。

    ソースファイルの一致にはワイルドカードも使用できます。例:

    -   `oss://[bucket_name]/[data_source_folder]/my-data?.csv` : そのフォルダー内の`my-data`で始まり、その後に 1 文字 ( `my-data1.csv`や`my-data2.csv`など) が続くすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    -   `oss://[bucket_name]/[data_source_folder]/my-data*.csv` : フォルダー内の`my-data`で始まるすべての CSV ファイルが同じターゲット テーブルにインポートされます。

    サポートされているのは`?`と`*`のみであることに注意してください。

    > **注記：**
    >
    > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

</SimpleTab>

インポート タスクを実行するときに、サポートされていない変換または無効な変換が検出されると、 TiDB Cloud Serverless はインポート ジョブを自動的に終了し、インポート エラーを報告します。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。
2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。
3.  CSV ファイル内のデータ型を確認します。
4.  インポートタスクをもう一度試してください。

## トラブルシューティング {#troubleshooting}

### データのインポート中に警告を解決する {#resolve-warnings-during-data-import}

**[インポートの開始]**をクリックした後、 `can't find the corresponding source files`などの警告メッセージが表示された場合は、正しいソース ファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、 **[詳細設定]**を使用して変更を加えることで、この問題を解決します。

これらの問題を解決した後、データを再度インポートする必要があります。

### インポートされたテーブルに行が 0 行あります {#zero-rows-in-the-imported-tables}

インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。行数が0の場合、入力したバケットURIに一致するデータファイルが存在しないことを意味します。この場合、正しいソースファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**詳細設定**を使用して変更を加えることで問題を解決してください。その後、該当するテーブルを再度インポートしてください。
