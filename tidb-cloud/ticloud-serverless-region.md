---
title: ticloud serverless region
summary: `ticloud serverless region` 的参考文档。
aliases: ['/tidbcloud/ticloud-serverless-regions']
---

# ticloud serverless region

列出所有可用于 TiDB Cloud Serverless 的可用区域：

```shell
ticloud serverless region [flags]
```

## 示例

列出所有可用于 TiDB Cloud Serverless 的可用区域：

```shell
ticloud serverless region
```

以 JSON 格式列出所有可用于 TiDB Cloud Serverless 集群的可用区域：

```shell
ticloud serverless region -o json
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| Flag                | Description                                                                                                              | Required | Note                                                 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -o, --output string | 指定输出格式（默认为 `human`）。有效值为 `human` 或 `json`。如需获取完整结果，请使用 `json` 格式。 | No       | 适用于非交互和交互模式。                            |
| -h, --help          | 显示该命令的帮助信息。                                                                                                   | No       | 适用于非交互和交互模式。                            |

## 继承参数

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                         | No       | 仅适用于非交互模式。在交互模式下，禁用颜色可能无法与某些 UI 组件兼容。                                          |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。           | No       | 适用于非交互和交互模式。                                                                                        |
| -D, --debug          | 启用调试模式。                                                                             | No       | 适用于非交互和交互模式。                                                                                        |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。