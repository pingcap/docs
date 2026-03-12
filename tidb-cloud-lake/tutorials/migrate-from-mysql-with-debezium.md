---
title: Migrate MySQL with Debezium (CDC)
sidebar_label: 'MySQL → Databend: Debezium (CDC)'
---

> **Capabilities**: CDC, Full Load  
> **✅ Recommended** for real-time migration with complete change data capture

In this tutorial, you will load data from MySQL to Databend with Debezium. Before you start, make sure you have successfully set up Databend, MySQL, and Debezium in your environment.

## Step 1. Prepare Data in MySQL

Create a database and a table in MySQL, and insert sample data into the table.

```sql
CREATE DATABASE mydb;
USE mydb;

CREATE TABLE products (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,description VARCHAR(512));
ALTER TABLE products AUTO_INCREMENT = 10;

INSERT INTO products VALUES (default,"scooter","Small 2-wheel scooter"),
(default,"car battery","12V car battery"),
(default,"12-pack drill bits","12-pack of drill bits with sizes ranging from #40 to #3"),
(default,"hammer","12oz carpenter's hammer"),
(default,"hammer","14oz carpenter's hammer"),
(default,"hammer","16oz carpenter's hammer"),
(default,"rocks","box of assorted rocks"),
(default,"jacket","water-proof black wind breaker"),
(default,"cloud","test for databend"),
(default,"spare tire","24 inch spare tire");
```

## Step 2. Create database in Databend

Create the corresponding database in Databend. Please note that you don't need to create a table that corresponds to the one in MySQL.

```sql
CREATE DATABASE debezium;
```

## Step 3. Create application.properties

Create the file _application.properties_, then start debezium-server-databend. For how to install and start the tool, see [Installing debezium-server-databend](#installing-debezium-server-databend).

When started for the first time, the tool performs a full synchronization of data from MySQL to Databend using the specified Batch Size. As a result, the data from MySQL is now visible in Databend after successful replication.

```text title='application.properties'
debezium.sink.type=databend
debezium.sink.databend.upsert=true
debezium.sink.databend.upsert-keep-deletes=false
debezium.sink.databend.database.databaseName=debezium
debezium.sink.databend.database.url=jdbc:databend://<your-databend-host>:<port>
debezium.sink.databend.database.username=<your-username>
debezium.sink.databend.database.password=<your-password>
debezium.sink.databend.database.primaryKey=id
debezium.sink.databend.database.tableName=products
debezium.sink.databend.database.param.ssl=true

# enable event schemas
debezium.format.value.schemas.enable=true
debezium.format.key.schemas.enable=true
debezium.format.value=json
debezium.format.key=json

# mysql source
debezium.source.connector.class=io.debezium.connector.mysql.MySqlConnector
debezium.source.offset.storage.file.filename=data/offsets.dat
debezium.source.offset.flush.interval.ms=60000

debezium.source.database.hostname=127.0.0.1
debezium.source.database.port=3306
debezium.source.database.user=root
debezium.source.database.password=123456
debezium.source.database.dbname=mydb
debezium.source.database.server.name=from_mysql
debezium.source.include.schema.changes=false
debezium.source.table.include.list=mydb.products
# debezium.source.database.ssl.mode=required
# Run without Kafka, use local file to store checkpoints
debezium.source.database.history=io.debezium.relational.history.FileDatabaseHistory
debezium.source.database.history.file.filename=data/status.dat
# do event flattening. unwrap message!
debezium.transforms=unwrap
debezium.transforms.unwrap.type=io.debezium.transforms.ExtractNewRecordState
debezium.transforms.unwrap.delete.handling.mode=rewrite
debezium.transforms.unwrap.drop.tombstones=true

# ############ SET LOG LEVELS ############
quarkus.log.level=INFO
# Ignore messages below warning level from Jetty, because it's a bit verbose
quarkus.log.category."org.eclipse.jetty".level=WARN
```

You're all set! If you query the products table in Databend, you will see that the data from MySQL has been successfully synchronized. Feel free to perform insertions, updates, or deletions in MySQL, and you will observe the corresponding changes reflected in Databend as well.
