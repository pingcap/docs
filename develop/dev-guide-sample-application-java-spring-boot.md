---
title: 使用 Spring Boot 连接 TiDB
summary: 学习如何使用 Spring Boot 连接 TiDB。本教程提供适用于 TiDB 的 Java 示例代码片段，结合 Spring Boot 使用。
---

# 使用 Spring Boot 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Spring](https://spring.io/) 是一个流行的开源 Java 容器框架。本文件以 [Spring Boot](https://spring.io/projects/spring-boot) 作为使用 Spring 的方式。

在本教程中，你可以学习如何结合 [Spring Data JPA](https://spring.io/projects/spring-data-jpa) 和 [Hibernate](https://hibernate.org/orm/) 作为 JPA 提供者，完成以下任务：

- 设置你的环境。
- 使用 Hibernate 和 Spring Data JPA 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你可以找到 [示例代码片段](#sample-code-snippets) 用于基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    >
    > 如果之前已创建密码，可以使用原密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

6. 复制粘贴对应的连接字符串到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    一定要用连接对话框中的参数替换 `{}` 占位符。

    {{{ .starter }}} 需要安全连接，因此需要将 `USE_SSL` 设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果尚未配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

5. 复制粘贴对应的连接字符串到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    一定要用连接对话框中的参数替换 `{}` 占位符。

6. 保存 `env.sh` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

2. 复制粘贴对应的连接字符串到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    一定要用连接对话框中的参数替换 `{}` 占位符，并将 `USE_SSL` 设置为 `false`。如果在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 在另一个终端会话中运行请求脚本：

    ```shell
    make request
    ```

3. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt)，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式，请查看 [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart) 仓库。

### 连接到 TiDB

编辑配置文件 `application.yml`：

```yaml
spring:
  datasource:
    url: ${TIDB_JDBC_URL:jdbc:mysql://localhost:4000/test}
    username: ${TIDB_USER:root}
    password: ${TIDB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

配置后，设置环境变量 `TIDB_JDBC_URL`、`TIDB_USER` 和 `TIDB_PASSWORD` 为你的 TiDB 集群的实际值。配置文件为这些环境变量提供了默认值。如果未配置环境变量，默认值如下：

- `TIDB_JDBC_URL`：`"jdbc:mysql://localhost:4000/test"`
- `TIDB_USER`：`"root"`
- `TIDB_PASSWORD`：`""`

### 数据管理：`@Repository`

Spring Data JPA 通过 `@Repository` 接口管理数据。要使用 `JpaRepository` 提供的 CRUD 操作，需要继承 `JpaRepository` 接口：

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

然后，在任何需要 `PlayerRepository` 的类中，可以使用 `@Autowired` 进行自动依赖注入，从而直接调用 CRUD 方法。示例：

```java
@Autowired
private PlayerRepository playerRepository;
```

### 插入或更新数据

```java
playerRepository.save(player);
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md) 和 [Update data](/develop/dev-guide-update-data.md)。

### 查询数据

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 删除数据

```java
playerRepository.deleteById(id);
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 了解本文件中使用的第三方库和框架的更多用法，请参考它们的官方文档：

    - [Spring Framework 文档](https://spring.io/projects/spring-framework)
    - [Spring Boot 文档](https://spring.io/projects/spring-boot)
    - [Spring Data JPA 文档](https://spring.io/projects/spring-data-jpa)
    - [Hibernate 文档](https://hibernate.org/orm/documentation)

- 通过 [开发者指南](/develop/dev-guide-overview.md) 中的章节学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。

- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

- 通过 Java 开发者课程：[用 Java 操作 TiDB](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>