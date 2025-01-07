---
title: TiDB Data Migration Quick Start
summary: Learn how to quickly set up a data migration environment using TiUP playground.
aliases: ['/docs/tidb-data-migration/dev/get-started/']
---

# Quick Start Guide for TiDB Data Migration

TiDB Data Migration (DM) is a powerful tool that replicates databases from MySQL-compatible databases to TiDB. This guide will walk you through setting up a local TiDB DM environment for development and testing using TiUP Playground.

> **Note:**
>
> For production deployments, please refer to [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster.md).

## Step 1: Set Up the Test Environment

TiUP is a command-line tool for managing TiDB components. Its Playground feature lets you quickly launch a temporary local environment with a TiDB database and TiDB DM for development and testing.

1. Install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Start TiUP Playground with a TiDB target database and DM components:

    ```shell
    tiup playground --dm-master 1 --dm-worker 1 --tiflash 0 --without-monitor
    ```

3. Verify the environment by checking in the output if TiDB and DM are running: 

    ```text
    TiDB Playground Cluster is started, enjoy!

    Connect TiDB:    mysql --host 127.0.0.1 --port 4000 -u root
    Connect DM:      tiup dmctl --master-addr 127.0.0.1:8261
    TiDB Dashboard:  http://127.0.0.1:2379/dashboard
    ```
4. Keep `tiup playground` running in the current terminal and open a new terminal for the next steps. This playground environment provides the running processes for the target TiDB database and the replication engine (DM-master and DM-worker). It will handle the data flow from MySQL (source) → DM (replication engine) → TiDB (target).

## Step 2: Prepare a Source Database (Optional)

You can use one or multiple MySQL instances as a source database. If you do not have a MySQL-compatible instance already, you can create one for testing purposes with the following procedure. If you already have a source MySQL database, you can skip to the Step 3.


<SimpleTab>

<div label="Docker">

You can use Docker to quickly deploy a test MySQL 8.0 instance by following this procedure.

1. Run a MySQL 8 docker container with:

    ```shell
    docker run --name mysql80 \
        -e MYSQL_ROOT_PASSWORD=MyPassw0rd! \
        -p 3306:3306 \
        -d mysql:8.0
    ```

2. Connect to MySQL with:

    ```shell
    docker exec -it mysql80 mysql -uroot -pMyPassw0rd!
    ```

3. Create a dedicated user for DM with the necessary privileges:

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

</SimpleTab>

<div label="macOS">

