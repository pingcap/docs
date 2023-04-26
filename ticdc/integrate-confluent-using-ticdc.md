---
title: Integrate Data with Confluent Cloud and Snowflake
summary: Learn how to stream TiDB data to Confluent Cloud, Snowflake, ksqlDB, and SQL Server.
---

# Confluent Cloud および Snowflake とデータを統合する {#integrate-data-with-confluent-cloud-and-snowflake}

Confluent は、強力なデータ統合機能を提供する Apache Kafka 互換のストリーミング データ プラットフォームです。このプラットフォームでは、ノンストップのリアルタイム ストリーミング データにアクセス、保存、および管理できます。

TiDB v6.1.0 以降、TiCDC は、増分データを Avro 形式で Confluent に複製することをサポートしています。このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)使用して TiDB の増分データを Confluent にレプリケートし、さらに Confluent Cloud を介して Snowflake、ksqlDB、および SQL Server にデータをレプリケートする方法を紹介します。このドキュメントの構成は次のとおりです。

1.  TiCDC を含む TiDB クラスターをすばやくデプロイします。
2.  TiDB から Confluent Cloud にデータをレプリケートする変更フィードを作成します。
3.  Confluent Cloud から Snowflake、ksqlDB、および SQL Server にデータをレプリケートするコネクタを作成します。
4.  go-tpc を使用して TiDB にデータを書き込み、Snowflake、ksqlDB、および SQL Server でデータの変更を観察します。

上記の手順は、ラボ環境で実行されます。これらの手順を参照して、本番環境にクラスターをデプロイすることもできます。

## 増分データを Confluent Cloud に複製する {#replicate-incremental-data-to-confluent-cloud}

### ステップ 1. 環境をセットアップする {#step-1-set-up-the-environment}

