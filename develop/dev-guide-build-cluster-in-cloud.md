---
title: Build a TiDB Cluster in TiDB Cloud
summary: Learn how to build a TiDB cluster in TiDB Cloud (Developer Tier) and connect to a TiDB Cloud cluster.
---

<!-- markdownlint-disable MD029 -->

# Build a TiDB cluster in TiDB Cloud (Developer Tier)

This document walks you through the quickest way to get started with TiDB. You will use [TiDB Cloud](https://en.pingcap.com/tidb-cloud) to create a free TiDB cluster, connect to it, and run a sample application on it.

<CustomContent platform="tidb">

If you need to run TiDB on your local machine, see [Starting TiDB Locally](/quick-start-with-tidb.md).

</CustomContent>

## Step 1. Create a free cluster

1. If you do not have a TiDB Cloud account, click [TiDB Cloud](https://tidbcloud.com/free-trial) to sign up for an account.
2. [Sign in](https://tidbcloud.com/) with your TiDB Cloud account.
3. To create a Developer Tier cluster for one year free, select the **Developer Tier** plan on the [plan page](https://tidbcloud.com/console/plans).
4. On the **Create Cluster** page, set up your cluster name, cloud provider (for now, only AWS is available for Developer Tier), and region (a nearby region is recommended). Then click **Create** to create your cluster.

   The cluster creation process starts and the **Security Quick Start** dialog box is displayed.

6. In the **Security Quick Start** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

    Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

7. After creating a cluster, on the **Active Clusters** page, click the name of your newly created cluster to navigate to the cluster control panel.

    ![active clusters](/media/develop/IMG_20220331-232643794.png)

7. Click **Connect** to create a traffic filter (a list of client IPs allowed for TiDB connection).

    ![connect](/media/develop/IMG_20220331-232726165.png)

8. In the popup window, locate **Step 2: Connect with a SQL client**, and then copy the string to connect with a SQL client for later use.

    ![SQL string](/media/develop/IMG_20220331-232800929.png)

    > **Note:**
    >
    > - For [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier), when you connect to your cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

## Step 2. Connect to a cluster

1. If the MySQL client is not installed, select your operating system and follow the steps below to install it.

<SimpleTab>

<div label="macOS">

For macOS, install [Homebrew](https://brew.sh/index) if you do not have it, and then run the following command to install the MySQL client:

{{< copyable "shell-regular" >}}

```shell
brew install mysql-client
```

The output is as follows:

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

To add the MySQL client to your PATH, locate the following command in the above output (if your output is inconsistent with the above output in the document, use the corresponding command in your output instead) and run it:

{{< copyable "shell-regular" >}}

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

Then, declare the global environment variable by the `source` command and verify that the MySQL client is installed successfully:

{{< copyable "shell-regular" >}}

```shell
source ~/.zshrc
mysql --version
```

An example of the expected output:

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

For Linux, the following takes CentOS 7 as an example:

{{< copyable "shell-regular" >}}

```shell
yum install mysql
```

Then, verify that the MySQL client is installed successfully:

{{< copyable "shell-regular" >}}

```shell
mysql --version
```

An example of the expected output:

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. Run the connection string obtained in [Step 1](#step-1-create-a-free-cluster).

{{< copyable "shell-regular" >}}

```shell
mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -p
```

3. Fill in the password to sign in.

## Step 3. Run the sample application

1. Clone the `tidb-example-java` project:

  {{< copyable "shell-regular" >}}

  ```shell
  git clone https://github.com/pingcap-inc/tidb-example-java.git
  ```

2. Change connection parameters.

  <SimpleTab>

  <div label="Local default cluster">

  No changes are required.

  </div>

  <div label="Non-local default cluster, TiDB Cloud, or other remote cluster">

  In `plain-java-jdbc/src/main/java/com/pingcap/JDBCExample.java`, modify the parameters of the host, port, user, and password:

  {{< copyable "" >}}

  ```java
  mysqlDataSource.setServerName("localhost");
  mysqlDataSource.setPortNumber(4000);
  mysqlDataSource.setDatabaseName("test");
  mysqlDataSource.setUser("<prefix>.root");
  mysqlDataSource.setPassword("");
  ```

  Suppose that the password you set is `123456` and the connection string you get from TiDB Cloud is the following:

  {{< copyable "" >}}

  ```shell
  mysql --connect-timeout 15 -u '<prefix>.root' -h xxx.tidbcloud.com -P 4000 -p
  ```

  In this case, you can modify the parameters as follows:

  {{< copyable "" >}}

  ```java
  mysqlDataSource.setServerName("xxx.tidbcloud.com");
  mysqlDataSource.setPortNumber(4000);
  mysqlDataSource.setDatabaseName("test");
  mysqlDataSource.setUser("<prefix>.root");
  mysqlDataSource.setPassword("123456");
  ```

  </div>

  </SimpleTab>

3. Run `make plain-java-jdbc`.

  Here is an example of the [expected output](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc).