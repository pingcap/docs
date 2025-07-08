---
title: ticloud serverless audit-log describe
summary: The reference of `ticloud serverless audit-log describe`.
---

# ticloud serverless audit-log describe

描述 TiDB Cloud Serverless 集群的数据库审计日志配置。

```shell
ticloud serverless audit-log describe [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless audit-log get [flags]
```

## 示例

以交互模式获取数据库审计日志配置：

```shell
ticloud serverless audit-log describe
```

以非交互模式获取数据库审计日志配置：

```shell
ticloud serverless audit-log describe -c <cluster-id>
```

## Flags

在非交互模式下，你需要手动输入所需的 flags。在交互模式下，可以按照 CLI 提示填写。

| Flag                    | 描述                         | 必填 | 备注                                               |
|-------------------------|------------------------------|--------|----------------------------------------------------|
| -c, --cluster-id string | 集群 ID                     | 是     | 仅在非交互模式下生效。                              |
| -h, --help              | 显示此命令的帮助信息。       | 否     | 在非交互和交互模式下均可使用。                        |

## 继承的 flags

| Flag                 | 描述                                                                 | 必填 | 备注                                                                 |
|----------------------|----------------------------------------------------------------------|--------|----------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                    | 否     | 仅在非交互模式下生效。在交互模式中，禁用颜色可能不适用于某些 UI 组件。 |
| -D, --debug          | 启用调试模式。                                                        | 否     | 在非交互和交互模式下均可使用。                                        |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，也欢迎任何贡献。