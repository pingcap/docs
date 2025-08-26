---
title: ticloud serverless audit-log config
summary: "`ticloud serverless audit-log config` 的参考文档。"
---

# ticloud serverless audit-log config

为 TiDB Cloud Serverless 集群配置数据库审计日志。

```shell
ticloud serverless audit-log config [flags]
```

## 示例

以交互模式配置数据库审计日志：

```shell
ticloud serverless audit-log config
```

以非交互模式启用数据库审计日志：

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

以非交互模式禁用数据库审计日志：

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

以非交互模式取消数据库审计日志的数据脱敏：

```shell
ticloud serverless audit-log config -c <cluster-id> --unredacted
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                      | 说明                                                                 | 是否必需 | 备注                                                 |
|---------------------------|----------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string   | 集群的 ID。                                                          | 是       | 仅在非交互模式下生效。                              |
| --enabled                 | 启用或禁用数据库审计日志。                                           | 否       | 仅在非交互模式下生效。                              |
| --unredacted              | 启用或禁用审计日志中的数据脱敏。                                     | 否       | 仅在非交互模式下生效。                              |
| -h, --help                | 显示该命令的帮助信息。                                               | 否       | 在非交互和交互模式下均可用。                        |

## 继承参数

| 参数                  | 说明                                                                                          | 是否必需 | 备注                                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color            | 禁用输出中的颜色。                                                                           | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string  | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。             | 否       | 在非交互和交互模式下均可用。                                                                                    |
| -D, --debug           | 启用调试模式。                                                                               | 否       | 在非交互和交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何形式的贡献。
