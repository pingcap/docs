---
title: ProxySQL 集成指南
summary: 了解如何将 TiDB Cloud 和 TiDB（自托管）与 ProxySQL 集成。
---

# 将 TiDB 与 ProxySQL 集成

本文档提供了对 ProxySQL 的高层次介绍，描述了如何在 [开发环境](#development-environment) 和 [生产环境](#production-environment)中将 ProxySQL 与 TiDB 集成，并通过 [查询路由的典型场景](#typical-scenario)演示了主要的集成优势。

如果你有兴趣了解更多关于 TiDB 和 ProxySQL 的信息，可以参考以下一些有用的链接：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
- [TiDB 开发者指南](/develop/dev-guide-overview.md)
- [ProxySQL 文档](https://proxysql.com/documentation/)

## 什么是 ProxySQL？

[ProxySQL](https://proxysql.com/) 是一个高性能的开源 SQL 代理。它具有灵活的架构，可以以多种不同方式部署，非常适合各种用例。例如，ProxySQL 可以通过缓存频繁访问的数据来提升性能。

ProxySQL 从设计之初就追求快速、高效、易用。它与 MySQL 完全兼容，支持你期望的所有高质量 SQL 代理功能。此外，ProxySQL 还具有一些独特的功能，使其成为广泛应用的理想选择。

## 为什么要集成 ProxySQL？

- ProxySQL 可以通过减少与 TiDB 交互时的延迟，帮助提升应用性能。无论你在构建什么样的应用，无论是使用无服务器函数（如 Lambda）实现的可扩展应用（工作负载具有不确定性且可能出现峰值），还是执行大量数据加载查询的应用，利用 ProxySQL 的强大功能如 [连接池](https://proxysql.com/documentation/detailed-answers-on-faq/) 和 [频繁查询缓存](https://proxysql.com/documentation/query-cache/)，都能立即获得好处。
- ProxySQL 可以作为额外的应用安全层，防御 SQL 漏洞（如 SQL 注入），借助 ProxySQL 提供的 [查询规则](#query-rules)，这是一个易于配置的功能。
- 由于 [ProxySQL](https://github.com/sysown/proxysql) 和 [TiDB](https://github.com/pingcap/tidb) 都是开源项目，你可以享受到零供应商锁定的优势。

## 部署架构

将 ProxySQL 与 TiDB 部署的最常见方式是将 ProxySQL 作为应用层与 TiDB 之间的独立中介。然而，这种方式的可扩展性和容错性无法得到保证，而且由于网络跳转，还会增加额外的延迟。为避免这些问题，另一种部署架构是将 ProxySQL 作为 sidecar 部署，示意如下：

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **Note:**
>
> 上述示意图仅供参考。你必须根据实际部署架构进行调整。

## 开发环境

本节介绍在开发环境中如何将 TiDB 与 ProxySQL 集成。要开始 ProxySQL 集成，你可以在满足所有 [前提条件](#prerequisite) 后，根据你的 TiDB 集群类型选择以下任意一种方案。

- Option 1: [将 TiDB Cloud 与 ProxySQL 集成](#option-1-integrate-tidb-cloud-with-proxysql)
- Option 2: [将 TiDB（自托管）与 ProxySQL 集成](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前提条件

根据你选择的方案，可能需要以下软件包：

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)
- [Docker Compose](https://docs.docker.com/compose/install/linux/)
- [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

你可以按照以下安装说明操作：

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1. [下载](https://docs.docker.com/get-docker/) 并启动 Docker（Docker Desktop 已包含 Docker Compose）。
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

    1. 从 [Git Windows 下载](https://git-scm.com/download/win) 页面下载 **64-bit Git for Windows Setup** 包。
    2. 按照安装向导完成安装，点击 **Next** 多次使用默认设置。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

- 下载并安装 MySQL Shell。

    1. 从 [MySQL 社区服务器下载](https://dev.mysql.com/downloads/mysql/) 页面下载 ZIP 格式的 MySQL 安装包。
    2. 解压后，找到 `mysql.exe` 在 `bin` 文件夹中。需要将 `bin` 文件夹的路径添加到系统变量中，并在 Git Bash 中设置到 `PATH` 变量：

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

    1. 从 [Docker 下载](https://www.docker.com/products/docker-desktop/) 页面下载 Docker Desktop 安装包。
    2. 双击运行安装程序，安装完成后会提示重启。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

- 下载最新的 Python 3 安装包，从 [Python 下载](https://www.python.org/downloads/) 页面下载安装。

</div>

</SimpleTab>

### Option 1: 将 TiDB Cloud 与 ProxySQL 集成

在此方案中，你将使用 [ProxySQL Docker 镜像](https://hub.docker.com/r/proxysql/proxysql) 和一个 {{{ .starter }}} 集群。以下步骤将会在端口 `16033` 上部署 ProxySQL，请确保此端口可用。

#### 步骤 1. 创建一个 {{{ .starter }}} 集群

1. [创建一个免费 {{{ .starter }}} 集群](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)。记住你为集群设置的 root 密码。
2. 获取你的集群主机名、端口和用户名，备用。

    1. 在 [Clusters](https://tidbcloud.com/project/clusters) 页面，点击你的集群名称进入集群概览页面。
    2. 在集群概览页面，找到 **Connection** 面板，复制 `Endpoint`、`Port` 和 `User` 字段，其中 `Endpoint` 即为你的集群主机名。

#### 步骤 2. 生成 ProxySQL 配置文件

1. 克隆 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

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

2. 切换到 `tidb-cloud-connect` 文件夹：

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

    提示时，输入你的集群端点作为 `Serverless Tier Host`，然后输入集群的用户名和密码。

    以下为示例输出，你会看到在当前 `tidb-cloud-connect` 文件夹下生成了三个配置文件。

    ```
    [Begin] generating configuration files..
    tidb-cloud-connect.cnf generated successfully.
    proxysql-prepare.sql generated successfully.
    proxysql-connect.py generated successfully.
    [End] all files generated successfully and placed in the current folder.
    ```

#### 步骤 3. 配置 ProxySQL

1. 启动 Docker。如果 Docker 已经启动，可以跳过此步骤：

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

2. 拉取 ProxySQL 镜像并在后台启动一个 ProxySQL 容器：

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

3. 通过运行以下命令，将 `proxysql-prepare.sql` 在 **ProxySQL 管理界面** 内执行，从而集成配置：

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

    > **Note:**
    >
    > `proxysql-prepare.sql` 脚本执行的内容包括：
    >
    > 1. 添加一个用户，用户名和密码为你的集群信息。
    > 2. 将用户分配到监控账户。
    > 3. 将你的 {{{ .starter }}} 集群添加到主机列表中。
    > 4. 启用 ProxySQL 与 {{{ .starter }}} 集群之间的安全连接。
    >
    > 为了更好理解，强烈建议你查看 `proxysql-prepare.sql` 文件。关于 ProxySQL 配置的更多信息，请参见 [ProxySQL 文档](https://proxysql.com/documentation/proxysql-configuration/)。

    以下为示例输出，你会看到你的集群主机名显示在输出中，表示 ProxySQL 与 {{{ .starter }}} 集群的连接已建立。

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

#### 步骤 4. 通过 ProxySQL 连接你的 TiDB 集群

1. 运行 `proxysql-connect.py`，脚本会自动启动 MySQL 客户端，并使用你在 [步骤 2](#step-2-generate-proxysql-configuration-files) 中指定的用户名和密码进行连接。

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

2. 连接到 TiDB 后，可以使用以下 SQL 语句验证连接是否成功：

    ```sql
    SELECT VERSION();
    ```

    如果显示出 TiDB 版本信息，说明你已成功通过 ProxySQL 连接到你的 {{{ .starter }}} 集群。随时可以输入 `quit` 并按 <kbd>enter</kbd> 退出 MySQL 客户端。

    > **Note:**
    >
    > ***调试用：*** 如果无法连接到集群，请检查 `tidb-cloud-connect.cnf`、`proxysql-prepare.sql` 和 `proxysql-connect.py` 文件，确保你提供的服务器信息正确无误。

3. 若要停止并删除容器，返回上级目录，运行以下命令：

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

## 其他方案：将 TiDB（自托管）与 ProxySQL 集成

此方案中，你将使用 [TiDB](https://hub.docker.com/r/pingcap/tidb) 和 [ProxySQL](https://hub.docker.com/r/proxysql/proxysql) 的 Docker 镜像搭建环境。你也可以尝试 [其他安装 TiDB（自托管）的方法](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)。

以下步骤将在端口 `6033` 和 `4000` 上部署 ProxySQL 和 TiDB，确保这些端口可用。

1. 启动 Docker。如果 Docker 已经启动，可以跳过此步骤：

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

2. 克隆 [集成示例代码仓库](https://github.com/pingcap-inc/tidb-proxysql-integration)：

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

3. 拉取最新的 ProxySQL 和 TiDB 镜像：

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

4. 启动包含 TiDB 和 ProxySQL 的集成环境：

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

    你可以使用 `root` 用户名，空密码登录 ProxySQL `6033` 端口。

5. 连接到 TiDB 通过 ProxySQL：

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

6. 连接到你的 TiDB 集群后，可以使用以下 SQL 语句验证连接：

    ```sql
    SELECT VERSION();
    ```

    如果显示出 TiDB 版本信息，说明你已成功通过 ProxySQL 连接到你的 TiDB 容器。

7. 停止并删除容器，返回上级目录，运行：

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