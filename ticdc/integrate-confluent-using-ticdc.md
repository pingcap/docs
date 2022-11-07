---
title: Quick Start Guide on Integrating TiDB with Confluent Platform
summary: Learn how to stream TiDB data to the Confluent Platform using TiCDC.
---

# Quick Start Guide on Integrating TiDB with Confluent Platform

This document introduces how to integrate TiDB to Confluent Platform using [TiCDC](/ticdc/ticdc-overview.md).

> **Warning:**
>
> This is still an experimental feature. Do **NOT** use it in a production environment.

[Confluent Platform](https://docs.confluent.io/current/platform.html) is a data streaming platform with Apache Kafka at its core. With many official and third-party sink connectors, Confluent Platform enables you to easily connect stream sources to relational or non-relational databases.

To integrate TiDB with Confluent Platform, you can use the TiCDC component with the Avro protocol. TiCDC can stream data changes to Kafka in the format that Confluent Platform recognizes. For the detailed integration guide, see the following sections:

## Prerequisites

> **Note:**
>
> In this tutorial, the [JDBC sink connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector) is used to replicate TiDB data to a downstream relational database. To make it simple, **SQLite** is used here as an example.

+ Make sure that Zookeeper, Kafka, and Schema Registry are properly installed. It is recommended that you follow the [Confluent Platform Quick Start Guide](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart) to deploy a local test environment.

+ Make sure that JDBC sink connector is installed by running the following command. The result should contain `jdbc-sink`.

    {{< copyable "shell-regular" >}}

    ```shell
<<<<<<< HEAD
    confluent local services connect connector list
    ```

## Integration procedures

1. Save the following configuration into `jdbc-sink-connector.json`:

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
=======
    tiup ctl:<cluster-version> cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://<broker_endpoint>/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=<broker_api_key>&sasl-password=<broker_api_secret>" --schema-registry="https://<schema_registry_api_key>:<schema_registry_api_secret>@<schema_registry_endpoint>" --changefeed-id="confluent-changefeed" --config changefeed.conf
    ```

    You need to replace the values of the following fields with those created or recorded in [Step 2. Create an access key pair](#step-2-create-an-access-key-pair):

    - `<broker_endpoint>`
    - `<broker_api_key>`
    - `<broker_api_secret>`
    - `<schema_registry_api_key>`
    - `<schema_registry_api_secret>`
    - `<schema_registry_endpoint>`

    Note that you should encode `<schema_registry_api_secret>` based on [HTML URL Encoding Reference](https://www.w3schools.com/tags/ref_urlencode.asp) before replacing its value. After you replace all the preceding fields, the configuration file is as follows:

    ```shell
    tiup ctl:<cluster-version> cdc changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://xxx-xxxxx.ap-east-1.aws.confluent.cloud:9092/ticdc-meta?protocol=avro&replication-factor=3&enable-tls=true&auto-create-topic=true&sasl-mechanism=plain&sasl-user=L5WWA4GK4NAT2EQV&sasl-password=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" --schema-registry="https://7NBH2CAFM2LMGTH7:xxxxxxxxxxxxxxxxxx@yyy-yyyyy.us-east-2.aws.confluent.cloud" --changefeed-id="confluent-changefeed" --config changefeed.conf
>>>>>>> 58015a654 (add version to tiup ctl (2) (#11186))
    ```

2. Create an instance of the JDBC sink connector by running the following command (assuming Kafka is listening on `127.0.0.1:8083`):

    {{< copyable "shell-regular" >}}

    ```shell
<<<<<<< HEAD
    curl -X POST -H "Content-Type: application/json" -d @jdbc-sink-connector.json http://127.0.0.1:8083/connectors
=======
    tiup ctl:<cluster-version> cdc changefeed list --pd="http://127.0.0.1:2379"
>>>>>>> 58015a654 (add version to tiup ctl (2) (#11186))
    ```

3. Deploy TiCDC in one of the following ways. If TiCDC is already deployed, you can skip this step.

    - [Deploy a new TiDB cluster that includes TiCDC using TiUP](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup)
    - [Add TiCDC to an existing TiDB cluster using TiUP](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-tiup)
    - [Add TiCDC to an existing TiDB cluster using binary (not recommended)](/ticdc/deploy-ticdc.md#add-ticdc-to-an-existing-tidb-cluster-using-binary-not-recommended)

    Make sure that your TiDB and TiCDC clusters are healthy before proceeding.

4. Create a `changefeed` by running the `cdc cli` command:

    {{< copyable "shell-regular" >}}

    ```shell
    ./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
    ```

    > **Note:**
    >
    > Make sure that PD, Kafka, and Schema Registry are running on their respective default ports.

## Test data replication

After TiDB is integrated with Confluent Platform, you can follow the example procedures below to test the data replication.

1. Create the `testdb` database in your TiDB cluster:

    {{< copyable "sql" >}}

    ```sql
    CREATE DATABASE IF NOT EXISTS testdb;
    ```

    Create the `test` table in `testdb`:

    {{< copyable "sql" >}}

    ```sql
    USE testdb;
    CREATE TABLE test (
        id INT PRIMARY KEY,
        v TEXT
    );
    ```

    > **Note:**
    >
    > If you need to change the database name or the table name, change `topics` in `jdbc-sink-connector.json` accordingly.

2. Insert data into TiDB:

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO test (id, v) values (1, 'a');
    INSERT INTO test (id, v) values (2, 'b');
    INSERT INTO test (id, v) values (3, 'c');
    INSERT INTO test (id, v) values (4, 'd');
    ```

3. Wait a moment for data to be replicated to the downstream. Then check the downstream for data:

    {{< copyable "shell-regular" >}}

    ```shell
    sqlite3 test.db
    sqlite> SELECT * from test;
    ```
