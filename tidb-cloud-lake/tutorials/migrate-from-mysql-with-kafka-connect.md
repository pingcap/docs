---
title: Migrate MySQL with Kafka Connect (CDC)
sidebar_label: 'MySQL → Databend: Kafka Connect (CDC)'
---

> **Capabilities**: CDC, Incremental, Full Load

This tutorial shows how to build a real-time data pipeline from MySQL to Databend using Kafka Connect.

## Overview

Kafka Connect is a tool for streaming data between Apache Kafka and other systems reliably and at scale. It simplifies building real-time data pipelines by standardizing data movement in and out of Kafka. For MySQL to Databend migration, Kafka Connect provides a seamless solution that enables:

- Real-time data synchronization from MySQL to Databend
- Automatic schema evolution and table creation
- Support for both new data capture and updates to existing data

The migration pipeline consists of two main components:

- **MySQL JDBC Source Connector**: Reads data from MySQL and publishes it to Kafka topics
- **Databend Sink Connector**: Consumes data from Kafka topics and writes it to Databend

## Prerequisites

- MySQL database with data you want to migrate
- Apache Kafka installed ([Kafka quickstart guide](https://kafka.apache.org/quickstart))
- Databend instance running
- Basic knowledge of SQL and command line

## Step 1: Set Up Kafka Connect

Kafka Connect supports two execution modes: Standalone and Distributed. For this tutorial, we'll use Standalone mode which is simpler for testing.

### Configure Kafka Connect

Create a basic worker configuration file `connect-standalone.properties` in your Kafka `config` directory:

```properties
bootstrap.servers=localhost:9092
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=true
value.converter.schemas.enable=true
offset.storage.file.filename=/tmp/connect.offsets
offset.flush.interval.ms=10000
```

## Step 2: Configure MySQL Source Connector

### Install Required Components

1. Download the [Kafka Connect JDBC](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc) plugin from Confluent Hub and extract it to your Kafka `libs` directory

2. Download the [MySQL JDBC Driver](https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.32/) and copy the JAR file to the same `libs` directory

### Create MySQL Source Configuration

Create a file `mysql-source.properties` in your Kafka `config` directory with the following content:

```properties
name=mysql-source
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
tasks.max=1

# Connection settings
connection.url=jdbc:mysql://localhost:3306/your_database?useSSL=false
connection.user=your_username
connection.password=your_password

# Table selection and topic mapping
table.whitelist=your_database.your_table
topics=mysql_data

# Sync mode configuration
mode=incrementing
incrementing.column.name=id

# Polling frequency
poll.interval.ms=5000
```

Replace the following values with your actual MySQL configuration:
- `your_database`: Your MySQL database name
- `your_username`: MySQL username
- `your_password`: MySQL password
- `your_table`: The table you want to migrate

### Sync Modes

The MySQL Source Connector supports three synchronization modes:

1. **Incrementing Mode**: Best for tables with an auto-incrementing ID column
   ```properties
   mode=incrementing
   incrementing.column.name=id
   ```

2. **Timestamp Mode**: Best for capturing both inserts and updates
   ```properties
   mode=timestamp
   timestamp.column.name=updated_at
   ```

3. **Timestamp+Incrementing Mode**: Most reliable for all changes
   ```properties
   mode=timestamp+incrementing
   incrementing.column.name=id
   timestamp.column.name=updated_at
   ```

## Step 3: Configure Databend Sink Connector

### Install Required Components

1. Download the [Databend Kafka Connector](https://github.com/databendcloud/databend-kafka-connect/releases) and place it in your Kafka `libs` directory

2. Download the [Databend JDBC Driver](https://central.sonatype.com/artifact/com.databend/databend-jdbc/) and copy it to your Kafka `libs` directory

### Create Databend Sink Configuration

Create a file `databend-sink.properties` in your Kafka `config` directory:

```properties
name=databend-sink
connector.class=com.databend.kafka.connect.DatabendSinkConnector

# Connection settings
connection.url=jdbc:databend://localhost:8000
connection.user=databend
connection.password=databend
connection.database=default

# Topic to table mapping
topics=mysql_data
table.name.format=${topic}

# Table management
auto.create=true
auto.evolve=true

# Write behavior
insert.mode=upsert
pk.mode=record_value
pk.fields=id
batch.size=1000
```

Adjust the Databend connection settings as needed for your environment.

## Step 4: Start the Migration Pipeline

Start Kafka Connect with both connector configurations:

```shell
bin/connect-standalone.sh config/connect-standalone.properties \
    config/mysql-source.properties \
    config/databend-sink.properties
```

## Step 5: Verify the Migration

### Check Data Synchronization

1. **Monitor Kafka Connect Logs**

   ```shell
   tail -f /path/to/kafka/logs/connect.log
   ```

2. **Verify Data in Databend**

   Connect to your Databend instance and run:

   ```sql
   SELECT * FROM mysql_data LIMIT 10;
   ```

### Test Schema Evolution

If you add a new column to your MySQL table, the schema change will automatically propagate to Databend:

1. **Add a column in MySQL**

   ```sql
   ALTER TABLE your_table ADD COLUMN new_field VARCHAR(100);
   ```

2. **Verify schema update in Databend**

   ```sql
   DESC mysql_data;
   ```

### Test Update Operations

To test updates, ensure you're using timestamp or timestamp+incrementing mode:

1. **Update your MySQL connector configuration**

   Edit `mysql-source.properties` to use timestamp+incrementing mode if your table has a timestamp column.

2. **Update data in MySQL**

   ```sql
   UPDATE your_table SET some_column='new value' WHERE id=1;
   ```

3. **Verify the update in Databend**

   ```sql
   SELECT * FROM mysql_data WHERE id=1;
   ```

## Key Features of Databend Kafka Connect

1. **Automatic Table and Column Creation**: With `auto.create` and `auto.evolve` settings, tables and columns are created automatically based on Kafka topic data

2. **Schema Support**: Supports Avro, JSON Schema, and Protobuf input data formats (requires Schema Registry)

3. **Multiple Write Modes**: Supports both `insert` and `upsert` write modes

4. **Multi-task Support**: Can run multiple tasks to improve performance

5. **High Availability**: In distributed mode, workload is automatically balanced with dynamic scaling and fault tolerance

## Troubleshooting

- **Connector Not Starting**: Check Kafka Connect logs for errors
- **No Data in Databend**: Verify topic exists and contains data using Kafka console consumer
- **Schema Issues**: Ensure `auto.create` and `auto.evolve` are set to `true`
