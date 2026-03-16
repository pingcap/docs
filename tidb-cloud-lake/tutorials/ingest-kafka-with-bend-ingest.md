---
title: Ingest Kafka with Bend Ingest
---

In this tutorial, we'll guide you through setting up a Kafka environment using Docker and loading messages from Kafka into Databend Cloud with [bend-ingest-kafka](https://github.com/databendcloud/bend-ingest-kafka).

### Step 1: Setting up Kafka Environment

Run the Apache Kafka Docker container on port 9092:

```shell
MacBook-Air:~ eric$ docker run -d \
>   --name kafka \
>   -p 9092:9092 \
>   apache/kafka:latest
Unable to find image 'apache/kafka:latest' locally
latest: Pulling from apache/kafka
690e87867337: Pull complete
5dddb19fae62: Pull complete
86caa4220d9f: Pull complete
7802c028acb4: Pull complete
16a3d1421c02: Pull complete
ab648c7f18ee: Pull complete
a917a90b7df6: Pull complete
4e446fc89158: Pull complete
f800ce0fc22f: Pull complete
a2e5e46262c3: Pull complete
Digest: sha256:c89f315cff967322c5d2021434b32271393cb193aa7ec1d43e97341924e57069
Status: Downloaded newer image for apache/kafka:latest
0261b8f3d5fde74f5f20340b58cb85d29d9b40ee4f48f1df2c41a68b616d22dc
```

### Step 2: Create Topic & Produce Messages

1. Access the Kafka container:

```shell
MacBook-Air:~ eric$ docker exec --workdir /opt/kafka/bin/ -it kafka sh
```

2. Create a new Kafka topic named `test-topic`:

```shell
/opt/kafka/bin $ ./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic
Created topic test-topic.
```

3. Produce messages to the test-topic using the Kafka console producer:

```shell
/opt/kafka/bin $ ./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```

4. Enter messages in JSON format:

```json
{"id": 1, "name": "Alice", "age": 30}
{"id": 2, "name": "Bob", "age": 25}
```

5. Stop the producer with Ctrl+C once done.

### Step 3: Create Table in Databend Cloud

Create the target table in Databend Cloud:

```sql
CREATE DATABASE doc;

CREATE    TABLE databend_topic (
          id INT NOT NULL,
          name VARCHAR NOT NULL,
          age INT NOT NULL
          ) ENGINE=FUSE;
```

### Step 4: Install & Run bend-ingest-kafka

1. Install the bend-ingest-kafka tool by running the following command:

```shell
go install  github.com/databendcloud/bend-ingest-kafka@latest
```

2. Run the following command to ingest messages from the `test-topic` Kafka topic into the target table in Databend Cloud:

```shell
MacBook-Air:~ eric$ bend-ingest-kafka \
>   --kafka-bootstrap-servers="localhost:9092" \
>   --kafka-topic="test-topic" \
>   --databend-dsn="<your-dsn>" \
>   --databend-table="doc.databend_topic" \
>   --data-format="json"
INFO[0000] Starting worker worker-0
WARN[0072] Failed to read message from Kafka: context deadline exceeded  kafka_batch_reader=ReadBatch
2024/08/20 15:10:15 ingest 2 rows (1.225576 rows/s), 75 bytes (45.959100 bytes/s)
```

3. Connect to Databend Cloud using BendSQL and verify that the data has been successfully loaded:

```bash
Welcome to BendSQL 0.19.2-1e338e1(2024-07-17T09:02:28.323121000Z).
Connecting to tn3ftqihs--eric.gw.aws-us-east-2.default.databend.com:443 with warehouse eric as user cloudapp
Connected to Databend Query v1.2.626-nightly-a055124b65(rust-1.81.0-nightly-2024-08-27T15:49:08.376336236Z)

cloudapp@(eric)/doc> SELECT * FROM databend_topic;

SELECT * FROM databend_topic

-[ RECORD 1 ]-----------------------------------
  id: 1
name: Alice
 age: 30
-[ RECORD 2 ]-----------------------------------
  id: 2
name: Bob
 age: 25
```

4. To load the messages in RAW mode, simple run the following command:

```bash
bend-ingest-kafka \
  --kafka-bootstrap-servers="localhost:9092" \
  --kafka-topic="test-topic" \
  --databend-dsn="<your-dsn>" \
  --is-json-transform=false 
```

You will get a new table in the `doc` database, containing the following rows:

```bash
cloudapp@(eric)/doc> SELECT * FROM test_ingest;

SELECT * FROM test_ingest

-[ RECORD 1 ]-----------------------------------
           uuid: 17f9e56e-19ba-4d42-88a0-e16b27815d04
        koffset: 0
     kpartition: 0
       raw_data: {"age":30,"id":1,"name":"Alice"}
record_metadata: {"create_time":"2024-08-27T19:10:45.888Z","key":"","offset":0,"partition":0,"topic":"test-topic"}
       add_time: 2024-08-27 19:12:55.081444
-[ RECORD 2 ]-----------------------------------
           uuid: 0f57f71a-32ee-4df3-b75e-d123b9a91543
        koffset: 1
     kpartition: 0
       raw_data: {"age":25,"id":2,"name":"Bob"}
record_metadata: {"create_time":"2024-08-27T19:10:52.946Z","key":"","offset":1,"partition":0,"topic":"test-topic"}
       add_time: 2024-08-27 19:12:55.081470
```
