---
title: TiDB Quick Start Guide
summary: Learn how to deploy a TiDB cluster quickly.
category: quick start
---

# TiDB Quick Start Guide

This guide introduces how to deploy and monitor a TiDB cluster on your local drive using Docker Compose for experimenting and testing.

> **Warning:** Deploying TiDB using Docker Compose can only be used for experimental purposes. For production usage, [use Ansible to deploy the TiDB cluster](op-guide/ansible-deployment.md).

## Prerequisites

Before you begin, make sure to install the following tools:

- [Git](https://git-scm.com/downloads)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL Client](https://dev.mysql.com/downloads/mysql/)

## Deploy a TiDB cluster

1. Download `tidb-docker-compose`:

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. Change the directory to tidb-docker-compose and get the latest TiDB Docker Images:

    ```bash
    cd tidb-docker-compose && docker-compose pull
    ```

3. Start the TiDB cluster:

    ```bash
    docker-compose up -d
    ```

Congratulations! You have deployed a TiDB cluster! You can see messages in your terminal of the default components of a TiDB cluster: 

- 1 TiDB instance
- 3 TiKV instances
- 3 Placement Driver (PD) instances
- Prometheus
- Grafana
- 2 TiSpark instances (one master, one slave)
- 1 TiDB-Vision instance

You can now test your TiDB server using one of the following methods:

- Use the MySQL client to connect to TiDB to read and write data:

    ```
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

- Use Grafana to view the status of the cluster via [http://localhost:3000](http://localhost:3000) with the default account name and password:  `admin` and `admin`.
- Use [TiDB-Vision](https://github.com/pingcap/tidb-vision), a cluster visualization tool, to see data transfer and load-balancing inside your cluster via [http://localhost:8010](http://localhost:8010).

## Test the cluster

This section demonstrates some basic CRUD operations of TiDB in the terminal.

### Create, show, and drop a database

- To create a database, use the `CREATE DATABASE` statement:

    ```sql
    CREATE DATABASE db_name [options];
    ```

    For example, to create a database named `samp_db`:

    ```sql
    CREATE DATABASE IF NOT EXISTS samp_db;
    ```

- To show the databases, use the `SHOW DATABASES` statement:

    ```sql
    SHOW DATABASES;
    ```

- To delete a database, use the `DROP DATABASE` statement:

    ```sql
    DROP DATABASE samp_db;
    ```

### Create, show, and drop a table

- To create a table, use the `CREATE TABLE` statement:

    ```sql
    CREATE TABLE table_name column_name data_type constraint;
    ```

    For example:

    ```sql
    CREATE TABLE person (
     number INT(11),
     name VARCHAR(255),
     birthday DATE
    );
    ```

    Add `IF NOT EXISTS` to prevent an error if the table exists:

    ```sql
    CREATE TABLE IF NOT EXISTS person (
     number INT(11),
     name VARCHAR(255),
     birthday DATE
    );
    ```

- To view the statement that creates the table, use the `SHOW CREATE` statement:

    ```sql
    SHOW CREATE table person;
    ```

- To show all the tables in a database, use the `SHOW TABLES` statement:

    ```sql
    SHOW TABLES FROM samp_db;
    ```

- To show all the columns in a table, use the `SHOW FULL COLUMNS` statement:

    ```sql
    SHOW FULL COLUMNS FROM person;
    ```

- To delete a table, use the `DROP TABLE` statement:

    ```sql
    DROP TABLE person;
    ```

    or

    ```sql
    DROP TABLE IF EXISTS person;
    ```

### Create, show, and drop an index

- To create an index for the column whose value is not unique, use the `CREATE INDEX` or `ALTER TABLE` statement:

    ```sql
    CREATE INDEX person_num ON person (number);
    ```

    or

    ```sql
    ALTER TABLE person ADD INDEX person_num (number);
    ```

- To create a unique index for the column whose value is unique, use the `CREATE UNIQUE INDEX` or `ALTER TABLE` statement:

    ```sql
    CREATE UNIQUE INDEX person_num ON person (number);
    ```

    or

    ```sql
    ALTER TABLE person ADD UNIQUE person_num on (number);
    ```

- To show all the indexes in a table, use the `SHOW INDEX` statement:

    ```sql
    SHOW INDEX from person;
    ```

- To delete an index, use the `DROP INDEX` or `ALTER TABLE` statement:

    ```sql
    DROP INDEX person_num ON person;
    ALTER TABLE person DROP INDEX person_num;
    ```

### Insert, select, update, and delete data

- To insert data into a table, use the `INSERT` statement:

    ```sql
    INSERT INTO person VALUES("1","tom","20170912");
    ```

- To view the data in a table, use the `SELECT` statement:

    ```sql
    SELECT * FROM person;
    +--------+------+------------+
    | number | name | birthday   |
    +--------+------+------------+
    |      1 | tom  | 2017-09-12 |
    +--------+------+------------+
    ```

- To update the data in a table, use the `UPDATE` statement:

    ```sql
    UPDATE person SET birthday='20171010' WHERE name='tom';

    SELECT * FROM person;
    +--------+------+------------+
    | number | name | birthday   |
    +--------+------+------------+
    |      1 | tom  | 2017-10-10 |
    +--------+------+------------+
    ```

- To delete the data in a table, use the `DELETE` statement:

    ```sql
    DELETE FROM person WHERE number=1;
    SELECT * FROM person;
    Empty set (0.00 sec)
    ```

### Create, authorize, and delete a user

- To create a user, use the `CREATE USER` statement. The following example creates a user named `tiuser` with the password `123456`:

    ```sql
    CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
    ```

- To grant `tiuser` the privilege to retrieve the tables in the `samp_db` database:

    ```sql
    GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
    ```

- To check the privileges of `tiuser`:

    ```sql
    SHOW GRANTS for tiuser@localhost;
    ```

- To delete `tiuser`:

    ```sql
    DROP USER 'tiuser'@'localhost';
    ```

## Stop the cluster

1. Exit from the MySQL client:

    ```sql
    > exit;
    ```

2. Stop the TiDB cluster:

    ```bash
    docker-compose down
    ```

> **Note:** If you want to restart the TiDB cluster, just repeat the second step and the third step in the [deployment section](#deploy-a-tidb-cluster).
