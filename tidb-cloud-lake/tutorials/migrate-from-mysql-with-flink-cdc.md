---
title: Migrate MySQL with Flink CDC
sidebar_label: 'MySQL → Databend: Flink CDC'
---

> **Capabilities**: CDC, Full Load, Transformation

In this tutorial, we'll walk you through the process of migrating from MySQL to Databend Cloud using Apache Flink CDC.

## Before You Start

Before you start, ensure you have the following prerequisites in place:

- [Docker](https://www.docker.com/) is installed on your local machine, as it will be used to launch MySQL.
- Java 8 or 11 is installed on your local machine, as it is required by the [Flink Databend Connector](https://github.com/databendcloud/flink-connector-databend).
- BendSQL is installed on your local machine. See [Installing BendSQL](/guides/connect/sql-clients/bendsql/#installing-bendsql) for instructions on how to install BendSQL using various package managers.

## Step 1: Launch MySQL in Docker

1. Create a configuration file named **mysql.cnf** with the following content, and save this file in a local directory that will be mapped to the MySQL container, e.g., `/Users/eric/Downloads/mysql.cnf`:

```cnf
[mysqld]
# Basic settings
server-id=1
log-bin=mysql-bin
binlog_format=ROW
binlog_row_image=FULL
expire_logs_days=3

# Character set settings
character_set_server=utf8mb4
collation-server=utf8mb4_unicode_ci

# Authentication settings
default-authentication-plugin=mysql_native_password
```

2. Start a MySQL container on your local machine. The command below launches a MySQL container named **mysql-server**, creates a database named **mydb**, and sets the root password to `root`:

```bash
docker run \
  --platform linux/amd64 \
  --name mysql-server \
  -v /Users/eric/Downloads/mysql.cnf:/etc/mysql/conf.d/custom.cnf \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_ROOT_HOST=% \
  -p 3306:3306 \
  -d mysql:5.7
```

3. Verify MySQL is running:

```bash
docker ps
```

Check the output for a container named **mysql-server**:

```bash 
CONTAINER ID   IMAGE       COMMAND                  CREATED        STATUS        PORTS                               NAMES
aac4c28be56e   mysql:5.7   "docker-entrypoint.s…"   17 hours ago   Up 17 hours   0.0.0.0:3306->3306/tcp, 33060/tcp   mysql-server
```

## Step 2: Populate MySQL with Sample Data

1. Log in to the MySQL container and enter the password `root` when prompted:

```bash
docker exec -it mysql-server mysql -u root -p
```

```
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 71
Server version: 5.7.44-log MySQL Community Server (GPL)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

2. Switch to the **mydb** database:

```bash
mysql> USE mydb;
Database changed
```

3. Copy and paste the following SQL to create a table named **products** and insert data:

```sql
CREATE TABLE products (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,description VARCHAR(512));

ALTER TABLE products AUTO_INCREMENT = 10;

INSERT INTO products VALUES (default,"scooter","Small 2-wheel scooter"),
(default,"car battery","12V car battery"),
(default,"12-pack drill bits","12-pack of drill bits with sizes ranging from #40 to #3"),
(default,"hammer","12oz carpenter's hammer"),
(default,"hammer","14oz carpenter's hammer"),
(default,"hammer","16oz carpenter's hammer"),
(default,"rocks","box of assorted rocks"),
(default,"jacket","black wind breaker"),
(default,"cloud","test for databend"),
(default,"spare tire","24 inch spare tire");
```

4. Verify the data:

```bash
mysql> select * from products;
+----+--------------------+---------------------------------------------------------+
| id | name               | description                                             |
+----+--------------------+---------------------------------------------------------+
| 10 | scooter            | Small 2-wheel scooter                                   |
| 11 | car battery        | 12V car battery                                         |
| 12 | 12-pack drill bits | 12-pack of drill bits with sizes ranging from #40 to #3 |
| 13 | hammer             | 12oz carpenter's hammer                                 |
| 14 | hammer             | 14oz carpenter's hammer                                 |
| 15 | hammer             | 16oz carpenter's hammer                                 |
| 16 | rocks              | box of assorted rocks                                   |
| 17 | jacket             | black wind breaker                                      |
| 18 | cloud              | test for databend                                       |
| 19 | spare tire         | 24 inch spare tire                                      |
+----+--------------------+---------------------------------------------------------+
10 rows in set (0.01 sec)
```

## Step 3: Set Up Target in Databend Cloud

1. Connect to Databend Cloud using BendSQL. If you're unfamiliar with BendSQL, refer to this tutorial: [Connecting to Databend Cloud using BendSQL](../getting-started/connect-to-databendcloud-bendsql.md).

2. Copy and paste the following SQL to create a target table named **products**:

```sql
CREATE    TABLE products (
          id INT NOT NULL,
          name VARCHAR(255) NOT NULL,
          description VARCHAR(512)
          );
```

## Step 4: Install Flink CDC

1. Download and extract Flink 1.17.1:

```bash
curl -O https://archive.apache.org/dist/flink/flink-1.17.1/flink-1.17.1-bin-scala_2.12.tgz
tar -xvzf flink-1.17.1-bin-scala_2.12.tgz
cd flink-1.17.1
```

2. Download the Databend and MySQL connectors into the **lib** folder:

```bash
curl -Lo lib/flink-connector-databend.jar https://github.com/databendcloud/flink-connector-databend/releases/latest/download/flink-connector-databend.jar

curl -Lo lib/flink-sql-connector-mysql-cdc-2.4.1.jar https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-mysql-cdc/2.4.1/flink-sql-connector-mysql-cdc-2.4.1.jar
```

3. Open the file **flink-conf.yaml** under `flink-1.17.1/conf/`, update `taskmanager.memory.process.size` to `4096m`, and save the file.

```yaml
taskmanager.memory.process.size: 4096m
```

4. Start a Flink cluster:

```shell
./bin/start-cluster.sh
```

You can now open the Apache Flink Dashboard if you go to [http://localhost:8081](http://localhost:8081) in your browser:

![Alt text](/img/load/cdc-dashboard.png)

## Step 5: Start Migration

1. Start the Flink SQL Client:

```bash
./bin/sql-client.sh
```

You will see the Flink SQL Client startup banner, confirming that the client has launched successfully.

```bash

                                   ▒▓██▓██▒
                               ▓████▒▒█▓▒▓███▓▒
                            ▓███▓░░        ▒▒▒▓██▒  ▒
                          ░██▒   ▒▒▓▓█▓▓▒░      ▒████
                          ██▒         ░▒▓███▒    ▒█▒█▒
                            ░▓█            ███   ▓░▒██
                              ▓█       ▒▒▒▒▒▓██▓░▒░▓▓█
                            █░ █   ▒▒░       ███▓▓█ ▒█▒▒▒
                            ████░   ▒▓█▓      ██▒▒▒ ▓███▒
                         ░▒█▓▓██       ▓█▒    ▓█▒▓██▓ ░█░
                   ▓░▒▓████▒ ██         ▒█    █▓░▒█▒░▒█▒
                  ███▓░██▓  ▓█           █   █▓ ▒▓█▓▓█▒
                ░██▓  ░█░            █  █▒ ▒█████▓▒ ██▓░▒
               ███░ ░ █░          ▓ ░█ █████▒░░    ░█░▓  ▓░
              ██▓█ ▒▒▓▒          ▓███████▓░       ▒█▒ ▒▓ ▓██▓
           ▒██▓ ▓█ █▓█       ░▒█████▓▓▒░         ██▒▒  █ ▒  ▓█▒
           ▓█▓  ▓█ ██▓ ░▓▓▓▓▓▓▓▒              ▒██▓           ░█▒
           ▓█    █ ▓███▓▒░              ░▓▓▓███▓          ░▒░ ▓█
           ██▓    ██▒    ░▒▓▓███▓▓▓▓▓██████▓▒            ▓███  █
          ▓███▒ ███   ░▓▓▒░░   ░▓████▓░                  ░▒▓▒  █▓
          █▓▒▒▓▓██  ░▒▒░░░▒▒▒▒▓██▓░                            █▓
          ██ ▓░▒█   ▓▓▓▓▒░░  ▒█▓       ▒▓▓██▓    ▓▒          ▒▒▓
          ▓█▓ ▓▒█  █▓░  ░▒▓▓██▒            ░▓█▒   ▒▒▒░▒▒▓█████▒
           ██░ ▓█▒█▒  ▒▓▓▒  ▓█                █░      ░░░░   ░█▒
           ▓█   ▒█▓   ░     █░                ▒█              █▓
            █▓   ██         █░                 ▓▓        ▒█▓▓▓▒█░
             █▓ ░▓██░       ▓▒                  ▓█▓▒░░░▒▓█░    ▒█
              ██   ▓█▓░      ▒                    ░▒█▒██▒      ▓▓
               ▓█▒   ▒█▓▒░                         ▒▒ █▒█▓▒▒░░▒██
                ░██▒    ▒▓▓▒                     ▓██▓▒█▒ ░▓▓▓▓▒█▓
                  ░▓██▒                          ▓░  ▒█▓█  ░░▒▒▒
                      ▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▓▓  ▓░▒█░

    ______ _ _       _       _____  ____  _         _____ _ _            _  BETA
   |  ____| (_)     | |     / ____|/ __ \| |       / ____| (_)          | |
   | |__  | |_ _ __ | | __ | (___ | |  | | |      | |    | |_  ___ _ __ | |_
   |  __| | | | '_ \| |/ /  \___ \| |  | | |      | |    | | |/ _ \ '_ \| __|
   | |    | | | | | |   <   ____) | |__| | |____  | |____| | |  __/ | | | |_
   |_|    |_|_|_| |_|_|\_\ |_____/ \___\_\______|  \_____|_|_|\___|_| |_|\__|

        Welcome! Enter 'HELP;' to list all available commands. 'QUIT;' to exit.
```

2. Set the checkpointing interval to 3 seconds.

```bash
Flink SQL> SET execution.checkpointing.interval = 3s;
```

3. Create corresponding tables with MySQL and Databend connectors in the Flink SQL Client (replace the placeholders with your actual values):

```sql
CREATE TABLE mysql_products (id INT,name STRING,description STRING,PRIMARY KEY (id) NOT ENFORCED)
WITH ('connector' = 'mysql-cdc',
'hostname' = '127.0.0.1',
'port' = '3306',
'username' = 'root',
'password' = 'root',
'database-name' = 'mydb',
'table-name' = 'products',
'server-time-zone' = 'UTC'
);

CREATE TABLE databend_products (id INT,name String,description String, PRIMARY KEY (`id`) NOT ENFORCED)
WITH ('connector' = 'databend',
'url'='databend://cloudapp:{password}@{host}:443/{database}?warehouse={warehouse_name}&ssl=true',
'database-name'='{database}',
'table-name'='products',
'sink.batch-size' = '1',
'sink.flush-interval' = '1000',
'sink.ignore-delete' = 'false',
'sink.max-retries' = '3');
```

4. In the Flink SQL Client, synchronize the data from the mysql_products table to the databend_products table:

```sql
Flink SQL> INSERT INTO databend_products SELECT * FROM mysql_products;
>
[INFO] Submitting SQL update statement to the cluster...
[INFO] SQL update statement has been successfully submitted to the cluster:
Job ID: 5b505d752b7c211cbdcb5566175b9182
```

You can now see a running job in the Apache Flink Dashboard:

![Alt text](/img/load/cdc-job.png)

You're all set! If you go back to the BendSQL terminal and query the **products** table in Databend Cloud, you will see that the data from MySQL has been successfully synchronized:

```sql
SELECT * FROM products;

┌──────────────────────────────────────────────────────────────────────────────────────┐
│   id  │        name        │                       description                       │
│ Int32 │       String       │                     Nullable(String)                    │
├───────┼────────────────────┼─────────────────────────────────────────────────────────┤
│    18 │ cloud              │ test for databend                                       │
│    19 │ spare tire         │ 24 inch spare tire                                      │
│    16 │ rocks              │ box of assorted rocks                                   │
│    17 │ jacket             │ black wind breaker                                      │
│    14 │ hammer             │ 14oz carpenter's hammer                                 │
│    15 │ hammer             │ 16oz carpenter's hammer                                 │
│    12 │ 12-pack drill bits │ 12-pack of drill bits with sizes ranging from #40 to #3 │
│    13 │ hammer             │ 12oz carpenter's hammer                                 │
│    10 │ scooter            │ Small 2-wheel scooter                                   │
│    11 │ car battery        │ 12V car battery                                         │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

5. Return to the MySQL terminal and insert a new product:

```sql
INSERT INTO products VALUES (default, "bicycle", "Lightweight road bicycle");
```

Next, in the BendSQL terminal, query the **products** table again to verify the new product has been synced:

```sql
SELECT * FROM products;

┌──────────────────────────────────────────────────────────────────────────────────────┐
│   id  │        name        │                       description                       │
│ Int32 │       String       │                     Nullable(String)                    │
├───────┼────────────────────┼─────────────────────────────────────────────────────────┤
│    12 │ 12-pack drill bits │ 12-pack of drill bits with sizes ranging from #40 to #3 │
│    11 │ car battery        │ 12V car battery                                         │
│    14 │ hammer             │ 14oz carpenter's hammer                                 │
│    13 │ hammer             │ 12oz carpenter's hammer                                 │
│    10 │ scooter            │ Small 2-wheel scooter                                   │
│    20 │ bicycle            │ Lightweight road bicycle                                │
│    19 │ spare tire         │ 24 inch spare tire                                      │
│    16 │ rocks              │ box of assorted rocks                                   │
│    15 │ hammer             │ 16oz carpenter's hammer                                 │
│    18 │ cloud              │ test for databend                                       │
│    17 │ jacket             │ black wind breaker                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```
