---
title: ticloud serverless audit-log filter-rule create
summary: "`ticloud serverless audit-log filter-rule create` 的参考文档。"
---

# ticloud serverless audit-log filter-rule create

为 TiDB Cloud Essential 集群创建一个审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule create [flags]
```

## 示例

以交互模式创建一个过滤规则：

```shell
ticloud serverless audit-log filter-rule create
```

以非交互模式创建一个捕获所有审计日志的过滤规则：

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

以非交互模式创建一个过滤规则，用于捕获 `test.t` 表的 `QUERY` 和 `EXECUTE` 事件，以及所有表的 `QUERY` 事件：

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY","EXECUTE"],"tables":["test.t"]},{"classes":["QUERY"]}]}'
```

## 参数

| 参数                    | 描述                                                                                                 | 是否必需 | 说明                                                 |
|-------------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 集群的 ID。                                                                                         | 是       | 仅在非交互模式下生效。                              |
| --display-name string   | 过滤规则的显示名称。                                                                                | 是       | 仅在非交互模式下生效。                              |
| --rule string           | 过滤规则表达式。可使用 `ticloud serverless audit-log filter-rule template` 查看过滤模板。            | 是       | 仅在非交互模式下生效。                              |
| -h, --help              | 显示该命令的帮助信息。                                                                              | 否       | 在交互和非交互模式下均可用。                        |

## 继承参数

| 参数                 | 描述                                                                                          | 是否必需 | 说明                                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | 启用调试模式。                                                                                | 否       | 在交互和非交互模式下均可用。                                                                                     |
| --no-color           | 禁用彩色输出。                                                                                | 否       | 仅在非交互模式下生效。                                                                                           |
| -P, --profile string | 指定要从你的配置文件中使用的 profile。                                                         | 否       | 在交互和非交互模式下均可用。                                                                                     |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。