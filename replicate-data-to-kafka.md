---
title: Integrate Data with Apache Kafka and Apache Flink
summary: TiCDC を使用して TiDB データを Apache Kafka および Apache Flink に複製する方法を学びます。
---

# Apache Kafka と Apache Flink でデータを統合する {#integrate-data-with-apache-kafka-and-apache-flink}

このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)を使用して TiDB データを Apache Kafka および Apache Flink に複製する方法について説明します。このドキュメントの構成は次のとおりです。

1.  TiCDC が組み込まれた TiDB クラスターを迅速にデプロイし、Kafka クラスターと Flink クラスターを作成します。
2.  TiDB から Kafka にデータを複製する変更フィードを作成します。
3.  go-tpc を使用して TiDB にデータを書き込みます。
4.  Kafka コンソール コンシューマー上のデータを観察し、データが指定された Kafka トピックに複製されていることを確認します。
5.  (オプション) Kafka データを消費するように Flink クラスターを構成します。

上記の手順はラボ環境で実行されています。これらの手順を参考に、本番環境にクラスターをデプロイすることもできます。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiCDC が含まれた TiDB クラスターをデプロイ。

    ラボまたはテスト環境では、 TiUP Playground を使用して、TiCDC が組み込まれた TiDB クラスターを迅速にデプロイできます。

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

    TiUPがまだインストールされていない場合は、 [TiUPをインストールする](/tiup/tiup-overview.md#install-tiup)を参照してください。本番環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)手順に従って TiCDC をデプロイできます。

2.  Kafka クラスターを作成します。

    -   ラボ環境: Kafka クラスターを起動するには、 [Apache Kafka クイックスタート](https://kafka.apache.org/quickstart)を参照してください。
    -   実稼働環境: Kafka本番クラスターをデプロイするには、 [Kafka を本番環境で実行する](https://docs.confluent.io/platform/current/kafka/deployment.html)を参照してください。

3.  (オプション) Flink クラスターを作成します。

    -   ラボ環境: Flink クラスターを起動するには、 [Apache Flink の最初のステップ](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/try-flink/local_installation/)を参照してください。
    -   実稼働環境: Flink本番クラスターをデプロイするには、 [Apache Kafka のデプロイメント](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/deployment/overview/)を参照してください。

## ステップ2. Kafka の変更フィードを作成する {#step-2-create-a-kafka-changefeed}

1.  changefeed 構成ファイルを作成します。

    Flinkの要件に従い、各テーブルの増分データは独立したトピックに送信され、イベントごとに主キーの値に基づいてパーティションがディスパッチされる必要があります。そのため、以下の内容のchangefeed設定ファイル`changefeed.conf`を作成する必要があります。

        [sink]
        dispatchers = [
        {matcher = ['*.*'], topic = "tidb_{schema}_{table}", partition="index-value"},
        ]

    設定ファイルの`dispatchers`の詳細な説明については[Kafka シンクのトピックおよびパーティションディスパッチャーのルールをカスタマイズする](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)参照してください。

2.  増分データを Kafka に複製するための変更フィードを作成します。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json" --changefeed-id="kafka-changefeed" --config="changefeed.conf"
    ```

    -   変更フィードが正常に作成されると、変更フィード ID などの変更フィード情報が次のように表示されます。

        ```shell
        Create changefeed successfully!
        ID: kafka-changefeed
        Info: {... changfeed info json struct ...}
        ```

    -   コマンドを実行した後に結果が返されない場合は、コマンドを実行したサーバーとシンク URI で指定された Kafka マシン間のネットワーク接続を確認してください。

    本番環境では、Kafka クラスターには複数のブローカーノードが存在します。そのため、シンク UIR に複数のブローカーのアドレスを追加できます。これにより、Kafka クラスターへの安定したアクセスが確保されます。Kafka クラスターがダウンした場合でも、変更フィードは引き続き機能します。Kafka クラスターに 3 つのブローカーノードがあり、IP アドレスがそれぞれ 127.0.0.1:9092、127.0.0.2:9092、127.0.0.3:9092 であるとします。この場合、次のシンク URI で変更フィードを作成できます。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576" --config="changefeed.conf"
    ```

3.  changefeed を作成した後、次のコマンドを実行して changefeed のステータスを確認します。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed list --server="http://127.0.0.1:8300"
    ```

    チェンジフィードを管理するには、 [TiCDC の変更フィードを管理する](/ticdc/ticdc-manage-changefeed.md)を参照してください。

## ステップ3. 変更ログを生成するためにデータを書き込む {#step-3-write-data-to-generate-change-logs}

上記の手順が完了すると、TiCDCはTiDBクラスター内の増分データの変更ログをKafkaに送信します。このセクションでは、TiDBにデータを書き込んで変更ログを生成する方法について説明します。

1.  サービスのワークロードをシミュレートします。

    ラボ環境で変更ログを生成するには、go-tpc を使用して TiDB クラスターにデータを書き込むことができます。具体的には、以下のコマンドを実行してTiUP bench を使用し、データベース`tpcc`作成し、この新しいデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    go-tpc の詳細については[TiDBでTPC-Cテストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

2.  Kafka トピック内のデータを消費します。

    チェンジフィードが正常に動作すると、Kafkaトピックにデータが書き込まれます。実行`kafka-console-consumer.sh`では、データがKafkaトピックに正常に書き込まれていることを確認できます。

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

この時点で、TiDBデータベースの増分データがKafkaに正常に複製されました。次に、Flinkを使用してKafkaデータを利用できます。あるいは、特定のサービスシナリオ向けにKafkaコンシューマークライアントを独自に開発することもできます。

## （オプション）ステップ4. Kafkaデータを消費するようにFlinkを構成する {#optional-step-4-configure-flink-to-consume-kafka-data}

1.  Flink Kafka コネクタをインストールします。

    Flinkエコシステムでは、Kafkaデータの取り込みとFlinkへのデータ出力にFlink Kafkaコネクタが使用されます。ただし、Flink Kafkaコネクタは自動的にインストールされません。使用するには、Flinkをインストールした後、Flink Kafkaコネクタとその依存関係をFlinkインストールディレクトリに追加してください。具体的には、以下のjarファイルをFlinkインストールディレクトリの`lib`ディレクトリにダウンロードしてください。すでにFlinkクラスターを実行している場合は、再起動して新しいプラグインをロードしてください。

    -   [flink-connector-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/1.15.0/flink-connector-kafka-1.15.0.jar)
    -   [flink-sql-コネクタ-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.15.0/flink-sql-connector-kafka-1.15.0.jar)
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

    `tpcc_orders`テーブルのデータを照会するには、次のコマンドを実行します。

    ```sql
    SELECT * FROM tpcc_orders;
    ```

    このコマンドを実行すると、次の図に示すように、テーブルに新しいデータがあることがわかります。

    ![SQL query result](/media/integrate/sql-query-result.png)

Kafka とのデータ統合が完了しました。
