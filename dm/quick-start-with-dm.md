---
title: Quick Start with TiDB Data Migration
summary: Learn how to quickly set up a data migration environment using TiUP Playground.
---

# Quick Start with TiDB Data Migration

[TiDB Data Migration (DM)](/dm/dm-overview.md) is a powerful tool that replicates data from MySQL-compatible databases to TiDB. This guide shows you how to quickly set up a local TiDB DM environment for development or testing using [TiUP Playground](/tiup/tiup-playground.md), and walks you through a simple task of migrating data from a source MySQL database to a target TiDB database.

> **Note:**
>
> For production deployments, see [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md).

## Step 1: Set up the test environment

[TiUP](/tiup/tiup-overview.md) is a cluster operation and maintenance tool. Its Playground feature lets you quickly launch a temporary local environment with a TiDB database and TiDB DM for development and testing.

1. Install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    > **Note:**
    >
    > If you have an existing installation of TiUP, ensure it is updated to v1.16.1 or later to use the `--dm-master` and `--dm-worker` flags. To check your current version, run the following command:
    >
    > ```shell
    > tiup --version
    > ```
    >
    > To upgrade TiUP to the latest version, run the following command:
    >
    > ```shell
    > tiup update --self
    > ```

2. Start TiUP Playground with a target TiDB database and DM components:

    ```shell
    tiup playground v8.5.1 --dm-master 1 --dm-worker 1 --tiflash 0 --without-monitor
    ```

3. Verify the environment by checking in the output whether TiDB and DM are running:

    ```text
    TiDB Playground Cluster is started, enjoy!

    Connect TiDB:    mysql --host 127.0.0.1 --port 4000 -u root
    Connect DM:      tiup dmctl --master-addr 127.0.0.1:8261
    TiDB Dashboard:  http://127.0.0.1:2379/dashboard
    ```

4. Keep `tiup playground` running in the current terminal and open a new terminal for the following steps.

    This playground environment provides the running processes for the target TiDB database and the replication engine (DM-master and DM-worker). It will handle the data flow: MySQL (source) → DM (replication engine) → TiDB (target).

## Step 2: Prepare a source database (optional)

