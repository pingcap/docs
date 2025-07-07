---
title: ticloud serverless audit-log filter-rule list
summary: `ticloud serverless audit-log filter-rule list` 的参考文档。
---

# ticloud serverless audit-log filter-rule list

列出 TiDB Cloud Serverless 集群的审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule list [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless audit-log filter list [flags]
```

## 示例

以交互模式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter list
```

以非交互模式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter list -c <cluster-id>
```

以非交互模式并以 JSON 格式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter list -c <cluster-id> -o json
```

## Flags

在非交互模式下，你需要手动输入必需的参数。在交互模式下，可以按照 CLI 提示填写。

| Flag                    | 描述                                                                                               | 必填 | 备注                                                    |
|-------------------------|---------------------------------------------------------------------------------------------------|--------|---------------------------------------------------------|
| -c, --cluster-id string | 要列出审计日志过滤规则的集群 ID。                                                                   | 否     | 仅在非交互模式下生效。                                   |
| -o, --output string     | 指定输出格式（默认为 `human`）。有效值为 `human` 或 `json`。若需完整结果，请使用 `json` 格式。             | 否     | 在非交互和交互模式下均可使用。                            |
| -h, --help              | 显示此命令的帮助信息。                                                                               | 否     | 在非交互和交互模式下均可使用。                            |

## 继承的 Flags

| Flag                 | 描述                                                                                          | 必填 | 备注                                                                                     |
|----------------------|------------------------------------------------------------------------------------------------|--------|------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                               | 否     | 仅在非交互模式下生效。在交互模式中，禁用颜色可能不适用于某些 UI 组件。                     |
| -P, --profile string | 指定在此命令中使用的[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                     | 否     | 在非交互和交互模式下均可使用。                                                            |
| -D, --debug          | 启用调试模式。                                                                                   | 否     | 在非交互和交互模式下均可使用。                                                            |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，也欢迎任何贡献。