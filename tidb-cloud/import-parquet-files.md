---
title:  Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# Amazon S3 または GCS からTiDB Cloudに Apache Parquet ファイルをインポートする {#import-apache-parquet-files-from-amazon-s3-or-gcs-into-tidb-cloud}

非圧縮および Snappy 圧縮[アパッチ寄木細工](https://parquet.apache.org/)形式のデータ ファイルの両方をTiDB Cloudにインポートできます。このドキュメントでは、Amazon Simple Storage Service (Amazon S3) または Google Cloud Storage (GCS) からTiDB Cloudに Parquet ファイルをインポートする方法について説明します。

> **ノート：**
>
> TiDB Cloudは、空のテーブルへの Parquet ファイルのインポートのみをサポートしています。既にデータが含まれている既存のテーブルにデータをインポートするには、このドキュメントに従って、 TiDB Cloudを使用してデータを一時的な空のテーブルにインポートし、 `INSERT SELECT`ステートメントを使用してデータをターゲットの既存のテーブルにコピーします。

## ステップ 1.Parquet ファイルを準備する {#step-1-prepare-the-parquet-files}

> **ノート：**
>
> 現在、 TiDB Cloudは、次のデータ型のいずれかを含む Parquet ファイルのインポートをサポートしていません。インポートする Parquet ファイルにそのようなデータ型が含まれている場合は、最初に[サポートされているデータ型](#supported-data-types) (たとえば、 `STRING` ) を使用して Parquet ファイルを再生成する必要があります。または、AWS Glue などのサービスを使用してデータ型を簡単に変換することもできます。
>
> -   `LIST`
> -   `NEST STRUCT`
> -   `BOOL`
> -   `ARRAY`
> -   `MAP`

1.  Parquet ファイルが 256 MB より大きい場合は、それぞれのサイズが約 256 MB の小さなファイルに分割することを検討してください。

    TiDB Cloudは、非常に大きな Parquet ファイルのインポートをサポートしていますが、サイズが 256 MB 前後の複数の入力ファイルで最高のパフォーマンスを発揮します。これは、 TiDB Cloudが複数のファイルを並行して処理できるため、インポート速度が大幅に向上する可能性があるためです。

2.  次のように Parquet ファイルに名前を付けます。

    -   Parquet ファイルにテーブル全体のすべてのデータが含まれている場合は、ファイルに`${db_name}.${table_name}.parquet`形式の名前を付けます。これは、データをインポートするときに`${db_name}.${table_name}`テーブルにマップされます。

    -   1 つのテーブルのデータが複数の Parquet ファイルに分割されている場合は、これらの Parquet ファイルに数値のサフィックスを追加します。たとえば、 `${db_name}.${table_name}.000001.parquet`と`${db_name}.${table_name}.000002.parquet`です。数値サフィックスは連続していなくてもかまいませんが、昇順でなければなりません。また、数字の前にゼロを追加して、すべてのサフィックスが同じ長さになるようにする必要もあります。

    > **ノート：**
    >
    > 上記のルールに従って Parquet ファイル名を更新できない場合 (たとえば、Parquet ファイル リンクが他のプログラムでも使用されている場合など) は、ファイル名を変更せずに[ステップ 4](#step-4-import-parquet-files-to-tidb-cloud)の**カスタム パターン**を使用してソース データをインポートできます。単一のターゲット テーブルに。

## ステップ 2. ターゲット表スキーマを作成する {#step-2-create-the-target-table-schemas}

Parquet ファイルにはスキーマ情報が含まれていないため、Parquet ファイルからTiDB Cloudにデータをインポートする前に、次のいずれかの方法を使用してテーブル スキーマを作成する必要があります。

-   方法 1: TiDB Cloudで、ソース データのターゲット データベースとテーブルを作成します。

-   方法 2: Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリで、ソース データのターゲット テーブル スキーマ ファイルを次のように作成します。

    1.  ソース データのデータベース スキーマ ファイルを作成します。

        Parquet ファイルが[ステップ1](#step-1-prepare-the-parquet-files)の命名規則に従っている場合、データベース スキーマ ファイルはデータ インポートのオプションです。それ以外の場合、データベース スキーマ ファイルは必須です。

        各データベース スキーマ ファイルは`${db_name}-schema-create.sql`形式で、 `CREATE DATABASE` DDL ステートメントを含む必要があります。このファイルを使用すると、 TiDB Cloudは、データをインポートするときにデータを格納するための`${db_name}`のデータベースを作成します。

        たとえば、次のステートメントを含む`mydb-scehma-create.sql`ファイルを作成すると、データをインポートするときにTiDB Cloudによって`mydb`データベースが作成されます。

        {{< copyable "" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2.  ソース データのテーブル スキーマ ファイルを作成します。

        Parquet ファイルが配置されている Amazon S3 または GCS ディレクトリにテーブル スキーマ ファイルを含めない場合、データをインポートするときに、 TiDB Cloudは対応するテーブルを作成しません。

        各テーブル スキーマ ファイルは`${db_name}.${table_name}-schema.sql`形式で、 `CREATE TABLE` DDL ステートメントを含む必要があります。このファイルを使用すると、データをインポートすると、 TiDB Cloudは`${db_name}`データベースに`${db_table}`テーブルを作成します。

        たとえば、次のステートメントを含む`mydb.mytable-schema.sql`ファイルを作成すると、データをインポートすると、 TiDB Cloudは`mydb`データベースに`mytable`テーブルを作成します。

        {{< copyable "" >}}

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **ノート：**
        >
        > 各`${db_name}.${table_name}-schema.sql`ファイルには、単一の DDL ステートメントのみを含める必要があります。ファイルに複数の DDL ステートメントが含まれている場合、最初のステートメントのみが有効になります。

## ステップ 3. クロスアカウント アクセスを構成する {#step-3-configure-cross-account-access}

TiDB Cloudが Amazon S3 または GCS バケット内の Parquet ファイルにアクセスできるようにするには、次のいずれかを実行します。

-   Parquet ファイルが Amazon S3 にある場合、 [Amazon S3 へのクロスアカウント アクセスを設定する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access) .

    完了したら、 [ステップ 4](#step-4-import-parquet-files-to-tidb-cloud)で必要になるため、Role ARN の値を書き留めます。

-   Parquet ファイルが GCS にある場合は、 [GCS へのクロスアカウント アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access) .

## ステップ 4. Parquet ファイルをTiDB Cloudにインポートする {#step-4-import-parquet-files-to-tidb-cloud}

Parquet ファイルをTiDB Cloudにインポートするには、次の手順を実行します。

1.  [**アクティブなクラスター]**ページに移動します。

2.  ターゲットクラスタの領域を見つけて、領域の右上隅にある [**データのインポート**] をクリックします。 [<strong>データ インポート タスク]</strong>ページが表示されます。

    > **ヒント：**
    >
    > または、[**アクティブなクラスター**] ページでターゲットクラスタの名前をクリックし、右上隅にある [<strong>データのインポート</strong>] をクリックすることもできます。

3.  [**データ インポート タスク]**ページで、次の情報を指定します。

    -   **データ ソース タイプ**: データ ソースのタイプを選択します。

    -   **バケット URL** : Parquet ファイルが配置されているバケット URL を選択します。

    -   **データ形式**: <strong>Parquet</strong>を選択します。

    -   **資格情報の設定**(このフィールドは AWS S3 でのみ表示されます): <strong>Role-ARN</strong>の Role ARN 値を入力します。

    -   **ターゲット クラスタ**: <strong>[ユーザー名]</strong>および [<strong>パスワード</strong>] フィールドに入力します。

    -   **DB/Tables Filter** : インポートするテーブルをフィルタリングする場合は、このフィールドに`,`で区切られた 1 つ以上のテーブル フィルターを指定できます。

        例えば：

        -   `db01.*` : `db01`データベース内のすべてのテーブルがインポートされます。
        -   `db01.table01*,db01.table02*` : `db01`データベースの`table01`と`table02`で始まるすべてのテーブルがインポートされます。
        -   `!db02.*` : `db02`データベースのテーブルを除き、他のすべてのテーブルがインポートされます。 `!`は、インポートする必要のないテーブルを除外するために使用されます。
        -   `*.*` : すべてのテーブルがインポートされます。

        詳細については、 [テーブル フィルター snytax](/table-filter.md#syntax)を参照してください。

    -   **カスタム パターン**: ファイル名が特定のパターンに一致する Parquet ファイルを単一のターゲット テーブルにインポートする場合は、<strong>カスタム パターン</strong>機能を有効にします。

        > **ノート：**
        >
        > この機能を有効にすると、1 つのインポート タスクで一度に 1 つのテーブルにのみデータをインポートできます。この機能を使用してデータを別のテーブルにインポートする場合は、インポートするたびに別のターゲット テーブルを指定して、複数回インポートする必要があります。

        **カスタム パターン**が有効になっている場合、次のフィールドで、Parquet ファイルと単一のターゲット テーブルとの間のカスタム マッピング ルールを指定する必要があります。

        -   **オブジェクト名パターン**: インポートする Parquet ファイルの名前と一致するパターンを入力します。 Parquet ファイルが 1 つしかない場合は、ここにファイル名を直接入力できます。

            例えば：

            -   `my-data?.parquet` : `my-data`と 1 文字 ( `my-data1.parquet`と`my-data2.parquet`など) で始まるすべての Parquet ファイルが同じターゲット テーブルにインポートされます。
            -   `my-data*.parquet` : `my-data`で始まるすべての Parquet ファイルが同じターゲット テーブルにインポートされます。

        -   **ターゲット テーブル名**: TiDB Cloudのターゲット テーブルの名前を入力します。これは`${db_name}.${table_name}`形式である必要があります。たとえば、 `mydb.mytable`です。このフィールドは特定のテーブル名を 1 つしか受け付けないため、ワイルドカードはサポートされていないことに注意してください。

4.  [**インポート]**をクリックします。

    データベース リソースの消費に関する警告メッセージが表示されます。

5.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケット URL のデータにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポート タスクが自動的に開始されます。 `AccessDenied`エラーが発生した場合は、 [S3 からのデータ インポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。

6.  インポートの進行状況が成功を示したら、 **Total Files:**の後の数字を確認します。

    数値がゼロの場合は、[**オブジェクト名パターン]**フィールドに入力した値と一致するデータ ファイルがないことを意味します。この場合、[<strong>オブジェクト名のパターン]</strong>フィールドに入力ミスがないかどうかを確認し、再試行してください。

インポート タスクの実行時に、サポートされていない変換または無効な変換が検出された場合、 TiDB Cloudはインポート ジョブを自動的に終了し、インポート エラーを報告します。

インポート エラーが発生した場合は、次の手順を実行します。

1.  部分的にインポートされたテーブルを削除します。

2.  テーブル スキーマ ファイルを確認してください。エラーがある場合は、テーブル スキーマ ファイルを修正します。

3.  Parquet ファイルのデータ型を確認します。

    サポートされていないデータ型 ( `NEST STRUCT` 、 `ARRAY` 、または`MAP`など) が Parquet ファイルに含まれている場合は、 [サポートされているデータ型](#supported-data-types) ( `STRING`など) を使用して Parquet ファイルを再生成する必要があります。

4.  インポート タスクを再試行します。

## サポートされているデータ型 {#supported-data-types}

次の表に、 TiDB Cloudにインポートできる、サポートされている Parquet データ型を示します。

| 寄木細工プリミティブ型             | 寄木細工の論理型         | TiDB または MySQL の型                                                                                                                                                   |
| ----------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ダブル                     | ダブル              | ダブル<br/>浮く                                                                                                                                                          |
| FIXED_LEN_BYTE_ARRAY(9) | 10 進数 (20,0)     | BIGINT 未署名                                                                                                                                                          |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s)     | 小数<br/>数値                                                                                                                                                           |
| INT32                   | DECIMAL(p,s)     | 小数<br/>数値                                                                                                                                                           |
| INT32                   | なし               | INT<br/>ミディアムミント<br/>年                                                                                                                                              |
| INT64                   | DECIMAL(p,s)     | 小数<br/>数値                                                                                                                                                           |
| INT64                   | なし               | BIGINT<br/>符号なし整数<br/>ミディアムミント 未署名                                                                                                                                  |
| INT64                   | TIMESTAMP_MICROS | 日付時刻<br/>タイムスタンプ                                                                                                                                                    |
| バイト配列                   | なし               | バイナリ<br/>少し<br/>BLOB<br/> CHAR<br/> LINESTRING<br/>ロングブロブ<br/>ミディアムブロブ<br/>複数行文字列<br/>小さな塊<br/>VARBINARY                                                            |
| バイト配列                   | ストリング            | 列挙型<br/>日にち<br/>小数<br/>ジオメトリ<br/>ジオメトリコレクション<br/>JSON<br/>ロングテキスト<br/>中文<br/>マルチポイント<br/>マルチポリゴン<br/>数値<br/>点<br/>ポリゴン<br/>設定<br/>文章<br/>時間<br/>小さなテキスト<br/>VARCHAR |
| SMALLINT                | なし               | INT32                                                                                                                                                               |
| SMALLINT 未署名            | なし               | INT32                                                                                                                                                               |
| TINYINT                 | なし               | INT32                                                                                                                                                               |
| TINYINT UNSIGNED        | なし               | INT32                                                                                                                                                               |
