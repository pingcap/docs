---
title: Import CSV Files from Cloud Storage into TiDB Cloud Premium
summary: Amazon S3またはAlibaba Cloud Object Storage Service（OSS）からCSVファイルをTiDB Cloud Premiumインスタンスにインポートする方法を学びましょう。
---

# クラウドストレージからCSVファイルをTiDB Cloud Premiumにインポートする {#import-csv-files-from-cloud-storage-into-tidb-cloud-premium}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Alibaba Cloud Object Storage Service (OSS) から CSV ファイルをTiDB Cloud Premium インスタンスにインポートする方法について説明します。

> **ヒント：**
>
> -   TiDB Cloud StarterまたはEssentialについては、 [TiDB Cloud StarterまたはEssentialにクラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)。
> -   TiDB Cloud Dedicatedについては、[クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)参照してください。

## 制限事項 {#limitations}

データの一貫性を確保するため、 TiDB Cloud Premium では、CSV ファイルを空のテーブルにのみインポートできます。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントの手順に従って一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータを対象の既存のテーブルにコピーします。

## ステップ1. CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSVファイルが256MiBを超える場合は、それぞれ約256MiBのサイズの小さなファイルに分割することを検討してください。

    TiDB Cloud Premiumは非常に大きなCSVファイルのインポートをサポートしていますが、サイズが約256MiBの複数の入力ファイルを扱う場合に最高のパフォーマンスを発揮します。これは、 TiDB Cloud Premiumが複数のファイルを並列処理できるため、インポート速度を大幅に向上させることができるからです。

