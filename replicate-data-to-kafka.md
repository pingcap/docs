---
title: Replicate data from TiDB to Apache Kafka
summary: Learn how to replicate data from TiDB to Apache Kafka
---

# TiDBからApacheKafkaにデータを複製する {#replicate-data-from-tidb-to-apache-kafka}

このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)を使用してTiDBからApache Kafkaにデータを複製する方法について説明します。これには、次の手順が含まれます。

-   TiCDCクラスタとKafkaクラスタをデプロイします。
-   Kafkaをシンクとしてチェンジフィードを作成します。
-   go-tpcを使用してTiDBクラスタにデータを書き込みます。 Kafkaコンソールコンシューマーで、データが指定されたKafkaトピックにレプリケートされていることを確認します。

これらの手順は、ラボ環境で実行されます。これらの手順を参照して、実稼働環境にクラスタをデプロイすることもできます。

## ステップ1.環境をセットアップします {#step-1-set-up-the-environment}

1.  TiCDCクラスタをデプロイします。

    `tiup playground`コマンドを実行すると、TiCDCをすばやく展開できます。

    {{< copyable "" >}}

    ```shell
    tiup playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1

    # View cluster status
    tiup status
    ```

    実稼働環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)の指示に従ってTiCDCをデプロイできます。

2.  Kafkaクラスタをデプロイします。

    -   Kafkaクラスタをすばやくデプロイするには、 [ApacheKakfaクイックスタート](https://kafka.apache.org/quickstart)を参照してください。
    -   Kafkaクラスタを実稼働環境にデプロイするには、 [Kafkaを本番環境で実行する](https://docs.confluent.io/platform/current/kafka/deployment.html)を参照してください。

## ステップ2.チェンジフィードを作成する {#step-2-create-a-changefeed}

tiup ctlを使用して、Kafkaをダウンストリームノードとして変更フィードを作成します。

{{< copyable "" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json" --changefeed-id="kafka-changefeed"
```

コマンドが正常に実行されると、チェンジフィードIDやシンクURIなどのチェンジフィードに関する情報が表示されます。

{{< copyable "" >}}

```shell
Create changefeed successfully!
ID: kafka-changefeed
Info: {"sink-uri":"kafka://127.0.0.1:9092/kafka-topic-name?protocol=canal-json","opts":{},"create-time":"2022-04-06T14:45:10.824475+08:00","start-ts":432335096583028737,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":"","config":{"case-sensitive":true,"enable-old-value":true,"force-replicate":false,"check-gc-safe-point":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null,"protocol":"canal-json","column-selectors":null},"cyclic-replication":{"enable":false,"replica-id":0,"filter-replica-ids":null,"id-buckets":0,"sync-ddl":false},"scheduler":{"type":"table-number","polling-time":-1},"consistent":{"level":"none","max-log-size":64,"flush-interval":1000,"storage":""}},"state":"normal","error":null,"sync-point-enabled":false,"sync-point-interval":600000000000,"creator-version":"v6.1.0-master"}
```

コマンドが情報を返さない場合は、コマンドが実行されたサーバーからターゲットのKafkaクラスタへのネットワーク接続を確認する必要があります。

実稼働環境では、Kafkaクラスタには複数のブローカーノードがあります。したがって、複数のブローカーのアドレスをシンクUIRに追加できます。これにより、Kafkaクラスタへの安定したアクセスが向上します。 Kafkaクラスタに障害が発生しても、チェンジフィードは引き続き機能します。 Kafkaクラスタに3つのブローカーノードがあり、IPアドレスがそれぞれ127.0.0.1:9092、127.0.0.2:9092、および127.0.0.3:9092であるとします。次のシンクURIを使用してチェンジフィードを作成できます。

{{< copyable "" >}}

```shell
tiup ctl cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092,127.0.0.2:9092,127.0.0.3:9092/kafka-topic-name?protocol=canal-json&partition-num=3&replication-factor=1&max-message-bytes=1048576"
```

上記のコマンドを実行した後、次のコマンドを実行して、チェンジフィードのステータスを確認します。

{{< copyable "" >}}

```shell
tiup ctl cdc changefeed list --pd="http://127.0.0.1:2379"
```

[レプリケーションタスクの管理（ `changefeed` ）](/ticdc/manage-ticdc.md#manage-replication-tasks-changefeed)で指示されているように、チェンジフィードのステータスを管理できます。

## ステップ3.TiDBクラスタでデータ変更を生成する {#step-3-generate-data-changes-in-the-tidb-cluster}

チェンジフィードが作成された後、 `DELETE`クラスタで`INSERT` 、または`UPDATE`操作などのイベント変更が発生すると、データ変更がTiCDCで生成されます。次に、TiCDCはデータ変更をチェンジフィードで指定されたシンクに複製します。このドキュメントでは、シンクはKafkaであり、データ変更は指定されたKafkaトピックに書き込まれます。

1.  サービスのワークロードをシミュレートします。

    ラボ環境では、 `go-tpc`を使用して、チェンジフィードのソースとして使用されるTiDBクラスタにデータを書き込むことができます。具体的には、次のコマンドを実行して、アップストリームTiDBクラスタにデータベース`tpcc`を作成します。次に、 `TiUP bench`を使用してこの新しいデータベースにデータを書き込みます。

    {{< copyable "" >}}

    ```shell
    create database tpcc;
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    `go-tpc`の詳細については、 [TiDBでTPC-Cテストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

2.  Kafkaからのデータ変更を消費します。

    チェンジフィードが正常に機能すると、Kafkaトピックにデータが書き込まれます。 `kafka-console-consumer.sh`を実行して、書き込まれたデータを表示できます。

    {{< copyable "" >}}

    ```shell
    ./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --from-beginning --topic `${topic-name}`
    ```

    実稼働環境では、Kafkaトピックのデータを使用するためにKafkaコンシューマーを開発する必要があります。