You can use one or more MySQL instances as a source database. If you already have a MySQL-compatible instance, skip to [Step 3](#step-3-configure-a-tidb-dm-source). Otherwise, take the following steps to create one for testing.

<SimpleTab groupId="os">

<div label="Docker" value="docker">

You can use Docker to quickly deploy a test MySQL 8.0 instance.

1. Run a MySQL 8.0 Docker container:

    ```shell
    docker run --name mysql80 \
        -e MYSQL_ROOT_PASSWORD=MyPassw0rd! \
        -p 3306:3306 \
        -d mysql:8.0
    ```

2. Connect to MySQL:

    ```shell
    docker exec -it mysql80 mysql -uroot -pMyPassw0rd!
    ```

3. Create a dedicated user with required privileges for DM testing:

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

4. Create sample data:

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="macOS" value="macos">

On macOS, you can quickly install and start MySQL 8.0 locally using [Homebrew](https://brew.sh).

1. Update Homebrew and install MySQL 8.0:

    ```shell
    brew update
    brew install mysql@8.0
    ```

2. Make MySQL commands accessible in the system path:

    ```shell
    brew link mysql@8.0 --force
    ```

3. Start the MySQL service:

    ```shell
    brew services start mysql@8.0
    ```

4. Connect to MySQL as the `root` user:

    ```shell
    mysql -uroot
    ```

5. Create a dedicated user with required privileges for DM testing:

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6. Create sample data:

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="CentOS" value="centos">

On Enterprise Linux distributions like CentOS, you can install MySQL 8.0 from the MySQL Yum repository.

1. Download and install the MySQL Yum repository package from [MySQL Yum repository download page](https://dev.mysql.com/downloads/repo/yum). For Linux versions other than 9, you must replace the `el9` (Enterprise Linux version 9) in the following URL while keeping `mysql80` for MySQL version 8.0:

    ```shell
    sudo yum install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
    ```

2. Install MySQL:

    ```shell
    sudo yum install -y mysql-community-server --nogpgcheck
    ```

3. Start MySQL:

    ```shell
    sudo systemctl start mysqld
    ```

4. Find the temporary root password in the MySQL log:

    ```shell
    sudo grep 'temporary password' /var/log/mysqld.log
    ```

5. Connect to MySQL as the `root` user with the temporary password:

    ```shell
    mysql -uroot -p
    ```

6. Reset the `root` password:

    ```sql
    ALTER USER 'root'@'localhost'
        IDENTIFIED BY 'MyPassw0rd!';
    ```

7. Create a dedicated user with required privileges for DM testing:

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

8. Create sample data:

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

<div label="Ubuntu" value="ubuntu">

On Ubuntu, you can install MySQL from the official Ubuntu repository.

1. Update your package list:

    ```shell
    sudo apt-get update
    ```

2. Install MySQL:

    ```shell
    sudo apt-get install -y mysql-server
    ```

3. Check whether the `mysql` service is running, and start the service if necessary:

    ```shell
    sudo systemctl status mysql
    sudo systemctl start mysql
    ```

4. Connect to MySQL as the `root` user using socket authentication:

    ```shell
    sudo mysql
    ```

5. Create a dedicated user with required privileges for DM testing:

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

6. Create sample data:

    ```sql
    CREATE DATABASE hello;
    USE hello;

    CREATE TABLE hello_tidb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    );

    INSERT INTO hello_tidb (name) VALUES ('Hello World');

    SELECT * FROM hello_tidb;
    ```

</div>

</SimpleTab>

## Step 3: Configure a TiDB DM source

After preparing the source MySQL database, configure TiDB DM to connect to it. To do this, create a source configuration file with the connection details and apply the configuration using the `dmctl` tool.

1. Create a source configuration file `mysql-01.yaml`:

    > **Note:**
    >
    > This step assumes you have already created the `tidb-dm` user with replication privileges in the source database, as described in [Step 2](#step-2-prepare-a-source-database-optional).

    ```yaml
    source-id: "mysql-01"
    from:
      host: "127.0.0.1"
      user: "tidb-dm"
      password: "MyPassw0rd!"    # In production environments, it is recommended to use a password encrypted with dmctl.
      port: 3306
    ```

2. Create a DM data source:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 operate-source create mysql-01.yaml
    ```

## Step 4: Create a TiDB DM task

After configuring the source database, you can create a migration task in TiDB DM. This task references the source MySQL instance and defines the connection details for the target TiDB database.

1. Create a DM task configuration file `tiup-playground-task.yaml`:

    ```yaml
    # Task
    name: tiup-playground-task
    task-mode: "all"              # Execute all phases - full data migration and incremental sync.

    # Source (MySQL)
    mysql-instances:
      - source-id: "mysql-01"

    ## Target (TiDB)
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: ""                # If the password is not empty, it is recommended to use a password encrypted with dmctl.
    ```

2. Start the task using the configuration file:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 start-task tiup-playground-task.yaml
    ```

## Step 5: Verify the data replication

After starting the migration task, verify whether data replication is working as expected. Use the `dmctl` tool to check the task status, and connect to the target TiDB database to confirm that the data has been successfully replicated from the source MySQL database.

1. Check the status of the TiDB DM task:

    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 query-status
    ```

2. Connect to the target TiDB database:

    ```shell
    mysql --host 127.0.0.1 --port 4000 -u root --prompt 'tidb> '
    ```

3. Verify the replicated data. If you have created the sample data in [Step 2](#step-2-prepare-a-source-database-optional), you will see the `hello_tidb` table replicated from the MySQL source database to the target TiDB database:

    ```sql
    SELECT * FROM hello.hello_tidb;
    ```

    The output is as follows:

    ```sql
    +----+-------------+
    | id | name        |
    +----+-------------+
    |  1 | Hello World |
    +----+-------------+
    1 row in set (0.00 sec)
    ```

## Step 6: Clean up (optional)

After completing your testing, you can clean up the environment by stopping the TiUP Playground, removing the source MySQL instance (if created for testing), and deleting unnecessary files.

1. Stop the TiUP Playground:

    In the terminal where the TiUP Playground is running, press <kbd>Control</kbd>+<kbd>C</kbd> to terminate the process. This stops all TiDB and DM components and deletes the target environment.

2. Stop and remove the source MySQL instance:

    If you have created a source MySQL instance for testing in [Step 2](#step-2-prepare-a-source-database-optional), stop and remove it by taking the following steps:

    <SimpleTab groupId="os">

    <div label="Docker" value="docker">

    To stop and remove the Docker container:

    ```shell
    docker stop mysql80
    docker rm mysql80
    ```

    </div>

    <div label="macOS" value="macos">

    If you installed MySQL 8.0 using Homebrew solely for testing, stop the service and uninstall it:

    ```shell
    brew services stop mysql@8.0
    brew uninstall mysql@8.0
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/opt/homebrew/var/mysql`).

    </div>

    <div label="CentOS" value="centos">

    If you installed MySQL 8.0 from the MySQL Yum repository solely for testing, stop the service and uninstall it:

    ```shell
    sudo systemctl stop mysqld
    sudo yum remove -y mysql-community-server
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/var/lib/mysql`).

    </div>

    <div label="Ubuntu" value="ubuntu">

    If you installed MySQL from the official Ubuntu repository solely for testing, stop the service and uninstall it:

    ```shell
    sudo systemctl stop mysql
    sudo apt-get remove --purge -y mysql-server
    sudo apt-get autoremove -y
    ```

    > **Note:**
    >
    > If you want to remove all MySQL data files, delete the MySQL data directory (commonly located at `/var/lib/mysql`).

    </div>

    </SimpleTab>

3. Remove the TiDB DM configuration files if they are no longer needed:

    ```shell
    rm mysql-01.yaml tiup-playground-task.yaml
    ```

4. If you no longer need TiUP, you can uninstall it:

    ```shell
    rm -rf ~/.tiup
    ```

## What's next

Now that you successfully created a task that migrates data from a source MySQL database to a target TiDB database in a testing environment, you can:

- Explore [TiDB DM Features](/dm/dm-overview.md)
- Learn about [TiDB DM Architecture](/dm/dm-arch.md)
- Set up [TiDB DM for a Proof of Concept or Production](/dm/deploy-a-dm-cluster-using-tiup.md)
- Configure advanced [DM Tasks](/dm/dm-task-configuration-guide.md)
