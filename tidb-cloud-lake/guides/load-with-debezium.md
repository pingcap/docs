---
title: Debezium
---

[Debezium](https://debezium.io/) is a set of distributed services to capture changes in your databases so that your applications can see those changes and respond to them. Debezium records all row-level changes within each database table in a change event stream, and applications simply read these streams to see the change events in the same order in which they occurred.

[debezium-server-databend](https://github.com/databendcloud/debezium-server-databend) is a lightweight CDC tool developed by Databend, based on Debezium Engine. Its purpose is to capture real-time changes in relational databases and deliver them as event streams to ultimately write the data into the target database Databend. This tool provides a simple way to monitor and capture database changes, transforming them into consumable events without the need for large data infrastructures like Flink, Kafka, or Spark.

### Installing debezium-server-databend

debezium-server-databend can be installed independently without the need for installing Debezium beforehand. Once you have decided to install debezium-server-databend, you have two options available. The first one is to install it from source by downloading the source code and building it yourself. Alternatively, you can opt for a more straightforward installation process using Docker.

#### Installing debezium-server-databend from Source

Before you start, make sure JDK 11 and Maven are installed on your system.

1. Clone the project:

```bash
git clone https://github.com/databendcloud/debezium-server-databend.git
```

2. Change into the project's root directory:

```bash
cd debezium-server-databend
```

3. Build and package debezium server:

```go
mvn -Passembly -Dmaven.test.skip package
```

4. Once the build is completed, unzip the server distribution package:

```bash
unzip debezium-server-databend-dist/target/debezium-server-databend-dist*.zip -d databendDist
```

5. Enter the extracted folder:

```bash
cd databendDist
```

6. Create a file named _application.properties_ in the _conf_ folder with the content in the sample [here](https://github.com/databendcloud/debezium-server-databend/blob/main/debezium-server-databend-dist/src/main/resources/distro/conf/application.properties.example), and modify the configurations according to your specific requirements. For description of the available parameters, see this [page](https://github.com/databendcloud/debezium-server-databend/blob/main/docs/docs.md).

```bash
nano conf/application.properties
```

7. Use the provided script to start the tool:

```bash
bash run.sh
```

#### Installing debezium-server-databend with Docker

Before you start, make sure Docker and Docker Compose are installed on your system.

1. Create a file named _application.properties_ in the _conf_ folder with the content in the sample [here](https://github.com/databendcloud/debezium-server-databend/blob/main/debezium-server-databend-dist/src/main/resources/distro/conf/application.properties.example), and modify the configurations according to your specific requirements. For description of the available Databend parameters, see this [page](https://github.com/databendcloud/debezium-server-databend/blob/main/docs/docs.md).

```bash
nano conf/application.properties
```

2. Create a file named _docker-compose.yml_ with the following content:

```dockerfile
version: '2.1'
services:
  debezium:
    image: ghcr.io/databendcloud/debezium-server-databend:pr-2
    ports:
      - "8080:8080"
      - "8083:8083"
    volumes:
      - $PWD/conf:/app/conf
      - $PWD/data:/app/data
```

3. Open a terminal or command-line interface and navigate to the directory containing the _docker-compose.yml_ file.

4. Use the following command to start the tool:

```bash
docker-compose up -d
```

### Tutorials

- [Migrating from MySQL with Debezium](/tutorials/migrate/migrating-from-mysql-with-debezium)