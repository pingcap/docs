---
title: ticloud serverless branch delete
summary: "`ticloud serverless branch delete` 的参考文档。"
---

# ticloud serverless branch delete

从你的 TiDB Cloud Serverless 集群中删除一个分支：

```shell
ticloud serverless branch delete [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless branch rm [flags]
```

## 示例

以交互模式删除一个 TiDB Cloud Serverless 分支：

```shell
ticloud serverless branch delete
```

以非交互模式删除一个 TiDB Cloud Serverless 分支：

```shell
ticloud branch delete --branch-id <branch-id> --cluster-id <cluster-id>
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                    | 描述                                | 是否必需 | 备注                                                 |
|-------------------------|-------------------------------------|----------|------------------------------------------------------|
| -b, --branch-id string  | 指定要删除的分支 ID。               | 是       | 仅在非交互模式下生效。                               |
| --force                 | 无需确认直接删除分支。              | 否       | 在非交互和交互模式下均可用。                         |
| -h, --help              | 显示此命令的帮助信息。              | 否       | 在非交互和交互模式下均可用。                         |
| -c, --cluster-id string | 指定集群的 ID。                     | 是       | 仅在非交互模式下生效。                               |

## 继承参数

| 参数                 | 描述                                                                                | 是否必需 | 备注                                                                                                             |
|----------------------|-------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                  | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定此命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。     | 否       | 在非交互和交互模式下均可用。                                                                                     |
| -D, --debug          | 启用调试模式。                                                                      | 否       | 在非交互和交互模式下均可用。                                                                                     |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。
