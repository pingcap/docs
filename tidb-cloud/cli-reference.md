---
title: TiDB Cloud CLI 参考
summary: 提供 TiDB Cloud CLI 的概览。
---

# TiDB Cloud CLI 参考（Beta）

> **Note:**
>
> 目前，TiDB Cloud CLI 处于 beta 阶段，暂不适用于 TiDB Cloud Dedicated 集群。

TiDB Cloud CLI 是一个命令行界面，允许你通过几行命令在终端中操作 TiDB Cloud。在 TiDB Cloud CLI 中，你可以轻松管理 TiDB Cloud 集群、向集群导入数据以及执行更多操作。

## 开始之前

请确保你已先[完成 TiDB Cloud CLI 环境的设置](/tidb-cloud/get-started-with-cli.md)。安装好 `ticloud` CLI 后，你就可以通过命令行管理 TiDB Cloud 集群。

## 可用命令

下表列出了 TiDB Cloud CLI 支持的命令。

要在终端中使用 `ticloud` CLI，请运行 `ticloud [command] [subcommand]`。如果你在使用 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)，请改用 `tiup cloud [command] [subcommand]`。

| Command               | Subcommand                                                            | Description                                    |
|-----------------------|-----------------------------------------------------------------------|------------------------------------------------|
| auth                  | login, logout, whoami                                                 | 登录与登出                                     |
| serverless (alias: s) | create, delete, describe, list, update, spending-limit, region, shell | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群          |
| serverless branch     | create, delete, describe, list, shell                                 | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的分支          |
| serverless import     | cancel, describe, list, start                                         | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的导入任务      |
| serverless export     | create, describe, list, cancel, download                              | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的导出任务      |
| serverless sql-user   | create, list, delete, update                                          | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的 SQL 用户         |
| serverless audit-log  | config, describe, filter-rule (alias: filter), download                                    | 管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据库审计日志         |
| completion            | bash, fish, powershell, zsh                                           | 为指定 shell 生成补全脚本                     |
| config                | create, delete, describe, edit, list, set, use                        | 配置用户配置文件                               |
| project               | list                                                                  | 管理项目                                       |
| upgrade               | -                                                                     | 将 CLI 升级到最新版本                          |
| help                  | auth, config, serverless, project, upgrade, help, completion          | 查看任意命令的帮助文档                         |

## 命令模式

TiDB Cloud CLI 针对部分命令提供了两种模式，便于使用：

- 交互模式

    你可以在不带参数的情况下运行命令（如 `ticloud config create`），CLI 会提示你输入相关信息。

- 非交互模式

    你需要在运行命令时提供所有必需的参数和选项，例如 `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`。

## 用户配置文件

对于 TiDB Cloud CLI，用户配置文件是与用户相关的一组属性，包括配置文件名、公钥、私钥和 OAuth token。要使用 TiDB Cloud CLI，你必须拥有一个用户配置文件。

### 使用 TiDB Cloud API key 创建用户配置文件

使用 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 创建用户配置文件。

### 使用 OAuth token 创建用户配置文件

使用 [`ticloud auth login`](/tidb-cloud/ticloud-auth-login.md) 为当前配置文件分配 OAuth token。如果不存在任何配置文件，则会自动创建一个名为 `default` 的配置文件。

> **Note:**
>
> 在上述两种方式中，TiDB Cloud API key 的优先级高于 OAuth token。如果当前配置文件中同时存在两者，将优先使用 API key。

### 列出所有用户配置文件

使用 [`ticloud config list`](/tidb-cloud/ticloud-config-list.md) 列出所有用户配置文件。

示例输出如下：

```
Profile Name
default (active)
dev
staging
```

在此示例输出中，`default` 用户配置文件为当前激活状态。

### 查看用户配置文件详情

使用 [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md) 获取用户配置文件的属性。

示例输出如下：

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### 设置用户配置文件属性

使用 [`ticloud config set`](/tidb-cloud/ticloud-config-set.md) 设置用户配置文件中的属性。

### 切换到其他用户配置文件

使用 [`ticloud config use`](/tidb-cloud/ticloud-config-use.md) 切换到其他用户配置文件。

示例输出如下：

```
Current profile has been changed to default
```

### 编辑配置文件

使用 [`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md) 打开配置文件进行编辑。

### 删除用户配置文件

使用 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) 删除用户配置文件。

## 全局参数

下表列出了 TiDB Cloud CLI 的全局参数。

| Flag                 | Description                                             | Required | Note                                                                                                             |
|----------------------|---------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                      | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定本次命令使用的激活用户配置文件。                    | 否       | 适用于非交互模式和交互模式。                                                                                     |
| -D, --debug          | 启用调试模式                                            | 否       | 适用于非交互模式和交互模式。                                                                                  |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎在 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose) 页面提交。同时，我们也欢迎任何贡献。