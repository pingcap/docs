---
title: ticloud serverless update
summary: `ticloud serverless update` 的参考文档。
---

# ticloud serverless update

更新一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless update [flags]
```

## 示例

以交互模式更新一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless update
```

以非交互模式更新 TiDB Cloud Serverless 集群的名称：

```shell
ticloud serverless update -c <cluster-id> --display-name <new-display-mame>
```

以非交互模式更新 TiDB Cloud Serverless 集群的标签：

```shell
ticloud serverless update -c <cluster-id> --labels "{\"label1\":\"value1\"}"
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                        | 描述                                         | 是否必需 | 备注                                               |
|-----------------------------|----------------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string     | 指定集群的 ID。                              | 是       | 仅在非交互模式下生效。                            |
| -n --display-name string    | 指定集群的新名称。                           | 否       | 仅在非交互模式下生效。                            |
| --labels string             | 指定集群的新标签。                           | 否       | 仅在非交互模式下生效。                            |
| --disable-public-endpoint   | 禁用集群的公共访问端点。                     | 否       | 仅在非交互模式下生效。                            |
| -h, --help                  | 显示该命令的帮助信息。                       | 否       | 在非交互和交互模式下均可用。                      |

## 继承参数

| 参数                   | 描述                                                                                  | 是否必需 | 备注                                                                                   |
|------------------------|---------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------|
| --no-color             | 禁用输出中的颜色。                                                                   | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。             |
| -P, --profile string   | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。      | 否       | 在非交互和交互模式下均可用。                                                          |
| -D, --debug            | 启用调试模式。                                                                       | 否       | 在非交互和交互模式下均可用。                                                          |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。