If you are on macOS, you can quickly install and start MySQL 8.0 locally via [Homebrew](https://brew.sh):

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

4. Connect to MySQL as `root`:

    ```shell
    mysql -uroot
    ```

5. For DM testing purposes, create a dedicated user and grant privileges:

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

<div label="CentOS">

On Enterprise Linux distros like CentOS, install MySQL 8.0 from the MySQL Yum repository:

1. Download and install the MySQL Yum repository package from [MySQL Yum repo download page](https://dev.mysql.com/downloads/repo/yum). For Linux versions different than 9, you must replace the `el9` (Enterprise Linux version 9) in the URL below while keeping `mysql80` for MySQL version 8.0:

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

5. Connect to MySQL as `root` with the temporary password:

    ```shell
    mysql -uroot -p
    ```

6. Reset MySQL `root` password: 

    ```sql
    ALTER USER 'root'@'localhost'
        IDENTIFIED BY 'MyPassw0rd!';    
    ```

6. For DM testing purposes, create a dedicated user and grant privileges:

    ```sql
    CREATE USER 'tidb-dm'@'%'
        IDENTIFIED WITH mysql_native_password
        BY 'MyPassw0rd!';

    GRANT PROCESS, BACKUP_ADMIN, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'tidb-dm'@'%';
    ```

7. Create sample data:

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

<div label="Ubuntu">

On Ubuntu, you can install MySQL from the official Ubuntu repository:

1. Update your package list:

    ```shell
    sudo apt-get update
    ```

2. Install MySQL:

    ```shell
    sudo apt-get install -y mysql-server
    ```

3. Check if `mysql` service is running, and start the service if necessary:

    ```shell
    sudo systemctl status mysql
    sudo systemctl start mysql
    ```


4. Connect to MySQL as `root` via socket authentication:

    ```shell
    sudo mysql
    ```

5. For DM testing purposes, create a dedicated user and grant privileges:

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


## Step 3: Configure a TiDB DM Source

With the source MySQL database ready and accessible, the next step is to configure TiDB DM to connect to it. This involves creating a source configuration file with the connection details and applying the configurations using the `dmctl` tool.

1. Create a source configuration file `mysql-01.yaml`:

    > **Note:** Here we assume the `tidb-dm` user with replication privileges has been created in the source database as shown in Step 2.

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

## Step 4: Create a TiDB DM Task

After configuring the source database, you can create a migration task in TiDB DM that will reference the source MySQL instances and define the target TiDB connection details. 

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

## Step 5: Verify the Data Replication

Once the migration task is running, you can verify that the data replication is working as expected using the `dmctl` tool and by connecting to the target database to confirm that the data has been successfully replicated from the source MySQL database to the target TiDB cluster.

1. Verify TiDB DM tasks status with:
    ```shell
    tiup dmctl --master-addr 127.0.0.1:8261 query-status
    ```

2. Connect to the TiDB target database to verify the replicated data:

    ```shell
    mysql -uroot -h127.0.0.1 -P4000 --prompt 'tidb> '
    ```

3. If you created the sample data in step 2, you can will see the `hello_tidb` table replicated from the MySQL source database to the TiDB target database:

    ```sql
    SELECT * FROM hello.hello_tidb;
    ```



## Step 6: Clean Up (Optional)

1. In the terminal where the TiUP Playground is running, press `Ctrl + C` to terminate the process. This will stop all TiDB and DM components and delete the target environment.

2. If you created a source MySQL instance for testing in Step 2, stop and remove.

    <SimpleTab>

    <div label="Docker">

    To stop and remove the Docker container:

    ```shell
    docker stop mysql80
    docker rm mysql80
    ```

    </div>

    <div label="macOS">

    If you installed MySQL 8.0 via Homebrew solely for testing, stop the service and uninstall with:

    ```shell
    brew services stop mysql@8.0
    brew uninstall mysql@8.0
    ```

    > **Note:** If you want to remove all MySQL data files, remove the MySQL data directory (commonly `/opt/homebrew/var/mysql`).

    </div>

    <div label="CentOS">

    If you installed MySQL 8.0 via the MySQL Yum repository, stop the service and uninstall with:

    ```shell
    sudo systemctl stop mysqld
    sudo yum remove -y mysql-community-server
    ```

    > **Note:** If you want to remove all MySQL data files, remove the MySQL data directory (commonly `/var/lib/mysql`).

    </div>

    <div label="Ubuntu">

    If you installed MySQL from the official Ubuntu repository, stop the service and uninstall with:

    ```shell
    sudo systemctl stop mysql
    sudo apt-get remove --purge -y mysql-server
    sudo apt-get autoremove -y
    ```

    > **Note:** If you want to remove all MySQL data files, remove the MySQL data directory (commonly `/var/lib/mysql`).

    </div>

    </SimpleTab>

3.	Remove the TiDB DM configuration files if they are no longer needed:

    ```shell
    rm mysql-01.yaml tiup-playground-task.yaml
    ```


4. If you no longer need TiUP, you can uninstall it:

    ```shell
    rm -rf ~/.tiup
    ```

## What's Next

Now that you successfully created a task that migrates data from a source MySQL database to a target TiDB in a testing environment, you can:

- Explore [TiDB DM Features](/dm/dm-features.md)
- Learn about [TiDB DM Architecture](/dm/dm-overview.md)
- Set up [TiDB DM for a Proof of Concept or Production](/dm/deploy-a-dm-cluster.md)
- Configure advanced [DM Tasks](/dm/dm-task-configuration-guide.md)
