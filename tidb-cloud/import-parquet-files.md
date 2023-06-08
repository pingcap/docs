---
title: Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# Apache Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする {#import-apache-parquet-files-from-amazon-s3-or-gcs-into-tidb-cloud}

非圧縮および Snappy 圧縮[<a href="https://parquet.apache.org/">アパッチ寄木細工</a>](https://parquet.apache.org/)形式のデータ ファイルの両方をTiDB Cloudにインポートできます。このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Google Cloud Storage (GCS) からTiDB Cloudに Parquet ファイルをインポートする方法について説明します。

> **ノート：**
>
> -   TiDB Cloud は、空のテーブルへの Parquet ファイルのインポートのみをサポートします。すでにデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従ってTiDB Cloudを使用して一時的な空のテーブルにデータをインポートし、その後`INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。
> -   TiDB Dedicatedクラスターにチェンジフィードがある場合、現在のデータインポート機能は[<a href="https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode">物理インポートモード</a>](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を使用するため、データをクラスターにインポートできません ([**データのインポート]**ボタンが無効になります)。このモードでは、インポートされたデータは変更ログを生成しないため、変更フィードはインポートされたデータを検出できません。

## ステップ 1. Parquet ファイルを準備する {#step-1-prepare-the-parquet-files}

> **ノート：**
>
> 現在、 TiDB Cloud は、次のデータ タイプのいずれかを含む Parquet ファイルのインポートをサポートしていません。インポートする Parquet ファイルにそのようなデータ型が含まれている場合は、最初に[<a href="#supported-data-types">サポートされているデータ型</a>](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。あるいは、AWS Glue などのサービスを使用して、データ型を簡単に変換することもできます。
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

    > **ノート：**
    >
    > 場合によっては、前述のルールに従って Parquet ファイル名を更新できない場合 (たとえば、Parquet ファイル リンクが他のプログラムでも使用されている場合)、ファイル名を変更しないで、 [<a href="#step-4-import-parquet-files-to-tidb-cloud">ステップ4</a>](#step-4-import-parquet-files-to-tidb-cloud)**ファイル パターン**を使用してソース データをインポートできます。単一のターゲットテーブルに。

## ステップ 2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schemas}

Parquet ファイルにはスキーマ情報が含まれていないため、Parquet ファイルからTiDB Cloudにデータをインポートする前に、次のいずれかの方法を使用してテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloudで、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリで、次のようにソース データのターゲット テーブル スキーマ ファイルを作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        Parquet ファイルが[<a href="#step-1-prepare-the-parquet-files">ステップ1</a>](#step-1-prepare-the-parquet-files)の命名規則に従っている場合、データベース スキーマ ファイルはデータ インポートのオプションになります。それ以外の場合、データベース スキーマ ファイルは必須です。

        各データベース スキーマ ファイルは`${db_name}-schema-create.sql`形式であり、 `CREATE DATABASE` DDL ステートメントが含まれている必要があります。データをインポートするときに、このファイルを使用して、 TiDB Cloud はデータを保存する`${db_name}`を作成します。

        たとえば、次のステートメントを含む`mydb-scehma-create.sql`ファイルを作成すると、データのインポート時にTiDB Cloud は`mydb`データベースを作成します。

        {{< copyable "" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリにテーブル スキーマ ファイルを含めない場合、データのインポート時にTiDB Cloudは対応するテーブルを作成しません。

        各テーブル スキーマ ファイルは`${db_name}.${table_name}-schema.sql`形式であり、 `CREATE TABLE` DDL ステートメントが含まれている必要があります。データをインポートすると、このファイルを使用して、 TiDB Cloud は`${db_name}`データベースに`${db_table}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、データをインポートすると、 TiDB Cloud は`mydb`データベースに`mytable`テーブルを作成します。

        {{< copyable "" >}}

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **ノート：**
        >
        > 各ファイルには`${db_name}.${table_name}-schema.sql`つの DDL ステートメントのみを含める必要があります。ファイルに複数の DDL ステートメントが含まれている場合、最初の DDL ステートメントのみが有効になります。

## ステップ 3. クロスアカウント アクセスを構成する {#step-3-configure-cross-account-access}

TiDB Cloud がAmazon S3 または GCS バケット内の Parquet ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   Parquet ファイルが Amazon S3 にある場合、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを設定する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access) .

    AWS アクセス キーまたはロール ARN を使用してバケットにアクセスできます。完了したら、アクセス キー (アクセス キー ID とシークレット アクセス キーを含む) またはロール ARN 値をメモします ( [<a href="#step-4-import-parquet-files-to-tidb-cloud">ステップ4</a>](#step-4-import-parquet-files-to-tidb-cloud)で必要になります)。

-   Parquet ファイルが GCS にある場合は、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access">GCS アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access) 。

## ステップ 4. Parquet ファイルをTiDB Cloudにインポートする {#step-4-import-parquet-files-to-tidb-cloud}

Parquet ファイルをTiDB Cloudにインポートするには、次の手順を実行します。

1.  ターゲットクラスターの**インポート**ページを開きます。

    1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

2.  **インポート**ページで:
    -   TiDB Dedicatedクラスターの場合は、右上隅にある**「データのインポート」**をクリックします。
    -   TiDB Serverless クラスターの場合は、アップロード領域の上にある**[S3 からデータをインポート]**リンクをクリックします。

3.  ソース Parquet ファイルについて次の情報を指定します。

    -   **データ形式**: **「Parquet」**を選択します。
    -   **バケット URI** : Parquet ファイルが配置されているバケット URI を選択します。
    -   **バケット アクセス**(このフィールドは AWS S3 でのみ表示されます): AWS アクセス キーまたはロール ARN を使用してバケットにアクセスできます。詳細については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。
        -   **AWS アクセス キー**: アクセス キー ID とシークレット アクセス キーを入力します。
        -   **ロール ARN** :**ロール ARN**のロール ARN 値を入力します。

    バケットのリージョンがクラスターと異なる場合は、クロスリージョンのコンプライアンスを確認してください。 **「次へ」**をクリックします。

    TiDB Cloudは、指定されたバケット URI 内のデータにアクセスできるかどうかの検証を開始します。検証後、 TiDB Cloudはデフォルトのファイル命名パターンを使用してデータ ソース内のすべてのファイルをスキャンしようとします。 `AccessDenied`エラーが発生した場合は、 [<a href="/tidb-cloud/troubleshoot-import-access-denied-error.md">S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング</a>](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

4.  必要に応じて、ファイル パターンを変更し、テーブル フィルター ルールを追加します。

    -   **ファイル パターン**: ファイル名が特定のパターンに一致する Parquet ファイルを単一のターゲット テーブルにインポートする場合は、ファイル パターンを変更します。

        > **ノート：**
        >
        > この機能を使用する場合、1 つのインポート タスクは一度に 1 つのテーブルにのみデータをインポートできます。この機能を使用してデータを別のテーブルにインポートする場合は、毎回異なるターゲット テーブルを指定して、複数回インポートする必要があります。

        ファイル パターンを変更するには、 **[ファイル パターン]**をクリックし、次のフィールドで Parquet ファイルと単一のターゲット テーブル間のカスタム マッピング ルールを指定し、 **[保存]**をクリックします。その後、提供されたカスタム マッピング ルールを使用してデータ ソース ファイルが再スキャンされます。

        -   **ソース ファイル名**: インポートする Parquet ファイルの名前と一致するパターンを入力します。 Parquet ファイルが 1 つだけの場合は、ここにファイル名を直接入力できます。 Parquet ファイルの名前には接尾辞`.parquet`が含まれている必要があることに注意してください。

            例えば：

            -   `my-data?.parquet` : `my-data`と 1 文字 ( `my-data1.parquet`や`my-data2.parquet`など) で始まるすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
            -   `my-data*.parquet` : `my-data`で始まるすべての Parquet ファイルが同じターゲット テーブルにインポートされます。

        -   **ターゲット テーブル名**: TiDB Cloudのターゲット テーブルの名前を入力します。これは`${db_name}.${table_name}`形式である必要があります。たとえば、 `mydb.mytable` 。このフィールドは 1 つの特定のテーブル名のみを受け入れるため、ワイルドカードはサポートされていないことに注意してください。

    -   **テーブル フィルター**: インポートするテーブルをフィルターする場合は、この領域でテーブル フィルター ルールを指定できます。

        例えば：

        -   `db01.*` : `db01`データベース内のすべてのテーブルがインポートされます。
        -   `!db02.*` : `db02`データベース内のテーブルを除き、他のすべてのテーブルがインポートされます。 `!`は、インポートする必要のないテーブルを除外するために使用されます。
        -   `*.*` : すべてのテーブルがインポートされます。

        詳細については、 [<a href="/table-filter.md#syntax">テーブルフィルターの構文</a>](/table-filter.md#syntax)を参照してください。

5.  **「次へ」**をクリックします。

6.  **[プレビュー]**ページで、インポートするデータを確認し、 **[インポートの開始]**をクリックします。

7.  インポートの進行状況に**「 Finished 」**と表示されたら、インポートされたテーブルを確認します。

    数値が 0 の場合は、 **[ソース ファイル名]**フィールドに入力した値と一致するデータ ファイルがないことを意味します。この場合は、 **「ソースファイル名」**フィールドにタイプミスがないか確認して、再試行してください。

8.  インポート タスクが完了したら、 **[インポート]**ページの**[データのクエリ]**をクリックして、インポートされたデータをクエリできます。 Chat2Qury の使用方法の詳細については、 [<a href="/tidb-cloud/explore-data-with-chat2query.md">AI を活用した Chat2Query でデータを探索する</a>](/tidb-cloud/explore-data-with-chat2query.md)を参照してください。

インポート タスクを実行するときに、サポートされていない変換または無効な変換が検出された場合、 TiDB Cloudはインポート ジョブを自動的に終了し、インポート エラーを報告します。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。

2.  テーブルスキーマファイルを確認してください。エラーがある場合は、テーブル スキーマ ファイルを修正します。

3.  Parquet ファイルのデータ型を確認してください。

    Parquet ファイルにサポートされていないデータ型 (たとえば、 `NEST STRUCT` 、 `ARRAY` 、または`MAP` ) が含まれている場合は、 [<a href="#supported-data-types">サポートされているデータ型</a>](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。

4.  インポートタスクを再試行してください。

## サポートされているデータ型 {#supported-data-types}

次の表に、 TiDB Cloudにインポートできるサポートされている Parquet データ タイプを示します。

| 寄木細工のプリミティブ タイプ         | 寄木細工の論理タイプ       | TiDB または MySQL の型                                                                                                                                                         |
| ----------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ダブル                     | ダブル              | ダブル<br/>浮く                                                                                                                                                                |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)    | BIGINT 署名なし                                                                                                                                                               |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                               |
| INT32                   | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                               |
| INT32                   | 該当なし             | INT<br/>ミディアムミント<br/>年                                                                                                                                                    |
| INT64                   | DECIMAL(p,s)     | 10進数<br/>数値                                                                                                                                                               |
| INT64                   | 該当なし             | BIGINT<br/> INT 符号なし<br/>ミディアムミント未署名                                                                                                                                      |
| INT64                   | TIMESTAMP_MICROS | 日付時刻<br/>タイムスタンプ                                                                                                                                                          |
| バイト配列                   | 該当なし             | バイナリ<br/>少し<br/>BLOB<br/>チャー<br/>ラインストリング<br/>ロングブロブ<br/>ミディアムブロブ<br/>複数行の文字列<br/>タイニーブロブ<br/>ヴァービナリー                                                                     |
| バイト配列                   | 弦                | ENUM<br/>日にち<br/>10進数<br/>幾何学模様<br/>ジオメトリコレクション<br/>JSON<br/>長文<br/>メディアテキスト<br/>マルチポイント<br/>マルチポリゴン<br/>数値<br/>点<br/>ポリゴン<br/>設定<br/>TEXT<br/>時間<br/>小さなテキスト<br/>VARCHAR |
| スモールント                  | 該当なし             | INT32                                                                                                                                                                     |
| 小さな署名なし                 | 該当なし             | INT32                                                                                                                                                                     |
| タイイント                   | 該当なし             | INT32                                                                                                                                                                     |
| TINYINT 署名なし            | 該当なし             | INT32                                                                                                                                                                     |