2.  CSVファイルの名前は以下のようにしてください。

    -   CSV ファイルにテーブル全体のデータがすべて含まれている場合は、ファイル名を`${db_name}.${table_name}.csv`形式で指定してください。この形式は、データをインポートする際に`${db_name}.${table_name}`テーブルにマッピングされます。

    -   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例えば、 `${db_name}.${table_name}.000001.csv`や`${db_name}.${table_name}.000002.csv`のようにです。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

    -   TiDB Cloud Premium は、 `.gzip` 、 `.gz` 、 `.zst` `.zstd` 、{ `.snappy`の形式で圧縮ファイルをインポートできます。圧縮 CSV ファイルをインポートする場合は、ファイル名を`${db_name}.${table_name}.${suffix}.csv.${compress}`形式で指定します。ここで`${suffix}`省略可能で、「000001」などの任意の整数を指定できます。例えば、 `trips.000001.csv.gz`ファイルを`bikeshare.trips`テーブルにインポートする場合は、ファイル名を`bikeshare.trips.000001.csv.gz`に変更する必要があります。

    > **注記：**
    >
    > -   パフォーマンスを向上させるためには、各圧縮ファイルのサイズを100MiBに制限することをお勧めします。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。
    > -   非圧縮ファイルの場合、場合によっては前述のルールに従ってCSVファイル名を更新できない場合（たとえば、CSVファイルリンクが他のプログラムでも使用されている場合）、ファイル名を変更せずに、[ステップ4](#step-4-import-csv-files)の**マッピング設定**を使用してソースデータを単一のターゲットテーブルにインポートできます。

## ステップ2．対象テーブルのスキーマを作成する {#step-2-create-the-target-table-schemas}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDB Cloud Premiumにデータをインポートする前に、以下のいずれかの方法を使用してテーブルスキーマを作成する必要があります。

-   方法1： TiDB Cloud Premiumで、ソースデータ用のターゲットデータベースとテーブルを作成します。

-   方法2：CSVファイルが保存されているAmazon S3またはAlibaba Cloud Object Storage Service（OSS）ディレクトリに、ソースデータ用のターゲットテーブルスキーマファイルを次のように作成します。

    1.  ソースデータ用のデータベーススキーマファイルを作成します。

        [ステップ1](#step-1-prepare-the-csv-files)の命名規則に従ってCSVファイルが作成されている場合、データベーススキーマファイルはデータインポートにおいてオプションです。そうでない場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式である必要があり、 `CREATE DATABASE` DDLステートメントが含まれている必要があります。このファイルを使用すると、 TiDB Cloud Premiumは、データのインポート時にデータを格納するための`${db_name}`データベースを作成します。

        例えば、次のステートメントを含む`mydb-schema-create.sql`ファイルを作成すると、 TiDB Cloud Premium はデータをインポートする際に`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソースデータ用のテーブルスキーマファイルを作成します。

        CSVファイルが保存されているAmazon S3またはAlibaba Cloud Object Storage Serviceディレクトリにテーブルスキーマファイルを含めない場合、 TiDB Cloud Premiumはデータのインポート時に対応するテーブルを作成しません。

        各テーブルスキーマファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDLステートメントを含んでいる必要があります。このファイルを使用すると、 TiDB Cloud Premiumは、データのインポート時に`${table_name}`データベースに`${db_name}`テーブルを作成します。

        例えば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、 TiDB Cloud Premium はデータをインポートする際に`mytable`データベースに`mydb`テーブルを作成します。

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

TiDB Cloud PremiumがAmazon S3またはAlibaba Cloud Object Storage Service（OSS）内のCSVファイルにアクセスできるようにするには、次のいずれかの操作を行います。

-   CSV ファイルが Amazon S3 にある場合は、 TiDB Cloud Premium インスタンスに対して[Amazon S3へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)。

    バケットにアクセスするには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、[ステップ4](#step-4-import-csv-files)で必要となるため、アクセスキー (アクセスキー ID とシークレット アクセスキーを含む) またはロール ARN の値をメモしておいてください。

-   CSV ファイルが Alibaba Cloud Object Storage Service (OSS) にある場合は、 TiDB Cloud Premium インスタンスの[Alibaba Cloud Object Storage Service (OSS) へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)。

## ステップ4．CSVファイルをインポートする {#step-4-import-csv-files}

CSVファイルをTiDB Cloud Premiumにインポートするには、以下の手順に従ってください。

<SimpleTab>
<div label="Amazon S3">

1.  対象のTiDB Cloud Premiumインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Amazon S3**を選択してください。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`s3://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力します。例: `s3://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`s3://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `s3://sampledata/ingest/` 。
    -   **認証情報**: AWS ロール ARN または AWS アクセス キーを使用してバケットにアクセスできます。詳細については、 [Amazon S3へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。
        -   **AWS ロール ARN** : AWS ロール ARN の値を入力してください。新しいロールを作成する必要がある場合は、 **[ここをクリックして AWS CloudFormation を使用して新しいロールを作成] をクリックし**、ガイド付き手順に従って、提供されているテンプレートを起動し、 IAM警告を確認し、スタックを作成し、生成された ARN をTiDB Cloud Premium にコピーしてください。
        -   **AWSアクセスキー**：AWSアクセスキーIDとAWSシークレットアクセスキーを入力してください。
    -   **バケットへのアクセスをテストする**：認証情報が正しく入力された後、このボタンをクリックして、 TiDB Cloud Premiumがバケットにアクセスできることを確認してください。
    -   **ターゲット接続**：インポートを実行するTiDBのユーザー名とパスワードを入力してください。必要に応じて、 **「接続テスト」を**クリックして認証情報を検証してください。

4.  **「次へ」**をクリックしてください。

5.  **ソースファイルマッピングの**セクションでは、 TiDB Cloud Premiumがバケットをスキャンし、ソースファイルと宛先テーブル間のマッピングを提案します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloud Premiumは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   [ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)ソース ファイルとターゲット テーブルに適用するには、自動マッピングを有効のままにしておきます。データ形式として**CSV**を選択したままにしておきます。

    -   **詳細オプション**：パネルを展開して`Ignore compatibility checks (advanced)`の切り替えボタンを表示します。スキーマ互換性検証を意図的にバイパスしたい場合を除き、無効のままにしておいてください。

    <!-- future feature -->

    > **注記：**
    >
    > 手動マッピング機能は近日中に利用可能になります。切り替え機能が利用可能になったら、自動マッピングオプションをオフにして、マッピングを手動で設定してください。
    >
    > -   **ソース**: `TableName.01.csv`のようなファイル名パターンを入力してください。ワイルドカード`*`と`?`がサポートされています (例: `my-data*.csv` )。
    > -   **対象データベース**と**対象テーブル**：一致したファイルの宛先オブジェクトを選択します。

6.  TiDB Cloud Premiumはソースパスを自動的にスキャンします。スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックしてください。

7.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1.  対象のTiDB Cloud Premiumインスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**をクリックします。

3.  **「クラウドストレージからデータをインポート」**ページで、以下の情報を入力してください。

    -   **ストレージプロバイダー**： **Alibaba Cloud OSS**を選択してください。
    -   **ソースファイルURI** ：
        -   1 つのファイルをインポートする場合は、ソースファイルの URI を`oss://[bucket_name]/[data_source_folder]/[file_name].csv`の形式で入力してください。例: `oss://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを`oss://[bucket_name]/[data_source_folder]/`の形式で入力してください。例： `oss://sampledata/ingest/` 。
    -   **Credential** : AccessKey ペアを使用してバケットにアクセスできます。詳細については、 [Alibaba Cloudオブジェクトストレージサービス（OSS）へのアクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)参照してください。
    -   **バケットへのアクセスをテストする**：認証情報が正しく入力された後、このボタンをクリックして、 TiDB Cloud Premiumがバケットにアクセスできることを確認してください。
    -   **ターゲット接続**：インポートを実行するTiDBのユーザー名とパスワードを入力してください。必要に応じて、 **「接続テスト」を**クリックして認証情報を検証してください。

4.  **「次へ」**をクリックしてください。

5.  **ソースファイルマッピングの**セクションでは、 TiDB Cloud Premiumがバケットをスキャンし、ソースファイルと宛先テーブル間のマッピングを提案します。

    **ソースファイルURI**でディレクトリが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**で単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloud Premiumは**ソース**フィールドにファイル名を自動的に入力します。この場合、データインポートの対象となるデータベースとテーブルを選択するだけで済みます。

    -   [ファイル命名規則](/tidb-cloud/naming-conventions-for-data-import.md)ソース ファイルとターゲット テーブルに適用するには、自動マッピングを有効のままにしておきます。データ形式として**CSV**を選択したままにしておきます。

    -   **詳細オプション**：パネルを展開して`Ignore compatibility checks (advanced)`の切り替えボタンを表示します。スキーマ互換性検証を意図的にバイパスしたい場合を除き、無効のままにしておいてください。

    <!-- future feature -->

    > **注記：**
    >
    > 手動マッピング機能は近日中に利用可能になります。切り替え機能が利用可能になったら、自動マッピングオプションをオフにして、マッピングを手動で設定してください。
    >
    > -   **ソース**: `TableName.01.csv`のようなファイル名パターンを入力してください。ワイルドカード`*`と`?`がサポートされています (例: `my-data*.csv` )。
    > -   **対象データベース**と**対象テーブル**：一致したファイルの宛先オブジェクトを選択します。

6.  TiDB Cloud Premiumはソースパスを自動的にスキャンします。スキャン結果を確認し、検出されたデータファイルと対応するターゲットテーブルをチェックしてから、 **「インポート開始」を**クリックしてください。

7.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。

</div>

</SimpleTab>

インポートタスクを実行する際に、サポートされていない変換や無効な変換が検出された場合、 TiDB Cloud Premium はインポートジョブを自動的に終了し、インポートエラーを報告します。

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
