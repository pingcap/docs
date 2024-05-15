---
title: Integrate Data with Apache Kafka and Apache Flink
summary: Learn how to replicate TiDB data to Apache Kafka and Apache Flink using TiCDC.
---

# Apache Kafka と Apache Flink でデータを統合する {#integrate-data-with-apache-kafka-and-apache-flink}

このドキュメントでは、 [ティCDC](/ticdc/ticdc-overview.md)使用して TiDB データを Apache Kafka および Apache Flink に複製する方法について説明します。このドキュメントの構成は次のとおりです。

1.  TiCDC が組み込まれた TiDB クラスターをすばやくデプロイし、Kafka クラスターと Flink クラスターを作成します。
2.  TiDB から Kafka にデータを複製する変更フィードを作成します。
3.  go-tpc を使用して TiDB にデータを書き込みます。
4.  Kafka コンソール コンシューマー上のデータを観察し、データが指定された Kafka トピックに複製されていることを確認します。
5.  (オプション) Kafka データを消費するように Flink クラスターを構成します。

上記の手順はラボ環境で実行されます。これらの手順を参照して、本番環境にクラスターをデプロイすることもできます。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiCDC が含まれた TiDB クラスターをデプロイ。

    ラボまたはテスト環境では、 TiUP Playground を使用して、TiCDC が組み込まれた TiDB クラスターを迅速にデプロイできます。

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

    TiUPがまだインストールされていない場合は、 [TiUPをインストールする](/tiup/tiup-overview.md#install-tiup)を参照してください。本番環境では、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)の手順に従って TiCDC をデプロイできます。

2.  Kafka クラスターを作成します。

    -   ラボ環境: Kafka クラスターを起動するには、 [Apache Kafka クイックスタート](https://kafka.apache.org/quickstart)を参照してください。
    -   実稼働環境: Kafka本番クラスターをデプロイするには、 [Kafka を本番環境で実行する](https://docs.confluent.io/platform/current/kafka/deployment.html)を参照してください。

3.  (オプション) Flink クラスターを作成します。

    -   ラボ環境: Flink クラスターを起動するには、 [Apache Flink の最初のステップ](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/try-flink/local_installation/)を参照してください。
    -   実稼働環境: Flink本番クラスターをデプロイするには、 [Apache Kafka のデプロイメント](https://nightlies.apache.org/flink/flink-docs-release-1.15/docs/deployment/overview/)を参照してください。

## ステップ2. Kafka チェンジフィードを作成する {#step-2-create-a-kafka-changefeed}

1.  changefeed 構成ファイルを作成します。

    Flink の要件に従い、各テーブルの増分データは独立したトピックに送信され、プライマリキーの値に基づいて各イベントごとにパーティションがディスパッチされる必要があります。そのため、次の内容の changefeed 構成ファイル`changefeed.conf`を作成する必要があります。

        [sink]
        dispatchers = [
        {matcher = ['*.*'], topic = "tidb_{schema}_{table}", partition="index-value"},
        ]

    設定ファイルの`dispatchers`の詳細な説明については[Kafka シンクのトピックおよびパーティションディスパッチャーのルールをカスタマイズする](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)を参照してください。

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

    -   コマンドを実行した後に結果が返されない場合は、コマンドを実行するサーバーとシンク URI で指定された Kafka マシン間のネットワーク接続を確認してください。

    本番環境では、Kafka クラスターには複数のブローカー ノードがあります。したがって、シンク UIR に複数のブローカーのアドレスを追加できます。これにより、Kafka クラスターへの安定したアクセスが保証されます。Kafka クラスターがダウンしている場合でも、changefeed は引き続き機能します。Kafka クラスターに 3 つのブローカー ノードがあり、IP アドレスがそれぞれ 127.0.0.1:9092、127.0.0.2:9092、127.0.0.3:9092 であるとします。次のシンク URI を使用して changefeed を作成できます。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server="http://127.0.0.1:8300" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576" --config="changefeed.conf"
    ```

3.  changefeed を作成したら、次のコマンドを実行して changefeed のステータスを確認します。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed list --server="http://127.0.0.1:8300"
    ```

    チェンジフィードを管理するには、 [TiCDC 変更フィードを管理する](/ticdc/ticdc-manage-changefeed.md)を参照してください。

## ステップ3. 変更ログを生成するためにデータを書き込む {#step-3-write-data-to-generate-change-logs}

上記の手順が完了すると、TiCDC は TiDB クラスター内の増分データの変更ログを Kafka に送信します。このセクションでは、TiDB にデータを書き込んで変更ログを生成する方法について説明します。

1.  サービスのワークロードをシミュレートします。

    ラボ環境で変更ログを生成するには、go-tpc を使用して TiDB クラスターにデータを書き込むことができます。具体的には、次のコマンドを実行して、 TiUP bench を使用して`tpcc`データベースを作成し、この新しいデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    go-tpcの詳細については[TiDB で TPC-C テストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

2.  Kafka トピック内のデータを消費します。

    チェンジフィードが正常に動作すると、Kafka トピックにデータが書き込まれます。実行`kafka-console-consumer.sh` 。データが Kafka トピックに正常に書き込まれていることを確認できます。

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

この時点で、TiDB データベースの増分データが Kafka に正常に複製されます。次に、Flink を使用して Kafka データを消費できます。または、特定のサービス シナリオ用に Kafka コンシューマー クライアントを自分で開発することもできます。

## (オプション) ステップ4. Kafkaデータを消費するようにFlinkを構成する {#optional-step-4-configure-flink-to-consume-kafka-data}

1.  Flink Kafka コネクタをインストールします。

    Flink エコシステムでは、Kafka データを消費し、Flink にデータを出力するために Flink Kafka コネクタが使用されます。ただし、Flink Kafka コネクタは自動的にインストールされません。これを使用するには、Flink をインストールした後、Flink Kafka コネクタとその依存関係を Flink インストール ディレクトリに追加します。具体的には、次の jar ファイルを Flink インストール ディレクトリの`lib`ディレクトリにダウンロードします。すでに Flink クラスターを実行している場合は、再起動して新しいプラグインをロードします。

    -   [flink-コネクタ-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/1.15.0/flink-connector-kafka-1.15.0.jar)
    -   [flink-sql-コネクタ-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.15.0/flink-sql-connector-kafka-1.15.0.jar)
    -   [kafka-クライアント-3.2.0.jar](https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/3.2.0/kafka-clients-3.2.0.jar)

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
