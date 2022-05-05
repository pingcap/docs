---
title: Choose Driver or ORM
summary: Choose driver or ORM framework to connect to TiDB.
---

# Choose Driver or ORM

TiDB is compatible with MySQL's protocol, but some features are not compatible with MySQL, such as:

Unsupported features:

- Stored procedures and functions
- Triggers
- `FOREIGN KEY` constraints

Features that are different from MySQL:

- Auto-increment ID: In TiDB, auto-incremental columns are globally unique. They are incremental on a single TiDB server, but ***not*** necessarily incremental among multiple TiDB servers or allocated sequentially.

Full compatibility differences can be found at [MySQL Compatibility](https://docs.pingcap.com/tidb/stable/mysql-compatibility)

## Java

> Support levels
>
> - **Full**: Indicates that there are no known issues with this Driver or ORM
> - **Verified**: You may have errors due to TiDB compatibility issues

### Java Drivers

**JDBC**

Support level: **Full`

Follow the instructions in the [JDBC official documentation](https://dev.mysql.com/doc/connector-j/8.0/en/), download and configure the Java JDBC driver to use it.

> **Note:**
>
> Version `8.0.16` and above is strongly recommended, which fixes two CVEs:
>
> - *CVE-2019-2692 directly
> - *CVE-2021-22569 indirectly

For a complete example application, see [Build a Simple CRUD App with TiDB and JDBC](/develop/sample-application-java.md)

### Java ORM Framework

#### Hibernate

Support level: `Full`

> **Note:**
>
> Hibernate does [not support nested transactions](https://stackoverflow.com/questions/37927208/nested-transaction-in-spring-app-with-jpa-postgres) currently. And TiDB does [not support Savepoint](https://github.com/pingcap/tidb/issues/6840) in the current version. If you are using a framework such as `Spring Data JPA`, do not use the `Propagation.NESTED` transaction propagation option in `@Transactional`, i.e.: `@Transactional( propagation = Propagation.NESTED)`
>
> You can use [this example](https://github.com/Icemap/tidb-savepoint) to quickly reproduce the output of TiDB and MySQL for Savepoint.

> ```
> MySQL:
> id: 1, coins: 1, goods: 1
> id: 3, coins: 1, goods: 1
>
> TiDB:
> 
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960" 
> [1.119ms] [rows:0] SAVEPOINT sp0x102cf8960
> 
> 2022/04/02 13:59:48 /<path>/go/pkg/mod/gorm.io/driver/mysql@v1.3.2/mysql.go:397 Error 1064: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 9 near "SAVEPOINT sp0x102cf8960" 
> [0.001ms] [rows:0] SAVEPOINT sp0x102cf8a00
> id: 1, coins: 1, goods: 1
> ```

You can use [Gradle](https://gradle.org/install) or [Maven](https://maven.apache.org/install.html) to get all the dependencies of your application and will download all dependencies (including the indirect dependencies) for you, to avoid managing the complex dependencies manually. Note that the TiDB dialect is only supported in Hibernate `6.0.0.Beta2` and above.

If you are using **Maven**, please add the following to your `<dependencies></dependencies>`:

{{< copyable "" >}}

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.0.0.CR2</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.28</version>
</dependency>
```

If you are using **Gradle**, please add the following to your `dependencies`:

{{< copyable "" >}}

```gradle
implementation 'org.hibernate:hibernate-core:6.0.0.CR2'
implementation 'mysql:mysql-connector-java:8.0.28'
```

Example of building a TiDB application:

- Native Java using Hibernate, see [Build a Simple CRUD App with TiDB and Java](/develop/sample-application-java.md)
- Spring Data JPA / Hibernate, see [Build the TiDB Application using Spring Boot](/develop/sample-application-spring-boot.md)

In addition, you need to specify the TiDB dialect in your [Hibernate configuration file](https://www.tutorialspoint.com/hibernate/hibernate_configuration.htm): `org.hibernate.dialect.TiDBDialect`, which is only supported in Hibernate `6.0.0.Beta2` and above. If you are unable to upgrade your `Hibernate` version, then please use the MySQL 5.7 dialect `org.hibernate.dialect.MySQL57Dialect` instead. However, this may cause unpredictable usage results and the absence of some TiDB-specific features, such as [sequences](https://docs.pingcap.com/tidb/stable/sql-statement-create-sequence), etc.
