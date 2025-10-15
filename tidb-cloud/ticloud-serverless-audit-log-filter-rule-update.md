---
title: ticloud serverless audit-log filter-rule update
summary: "`ticloud serverless audit-log filter-rule update` 的参考文档。"
---

# ticloud serverless audit-log filter-rule update

为 TiDB Cloud Essential 集群更新审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule update [flags]
```

## 示例

以交互模式更新审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule update
```

以非交互模式启用审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled
```

以非交互模式禁用审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

以非交互模式更新审计日志过滤规则的过滤条件：

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

## 参数

| 参数                      | 描述                                                                                                   | 是否必需 | 说明                                               |
|---------------------------|--------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string   | 集群的 ID。                                                                                            | 是       | 仅在非交互模式下生效。                            |
| --display-name string     | 过滤规则的显示名称。                                                                                   | 否       | 仅在非交互模式下生效。                            |
| --enabled                 | 启用或禁用该过滤规则。                                                                                 | 否       | 仅在非交互模式下生效。                            |
| --filter-rule-id string   | 过滤规则的 ID。                                                                                        | 是       | 仅在非交互模式下生效。                            |
| --rule string             | 完整的过滤规则表达式。可使用 [`ticloud serverless audit-log filter template`](/tidb-cloud/ticloud-serverless-audit-log-filter-rule-template.md) 查看过滤模板。 | 否       | 仅在非交互模式下生效。                            |
| -h, --help                | 显示该命令的帮助信息。                                                                                 | 否       | 在交互和非交互模式下均可用。                      |

## 继承参数

| 参数                  | 描述                                                                                 | 是否必需 | 说明                                                                                 |
|-----------------------|--------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------|
| -D, --debug           | 启用调试模式。                                                                      | 否       | 在交互和非交互模式下均可用。                                                        |
| --no-color            | 禁用彩色输出。                                                                      | 否       | 仅在非交互模式下生效。                                                              |
| -P, --profile string  | 指定从你的配置文件中使用的 profile。                                                 | 否       | 在交互和非交互模式下均可用。                                                        |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。