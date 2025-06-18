---
title: Import Apache Parquet Files from Cloud Storage into TiDB Cloud Dedicated
summary: Apache Parquet ファイルを Amazon S3、GCS、または Azure Blob Storage からTiDB Cloud Dedicated にインポートする方法を学びます。
---

# クラウドストレージからTiDB Cloud DedicatedにApache Parquetファイルをインポートする {#import-apache-parquet-files-from-cloud-storage-into-tidb-cloud-dedicated}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS)、またはAzure Blob StorageからTiDB Cloud DedicatedにApache Parquetファイルをインポートする方法について説明します。Parquetファイルは、非圧縮または[Google スナッピー](https://github.com/google/snappy)で圧縮された状態でインポートできます。その他のParquet圧縮コーデックはサポートされていません。

## 制限事項 {#limitations}

-   データの一貫性を確保するため、 TiDB Cloud空のテーブルへのParquetファイルのインポートのみが許可されています。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従ってTiDB Cloudで一時的な空のテーブルにデータをインポートし、 `INSERT SELECT`ステートメントを使用してデータを既存のターゲットテーブルにコピーします。

-   TiDB Cloud Dedicated クラスターで[チェンジフィード](/tidb-cloud/changefeed-overview.md)または[ポイントインタイムリストア](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)有効になっている場合、現在のデータインポート機能は[物理インポートモード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)使用しているため、クラスターにデータをインポートできません（「**データのインポート**」ボタンは無効になります）。このモードでは、インポートされたデータは変更ログを生成しないため、変更フィードとポイントインタイム復元はインポートされたデータを検出できません。

## ステップ1. Parquetファイルを準備する {#step-1-prepare-the-parquet-files}

