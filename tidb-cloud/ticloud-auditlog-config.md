---
title: ticloud serverless audit-log config
summary: The reference of `ticloud serverless audit-log config`.
---

# ticloud serverless audit-log config

配置 TiDB Cloud Serverless 集群的数据库审计日志。

```shell
ticloud serverless audit-log config [flags]
```

## 示例

在交互模式下配置数据库审计日志：

```shell
ticloud serverless audit-log config
```

在非交互模式下启用数据库审计日志：

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

在非交互模式下禁用数据库审计日志：

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

在非交互模式下取消审计日志的脱红：

```shell
ticloud serverless audit-log config -c <cluster-id> --unredacted
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                     | 描述                                                                 | 是否必需 | 备注                                               |
|--------------------------|----------------------------------------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string  | 集群的 ID。                                                          | 是       | 仅在非交互模式下生效。                              |
| --enabled                | 启用或禁用数据库审计日志。                                              | 否       | 仅在非交互模式下生效。                              |
| --unredacted             | 启用或禁用审计日志中的数据脱红。                                          | 否       | 仅在非交互模式下生效。                              |
| -h, --help               | 显示此命令的帮助信息。                                                  | 否       | 在非交互和交互模式下均可使用。                        |

## 继承的标志

| 标志                     | 描述                                                                 | 是否必需 | 备注                                               |
|--------------------------|----------------------------------------------------------------------|----------|----------------------------------------------------|
| --no-color               | 禁用输出中的颜色。                                                      | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能在某些 UI 组件中不起作用。 |
| -P, --profile string     | 指定在此命令中使用的[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下均可使用。                        |
| -D, --debug              | 启用调试模式。                                                          | 否       | 在非交互和交互模式下均可使用。                        |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，也欢迎任何贡献。