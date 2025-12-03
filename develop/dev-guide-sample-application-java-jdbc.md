---
title: 使用 JDBC 连接 TiDB
summary: 学习如何使用 JDBC 连接 TiDB。本教程提供了可用于 TiDB 的 Java 示例代码片段。
---

# 使用 JDBC 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，JDBC（Java Database Connectivity）是 Java 的数据访问 API。[MySQL Connector/J](https://dev.mysql.com/downloads/connector/j/) 是 MySQL 的 JDBC 实现。

在本教程中，你可以学习如何使用 TiDB 和 JDBC 完成以下任务：

- 搭建你的环境。
- 使用 JDBC 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本 CRUD 操作的示例代码。

<CustomContent platform="tidb">

> **Note:**
>
> - 本教程适用于 TiDB Cloud Starter、TiDB Cloud Essential、TiDB Cloud Dedicated 以及 TiDB 自建集群。
> - 从 TiDB v7.4 开始，如果在 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或设置为 `UTF-8`，则 JDBC 连接中使用的排序规则取决于 JDBC 驱动版本。更多信息请参见 [JDBC 连接中使用的排序规则](/faq/sql-faq.md#collation-used-in-jdbc-connections)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - 本教程适用于 TiDB Cloud Starter、TiDB Cloud Essential、TiDB Cloud Dedicated 以及 TiDB 自建集群。
> - 从 TiDB v7.4 开始，如果在 JDBC URL 中未配置 `connectionCollation`，且 `characterEncoding` 未配置或设置为 `UTF-8`，则 JDBC 连接中使用的排序规则取决于 JDBC 驱动版本。更多信息请参见 [JDBC 连接中使用的排序规则](https://docs.pingcap.com/tidb/stable/sql-faq#collation-used-in-jdbc-connections)。

</CustomContent>

## 前置条件

完成本教程，你需要：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **Note:**
>
> 出于安全考虑，建议你在通过互联网连接 TiDB 集群时，使用 `VERIFY_IDENTITY` 建立 TLS 连接。TiDB Cloud Starter、TiDB Cloud Essential 和 TiDB Cloud Dedicated 使用 Subject Alternative Name (SAN) 证书，这要求 MySQL Connector/J 版本大于等于 [8.0.22](https://dev.mysql.com/doc/relnotes/connector-j/en/news-8-0-22.html)。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-jdbc-quickstart.git
cd tidb-java-jdbc-quickstart
```

### 第 2 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致

    > **Tip:**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

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

    TiDB Cloud Starter 需要安全连接，因此你需要将 `USE_SSL` 的值设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参考 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置，以便首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

2. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-jdbc-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参考 [tidb-samples/tidb-java-jdbc-quickstart](https://github.com/tidb-samples/tidb-java-jdbc-quickstart) 仓库。

### 连接 TiDB

```java
public MysqlDataSource getMysqlDataSource() throws SQLException {
    MysqlDataSource mysqlDataSource = new MysqlDataSource();

    mysqlDataSource.setServerName(${tidb_host});
    mysqlDataSource.setPortNumber(${tidb_port});
    mysqlDataSource.setUser(${tidb_user});
    mysqlDataSource.setPassword(${tidb_password});
    mysqlDataSource.setDatabaseName(${tidb_db_name});
    if (${tidb_use_ssl}) {
        mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
        mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
    }

    return mysqlDataSource;
}
```

使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}` 和 `${tidb_db_name}` 替换为你 TiDB 集群的实际值。

### 插入数据

```java
public void createPlayer(PlayerBean player) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSource();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
        preparedStatement.setString(1, player.getId());
        preparedStatement.setInt(2, player.getCoins());
        preparedStatement.setInt(3, player.getGoods());

        preparedStatement.execute();
    }
}
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```java
public void getPlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
        preparedStatement.setString(1, id);
        preparedStatement.execute();

        ResultSet res = preparedStatement.executeQuery();
        if(res.next()) {
            PlayerBean player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
            System.out.println(player);
        }
    }
}
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```java
public void updatePlayer(String id, int amount, int price) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement transfer = connection.prepareStatement("UPDATE player SET goods = goods + ?, coins = coins + ? WHERE id=?");
        transfer.setInt(1, -amount);
        transfer.setInt(2, price);
        transfer.setString(3, id);
        transfer.execute();
    }
}
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```java
public void deletePlayer(String id) throws SQLException {
    MysqlDataSource mysqlDataSource = getMysqlDataSourceByEnv();
    try (Connection connection = mysqlDataSource.getConnection()) {
        PreparedStatement deleteStatement = connection.prepareStatement("DELETE FROM player WHERE id=?");
        deleteStatement.setString(1, id);
        deleteStatement.execute();
    }
}
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 使用驱动还是 ORM 框架？

Java 驱动提供了对数据库的底层访问，但这要求开发者：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行映射为数据对象。

除非你需要编写复杂的 SQL 语句，否则推荐使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架进行开发，例如 [Hibernate](/develop/dev-guide-sample-application-java-hibernate.md)、[MyBatis](/develop/dev-guide-sample-application-java-mybatis.md) 或 [Spring Data JPA](/develop/dev-guide-sample-application-java-spring-boot.md)。它可以帮助你：

- 减少用于管理连接和事务的 [样板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 通过数据对象操作数据，而不是大量 SQL 语句。

### MySQL 兼容性

在 MySQL 中，当你向 `DECIMAL` 列插入数据时，如果小数位数超过了该列定义的精度，MySQL 会自动截断多余的小数位并成功插入，无论多余的小数位有多少。

在 TiDB v8.5.3 及更早版本中：

- 如果小数位数超过定义的精度但不超过 72，TiDB 也会自动截断多余的小数位并成功插入。
- 但如果小数位数超过 72，插入会失败并返回错误。

从 TiDB v8.5.4 开始，TiDB 行为与 MySQL 保持一致：无论多余的小数位有多少，都会自动截断并成功插入。

## 后续步骤

- 通过 [MySQL Connector/J 文档](https://dev.mysql.com/doc/connector-j/en/) 学习更多 MySQL Connector/J 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 通过 Java 开发者课程学习：[Working with TiDB from Java](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
