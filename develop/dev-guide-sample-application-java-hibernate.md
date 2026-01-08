---
title: 使用 Hibernate 连接 TiDB
summary: 学习如何使用 Hibernate 连接 TiDB。本教程提供了可与 TiDB 搭配使用的 Java 示例代码片段。
---

# 使用 Hibernate 连接 TiDB

TiDB 是一个 MySQL 兼容的数据库，[Hibernate](https://hibernate.org/orm/) 是流行的开源 Java ORM。由于 TiDB 与 MySQL 高度兼容，建议你将 `org.hibernate.dialect.MySQLDialect` 作为 Hibernate 的 dialect，以获得长期兼容性。或者，你也可以使用 TiDB 专用的 dialect（`org.hibernate.community.dialect.TiDBDialect`），该 dialect 可在 [Hibernate community dialects](https://github.com/hibernate/hibernate-orm/tree/main/hibernate-community-dialects) 中找到，但并非由 PingCAP 维护。如果你在使用 `MySQLDialect` 时遇到任何兼容性问题，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

在本教程中，你可以学习如何使用 TiDB 和 Hibernate 完成以下任务：

- 搭建你的环境。
- 使用 Hibernate 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本 CRUD 操作的代码示例。

> **注意：**
>
> 本教程适用于 TiDB Cloud Starter、TiDB Cloud Essential、TiDB Cloud Dedicated 以及自建 TiDB。

## 前提条件

完成本教程，你需要：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参照 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参照 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-hibernate-quickstart.git
cd tidb-java-hibernate-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境匹配

    > **提示：**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **提示：**
    >
    > 如果你之前已创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

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

    请务必将 `{}` 占位符替换为连接对话框中获得的连接参数。

    TiDB Cloud Starter 需要安全连接，因此你需要将 `USE_SSL` 的值设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你尚未配置 IP 访问列表，请点击 **Configure IP Access List**，或参照 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行首次连接前的配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

    请务必将 `{}` 占位符替换为连接对话框中获得的连接参数。

6. 保存 `env.sh` 文件。

</div>
<div label="TiDB 自建版">

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

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-hibernate-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参见 [tidb-samples/tidb-java-hibernate-quickstart](https://github.com/tidb-samples/tidb-java-hibernate-quickstart) 仓库。

### 连接 TiDB

编辑 Hibernate 配置文件 `hibernate.cfg.xml`：

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

请务必将 `${tidb_jdbc_url}`、`${tidb_user}` 和 `${tidb_password}` 替换为你 TiDB 集群的实际值。然后，定义如下函数：

```java
public SessionFactory getSessionFactory() {
    return new Configuration()
            .configure("hibernate.cfg.xml")
            .addAnnotatedClass(${your_entity_class})
            .buildSessionFactory();
}
```

使用该函数时，你需要将 `${your_entity_class}` 替换为你自己的数据实体类。若有多个实体类，需要为每个类添加一条 `.addAnnotatedClass(${your_entity_class})` 语句。上述函数只是配置 Hibernate 的一种方式。如果你在配置过程中遇到问题，或想了解更多 Hibernate 相关内容，请参考 [Hibernate 官方文档](https://hibernate.org/orm/documentation)。

### 插入或更新数据

```java
try (Session session = sessionFactory.openSession()) {
    session.persist(new PlayerBean("id", 1, 1));
}
```

更多信息参见 [插入数据](/develop/dev-guide-insert-data.md) 和 [修改数据](/develop/dev-guide-update-data.md)。

### 查询数据

```java
try (Session session = sessionFactory.openSession()) {
    PlayerBean player = session.get(PlayerBean.class, "id");
    System.out.println(player);
}
```

更多信息参见 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 删除数据

```java
try (Session session = sessionFactory.openSession()) {
    session.remove(new PlayerBean("id", 1, 1));
}
```

更多信息参见 [删除数据](/develop/dev-guide-delete-data.md)。

## 与 `MySQLDialect` 的兼容性

当你在 TiDB 中使用 `MySQLDialect` 时，请注意以下行为：

### `SERIALIZABLE` 隔离级别

应用程序如果尝试设置 `SERIALIZABLE` 事务隔离级别，在 TiDB 中会遇到如下错误：

```
The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

为避免该错误，请在服务器端设置如下 TiDB 系统变量：

```sql
SET GLOBAL tidb_skip_isolation_level_check=1;
```

启用该变量后，TiDB 会接受指定 `SERIALIZABLE` 的请求而不返回错误。内部实际仍采用 `REPEATABLE-READ`，这是 TiDB 的最强隔离级别。更多信息参见 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check)。

> **注意：**
>
> 社区维护的 `TiDBDialect` 会自动处理该行为，跳过需要 `SERIALIZABLE` 隔离级别的特性。

### `CHECK` 约束

Hibernate 的 [`@Check`](https://docs.hibernate.org/orm/6.5/javadocs/org/hibernate/annotations/Check.html) 注解会生成 DDL `CHECK` 约束。[MySQL 8.0.16 及以上版本](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html) 默认会强制执行这些约束，但 TiDB 默认不会强制执行，除非你显式开启。

如需在 TiDB 中启用 `CHECK` 约束强制执行，请设置如下系统变量：

```sql
SET GLOBAL tidb_enable_check_constraint=ON;
```

如果未设置该变量，TiDB 会接受 `CHECK` 约束语法但不会强制执行，可能导致数据完整性问题。更多信息参见 [`CHECK` 约束](/constraints.md#check)。

## 后续步骤

- 通过 [Hibernate 文档](https://hibernate.org/orm/documentation) 学习更多 Hibernate 用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[修改数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 通过 Java 开发者课程学习：[Working with TiDB from Java](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>