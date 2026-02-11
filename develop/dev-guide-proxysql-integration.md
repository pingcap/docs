---
title: 集成 TiDB 与 ProxySQL
summary: 了解如何将 TiDB Cloud 和 TiDB（自托管）与 ProxySQL 集成。
aliases: ['/tidb/stable/dev-guide-proxysql-integration/','/tidb/dev/dev-guide-proxysql-integration/','/tidbcloud/dev-guide-proxysql-integration/']
---

# 集成 TiDB 与 ProxySQL

本文档提供了 ProxySQL 的高级介绍，描述了如何在 [开发环境](#development-environment) 和 [生产环境](#production-environment) 中将 ProxySQL 与 TiDB 集成，并通过 [查询路由场景](#typical-scenario) 展示了关键的集成优势。

如果你希望进一步了解 TiDB 和 ProxySQL，可以参考以下链接：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
- [TiDB Developer Guide](https://docs.pingcap.com/developer/)
- [ProxySQL Documentation](https://proxysql.com/documentation/)

## 什么是 ProxySQL？

[ProxySQL](https://proxysql.com/) 是一个高性能的开源 SQL 代理。它拥有灵活的架构，可以以多种方式部署，非常适合多种使用场景。例如，ProxySQL 可用于通过缓存频繁访问的数据来提升性能。

ProxySQL 从零开始设计，目标是快速、高效且易于使用。它完全兼容 MySQL，并支持你期望从高质量 SQL 代理获得的所有功能。此外，ProxySQL 还具备许多独特特性，使其成为各种应用的理想选择。

## 为什么要集成 ProxySQL？

- ProxySQL 可以通过减少与 TiDB 交互时的延时来提升应用性能。无论你构建的是基于 Lambda 等无服务器函数的可扩展应用，工作负载不可预测且可能激增，还是需要执行大量数据加载查询的应用，都可以通过 ProxySQL 的强大功能（如 [连接池](https://proxysql.com/documentation/detailed-answers-on-faq/) 和 [缓存常用查询](https://proxysql.com/documentation/query-cache/)）获得直接收益。
- ProxySQL 可以作为应用安全的额外防护层，利用 [查询规则](#query-rules)（ProxySQL 提供的易于配置的功能）防御 SQL 注入等 SQL 漏洞。
- 由于 [ProxySQL](https://github.com/sysown/proxysql) 和 [TiDB](https://github.com/pingcap/tidb) 都是开源项目，你可以获得零厂商锁定的优势。

## 部署架构

将 ProxySQL 与 TiDB 部署的最直接方式，是将 ProxySQL 作为应用层与 TiDB 之间的独立中间层。然而，这种方式无法保证扩展性和容错性，并且由于网络跳转会增加额外延时。为避免这些问题，另一种部署架构是将 ProxySQL 作为 sidecar 部署，如下图所示：

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注意：**
>
> 上述示意图仅供参考。你需要根据实际部署架构进行调整。

## 开发环境

本节介绍如何在开发环境中将 TiDB 与 ProxySQL 集成。在开始 ProxySQL 集成前，请根据你的 TiDB 集群类型，选择以下任一方案，并确保已满足所有 [前置条件](#prerequisite)。

- 方案 1：[集成 TiDB Cloud 与 ProxySQL](#option-1-integrate-tidb-cloud-with-proxysql)
- 方案 2：[集成 TiDB（自托管）与 ProxySQL](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前置条件

根据你选择的方案，可能需要以下软件包：

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)
- [Docker Compose](https://docs.docker.com/compose/install/linux/)
- [MySQL Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

你可以按照以下安装说明操作：

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1. [下载](https://docs.docker.com/get-docker/)并启动 Docker（Docker Desktop 已包含 Docker Compose）。
2. 运行以下命令安装 Python 和 `mysql-client`：

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python mysql-client
    ```

</div>

<div label="CentOS" value="CentOS">

```bash
curl -fsSL https://get.docker.com | bash -s docker
yum install -y git python39 docker-ce docker-ce-cli containerd.io docker-compose-plugin mysql
systemctl start docker
```

</div>

<div label="Windows" value="Windows">

- 下载并安装 Git。

    1. 从 [Git Windows Download](https://git-scm.com/download/win) 页面下载 **64-bit Git for Windows Setup** 安装包。
    2. 按照安装向导安装 Git。你可以多次点击 **Next** 使用默认安装设置。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

- 下载并安装 MySQL Shell。

    1. 从 [MySQL Community Server Download](https://dev.mysql.com/downloads/mysql/) 页面下载 MySQL Installer 的 ZIP 文件。
    2. 解压文件，在 `bin` 文件夹中找到 `mysql.exe`。你需要将 `bin` 文件夹的路径添加到系统变量，并在 Git Bash 中设置到 `PATH` 变量：

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        例如：

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

- 下载并安装 Docker。

    1. 从 [Docker Download](https://www.docker.com/products/docker-desktop/) 页面下载 Docker Desktop 安装包。
    2. 双击安装包进行安装。安装完成后会提示重启。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

- 从 [Python Download](https://www.python.org/downloads/) 页面下载最新版 Python 3 安装包并运行。

</div>

</SimpleTab>

### 方案 1：集成 TiDB Cloud 与 ProxySQL

在本集成方案中，你将使用 [ProxySQL Docker 镜像](https://hub.docker.com/r/proxysql/proxysql) 和 TiDB Cloud Starter 集群。以下步骤会将 ProxySQL 设置在 `16033` 端口，请确保该端口可用。

#### 步骤 1. 创建 TiDB Cloud Starter 集群

1. [创建一个免费的 TiDB Cloud Starter 集群](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)。记住你为集群设置的 root 密码。
2. 获取你的集群主机名、端口和用户名，供后续使用。

    1. 在 [Clusters](https://tidbcloud.com/console/clusters) 页面，点击你的集群名称进入集群概览页。
    2. 在集群概览页，找到 **Connection** 面板，复制 `Endpoint`、`Port` 和 `User` 字段，其中 `Endpoint` 即为你的集群主机名。

#### 步骤 2. 生成 ProxySQL 配置文件

1. 克隆 TiDB 与 ProxySQL 的 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

2. 进入 `tidb-cloud-connect` 文件夹：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    </SimpleTab>

3. 运行 `proxysql-config.py` 生成 ProxySQL 配置文件：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-config.py
    ```

    </div>

    </SimpleTab>

    按提示输入你的集群 endpoint 作为 `Serverless Tier Host`，然后输入集群的用户名和密码。

    以下为示例输出。你会看到在当前 `tidb-cloud-connect` 文件夹下生成了三个配置文件。

    ```
    [Begin] generating configuration files..
    tidb-cloud-connect.cnf generated successfully.
    proxysql-prepare.sql generated successfully.
    proxysql-connect.py generated successfully.
    [End] all files generated successfully and placed in the current folder.
    ```

#### 步骤 3. 配置 ProxySQL

1. 启动 Docker。如果 Docker 已启动可跳过此步：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 图标启动。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 图标启动。

    </div>

    </SimpleTab>

2. 拉取 ProxySQL 镜像并在后台启动 ProxySQL 容器：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

3. 通过以下命令集成 ProxySQL，在 **ProxySQL Admin Interface** 内执行 `proxysql-prepare.sql`：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    </SimpleTab>

    > **注意：**
    >
    > `proxysql-prepare.sql` 脚本执行以下操作：
    >
    > 1. 使用你的集群用户名和密码添加用户。
    > 2. 将该用户分配给监控账户。
    > 3. 将你的 TiDB Cloud Starter 集群添加到主机列表。
    > 4. 启用 ProxySQL 与 TiDB Cloud Starter 集群之间的安全连接。
    >
    > 建议你查阅 `proxysql-prepare.sql` 文件以深入了解。更多 ProxySQL 配置内容，参见 [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/)。

    以下为示例输出。你会看到输出中显示了你的集群主机名，说明 ProxySQL 与 TiDB Cloud Starter 集群的连通性已建立。

    ```
    *************************** 1. row ***************************
        hostgroup_id: 0
            hostname: gateway01.us-west-2.prod.aws.tidbcloud.com
                port: 4000
            gtid_port: 0
                status: ONLINE
                weight: 1
            compression: 0
        max_connections: 1000
    max_replication_lag: 0
                use_ssl: 1
        max_latency_ms: 0
                comment:
    ```

#### 步骤 4. 通过 ProxySQL 连接 TiDB 集群

1. 运行 `proxysql-connect.py` 连接 TiDB 集群。该脚本会自动启动 MySQL 客户端，并使用你在 [步骤 2](#step-2-generate-proxysql-configuration-files) 指定的用户名和密码进行连接。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-connect.py
    ```

    </div>

    </SimpleTab>

2. 连接到 TiDB 集群后，可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果显示 TiDB 版本，说明你已通过 ProxySQL 成功连接到 TiDB Cloud Starter 集群。随时输入 `quit` 并按 <kbd>enter</kbd> 退出 MySQL 客户端。

    > **注意：**
    >
    > ***调试提示：*** 如果无法连接集群，请检查 `tidb-cloud-connect.cnf`、`proxysql-prepare.sql` 和 `proxysql-connect.py` 文件，确保你提供的服务器信息可用且正确。

3. 停止并移除容器，并返回上级目录，运行以下命令：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

### 方案 2：集成 TiDB（自托管）与 ProxySQL

在本集成方案中，你将使用 [TiDB](https://hub.docker.com/r/pingcap/tidb) 和 [ProxySQL](https://hub.docker.com/r/proxysql/proxysql) 的 Docker 镜像搭建环境。你也可以根据兴趣尝试 [其他 TiDB（自托管）安装方式](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)。

以下步骤会将 ProxySQL 和 TiDB 分别设置在 `6033` 和 `4000` 端口，请确保这些端口可用。

1. 启动 Docker。如果 Docker 已启动可跳过此步：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    双击已安装的 Docker 图标启动。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    双击已安装的 Docker 图标启动。

    </div>

    </SimpleTab>

2. 克隆 TiDB 与 ProxySQL 的 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

3. 拉取 ProxySQL 和 TiDB 的最新镜像：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    </SimpleTab>

4. 启动包含 TiDB 和 ProxySQL 的集成环境（以容器方式运行）：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

    登录 ProxySQL `6033` 端口时，可使用 `root` 用户名和空密码。

5. 通过 ProxySQL 连接 TiDB：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    </SimpleTab>

6. 连接到 TiDB 集群后，可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果显示 TiDB 版本，说明你已通过 ProxySQL 成功连接到 TiDB 容器。

7. 停止并移除容器，并返回上级目录，运行以下命令：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

## 生产环境

在生产环境中，建议你直接使用 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated/)，以获得全托管体验。

### 前置条件

下载并安装 MySQL 客户端。例如 [MySQL Shell](https://dev.mysql.com/downloads/shell/)。

### 在 CentOS 上集成 TiDB Cloud 与 ProxySQL

ProxySQL 可在多种平台上安装。以下以 CentOS 为例。

完整支持平台及对应版本要求，参见 [ProxySQL documentation](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 1. 创建 TiDB Cloud Dedicated 集群

详细步骤参见 [Create a TiDB Cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)。

#### 步骤 2. 安装 ProxySQL

1. 将 ProxySQL 添加到 YUM 仓库：

    ```bash
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. 安装 ProxySQL：

    ```bash
    yum install -y proxysql
    ```

3. 启动 ProxySQL：

    ```bash
    systemctl start proxysql
    ```

更多 ProxySQL 支持平台及安装方法，参见 [ProxySQL README](https://github.com/sysown/proxysql#installation) 或 [ProxySQL installation documentation](https://proxysql.com/documentation/installing-proxysql/)。

#### 步骤 3. 配置 ProxySQL

要将 ProxySQL 作为 TiDB 的代理，需要对 ProxySQL 进行配置。你可以选择 [在 ProxySQL Admin Interface 内执行 SQL 语句](#option-1-configure-proxysql-using-the-admin-interface)（推荐），或使用 [配置文件](#option-2-configure-proxysql-using-a-configuration-file)。

> **注意：**
>
> 以下仅列出 ProxySQL 的必要配置项。
> 完整配置项列表参见 [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/)。

##### 方案 1：通过 Admin Interface 配置 ProxySQL

1. 通过标准 ProxySQL Admin interface 重新配置 ProxySQL 内部，可通过任意 MySQL 命令行客户端访问（默认端口为 `6032`）：

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上述操作会进入 ProxySQL admin 提示符。

2. 配置要使用的 TiDB 集群，可向 ProxySQL 添加一个或多个 TiDB 集群。以下语句以添加一个 TiDB Cloud Dedicated 集群为例。你需要将 `<tidb cloud dedicated cluster host>` 和 `<tidb cloud dedicated cluster port>` 替换为你的 TiDB Cloud endpoint 和端口（默认端口为 `4000`）。

    ```sql
    INSERT INTO mysql_servers(hostgroup_id, hostname, port) 
    VALUES 
      (
        0,
        '<tidb cloud dedicated cluster host>', 
        <tidb cloud dedicated cluster port>
      );
    LOAD mysql servers TO runtime;
    SAVE mysql servers TO DISK;
    ```

    > **注意：**
    >
    > - `hostgroup_id`：指定主机组 ID。ProxySQL 通过主机组管理集群。若需将 SQL 流量均匀分发到这些集群，可将需要负载均衡的多个集群配置到同一主机组。若需区分集群（如读写分离），可配置不同主机组。
    > - `hostname`：TiDB 集群的 endpoint。
    > - `port`：TiDB 集群的端口。

3. 配置 Proxy 登录用户，确保用户在 TiDB 集群上有适当权限。以下语句中，需将 '*tidb cloud dedicated cluster username*' 和 '*tidb cloud dedicated cluster password*' 替换为实际的集群用户名和密码。

    ```sql
    INSERT INTO mysql_users(
      username, password, active, default_hostgroup, 
      transaction_persistent
    ) 
    VALUES 
      (
        '<tidb cloud dedicated cluster username>', 
        '<tidb cloud dedicated cluster password>', 
        1, 0, 1
      );
    LOAD mysql users TO runtime;
    SAVE mysql users TO DISK;
    ```

    > **注意：**
    >
    > - `username`：TiDB 用户名。
    > - `password`：TiDB 密码。
    > - `active`：控制用户是否激活。`1` 表示**激活**，可用于登录，`0` 表示未激活。
    > - `default_hostgroup`：用户默认使用的主机组，SQL 流量会分发到该主机组，除非查询规则将流量重定向到特定主机组。
    > - `transaction_persistent`：`1` 表示持久事务。当用户在连接中开启事务时，所有查询语句都会路由到同一主机组，直到事务提交或回滚。

##### 方案 2：通过配置文件配置 ProxySQL

此方案仅作为配置 ProxySQL 的备选方法。更多信息参见 [Configuring ProxySQL through the config file](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)。

1. 删除现有 SQLite 数据库（配置会存储于此）：

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > 删除 SQLite 数据库文件后，所有通过 ProxySQL Admin interface 做的配置更改都会丢失。

2. 按需修改 `/etc/proxysql.cnf` 配置文件。例如：

    ```
    mysql_servers:
    (
        {
            address="<tidb cloud dedicated cluster host>"
            port=<tidb cloud dedicated cluster port>
            hostgroup=0
            max_connections=2000
        }
    )

    mysql_users:
    (
        {
            username = "<tidb cloud dedicated cluster username>"
            password = "<tidb cloud dedicated cluster password>"
            default_hostgroup = 0
            max_connections = 1000
            default_schema = "test"
            active = 1
            transaction_persistent = 1
        }
    )
    ```

    上述示例中：

    - `address` 和 `port`：指定 TiDB Cloud 集群的 endpoint 和端口。
    - `username` 和 `password`：指定 TiDB Cloud 集群的用户名和密码。

3. 重启 ProxySQL：

    ```bash
    systemctl restart proxysql
    ```

    重启后，SQLite 数据库会自动创建。

> **警告：**
>
> 生产环境中请勿使用默认凭据运行 ProxySQL。在启动 `proxysql` 服务前，可在 `/etc/proxysql.cnf` 文件中通过修改 `admin_credentials` 变量更改默认值。

## 典型场景

本节以查询路由为例，展示集成 ProxySQL 与 TiDB 后可获得的一些优势。

### 查询规则

数据库可能因高并发、错误代码或恶意垃圾流量而过载。通过 ProxySQL 的查询规则，你可以快速有效地应对这些问题，实现查询的重定向、重写或拒绝。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注意：**
>
> 以下步骤将使用 TiDB 和 ProxySQL 的容器镜像配置查询规则。如果你尚未拉取镜像，可参考 [集成部分](#option-2-integrate-tidb-self-hosted-with-proxysql) 获取详细步骤。

1. 克隆 TiDB 与 ProxySQL 的 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)。如已在前述步骤中克隆可跳过。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    </SimpleTab>

2. 进入 ProxySQL 规则示例目录：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    </SimpleTab>

3. 运行以下命令，启动两个 TiDB 容器和一个 ProxySQL 容器：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

    </SimpleTab>

    如果一切正常，将启动以下容器：

    - 两个 TiDB 集群的 Docker 容器，分别暴露端口 `4001`、`4002`
    - 一个 ProxySQL Docker 容器，暴露端口 `6034`

4. 在两个 TiDB 容器中，使用 `mysql` 创建结构相同的表，并插入不同数据（`'tidb-server01-port-4001'`、`'tidb-server02-port-4002'`）以区分容器。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    </SimpleTab>

5. 运行以下命令配置 ProxySQL，在 ProxySQL Admin Interface 内执行 `proxysql-prepare.sql`，建立 TiDB 容器与 ProxySQL 的代理连接。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    </SimpleTab>

    > **注意：**
    >
    > `proxysql-prepare.sql` 执行以下操作：
    >
    > - 在 ProxySQL 中添加 TiDB 集群，`hostgroup_id` 分别为 `0` 和 `1`。
    > - 添加用户 `root`，空密码，`default_hostgroup` 设为 `0`。
    > - 添加规则 `^SELECT.*FOR UPDATE$`，`rule_id` 为 `1`，`destination_hostgroup` 为 `0`。若 SQL 语句匹配该规则，请求将转发到 `hostgroup` 为 `0` 的 TiDB 集群。
    > - 添加规则 `^SELECT`，`rule_id` 为 `2`，`destination_hostgroup` 为 `1`。若 SQL 语句匹配该规则，请求将转发到 `hostgroup` 为 `1` 的 TiDB 集群。
    >
    > 建议你查阅 `proxysql-prepare.sql` 文件以深入了解。更多 ProxySQL 配置内容，参见 [ProxySQL documentation](https://proxysql.com/documentation/proxysql-configuration/)。

    以下是 ProxySQL 匹配查询规则的补充说明：

    - ProxySQL 会按 `rule_id` 的正序逐条匹配规则。
    - `^` 符号匹配 SQL 语句开头，`$` 匹配结尾。

    更多 ProxySQL 正则表达式与模式匹配内容，参见 ProxySQL 文档 [mysql-query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)。

    全部参数列表参见 [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)。

6. 验证配置并检查查询规则是否生效。

    1. 以 `root` 用户登录 ProxySQL MySQL Interface：

        <SimpleTab groupId="os">

        <div label="macOS" value="macOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="CentOS" value="CentOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="Windows (Git Bash)" value="Windows">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        </SimpleTab>

    2. 执行以下 SQL 语句：

        - 执行 `SELECT` 语句：

            ```sql
            SELECT * FROM test.tidb_server;
            ```

            该语句会匹配 rule_id `2`，并转发到 `hostgroup 1` 的 TiDB 集群。

        - 执行 `SELECT ... FOR UPDATE` 语句：

            ```sql
            SELECT * FROM test.tidb_server FOR UPDATE;
            ```

            该语句会匹配 rule_id `1`，并转发到 `hostgroup 0` 的 TiDB 集群。

        - 开启一个事务：

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            在该事务中，`BEGIN` 语句不会匹配任何规则，使用默认主机组（本例为 `hostgroup 0`）。由于 ProxySQL 默认启用用户 transaction_persistent，事务内所有语句都会在同一主机组执行，因此 `INSERT` 和 `SELECT * FROM test.tidb_server;` 也会转发到 `hostgroup 0` 的 TiDB 集群。

        以下为示例输出。如果你获得类似输出，说明已成功配置 ProxySQL 查询规则。

        ```sql
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server02-port-4002 |
        +-------------------------+
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server01-port-4001 |
        +-------------------------+
        +--------------------------------+
        | server_name                    |
        +--------------------------------+
        | tidb-server01-port-4001        |
        | insert this and rollback later |
        +--------------------------------+
        ```

    3. 随时输入 `quit` 并按 <kbd>enter</kbd> 退出 MySQL 客户端。

7. 停止并移除容器，并返回上级目录，运行以下命令：

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    </SimpleTab>

## 需要帮助？

- 在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问。
- [提交 TiDB Cloud 支持工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 自托管支持工单](/support.md)
