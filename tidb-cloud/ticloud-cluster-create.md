---
title: ticloud serverless create
summary: `ticloud serverless create` 的参考文档。
---

# ticloud serverless create

创建一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create [flags]
```

## 示例

以交互模式创建一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create
```

以非交互模式创建一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create --display-name <display-name> --region <region>
```

以非交互模式并设置消费上限创建一个 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create --display-name <display-name> --region <region> --spending-limit-monthly <spending-limit-monthly>
``` 

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                          | 描述                                                                                                    | 是否必需 | 备注                                                |
|------------------------------|---------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -n --display-name string     | 指定要创建的集群名称。                                                                                  | 是       | 仅在非交互模式下生效。                             |
| --spending-limit-monthly int | 指定每月最大消费上限（单位为美元分）。                                                                  | 否       | 仅在非交互模式下生效。                             |
| -p, --project-id string      | 指定要创建集群的项目 ID，默认值为 `default project`。                                                   | 否       | 仅在非交互模式下生效。                             |
| -r, --region string          | 指定云区域名称。你可以使用 "ticloud serverless region" 查看所有区域。                                   | 是       | 仅在非交互模式下生效。                             |
| --disable-public-endpoint    | 禁用公网访问入口。                                                                                      | 否       | 仅在非交互模式下生效。                             |
| --encryption                 | 启用增强的静态加密。                                                                                    | 否       | 仅在非交互模式下生效。                             |
| -h, --help                   | 显示该命令的帮助信息。                                                                                  | 否       | 在非交互和交互模式下均可用。                       |

## 继承参数

| 参数                  | 描述                                                                                          | 是否必需 | 备注                                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。               | 否       | 在非交互和交互模式下均可用。                                                                                     |
| -D, --debug          | 启用调试模式。                                                                                | 否       | 在非交互和交互模式下均可用。                                                                                     |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何贡献。