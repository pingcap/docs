---
title: TiDB Cloud CLI 参考手册
summary: 提供 TiDB Cloud CLI 的概述。
---

# TiDB Cloud CLI 参考手册 (Beta)

> **Note:**
>
> TiDB Cloud CLI 处于测试阶段。

TiDB Cloud CLI 是一个命令行界面，允许你通过终端使用少量命令操作 TiDB Cloud。在 TiDB Cloud CLI 中，你可以轻松管理你的 TiDB Cloud 集群、导入数据到集群，以及执行更多操作。

## 在开始之前

请确保先[设置你的 TiDB Cloud CLI 环境](/tidb-cloud/get-started-with-cli.md)。安装好 `ticloud` CLI 后，你就可以通过命令行管理你的 TiDB Cloud 集群。

## 可用命令

下表列出了 TiDB Cloud CLI 支持的命令。

在终端中使用 `ticloud [command] [subcommand]` 来调用命令。如果你使用的是 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)，请使用 `tiup cloud [command] [subcommand]`。

| 命令                | 子命令                                                               | 描述                                       |
|---------------------|----------------------------------------------------------------------|--------------------------------------------|
| auth                | login, logout, whoami                                                | 登录和登出                                 |
| serverless (别名：s) | create, delete, describe, list, update, spending-limit, region, shell | 管理 TiDB Cloud Serverless 集群            |
| serverless branch   | create, delete, describe, list, shell                                | 管理 TiDB Cloud Serverless 分支             |
| serverless import   | cancel, describe, list, start                                       | 管理 TiDB Cloud Serverless 导入任务        |
| serverless export   | create, describe, list, cancel, download                            | 管理 TiDB Cloud Serverless 导出任务        |
| serverless sql-user | create, list, delete, update                                         | 管理 TiDB Cloud Serverless SQL 用户          |
| serverless audit-log| config, describe, filter-rule (别名：filter), download               | 管理 TiDB Cloud Serverless 数据库审计日志  |
| ai                  | -                                                                    | 与 TiDB Bot 聊天                            |
| completion          | bash, fish, powershell, zsh                                          | 生成指定 shell 的补全脚本                   |
| config              | create, delete, describe, edit, list, set, use                       | 配置用户配置文件                            |
| project             | list                                                                 | 管理项目                                   |
| upgrade             | -                                                                    | 将 CLI 升级到最新版本                        |
| help                | auth, config, serverless, ai, project, upgrade, help, completion     | 查看任何命令的帮助                         |

## 命令模式

TiDB Cloud CLI 为部分命令提供两种模式，方便使用：

- 交互模式

    你可以运行不带参数的命令（例如 `ticloud config create`），CLI 会提示你输入。

- 非交互模式

    你必须在运行命令时提供所有必需的参数和标志，例如 `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`。

## 用户配置文件

对于 TiDB Cloud CLI，用户配置文件是与用户相关的一组属性，包括配置文件名、公共密钥、私有密钥和 OAuth 令牌。要使用 TiDB Cloud CLI，必须拥有一个用户配置文件。

### 使用 TiDB Cloud API 密钥创建用户配置文件

使用 [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) 创建用户配置文件。

### 使用 OAuth 令牌创建用户配置文件

使用 [`ticloud auth login`](/tidb-cloud/ticloud-auth-login.md) 将 OAuth 令牌分配给当前配置文件。如果不存在配置文件，将自动创建一个名为 `default` 的配置文件。

> **Note:**
>
> 在前述两种方法中，TiDB Cloud API 密钥优先级高于 OAuth 令牌。如果当前配置文件中同时存在两者，将优先使用 API 密钥。

### 列出所有用户配置文件

使用 [`ticloud config list`](/tidb-cloud/ticloud-config-list.md) 列出所有用户配置文件。

示例输出如下：

```
Profile Name
default (active)
dev
staging
```

在此示例中，用户配置文件 `default` 当前处于激活状态。

### 查看用户配置文件详情

使用 [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md) 获取用户配置文件的属性。

示例输出如下：

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### 设置用户配置文件中的属性

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

## 全局标志

下表列出了 TiDB Cloud CLI 的全局标志。

| 标志                | 描述                                              | 必需 | 备注                                                                                                              |
|---------------------|--------------------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| --no-color          | 禁用输出中的颜色。                                | 否     | 仅在非交互模式下生效。在交互模式中，禁用颜色可能不适用于某些 UI 组件。                                                 |
| -P, --profile string | 指定在此命令中使用的激活用户配置文件。             | 否     | 在非交互和交互模式下均有效。                                                                                        |
| -D, --debug        | 启用调试模式                                      | 否     | 在非交互和交互模式下均有效。                                                                                        |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，也欢迎任何贡献。