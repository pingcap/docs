---
title: Quick Start Guide on Integrating TiDB with Confluent Platform
summary: Learn how to stream TiDB data to the Confluent Platform using TiCDC.
---

# TiDBとConfluentプラットフォームの統合に関するクイックスタートガイド {#quick-start-guide-on-integrating-tidb-with-confluent-platform}

このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)を使用してTiDBをConfluentプラットフォームに統合する方法を紹介します。

> **警告：**
>
> これはまだ実験的機能です。実稼働環境では使用し**ない**でください。

[コンフルエントなプラットフォーム](https://docs.confluent.io/current/platform.html)は、ApacheKafkaをコアとするデータストリーミングプラットフォームです。多くの公式およびサードパーティのシンクコネクタを備えたConfluentPlatformを使用すると、ストリームソースをリレーショナルデータベースまたは非リレーショナルデータベースに簡単に接続できます。

TiDBをConfluentPlatformと統合するには、TiCDCコンポーネントをAvroプロトコルで使用できます。 TiCDCは、ConfluentPlatformが認識できる形式でデータの変更をKafkaにストリーミングできます。詳細な統合ガイドについては、次のセクションを参照してください。

## 前提条件 {#prerequisites}

> **ノート：**
>
> このチュートリアルでは、 [JDBCシンクコネクタ](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector)を使用してTiDBデータをダウンストリームのリレーショナルデータベースに複製します。簡単にするために、ここでは例として**SQLite**を使用します。

-   Zookeeper、Kafka、およびSchemaRegistryが正しくインストールされていることを確認してください。 [Confluentプラットフォームクイックスタートガイド](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart)に従って、ローカルテスト環境を展開することをお勧めします。

-   次のコマンドを実行して、JDBCシンクコネクタがインストールされていることを確認します。結果には`jdbc-sink`が含まれている必要があります。

    {{< copyable "" >}}

    ```shell
    confluent local services connect connector list
    ```

## 統合手順 {#integration-procedures}

1.  次の構成を`jdbc-sink-connector.json`に保存します。

    {{< copyable "" >}}

    ```json
    {
      "name": "jdbc-sink-connector",
      "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics": "testdb_test",
        "connection.url": "sqlite:test.db",
        "connection.ds.pool.size": 5,
        "table.name.format": "test",
        "auto.create": true,
        "auto.evolve": true
      }
    }
    ```

2.  次のコマンドを実行して、JDBCシンクコネクタのインスタンスを作成します（Kafkaが`127.0.0.1:8083`をリッスンしていると仮定します）。

    {{< copyable "" >}}

    ```shell
    curl -X POST -H "Content-Type: application/json" -d @jdbc-sink-connector.json http://127.0.0.1:8083/connectors
    ```

3.  次のいずれかの方法でTiCDCをデプロイします。 TiCDCがすでに展開されている場合は、この手順をスキップできます。

    -   [TiUPを使用してTiCDCを含む新しいTiDBクラスタをデプロイします](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup)
    -   [TiUPを使用して既存のTiDBクラスタにTiCDCを追加します](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-tiup)
    -   [バイナリを使用して既存のTiDBクラスタにTiCDCを追加します（非推奨）](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-binary-not-recommended)

    続行する前に、TiDBおよびTiCDCクラスターが正常であることを確認してください。

4.  `cdc cli`コマンドを実行して`changefeed`を作成します。

    {{< copyable "" >}}

    ```shell
    ./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
    ```

    > **ノート：**
    >
    > PD、Kafka、およびSchemaRegistryがそれぞれのデフォルトポートで実行されていることを確認してください。

## データ複製のテスト {#test-data-replication}

TiDBがConfluentPlatformと統合された後、以下の手順例に従ってデータ複製をテストできます。

1.  TiDBクラスタに`testdb`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE IF NOT EXISTS testdb;
    ```

    `testdb`に`test`のテーブルを作成します。

    {{< copyable "" >}}

    ```sql
    USE testdb;
    CREATE TABLE test (
        id INT PRIMARY KEY,
        v TEXT
    );
    ```

    > **ノート：**
    >
    > データベース名またはテーブル名を変更する必要がある場合は、それに応じて`jdbc-sink-connector.json`の`topics`を変更します。

2.  TiDBにデータを挿入します。

    {{< copyable "" >}}

    ```sql
    INSERT INTO test (id, v) values (1, 'a');
    INSERT INTO test (id, v) values (2, 'b');
    INSERT INTO test (id, v) values (3, 'c');
    INSERT INTO test (id, v) values (4, 'd');
    ```

3.  データがダウンストリームに複製されるまでしばらく待ちます。次に、ダウンストリームでデータを確認します。

    {{< copyable "" >}}

    ```shell
    sqlite3 test.db
    sqlite> SELECT * from test;
    ```
