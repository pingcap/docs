---
title: ticloud serverless audit-log filter-rule template
summary: 参考 `ticloud serverless audit-log filter-rule template`。
---

# ticloud serverless audit-log filter-rule template

显示 TiDB Cloud Serverless 集群的审计日志过滤规则模板。

```shell
ticloud serverless audit-log filter-rule template [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless audit-log filter template [flags]
```

## 示例

以交互模式显示过滤模板：

```shell
ticloud serverless audit-log filter template
```

以非交互模式显示过滤模板：

```shell
ticloud serverless audit-log filter template --cluster-id <cluster-id>
```

## Flags

在非交互模式下，你需要手动输入所需的 flags。在交互模式下，你只需按照 CLI 提示填写即可。

| Flag                    | 描述                                                      | 必填 | 备注                                                      |
|-------------------------|-----------------------------------------------------------|--------|-----------------------------------------------------------|
| -c, --cluster-id string | 集群的 ID（可选，用于在模板可能变为集群特定时提供上下文）。 | 否     | 仅在非交互模式下生效。                                    |
| -h, --help              | 显示此命令的帮助信息。                                    | 否     | 在非交互和交互模式下均有效。                                |

## 继承的 flags

| Flag                 | 描述                                                                 | 必填 | 备注                                                                 |
|----------------------|----------------------------------------------------------------------|--------|----------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                    | 否     | 仅在非交互模式下生效。在交互模式中，禁用颜色可能不适用于某些 UI 组件。 |
| -P, --profile string | 指定在此命令中使用的[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否     | 在非交互和交互模式下均有效。                                         |
| -D, --debug          | 启用调试模式。                                                        | 否     | 在非交互和交互模式下均有效。                                         |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，也欢迎任何贡献。