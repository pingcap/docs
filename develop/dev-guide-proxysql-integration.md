---
title: ProxySQL Integration Guide
summary:  Learn how to integrate TiDB Cloud and TiDB (self-hosted)  with ProxySQL
---

# ProxySQL Integration Guide

## Integrate TiDB with ProxySQL

This document provides a high-level introduction to ProxySQL, describes how to [integrate ProxySQL with TiDB](#option-1---integrate-tidb-serverless-with-proxysql), and demonstrates the key integration benefits through some [typical scenarios](#typical-scenarios).
Meanwhile, if you are interested in learning more about TiDB and ProxySQL, you can find some useful links as follows:

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/select-cluster-tier)
- [TiDB Developer Guide](/develop/dev-guide-overview.md)
- [ProxySQL Documentation](https://proxysql.com/documentation/)

## What is ProxySQL?

[ProxySQL](https://proxysql.com/) is a high-performance, open-source SQL proxy. It has a flexible architecture and can be deployed in several different ways, making it ideal for a variety of use cases. For example, ProxySQL can be used to improve performance by caching frequently-accessed data, or to scale out MySQL reads by load-balancing traffic across multiple servers.
ProxySQL is designed from the ground up to be fast, efficient, and easy to use. It is fully compatible with MySQL, and supports all of the features you would expect from a high-end SQL proxy. In addition, ProxySQL comes with a number of unique features that make it an ideal choice for a wide range of applications.

## Why ProxySQL integration?

- ProxySQL can help boost application performance by reducing latency when interacting with TiDB.  Irrespective of what you are building, whether it is a scalable application using serverless functions like Lambda, where the workload is nondeterministic and can spike, or if you are building an application to execute queries that load tons of data. By leveraging powerful capabilities of ProxySQL such as [connection pooling](https://proxysql.com/documentation/detailed-answers-on-faq/), [load-balancing](https://proxysql.com/documentation/ProxySQL-Configuration/), and [caching](https://proxysql.com/documentation/query-cache/) frequently-used queries, applications can gain immediate benefits.
- ProxySQL can act as an additional layer of application security protection against SQL vulnerabilities such as SQL Injection with the help of [Query Rules](#query-rules), an easy-to-configure feature available in ProxySQL.
- You can get the benefits of zero vendor lock-in as both [ProxySQL](https://github.com/sysown/proxysql) and [TiDB](https://github.com/pingcap/tidb) are open-source projects.

## Deployment architecture

While the most obvious way to deploy ProxySQL with TiDB would be to add ProxySQL as an as a standalone intermediary between Application layer and TiDB Cluster, this may work but may not be a scalable solution. In addition to this, it may end up being a single point of failure and also add additional latency due to network hop.  To overcome this kind of challenge, an alternate method of this deployment architecture may involve deploying ProxySQL as a side car as illustrated below:

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **Note:**
>
> The above illustration is only for reference purposes. You must adapt it according to your current deployment architecture.

## Development environment

This section describes how to integrate TiDB with ProxySQL in a development environment.
To get started with the ProxySQL integration, you can choose either of the following options depending on your TiDB cluster type after you have all the required [prerequisites](#prerequisite) in place.

- [Option 1 - Integrate TiDB Serverless with ProxySQL](#option-1---integrate-tidb-serverless-with-proxysql)
- [Option 2 - Integrate TiDB (self-hosted) with ProxySQL](#option-2---integrate-tidb-self-hosted-with-proxysql)

### Prerequisite

Depending on the option you choose, you might proceed with downloading and installing the prerequisite using the following links:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [python3](https://www.python.org/downloads/)
- [Docker Compose](https://docker-docs.netlify.app/compose/install/)
- [mysql client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

Alternatively, you can also follow the installation instructions below:

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

- Download and start `Docker` manually (the Docker desktop already includes the docker-compose).
- Run the command below to install `python` and `mysql-client`:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python mysql-client
    ```

</div>

<div label="CentOS" value="CentOS">

```bash
curl -fsSL https://get.docker.com | bash -s docker
yum install -y git python39 docker-ce docker-ce-cli containerd.io docker-compose-plugin mysql
systemctl start docker
```

</div>

<div label="Windows" value="Windows">

1. Download and install Git.

    1. Download the 64-bit Git for Windows Setup package from the Git Windows Download page.
    2. Install the Git package by following the setup wizard. You can click Next for a few times to use the default installation settings.

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

2. Download and install MySQL Shell.

    1. Download the ZIP file of MySQL Installer from the [MySQL Community Server Download](https://dev.mysql.com/downloads/mysql/) page.
    2. Unzip the file, and locate `mysql.exe` in the bin folder. You need to add the path of the bin folder to the System Variable and set it into the `Path` variable at Git Bush:

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        For example:

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

3. Download and install Docker.

    1. Download Docker Deskstop Installer from the [Docker Download](https://www.docker.com/products/docker-desktop/) page.
    2. Double-click the installer to run it. After the installation is completed, you will be prompted for a restart.

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

4. Download the latest Python 3 version from the [Python Download](https://www.python.org/downloads/) page and install it.

</div>

</SimpleTab>

### Option 1 -  Integrate TiDB Serverless with ProxySQL

For this integration, you will be using the [ProxySQL Docker Image](https://hub.docker.com/r/proxysql/proxysql) along with TiDB Serverless Tier cluster.  In the following steps, we will be setting up ProxySQL on port `16033`, so make sure this port is not in use and is available.

#### Step 1. Create a TiDB Cloud Serverless Tier cluster

1. [Create a free TiDB Serverless Tier cluster](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster). Remember the root password that you set for your cluster.
2. Get your cluster hostname, username, and port for later use.

    1. On the [Clusters page](https://tidbcloud.com/console/clusters), click your cluster name to go to the cluster overview page.
    2. On the cluster overview page,  locate the **Connection** pane, and then copy the `Endpoint`, `Port`, and `User` information, where the `Endpoint` is your cluster hostname.

#### Step 2. Prepare ProxySQL configuration files

1. Clone the [integration example code repository](https://github.com/pingcap-inc/tidb-proxysql-integration) for TiDB and ProxySQL:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

2. Navigate to `tidb-cloud-connect` folder:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    </SimpleTab>

3. Generate the ProxySQL configuration files by running `proxysql-config.py`:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-config.py
    ```

    </div>

    </SimpleTab>

When prompted, enter the endpoint of your cluster for `Serverless Tier Host`,  and then enter the username and the password of your cluster.
The following is an example output. You will see that three configuration files are generated inside the current `tidb-cloud-connect` folder.

```
[Begin] generating configuration files..
tidb-cloud-connect.cnf generated successfully.
proxysql-prepare.sql generated successfully.
proxysql-connect.py generated successfully.
[End] all files generated successfully and placed in the current folder.
```

#### Step 3. Configure ProxySQL

1. Start Docker. If Docker has already started, skip this step:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    Double-click the icon of the installed Docker to start it.

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    Double-click the icon of the installed Docker to start it.

    </div>

    </SimpleTab>

2. Pull down the ProxySQL Docker image and start a ProxySQL container:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

3. Integrate with ProxySQL by running the following command, which will execute `proxysql-prepare.sql` inside **ProxySQL Admin Interface**:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    </SimpleTab>

> **Note:**
>
> The proxysql-prepare.sql script does the following:
>
> 1. Add  a user using the username and password of your cluster.
> 2. Assigns the user to the monitoring account.
> 3. Add your TiDB Serverless Tier cluster to the list of hosts.
> 4. Enables a secure connection between ProxySQL and TiDB Serverless.
>
> To have a better understanding, it is strongly recommended that you review the proxysql-prepare.sql file. To learn more about ProxySQL configuration, see [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/).

The following is an example output. You will see that the hostname of your cluster is shown in the output, which means that the connectivity between ProxySQL and the TiDB Serverless Tier cluster is established.

```
*************************** 1. row ***************************
       hostgroup_id: 0
           hostname: gateway01.us-west-2.prod.aws.tidbcloud.com
               port: 4000
          gtid_port: 0
             status: ONLINE
             weight: 1
        compression: 0
    max_connections: 1000
max_replication_lag: 0
            use_ssl: 1
     max_latency_ms: 0
            comment: 
```

#### Step 4. Connect to your TiDB cluster through ProxySQL

1. Run proxysql-connect.py in a Terminal. The script will automatically launch the mysql client and use your `serverless tier username` and `root password` for login.

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-connect.py
    ```

    </div>

    </SimpleTab>

2. After logging into your TiDB cluster, you can use the following SQL statement to validate the connection:

    ```sql
    SELECT VERSION();
    ```

    If the TiDB version information is displayed, you are successfully connected to your TiDB serverless through ProxySQL. To exit from the mysql client anytime, enter quit and press enter.

    > **Note:**
    >
    > ***For Debugging:*** If you are unable to connect to the cluster, review the files `tidb-cloud-connect.cnf`, `proxysql-prepare.sql`, and `proxysql-connect.py`. Make sure that the server information you provided is available and correct.

3. To stop and remove containers, and jump out to the previous folder, run the following command:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

### Option 2 -  Integrate TiDB (self-hosted) with ProxySQL

For this integration, we will set up an environment using docker for [TiDB](https://hub.docker.com/r/pingcap/tidb) and [ProxySQL](https://hub.docker.com/r/proxysql/proxysql).
You are encouraged to try [other ways of installing TiDB server](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb) in your own interest.
The following steps will set up ProxySQL and TiDB server on ports `6033` and `4000`, so make sure these ports are not in use and are available.

1. Start Docker. If Docker has already started, skip this step:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    Double-click the icon of the installed Docker to start it.

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    Double-click the icon of the installed Docker to start it.

    </div>

    </SimpleTab>

2. Clone the [integration example code repository](https://github.com/pingcap-inc/tidb-proxysql-integration) for TiDB and ProxySQL:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

3. Pull down the latest Docker images of ProxySQL and TiDB:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    </SimpleTab>

4. Start an integrated environment using both TiDB and ProxySQL running as containers:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

    To log in to the ProxySQL `6033` port, you can use the `root` username with an empty password.

5. Connect to TiDB via ProxySQL:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    </SimpleTab>

6. After logging into your TiDB cluster, you can use the following SQL statement to validate the connection:

    ```sql
    SELECT VERSION();
    ```

    If the TiDB version information is displayed, you are successfully connected to your TiDB container instances through ProxySQL.

7. To stop and remove containers, and jump out to the previous folder, run the following command:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

## Production environment

For a production environment, this section of the documentation recommends you use [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) directly for a fully managed experience.

### Prerequisite

- Download and install a MySQL client. For example, [MySQL Shell](https://dev.mysql.com/downloads/shell/).

### Integrate TiDB Cluster with ProxySQL on CentOS

ProxySQL can be installed on many different platforms. The document takes CentOS as an example.
For a full list of supported platforms and the corresponding version requirements, see [ProxySQL documentation](https://proxysql.com/documentation/installing-proxysql/).

#### Step 1. Create a TiDB Cloud Dedicated Tier cluster

For detailed steps, see [Create a TiDB Cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster).

#### Step 2. Install ProxySQL

1. Add ProxySQL to the YUM repository:

    ```bash
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. Install ProxySQL:

    ```bash
    yum install -y proxysql
    ```

3. Start ProxySQL:

    ```bash
    systemctl start proxysql
    ```

To learn more about the supported platforms of ProxySQL and their installation, refer to [ProxySQL README](https://github.com/sysown/proxysql#installation) or [ProxySQL installation documentation](https://proxysql.com/documentation/installing-proxysql/).

#### Step 3. Configure ProxySQL

To use ProxySQL as a proxy for TiDB, you need to configure ProxySQL. To do so, you can either execute SQL statements inside ProxySQL Admin Interface (recommended) or use the [configuration file](#option-2-configure-proxysql-using-a-configuration-file).

> **Note:**
>
> The following sections list only the required configuration items.
> For a comprehensive list of configurations, see [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/).

##### Option 1: Configuring ProxySQL using the Admin Interface

1. Reconfigure ProxySQL’s internals using the standard ProxySQL the Admin interface, accessible via any MySQL command line client (available by default on port `6032`):

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    The above step will take you to the ProxySQL admin prompt.

2. Configure the TiDB servers to be used, you can add one or multiple TiDB servers to ProxySQL. In this example we will be add TiDBCloud instance. Replace '*tidb cloud dedicated cluster host*' and '*tidb cloud dedicated cluster port*' with the actual TiDB cloud endpoint and port that's been configured( Default port is 4000)

    ```sql
    INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (0, '<tidb cloud dedicated cluster host>', <tidb cloud dedicated cluster port>);
    LOAD mysql servers TO runtime;
    SAVE mysql servers TO DISK;
    ```

    > **Note:**
    >
    > `hostgroup_id`: ProxySQL manages servers using hostgroup. To distribute SQL traffic to these servers evenly, you can configure several servers that need load balancing to the same hostgroup. To distinguish the servers, such as for read and write purposes, you can configure them to use different hostgroup.
    > `hostname`: The IP address or domain of the TiDB server.
    > `port`:  The port of TiDB server.

3. Configure Proxy login users to make sure that the users have appropriate permissions on the TiDB server. In the code below Replace '*tidb cloud dedicated cluster username*' and 'tidb cloud dedicated cluster password' with the cluster `username` and `password` that's been configured.

    ```sql
    INSERT INTO mysql_users(username, password, active, default_hostgroup, transaction_persistent) VALUES ('<tidb cloud dedicated cluster username>', '<tidb cloud dedicated cluster password>', 1, 0, 1);
    LOAD mysql users TO runtime;
    SAVE mysql users TO DISK;
    ```

    > **Note:**
    >
    > `username`: TiDB username.
    > `password`: TiDB password.
    > `active`: controls whether the user is active. `1` indicates that the user is **active** and can be used for login, while `0` indicates that the user is inactive.
    > `default_hostgroup`: the default hostgroup used by the user, where SQL traffic is distributed  unless the query rule overrides the traffic to a specific hostgroup.
    > `transaction_persistent`: `1` indicates persistent transaction. This is when the user starts a transaction within a connection, all query statements are routed to the same hostgroup until the transaction is committed or rolled back.

##### Option 2: Configure ProxySQL using a configuration file

This option should only be considered as an alternate method for configuring ProxySQL. For more information, see [Configuring ProxySQL through the config file](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file).

1. Delete any existing SQLite database (where configurations are stored internally):

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **Warning:**
    >
    > If you delete the SQLite database file, any configuration changes made using ProxySQL Admin interface will be lost.

2. Locate the configuration file in `/etc/proxysql.cnf` and modify it according to your need.

    For example:

    ```
    mysql_servers:
    (
        {
            address="<tidb cloud dedicated cluster host>"
            port=<tidb cloud dedicated cluster port>
            hostgroup=0
            max_connections=2000
        }
    )

    mysql_users:
    (
        {
            username = "<tidb cloud dedicated cluster username>"
            password = "<tidb cloud dedicated cluster password>"
            default_hostgroup = 0
            max_connections = 1000
            default_schema = "test"
            active = 1
            transaction_persistent = 1
        }
    )
    ```

    Replace:

    - `tidb cloud dedicated cluster host` with the actual TiDB Cloud `endpoint`
    - `tidb cloud dedicated cluster username` with TiDB Cloud `username`
    - `tidb cloud dedicated cluster password` with TiDB Cloud `password`

3. Restart ProxySQL:

    ```bash
    systemctl restart proxysql
    ```

    After the restart, the SQLite database will be created automatically.

> **Warning:**
>
> Do not run ProxySQL with default credentials in production. Before starting the `proxysql` service, you can change the defaults in the `/etc/proxysql.cnf` file by changing the admin_credentials variable.

## Typical scenarios

This section of the document discusses some of the benefits that we can leverage by integrating ProxySQL with TiDB Server, such as Loadbalancing and query routing with some examples.

For these examples, we will be using the docker version of TiDB and ProxySQL to configure load balancing, so if you have been following along, the assumption is that you already have a setup installed and running, if not, visit our [getting started section](#option-2---integrate-tidb-self-hosted-with-proxysql) to learn more.

### Query rules

Databases can be overloaded by high traffic, faulty code, or malicious spam. With ProxySQL's query rules, you can respond to these issues quickly and effectively by rerouting, rewriting, or rejecting queries.

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

1. Clone the [integration example code repository](https://github.com/pingcap-inc/tidb-proxysql-integration) for TiDB and ProxySQL. Skip this step if you have already cloned it in the previous steps.

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

2. Navigate to the example directory for ProxySQL rules:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    </SimpleTab>

3. Run the following command to start two Docker instances of TiDB server containers and a ProxySQL Docker instance:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

    If everything goes well, the following Docker instances are started:

    - Two Docker instances of TiDB server exposed via ports `4001`, `4002`
    - One ProxySQL Docker instance exposed via port `6034`.

4. In the two TiDB container instances, using `mysql client` to create a table with a similar schema definition and then insert different data (`'tidb-server01-port-4001'`, `'tidb-server02-port-4002'`) to identify these instances.

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
        mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
        mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    </SimpleTab>

5. Configure ProxySQL by running the following command, which will execute proxysql-prepare.sql inside ProxySQL Admin Interface to establish a proxy connection between the TiDB instances and ProxySQL.

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    </SimpleTab>

    > **Note:**
    >
    > The proxysql-prepare.sql does the following:
    >
    > - Adds the TiDB server instances in ProxySQL with `hostgroup_id` as `0` and `1`.
    > - Adds a user `root` with an empty password and sets `default_hostgroup` as `0`.
    > - Adds the rule `^SELECT.*FOR UPDATE$` with `rule_id` as `1` and `destination_hostgroup` as `0`. If a SQL statement matches this rule, the request will be   forwarded to the TiDB server with `hostgroup` as `0`.
    > - Adds the rule `^SELECT` with `rule_id` as `2` and `destination_hostgroup` as `1`. If SQL statements match this rule, it uses the TiDB server with `hostgroup` as `1`.
    >
    > To have a better understanding, it is strongly recommended that you review the proxysql-prepare.sql file. To learn more about ProxySQL configuration, see [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/).

    Here is some additional information about how ProxySQL patterns match query rules:

    - ProxySQL tries to match the rules one by one in the order of `rule_id` from smallest to largest.
    - `^` symbol matches the beginning of a SQL statement and `$` matches the end.

    For more information on ProxSQL regular expression and pattern matching, see [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex) in ProxySQL documentation.
    For a full list of parameters, see [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules) in ProxySQL documentation.

6. Verify the configuration and check whether the query rules work.

    1. Log into ProxySQL MySQL Interface as the `root` user:

        <SimpleTab groupId="os">

        <div label="macOS" value="macOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="CentOS" value="CentOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="Windows (Git Bash)" value="Windows">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        </SimpleTab>

    2. Execute the following SQL statements:

        - Execute a SELECT statement:

            ```sql
            SELECT * FROM test.tidb_server;
            ```

            This statement will match rule_id `2` and forward the statement to the TiDB server on `hostgroup 1`.

        - Execute a `SELECT ... FOR UPDATE` statement:

            ```sql
            SELECT * FROM test.tidb_server for UPDATE;
            ```

            This statement will match rule_id `1` and forward the statement to the TiDB server on `hostgroup 0`.

        - Start a transaction:

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            In this transaction, the `BEGIN` statement will not match any rules. It uses the default hostgroup (`hostgroup 0` in this example). Because ProxySQL enables user transaction_persistent by default, which will execute all statements within the same transaction in the same hostgroup, the `INSERT` and `SELECT * FROM test.tidb_server;` statements will also be forwarded to the TiDB server `hostgroup 0`.

        The following is an example output. If you get a similar output, you have successfully configured the query rules with ProxySQL.

        ```sql
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server02-port-4002 |
        +-------------------------+
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server01-port-4001 |
        +-------------------------+
        +--------------------------------+
        | server_name                    |
        +--------------------------------+
        | tidb-server01-port-4001        |
        | insert this and rollback later |
        +--------------------------------+
        ```

    3. To exit anytime, enter `quit` and press `enter`.

7. To stop and remove containers, and jump out to the previous folder, run the following command:

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>