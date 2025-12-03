---
title: Import CSV Files from Cloud Storage into TiDB Cloud Premium
summary: Amazon S3 または Alibaba Cloud Object Storage Service (OSS) からTiDB Cloud Premium インスタンスに CSV ファイルをインポートする方法を学びます。
---

# クラウドストレージからTiDB Cloud PremiumにCSVファイルをインポートする {#import-csv-files-from-cloud-storage-into-tidb-cloud-premium}

このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Alibaba Cloud Object Storage Service (OSS) からTiDB Cloud Premium インスタンスに CSV ファイルをインポートする方法について説明します。

> **警告：**
>
> TiDB Cloud Premium は現在、一部の AWS リージョンで**プライベートプレビュー**としてご利用いただけます。
>
> 組織で Premium がまだ有効になっていない場合、または別のクラウド プロバイダーやリージョンでアクセスする必要がある場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[サポート]**をクリックするか、Web サイトの[お問い合わせ](https://www.pingcap.com/contact-us)フォームからリクエストを送信してください。

> **ヒント：**
>
> -   TiDB Cloud Starter または Essential については、 [クラウドストレージからTiDB Cloud StarterまたはEssentialにCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)参照してください。
> -   TiDB Cloud Dedicated については、 [クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)参照してください。

## 制限事項 {#limitations}

データの整合性を確保するため、 TiDB Cloud PremiumではCSVファイルのインポートは空のテーブルのみに制限されています。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従って一時的な空のテーブルにデータをインポートし、その後、 `INSERT SELECT`ステートメントを使用してデータを対象の既存テーブルにコピーします。

## ステップ1.CSVファイルを準備する {#step-1-prepare-the-csv-files}

1.  CSV ファイルが 256 MiB より大きい場合は、サイズがそれぞれ約 256 MiB の小さなファイルに分割することを検討してください。

    TiDB Cloud Premiumは非常に大きなCSVファイルのインポートをサポートしていますが、256MiB程度の複数の入力ファイルで最適なパフォーマンスを発揮します。これは、 TiDB Cloud Premiumが複数のファイルを並列処理できるため、インポート速度が大幅に向上するからです。

2.  CSV ファイルに次のように名前を付けます。

    -   CSV ファイルにテーブル全体のすべてのデータが含まれている場合は、データをインポートするときに`${db_name}.${table_name}`テーブルにマップされる`${db_name}.${table_name}.csv`形式でファイルに名前を付けます。

    -   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加します。例： `${db_name}.${table_name}.000001.csv`と`${db_name}.${table_name}.000002.csv`数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

    -   TiDB Cloud Premiumは`.gz`以下の形式の圧縮ファイルのインポートをサポートしています： `.gzip` `.snappy`圧縮`.zstd`れたCSVファイルをインポートする場合は、ファイル名`.zst` `${db_name}.${table_name}.${suffix}.csv.${compress}`形式にしてください。13 `${suffix}`オプションで、「000001」などの任意の整数にすることができます。例えば、 `trips.000001.csv.gz`ファイルを`bikeshare.trips`テーブルにインポートする場合は、ファイル名を`bikeshare.trips.000001.csv.gz`に変更する必要があります。

    > **注記：**
    >
    > -   パフォーマンスを向上させるには、各圧縮ファイルのサイズを 100 MiB に制限することをお勧めします。
    > -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。
    > -   非圧縮ファイルの場合、前述のルールに従って CSV ファイル名を更新できないケース (たとえば、CSV ファイル リンクが他のプログラムでも使用されている場合) は、ファイル名を変更せずに、 [ステップ4](#step-4-import-csv-files)の**マッピング設定**を使用してソース データを単一のターゲット テーブルにインポートできます。

## ステップ2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schemas}

CSV ファイルにはスキーマ情報が含まれていないため、CSV ファイルからTiDB Cloud Premium にデータをインポートする前に、次のいずれかの方法でテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloud Premium で、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: CSV ファイルが保存されている Amazon S3 または Alibaba Cloud Object Storage Service (OSS) ディレクトリで、次のようにソース データのターゲット テーブル スキーマ ファイルを作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        CSVファイルが[ステップ1](#step-1-prepare-the-csv-files)命名規則に従っている場合、データベーススキーマファイルはデータのインポートに必須ではありません。そうでない場合は、データベーススキーマファイルは必須です。

        各データベーススキーマファイルは`${db_name}-schema-create.sql`形式で、 `CREATE DATABASE` DDLステートメントを含んでいる必要があります。このファイルを使用して、 TiDB Cloud Premiumはデータをインポートする際に、データを格納するための`${db_name}`データベースを作成します。

        たとえば、次のステートメントを含む`mydb-schema-create.sql`ファイルを作成すると、 TiDB Cloud Premium はデータをインポートするときに`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        CSV ファイルが保存されている Amazon S3 または Alibaba Cloud Object Storage Service ディレクトリにテーブル スキーマ ファイルを含めない場合、 TiDB Cloud Premium はデータをインポートするときに対応するテーブルを作成しません。

        各テーブルスキーマファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDLステートメントを含む必要があります。このファイルを使用することで、 TiDB Cloud Premiumはデータをインポートする際に`${db_name}`データベースに`${table_name}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、 TiDB Cloud Premium は、データをインポートするときに`mydb`データベースに`mytable`テーブルを作成します。

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

TiDB Cloud Premium が Amazon S3 または Alibaba Cloud Object Storage Service (OSS) 内の CSV ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   CSV ファイルが Amazon S3 にある場合は、TiDB インスタンス用に[Amazon S3 アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access) 。

    バケットへのアクセスには、AWS アクセスキーまたはロール ARN のいずれかを使用できます。完了したら、アクセスキー（アクセスキー ID とシークレットアクセスキーを含む）またはロール ARN の値をメモしておいてください。これらは[ステップ4](#step-4-import-csv-files)で必要になります。

-   CSV ファイルが Alibaba Cloud Object Storage Service (OSS) にある場合は、TiDB インスタンスごとに[Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access) 。

## ステップ4.CSVファイルをインポートする {#step-4-import-csv-files}

CSV ファイルをTiDB Cloud Premium にインポートするには、次の手順を実行します。

<SimpleTab>
<div label="Amazon S3">

1.  ターゲット TiDB インスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

    2.  ターゲット TiDB インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**をクリックします。

3.  **「クラウド ストレージからのデータのインポート」**ページで、次の情報を入力します。

    -   **ストレージプロバイダー**: **Amazon S3**を選択します。
    -   **ソースファイルURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIを次の形式で入力します`s3://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `s3://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを次の形式で入力します`s3://[bucket_name]/[data_source_folder]/` 。例： `s3://sampledata/ingest/` 。
    -   **認証情報**: バケットにアクセスするには、AWS ロール ARN または AWS アクセスキーのいずれかを使用できます。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access)参照してください。
        -   **AWS ロール ARN** : AWS ロール ARN 値を入力します。新しいロールを作成する必要がある場合は、 **「AWS CloudFormation で新しいロールを作成するには、こちらをクリックしてください」を**クリックし、ガイドに従って提供されたテンプレートを起動し、 IAM の警告を確認してスタックを作成し、生成された ARN をTiDB Cloud Premium にコピーします。
        -   **AWS アクセスキー**: AWS アクセスキー ID と AWS シークレットアクセスキーを入力します。
    -   **バケット アクセスのテスト**: 資格情報が設定された後、このボタンをクリックして、 TiDB Cloud Premium がバケットにアクセスできることを確認します。
    -   **ターゲット接続**: インポートを実行するTiDBのユーザー名とパスワードを入力します。必要に応じて、 **「接続テスト」を**クリックして資格情報を検証します。

4.  **「次へ」**をクリックします。

5.  **ソース ファイル マッピング**セクションでは、 TiDB Cloud Premium がバケットをスキャンし、ソース ファイルと宛先テーブル間のマッピングを提案します。

    **ソース ファイル URI**にディレクトリを指定すると、**自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**に単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloud Premiumによって**ソース**フィールドにファイル名が自動的に入力されます。この場合、データのインポート対象となるデータベースとテーブルを選択するだけで済みます。

    -   自動マッピングを有効のままにしておくと、ソースファイルとターゲットテーブルに[ファイルの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)適用されます。データ形式は**CSV**のままにしておいてください。

    -   **詳細オプション**：パネルを展開すると、 `Ignore compatibility checks (advanced)`トグルが表示されます。スキーマ互換性検証を意図的にバイパスする場合を除き、無効のままにしてください。

    <!-- future feature -->

    > **注記：**
    >
    > 手動マッピングは近日中に利用可能になります。切り替えボタンが利用可能になったら、自動マッピングオプションをオフにして、手動でマッピングを設定してください。
    >
    > -   **ソース**: `TableName.01.csv`のようなファイル名パターンを入力します。ワイルドカード`*`と`?`サポートされています (例: `my-data*.csv` )。
    > -   **ターゲット データベース**と**ターゲット テーブル**: 一致したファイルの宛先オブジェクトを選択します。

6.  TiDB Cloud Premiumはソースパスを自動的にスキャンします。スキャン結果を確認し、見つかったデータファイルと対応するターゲットテーブルを確認して、 **「インポートを開始」を**クリックします。

7.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認します。

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1.  ターゲット TiDB インスタンスの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

    2.  ターゲット TiDB インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[インポート]**をクリックします。

2.  **「Cloud Storage からデータをインポート」**をクリックします。

3.  **「クラウド ストレージからのデータのインポート」**ページで、次の情報を入力します。

    -   **ストレージプロバイダー**: **Alibaba Cloud OSS**を選択します。
    -   **ソースファイルURI** :
        -   1つのファイルをインポートする場合は、ソースファイルのURIを次の形式で入力します`oss://[bucket_name]/[data_source_folder]/[file_name].csv` 。たとえば、 `oss://sampledata/ingest/TableName.01.csv` 。
        -   複数のファイルをインポートする場合は、ソースフォルダのURIを次の形式で入力します`oss://[bucket_name]/[data_source_folder]/` 。例： `oss://sampledata/ingest/` 。
    -   **認証情報**: AccessKeyペアを使用してバケットにアクセスできます。詳細については、 [Alibaba Cloud Object Storage Service (OSS) アクセスを構成する](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access)ご覧ください。
    -   **バケット アクセスのテスト**: 資格情報が設定された後、このボタンをクリックして、 TiDB Cloud Premium がバケットにアクセスできることを確認します。
    -   **ターゲット接続**: インポートを実行するTiDBのユーザー名とパスワードを入力します。必要に応じて、 **「接続テスト」を**クリックして資格情報を検証します。

4.  **「次へ」**をクリックします。

5.  **ソース ファイル マッピング**セクションでは、 TiDB Cloud Premium がバケットをスキャンし、ソース ファイルと宛先テーブル間のマッピングを提案します。

    **ソース ファイル URI**にディレクトリを指定すると、**自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する**オプションがデフォルトで選択されます。

    > **注記：**
    >
    > **ソースファイルURI**に単一のファイルが指定されている場合、 **「自動マッピングに<a href="/tidb-cloud/naming-conventions-for-data-import.md">ファイル命名規則</a>を使用する」**オプションは表示されず、 TiDB Cloud Premiumによって**ソース**フィールドにファイル名が自動的に入力されます。この場合、データのインポート対象となるデータベースとテーブルを選択するだけで済みます。

    -   自動マッピングを有効のままにしておくと、ソースファイルとターゲットテーブルに[ファイルの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)適用されます。データ形式は**CSV**のままにしておいてください。

    -   **詳細オプション**：パネルを展開すると、 `Ignore compatibility checks (advanced)`トグルが表示されます。スキーマ互換性検証を意図的にバイパスする場合を除き、無効のままにしてください。

    <!-- future feature -->

    > **注記：**
    >
    > 手動マッピングは近日中に利用可能になります。切り替えボタンが利用可能になったら、自動マッピングオプションをオフにして、手動でマッピングを設定してください。
    >
    > -   **ソース**: `TableName.01.csv`のようなファイル名パターンを入力します。ワイルドカード`*`と`?`サポートされています (例: `my-data*.csv` )。
    > -   **ターゲット データベース**と**ターゲット テーブル**: 一致したファイルの宛先オブジェクトを選択します。

6.  TiDB Cloud Premiumはソースパスを自動的にスキャンします。スキャン結果を確認し、見つかったデータファイルと対応するターゲットテーブルを確認して、 **「インポートを開始」を**クリックします。

7.  インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認します。

</div>

</SimpleTab>

インポート タスクを実行するときに、サポートされていない変換または無効な変換が検出されると、 TiDB Cloud Premium はインポート ジョブを自動的に終了し、インポート エラーを報告します。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。
2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブルスキーマファイルを修正してください。
3.  CSV ファイル内のデータ型を確認します。
4.  インポートタスクをもう一度試してください。

## トラブルシューティング {#troubleshooting}

### データのインポート中に発生する警告を解決する {#resolve-warnings-during-data-import}

**[インポートの開始]**をクリックした後、 `can't find the corresponding source files`などの警告メッセージが表示された場合は、正しいソース ファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、 **[詳細設定]**を使用して変更を加えることで、この問題を解決します。

これらの問題を解決した後、データを再度インポートする必要があります。

### インポートされたテーブルに行が 0 行あります {#zero-rows-in-the-imported-tables}

インポートの進行状況が**「完了」**と表示されたら、インポートされたテーブルを確認してください。行数が0の場合、入力したバケットURIに一致するデータファイルが存在しないことを意味します。この場合、正しいソースファイルを指定するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**詳細設定**を使用して変更を加えることで問題を解決してください。その後、該当するテーブルを再度インポートしてください。
