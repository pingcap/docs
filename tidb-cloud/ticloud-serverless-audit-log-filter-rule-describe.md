---
title: ticloud serverless audit-log filter-rule describe
summary: "`ticloud serverless audit-log filter-rule describe` 的参考文档。"
---

# ticloud serverless audit-log filter-rule describe

描述 TiDB Cloud Essential 集群的审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule describe [flags]
```

## 示例

以交互模式描述一个审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule describe
```

以非交互模式描述一个审计日志过滤规则：

```shell
ticloud serverless audit-log filter-rule describe --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

## 参数

| 参数                      | 描述                              | 是否必需 | 备注                                         |
|---------------------------|-----------------------------------|----------|----------------------------------------------|
| -c, --cluster-id string   | 集群的 ID。                       | 是       | 仅在非交互模式下生效。                      |
| --filter-rule-id string   | 过滤规则的 ID。                   | 是       | 仅在非交互模式下生效。                      |
| -h, --help                | 显示该命令的帮助信息。             | 否       | 在交互和非交互模式下均可用。                |

## 继承参数

| 参数                    | 描述                                                                 | 是否必需 | 备注                                         |
|-------------------------|----------------------------------------------------------------------|----------|----------------------------------------------|
| -D, --debug             | 启用调试模式。                                                       | 否       | 在交互和非交互模式下均可用。                |
| --no-color              | 禁用彩色输出。                                                       | 否       | 仅在非交互模式下生效。                      |
| -P, --profile string    | 指定要使用的配置文件中的 profile。                                   | 否       | 在交互和非交互模式下均可用。                |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。