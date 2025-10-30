---
title: 构建 TiDB Cloud Starter 集群
summary: 了解如何在 TiDB Cloud 中构建 TiDB Cloud Starter 集群并连接到它。
---

<!-- markdownlint-disable MD029 -->

# 构建 TiDB Cloud Starter 集群

<CustomContent platform="tidb">

本文档将带你快速上手 TiDB。你将使用 [TiDB Cloud](https://www.pingcap.com/tidb-cloud) 创建一个 TiDB Cloud Starter 集群，连接到它，并在其上运行一个示例应用程序。

如果你需要在本地机器上运行 TiDB，请参见 [本地启动 TiDB](/quick-start-with-tidb.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

本文档将带你快速上手 TiDB Cloud。你将创建一个 TiDB 集群，连接到它，并在其上运行一个示例应用程序。

</CustomContent>

## 第 1 步. 创建 TiDB Cloud Starter 集群 {#step-1-create-a-tidb-cloud-cluster}

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册账号。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

3. 在 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击 **Create Cluster**。

4. 在 **Create Cluster** 页面，**Starter** 默认已选中。如有需要，可修改默认集群名称，然后选择你希望创建集群的区域。

5. 点击 **Create** 创建 TiDB Cloud Starter 集群。

    你的 TiDB Cloud 集群将在大约 30 秒内创建完成。

6. 集群创建完成后，点击你的集群名称进入集群概览页面，然后点击右上角的 **Connect**。此时会弹出连接对话框。

7. 在对话框中，选择你偏好的连接方式和操作系统，以获取对应的连接字符串。本文档以 MySQL 客户端为例。

8. 点击 **Generate Password** 生成一个随机密码。生成的密码只会显示一次，请妥善保存。如果你未设置 root 密码，将无法连接到集群。

<CustomContent platform="tidb">

> **注意：**
>
> 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 集群，连接集群时，必须在用户名中包含集群的前缀，并用引号包裹用户名。更多信息请参见 [用户名前缀](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 集群，连接集群时，必须在用户名中包含集群的前缀，并用引号包裹用户名。更多信息请参见 [用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

</CustomContent>

## 第 2 步. 连接到集群

1. 如果未安装 MySQL 客户端，请选择你的操作系统并按照以下步骤安装。

<SimpleTab>

<div label="macOS">

对于 macOS，如果你还没有安装 [Homebrew](https://brew.sh/index)，请先安装，然后运行以下命令安装 MySQL 客户端：

```shell
brew install mysql-client
```

输出如下：

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

要将 MySQL 客户端添加到 PATH，请在上述输出中找到以下命令（如果你的输出与本文档中的输出不一致，请使用你输出中的对应命令）并运行：

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

然后，通过 `source` 命令声明全局环境变量，并验证 MySQL 客户端是否安装成功：

```shell
source ~/.zshrc
mysql --version
```

预期输出示例：

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

对于 Linux，这里以 Ubuntu 为例：

```shell
apt-get install mysql-client
```

然后，验证 MySQL 客户端是否安装成功：

```shell
mysql --version
```

预期输出示例：

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. 运行在[第 1 步](#step-1-create-a-tidb-cloud-cluster)中获取的连接字符串。

    
    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **注意：**
>
> - 连接 TiDB Cloud Starter 集群时，必须[使用 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)。
> - 如果在连接 TiDB Cloud Starter 集群时遇到问题，可以参考 [安全连接到 TiDB Cloud Starter 集群](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) 获取更多信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 连接 TiDB Cloud Starter 集群时，必须[使用 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
> - 如果在连接 TiDB Cloud Starter 集群时遇到问题，可以参考 [安全连接到 TiDB Cloud Starter 集群](/tidb-cloud/secure-connections-to-serverless-clusters.md) 获取更多信息。

</CustomContent>

3. 输入密码进行登录。

## 第 3 步. 执行 SQL 语句

让我们尝试在 TiDB Cloud 上执行你的第一条 SQL 语句。

```sql
SELECT 'Hello TiDB Cloud!';
```

预期输出：

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

如果你的实际输出与预期输出类似，恭喜你，已经在 TiDB Cloud 上成功执行了一条 SQL 语句。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
