---
title: TiDB Quick Start Guide
summary: Learn how to deploy, monitor, test and stop a TiDB cluster.
category: quick start
---

# TiDB Quick Start Guide

## Before you begin

This guide introduces you the quickest way to deploy a TiDB cluster locally - using Docker Compose. Once you've installed [Docker Compose](https://docs.docker.com/compose/install/), [Git](https://git-scm.com/downloads) and [MySQL Server](https://dev.mysql.com/downloads/mysql/), you are all set.

> **Warning:** Running TiDB in Docker involves risks and is strongly discouraged for production application. For the production environment, it is recommended to [deploy TiDB using Ansible](op-guide/ansible-deployment.md).

## Deploy a TiDB cluster

First, open a terminal and enter the following commands:

1. To download `tidb-docker-compose`:

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. To get the latest TiDB Docker images and start the cluster:

    ```bash
    cd tidb-docker-compose && docker-compose pull 
    docker-compose up -d
    ```

3. Make sure that you have enabled the MySQL Server service in order to access the cluster:

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

## Monitor the cluster

After your machine successfully connects to MySQL Server on `127.0.0.1`, you can monitor real-time activities in the TiDB cluster with:

1. The [Grafana monitoring interface](op-guide/monitor-overview.md/#about-grafana-in-tidb):

    - Default address: <http://localhost:3000>
    - Default account name: admin
    - Default password: admin

2. The [cluster data visualization interface](https://github.com/pingcap/tidb-vision): 

    - Default address: <http://localhost:8010>

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
