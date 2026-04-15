---
title: Import CSV Files from Cloud Storage into TiDB Cloud Dedicated
summary: Amazon S3、GCS、またはAzure Blob StorageからCSVファイルをTiDB Cloud Dedicatedにインポートする方法を学びましょう。
aliases: ['/ja/tidbcloud/migrate-from-amazon-s3-or-gcs','/ja/tidbcloud/migrate-from-aurora-bulk-import']
---

# クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする {#import-csv-files-from-cloud-storage-into-tidb-cloud-dedicated}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、または Azure Blob Storage から CSV ファイルをTiDB Cloud Dedicatedにインポートする方法について説明します。

> **ヒント：**
>
> TiDB Cloud StarterまたはTiDB Cloud Essentialについては、 [TiDB Cloud StarterまたはEssentialにクラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB CloudCSV ファイルを空のテーブルにのみインポートできます。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントの手順に従ってTiDB Cloud を使用して一時的な空のテーブルにデータをインポートし、その後`INSERT SELECT`ステートメントを使用してデータを対象の既存のテーブルにコピーします。

-   TiDB Cloud Dedicatedクラスターに[変更フィード](/tidb-cloud/changefeed-overview.md)があるか、 [特定時点への復元](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)が有効になっている場合、現在のデータ インポート機能は[物理輸入モード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を使用しているため、クラスターにデータをインポートできません ([**データのインポート]**ボタンが無効になります)。このモードでは、インポートされたデータは変更ログを生成しないため、変更フィードとポイントインタイム リストアはインポートされたデータを検出できません。

## ステップ1. CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSVファイルのサイズが256MiBを超える場合は、それぞれ約256MiBのサイズの小さなファイルに分割することを検討してください。

    TiDB Cloudは非常に大きなCSVファイルのインポートをサポートしていますが、256MiB程度のサイズの複数の入力ファイルを扱う場合に最高のパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並列処理できるため、インポート速度を大幅に向上させることができるからです。

2.  CSVファイルの名前は以下のようにしてください。

    -   CSV ファイルにテーブル全体のデータがすべて含まれている場合は、ファイル名を`${db_name}.${table_name}.csv`形式で指定してください。この形式は、データをインポートする際に`${db_name}.${table_name}`テーブルにマッピングされます。

    -   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例えば、 `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`のようにです。数値サフィックスは連続していなくても構いませんが、昇順でなければなりません。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

    -   TiDB Cloudは、 `.gzip` 、 `.gz` 、{ `.zst` `.zstd` 、および`.snappy`形式で圧縮ファイルをインポートすることをサポートしています。圧縮 CSV ファイルをインポートする場合は、ファイル名を`${db_name}.${table_name}.${suffix}.csv.${compress}`形式で指定します。ここで`${suffix}`は省略可能で、「000001」などの任意の整数を指定できます。例えば、 `trips.000001.csv.gz`ファイルを`bikeshare.trips`テーブルにインポートする場合は、ファイル名を`bikeshare.trips.000001.csv.gz`に変更する必要があります。

    > **注記：**
    >
    > -   データファイルのみを圧縮すればよく、データベースファイルやテーブルスキーマファイルを圧縮する必要はありません。
    > -   パフォーマンスを向上させるためには、各圧縮ファイルのサイズを100MiBに制限することをお勧めします。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。
    > -   圧縮されていないファイルの場合、前述のルールに従って CSV ファイル名を更新できない場合 (たとえば、CSV ファイル リンクが他のプログラムでも使用されている場合)、ファイル名を変更せずに、[ステップ4](#step-4-import-csv-files-to-tidb-cloud)の**宛先マッピング**手順で**<a href="/tidb-cloud/naming-conventions-for-data-import.md">「TiDB ファイル命名規則</a>を使用して自動マッピングを行う」の**選択を解除して、ソース ファイルを単一のターゲット テーブルに手動でマッピングできます。

## ステップ2．対象テーブルのスキーマを作成する {#step-2-create-the-target-table-schemas}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDB Cloudにデータをインポートする前に、以下のいずれかの方法を使用してテーブルスキーマを作成する必要があります。

-   方法1： TiDB Cloudで、ソースデータ用のターゲットデータベースとテーブルを作成します。

-   方法2：CSVファイルが保存されているAmazon S3、GCS、またはAzure Blob Storageディレクトリに、ソースデータ用のターゲットテーブルスキーマファイルを次のように作成します。

    1.  ソースデータ用のデータベーススキーマファイルを作成します。

        [ステップ1](#step-1-prepare-the-csv-files)の命名規則に従ってCSVファイルが作成されている場合、データベーススキーマファイルはデータインポートにおいてオプションです。そうでない場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式である必要があり、 `CREATE DATABASE` DDLステートメントが含まれている必要があります。このファイルを使用すると、 TiDB Cloudは`${db_name}`データベースを作成し、データのインポート時にそのデータベースにデータを格納します。

        例えば、次のステートメントを含む`mydb-schema-create.sql`ファイルを作成すると、 TiDB Cloud はデータをインポートする際に`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソースデータ用のテーブルスキーマファイルを作成します。

        CSVファイルが保存されているAmazon S3、GCS、またはAzure Blob Storageディレクトリにテーブルスキーマファイルを含めない場合、 TiDB Cloudはデータのインポート時に対応するテーブルを作成しません。

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

TiDB CloudがAmazon S3バケット、GCSバケット、またはAzure Blob Storageコンテナ内のCSVファイルにアクセスできるようにするには、次のいずれかの操作を行います。

-   CSV ファイルが Amazon S3 にある場合は、 [Amazon S3へのアクセスを設定する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

    バケットにアクセスするには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、[ステップ4](#step-4-import-csv-files-to-tidb-cloud)で必要となるため、アクセスキー (アクセスキー ID とシークレット アクセスキーを含む) またはロール ARN の値をメモしておいてください。

-   CSV ファイルが GCS にある場合は、 [GCSへのアクセスを設定する](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

-   CSV ファイルが Azure Blob Storage にある場合は、 [Azure Blob Storageへのアクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

## ステップ4. CSVファイルをTiDB Cloudにインポートする {#step-4-import-csv-files-to-tidb-cloud}

CSVファイルをTiDB Cloudにインポートするには、以下の手順に従ってください。

<SimpleTab>
<div label="Amazon S3">

1.  対象のTiDB Cloud Dedicatedクラスタの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Amazon S3**を選択してください。
    -   **ソースURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`s3://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力してください。例: `s3://mybucket/myfolder/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`s3://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `s3://mybucket/myfolder/` 。
    -   **認証情報**: AWS ロール ARN または AWS アクセス キーを使用してバケットにアクセスできます。詳細については、 [Amazon S3へのアクセスを設定する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)参照してください。
        -   **AWS ロール ARN** (推奨): AWS ロール ARN の値を入力します。まだロール ARN がない場合は、 **[ここをクリックして AWS CloudFormation を使用して新しいロール ARN を作成する] を**クリックし、画面の指示に従うか、 **[問題が発生しましたか?] ダイアログでロール ARN を手動で作成して、**クラスター**のTiDB Cloudアカウント ID**と**TiDB Cloud外部 ID**を取得し、 IAMロールを手動で作成します。
        -   **AWSアクセスキー**：AWSアクセスキーIDとAWSシークレットアクセスキーを入力してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースURI**でディレクトリを指定すると、 TiDB Cloudはデフォルトで**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則を</a>使用する」**オプションを選択します。

    > **注記：**
    >
    > **ソースURI**で単一のファイルを指定すると、 TiDB Cloudは**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則</a>を使用する」**オプションを表示せず、**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを入力するだけで済みます。

    -   TiDB Cloud が[TiDBファイルの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソースファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。ソースフォルダにスキーマファイル ( `${db_name}-schema-create.sql`や`${db_name}.${table_name}-schema.sql`など) が含まれている場合、 TiDB Cloud は、ターゲットデータベースとテーブルがまだ存在しない場合に、それらを使用して作成します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。TiDB TiDB Cloud は`*`と`?`のワイルドカードのみをサポートしています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを入力してください。

    必要に応じて、 **「CSVコンフィグレーションの編集」**をクリックして、CSVファイルに合わせてオプションを設定してください。区切り文字や区切り記号の設定、エスケープ文字にバックスラッシュを使用するかどうかの指定、ファイルにヘッダー行が含まれているかどうかの指定が可能です。

6.  **「次へ」**をクリックします。TiDB TiDB Cloudがソースファイルをスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Google Cloud">

1.  対象のTiDB Cloud Dedicatedクラスタの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Google Cloud Storageを**選択してください。
    -   **ソースURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`gs://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `gs://mybucket/myfolder/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`gs://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `gs://mybucket/myfolder/` 。
    -   **Google Cloud サービス アカウント ID** : TiDB Cloud は、このページで一意の Google Cloud サービス アカウント ID ( `example-service-account@your-project.iam.gserviceaccount.com`など) を提供します。このサービス アカウント ID に、Google Cloud プロジェクト内の GCS バケットに対して必要なIAM権限（ `Storage Object Viewer`など）を付与します。詳細については、 [GCSへのアクセスを設定する](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)参照してください。

4.  **「次へ」**をクリックしてください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースURI**でディレクトリを指定すると、 TiDB Cloudはデフォルトで**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則を</a>使用する」**オプションを選択します。

    > **注記：**
    >
    > **ソースURI**で単一のファイルを指定すると、 TiDB Cloudは**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則</a>を使用する」**オプションを表示せず、**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを入力するだけで済みます。

    -   TiDB Cloud が[TiDBファイルの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソースファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。ソースフォルダにスキーマファイル ( `${db_name}-schema-create.sql`や`${db_name}.${table_name}-schema.sql`など) が含まれている場合、 TiDB Cloud は、ターゲットデータベースとテーブルがまだ存在しない場合に、それらを使用して作成します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。TiDB TiDB Cloud は`*`と`?`のワイルドカードのみをサポートしています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを入力してください。

    必要に応じて、 **「CSVコンフィグレーションの編集」**をクリックして、CSVファイルに合わせてオプションを設定してください。区切り文字や区切り記号の設定、エスケープ文字にバックスラッシュを使用するかどうかの指定、ファイルにヘッダー行が含まれているかどうかの指定が可能です。

6.  **「次へ」**をクリックします。TiDB TiDB Cloudがソースファイルをスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Azure Blob Storage">

1.  対象のTiDB Cloud Dedicatedクラスタの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Azure Blob Storageを**選択します。

    -   **ソースURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].csv`の形式で入力してください。例: `https://myaccount.blob.core.windows.net/mycontainer/myfolder/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/`の形式で入力してください。例： `https://myaccount.blob.core.windows.net/mycontainer/myfolder/` 。

    -   **接続方法**： TiDB CloudがAzure Blob Storageに接続する方法を選択してください。

        -   **パブリック**（デフォルト）：パブリックインターネット経由で接続します。storageアカウントがパブリックネットワークへのアクセスを許可している場合にこのオプションを使用してください。
        -   **プライベートリンク**：Azure プライベートエンドポイント経由で接続し、ネットワークから隔離されたアクセスを実現します。storageアカウントがパブリックアクセスをブロックしている場合、またはセキュリティポリシーでプライベート接続が必要な場合にこのオプションを使用します。**プライベートリンク**を選択した場合は、追加フィールド**「Azure Blob Storage リソース ID」**も入力する必要があります。リソース ID を確認するには：

            1.  [Azureポータル](https://portal.azure.com/)にアクセスします。
            2.  storageアカウントに移動し、 **[概要]** &gt; **[JSONビュー]**をクリックします。
            3.  `id`プロパティの値をコピーします。リソース ID は`/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account_name>`の形式です。

    -   **SAS トークン**: TiDB Cloud がAzure Blob Storage コンテナー内のソース ファイルにアクセスできるようにするアカウント SAS トークンを入力します。まだお持ちでない場合は、 **「ここをクリックして Azure ARM テンプレートを使用して新しいものを作成します」を**クリックし、画面の指示に従うか、アカウント SAS トークンを手動で作成します。詳細については、 [Azure Blob Storageへのアクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)参照してください。

4.  **「次へ」**をクリックしてください。

    接続方法として**プライベートリンク**を選択した場合、 TiDB Cloudはstorageアカウント用のプライベートエンドポイントを作成します。ウィザードを続行するには、Azureポータルでこのエンドポイント要求を承認する必要があります。

    1.  [Azureポータル](https://portal.azure.com/)に移動し、storageアカウントに移動します。

    2.  **「ネットワーク」** &gt; **「プライベートエンドポイント接続」**をクリックします。

    3.  TiDB Cloudからの保留中の接続要求を見つけて、 **「承認」**をクリックします。

    4.  [TiDB Cloudコンソール](https://tidbcloud.com/)に戻ります。エンドポイントが承認されると、インポート ウィザードが自動的に続行されます。

    > **注記：**
    >
    > エンドポイントがまだ承認されていない場合、 TiDB Cloud は接続が承認待ちであることを示すメッセージを表示します。Azure でリクエスト[Azureポータル](https://portal.azure.com/)承認してから、再試行してください。

5.  **「宛先マッピング」**セクションで、ソースファイルをターゲットテーブルにどのようにマッピングするかを指定します。

    **ソースURI**でディレクトリを指定すると、 TiDB Cloudはデフォルトで**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則を</a>使用する」**オプションを選択します。

    > **注記：**
    >
    > **ソースURI**で単一のファイルを指定すると、 TiDB Cloudは**「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">TiDBファイル命名規則</a>を使用する」**オプションを表示せず、**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを入力するだけで済みます。

    -   TiDB Cloud が[TiDBファイルの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従うすべてのソースファイルを対応するテーブルに自動的にマッピングするには、このオプションを選択したままにして、データ形式として**CSV**を選択します。ソースフォルダにスキーマファイル ( `${db_name}-schema-create.sql`や`${db_name}.${table_name}-schema.sql`など) が含まれている場合、 TiDB Cloud は、ターゲットデータベースとテーブルがまだ存在しない場合に、それらを使用して作成します。

    -   ソースCSVファイルをターゲットデータベースおよびテーブルに関連付けるためのマッピングルールを手動で構成するには、このオプションの選択を解除し、次のフィールドに入力します。

        -   **ソース**: ファイル名のパターンを`[file_name].csv`の形式で入力してください。例: `TableName.01.csv` 。ワイルドカードを使用して複数のファイルを照合することもできます。TiDB TiDB Cloud は`*`と`?`のワイルドカードのみをサポートしています。

            -   `my-data?.csv` : `my-data` `my-data1.csv`や`my-data2.csv`のような 1 文字が続くすべての CSV ファイルに一致します。
            -   `my-data*.csv` : `my-data`で始まるすべての CSV ファイルに一致します。たとえば`my-data-2023.csv`や`my-data-final.csv`などです。

        -   **対象データベース**と**対象テーブル**：データをインポートする対象データベースとテーブルを入力してください。

    必要に応じて、 **「CSVコンフィグレーションの編集」**をクリックして、CSVファイルに合わせてオプションを設定してください。区切り文字や区切り記号の設定、エスケープ文字にバックスラッシュを使用するかどうかの指定、ファイルにヘッダー行が含まれているかどうかの指定が可能です。

6.  **「次へ」**をクリックします。TiDB TiDB Cloudがソースファイルをスキャンします。

7.  スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックします。

8.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

</SimpleTab>

インポートタスクを実行する際に、サポートされていない変換や無効な変換が検出された場合、 TiDB Cloud はインポートジョブを自動的に終了し、インポートエラーを報告します。詳細は**「ステータス」**フィールドで確認できます。

インポートエラーが発生した場合は、以下の手順を実行してください。

1.  部分的にインポートされたテーブルを削除します。
2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。
3.  CSVファイル内のデータ型を確認してください。
4.  インポートタスクをもう一度実行してみてください。

## トラブルシューティング {#troubleshooting}

### データインポート中の警告を解決する {#resolve-warnings-during-data-import}

**事前チェック**ステップで`can't find the corresponding source files`などの警告が表示された場合は、正しいソースファイルを提供するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**宛先マッピング**ステップに戻って手動マッピングルールに切り替えることで問題を解決します。

これらの問題を解決したら、ウィザードに戻り、インポートを再度実行してください。

### インポートされたテーブルに行が0件あります {#zero-rows-in-the-imported-tables}

インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。行数がゼロの場合は、入力したソースURIに一致するデータファイルがなかったことを意味します。この場合は、正しいソースファイルを指定するか、既存のファイルを[データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って名前変更するか、または**「宛先マッピング」**ステップに戻って手動マッピング規則に切り替えることで問題を解決してください。その後、再度テーブルをインポートしてください。
