---
title: ticloud serverless audit-log download
summary: `ticloud serverless audit-log download` 的参考文档。
---

# ticloud serverless audit-log download

从 TiDB Cloud Serverless 集群下载数据库审计日志。

```shell
ticloud serverless audit-log download [flags]
```

## 示例

以交互模式下载数据库审计日志：

```shell
ticloud serverless audit-log download
```

以非交互模式下载数据库审计日志：

```shell
ticloud serverless audit-log download -c <cluster-id> --start-date <start-date> --end-date <end-date>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| Flag                    | 描述                                                                                                         | 是否必需 | 备注                                                 |
|-------------------------|--------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 集群 ID。                                                                                                   | 是       | 仅在非交互模式下生效。                              |
| --start-date string     | 你想要下载的审计日志的起始日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。                                    | 是       | 仅在非交互模式下生效。                              |
| --end-date string       | 你想要下载的审计日志的结束日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。                                    | 是       | 仅在非交互模式下生效。                              |
| --output-path string    | 你希望下载审计日志的路径。如果未指定，日志将下载到当前目录。                                                | 否       | 仅在非交互模式下生效。                              |
| --concurrency int       | 下载并发数（默认为 `3`）。                                                                                  | 否       | 在非交互和交互模式下均可用。                        |
| --force                 | 无需确认直接下载。                                                                                          | 否       | 在非交互和交互模式下均可用。                        |
| -h, --help              | 显示该命令的帮助信息。                                                                                      | 否       | 在非交互和交互模式下均可用。                        |

## 继承参数

| Flag                 | 描述                                                                                          | 是否必需 | 备注                                                                                                             |
|----------------------|---------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                           | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。             | 否       | 在非交互和交互模式下均可用。                                                                                    |
| -D, --debug          | 启用调试模式。                                                                               | 否       | 在非交互和交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时也欢迎任何形式的贡献。