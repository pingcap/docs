---
title: 使用 MyBatis 连接 TiDB
summary: 学习如何使用 MyBatis 连接 TiDB。本教程提供了适用于 TiDB 的 Java 示例代码片段，演示如何使用 MyBatis。
---

# 使用 MyBatis 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[MyBatis](https://mybatis.org/mybatis-3/index.html) 是一个流行的开源 Java ORM 框架。

在本教程中，你可以学习如何使用 TiDB 和 MyBatis 完成以下任务：

- 设置你的环境。
- 使用 MyBatis 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你可以查阅 [示例代码片段](#sample-code-snippets) 以了解基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要具备：

- **Java Development Kit (JDK) 17** 或更高版本。你可以根据业务和个人需求选择 [OpenJDK](https://openjdk.org/) 或 [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)。
- [Maven](https://maven.apache.org/install.html) **3.8** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-java-mybatis-quickstart.git
cd tidb-java-mybatis-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

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

6. 复制粘贴相应的连接字符串到 `env.sh` 文件中。示例内容如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数。

    {{{ .starter }}} 需要安全连接，因此需要将 `USE_SSL` 设置为 `true`。

7. 保存 `env.sh` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果尚未配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

5. 复制粘贴相应的连接字符串到 `env.sh` 文件中。示例内容如下：

    ```shell
    export TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # 例如 root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数。

6. 保存 `env.sh` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `env.sh.example` 复制并重命名为 `env.sh`：

    ```shell
    cp env.sh.example env.sh
    ```

2. 复制粘贴相应的连接字符串到 `env.sh` 文件中。示例内容如下：

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    一定要将 `{}` 占位符替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `env.sh` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-mybatis-quickstart/blob/main/Expected-Output.txt)，确认输出是否匹配。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式，请查阅 [tidb-samples/tidb-java-mybatis-quickstart](https://github.com/tidb-samples/tidb-java-mybatis-quickstart) 仓库。

### 连接到 TiDB

编辑 MyBatis 配置文件 `mybatis-config.xml`：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="lazyLoadingEnabled" value="false"/>
        <setting name="aggressiveLazyLoading" value="true"/>
        <setting name="logImpl" value="LOG4J"/>
    </settings>

    <environments default="development">
        <environment id="development">
            <!-- JDBC 事务管理器 -->
            <transactionManager type="JDBC"/>
            <!-- 数据库连接池 -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="${tidb_jdbc_url}"/>
                <property name="username" value="${tidb_user}"/>
                <property name="password" value="${tidb_password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="${mapper_location}.xml"/>
    </mappers>
</configuration>
```

请确保将 `${tidb_jdbc_url}`、`${tidb_user}` 和 `${tidb_password}` 替换为你的 TiDB 集群的实际值。同时，将 `${mapper_location}` 替换为你的 mapper XML 配置文件路径。对于多个 mapper XML 文件，需要为每个添加 `<mapper/>` 标签。然后定义如下函数：

```java
public SqlSessionFactory getSessionFactory() {
    InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
}
```

### 插入数据

在 mapper XML 中添加节点，并在配置在 XML 配置文件的 `mapper.namespace` 属性中的接口类中添加同名函数：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods)
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER})
    </insert>
</mapper>
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

在 mapper XML 中添加节点，并在配置在 XML 配置文件的 `mapper.namespace` 属性中的接口类中添加同名函数。特别是，如果你使用 `resultMap` 作为 MyBatis 查询函数的返回类型，确保 `<resultMap/>` 节点配置正确。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
        <constructor>
            <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
            <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
            <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
        </constructor>
    </resultMap>

    <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select id, coins, goods
    from player
    where id = #{id,jdbcType=VARCHAR}
    </select>
</mapper>
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

在 mapper XML 中添加节点，并在配置在 XML 配置文件的 `mapper.namespace` 属性中的接口类中添加同名函数：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
    </update>
</mapper>
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

在 mapper XML 中添加节点，并在配置在 XML 配置文件的 `mapper.namespace` 属性中的接口类中添加同名函数：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
    </delete>
</mapper>
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 通过 [MyBatis 官方文档](http://www.mybatis.org/mybatis-3/) 了解更多 MyBatis 的用法。
- 参考 [开发者指南](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。
- 通过 Java 开发者课程学习： [Java 使用 TiDB](https://eng.edu.pingcap.com/catalog/info/id:212)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>