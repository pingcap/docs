---
title: Build the TiDB Application using Spring Boot
summary: Gives an example of building a TiDB application using Spring Boot.
---

<!-- markdownlint-disable MD029 -->

# Build the TiDB Application using Spring Boot

This tutorial shows you how to build a [Spring Boot](https://spring.io/projects/spring-boot) Web application using TiDB. The [Spring Data JPA](https://spring.io/projects/spring-data-jpa) module is used as the framework for data access capabilities. The code repository for this sample application can be downloaded from [Github](https://github.com/pingcap-inc/tidb-example-java).

This is an example application for building a Restful API, showing a generic **Spring Boot** backend service using **TiDB** as the database. The following process was designed to recreate a realistic scenario:

This is an example of a game where each player has two attributes: `coins` and `goods`, and each player has a field `id` that uniquely identifies the player. Players can trade freely if they have sufficient coins and goods.

You can use this example as a base to build your application.

## Step 1. Launch your TiDB cluster

This part describes how to start a TiDB cluster.

### Using TiDB Cloud Free Cluster

[Create a free cluster](/develop/build-cluster-in-cloud.md#step-1-create-a-free-cluster)

### Using Local Clusters

This will briefly describe the process of starting a test cluster, for a full environment cluster deployment, or to see a more detailed deployment, please refer to [Starting TiDB Locally](/quick-start-with-tidb.md).

**Deploy local test clusters**

Applicable scenario: Use a local Mac or single-instance Linux environment to quickly deploy a TiDB test cluster, and experience the basic architecture of a TiDB cluster, and the operation of basic components such as TiDB, TiKV, PD, and Monitoring.

1. Download and install TiUP.

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare global environment variables.

    > **Note:**
    >
    > When TiUP is installed, you will be prompted for the absolute path of the corresponding `profile` file. Before executing the following `source` command, you need to modify the command according to the actual location of the `profile` file.

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. Execute the following command in the current session to start the cluster.

    - Executing the `tiup playground` command directly runs the latest version of the TiDB cluster, with 1 TiDB, TiKV, PD, and TiFlash instance:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - You can also specify the TiDB version and the number of instances of each component. The command is similar to:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

    The above command downloads and launches a version of the cluster locally (for example, v5.4.0). The latest version can be executed by `tiup list tidb` to check it out. The results of the operation will show how the cluster is accessed:

    ```
    CLUSTER START SUCCESSFULLY, Enjoy it ^-^
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
    To view the dashboard: http://127.0.0.1:2379/dashboard
    PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
    To view the Prometheus: http://127.0.0.1:9090
    To view the Grafana: http://127.0.0.1:3000
    ```

> **Note:**
>
> - TiDB supports v5.2.0 and later version runs `tiup playground` on Apple M1 machines.
> - When a playground is executed in this way, TiUP will clean up the original cluster data after the deployment test is completed, and a new cluster will be obtained after re-executing the command.
> - If you want to persist the data, you can execute TiUp's `--tag` parameter: `tiup --tag <your-tag> playground ...`, refer to the [TiUP Reference](/tiup/tiup-reference.md#-t---tag) for details.

## Step 2. Install JDK

Please download and install the **Java Development Kit** (JDK) on your computer, which is a necessary tool for Java development. **Spring Boot** supports Java version 8 or higher JDK, we recommend using Java version 11 or higher JDK due to **Hibernate** version.

We support both **Oracle JDK** and **OpenJDK**, please choose your preference, this tutorial will use version 17 of **OpenJDK**.

## Step 3. Install Maven

This sample application uses **Maven** to manage the application's dependencies; Spring supports **Maven** from version 3.2 and above, and as dependency management software, the latest stable version of **Maven** is recommended.

Here is how to install **Maven** from the command line.

- macOS:

    {{< copyable "shell-regular" >}}

    ```
    brew install maven
    ```

- Installation on Debian-based Linux distributions (e.g. Ubuntu, etc.):

    {{< copyable "shell-regular" >}}

    ```
    apt-get install maven
    ```

- Install on Red Hat-based Linux distributions (e.g. Fedora, CentOS, etc.):

1. dnf software package manager

    {{< copyable "shell-regular" >}}

    ```
    dnf install maven
    ```

2. yum software package manager

    {{< copyable "shell-regular" >}}

    ```
    yum install maven
    ```

For other installation methods, please refer to the Maven [official documentation](https://maven.apache.org/install.html).

## Step 4. Get the application code

Please download or clone the [sample code library](https://github.com/pingcap-inc/tidb-example-java) and go to the directory `spring-jpa-hibernate`.

### Create the same dependency blank application (optional)

This application is built using [Spring Initializr](https://start.spring.io/). You can quickly get a blank application with the same dependencies as this sample application by clicking on the following options and changing a few configuration items:

**Project**

- Maven Project

**Language**

- Java

**Spring Boot**

- 3.0.0-M2

**Project Metadata**

- Group: com.pingcap
- Artifact: spring-jpa-hibernate
- Name: spring-jpa-hibernate
- Package name: com.pingcap
- Packaging: Jar
- Java: 17

**Dependencies**

- Spring Web
- Spring Data JPA
- MySQL Driver

After the configuration is completed as shown in the figure:

![Spring Initializr Config](/media/develop/IMG_20220401-234316020.png)

> **Note:**
>
> Although SQL is relatively standardized, each database vendor uses a subset and superset of ANSI SQL defined syntax. This is referred to as the database’s dialect. Hibernate handles variations across these dialects through its `org.hibernate.dialect.Dialect` class and the various subclasses for each database vendor.
>
> In most cases, Hibernate will be able to determine the proper Dialect to use by asking some questions of the JDBC Connection during bootstrap. For information on Hibernate’s ability to determine the proper Dialect to use (and your ability to influence that resolution), see [Dialect resolution](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#portability-dialectresolver).
>
> If for some reason it is not able to determine the proper one or you want to use a custom Dialect, you will need to set the `hibernate.dialect` setting.
>
> _—— Excerpt from the Hibernate official documentation: [Database Dialect](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#database-dialect)_

Subsequently, the project can be used normally, but only in the same way that **TiDB** can be used with **MySQL**, i.e. using the **MySQL Dialect**. This is due to the fact that **Hibernate** supports the **TiDB Dialect** from version `6.0.0.Beta2` and above, while the default dependency of **Spring Data JPA** on **Hibernate** is `5.6.4.Final`. Therefore, we recommend the following changes to `pom.xml`.

1. The `jakarta` packages introduced within `Spring Data JPA` are excluded as shown in this [dependency file](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L26):

    {{< copyable "" >}}

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    ```

    Changed to:

    {{< copyable "" >}}

    ```xml
    <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-core-jakarta</artifactId>
        </exclusion>
    </exclusions>
    </dependency>
    ```

2. Then introduce **Hibernate** dependencies from version `6.0.0.Beta2` and above, as shown in this [dependency file](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/pom.xml#L53), using version `6.0.0.CR2` as an example:

    {{< copyable "" >}}

    ```xml
    <dependency>
        <groupId>org.hibernate.orm</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>6.0.0.CR2</version>
    </dependency>
    ```

    Once the changes are made, you can get a blank **Spring Boot** application with the same dependencies as the sample application.

## Step 5. Run the application

Here the application code is compiled and run, resulting in a web application. hibernate will create a table `player_jpa` within the database `test`, and if you make requests using the application's Restful API, these requests will run database [transactions](/develop/transaction-overview.md) on the TiDB cluster.

If you want to learn more about the code of this application, you can see the [Implementation Details](#implementation-details) at the bottom of this tutorial.

### Step 5.1 Changing Parameters

If you are using a non-local default cluster, TiDB Cloud or other remote cluster, change the `application.yml` (located in `src/main/resources`) for spring.datasource.url / spring.datasource.username / spring.datasource.password parameters.

{{< copyable "" >}}

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

If you set the password to `123456`, the connection string you get in TiDB Cloud is:

{{< copyable "shell-regular" >}}

```
mysql --connect-timeout 15 -u root -h tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com -P 4000 -p
```

Then the configuration file should be changed to:

{{< copyable "" >}}

```yaml
spring:
  datasource:
    url: jdbc:mysql://tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com:4000/test
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

### Step 5.2 Run

Open a terminal and make sure you are in the `spring-jpa-hibernate` directory, or if you are not already in this directory, use the command to enter.

{{< copyable "shell-regular" >}}

```shell
cd <path>/tidb-example-java/spring-jpa-hibernate
```

#### Build and run with Make (recommended)

{{< copyable "shell-regular" >}}

```shell
make
```

#### Build and run manually

We recommend that you build and run using the `make` command, but if you prefer to build manually, follow these steps step-by-step to get the same results.

Clear cache and package:

{{< copyable "shell-regular" >}}

```shell
mvn clean package
```

Running applications with JAR files:

{{< copyable "shell-regular" >}}

```shell
java -jar target/spring-jpa-hibernate-0.0.1.jar
```

### Step 5.3 Output

The final part of the output should look like the following:

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::             (v3.0.0-M1)

2022-03-28 18:46:01.429  INFO 14923 --- [           main] com.pingcap.App                          : Starting App v0.0.1 using Java 17.0.2 on CheesedeMacBook-Pro.local with PID 14923 (/path/code/tidb-example-java/spring-jpa-hibernate/target/spring-jpa-hibernate-0.0.1.jar started by cheese in /path/code/tidb-example-java/spring-jpa-hibernate)
2022-03-28 18:46:01.430  INFO 14923 --- [           main] com.pingcap.App                          : No active profile set, falling back to default profiles: default
2022-03-28 18:46:01.709  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2022-03-28 18:46:01.733  INFO 14923 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 20 ms. Found 1 JPA repository interfaces.
2022-03-28 18:46:02.010  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2022-03-28 18:46:02.016  INFO 14923 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2022-03-28 18:46:02.016  INFO 14923 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/10.0.16]
2022-03-28 18:46:02.050  INFO 14923 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2022-03-28 18:46:02.051  INFO 14923 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 598 ms
2022-03-28 18:46:02.143  INFO 14923 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2022-03-28 18:46:02.173  INFO 14923 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 6.0.0.CR2
2022-03-28 18:46:02.262  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.sharedCache.mode], use [jakarta.persistence.sharedCache.mode] instead
2022-03-28 18:46:02.324  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2022-03-28 18:46:02.415  INFO 14923 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection com.mysql.cj.jdbc.ConnectionImpl@2575f671
2022-03-28 18:46:02.416  INFO 14923 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2022-03-28 18:46:02.443  INFO 14923 --- [           main] SQL dialect                              : HHH000400: Using dialect: org.hibernate.dialect.TiDBDialect
Hibernate: drop table if exists player_jpa
Hibernate: drop sequence player_jpa_id_seq
Hibernate: create sequence player_jpa_id_seq start with 1 increment by 1
Hibernate: create table player_jpa (id bigint not null, coins integer, goods integer, primary key (id)) engine=InnoDB
2022-03-28 18:46:02.883  INFO 14923 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2022-03-28 18:46:02.888  INFO 14923 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2022-03-28 18:46:03.125  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.132  WARN 14923 --- [           main] org.hibernate.orm.deprecation            : HHH90000021: Encountered deprecated setting [javax.persistence.lock.timeout], use [jakarta.persistence.lock.timeout] instead
2022-03-28 18:46:03.168  WARN 14923 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2022-03-28 18:46:03.307  INFO 14923 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-03-28 18:46:03.311  INFO 14923 --- [           main] com.pingcap.App                          : Started App in 2.072 seconds (JVM running for 2.272)
```

The output log, which indicates what the application did during startup, shows that the application started a **Servlet** using [Tomcat](https://tomcat.apache.org/), used `Hibernate` as the ORM, [HikariCP](https://github.com/brettwooldridge/HikariCP) as the database connection pool implementation, and used `org.hibernate.dialect.TiDBDialect` as the database dialect. After startup, `Hibernate` deletes and re-creates the table `player_jpa` and the sequence `player_jpa_id_seq`. At the end of startup, it listens on port `8080` to provide HTTP services to the outside.

If you want to learn more about the code of this application, you can see the [implementation details](#implementation-details) at the bottom of this tutorial.

## Step 6. HTTP Request

Once the service is up and running, the HTTP interface can be used to request the back-end application. `http://localhost:8080` is our service providing the root address. We use a series of HTTP requests to show how to use the service.

### Step 6.1 Using Postman Requests (recommended)

You can download this [configuration file](https://raw.githubusercontent.com/pingcap-inc/tidb-example-java/main/spring-jpa-hibernate/Player.postman_collection.json) locally and import it into [Postman](https://www.postman.com/) as shown here:

![postman import](/media/develop/IMG_20220402-003303222.png)

#### Create player

Click on the **Create** tab and the **Send** button to send a request in the form of a Post to `http://localhost:8080/player/`. The return value is the number of players added, which is expected to be 1.

![Postman-Create](/media/develop/IMG_20220402-003350731.png)

#### Get Player Information by ID

Click on the **GetByID** tab and the **Send** button to send a Get form of the `http://localhost:8080/player/1` request. The return value is the player information with ID 1.

![Postman-GetByID](/media/develop/IMG_20220402-003416079.png)

#### Get Player Information in Bulk by Limit

Click on the **GetByLimit** tab and the **Send** button to send a request in the form of a Get to `http://localhost:8080/player/limit/3`. The return value is a list of information for up to 3 players.

![Postman-GetByLimit](/media/develop/IMG_20220402-003505846.png)

#### Get Player Information by Page

Click on the **GetByPage** tab and the **Send** button to send a Get form of the `http://localhost:8080/player/page?index=0&size=2` request. The return value is the page with index 0, with 2 lists of player information per page. In addition, it contains paging information such as offset, totalPages, sort, etc.

![Postman-GetByPage](/media/develop/IMG_20220402-003528474.png)

#### Count Players

Click the **Count** tab and the **Send** button to send a Get form of the `http://localhost:8080/player/count` request. The return value is the number of players.

![Postman-Count](/media/develop/IMG_20220402-003549966.png)

#### Player Trading

Click on the **Trade** tab and the **Send** button to send a Put request to `http://localhost:8080/player/trade` with the request parameters are sell player ID `sellID`, buy player ID `buyID`, number of goods purchased `amount`, number of coins consumed for the purchase `price`. The return value is whether the transaction is successful or not. When there are insufficient goods for the selling player, insufficient gold for the buying player, or database error, the transaction will not be successful and no player's gold or goods will be lost due to the database [transaction](/develop/transaction-overview.md) guarantee.

![Postman-Trade](/media/develop/IMG_20220402-003659102.png)

### Step 6.2 Using curl requests

Of course, you can also use curl to make requests directly.

#### Create player

We use the **Post** method to request the `/player` endpoint request to create players, i.e.

{{< copyable "shell-regular" >}}

```shell
curl --location --request POST 'http://localhost:8080/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
```

Here we use JSON as the load of our message. It means that we need to create a player with `coins` of 100 and `goods` of 20. The return value is the number of players created.

```json
1
```

#### Get Player Information by ID

We use the **Get** method to request the `/player` endpoint request to get the player information, additionally we need to give the player `id` parameter in the path, i.e. `/player/{id}`, for example when requesting a player with `id` 1:

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/1'
```

The return value is the player's information:

```json
{
  "coins": 200,
  "goods": 10,
  "id": 1
}
```

#### Get Player Information in Bulk by Limit

We use the **Get** method to request the `/player/limit` endpoint request to get player information, additionally we need to give the total number of player information to limit the query on the path, i.e. `/player/limit/{limit}`, for example when requesting information for up to 3 players.

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/limit/3'
```

The return value is a list of player information:

```json
[
  {
    "coins": 200,
    "goods": 10,
    "id": 1
  },
  {
    "coins": 0,
    "goods": 30,
    "id": 2
  },
  {
    "coins": 100,
    "goods": 20,
    "id": 3
  }
]
```

#### Get Player Information by Page

We use the **Get** method to request the `/player/page` endpoint request to paginate the player information, additionally we need to use the URL parameter, for example when requesting a page number `index` of 0 and a maximum request `size` of 2 per page.

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/page?index=0&size=2'
```

The return value is the page with `index` 0, with 2 lists of player information per page. In addition, it contains paging information such as offset, totalPages, sort, etc.

```json
{
  "content": [
    {
      "coins": 200,
      "goods": 10,
      "id": 1
    },
    {
      "coins": 0,
      "goods": 30,
      "id": 2
    }
  ],
  "empty": false,
  "first": true,
  "last": false,
  "number": 0,
  "numberOfElements": 2,
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 2,
    "paged": true,
    "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
    },
    "unpaged": false
  },
  "size": 2,
  "sort": {
    "empty": true,
    "sorted": false,
    "unsorted": true
  },
  "totalElements": 4,
  "totalPages": 2
}
```

#### Count Players

We use the **Get** method to request the `/player/count` endpoint request to get the number of players:

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8080/player/count'
```

The return value is the number of players:

```json
4
```

#### Player Trading

We initiate a transaction between players by requesting the `/player/trade` endpoint request using the **Put** method, i.e.

{{< copyable "shell-regular" >}}

```shell
curl --location --request PUT 'http://localhost:8080/player/trade' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'sellID=1' \
  --data-urlencode 'buyID=2' \
  --data-urlencode 'amount=10' \
  --data-urlencode 'price=100'
```

We use **Form Data** as the payload of our message with the request parameters are sell player ID `sellID`, buy player ID `buyID`, number of goods purchased `amount`, number of coins consumed for purchase `price`.

The return value is whether the transaction is successful or not. When there is insufficient goods for the selling player, insufficient gold for the buying player or database error, the transaction will not be successful and no player's gold or goods will be lost due to the database [transaction](/develop/transaction-overview.md) guarantee.

```json
true
```

### Step 6.3 Request with Shell Script

We have written the request process as a [shell script](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/request.sh) for your testing purposes and the script will do the following things:

1. create 10 players in a loop
2. get the information of players with the `id` of 1
3. get a list of up to 3 players
4. get a page of players with the `index` of 0 and the `size` of 2
5. get the total number of players
6. the player with the `id` of 1 is the seller and the player with the id of 2 is the buyer, buy 10 goods and cost 100 gold coins

You can run this script with `make request` or `./request.sh` command and the result should look like this:

```
cheese@CheesedeMacBook-Pro spring-jpa-hibernate % make request
./request.sh
loop to create 10 players:
1111111111

get player 1:
{"id":1,"coins":200,"goods":10}

get players by limit 3:
[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30},{"id":3,"coins":100,"goods":20}]

get first players:
{"content":[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30}],"pageable":{"sort":{"empty":true,"unsorted":true,"sorted":false},"offset":0,"pageNumber":0,"pageSize":2,"paged":true,"unpaged":false},"last":false,"totalPages":7,"totalElements":14,"first":true,"size":2,"number":0,"sort":{"empty":true,"unsorted":true,"sorted":false},"numberOfElements":2,"empty":false}

get players count:
14

trade by two players:
false
```

## Implementation Details

This subsection describes the components in the sample application project.

### Overview

The catalog tree for this example project is shown below (with the parts that are incomprehensible removed):

```
.
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── App.java
        │           ├── controller
        │           │   └── PlayerController.java
        │           ├── dao
        │           │   ├── PlayerBean.java
        │           │   └── PlayerRepository.java
        │           └── service
        │               ├── PlayerService.java
        │               └── impl
        │                   └── PlayerServiceImpl.java
        └── resources
            └── application.yml
```

- `pom.xml` declares the project's Maven configuration, such as dependencies, packaging, etc.
- `application.yml` declares the project's user configuration, such as database address, password, database dialect used, etc.
- `App.java` is the entry point of the project
- `controller` is the package that exposes the HTTP interface to the project
- `service` is the package that implements the interface and logic of the project
- `dao` is the package that implements the connection to the database and the persistence of the data

### Configuration

This part will briefly describe the Maven configuration in the `pom.xml` file and the user configuration in the `application.yml` file.

#### Maven Configuration

The `pom.xml` file is a Maven configuration file that declares the project's Maven dependencies, packaging methods, packaging information, etc. You can replicate the process of generating this configuration file by [create the same dependency blank application](#create-the-same-dependency-blank-application-optional), or copying it directly to your project.

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>
   <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.0.0-M1</version>
      <relativePath/> <!-- lookup parent from repository -->
   </parent>

   <groupId>com.pingcap</groupId>
   <artifactId>spring-jpa-hibernate</artifactId>
   <version>0.0.1</version>
   <name>spring-jpa-hibernate</name>
   <description>an example for spring boot, jpa, hibernate and TiDB</description>

   <properties>
      <java.version>17</java.version>
      <maven.compiler.source>17</maven.compiler.source>
      <maven.compiler.target>17</maven.compiler.target>
   </properties>

   <dependencies>
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-data-jpa</artifactId>
         <exclusions>
            <exclusion>
               <groupId>org.hibernate</groupId>
               <artifactId>hibernate-core-jakarta</artifactId>
            </exclusion>
         </exclusions>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-web</artifactId>
      </dependency>

      <dependency>
         <groupId>mysql</groupId>
         <artifactId>mysql-connector-java</artifactId>
         <scope>runtime</scope>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>

      <dependency>
         <groupId>org.hibernate.orm</groupId>
         <artifactId>hibernate-core</artifactId>
         <version>6.0.0.CR2</version>
      </dependency>
   </dependencies>

   <build>
      <plugins>
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
         </plugin>
      </plugins>
   </build>

   <repositories>
      <repository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </repository>
   </repositories>
   <pluginRepositories>
      <pluginRepository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </pluginRepository>
   </pluginRepositories>
</project>
```

#### User Configuration

`application.yml` This configuration file declares the user configuration, such as database address, password, database dialect used, etc.

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

The [YAML](https://yaml.org/) configuration has:

- `spring.datasource.url` : URL of the database connection
- `spring.datasource.url` : database username
- `spring.datasource.password` : the database password, this is empty, need to comment or delete
- `spring.datasource.driver-class-name` : database driver, since TiDB is compatible with MySQL, use mysql-connector-java driver class here `com.mysql.cj.jdbc`.
- `jpa.show-sql` : when true, the SQL run by JPA will be printed
- `jpa.database-platform` : the selected database dialect, here we connect to TiDB, so naturally we choose **TiDB dialect**, this dialect is only available in Hibernate version `6.0.0.Beta2` and above, please notice the dependency version.
- `jpa.hibernate.ddl-auto` : The `create-drop` selected here will create the table at the beginning of the program and delete it on exit. Please do not use this in a formal environment, but we are using this as a sample application and want to minimize the impact on the database data, so we have chosen this option.

### Entry Point

Entry point `App.java`:

{{< copyable "" >}}

```java
package com.pingcap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.ApplicationPidFileWriter;

@SpringBootApplication
public class App {
   public static void main(String[] args) {
      SpringApplication springApplication = new SpringApplication(App.class);
      springApplication.addListeners(new ApplicationPidFileWriter("spring-jpa-hibernate.pid"));
      springApplication.run(args);
   }
}
```

Our entry class is very simple, starting with the standard configuration annotation [@SpringBootApplication](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/SpringBootApplication.html) for Spring Boot applications. For more information, see [Using the @SpringBootApplication Annotation](https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-using-springbootapplication-annotation) in the Spring Boot official documentation. Then, use the `ApplicationPidFileWriter` to write a PID (process identification number) file called `spring-jpa-hibernate.pid` during application startup, which can be used externally to close the application.

### Data Access Object

The `dao` (Data Access Object) package, implements the persistence of data objects.

#### Entity objects

The `PlayerBean.java` file is an entity object, which corresponds to a table in the database:

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.*;

/**
 * it's core entity in hibernate
 * @Table appoint to table name
 */
@Entity
@Table(name = "player_jpa")
public class PlayerBean {
    /**
     * @ID primary key
     * @GeneratedValue generated way. this field will use generator named "player_id"
     * @SequenceGenerator using `sequence` feature to create a generator,
     *    and it named "player_jpa_id_seq" in database, initial form 1 (by `initialValue`
     *    parameter default), and every operator will increase 1 (by `allocationSize`)
     */
    @Id
    @GeneratedValue(generator="player_id")
    @SequenceGenerator(name="player_id", sequenceName="player_jpa_id_seq", allocationSize=1)
    private Long id;

    /**
     * @Column field
     */
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

We can see that the entity class has several annotations that give Hibernate additional information to bind the entity class to the table.

- `@Entity` declares that `PlayerBean` is an entity class
- `@Table` relates this entity class to the table `player_jpa` using the annotated attribute `name`
- `@Id` declare that this property is related to the primary key column of the table
- `@GeneratedValue` indicates that the value of this column is generated automatically and should not be set manually, using the attribute `generator` to specify the name of the generator as `player_id`.
- `@SequenceGenerator` declares a generator that uses [sequence](/common/sql-statements/sql-statement-create-sequence.md), and uses the annotation attribute `name` to declare the name of the generator as `player_id` (to be consistent with the name specified in `@GeneratedValue`). Then use the annotation attribute `sequenceName` to specify the name of the sequence in the database. Finally, the annotation attribute `allocationSize` is used to declare the sequence's step size to be 1.
- `@Column` declares each private attribute as a column of the table `player_jpa`, and uses the annotated attribute `name` to determine the name of the column corresponding to the attribute.

#### Repository

To abstract the database layer, Spring applications use the [Repository](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories) interface, or a sub-interface of the `Repository`. This interface maps to a database object, such as a table. JPA will implement some methods for us, such as [INSERT](/common/sql-statements/sql-statement-insert.md), or [SELECT](/common/sql-statements/sql-statement-select.md), etc.

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.LockModeType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
    /**
     * use HQL to query by page
     * @param pageable a pageable parameter required by hibernate
     * @return player list package by page message
     */
    @Query(value = "SELECT player_jpa FROM PlayerBean player_jpa")
    Page<PlayerBean> getPlayersByPage(Pageable pageable);

    /**
     * use SQL to query by limit, using named parameter
     * @param limit sql parameter
     * @return player list (max size by limit)
     */
    @Query(value = "SELECT * FROM player_jpa LIMIT :limit", nativeQuery = true)
    List<PlayerBean> getPlayersByLimit(@Param("limit") Integer limit);

    /**
     * query player and add a lock for update
     * @param id player id
     * @return player
     */
    @Lock(value = LockModeType.PESSIMISTIC_WRITE)
    @Query(value = "SELECT player FROM PlayerBean player WHERE player.id = :id")
    // @Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
    PlayerBean getPlayerAndLock(@Param("id") Long id);
}
```

The `PlayerRepository` extends the interface JpaRepository used by Spring for JPA data access, and we use the `@Query` annotation to indicate Hibernate how to implement queries in this interface. We use two query syntaxes here, where the query in the interface `getPlayersByPage` uses a syntax that Hibernate calls [HQL](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#hql) (Hibernate Query Language). The interface `getPlayersByLimit` uses native SQL, and the `@Query` annotation parameter `nativeQuery` needs to be set to `true` when using the native SQL syntax.

In the SQL for the `getPlayersByLimit` annotation, `:limit` is called [named parameters](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#jpql-query-parameters) in Hibernate, and Hibernate will automatically find and splice the parameter by name within the interface where the annotation resides. You can also use `@Param` to specify a different name than the parameter for injection.

In `getPlayerAndLock` we use an annotation [@Lock](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/Lock.html) which declares that locking is done here using pessimistic locks, for more information about other locking methods see [here](https://openjpa.apache.org/builds/2.2.2/apache-openjpa/docs/jpa_overview_em_locking.html). The `@Lock` annotation can only be used with `HQL`, otherwise, an error will occur. If you want to use SQL directly for locking, you can use the annotation directly in the comments section:

{{< copyable "" >}}

```java
@Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
```

Use SQL: `FOR UPDATE` to add locks directly. You can also go deeper into the principles with the TiDB [SELECT document](/common/sql-statements/sql-statement-select.md).

### Logic Implementation

The logic implementation layer: `service` package, contains the interfaces and logic implemented by the project.

#### Interface

The reason for defining an interface within the `PlayerService.java` file and implementing the interface instead of writing a class directly is to try to keep the example as close to actual use as possible and to reflect the [open-closed principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle) of the design. You can also omit this interface and inject the implementation class directly into the dependency class, but we don't recommend this.

{{< copyable "" >}}

```java
package com.pingcap.service;

import com.pingcap.dao.PlayerBean;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlayerService {
    /**
     * create players by passing in a List of PlayerBean
     *
     * @param players will create players list
     * @return The number of create accounts
     */
    Integer createPlayers(List<PlayerBean> players);

    /**
     * buy goods and transfer funds between one player and another in one transaction
     * @param sellId sell player id
     * @param buyId buy player id
     * @param amount goods amount, if sell player has not enough goods, the trade will break
     * @param price price should pay, if buy player has not enough coins, the trade will break
     */
    void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException;

    /**
     * get the player info by id.
     *
     * @param id player id
     * @return the player of this id
     */
    PlayerBean getPlayerByID(Long id);

    /**
     * get a subset of players from the data store by limit.
     *
     * @param limit return max size
     * @return player list
     */
    List<PlayerBean> getPlayers(Integer limit);

    /**
     * get a page of players from the data store.
     *
     * @param index page index
     * @param size page size
     * @return player list
     */
    Page<PlayerBean> getPlayersByPage(Integer index, Integer size);

    /**
     * count players from the data store.
     *
     * @return all players count
     */
    Long countPlayers();
}
```

#### Implementation (Important)

The `PlayerService.java` file implements the `PlayerService` interface, where all our data processing logic is written.

{{< copyable "" >}}

```java
package com.pingcap.service.impl;

import com.pingcap.dao.PlayerBean;
import com.pingcap.dao.PlayerRepository;
import com.pingcap.service.PlayerService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * PlayerServiceImpl implements PlayerService interface
 * @Transactional it means every method in this class, will package by a pair of
 *     transaction.begin() and transaction.commit(). and it will be call
 *     transaction.rollback() when method throw an exception
 */
@Service
@Transactional
public class PlayerServiceImpl implements PlayerService {
    @Autowired
    private PlayerRepository playerRepository;

    @Override
    public Integer createPlayers(List<PlayerBean> players) {
        return playerRepository.saveAll(players).size();
    }

    @Override
    public void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException {
        PlayerBean buyPlayer = playerRepository.getPlayerAndLock(buyId);
        PlayerBean sellPlayer = playerRepository.getPlayerAndLock(sellId);
        if (buyPlayer == null || sellPlayer == null) {
            throw new RuntimeException("sell or buy player not exist");
        }

        if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
            throw new RuntimeException("coins or goods not enough, rollback");
        }

        buyPlayer.setGoods(buyPlayer.getGoods() + amount);
        buyPlayer.setCoins(buyPlayer.getCoins() - price);
        playerRepository.save(buyPlayer);

        sellPlayer.setGoods(sellPlayer.getGoods() - amount);
        sellPlayer.setCoins(sellPlayer.getCoins() + price);
        playerRepository.save(sellPlayer);
    }

    @Override
    public PlayerBean getPlayerByID(Long id) {
        return playerRepository.findById(id).orElse(null);
    }

    @Override
    public List<PlayerBean> getPlayers(Integer limit) {
        return playerRepository.getPlayersByLimit(limit);
    }

    @Override
    public Page<PlayerBean> getPlayersByPage(Integer index, Integer size) {
        return playerRepository.getPlayersByPage(PageRequest.of(index, size));
    }

    @Override
    public Long countPlayers() {
        return playerRepository.count();
    }
}
```

Here we use the `@Service` annotation to declare that the life cycle of this object is managed by `Spring`.

Note that the PlayerServiceImpl implementation class has a [@Transactional](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#transaction-declarative-annotations) annotation in addition to the `@Service` annotation. When transaction management is enabled in the application (which can be turned on using [@EnableTransactionManagement](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html), but is turned on by default by `Spring Boot` and does not need to be configured manually again), `Spring` automatically wraps all objects with the `@Transactional` annotation in a proxy, which is used for object invocation processing.

You can simply assume that when the agent calls a function inside an object with the `@Transactional` annotation: 

- At the top of the function it will start the transaction with `transaction.begin()`
- When the function returns, it will call `transaction.commit()` to commit the transaction
- When any runtime error occurs, the agent will call `transaction.rollback()` to roll back.

You can refer to [Database Transactions](/develop/transaction-overview.md) for more information on transactions, or read the article on the `Spring` website to [Understanding the Spring Framework’s Declarative Transaction Implementation](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#tx-decl-explained).

Of the implementation classes, the `buyGoods` function is the one to focus on, as it throws an exception if it is not logical and directs `Hibernate` to perform a transaction rollback to prevent incorrect data.

### External HTTP Interface

The `controller` package exposes the HTTP interface to the outside world and allows access to the service via the [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api#).

{{< copyable "" >}}

```java
package com.pingcap.controller;

import com.pingcap.dao.PlayerBean;
import com.pingcap.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/player")
public class PlayerController {
    @Autowired
    private PlayerService playerService;

    @PostMapping
    public Integer createPlayer(@RequestBody @NonNull List<PlayerBean> playerList) {
        return playerService.createPlayers(playerList);
    }

    @GetMapping("/{id}")
    public PlayerBean getPlayerByID(@PathVariable Long id) {
        return playerService.getPlayerByID(id);
    }

    @GetMapping("/limit/{limit_size}")
    public List<PlayerBean> getPlayerByLimit(@PathVariable("limit_size") Integer limit) {
        return playerService.getPlayers(limit);
    }

    @GetMapping("/page")
    public Page<PlayerBean> getPlayerByPage(@RequestParam Integer index, @RequestParam("size") Integer size) {
        return playerService.getPlayersByPage(index, size);
    }

    @GetMapping("/count")
    public Long getPlayersCount() {
        return playerService.countPlayers();
    }

    @PutMapping("/trade")
    public Boolean trade(@RequestParam Long sellID, @RequestParam Long buyID, @RequestParam Integer amount, @RequestParam Integer price) {
        try {
            playerService.buyGoods(sellID, buyID, amount, price);
        } catch (RuntimeException e) {
            return false;
        }

        return true;
    }
}
```

`PlayerController` uses annotations as many as possible to demonstrate feature, in real projects, please try to keep the style uniform while following the rules of your company or group. We will explain annotations in `PlayerController` one by one:

- [@RestController](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html) declares the `PlayerController` as a [Web Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) and serializes the return value as `JSON` output.
- [@RequestMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html)  maps the URL endpoint to `/player`, i.e. this `Web Controller` only listens for requests under the `/player` URL.
- `@Autowired` means `Spring` container can autowire relationships between collaborating beans. As you can see, we declare that we need a `PlayerService` object here, which is an interface, and we don't specify which implementation class to use. This is automatically assembled by Spring. For the rules of this assembly, see the article [The IoC container](https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/beans.html) on Spring's official website.
- [@PostMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PostMapping.html) declares that this function will respond to a [POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) type request in HTTP.
    - `@RequestBody` declares that the entire HTTP payload is parsed here into the parameter named `playerList`.
    - `@NonNull` declares that the parameter must not be null, otherwise, it will return an error
- [@GetMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/GetMapping.html) declares that this function will respond to a [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) type request in HTTP.
    - [@PathVariable](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PathVariable.html) shows that the annotation has placeholders like `{id}`, `{limit_size}` which will be bound to the variable annotated by `@PathVariable`, based on the annotation attribute name (variable name can be omitted, i.e. `@PathVariable(name="limit_size")` can be written as `@PathVariable("limit_size")`), which is the same as the variable name when not specified specifically
- [@PutMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PutMapping.html) declares that this function will respond to a [PUT](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT) type request in HTTP
- [@RequestParam](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestParam.html) declares that this function will parse URL parameters, form parameters, and other parameters in the request and bind them to the annotated variables
