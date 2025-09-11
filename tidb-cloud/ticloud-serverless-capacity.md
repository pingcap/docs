---
title: ticloud serverless capacity
summary: `ticloud serverless capacity` 的参考文档。
---

# ticloud serverless capacity

为 TiDB Cloud 集群设置最大和最小请求容量单元（RCU）的容量。

```shell
ticloud serverless capacity [flags]
```

## 示例

以交互模式为 TiDB Cloud 集群设置容量：

```shell
 ticloud serverless capacity
```

以非交互模式为 TiDB Cloud 集群设置容量：

```shell
ticloud serverless capacity -c <cluster-id> --max-rcu <maximum-rcu> --min-rcu <minimum-rcu>
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| Flag                    | 说明                                                         | 是否必需 | 备注                                               |
|-------------------------|--------------------------------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                                              | 是       | 仅在非交互模式下生效。                             |
| --max-rcu int32         | 指定集群的最大请求容量单元（RCU），最大可设置为 100000。      | 否       | 仅在非交互模式下生效。                             |
| --min-rcu int32         | 指定集群的最小请求容量单元（RCU），最小需为 2000。            | 否       | 仅在非交互模式下生效。                             |
| -h, --help              | 显示该命令的帮助信息。                                       | 否       | 在非交互和交互模式下均可用。                       |

## 继承参数

| Flag                 | 说明                                                                                                   | 是否必需 | 备注                                                                                      |
|----------------------|--------------------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                     | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                       | 否       | 在非交互和交互模式下均可用。                                                              |
| -D, --debug          | 启用调试模式。                                                                                         | 否       | 在非交互和交互模式下均可用。                                                              |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何形式的贡献。