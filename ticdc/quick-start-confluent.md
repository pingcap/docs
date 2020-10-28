---
title: Quickstart on integrating with Confluent Platform
summary: Learn how to stream TiDB  data to Confluent Platform via TiCDC.
aliases: ['/docs/dev/ticdc/quick-start-confluent/','/docs/dev/ticdc/quick-start-confluent/']
---

# Quickstart on integrating with Confluent Platform

This document describes how to stream TiDB data to Confluent Platform via TiCDC.

## Background

Confluent Platform is a stream data platform with Kafka at its core. With the numerous official and third-party sink connectors, Confluent Platform provides a way to easily connect stream sources to data sinks such as Elasticsearch, Cassandra and other relational databases. To support integration with Confluent Platform, TiCDC is capable of streaming data changes to Kafka in a format that Confluent Platform recognizes using the Avro protocol.

## Install and configure Confluent Platform components

### Step 1

Install Zookeeper, Kafka and Schema Registry and make sure they are healthy. We recommend that you follow [the official guide](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart) to deploy a local testing environment.

For this tutorial, we will use the [JDBC sink connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html#load-the-jdbc-sink-connector) to replicate TiDB data to a downstream relational database. We will use **SQLite** here as an example because of its simplicity.

Make sure that JDBC sink connector is installed by running

```shell
confluent local services connect connector list
```

The result should contain `jdbc-sink`.

### Step 2

Save the following configuration into `jdbc-sink-connector.json`

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

Then create an instance of the connector by running (assuming Kafka is listening on 127.0.0.1:8083)

```shell
  curl -X POST -H "Content-Type: application/json" -d jdbc-sink-connector.json http://127.0.0.1:8083/connectors

```

## Deploy and configure TiCDC

### Step 1 (Skip if TiCDC is already deployed)

You can deploy TiCDC in one of the following ways:

- [Deploy and install TiCDC using TiUP](/ticdc/manage-ticdc.md#deploy-and-install-ticdc-using-tiup)
- [Use Binary](/ticdc/manage-ticdc.md#use-binary)

Make sure that your TiDB and TiCDC clusters are healthy before proceeding.

### Step 2

Create a changefeed by `cdc cli`. Note that we assume PD, Kafka and Schema Registry are running on their respective default port. If yours are not, please adjust accordingly.

```shell 
./cdc cli changefeed create --pd="http://127.0.0.1:2379" --sink-uri="kafka://127.0.0.1:9092/testdb_test?protocol=avro" --opts "registry=http://127.0.0.1:8081"
```

## Test data replication

### Step 1

Create database `testdb` in your TiDB cluster.

```sql
CREATE DATABASE IF NOT EXISTS testdb;
```

Create table `test` in `testdb`.

```sql
USE testdb;
CREATE TABLE test (
    id INT PRIMARY KEY,
    v TEXT
);
```

Note that `topics` in `jdbc-sink-connector.json` should be changed accordingly if you need to change the database name, or the table name.

### Step 2

Insert data into TiDB.

```sql
INSERT INTO test (id, v) values (1, 'a');
INSERT INTO test (id, v) values (2, 'b');
INSERT INTO test (id, v) values (3, 'c');
INSERT INTO test (id, v) values (4, 'd');
```

### Step 3

Waiting for a minute so that the data can be replicated. Then check the downstream for data.

```shell
sqlite3 test.db
sqlite> SELECT * from test;
```
