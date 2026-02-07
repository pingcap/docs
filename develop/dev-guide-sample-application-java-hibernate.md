---
title: Connect to TiDB with Hibernate
summary: Learn how to connect to TiDB using Hibernate. This tutorial gives Java sample code snippets that work with TiDB using Hibernate.
aliases: ['/tidb/stable/dev-guide-sample-application-java-hibernate/','/tidb/dev/dev-guide-sample-application-java-hibernate/','/tidbcloud/dev-guide-sample-application-java-hibernate/']
---

# Connect to TiDB with Hibernate

TiDB is a MySQL-compatible database, and [Hibernate](https://hibernate.org/orm/) is a popular open-source Java ORM. Because TiDB is highly compatible with MySQL, it is recommended that you use `org.hibernate.dialect.MySQLDialect` as the Hibernate dialect for long-term compatibility. Alternatively, a TiDB-specific dialect (`org.hibernate.community.dialect.TiDBDialect`) is available in [Hibernate community dialects](https://github.com/hibernate/hibernate-orm/tree/main/hibernate-community-dialects), but it is not maintained by PingCAP. If you use `MySQLDialect` and encounter any compatibility issues, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

In this tutorial, you can learn how to use TiDB and Hibernate to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Hibernate.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note:**
>
> This tutorial works with {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated, and TiDB Self-Managed.

## Prerequisites

To complete this tutorial, you need:

- **Java Development Kit (JDK) 17** or higher. You can choose [OpenJDK](https://openjdk.org/) or [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/) based on your business and personal requirements.
- [Maven](https://maven.apache.org/install.html) **3.8** or higher.
- [Git](https://git-scm.com/downloads).
- A TiDB cluster.

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-java-hibernate-quickstart.git
cd tidb-java-hibernate-quickstart
```

### Step 2: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

6. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

    {{{ .starter }}} requires a secure connection. Therefore, you need to set the value of `USE_SSL` to `true`.

7. Save the `env.sh` file.

</div>
<div label="TiDB Cloud Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **Public** from the **Connection Type** drop-down list, and then click **CA cert** to download the CA certificate.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) to configure it before your first connection.

    In addition to the **Public** connection type, TiDB Cloud Dedicated supports **Private Endpoint** and **VPC Peering** connection types. For more information, see [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster).

4. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

5. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

6. Save the `env.sh` file.

</div>
<div label="TiDB Self-Managed" value="tidb">

1. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

2. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters, and set `USE_SSL` to `false`. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `env.sh` file.

</div>
</SimpleTab>

### Step 3: Run the code and check the result

1. Execute the following command to run the sample code:

    ```shell
    make
    ```

2. Check the [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-hibernate-quickstart/blob/main/Expected-Output.txt) to see if the output matches.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-java-hibernate-quickstart](https://github.com/tidb-samples/tidb-java-hibernate-quickstart) repository.

### Connect to TiDB

Edit the Hibernate configuration file `hibernate.cfg.xml`:

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.MySQLDialect</property>
        <property name="hibernate.connection.url">${tidb_jdbc_url}</property>
        <property name="hibernate.connection.username">${tidb_user}</property>
        <property name="hibernate.connection.password">${tidb_password}</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

Be sure to replace `${tidb_jdbc_url}`, `${tidb_user}`, and `${tidb_password}` with the actual values of your TiDB cluster. Then, define the following function:

```java
public SessionFactory getSessionFactory() {
    return new Configuration()
            .configure("hibernate.cfg.xml")
            .addAnnotatedClass(${your_entity_class})
            .buildSessionFactory();
}
```

When using this function, you need to replace `${your_entity_class}` with your own data entity class. For multiple entity classes, you need to add a `.addAnnotatedClass(${your_entity_class})` statement for each. The preceding function is just one way to configure Hibernate. If you encounter any issues in the configuration or want to learn more about Hibernate, refer to the [Hibernate official documentation](https://hibernate.org/orm/documentation).

### Insert or update data

```java
try (Session session = sessionFactory.openSession()) {
    session.persist(new PlayerBean("id", 1, 1));
}
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md) and [Update data](/develop/dev-guide-update-data.md).

### Query data

```java
try (Session session = sessionFactory.openSession()) {
    PlayerBean player = session.get(PlayerBean.class, "id");
    System.out.println(player);
}
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Delete data

```java
try (Session session = sessionFactory.openSession()) {
    session.remove(new PlayerBean("id", 1, 1));
}
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Compatibility with `MySQLDialect`

When you use `MySQLDialect` with TiDB, be aware of the following behaviors:

### `SERIALIZABLE` isolation level

Applications that attempt to set the `SERIALIZABLE` transaction isolation level will encounter the following error in TiDB:

```
The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

To avoid this error, set the following TiDB system variable on the server side:

```sql
SET GLOBAL tidb_skip_isolation_level_check=1;
```

After this variable is enabled, TiDB accepts requests that specify `SERIALIZABLE` without returning an error. Internally, TiDB still uses `REPEATABLE-READ`, which is its strongest isolation level. For more information, see [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check).

> **Note:**
>
> The community-maintained `TiDBDialect` handles this behavior automatically by skipping features that require the `SERIALIZABLE` isolation level.

### `CHECK` constraints

Hibernate's [`@Check`](https://docs.hibernate.org/orm/6.5/javadocs/org/hibernate/annotations/Check.html) annotation generates DDL `CHECK` constraints. [MySQL 8.0.16 and later verions](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html) enforces these constraints by default, but TiDB does not enforce them unless explicitly enabled.

To enable `CHECK` constraint enforcement in TiDB, set the following system variable:

```sql
SET GLOBAL tidb_enable_check_constraint=ON;
```

Without this setting, TiDB accepts the `CHECK` constraint syntax but does not enforce it, which might lead to unexpected data integrity issues. For more information, see [`CHECK` constraints](/constraints.md#check).

## Next steps

- Learn more usage of Hibernate from [the documentation of Hibernate](https://hibernate.org/orm/documentation).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](https://docs.pingcap.com/developer/), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.
- Learn through the course for Java developers: [Working with TiDB from Java](https://eng.edu.pingcap.com/catalog/info/id:212).

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
