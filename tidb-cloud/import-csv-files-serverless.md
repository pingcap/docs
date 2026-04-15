---
title: Import CSV Files from Cloud Storage into TiDB Cloud Starter or Essential
summary: Amazon S3、GCS、Azure Blob Storage、またはAlibaba Cloud Object Storage Service (OSS) からCSVファイルをTiDB Cloud StarterまたはTiDB Cloud Essentialにインポートする方法を学びましょう。
---

# TiDB Cloud StarterまたはEssentialにクラウドストレージからCSVファイルをインポートする {#import-csv-files-from-cloud-storage-into-tidb-cloud-starter-or-essential}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、Azure Blob Storage、または Alibaba Cloud Object Storage Service (OSS) から CSV ファイルをTiDB Cloud StarterまたはTiDB Cloud Essentialにインポートする方法について説明します。

> **注記：**
>
> TiDB Cloud Dedicatedについては、[クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)参照してください。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB CloudCSV ファイルのインポートは空のテーブルにのみ許可されています。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントの手順に従って一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータを対象の既存のテーブルにコピーします。

## ステップ1. CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSVファイルが256MiBを超える場合は、それぞれ約256MiBのサイズの小さなファイルに分割することを検討してください。

    TiDB Cloudは非常に大きなCSVファイルのインポートをサポートしていますが、256MiB程度のサイズの複数の入力ファイルを扱う場合に最高のパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並列処理できるため、インポート速度を大幅に向上させることができるからです。

2.  CSVファイルの名前は以下のようにしてください。

    -   CSV ファイルにテーブル全体のデータがすべて含まれている場合は、ファイル名を`${db_name}.${table_name}.csv`形式で指定してください。この形式は、データをインポートする際に`${db_name}.${table_name}`テーブルにマッピングされます。

    -   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例えば、 `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`のようにです。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

    -   TiDB Cloudは、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` `.snappy`の各形式の圧縮ファイルのインポートをサポートしています。圧縮 CSV ファイルをインポートする場合は、ファイル名を`${db_name}.${table_name}.${suffix}.csv.${compress}`形式で指定します。この形式では、 `${suffix}`は省略可能で、「000001」などの任意の整数を指定できます。例えば、 `trips.000001.csv.gz`ファイルを`bikeshare.trips`テーブルにインポートする場合は、ファイル名を`bikeshare.trips.000001.csv.gz`に変更する必要があります。

    > **注記：**
    >
    > -   パフォーマンスを向上させるためには、各圧縮ファイルのサイズを100MiBに制限することをお勧めします。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。
    > -   非圧縮ファイルの場合、場合によっては前述のルールに従ってCSVファイル名を更新できない場合（たとえば、CSVファイルリンクが他のプログラムでも使用されている場合）、ファイル名を変更せずに、[ステップ4](#step-4-import-csv-files)の**マッピング設定**を使用してソースデータを単一のターゲットテーブルにインポートできます。

## ステップ2．対象テーブルのスキーマを作成する {#step-2-create-the-target-table-schemas}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDB Cloudにデータをインポートする前に、以下のいずれかの方法を使用してテーブルスキーマを作成する必要があります。

-   方法1： TiDB Cloudで、ソースデータ用のターゲットデータベースとテーブルを作成します。

-   方法2：CSVファイルが保存されているAmazon S3、GCS、Azure Blob Storage、またはAlibaba Cloud Object Storage Serviceのディレクトリに、ソースデータ用のターゲットテーブルスキーマファイルを次のように作成します。

    1.  ソースデータ用のデータベーススキーマファイルを作成します。

        [ステップ1](#step-1-prepare-the-csv-files)の命名規則に従ってCSVファイルが作成されている場合、データベーススキーマファイルはデータインポートにおいてオプションです。そうでない場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式である必要があり、 `CREATE DATABASE` DDLステートメントが含まれている必要があります。このファイルを使用すると、 TiDB Cloudは`${db_name}`データベースを作成し、データのインポート時にそのデータベースにデータを格納します。

        例えば、次のステートメントを含む`mydb-schema-create.sql`ファイルを作成すると、 TiDB Cloud はデータをインポートする際に`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソースデータ用のテーブルスキーマファイルを作成します。

        CSVファイルが保存されているAmazon S3、GCS、Azure Blob Storage、またはAlibaba Cloud Object Storage Serviceディレクトリにテーブルスキーマファイルを含めない場合、 TiDB Cloudはデータのインポート時に対応するテーブルを作成しません。

        各テーブルスキーマファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDLステートメントを含んでいる必要があります。このファイルを使用すると、 TiDB Cloudはデータのインポート時に`${db_table}`データベースに`${db_name}`テーブルを作成します。

        例えば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、 TiDB Cloud はデータをインポートする際に`mytable`データベースに`mydb`テーブルを作成します。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注記：**
        >
        > `${db_name}.${table_name}-schema.sql`ファイルには、単一の DDL ステートメントのみを含める必要があります。ファイルに複数の DDL ステートメントが含まれている場合、最初のステートメントのみが有効になります。

## ステップ3．アカウント間アクセスの設定 {#step-3-configure-cross-account-access}

