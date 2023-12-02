---
title: Integrate Data with Apache Kafka and Apache Flink
summary: Learn how to replicate TiDB data to Apache Kafka and Apache Flink using TiCDC.
---

# Apache Kafka および Apache Flink とデータを統合する {#integrate-data-with-apache-kafka-and-apache-flink}

このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)を使用して TiDB データを Apache Kafka および Apache Flink にレプリケートする方法について説明します。この文書の構成は次のとおりです。

1.  TiCDC を含む TiDB クラスターを迅速にデプロイし、Kafka クラスターと Flink クラスターを作成します。
2.  データを TiDB から Kafka にレプリケートする変更フィードを作成します。
3.  go-tpc を使用して TiDB にデータを書き込みます。
4.  Kafka コンソール コンシューマでデータを観察し、データが指定された Kafka トピックにレプリケートされていることを確認します。
5.  (オプション) Kafka データを消費するように Flink クラスターを構成します。

前述の手順はラボ環境で実行されます。これらの手順を参照して、本番環境にクラスターをデプロイすることもできます。

## ステップ 1. 環境をセットアップする {#step-1-set-up-the-environment}

1.  TiCDC を含む TiDB クラスターをデプロイ。

    ラボまたはテスト環境では、 TiUP Playground を使用して、TiCDC が組み込まれた TiDB クラスターを迅速にデプロイできます。

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

    TiUPがまだインストールされていない場合は、 [TiUPをインストールする](/tiup/tiup-overview.md#install-tiup)を参照してください。本番環境では、 [TiCDCのデプロイ](/ticdc/deploy-ticdc.md)手順に従って TiCDC をデプロイできます。

2.  Kafka クラスターを作成します。

    -   ラボ環境: Kafka クラスターを開始するには、 [Apache Kakfa クイックスタート](https://kafka.apache.org/quickstart)を参照してください。
    -   実稼働環境: Kafka本番クラスターをデプロイするには、 [本番環境での Kafka の実行](https://docs.confluent.io/platform/current/kafka/deployment.html)を参照してください。

3.  (オプション) Flink クラスターを作成します。

    -   ラボ環境: Flink クラスターを開始するには、 [Apache Flink 最初のステップ](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/try-flink/local_installation/)を参照してください。
    -   実稼働環境: Flink本番クラスターをデプロイするには、 [Apache Kafkaのデプロイメント](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/deployment/overview/)を参照してください。

## ステップ 2. Kafka チェンジフィードを作成する {#step-2-create-a-kafka-changefeed}

1.  チェンジフィード構成ファイルを作成します。

    Flink の要求に応じて、各テーブルの増分データを独立したトピックに送信する必要があり、主キー値に基づいてイベントごとにパーティションをディスパッチする必要があります。したがって、次の内容で変更フィード構成ファイル`changefeed.conf`を作成する必要があります。

        [sink]
        dispatchers = [
        {matcher = ['*.*'], topic = "tidb_{schema}_{table}", partition="index-value"},
        ]

    設定ファイルの`dispatchers`の詳細については、 [Kafka シンクのトピックおよびパーティション ディスパッチャーのルールをカスタマイズする](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)を参照してください。

2.  増分データを Kafka にレプリケートするための変更フィードを作成します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json" --changefeed-id="kafka-changefeed" --config="changefeed.conf"
    ```

    -   チェンジフィードが正常に作成されると、以下に示すように、チェンジフィード ID などのチェンジフィード情報が表示されます。

        ```shell
        Create changefeed successfully!
        ID: kafka-changefeed
        Info: {... changfeed info json struct ...}
        ```

    -   コマンドの実行後に結果が返されない場合は、コマンドを実行したサーバーとシンク URI で指定された Kafka マシン間のネットワーク接続を確認してください。

    本番環境では、Kafka クラスターに複数のブローカー ノードがあります。したがって、複数のブローカーのアドレスをシンク UIR に追加できます。これにより、Kafka クラスターへの安定したアクセスが保証されます。 Kafka クラスターがダウンしても、チェンジフィードは引き続き機能します。 Kafka クラスターに 3 つのブローカー ノードがあり、IP アドレスがそれぞれ 127.0.0.1:9092、127.0.0.2:9092、および 127.0.0.3:9092 であるとします。次のシンク URI を使用して変更フィードを作成できます。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576" --config="changefeed.conf"
    ```

3.  変更フィードを作成した後、次のコマンドを実行して変更フィードのステータスを確認します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed list --server="http://127.0.0.1:8300"
    ```

    チェンジフィードを管理するには、 [TiCDC 変更フィードの管理](/ticdc/ticdc-manage-changefeed.md)を参照してください。

## ステップ 3. データを書き込んで変更ログを生成する {#step-3-write-data-to-generate-change-logs}

前述の手順が完了すると、TiCDC は TiDB クラスター内の増分データの変更ログを Kafka に送信します。このセクションでは、TiDB にデータを書き込んで変更ログを生成する方法について説明します。

1.  サービスのワークロードをシミュレートします。

    ラボ環境で変更ログを生成するには、go-tpc を使用してデータを TiDB クラスターに書き込むことができます。具体的には、次のコマンドを実行してTiUPベンチを使用して`tpcc`データベースを作成し、この新しいデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    go-tpc の詳細については、 [TiDB で TPC-C テストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

2.  Kafka トピック内のデータを使用します。

    チェンジフィードが正常に動作すると、データが Kafka トピックに書き込まれます。 `kafka-console-consumer.sh`を実行します。データが Kafka トピックに正常に書き込まれていることがわかります。

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

この時点で、TiDB データベースの増分データは Kafka に正常にレプリケートされます。次に、Flink を使用して Kafka データを使用できます。あるいは、特定のサービス シナリオ向けに Kafka コンシューマ クライアントを自分で開発することもできます。

## (オプション) ステップ 4. Kafka データを消費するように Flink を構成する {#optional-step-4-configure-flink-to-consume-kafka-data}

1.  Flink Kafka コネクタをインストールします。

    Flink エコシステムでは、Flink Kafka コネクタを使用して Kafka データを消費し、データを Flink に出力します。ただし、Flink Kafka コネクタは自動的にはインストールされません。これを使用するには、Flink をインストールした後、Flink Kafka コネクタとその依存関係を Flink インストール ディレクトリに追加します。具体的には、以下のjarファイルをFlinkインストールディレクトリの`lib`ディレクトリにダウンロードします。すでに Flink クラスターを実行している場合は、再起動して新しいプラグインをロードします。

    -   [flink-connector-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/1.15.0/flink-connector-kafka-1.15.0.jar)
    -   [flink-sql-connector-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.15.0/flink-sql-connector-kafka-1.15.0.jar)
    -   [kafka-clients-3.2.0.jar](https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/3.2.0/kafka-clients-3.2.0.jar)

2.  テーブルを作成します。

    Flink がインストールされているディレクトリで、次のコマンドを実行して Flink SQL クライアントを起動します。

    ```shell
    [root@flink flink-1.15.0]# ./bin/sql-client.sh
    ```

    次に、次のコマンドを実行して、 `tpcc_orders`という名前のテーブルを作成します。

    ```sql
    CREATE TABLE tpcc_orders (
        o_id INTEGER,
        o_d_id INTEGER,
        o_w_id INTEGER,
        o_c_id INTEGER,
        o_entry_d STRING,
        o_carrier_id INTEGER,
        o_ol_cnt INTEGER,
        o_all_local INTEGER
    ) WITH (
    'connector' = 'kafka',
    'topic' = 'tidb_tpcc_orders',
    'properties.bootstrap.servers' = '127.0.0.1:9092',
    'properties.group.id' = 'testGroup',
    'format' = 'canal-json',
    'scan.startup.mode' = 'earliest-offset',
    'properties.auto.offset.reset' = 'earliest'
    )
    ```

    `topic`と`properties.bootstrap.servers`環境内の実際の値に置き換えます。

3.  テーブルのデータをクエリします。

    次のコマンドを実行して、 `tpcc_orders`テーブルのデータをクエリします。

    ```sql
    SELECT * FROM tpcc_orders;
    ```

    このコマンドを実行すると、次の図に示すように、テーブルに新しいデータがあることがわかります。

    ![SQL query result](/media/integrate/sql-query-result.png)

Kafka とのデータ統合が完了しました。
