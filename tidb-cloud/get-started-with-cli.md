---
title: TiDB Cloud CLI 快速入门
summary: 了解如何通过 TiDB Cloud CLI 管理 TiDB Cloud 资源。
---

# TiDB Cloud CLI 快速入门

TiDB Cloud 提供了一个命令行界面（CLI）[`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)，你可以通过在终端输入几行命令与 TiDB Cloud 进行交互。例如，你可以使用 `ticloud` 轻松完成以下操作：

- 创建、删除和列出你的集群。
- 向你的集群导入数据。
- 从你的集群导出数据。

> **Note:**
>
> TiDB Cloud CLI 目前处于 beta 阶段。

## 开始之前

- 拥有一个 TiDB Cloud 账号。如果你还没有账号，请[注册免费试用](https://tidbcloud.com/free-trial)。

## 安装

<SimpleTab>
<div label="macOS/Linux">

对于 macOS 或 Linux，你可以通过以下任意一种方式安装 `ticloud`：

- 通过脚本安装（推荐）

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

- 通过 [TiUP](https://tiup.io/) 安装

    ```shell
    tiup install cloud
    ```

- 手动安装

    从 [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) 页面下载预编译的二进制文件，并将其复制到你希望安装的位置。

- 在 GitHub Actions 中安装

    如果需要在 GitHub Action 中设置 `ticloud`，请使用 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)。

如果你还没有安装 MySQL 命令行客户端，可以通过包管理器进行安装：

- 基于 Debian 的发行版：

    ```shell
    sudo apt-get install mysql-client
    ```

- 基于 RPM 的发行版：

    ```shell
    sudo yum install mysql
    ```

- macOS：

  ```shell
  brew install mysql-client
  ```

</div>

<div label="Windows">

对于 Windows，你可以通过以下任意一种方式安装 `ticloud`：

- 手动安装

    从 [releases](https://github.com/tidbcloud/tidbcloud-cli/releases/latest) 页面下载预编译的二进制文件，并将其复制到你希望安装的位置。

- 在 GitHub Actions 中安装

    如果需要在 GitHub Actions 中设置 `ticloud`，请使用 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)。

如果你还没有安装 MySQL 命令行客户端，可以参考 [MySQL Installer for Windows](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html) 中的安装说明。要在 Windows 上启动 `ticloud connect`，你需要将包含 `mysql.exe` 的目录添加到 PATH 环境变量中。

</div>
</SimpleTab>

## 快速入门

[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 是开始使用 TiDB Cloud 的最佳方式。本节将介绍如何使用 TiDB Cloud CLI 创建一个 TiDB Cloud Starter 集群。

### 创建用户配置文件或登录 TiDB Cloud

在使用 TiDB Cloud CLI 创建集群之前，你需要先创建用户配置文件或登录 TiDB Cloud。

- 使用你的 [TiDB Cloud API key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) 创建用户配置文件：

    ```shell
    ticloud config create
    ```

    > **Warning:**
    >
    > 配置文件名 **MUST NOT** 包含 `.`。

- 通过认证登录 TiDB Cloud：

    ```shell
    ticloud auth login
    ```

    登录成功后，OAuth token 会分配给当前配置文件。如果没有配置文件，token 会分配给名为 `default` 的配置文件。

> **Note:**
>
> 在上述两种方式中，TiDB Cloud API key 的优先级高于 OAuth token。如果两者都存在，将优先使用 API key。

### 创建 TiDB Cloud Starter 集群

要创建 TiDB Cloud Starter 集群，输入以下命令，并根据 CLI 提示填写所需信息：

```shell
ticloud serverless create
```

## 使用 TiDB Cloud CLI

查看所有可用命令：

```shell
ticloud --help
```

验证你使用的是最新版本：

```shell
ticloud version
```

如果不是最新版本，请更新到最新版：

```shell
ticloud update
```

### 通过 TiUP 使用 TiDB Cloud CLI

TiDB Cloud CLI 也可以通过 [TiUP](https://tiup.io/) 使用，组件名称为 `cloud`。

查看所有可用命令：

```shell
tiup cloud --help
```

使用 `tiup cloud <command>` 运行命令。例如：

```shell
tiup cloud serverless create
```

通过 TiUP 更新到最新版：

```shell
tiup update cloud
```

## 后续操作

查阅 [CLI 参考](/tidb-cloud/cli-reference.md) 以探索 TiDB Cloud CLI 的更多功能。

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时也欢迎任何贡献。