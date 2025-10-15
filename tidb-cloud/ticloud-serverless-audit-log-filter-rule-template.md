---
title: ticloud serverless audit-log filter-rule template
summary: "`ticloud serverless audit-log filter-rule template` 的参考文档。"
---

# ticloud serverless audit-log filter-rule template

展示 TiDB Cloud Essential 集群的审计日志过滤规则模板。

```shell
ticloud serverless audit-log filter-rule template [flags]
```

## 示例

以交互模式展示过滤模板：

```shell
ticloud serverless audit-log filter-rule template
```

以非交互模式展示过滤模板：

```shell
ticloud serverless audit-log filter-rule template --cluster-id <cluster-id>
```

## 参数

| Flag                    | 描述                                   | 是否必需 | 备注                                         |
|-------------------------|----------------------------------------|----------|----------------------------------------------|
| -c, --cluster-id string | 集群的 ID。                            | 否       | 仅在非交互模式下生效。                      |
| -h, --help              | 显示该命令的帮助信息。                 | 否       | 在交互和非交互模式下均可用。                |

## 继承参数

| Flag                 | 描述                                                                 | 是否必需 | 备注                                         |
|----------------------|----------------------------------------------------------------------|----------|----------------------------------------------|
| -D, --debug          | 启用调试模式。                                                       | 否       | 在交互和非交互模式下均可用。                |
| --no-color           | 禁用彩色输出。                                                       | 否       | 仅在非交互模式下生效。                      |
| -P, --profile string | 指定从你的配置文件中使用的 profile。                                 | 否       | 在交互和非交互模式下均可用。                |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。