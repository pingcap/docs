---
title: ticloud serverless export download
summary: "`ticloud serverless export download` 的参考文档。"
---

# ticloud serverless export download

从 TiDB Cloud Serverless 集群下载导出的数据到本地存储：

```shell
ticloud serverless export download [flags]
```

## 示例

以交互模式下载导出的数据：

```shell
ticloud serverless export download
```

以非交互模式下载导出的数据：

```shell
ticloud serverless export download -c <cluster-id> -e <export-id>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                      | 说明                                                                                                              | 是否必需 | 备注                                               |
|---------------------------|-------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string   | 指定集群的 ID。                                                                                                   | 是       | 仅在非交互模式下生效。                            |
| -e, --export-id string    | 指定导出任务的 ID。                                                                                               | 是       | 仅在非交互模式下生效。                            |
| --output-path string      | 指定保存下载数据的目标路径。如果未指定，则数据下载到当前目录。                                                    | 否       | 仅在非交互模式下生效。                            |
| --concurrency int         | 指定下载并发数。默认值为 `3`。                                                                                   | 否       | 在非交互和交互模式下均可用。                      |
| --force                   | 无需确认直接下载导出的数据。                                                                                      | 否       | 在非交互和交互模式下均可用。                      |
| -h, --help                | 显示该命令的帮助信息。                                                                                            | 否       | 在非交互和交互模式下均可用。                      |

## 继承参数

| 参数                    | 说明                                                                                                 | 是否必需 | 备注                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------|
| --no-color              | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。             |
| -P, --profile string    | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                     | 否       | 在非交互和交互模式下均可用。                                                          |
| -D, --debug             | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均可用。                                                          |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。