> **注記：**
>
> 現在、 TiDB Cloud は、以下のいずれかのデータ型を含む Parquet ファイルのインポートをサポートしていません。インポートする Parquet ファイルにこれらのデータ型が含まれている場合は、まず[サポートされているデータ型](#supported-data-types) （例： `STRING` ）を使用して Parquet ファイルを再生成する必要があります。あるいは、AWS Glue などのサービスを使用してデータ型を簡単に変換することもできます。
>
> -   `LIST`
> -   `NEST STRUCT`
> -   `BOOL`
> -   `ARRAY`
> -   `MAP`

1.  Parquet ファイルが 256 MB より大きい場合は、サイズがそれぞれ約 256 MB の小さなファイルに分割することを検討してください。

    TiDB Cloudは非常に大きなParquetファイルのインポートをサポートしていますが、256MB程度の複数の入力ファイルで最適なパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並列処理できるため、インポート速度が大幅に向上するからです。

2.  Parquet ファイルに次のように名前を付けます。

    -   Parquet ファイルにテーブル全体のすべてのデータが含まれている場合は、データをインポートするときに`${db_name}.${table_name}`テーブルにマップされる`${db_name}.${table_name}.parquet`形式でファイルに名前を付けます。

    -   1つのテーブルのデータが複数のParquetファイルに分割されている場合は、これらのParquetファイルに数値サフィックスを追加します。例： `${db_name}.${table_name}.000001.parquet`と`${db_name}.${table_name}.000002.parquet` 。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さを揃えるため、数値の前にゼロを追加する必要があります。

    > **注記：**
    >
    > -   場合によっては、前述のルールに従って Parquet ファイル名を更新できない場合 (たとえば、Parquet ファイル リンクが他のプログラムでも使用されている場合) は、ファイル名を変更せずに、 [ステップ4](#step-4-import-parquet-files-to-tidb-cloud)の**マッピング設定**を使用してソース データを単一のターゲット テーブルにインポートできます。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。

## ステップ2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schemas}

Parquet ファイルにはスキーマ情報が含まれていないため、Parquet ファイルからTiDB Cloudにデータをインポートする前に、次のいずれかの方法でテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloudで、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: Parquet ファイルが配置されている Amazon S3、GCS、または Azure Blob Storage ディレクトリで、次のようにソース データのターゲット テーブル スキーマ ファイルを作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        Parquetファイルが[ステップ1](#step-1-prepare-the-parquet-files)の命名規則に従っている場合、データベーススキーマファイルはデータのインポートに必須ではありません。そうでない場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式で、 `CREATE DATABASE` DDLステートメントを含んでいる必要があります。このファイルを使用して、 TiDB Cloudはデータをインポートする際に、データを格納するための`${db_name}`データベースを作成します。

        たとえば、次のステートメントを含む`mydb-scehma-create.sql`ファイルを作成すると、 TiDB Cloud はデータをインポートするときに`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        Parquet ファイルが配置されている Amazon S3、GCS、または Azure Blob Storage ディレクトリにテーブル スキーマ ファイルを含めない場合、 TiDB Cloud はデータをインポートしたときに対応するテーブルを作成しません。

        各テーブルスキーマファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDLステートメントを含む必要があります。このファイルを使用することで、 TiDB Cloudはデータをインポートする際に`${db_name}`データベースに`${db_table}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、 TiDB Cloud はデータをインポートするときに`mydb`データベースに`mytable`テーブルを作成します。

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

TiDB Cloud がAmazon S3 バケット、GCS バケット、または Azure Blob Storage コンテナ内の Parquet ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   Parquet ファイルが Amazon S3 にある場合は、 [Amazon S3 アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access) 。

    バケットにアクセスするには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、アクセスキー（アクセスキー ID とシークレットアクセスキーを含む）またはロール ARN の値をメモしておいてください。これらは[ステップ4](#step-4-import-parquet-files-to-tidb-cloud)で必要になります。

-   Parquet ファイルが GCS にある場合は、 [GCS アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access) 。

-   Parquet ファイルが Azure Blob Storage にある場合は、 [Azure Blob Storage アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access) 。

## ステップ4. ParquetファイルをTiDB Cloudにインポートする {#step-4-import-parquet-files-to-tidb-cloud}

Parquet ファイルをTiDB Cloudにインポートするには、次の手順を実行します。

<SimpleTab>
<div label="Amazon S3">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **Cloud Storage からデータをインポート**を選択します。

3.  **「Amazon S3 からのデータのインポート」**ページで、次の情報を入力します。

    -   **含まれるスキーマファイル**: ソースフォルダにターゲットテーブルのスキーマファイル（例： `${db_name}-schema-create.sql` ）が含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **Parquet**を選択します。
    -   **フォルダURI** : ソースフォルダのURIを`s3://[bucket_name]/[data_source_folder]/`形式で入力します。パスは`/`で終わる必要があります。例： `s3://sampledata/ingest/` 。
    -   **バケットアクセス**: バケットにアクセスするには、AWS IAMロール ARN または AWS アクセスキーのいずれかを使用できます。
        -   **AWS ロール ARN** （推奨）：AWS IAMロールの ARN 値を入力します。バケットのIAMロールがまだない場合は、「 **AWS CloudFormation で新規ロールを作成するには、こちらをクリックしてください」をクリックし**、画面の指示に従って、提供されている AWS CloudFormation テンプレートを使用して作成できます。または、バケットのIAMロール ARN を手動で作成することもできます。
        -   **AWS アクセスキー**: AWS アクセスキー ID と AWS シークレットアクセスキーを入力します。
        -   両方の方法の詳細な手順については、 [Amazon S3 アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)参照してください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、個々のターゲットテーブルと対応するParquetファイルのマッピングをカスタマイズできます。ターゲットデータベースとテーブルごとに、以下の設定を行います。

    -   **ターゲット データベース**: リストから対応するデータベース名を選択します。
    -   **ターゲット テーブル**: リストから対応するテーブル名を選択します。
    -   **ソースファイルのURIと名前**: フォルダ名とファイル名を含むソースファイルの完全なURIを、 `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`形式で入力してください。例: `s3://sampledata/ingest/TableName.01.parquet`ワイルドカード ( `?`と`*` ) を使用して複数のファイルに一致させることもできます。例:
        -   `s3://[bucket_name]/[data_source_folder]/my-data1.parquet` : `my-data1.parquet` in `[data_source_folder]`という名前の単一の Parquet ファイルがターゲット テーブルにインポートされます。
        -   `s3://[bucket_name]/[data_source_folder]/my-data?.parquet` : `my-data`で始まり、その後に`[data_source_folder]`の 1 つの文字 ( `my-data1.parquet`や`my-data2.parquet`など) が続くすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
        -   `s3://[bucket_name]/[data_source_folder]/my-data*.parquet` : `[data_source_folder]`内の`my-data`で始まるすべての Parquet ファイル ( `my-data10.parquet`や`my-data100.parquet`など) が同じターゲット テーブルにインポートされます。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Google Cloud">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **Cloud Storage からデータをインポート**を選択します。

3.  **「Google Cloud Storage からのデータのインポート」**ページで、ソース Parquet ファイルについて次の情報を入力します。

    -   **含まれるスキーマファイル**: ソースフォルダにターゲットテーブルのスキーマファイル（例： `${db_name}-schema-create.sql` ）が含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **Parquet**を選択します。
    -   **フォルダURI** : ソースフォルダのURIを`gs://[bucket_name]/[data_source_folder]/`形式で入力します。パスは`/`で終わる必要があります。例： `gs://sampledata/ingest/` 。
    -   **Google Cloud サービスアカウント ID** : TiDB Cloud は、このページで一意のサービスアカウント ID（例: `example-service-account@your-project.iam.gserviceaccount.com` ）を提供します。このサービスアカウント ID に、Google Cloud プロジェクト内の GCS バケットに対する必要なIAM権限（「ストレージオブジェクト閲覧者」など）を付与する必要があります。詳細については、 [GCS アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)ご覧ください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、個々のターゲットテーブルと対応するParquetファイルのマッピングをカスタマイズできます。ターゲットデータベースとテーブルごとに、以下の設定を行います。

    -   **ターゲット データベース**: リストから対応するデータベース名を選択します。
    -   **ターゲット テーブル**: リストから対応するテーブル名を選択します。
    -   **ソースファイルのURIと名前**: フォルダ名とファイル名を含むソースファイルの完全なURIを、 `gs://[bucket_name]/[data_source_folder]/[file_name].parquet`形式で入力してください。例: `gs://sampledata/ingest/TableName.01.parquet`ワイルドカード ( `?`と`*` ) を使用して複数のファイルに一致させることもできます。例:
        -   `gs://[bucket_name]/[data_source_folder]/my-data1.parquet` : `my-data1.parquet` in `[data_source_folder]`という名前の単一の Parquet ファイルがターゲット テーブルにインポートされます。
        -   `gs://[bucket_name]/[data_source_folder]/my-data?.parquet` : `my-data`で始まり、その後に`[data_source_folder]`の 1 つの文字 ( `my-data1.parquet`や`my-data2.parquet`など) が続くすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
        -   `gs://[bucket_name]/[data_source_folder]/my-data*.parquet` : `[data_source_folder]`内の`my-data`で始まるすべての Parquet ファイル ( `my-data10.parquet`や`my-data100.parquet`など) が同じターゲット テーブルにインポートされます。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Azure Blob Storage">

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **Cloud Storage からデータをインポート**を選択します。

3.  **Azure Blob Storage からのデータのインポート**ページで、次の情報を入力します。

    -   **含まれるスキーマファイル**: ソースフォルダにターゲットテーブルのスキーマファイル（例： `${db_name}-schema-create.sql` ）が含まれている場合は**「はい」**を選択します。含まれていない場合は**「いいえ」**を選択します。
    -   **データ形式**: **Parquet**を選択します。
    -   **フォルダーURI** : ソースファイルが保存されているAzure Blob StorageのURIを`https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/`形式で入力します。パスは`/`で終わる必要があります。例: `https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/` 。
    -   **SAS トークン**: TiDB Cloud がAzure Blob Storage コンテナー内のソースファイルにアクセスできるように、アカウント SAS トークンを入力します。まだトークンをお持ちでない場合は、提供されている Azure ARM テンプレートを使用して作成できます。「 **Azure ARM テンプレートを使用して新規作成するには、こちらをクリックしてください」をクリックし**、画面の指示に従ってください。または、アカウント SAS トークンを手動で作成することもできます。詳細については、 [Azure Blob Storage アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)参照してください。

4.  **[接続]**をクリックします。

5.  **[宛先]**セクションで、ターゲット データベースとテーブルを選択します。

    複数のファイルをインポートする場合、 **「詳細設定」** &gt; **「マッピング設定」**を使用して、個々のターゲットテーブルと対応するParquetファイルのマッピングをカスタマイズできます。ターゲットデータベースとテーブルごとに、以下の設定を行います。

    -   **ターゲット データベース**: リストから対応するデータベース名を選択します。
    -   **ターゲット テーブル**: リストから対応するテーブル名を選択します。
    -   **ソースファイルのURIと名前**: フォルダ名とファイル名を含むソースファイルの完全なURIを、 `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].parquet`形式で入力してください。例: `https://myaccount.blob.core.windows.net/mycontainer/data-ingestion/TableName.01.parquet`ワイルドカード ( `?`と`*` ) を使用して複数のファイルに一致させることもできます。例:
        -   `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data1.parquet` : `my-data1.parquet` in `[data_source_folder]`という名前の単一の Parquet ファイルがターゲット テーブルにインポートされます。
        -   `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data?.parquet` : `my-data`で始まり、その後に`[data_source_folder]`の 1 つの文字 ( `my-data1.parquet`や`my-data2.parquet`など) が続くすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
        -   `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/my-data*.parquet` : `[data_source_folder]`内の`my-data`で始まるすべての Parquet ファイル ( `my-data10.parquet`や`my-data100.parquet`など) が同じターゲット テーブルにインポートされます。

6.  **[インポートの開始]を**クリックします。

7.  インポートの進行状況に**「完了」と**表示されたら、インポートされたテーブルを確認します。

</div>

</SimpleTab>

インポートタスクの実行中に、サポートされていない変換や無効な変換が検出された場合、 TiDB Cloud はインポートジョブを自動的に終了し、インポートエラーを報告します。詳細は**「ステータス」**フィールドで確認できます。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。

2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。

3.  Parquet ファイル内のデータ型を確認します。

    Parquet ファイルにサポートされていないデータ型 (たとえば、 `NEST STRUCT` 、 `ARRAY` 、 `MAP` ) が含まれている場合は、 [サポートされているデータ型](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。

4.  インポートタスクをもう一度試してください。

## サポートされているデータ型 {#supported-data-types}

次の表は、TiDB Cloudにインポートできるサポートされている Parquet データ型を示しています。

| 寄木細工のプリミティブタイプ | Parquet論理型    | TiDBまたはMySQLの型                                                                                                                                                      |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ダブル            | ダブル           | ダブル<br/>フロート                                                                                                                                                        |
| 固定長バイト配列(9)    | 10進数(20,0)    | BIGINT 符号なし                                                                                                                                                         |
| 固定長バイト配列(N)    | DECIMAL(p,s)  | 小数点<br/>数値                                                                                                                                                          |
| INT32          | DECIMAL(p,s)  | 小数点<br/>数値                                                                                                                                                          |
| INT32          | 該当なし          | INT<br/>ミディアムミント<br/>年                                                                                                                                              |
| INT64          | DECIMAL(p,s)  | 小数点<br/>数値                                                                                                                                                          |
| INT64          | 該当なし          | ビッグイント<br/>符号なし整数<br/>ミディアムミント 未署名                                                                                                                                  |
| INT64          | タイムスタンプ_マイクロ秒 | 日時<br/>タイムスタンプ                                                                                                                                                      |
| バイト配列          | 該当なし          | バイナリ<br/>少し<br/>ブロブ<br/>チャー<br/>ラインストリング<br/>ロングブロブ<br/>ミディアムブロブ<br/>マルチラインストリング<br/>タイニーブロブ<br/>VARBINARY                                                          |
| バイト配列          | 弦             | 列挙型<br/>日付<br/>小数点<br/>幾何学<br/>ジオメトリコレクション<br/>JSON<br/>長文<br/>中テキスト<br/>マルチポイント<br/>マルチポリゴン<br/>数値<br/>ポイント<br/>ポリゴン<br/>セット<br/>TEXT<br/>時間<br/>小さなテキスト<br/>可変長文字 |
| スモールイント        | 該当なし          | INT32                                                                                                                                                               |
| SMALLINT 符号なし  | 該当なし          | INT32                                                                                                                                                               |
| タイニーイント        | 該当なし          | INT32                                                                                                                                                               |
| TINYINT 符号なし   | 該当なし          | INT32                                                                                                                                                               |

## トラブルシューティング {#troubleshooting}

### データのインポート中に警告を解決する {#resolve-warnings-during-data-import}

**[インポートの開始]**をクリックした後、 `can't find the corresponding source files`などの警告メッセージが表示された場合は、正しいソース ファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、 **[詳細設定]**を使用して変更を加えることで、この問題を解決します。

これらの問題を解決した後、データを再度インポートする必要があります。

### インポートされたテーブルに行が 0 行あります {#zero-rows-in-the-imported-tables}

インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。行数が0の場合、入力したバケットURIに一致するデータファイルが存在しないことを意味します。この場合、正しいソースファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**詳細設定**を使用して変更を加えることで問題を解決してください。その後、該当するテーブルを再度インポートしてください。
