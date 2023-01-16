---
title: Quick Start Guide on Integrating TiDB with Confluent Platform
summary: Learn how to stream TiDB data to the Confluent Platform using TiCDC.
---

# TiDB と Confluent Platform の統合に関するクイック スタート ガイド {#quick-start-guide-on-integrating-tidb-with-confluent-platform}

このドキュメントでは、 [TiCDC](/ticdc/ticdc-overview.md)を使用して TiDB を Confluent Platform に統合する方法を紹介します。

> **警告：**
>
> これはまだ実験的機能です。本番環境では使用し**ない**でください。

[コンフルエントなプラットフォーム](https://docs.confluent.io/current/platform.html)は、Apache Kafka をコアとするデータ ストリーミング プラットフォームです。多くの公式およびサードパーティのシンク コネクタを備えた Confluent Platform では、ストリーム ソースをリレーショナル データベースまたは非リレーショナル データベースに簡単に接続できます。

TiDB を Confluent Platform と統合するには、TiCDCコンポーネントを Avro プロトコルと共に使用できます。 TiCDC は、Confluent Platform が認識する形式でデータの変更を Kafka にストリーミングできます。詳細な統合ガイドについては、次のセクションを参照してください。

## 前提条件 {#prerequisites}

> **ノート：**
>
> このチュートリアルでは、 [JDBC シンク コネクタ](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector)を使用して TiDB データを下流のリレーショナル データベースに複製します。簡単にするために、ここでは**SQLite**を例として使用します。

-   Zookeeper、Kafka、およびスキーマ レジストリが正しくインストールされていることを確認します。 [Confluent プラットフォーム クイック スタート ガイド](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart)に従ってローカル テスト環境を展開することをお勧めします。

-   次のコマンドを実行して、JDBC シンク コネクタがインストールされていることを確認します。結果には`jdbc-sink`が含まれている必要があります。

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
        "connection.url": "jdbc:sqlite:/tmp/test.db", 
        "connection.ds.pool.size": 5,
        "table.name.format": "test",
        "auto.create": true,
        "auto.evolve": true
      }
    }
    ```

2.  次のコマンドを実行して、JDBC シンク コネクタのインスタンスを作成します (Kafka が`127.0.0.1:8083`でリッスンしていると仮定します)。

    {{< copyable "" >}}

    ```shell
    curl -X POST -H "Content-Type: application/json" -d @jdbc-sink-connector.json http://127.0.0.1:8083/connectors
    ```

3.  次のいずれかの方法で TiCDC をデプロイします。 TiCDC がすでにデプロイされている場合は、この手順をスキップできます。

    -   [TiUP を使用してTiUPを含む新しい TiDB クラスターをデプロイする](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup)
    -   [TiUP を使用して既存の TiDB クラスターにTiUPを追加する](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-tiup)
    -   [バイナリを使用して TiCDC を既存の TiDB クラスターに追加する (非推奨)](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-binary-not-recommended)

    続行する前に、TiDB および TiCDC クラスターが正常であることを確認してください。

4.  `cdc cli`コマンドを実行して`changefeed`を作成します。

    {{< copyable "" >}}

    ```shell
    ./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
    ```

    > **ノート：**
    >
    > PD、Kafka、およびスキーマ レジストリがそれぞれのデフォルト ポートで実行されていることを確認します。

## データ複製のテスト {#test-data-replication}

TiDB が Confluent Platform と統合されたら、以下の手順例に従ってデータ複製をテストできます。

1.  TiDB クラスターに`testdb`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE IF NOT EXISTS testdb;
    ```

    `testdb`で`test`テーブルを作成します。

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

2.  データを TiDB に挿入します。

    {{< copyable "" >}}

    ```sql
    INSERT INTO test (id, v) values (1, 'a');
    INSERT INTO test (id, v) values (2, 'b');
    INSERT INTO test (id, v) values (3, 'c');
    INSERT INTO test (id, v) values (4, 'd');
    ```

3.  データがダウンストリームにレプリケートされるまでしばらく待ちます。次に、ダウンストリームのデータを確認します。

    {{< copyable "" >}}

    ```shell
    sqlite3 test.db
    sqlite> SELECT * from test;
    ```
