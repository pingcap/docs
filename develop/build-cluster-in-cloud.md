---
title: Build a TiDB Cluster in TiDB Cloud (DevTier)
summary: Build a TiDB Cluster in TiDB Cloud (DevTier) and connect to a TiDB Cloud cluster.
---

<!-- markdownlint-disable MD029 -->

# Build a TiDB Cluster in TiDB Cloud (DevTier)

This page will guide you on the fastest way to get started with TiDB. You will use TiDB Cloud to create and launch a free TiDB cluster, and insert data using the TiDB SQL client. Then the data will be read from the sample program.

If you need to start TiDB on your local machine, see [Starting TiDB Locally](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb).

## Step 1. Create a free cluster

1. If you do not already have a TiDB Cloud account, register [TiDB Cloud](https://tidbcloud.com/signup) first
2. [Sign in](https://tidbcloud.com/) with your TiDB Cloud account
3. Choose a Developer Tier plan for one year free at [plans](https://tidbcloud.com/console/plans), or go directly to the **Create a Cluster (Dev Tier)** page by clicking [Create a Cluster (Dev Tier)](https://tidbcloud.com/console/create-cluster?tier=dev).
4. Please fill in the cluster name / password / cloud service provider (for now, only AWS is available) / availability zone (nearby is recommended) on the **Create a Cluster (Dev Tier)** page and then click the **Create** button to create the cluster.
5. Wait for a while. After 5-15 minutes, the creation will be completed. You can check the creation progress at [Active Clusters](https://tidbcloud.com/console/clusters).
6. After creation, on the **Active Clusters** page, click the cluster name to enter the cluster control panel

    ![active clusters](/media/develop/IMG_20220331-232643794.png)

7. Click **Connect** to create a traffic filter (list of client IPs allowed to connect)

    ![connect](/media/develop/IMG_20220331-232726165.png)

8. Click **Add Your Current IP Address** in the popup window. We will be filled in by your current network IP. Click **Create Filter** to create a traffic filter.
9. Copy the connection string from the popup window **Step 2: Connect with a SQL client** for the next step.

    ![SQL string](/media/develop/IMG_20220331-232800929.png)

## Step 2. Connect to a cluster

1. If the MySQL client is not installed, select your operating system and follow the steps below to install

<SimpleTab>

<div label="macOS">

If you don't have homebrew, please move to the [brew official website](https://brew.sh/index) to install

{{< copyable "shell-regular" >}}

```shell
brew install mysql-client
```

In the command line output of the installation, you get the following information:

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

Run this line (if the command line output is inconsistent with the documentation here, please refer to the command line output):

{{< copyable "shell-regular" >}}

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

Once done, take the configuration file into effect (for example `~/.zshrc`) and verify that the MySQL client is installed successfully:

{{< copyable "shell-regular" >}}

```shell
source ~/.zshrc
mysql --version
```

Expect output similar to the following:

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

Take CentOS7 as an example:

{{< copyable "shell-regular" >}}

```shell
yum install mysql
```

Once done, verify that the MySQL client is installed successfully:

{{< copyable "shell-regular" >}}

```shell
mysql --version
```

Expect output similar to the following:

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. Run the connection string obtained in [step 1](#step-1-create-a-free-cluster).

{{< copyable "shell-regular" >}}

```shell
mysql --connect-timeout 15 -u root -h <host> -P 4000 -p
```

3. Fill in the password to complete the sign in.

## Step 3. Run the sample application

1. Clone the tidb-example-java project

{{< copyable "shell-regular" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

2. Change connection parameters

<SimpleTab>

<div label="Local default cluster">

No changes required

</div>

<div label="Non-local default cluster, TiDB Cloud, or other remote cluster">

Change the parameters for Host / Post / User / Password in plain-java-jdbc/src/main/java/com/pingcap/JDBCExample.java:

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

If the password you set is `123456`, the connection string you get in TiDB Cloud is:

{{< copyable "" >}}

```java
mysql --connect-timeout 15 -u root -h tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com -P 4000 -p
```

Then here you should change the parameter to:

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("123456");
```

</div>

</SimpleTab>

3. Run `make plain-java-jdbc`

The output should be as [expected](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc).