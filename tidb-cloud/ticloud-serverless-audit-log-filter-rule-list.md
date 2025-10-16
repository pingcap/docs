---
title: ticloud serverless audit-log filter-rule list
summary: "`ticloud serverless audit-log filter-rule list` 的参考文档。"
---

# ticloud serverless audit-log filter-rule list

列出 TiDB Cloud Essential 集群的审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule list [flags]
```

## 示例

以交互模式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule list
```

以非交互模式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id>
```

以非交互模式并以 JSON 格式列出所有审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id> -o json
```

## 参数

| Flag                    | Description                                                                                       | Required | Note                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 集群的 ID。                                                                                       | No       | 仅在非交互模式下生效。                              |
| -o, --output string     | 指定输出格式。有效值为 `human`（默认）或 `json`。如需完整结果，请使用 `json` 格式。                | No       | 在交互和非交互模式下均可用。                        |
| -h, --help              | 显示该命令的帮助信息。                                                                            | No       | 在交互和非交互模式下均可用。                        |

## 继承参数

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | 启用调试模式。                                                                                       | No       | 在交互和非交互模式下均可用。                                                                                    |
| --no-color           | 禁用彩色输出。                                                                                       | No       | 仅在非交互模式下生效。                                                                                          |
| -P, --profile string | 指定从你的配置文件中使用的 profile。                                                                  | No       | 在交互和非交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。