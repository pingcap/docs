---
title: Integrate TiDB with ProxySQL Step by Step
summary: Introduce how to integrate TiDB with ProxySQL step by step.
---

# Integrate TiDB with ProxySQL Step by Step

This document briefly describes how to integrate **TiDB** with **ProxySQL** using CentOS 7 as an example. If you want to integrate using other systems, refer to the [Try Out](#4-try-out) section, which introduces how to deploy a test integration environment using **Docker** and **Docker Compose**. For more information, refer to:

- [TiDB Documentation](https://docs.pingcap.com/)
- [TiDB Developer Guide](/develop/dev-guide-overview.md)
- [ProxySQL Documentation](https://proxysql.com/documentation/)
- [TiDB with ProxySQL Integration Test](https://github.com/Icemap/tidb-proxysql-integration-test)

## 1. Startup TiDB

### Test environment

<SimpleTab grouId="startup-tidb">

<div label="Source compilation" value="source-code">

1. Download [TiDB](https://github.com/pingcap/tidb) code, change to the `tidb-server` folder and run the `go build` command.

    ```shell
    git clone git@github.com:pingcap/tidb.git
    cd tidb/tidb-server
    go build
    ```

2. Use the configuration file [`tidb-config.toml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/tidb-config.toml) to start TiDB. The command is as follows:

    ```shell
    ${TIDB_SERVER_PATH} -config ./tidb-config.toml -store unistore -path "" -lease 0s > ${LOCAL_TIDB_LOG} 2>&1 &
    ```

> **Note:**
>
> - The preceding command uses `unistore` as the storage engine, which is a test storage engine in TiDB. Make sure you use it in test environment only.
> - `TIDB_SERVER_PATH`: the location of the binary compiled with `go build` in the preceding step. For example, if you execute the previous command under `/usr/local`, `TIDB_SERVER_PATH` is `/usr/local/tidb/tidb-server/tidb-server`.
> - `LOCAL_TIDB_LOG`: the log file path of TiDB.

</div>

<div label="TiUP" value="tiup">

[TiUP](/tiup/tiup-overview.md), as the package manager, makes it far easier to manage different cluster components in the TiDB ecosystem, such as TiDB, PD, and TiKV.

1. Install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Start TiDB in the test environment:

    ```shell
    tiup playground
    ```

</div>

<div label="TiDB Cloud" value="tidb-cloud">

You can refer to [Build a TiDB cluster in TiDB Cloud (Developer Tier)](/develop/dev-guide-build-cluster-in-cloud.md).

</div>

</SimpleTab>

### Production environment

<SimpleTab grouId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

It is recommended to use [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) directly when you need hosting TiDB services (for example, you cannot manage it yourself, or you need a cloud-native environment). To build a TiDB cluster in production environment, refer to [Create a TiDB cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster).

</div>

<div label="Deploy Locally" value="tiup">

The production environment is much more complex than the test environment. To deploy an on-premises production cluster, it is recommended to refer to [Deploy a TiDB cluster using TiUP](/production-deployment-using-tiup.md) and then deploy it based on hardware conditions.

</div>

</SimpleTab>

## 2. Startup ProxySQL

### Install by yum

1. Add the repository:

    ```shell
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. Install ProxySQL:

    ```shell
    yum install proxysql
    ```

3. Start ProxySQL:

    ```shell
    systemctl start proxysql
    ```

### Other ways

To install ProxySQL using other ways, refer to the [ProxySQL README](https://github.com/sysown/proxysql#installation) or the [ProxySQL installation documentation](https://proxysql.com/documentation/).

## 3. Configure ProxySQL

To use ProxySQL as a proxy for TiDB, you need to configure ProxySQL. The required configuration items are listed in the following sections. For more details about other configuration items, refer to the [ProxySQL official documentation](https://proxysql.com/documentation/).

### Simple introduction

ProxySQL uses a separate port for configuration management and another port for proxying. We call the entry point for configuration management **_ProxySQL Admin interface_** and the entry point for proxying **_ProxySQL MySQL Interface_**.

- **_ProxySQL Admin interface_**: It is possible to connect to the admin interface either using a user with `admin` privileges to read and write configuration or a user with `stats` privileges that can only read certain statistics (no read or write configuration). The default credentials are `admin:admin` and `stats:stats`, but for security reasons, it is possible to connect locally using the default credentials. To connect remotely a new user needs to configure it, and often it is named `radmin`.
- **_ProxySQL MySQL Interface_**: Used as a proxy to forward SQL to the configured service.

![proxysql config flow](/media/develop/proxysql_config_flow.png)

There are three layers in ProxySQL configuration: `runtime`, `memory`, and `disk`. You can change the configuration of the `memory` layer only. After changing the configuration, you can use `LOAD xxx TO runtime` to make the configuration effective, and/or you can use `SAVE xxx TO DISK` to save to the disk to prevent configuration loss.

![proxysql config layer](/media/develop/proxysql_config_layer.png)

### Configure TiDB Server

Add TiDB backend in ProxySQL, you can add multiple TiDB backends if you have more than one. Please do this at **_ProxySQL Admin interface_**:

```sql
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (0, '127.0.0.1', 4000);
LOAD mysql servers TO runtime;
SAVE mysql servers TO DISK;
```

Field Explanation:

- `hostgroup_id`: ProxySQL manages backend services by **hostgroup**, you can configure several services that need load balancing as the same hostgroup, so that ProxySQL will distribute SQL to these services evenly. And when you need to distinguish different backend services (such as read/write splitting scenario), you can configure them as different hostgroups.
- `hostname`: IP or domain of the backend service.
- `port`: The port of the backend service.

### Configure Proxy login user

Add a TiDB backend login user to ProxySQL. ProxySQL will allow this account to log in **_ProxySQL MySQL Interface_** and ProxySQL will use it to create a connection to TiDB, so make sure this account has the appropriate permissions in TiDB. Please do this at **_ProxySQL Admin interface_**:

```sql
INSERT INTO mysql_users(username, password, active, default_hostgroup, transaction_persistent) VALUES ('root', '', 1, 0, 1);
LOAD mysql users TO runtime;
SAVE mysql users TO DISK;
```

Field Explanation:

- `username`: username
- `password`: password
- `active`: `1` is active, `0` is inactive, only the `active = 1` user can log in.
- `default_hostgroup`: This user default **hostgroup**, where its traffic will be sent unless query rules route the traffic to a different hostgroup.
- `transaction_persistent`: A value of `1` indicates transaction persistence, i.e., when a connection opens a transaction using this user, then until the transaction is committed or rolled back. All statements are routed to the same **hostgroup**.

### Configure by configure file

In addition to configuration using **_ProxySQL Admin interface_**, configuration files can also be used for configuration. In [Official Explanation](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file), the configuration file should only be considered as a secondary way of initialization and not as the primary way of configuration. The configuration file is only read when the SQLite database is not created and the configuration file will not continue to be read subsequently. Therefore, when using the configuration file, you should delete the SQLite database. It will **_LOSE_** the changes you made to the configuration in **_ProxySQL Admin interface_**:

```shell
rm /var/lib/proxysql/proxysql.db
```

Alternatively, it is also possible to run `LOAD xxx FROM CONFIG` to override the current in-memory configuration with the configuration on configuration file.

The configuration file is located at `/etc/proxysql.cnf`, we will translate the preceding required configuration to the configuration file way, only change `mysql_servers`, `mysql_users` two nodes, the rest of the configuration items can check `/etc/proxysql.cnf`:

```
mysql_servers =
(
    {
        address="127.0.0.1"
        port=4000
        hostgroup=0
        max_connections=2000
    }
)

mysql_users:
(
    {
        username = "root"
        password = ""
        default_hostgroup = 0
        max_connections = 1000
        default_schema = "test"
        active = 1
        transaction_persistent = 1
    }
)
```

Then use `systemctl restart proxysql` to restart the service and it will take effect. The SQLite database will be created automatically after the configuration file takes effect and the configuration file will not be read again.

### Other config items

The preceding config items are required. You can get all the config items' names and their roles in the [Global Variables](https://proxysql.com/documentation/global-variables/) article in the ProxySQL documentation.

## 4. Try out

You can use Docker and Docker Compose for quick start. Make sure the ports `4000` and `6033` are not allocated.

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test && docker-compose pull # Get the latest Docker images
sudo setenforce 0 # Only on Linux
docker-compose up -d
```

This has completed the startup of an integrated TiDB and ProxySQL environment, which will start two containers. **_DO NOT_** use it to create cluster in a production environment. You can connect to the port `6033` (ProxySQL) using the username `root` and an empty password. The container specific configuration can be found in [docker-compose.yaml](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/docker-compose.yaml) and the ProxySQL specific configuration can be found in [proxysql-docker.cnf](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/proxysql-docker.cnf).

Run the following command:

```shell
mysql -u root -h 127.0.0.1 -P 6033 -e "SELECT VERSION()"
```

The result is as follows:

```sql
+--------------------+
| VERSION()          |
+--------------------+
| 5.7.25-TiDB-v6.1.0 |
+--------------------+
```

## 5. Example

Dependencies:

- Docker
- Docker Compose
- MySQL Client

Clone and change to the example code repository:

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test
```

All subsequent examples use the `tidb-proxysql-integration-test` directory as the root directory.

### Example of load balancing: Admin Interface

Change to the sample directory:

```shell
cd example/load-balance-admin-interface
```

**Run with script**

Use **_ProxySQL Admin Interface_** to configure a load balancing traffic as an example. The script can be run using the following command:

```shell
./test-load-balance.sh
```

**Run step by step**

1. Start 3 TiDB containers through **Docker Compose**, all the  ports in the container are `4000`, and mapped to host ports `4001`, `4002`, `4003`. After the TiDB container instances are started, start one container of ProxySQL through **Docker Compose**, the port `6033` in the container is for **_ProxySQL MySQL Interface_**, and mapped host port 6034. The **_ProxySQL Admin Interface_** port is not exposed because it can only log in locally (i.e., inside the container). This process is written in [docker-compose.yaml](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/docker-compose.yaml).

    ```shell
    docker-compose up -d
    ```

2. Within the 3 TiDB instances, create the same table structure but write different data: `'tidb-0'`, `'tidb-1'`, `'tidb-2'`, in order to distinguish between the different database instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF

    mysql -u root -h 127.0.0.1 -P 4003 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-2');
    EOF
    ```

3. Use the `docker-compose exec` command to run the prepared [SQL file](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/proxysql-prepare.sql) for configuring ProxySQL in **_ProxySQL Admin Interface_**:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    This SQL file will run:

    1. Add 3 TiDB backend hosts with `hostgroup_id` of `0`.
    2. Take effect the TiDB backend configuration and save it on disk.
    3. Add user `root` with an empty password and `default_hostgroup` as `0`, corresponding to the preceding TiDB backend `hostgroup_id`.
    4. Take effect the user configuration and save it on disk.

4. Log in to **_ProxySQL MySQL Interface_** with the `root` user and query 5 times, expecting three different returns: `'tidb-0'`, `'tidb-1'` and `'tidb-2'`.

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -t << EOF
    select * from test.test;
    select * from test.test;
    select * from test.test;
    select * from test.test;
    select * from test.test;
    EOF
    ```

5. Stop and clear Docker Compose started resources, such as: containers and network topologies.

    ```shell
    docker-compose down
    ```

**Expect Output**

Because of load balancing, it is expected that the output will have three different results: `'tidb-0'`, `'tidb-1'`, and `'tidb-2'`. But the exact order cannot be expected. One of the expected outputs is:

```
# ./test-load-balance.sh 
Creating network "load-balance-admin-interface_default" with the default driver
Creating load-balance-admin-interface_tidb-1_1 ... done
Creating load-balance-admin-interface_tidb-2_1 ... done
Creating load-balance-admin-interface_tidb-0_1 ... done
Creating load-balance-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-2 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping load-balance-admin-interface_proxysql_1 ... done
Stopping load-balance-admin-interface_tidb-0_1   ... done
Stopping load-balance-admin-interface_tidb-2_1   ... done
Stopping load-balance-admin-interface_tidb-1_1   ... done
Removing load-balance-admin-interface_proxysql_1 ... done
Removing load-balance-admin-interface_tidb-0_1   ... done
Removing load-balance-admin-interface_tidb-2_1   ... done
Removing load-balance-admin-interface_tidb-1_1   ... done
Removing network load-balance-admin-interface_default
```

### Example of user split: Admin Interface

Change to the sample directory:

```shell
cd example/user-split-admin-interface
```

**Run with script**

Use **_ProxySQL Admin Interface_** to configure a user split traffic as an example. The different users will use their own TiDB backend. The script can be run using the following command:

```shell
./test-user-split.sh
```

**Run step by step**

1. Start 2 TiDB containers through **Docker Compose**,  all the ports in the container are `4000`, and mapped to host ports `4001` and `4002`. After the TiDB container instances are started, start one container of ProxySQL through **Docker Compose**, the port `6033` in the container is for **_ProxySQL MySQL Interface_**, and mapped host port 6034. The **_ProxySQL Admin Interface_** port is not exposed because it can only log in locally (i.e., inside the container). This process is written in [docker-compose.yaml](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/docker-compose.yaml).

    ```shell
    docker-compose up -d
    ```

2. Within the 2 TiDB instances, create the same table structure but write different data: `'tidb-0'`, `'tidb-1'`, in order to distinguish between the different database instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. Create a new user for ProxySQL in the `tidb-1` instance:

    ```shell
    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    CREATE USER 'root1' IDENTIFIED BY '';
    GRANT ALL PRIVILEGES ON *.* TO 'root1'@'%';
    FLUSH PRIVILEGES;
    EOF
    ```

4. Use the `docker-compose exec` command to run the prepared [SQL file](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/proxysql-prepare.sql) for configuring ProxySQL in **_ProxySQL Admin Interface_**:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    This SQL file will run:

    1. Add 2 TiDB backend hosts. `hostgroup_id` of `tidb-0` is `0`, and `hostgroup_id` of `tidb-1` is `1`.
    2. Take effect the TiDB backend configuration and save it on disk.
    3. Add user `root` with an empty password and `default_hostgroup` as `0`. It means that the SQL will default route to `tidb-0`.
    4. Add user `root1` with an empty password and `default_hostgroup` as `1`. It means that the SQL will default route to `tidb-1`.
    5. Take effect the user configuration and save it on disk.

5. Log in to **_ProxySQL MySQL Interface_** with the `root` user and `root1` user. The expected return is `'tidb-0'` and `'tidb-1'`.

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -e "select * from test.test;"
    mysql -u root1 -h 127.0.0.1 -P 6034 -e "select * from test.test;"
    ```

6. Stop and clear Docker Compose started resources, such as: containers and network topologies.

    ```shell
    docker-compose down
    ```

**Expect Output**

```
# ./test-user-split.sh 
Creating network "user-split-admin-interface_default" with the default driver
Creating user-split-admin-interface_tidb-1_1 ... done
Creating user-split-admin-interface_tidb-0_1 ... done
Creating user-split-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping user-split-admin-interface_proxysql_1 ... done
Stopping user-split-admin-interface_tidb-0_1   ... done
Stopping user-split-admin-interface_tidb-1_1   ... done
Removing user-split-admin-interface_proxysql_1 ... done
Removing user-split-admin-interface_tidb-0_1   ... done
Removing user-split-admin-interface_tidb-1_1   ... done
Removing network user-split-admin-interface_default
```

### Example of proxy rules: Admin Interface

Change to the sample directory:

```shell
cd example/proxy-rule-admin-interface
```

**Run with script**

Use **_ProxySQL Admin Interface_** to configure a common read/write separation traffic as an example. It will use the rules to match the SQL that will be run, thus forwarding the read and write SQL to different TiDB backends (if neither match, the user's `default_hostgroup` will be used).  The script can be run using the following command:

```shell
./proxy-rule-split.sh
```

**Run step by step**

1. Start 2 TiDB containers through **Docker Compose**, all the ports in the container are `4000`, and mapped to host ports `4001` and `4002`. After the TiDB container instances are started, start one container of ProxySQL through **Docker Compose**, the port `6033` in the container is for **_ProxySQL MySQL Interface_**, and mapped host port 6034. The **_ProxySQL Admin Interface_** port is not exposed because it can only log in locally (i.e., inside the container). This process is written in [docker-compose.yaml](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/docker-compose.yaml).

    ```shell
    docker-compose up -d
    ```

2. Within the 2 TiDB instances, create the same table structure but write different data: `'tidb-0'`, `'tidb-1'`, in order to distinguish between the different database instances. The command to write data to one of the TiDB instances is shown here, and the same for the other one instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. Use the `docker-compose exec` command to run the prepared [SQL file](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/proxysql-prepare.sql) for configuring ProxySQL in **_ProxySQL Admin Interface_**:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    This SQL file will run:

    1. Add 2 TiDB backend hosts. `hostgroup_id` of `tidb-0` is `0`, and `hostgroup_id` of `tidb-1` is `1`.
    2. Take effect the TiDB backend configuration and save it on disk.
    3. Add user `root` with an empty password and `default_hostgroup` as `0`. It means that the SQL will default route to `tidb-0`.
    4. Take effect the user configuration and save it on disk.
    5. Add the rule `^SELECT.*FOR UPDATE$` with `rule_id` as `1` and `destination_hostgroup` as `0`. It means if SQL statements match this rule, it will be using the TiDB with `hostgroup` as `0` (this rule is for forwarding `SELECT ... FOR UPDATE` statement to the database where it is written).
    6. Add the rule `^SELECT` with `rule_id` as `2` and `destination_hostgroup` as `1`. It means if SQL statements match this rule, it will be using the TiDB with `hostgroup` as `1`.
    7. Take effect the rule configuration and save it on disk.

    > **Note:**
    >
    > About the matching rules:
    >
    > - ProxySQL will try to match the rules one by one in the order of `rule_id` from smallest to largest.
    > - `^` matches the beginning of the SQL statement, `$` matches the end.
    > - `match_digest` is to match the parameterized SQL statement, see [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex).
    > - Important parameters:
    >
    >     - `digest`: Match the parameterized hash value.
    >     - `match_pattern`: Match the raw SQL statements.
    >     - `negate_match_pattern`: When value is `1`, inverse the match for `match_digest` or `match_pattern`.
    >     - `log`: Whether log the query.
    >     - `replace_pattern`: If it is not empty, the value of this field will be replaced by the content of the matched part of SQL.
    >
    > - See [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules) for full parameters.

4. Log in to **_ProxySQL MySQL Interface_** with the `root`:

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034
    ```

    The following statements can be run after login:

    - `SELECT` statement:

        ```sql
        SELECT * FROM test.test;
        ```

        Expect to match rules with `rule_id` of `2`. Forwarded to the TiDB backend `tidb-1` with `hostgroup` of `1`.

    - `SELECT ... FOR UPDATE` statement:

        ```sql
        SELECT * FROM test.test for UPDATE;
        ```

        Expect to match rules with `rule_id` of `1`. Forwarded to the TiDB backend `tidb-0` with `hostgroup` of `0`.

    - Transaction:

        ```sql
        BEGIN;
        INSERT INTO test.test (db) VALUES ('insert this and rollback later');
        SELECT * FROM test.test;
        ROLLBACK;
        ```

        The `INSERT` statement is expected to not match all rules. It will use the `default_hostgroup` of the user (It is `0`) and thus forward to the TiDB backend `tidb-0`(`hostgroup` is `0`). And ProxySQL turns on user `transaction_persistent` by default, this will cause all statements within the same transaction to run in the same `hostgroup`. So `SELECT * FROM test.test;` will also be forwarded to the TiDB backend `tidb-0`(`hostgroup` is `0`).

5. Stop and clear Docker Compose started resources, such as: containers and network topologies.

    ```shell
    docker-compose down
    ```

**Expect Output**

```
# ./proxy-rule-split.sh
Creating network "proxy-rule-admin-interface_default" with the default driver
Creating proxy-rule-admin-interface_tidb-1_1 ... done
Creating proxy-rule-admin-interface_tidb-0_1 ... done
Creating proxy-rule-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------------------------------+
| db                             |
+--------------------------------+
| tidb-0                         |
| insert this and rollback later |
+--------------------------------+
Stopping proxy-rule-admin-interface_proxysql_1 ... done
Stopping proxy-rule-admin-interface_tidb-0_1   ... done
Stopping proxy-rule-admin-interface_tidb-1_1   ... done
Removing proxy-rule-admin-interface_proxysql_1 ... done
Removing proxy-rule-admin-interface_tidb-0_1   ... done
Removing proxy-rule-admin-interface_tidb-1_1   ... done
Removing network proxy-rule-admin-interface_default
```

### Example of load balancing: Configuration File

Use configuration file to configure a load balancing traffic as an example. Achieves the same as [Example of Load Balancing - Admin Interface](#example-of-load-balancing-admin-interface), only changed using configuration file to initializing the ProxySQL configuration.

> **Note:**
>
> - The configuration of ProxySQL is stored in SQLite. Configuration file is only read when SQLite database does not exist.
> - ProxySQL does **NOT** recommend using configuration file for configuration changes, use them only for initial configuration, do not rely too much on configuration files.

**Run**

```shell
cd example/load-balance-config-file
./test-load-balance.sh
```