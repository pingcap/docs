---
title: ticloud serverless audit-log filter-rule create
summary: `ticloud serverless audit-log filter-rule create` 的参考文档。
---

# ticloud serverless audit-log filter-rule create

为 TiDB Cloud Serverless 集群创建审计日志过滤规则。

```shell
ticloud serverless audit-log filter-rule create [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless audit-log filter create [flags]
```

## 示例

以交互模式创建过滤规则：

```shell
ticloud serverless audit-log filter create
```

在非交互模式下创建捕获所有审计日志的过滤规则：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

在非交互模式下创建过滤 `QUERY` 和 `EXECUTE` 事件（针对 `test.t` 表）以及过滤所有表的 `QUERY` 事件的规则：

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY","EXECUTE"],"tables":["test.t"]},{"classes":["QUERY"]}]}'
```

## Flags

在非交互模式下，你需要手动输入必填的参数。在交互模式下，可以按照 CLI 提示填写。

| Flag                    | 描述                                                                                                         | 必填 | 备注                                                      |
|-------------------------|--------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------------|
| -c, --cluster-id string | 集群的 ID。                                                                                                 | 是     | 仅在非交互模式下生效。                                    |
| --name string           | 过滤规则的名称。                                                                                             | 是     | 仅在非交互模式下生效。                                    |
| --rule string           | 过滤规则表达式。可使用 `ticloud serverless audit-log filter template` 查看过滤模板。                        | 是     | 仅在非交互模式下生效。                                    |
| -h, --help              | 显示此命令的帮助信息。                                                                                       | 否     | 在非交互和交互模式下均可使用。                              |

## 继承的 Flags

| Flag                 | 描述                                                                                                         | 必填 | 备注                                                      |
|----------------------|--------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                           | 否     | 仅在非交互模式下生效。在交互模式中，禁用颜色可能在某些 UI 组件中不起作用。 |
| -P, --profile string | 指定在此命令中使用的[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                            | 否     | 在非交互和交互模式下均可使用。                              |
| -D, --debug          | 启用调试模式。                                                                                               | 否     | 在非交互和交互模式下均可使用。                              |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。