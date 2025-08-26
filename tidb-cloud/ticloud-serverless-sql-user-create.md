---
title: ticloud serverless sql-user create
summary: `ticloud serverless sql-user create` 的参考文档。
---

# ticloud serverless sql-user create

创建一个 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user create [flags]
```

## 示例

以交互模式创建一个 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user create
```

以非交互模式创建一个 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user create --user <user-name> --password <password> --role <role> --cluster-id <cluster-id>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 的提示填写即可。

| 参数                    | 描述                                      | 是否必需 | 备注                                                 |
|-------------------------|------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                          | 是       | 仅在非交互模式下生效。                              |
| --password string       | 指定 SQL 用户的密码。                    | 否       | 仅在非交互模式下生效。                              |
| --role strings          | 指定 SQL 用户的角色。                    | 否       | 仅在非交互模式下生效。                              |
| -u, --user string       | 指定 SQL 用户的名称。                    | 否       | 仅在非交互模式下生效。                              |
| -h, --help              | 显示该命令的帮助信息。                   | 否       | 在非交互和交互模式下均可用。                        |

## 继承参数

| 参数                 | 描述                                                                                          | 是否必需 | 备注                                                                                                             |
|----------------------|---------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                          | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                      |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。             | 否       | 在非交互和交互模式下均可用。                                                                                    |
| -D, --debug          | 启用调试模式。                                                                              | 否       | 在非交互和交互模式下均可用。                                                                                    |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何形式的贡献。