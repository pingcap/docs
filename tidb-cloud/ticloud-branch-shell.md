---
title: ticloud serverless branch shell
summary: `ticloud serverless branch shell` 的参考文档。
aliases: ['/tidbcloud/ticloud-connect']
---

# ticloud serverless branch shell

连接到 TiDB Cloud Serverless 集群的某个分支：

```shell
ticloud serverless branch shell [flags]
```

## 示例

以交互模式连接到 TiDB Cloud Serverless 分支：

```shell
ticloud serverless branch shell
```

以非交互模式，使用默认用户连接到 TiDB Cloud Serverless 分支：

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id>
```

以非交互模式，使用默认用户和密码连接到 TiDB Cloud Serverless 分支：

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> --password <password>
```

以非交互模式，使用指定用户和密码连接到 TiDB Cloud Serverless 分支：

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> -u <user-name> --password <password>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 的提示填写即可。

| 参数                      | 说明                                   | 是否必需 | 备注                                               |
|---------------------------|----------------------------------------|----------|----------------------------------------------------|
| -b, --branch-id string    | 指定分支的 ID。                        | 是       | 仅在非交互模式下生效。                            |
| -c, --cluster-id string   | 指定集群的 ID。                        | 是       | 仅在非交互模式下生效。                            |
| -h, --help                | 显示该命令的帮助信息。                 | 否       | 在非交互和交互模式下均可用。                      |
| --password                | 指定用户的密码。                       | 否       | 仅在非交互模式下生效。                            |
| -u, --user string         | 指定登录的用户。                       | 否       | 仅在非交互模式下生效。                            |

## 继承参数

| 参数                  | 说明                                                                                  | 是否必需 | 备注                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------|
| --no-color            | 禁用输出中的颜色。                                                                   | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。             |
| -P, --profile string  | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。      | 否       | 在非交互和交互模式下均可用。                                                          |
| -D, --debug           | 启用调试模式。                                                                       | 否       | 在非交互和交互模式下均可用。                                                          |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎在 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose) 页面提交。我们也欢迎任何形式的贡献。