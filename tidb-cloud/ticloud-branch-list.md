---
title: ticloud serverless branch list
summary: `ticloud serverless branch list` 的参考文档。
---

# ticloud serverless branch list

列出所有 TiDB Cloud Serverless 集群的分支：

```shell
ticloud serverless branch list <cluster-id> [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless branch ls <cluster-id> [flags]
```

## 示例

以交互模式列出所有 TiDB Cloud Serverless 集群的分支：

```shell
ticloud serverless branch list
```

以非交互模式列出指定 TiDB Cloud Serverless 集群的所有分支：

```shell
ticloud serverless branch list -c <cluster-id>
```

以 JSON 格式列出指定 TiDB Cloud Serverless 集群的所有分支：

```shell
ticloud serverless branch list <cluster-id> -o json
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                    | 说明                                                                                                              | 是否必需 | 备注                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                                                                                                   | 是       | 仅在非交互模式下生效。                              |
| -h, --help              | 显示该命令的帮助信息。                                                                                            | 否       | 在非交互和交互模式下均可用。                        |
| -o, --output string     | 指定输出格式（默认为 **human**）。可选值为 **human** 或 **json**。如需获取完整结果，建议使用 **json** 格式。      | 否       | 在非交互和交互模式下均可用。                        |

## 继承参数

| 参数                 | 说明                                                                                          | 是否必需 | 备注                                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。              | 否       | 在非交互和交互模式下均可用。                                                                                    |
| -D, --debug          | 启用调试模式。                                                                                | 否       | 在非交互和交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。