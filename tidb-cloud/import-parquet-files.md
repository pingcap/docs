---
title: Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# Apache Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする {#import-apache-parquet-files-from-amazon-s3-or-gcs-into-tidb-cloud}

非圧縮および Snappy 圧縮[アパッチ寄木細工](https://parquet.apache.org/)形式のデータ ファイルの両方をTiDB Cloudにインポートできます。このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Google Cloud Storage (GCS) からTiDB Cloudに Parquet ファイルをインポートする方法について説明します。

> **注記：**
>
> -   TiDB Cloud は、空のテーブルへの Parquet ファイルのインポートのみをサポートします。すでにデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従ってTiDB Cloudを使用して一時的な空のテーブルにデータをインポートし、その後`INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。
> -   TiDB 専用クラスターにチェンジフィードがある場合、現在のデータインポート機能は[物理インポートモード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を使用するため、データをクラスターにインポートできません ([**データのインポート]**ボタンが無効になります)。このモードでは、インポートされたデータは変更ログを生成しないため、変更フィードはインポートされたデータを検出できません。
> -   TiDB 専用クラスターのみが GCS からの Parquet ファイルのインポートをサポートしています。

## ステップ 1. Parquet ファイルを準備する {#step-1-prepare-the-parquet-files}

> **注記：**
>
> 現在、 TiDB Cloud は、次のデータ タイプのいずれかを含む Parquet ファイルのインポートをサポートしていません。インポートする Parquet ファイルにそのようなデータ型が含まれている場合は、最初に[サポートされているデータ型](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。あるいは、AWS Glue などのサービスを使用して、データ型を簡単に変換することもできます。
>
> -   `LIST`
> -   `NEST STRUCT`
> -   `BOOL`
> -   `ARRAY`
> -   `MAP`

1.  Parquet ファイルが 256 MB より大きい場合は、ファイルを 256 MB 程度の小さなファイルに分割することを検討してください。

    TiDB Cloudは非常に大きな Parquet ファイルのインポートをサポートしていますが、サイズが約 256 MB の複数の入力ファイルで最適なパフォーマンスを発揮します。これは、 TiDB Cloud が複数のファイルを並行して処理できるため、インポート速度が大幅に向上する可能性があります。

2.  Parquet ファイルに次のように名前を付けます。

    -   Parquet ファイルにテーブル全体のすべてのデータが含まれている場合は、ファイルに`${db_name}.${table_name}.parquet`形式で名前を付けます。これは、データをインポートするときに`${db_name}.${table_name}`テーブルにマップされます。

    -   1 つのテーブルのデータが複数の Parquet ファイルに分割されている場合は、これらの Parquet ファイルに数値の接尾辞を追加します。たとえば、 `${db_name}.${table_name}.000001.parquet`と`${db_name}.${table_name}.000002.parquet`です。数値接尾辞は連続していなくてもかまいませんが、昇順である必要があります。また、すべての接尾辞が同じ長さになるように、数値の前にゼロを追加する必要があります。

    > **注記：**
    >
    > 場合によっては、前述のルールに従って Parquet ファイル名を更新できない場合 (たとえば、Parquet ファイル リンクが他のプログラムでも使用されている場合)、ファイル名を変更しないで、 [ステップ4](#step-4-import-parquet-files-to-tidb-cloud)の**マッピング設定**を使用してソース データをインポートできます。単一のターゲットテーブルに。

## ステップ 2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schemas}

Parquet ファイルにはスキーマ情報が含まれていないため、Parquet ファイルからTiDB Cloudにデータをインポートする前に、次のいずれかの方法を使用してテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloudで、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリで、次のようにソース データのターゲット テーブル スキーマ ファイルを作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        Parquet ファイルが[ステップ1](#step-1-prepare-the-parquet-files)の命名規則に従っている場合、データベース スキーマ ファイルはデータ インポートのオプションになります。それ以外の場合、データベース スキーマ ファイルは必須です。

        各データベース スキーマ ファイルは`${db_name}-schema-create.sql`形式であり、 `CREATE DATABASE` DDL ステートメントが含まれている必要があります。データをインポートするときに、このファイルを使用して、 TiDB Cloud はデータを保存する`${db_name}`を作成します。

        たとえば、次のステートメントを含む`mydb-scehma-create.sql`ファイルを作成すると、データのインポート時にTiDB Cloud は`mydb`データベースを作成します。

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリにテーブル スキーマ ファイルを含めない場合、データのインポート時にTiDB Cloudは対応するテーブルを作成しません。

        各テーブル スキーマ ファイルは`${db_name}.${table_name}-schema.sql`形式であり、 `CREATE TABLE` DDL ステートメントが含まれている必要があります。データをインポートすると、このファイルを使用して、 TiDB Cloud は`${db_name}`データベースに`${db_table}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、データをインポートすると、 TiDB Cloud は`mydb`データベースに`mytable`テーブルを作成します。

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **注記：**
        >
        > 各ファイルには`${db_name}.${table_name}-schema.sql`つの DDL ステートメントのみを含める必要があります。ファイルに複数の DDL ステートメントが含まれている場合、最初の DDL ステートメントのみが有効になります。

## ステップ 3. クロスアカウント アクセスを構成する {#step-3-configure-cross-account-access}

TiDB Cloud がAmazon S3 または GCS バケット内の Parquet ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   Parquet ファイルが Amazon S3 にある場合、 [Amazon S3 アクセスを設定する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access) .

    AWS アクセス キーまたはロール ARN を使用してバケットにアクセスできます。完了したら、アクセス キー (アクセス キー ID とシークレット アクセス キーを含む) またはロール ARN 値をメモします ( [ステップ4](#step-4-import-parquet-files-to-tidb-cloud)で必要になります)。

-   Parquet ファイルが GCS にある場合は、 [GCS アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access) 。

## ステップ 4. Parquet ファイルをTiDB Cloudにインポートする {#step-4-import-parquet-files-to-tidb-cloud}

Parquet ファイルをTiDB Cloudにインポートするには、次の手順を実行します。

1.  ターゲットクラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **インポート**ページで:
    -   TiDB 専用クラスターの場合は、右上隅にある**「データのインポート」**をクリックします。
    -   TiDB サーバーレス クラスターの場合は、アップロード領域の上にある**[S3 からデータをインポート]**リンクをクリックします。

3.  ソース Parquet ファイルについて次の情報を指定します。

    -   **場所**: **Amazon S3**を選択します。
    -   **データ形式**: **「Parquet」**を選択します。
    -   **バケット URI** : Parquet ファイルが配置されているバケット URI を選択します。 URI の末尾に`/`含める必要があることに注意してください (例: `s3://sampledate/ingest/` )。
    -   **バケット アクセス**(このフィールドは AWS S3 でのみ表示されます): AWS アクセス キーまたはロール ARN を使用してバケットにアクセスできます。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。
        -   **AWS アクセス キー**: AWS アクセス キー ID と AWS シークレット アクセス キーを入力します。
        -   **AWS ロール ARN** : ロール ARN 値を入力します。

4.  **事前に作成されたテーブルにインポートする**か、 **S3 からスキーマとデータをインポートするか**を選択できます。

    -   **事前に作成されたテーブルにインポートを使用**すると、事前に TiDB にテーブルを作成し、データをインポートするテーブルを選択できます。この場合、インポートするテーブルを最大 1000 個選択できます。左側のナビゲーション ペインで**Chat2Qury を**クリックしてテーブルを作成できます。 Chat2Qury の使用方法の詳細については、 [AI を活用した Chat2Query でデータを探索する](/tidb-cloud/explore-data-with-chat2query.md)を参照してください。
    -   **S3 からスキーマとデータをインポートすると、**テーブルを作成するための SQL スクリプトをインポートし、S3 に保存されている対応するテーブル データを TiDB にインポートできます。

5.  ソース ファイルが命名規則を満たしていない場合は、単一のターゲット テーブルと CSV ファイルの間にカスタム マッピング ルールを指定できます。その後、提供されたカスタム マッピング ルールを使用してデータ ソース ファイルが再スキャンされます。マッピングを変更するには、 **[詳細設定]**をクリックし、 **[マッピング設定]**をクリックします。 **[マッピング設定] は、** **[事前作成されたテーブルにインポート] を**選択した場合にのみ使用できることに注意してください。

    -   **ターゲット データベース**: 選択したターゲット データベースの名前を入力します。

    -   **ターゲット テーブル**: 選択したターゲット テーブルの名前を入力します。このフィールドは 1 つの特定のテーブル名のみを受け入れるため、ワイルドカードはサポートされていないことに注意してください。

    -   **ソース ファイルの URI と名前**: ソース ファイルの URI と名前を次の形式で入力します。 `s3://[bucket_name]/[data_source_folder]/[file_name].parquet` .たとえば、 `s3://sampledate/ingest/TableName.01.parquet` 。ワイルドカードを使用してソース ファイルと一致させることもできます。例えば：

        -   `s3://[bucket_name]/[data_source_folder]/my-data?.parquet` : そのフォルダー内の`my-data`と 1 文字 ( `my-data1.parquet`や`my-data2.parquet`など) で始まるすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
        -   `s3://[bucket_name]/[data_source_folder]/my-data*.parquet` : `my-data`で始まるフォルダー内のすべての Parquet ファイルが同じターゲット テーブルにインポートされます。

        `?`と`*`のみがサポートされることに注意してください。

        > **注記：**
        >
        > URI にはデータ ソース フォルダーが含まれている必要があります。

6.  **[インポートの開始]**をクリックします。

7.  インポートの進行状況に**Completed**と表示されたら、インポートされたテーブルを確認します。

インポート タスクを実行するときに、サポートされていない変換または無効な変換が検出された場合、 TiDB Cloudはインポート ジョブを自動的に終了し、インポート エラーを報告します。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。

2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブル スキーマ ファイルを修正します。

3.  Parquet ファイルのデータ型を確認してください。

    Parquet ファイルにサポートされていないデータ型 (たとえば、 `NEST STRUCT` 、 `ARRAY` 、または`MAP` ) が含まれている場合は、 [サポートされているデータ型](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。

4.  インポートタスクを再試行してください。

## サポートされているデータ型 {#supported-data-types}

次の表に、 TiDB Cloudにインポートできるサポートされている Parquet データ タイプを示します。

| 寄木細工のプリミティブ タイプ         | 寄木細工の論理タイプ       | TiDB または MySQL の型                                                                                                                                                            |
| ----------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ダブル                     | ダブル              | ダブル<br/>浮く                                                                                                                                                                   |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)    | BIGINT 署名なし                                                                                                                                                                  |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                                  |
| INT32                   | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                                  |
| INT32                   | 該当なし             | INT<br/>ミディアムミント<br/>年                                                                                                                                                       |
| INT64                   | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                                  |
| INT64                   | 該当なし             | BIGINT<br/> INT 符号なし<br/>ミディアムミント未署名                                                                                                                                         |
| INT64                   | TIMESTAMP_MICROS | 日付時刻<br/>タイムスタンプ                                                                                                                                                             |
| バイト配列                   | 該当なし             | バイナリ<br/>少し<br/>BLOB<br/>チャー<br/>ラインストリング<br/>ロングブロブ<br/>ミディアムブロブ<br/>複数行の文字列<br/>タイニーブロブ<br/>ヴァービナリー                                                                        |
| バイト配列                   | 弦                | ENUM<br/>日付<br/>10進数<br/>幾何学模様<br/>ジオメトリコレクション<br/>JSON<br/>長文<br/>メディアテキスト<br/>マルチポイント<br/>マルチポリゴン<br/>数値<br/>ポイント<br/>ポリゴン<br/>セット<br/>TEXT<br/>時間<br/>小さなテキスト<br/>VARCHAR |
| スモールント                  | 該当なし             | INT32                                                                                                                                                                        |
| 小さな署名なし                 | 該当なし             | INT32                                                                                                                                                                        |
| タイイント                   | 該当なし             | INT32                                                                                                                                                                        |
| TINYINT 署名なし            | 該当なし             | INT32                                                                                                                                                                        |

## トラブルシューティング {#troubleshooting}

### データインポート中の警告を解決する {#resolve-warnings-during-data-import}

**[インポートの開始]**をクリックした後、 `can't find the corresponding source files`などの警告メッセージが表示された場合は、正しいソース ファイルを提供するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、**詳細設定を**使用して変更することで問題を解決します。

これらの問題を解決した後、データを再度インポートする必要があります。

### インポートされたテーブルの行がゼロ {#zero-rows-in-the-imported-tables}

インポートの進行状況に**Completed**と表示されたら、インポートされたテーブルを確認します。行数がゼロの場合は、入力したバケット URI に一致するデータ ファイルがなかったことを意味します。この場合、正しいソース ファイルを提供するか、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に従って既存のファイルの名前を変更するか、または**詳細設定**を使用して変更を加えることで、この問題を解決します。その後、それらのテーブルを再度インポートします。
