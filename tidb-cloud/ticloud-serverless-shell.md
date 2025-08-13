---
title: ticloud serverless shell
summary: `ticloud serverless shell` 的参考文档。
aliases: ['/tidbcloud/ticloud-connect']
---

# ticloud serverless shell

连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell [flags]
```

## 示例

以交互模式连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell
```

以非交互模式，使用默认用户连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id>
```

以非交互模式，使用默认用户和密码连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id> --password <password>
```

以非交互模式，使用指定用户和密码连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id> -u <user-name> --password <password>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                      | 描述                                   | 是否必需 | 备注                                               |
|---------------------------|----------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string   | 指定集群的 ID。                        | 是       | 仅在非交互模式下生效。                            |
| -h, --help                | 显示该命令的帮助信息。                 | 否       | 在非交互和交互模式下均可用。                      |
| --password                | 指定用户的密码。                       | 否       | 仅在非交互模式下生效。                            |
| -u, --user string         | 指定登录的用户。                       | 否       | 仅在非交互模式下生效。                            |

## 继承参数

| 参数                  | 描述                                                                                      | 是否必需 | 备注                                                                                   |
|-----------------------|-------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------|
| --no-color            | 禁用输出中的颜色。                                                                       | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。             |
| -P, --profile string  | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。          | 否       | 在非交互和交互模式下均可用。                                                          |
| -D, --debug           | 启用调试模式。                                                                           | 否       | 在非交互和交互模式下均可用。                                                          |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。