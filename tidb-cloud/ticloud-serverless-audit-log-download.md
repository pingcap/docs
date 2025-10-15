---
title: ticloud serverless audit-log download
summary: "`ticloud serverless audit-log download` 的参考文档。"
---

# ticloud serverless audit-log download

从 TiDB Cloud Essential 集群下载数据库审计日志文件。

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

## 参数

| Flag                    | Description                                                                                   | Required | Note                                                 |
|-------------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 集群的 ID。                                                                                   | Yes      | 仅在非交互模式下生效。                              |
| --start-date string     | 你想要下载的审计日志的起始日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。                      | Yes      | 仅在非交互模式下生效。                              |
| --end-date string       | 你想要下载的审计日志的结束日期，格式为 `YYYY-MM-DD`，例如 `2025-01-01`。                      | Yes      | 仅在非交互模式下生效。                              |
| --output-path string    | 下载审计日志的路径。如果未指定，日志将下载到当前目录。                                         | No       | 仅在非交互模式下生效。                              |
| --concurrency int       | 并发下载的数量。默认值为 `3`。                                                                | No       | 在交互和非交互模式下均可用。                        |
| --force                 | 无需确认直接下载审计日志。                                                                    | No       | 在交互和非交互模式下均可用。                        |
| -h, --help              | 显示该命令的帮助信息。                                                                        | No       | 在交互和非交互模式下均可用。                        |

## 继承参数

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | 启用调试模式。                                                                                       | No       | 在交互和非交互模式下均可用。                                                                                    |
| --no-color           | 禁用彩色输出。                                                                                       | No       | 仅在非交互模式下生效。                                                                                          |
| -P, --profile string | 指定从你的配置文件中使用的 profile。                                                                  | No       | 在交互和非交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何贡献。