1.  TiCDC を含む TiDB クラスターをデプロイ。

    ラボまたはテスト環境では、 TiUP Playground を使用して、TiCDC を含む TiDB クラスターをすばやくデプロイできます。

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

    TiUPがインストールされていない場合は、 [TiUPをインストールする](/tiup/tiup-overview.md#install-tiup)を参照してください。本番環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)指示に従って TiCDC をデプロイできます。

2.  Confluent Cloud を登録し、Confluent クラスタを作成します。

    Basic クラスターを作成し、インターネット経由でアクセスできるようにします。詳細については、 [Confluent Cloud のクイック スタート](https://docs.confluent.io/cloud/current/get-started/index.html)を参照してください。

### ステップ 2. アクセス キー ペアを作成する {#step-2-create-an-access-key-pair}

1.  クラスター API キーを作成します。

    [コンフルエントなクラウド](https://confluent.cloud)にサインインします。 **[データ統合]** &gt; <strong>[API キー]</strong> &gt; [<strong>キーの作成]</strong>を選択します。表示される<strong>[API キーのスコープの選択]</strong>ページで、 <strong>[グローバル アクセス]</strong>を選択します。

    作成後、以下に示すようにキー ペア ファイルが生成されます。

    ```
    === Confluent Cloud API key: xxx-xxxxx ===

    API key:
    L5WWA4GK4NAT2EQV

    API secret:
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    Bootstrap server:
    xxx-xxxxx.ap-east-1.aws.confluent.cloud:9092
    ```

2.  スキーマ レジストリ エンドポイントを記録します。

    Confluent Cloud Console で、 **[スキーマ レジストリ]** &gt; <strong>[API エンドポイント]</strong>を選択します。スキーマ レジストリ エンドポイントを記録します。次に例を示します。

    ```
    https://yyy-yyyyy.us-east-2.aws.confluent.cloud
    ```

3.  スキーマ レジストリ API キーを作成します。

    Confluent Cloud Console で、 **[スキーマ レジストリ]** &gt; <strong>[API 資格情報]</strong>を選択します。 <strong>[編集]</strong> 、 <strong>[キーの作成] の</strong>順にクリックします。

    作成後、以下に示すようにキー ペア ファイルが生成されます。

    ```
    === Confluent Cloud API key: yyy-yyyyy ===
    API key:
    7NBH2CAFM2LMGTH7
    API secret:
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

    この手順は、Confluent CLI を使用して実行することもできます。詳細については、 [Confluent CLI を Confluent Cloud クラスタに接続する](https://docs.confluent.io/confluent-cli/current/connect.html)を参照してください。

### ステップ 3. Kafka チェンジフィードを作成する {#step-3-create-a-kafka-changefeed}

1.  changefeed 構成ファイルを作成します。

    Avro と Confluent Connector の要件に応じて、各テーブルの増分データを独立したトピックに送信する必要があり、主キーの値に基づいて各イベントに対してパーティションをディスパッチする必要があります。したがって、次の内容で changefeed 構成ファイル`changefeed.conf`を作成する必要があります。

    ```
    [sink]
    dispatchers = [
    {matcher = ['*.*'], topic = "tidb_{schema}_{table}", partition="index-value"},
    ]
    ```

    構成ファイルの`dispatchers`の詳細な説明については、 [Kafka Sink のトピックおよびパーティション ディスパッチャーのルールをカスタマイズする](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)を参照してください。

2.  増分データを Confluent Cloud にレプリケートするための変更フィードを作成します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://<broker_endpoint>/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=<broker_api_key>&sasl-password=<broker_api_secret>" --schema-registry="https://<schema_registry_api_key>:<schema_registry_api_secret>@<schema_registry_endpoint>" --changefeed-id="confluent-changefeed" --config changefeed.conf
    ```

    次のフィールドの値を、 [ステップ 2. アクセス キー ペアを作成する](#step-2-create-an-access-key-pair)で作成または記録した値に置き換える必要があります。

    -   `<broker_endpoint>`
    -   `<broker_api_key>`
    -   `<broker_api_secret>`
    -   `<schema_registry_api_key>`
    -   `<schema_registry_api_secret>`
    -   `<schema_registry_endpoint>`

    値を置き換える前に、 [HTML URL エンコーディング リファレンス](https://www.w3schools.com/tags/ref_urlencode.asp)に基づいて`<schema_registry_api_secret>`をエンコードする必要があることに注意してください。前述のすべてのフィールドを置き換えると、構成ファイルは次のようになります。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://xxx-xxxxx.ap-east-1.aws.confluent.cloud:9092/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=L5WWA4GK4NAT2EQV&sasl-password=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" --schema-registry="https://7NBH2CAFM2LMGTH7:xxxxxxxxxxxxxxxxxx@yyy-yyyyy.us-east-2.aws.confluent.cloud" --changefeed-id="confluent-changefeed" --config changefeed.conf
    ```

    -   コマンドを実行して、変更フィードを作成します。

        -   変更フィードが正常に作成されると、次のように、変更フィード ID などの変更フィード情報が表示されます。

            ```shell
            Create changefeed successfully!
            ID: confluent-changefeed
            Info: {... changfeed info json struct ...}
            ```

        -   コマンドを実行しても結果が返されない場合は、コマンドを実行したサーバーと Confluent Cloud 間のネットワーク接続を確認してください。詳細については、 [Confluent Cloud への接続をテストする](https://docs.confluent.io/cloud/current/networking/testing.html)を参照してください。

3.  変更フィードを作成したら、次のコマンドを実行して変更フィードのステータスを確認します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed list --server="http://127.0.0.1:8300"
    ```

    [TiCDC チェンジフィードの管理](/ticdc/ticdc-manage-changefeed.md)を参照して、変更フィードを管理できます。

### ステップ 4. データを書き込んで変更ログを生成する {#step-4-write-data-to-generate-change-logs}

上記の手順が完了すると、TiCDC は TiDB クラスター内の増分データの変更ログを Confluent Cloud に送信します。このセクションでは、TiDB にデータを書き込んで変更ログを生成する方法について説明します。

1.  サービスのワークロードをシミュレートします。

    ラボ環境で変更ログを生成するには、go-tpc を使用してデータを TiDB クラスターに書き込みます。具体的には、次のコマンドを実行して、TiDB クラスターにデータベース`tpcc`を作成します。次に、 TiUPベンチを使用して、この新しいデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    go-tpc の詳細については、 [TiDB で TPC-C テストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

2.  Confluent Cloud でデータを観察します。

    ![Confluent topics](/media/integrate/confluent-topics.png)

    Confluent Cloud Console で、 **[トピック]**をクリックします。ターゲット トピックが作成され、データを受信していることがわかります。この時点で、TiDB データベースの増分データが Confluent Cloud に正常に複製されます。

## データを Snowflake と統合する {#integrate-data-with-snowflake}

Snowflake は、クラウド ネイティブのデータ ウェアハウスです。 Confluent では、Snowflake シンク コネクタを作成することで、TiDB の増分データを Snowflake にレプリケートできます。

### 前提条件 {#prerequisites}

-   Snowflake クラスターを登録して作成しました。 [スノーフレーク入門](https://docs.snowflake.com/en/user-guide-getting-started.html)を参照してください。
-   Snowflake クラスターに接続する前に、その秘密鍵を生成しました。 [キー ペア認証とキー ペア ローテーション](https://docs.snowflake.com/en/user-guide/key-pair-auth.html)を参照してください。

### 統合手順 {#integration-procedure}

1.  Snowflake でデータベースとスキーマを作成します。

    Snowflake コントロール コンソールで、 **[データ]** &gt; <strong>[データベース]</strong>を選択します。 `TPCC`という名前のデータベースと`TiCDC`という名前のスキーマを作成します。

2.  Confluent Cloud Console で、 **[データ統合]** &gt; <strong>[コネクタ]</strong> &gt; <strong>[Snowflake Sink]</strong>を選択します。以下のページが表示されます。

    ![Add snowflake sink connector](/media/integrate/add-snowflake-sink-connector.png)

3.  Snowflake にレプリケートするトピックを選択します。次に、次のページに進みます。

    ![Configuration](/media/integrate/configuration.png)

4.  Snowflakeに接続するための認証情報を指定します。前の手順で作成した値を**データベース名**と<strong>スキーマ名</strong>に入力します。次に、次のページに進みます。

    ![Configuration](/media/integrate/configuration.png)

5.  **[コンフィグレーション]**ページで、 <strong>[入力 Kafka レコードの値の形式]</strong>と<strong>[入力 Kafka レコードのキー形式]</strong>の両方で`AVRO`を選択します。次に<strong>[続行]</strong>をクリックします。コネクタが作成され、ステータスが<strong>Running</strong>になるまで待ちます。これには数分かかる場合があります。

    ![Data preview](/media/integrate/data-preview.png)

6.  Snowflake コンソールで、 **[データ]** &gt; <strong>[データベース]</strong> &gt; <strong>[TPCC]</strong> &gt; <strong>[TiCDC]</strong>を選択します。 TiDB の増分データが Snowflake にレプリケートされていることがわかります。 Snowflake とのデータ統合が完了しました (前の図を参照)。ただし、Snowflake のテーブル構造は TiDB とは異なり、データは Snowflake に段階的に挿入されます。ほとんどのシナリオでは、Snowflake のデータは TiDB の変更ログを保存するのではなく、TiDB のデータのレプリカであると予想されます。この問題については、次のセクションで説明します。

### Snowflake で TiDB テーブルのデータ レプリカを作成する {#create-data-replicas-of-tidb-tables-in-snowflake}

前のセクションでは、TiDB の増分データの変更ログが Snowflake に複製されました。このセクションでは、これらの変更ログを Snowflake の TASK および STREAM 機能を使用してイベント タイプ`INSERT` 、 `UPDATE` 、および`DELETE`に従って処理し、上流と同じ構造のテーブルに書き込み、データを作成する方法について説明します。 Snowflake の TiDB テーブルのレプリカ。以下は、例として`ITEM`テーブルを取り上げます。

`ITEM`テーブルの構造は次のとおりです。

```
CREATE TABLE `item` (
  `i_id` int(11) NOT NULL,
  `i_im_id` int(11) DEFAULT NULL,
  `i_name` varchar(24) DEFAULT NULL,
  `i_price` decimal(5,2) DEFAULT NULL,
  `i_data` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`i_id`)
);
```

Snowflake には、Confluent Snowflake Sink Connector によって自動的に作成される`TIDB_TEST_ITEM`という名前のテーブルがあります。テーブル構造は次のとおりです。

```
create or replace TABLE TIDB_TEST_ITEM (
        RECORD_METADATA VARIANT,
        RECORD_CONTENT VARIANT
);
```

1.  Snowflake で、TiDB と同じ構造のテーブルを作成します。

    ```
    create or replace table TEST_ITEM (
        i_id INTEGER primary key,
        i_im_id INTEGER,
        i_name VARCHAR,
        i_price DECIMAL(36,2),
        i_data VARCHAR
    );
    ```

2.  `TIDB_TEST_ITEM`のストリームを作成し、次のように`append_only` ～ `true`を設定します。

    ```
    create or replace stream TEST_ITEM_STREAM on table TIDB_TEST_ITEM append_only=true;
    ```

    このように、作成されたストリームはリアルタイムで`INSERT`イベントのみをキャプチャします。具体的には、TiDB で`ITEM`の新しい変更ログが生成されると、その変更ログが`TIDB_TEST_ITEM`に挿入され、ストリームによってキャプチャされます。

3.  ストリーム内のデータを処理します。イベントの種類に応じて、 `TEST_ITEM`テーブルのストリーム データを挿入、更新、または削除します。

    ```
    --Merge data into the TEST_ITEM table
    merge into TEST_ITEM n
      using
          -- Query TEST_ITEM_STREAM
          (SELECT RECORD_METADATA:key as k, RECORD_CONTENT:val as v from TEST_ITEM_STREAM) stm
          -- Match the stream with table on the condition that i_id is equal
          on k:i_id = n.i_id
      -- If the TEST_ITEM table contains a record that matches i_id and v is empty, delete this record
      when matched and IS_NULL_VALUE(v) = true then
          delete

      -- If the TEST_ITEM table contains a record that matches i_id and v is not empty, update this record
      when matched and IS_NULL_VALUE(v) = false then
          update set n.i_data = v:i_data, n.i_im_id = v:i_im_id, n.i_name = v:i_name, n.i_price = v:i_price

      -- If the TEST_ITEM table does not contain a record that matches i_id, insert this record
      when not matched then
          insert
              (i_data, i_id, i_im_id, i_name, i_price)
          values
              (v:i_data, v:i_id, v:i_im_id, v:i_name, v:i_price)
    ;
    ```

    前の例では、Snowflake の`MERGE INTO`ステートメントを使用して、特定の条件でストリームとテーブルを照合し、レコードの削除、更新、挿入などの対応する操作を実行します。この例では、次の 3 つのシナリオに対して 3 つの`WHERE`句が使用されています。

    -   ストリームとテーブルが一致し、ストリーム内のデータが空の場合、テーブル内のレコードを削除します。
    -   ストリームとテーブルが一致し、ストリーム内のデータが空でない場合、テーブル内のレコードを更新します。
    -   ストリームとテーブルが一致しない場合、テーブルにレコードを挿入します。

4.  手順 3 のステートメントを定期的に実行して、データが常に最新であることを確認します。 Snowflakeの`SCHEDULED TASK`の機能を使用することもできます。

    ```
    -- Create a TASK to periodically execute the MERGE INTO statement
    create or replace task STREAM_TO_ITEM
        warehouse = test
        -- Execute the TASK every minute
        schedule = '1 minute'
    when
        -- Skip the TASK when there is no data in TEST_ITEM_STREAM
        system$stream_has_data('TEST_ITEM_STREAM')
    as
    -- Merge data into the TEST_ITEM table. The statement is the same as that in the preceding example
    merge into TEST_ITEM n
      using
          (select RECORD_METADATA:key as k, RECORD_CONTENT:val as v from TEST_ITEM_STREAM) stm
          on k:i_id = n.i_id
      when matched and IS_NULL_VALUE(v) = true then
          delete
      when matched and IS_NULL_VALUE(v) = false then
          update set n.i_data = v:i_data, n.i_im_id = v:i_im_id, n.i_name = v:i_name, n.i_price = v:i_price
      when not matched then
          insert
              (i_data, i_id, i_im_id, i_name, i_price)
          values
              (v:i_data, v:i_id, v:i_im_id, v:i_name, v:i_price)
    ;
    ```

この時点で、特定の ETL 機能を備えたデータ チャネルが確立されました。このデータ チャネルを通じて、TiDB の増分データ変更ログを Snowflake にレプリケートし、TiDB のデータ レプリカを維持し、Snowflake でデータを使用できます。

最後のステップは、 `TIDB_TEST_ITEM`テーブルの不要なデータを定期的にクリーンアップすることです。

```
-- Clean up the TIDB_TEST_ITEM table every two hours
create or replace task TRUNCATE_TIDB_TEST_ITEM
    warehouse = test
    schedule = '120 minute'
when
    system$stream_has_data('TIDB_TEST_ITEM')
as
    TRUNCATE table TIDB_TEST_ITEM;
```

## データを ksqlDB と統合する {#integrate-data-with-ksqldb}

ksqlDB は、ストリーム処理アプリケーション専用のデータベースです。 Confluent Cloud で ksqlDB クラスターを作成し、TiCDC によって複製された増分データにアクセスできます。

1.  Confluent Cloud Console で**ksqlDB を**選択し、指示に従って ksqlDB クラスターを作成します。

    ksqlDB クラスターのステータスが**Running**になるまで待ちます。このプロセスには数分かかります。

2.  ksqlDB エディターで、次のコマンドを実行して、 `tidb_tpcc_orders`トピックにアクセスするためのストリームを作成します。

    ```sql
    CREATE STREAM orders (o_id INTEGER, o_d_id INTEGER, o_w_id INTEGER, o_c_id INTEGER, o_entry_d STRING, o_carrier_id INTEGER, o_ol_cnt INTEGER, o_all_local INTEGER) WITH (kafka_topic='tidb_tpcc_orders', partitions=3, value_format='AVRO');
    ```

3.  次のコマンドを実行して、注文の STREAM データを確認します。

    ```sql
    SELECT * FROM ORDERS EMIT CHANGES;
    ```

    ![Select from orders](/media/integrate/select-from-orders.png)

    前の図に示すように、増分データが ksqlDB に複製されていることがわかります。 ksqlDB とのデータ統合が行われます。

## データを SQL Server と統合する {#integrate-data-with-sql-server}

Microsoft SQL Server は、Microsoft が開発したリレーショナル データベース管理システム (RDBMS) です。 Confluent では、SQL Server シンク コネクタを作成することで、TiDB の増分データを SQL Server にレプリケートできます。

1.  SQL Server に接続し、 `tpcc`という名前のデータベースを作成します。

    ```shell
    [ec2-user@ip-172-1-1-1 bin]$ sqlcmd -S 10.61.43.14,1433 -U admin
    Password:
    1> create database tpcc
    2> go
    1> select name from master.dbo.sysdatabases
    2> go
    name
    ----------------------------------------------------------------------
    master
    tempdb
    model
    msdb
    rdsadmin
    tpcc
    (6 rows affected)
    ```

2.  Confluent Cloud Console で、 **[データ統合]** &gt; <strong>[コネクタ]</strong> &gt; <strong>[Microsoft SQL Server Sink]</strong>を選択します。以下のページが表示されます。

    ![Topic selection](/media/integrate/topic-selection.png)

3.  SQL Server にレプリケートするトピックを選択します。次に、次のページに進みます。

    ![Authentication](/media/integrate/authentication.png)

4.  接続および認証情報を入力します。次に、次のページに進みます。

5.  **[コンフィグレーション]**ページで、次のフィールドを構成し、 <strong>[続行]</strong>をクリックします。

    | 分野                 | 価値         |
    | :----------------- | :--------- |
    | 入力 Kafka レコード値の形式  | アブロ        |
    | 挿入モード              | アップサート     |
    | テーブルの自動作成          | 真実         |
    | 列の自動追加             | 真実         |
    | PK モード             | record_key |
    | 入力 Kafka レコード キー形式 | アブロ        |
    | null で削除           | 真実         |

6.  構成後、 **[続行]**をクリックします。コネクタのステータスが<strong>Running</strong>になるまで待ちます。これには数分かかる場合があります。

    ![Results](/media/integrate/results.png)

7.  SQL Server に接続し、データを観察します。前の図に示すように、増分データが SQL Server にレプリケートされていることがわかります。 SQL Server とのデータ統合が完了しました。
