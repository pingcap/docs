---
title: ticloud serverless audit-log describe
summary: `ticloud serverless audit-log describe` 的参考文档。
---

# ticloud serverless audit-log describe

描述 TiDB Cloud Serverless 集群的数据库审计日志配置。

```shell
ticloud serverless audit-log describe [flags]
```

或者使用以下别名命令：

```shell
ticloud serverless audit-log get [flags]
```

## 示例

以交互模式获取数据库审计日志配置：

```shell
ticloud serverless audit-log describe
```

以非交互模式获取数据库审计日志配置：

```shell
ticloud serverless audit-log describe -c <cluster-id>
```

## 参数说明

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                      | 描述                              | 是否必需 | 备注                                               |
|---------------------------|-----------------------------------|----------|----------------------------------------------------|
| -c, --cluster-id string   | 集群 ID。                         | 是       | 仅在非交互模式下生效。                             |
| -h, --help                | 显示该命令的帮助信息。            | 否       | 在非交互和交互模式下均可用。                       |

## 继承参数

| 参数                  | 描述                                                                 | 是否必需 | 备注                                                                                   |
|-----------------------|----------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------|
| --no-color            | 禁用输出中的颜色。                                                   | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示效果。          |
| -D, --debug           | 启用调试模式。                                                       | 否       | 在非交互和交互模式下均可用。                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎在 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose) 页面提交。同时也欢迎任何形式的贡献。