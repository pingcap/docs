---
title: 使用 Spring Boot 连接 TiDB
summary: 学习如何使用 Spring Boot 连接 TiDB。本教程提供了可与 TiDB 搭配使用的 Java 示例代码片段。
---

# 使用 Spring Boot 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[Spring](https://spring.io/) 是 Java 领域流行的开源容器框架。本文档以 [Spring Boot](https://spring.io/projects/spring-boot) 作为使用 Spring 的方式。

在本教程中，你可以学习如何结合 TiDB、[Spring Data JPA](https://spring.io/projects/spring-data-jpa) 以及作为 JPA 提供者的 [Hibernate](https://hibernate.org/orm/)，完成以下任务：

- 搭建你的开发环境。
- 使用 Hibernate 和 Spring Data JPA 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本的 CRUD 操作示例。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### 第 2 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致

    > **Tip:**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令，复制 `env.sh.example` 并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

6. 将对应的连接字符串复制粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数。

    {{{ .starter }}} 需要安全连接，因此你需要将 `USE_SSL` 的值设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参考 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置，以便首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，复制 `env.sh.example` 并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

5. 将对应的连接字符串复制粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数。

6. 保存 `env.sh` 文件。

</div>
<div label="TiDB 自建集群">

1. 运行以下命令，复制 `env.sh.example` 并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

2. 将对应的连接字符串复制粘贴到 `env.sh` 文件中。示例结果如下：

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    请务必将 `{}` 占位符替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>
</SimpleTab>

### 第 3 步：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 在另一个终端会话中运行请求脚本：

    ```shell
    make request
    ```

3. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式请参考 [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart) 仓库。

### 连接 TiDB

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

配置完成后，将环境变量 `TIDB_JDBC_URL`、`TIDB_USER` 和 `TIDB_PASSWORD` 设置为你 TiDB 集群的实际值。配置文件为这些环境变量提供了默认值。如果你未配置环境变量，默认值如下：

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

然后，你可以在需要 `PlayerRepository` 的任何类中使用 `@Autowired` 进行自动依赖注入，从而直接使用 CRUD 功能。示例如下：

```java
@Autowired
private PlayerRepository playerRepository;
```

### 插入或更新数据

```java
playerRepository.save(player);
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md) 和 [更新数据](/develop/dev-guide-update-data.md)。

### 查询数据

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 删除数据

```java
playerRepository.deleteById(id);
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 了解本文档中使用的第三方库和框架的更多用法，请参考其官方文档：

    - [Spring Framework 官方文档](https://spring.io/projects/spring-framework)
    - [Spring Boot 官方文档](https://spring.io/projects/spring-boot)
    - [Spring Data JPA 官方文档](https://spring.io/projects/spring-data-jpa)
    - [Hibernate 官方文档](https://hibernate.org/orm/documentation)

- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 通过 Java 开发者课程学习：[Working with TiDB from Java](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