TiDB CloudがAmazon S3、GCS、Azure Blob Storage、またはAlibaba Cloud Object Storage Serviceバケット内のCSVファイルにアクセスできるようにするには、次のいずれかの操作を行います。

-   CSV ファイルが Amazon S3 にある場合は、 TiDB Cloud StarterまたはEssentialインスタンスに対して[Amazon S3へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

    バケットにアクセスするには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、[ステップ4](#step-4-import-csv-files)で必要となるため、アクセスキー (アクセスキー ID とシークレット アクセスキーを含む) またはロール ARN の値をメモしておいてください。

-   CSV ファイルが GCS にある場合は、 TiDB Cloud StarterまたはEssentialインスタンスに対して[GCSへのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)。

-   CSV ファイルが Azure Blob Storage にある場合は、 TiDB Cloud StarterまたはEssentialインスタンスに対して[Azure Blob Storageへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)。

-   CSV ファイルが Alibaba Cloud Object Storage Service (OSS) にある場合は、 TiDB Cloud StarterまたはEssentialインスタンス[Alibaba Cloud Object Storage Service (OSS) へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## ステップ4．CSVファイルをインポートする {#step-4-import-csv-files}

CSVファイルをTiDB Cloud StarterまたはTiDB Cloud Essentialにインポートするには、以下の手順に従ってください。

<SimpleTab>
<div label="Amazon S3">

1.  対象のTiDB Cloud StarterまたはEssentialインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Amazon S3**を選択してください。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`s3://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `s3://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`s3://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `s3://sampledata/ingest/` 。
    -   **認証情報**: AWS ロール ARN または AWS アクセス キーを使用してバケットにアクセスできます。詳細については、 [Amazon S3へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。
        -   **AWSロールARN** ：AWSロールARNの値を入力してください。
        -   **AWSアクセスキー**：AWSアクセスキーIDとAWSシークレットアクセスキーを入力してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloudは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   TiDB Cloud が[ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソース ファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。 `*`と`?`ワイルドカードのみがサポートされています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを選択します。

6.  **「次へ」**をクリックしてください。TiDB TiDB Cloudがソースファイルを適切にスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Google Cloud">

1.  対象のTiDB Cloud StarterまたはEssentialインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Google Cloud Storageを**選択してください。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `[gcs|gs]://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`[gcs|gs]://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `[gcs|gs]://sampledata/ingest/` 。
    -   **認証情報**: GCS IAM役割サービス アカウント キーを使用してバケットにアクセスできます。詳細については、 [GCSへのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-gcs-access)参照してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloudは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   TiDB Cloud が[ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソース ファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。 `*`と`?`ワイルドカードのみがサポートされています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを選択します。

6.  **「次へ」**をクリックしてください。TiDB TiDB Cloudがソースファイルを適切にスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Azure Blob Storage">

1.  対象のTiDB Cloud StarterまたはEssentialインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Azure Blob Storageを**選択します。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `[azure|https]://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`[azure|https]://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `[azure|https]://sampledata/ingest/` 。
    -   **資格情報**: Shared Access Signature (SAS) トークンを使用してバケットにアクセスできます。詳細については、 [Azure Blob Storageへのアクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access)参照してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloudは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   TiDB Cloud が[ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソース ファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。 `*`と`?`ワイルドカードのみがサポートされています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを選択します。

6.  **「次へ」**をクリックしてください。TiDB TiDB Cloudがソースファイルを適切にスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1.  対象のTiDB Cloud StarterまたはEssentialインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Alibaba Cloud OSS**を選択してください。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`oss://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `oss://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`oss://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `oss://sampledata/ingest/` 。
    -   **Credential** : AccessKey ペアを使用してバケットにアクセスできます。詳細については、 [Alibaba Cloudオブジェクトストレージサービス（OSS）へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)参照してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloudは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   TiDB Cloud が[ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソース ファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。 `*`と`?`ワイルドカードのみがサポートされています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを選択します。

6.  **「次へ」**をクリックしてください。TiDB TiDB Cloudがソースファイルを適切にスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

</SimpleTab>

インポートタスクを実行する際に、サポートされていない変換や無効な変換が検出された場合、 TiDB Cloud はインポートジョブを自動的に終了し、インポートエラーを報告します。

インポートエラーが発生した場合は、以下の手順を実行してください。

1.  部分的にインポートされたテーブルを削除します。
2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。
3.  CSVファイル内のデータ型を確認してください。
4.  インポートタスクをもう一度実行してみてください。

## トラブルシューティング {#troubleshooting}

### データインポート中の警告を解決する {#resolve-warnings-during-data-import}

**[インポートの開始]**をクリックした後、 `can't find the corresponding source files`などの警告メッセージが表示された場合は、正しいソース ファイルを提供するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**詳細設定**を使用して変更することで問題を解決します。

これらの問題を解決した後、データを再度インポートする必要があります。

### インポートされたテーブルに行が0件あります {#zero-rows-in-the-imported-tables}

インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。行数がゼロの場合は、入力したバケットURIに一致するデータファイルがなかったことを意味します。この場合は、正しいソースファイルを指定するか、既存のファイルを[データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って名前変更するか、または**詳細設定**を使用して変更することで問題を解決してください。その後、再度テーブルをインポートしてください。
