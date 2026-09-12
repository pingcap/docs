---
title: 使用 dbt 加载数据
summary: dbt 是一种转换工作流，可帮助你在产出更高质量结果的同时完成更多工作。你可以使用 dbt 将分析代码模块化并集中管理，同时为数据团队提供软件工程工作流中常见的防护机制。在安全部署到生产环境之前，你可以协作构建数据模型、进行版本管理，并对查询进行测试和文档化，同时获得监控和可观测性。
---

# 使用 dbt 加载数据

[dbt](https://www.getdbt.com/) 是一种转换工作流，可帮助你在产出更高质量结果的同时完成更多工作。你可以使用 dbt 将分析代码模块化并集中管理，同时为数据团队提供软件工程工作流中常见的防护机制。在安全部署到生产环境之前，你可以协作构建数据模型、进行版本管理，并对查询进行测试和文档化，同时获得监控和可观测性。

[tidbcloudlake-dbt](https://github.com/tidbcloud/lake-dbt) 是由 {{{ .lake }}} 开发的一个插件，主要目标是实现 dbt 与 {{{ .lake }}} 的平滑集成。借助该插件，你可以使用 dbt 无缝执行数据建模、转换和清洗任务，并方便地将输出加载到 {{{ .lake }}} 中。下表展示了 tidbcloudlake-dbt 插件对 dbt 常用功能的支持级别：

| 功能                      | 支持？ |
|----------------------------- |----------- |
| 表物化        | 是        |
| 视图物化         | 是        |
| 增量物化  | 是        |
| 临时物化    | 否         |
| 数据填充                        | 是        |
| 源                      | 是        |
| 自定义数据测试            | 是        |
| 文档生成                | 是        |
| 快照                    | 是        |
| 连接重试             | 是        |

## 安装 tidbcloudlake-dbt {#install-tidbcloudlake-dbt}

为了方便使用，tidbcloudlake-dbt 插件的安装流程已简化，因为它现在已将 dbt 作为必需依赖关系包含在内。要轻松完成 dbt 和 tidbcloudlake-dbt 插件的安装，请运行以下命令：

```shell
pip3 install tidbcloudlake-dbt
```

不过，如果你希望单独安装 dbt，可以参考 dbt 官方安装指南获取详细说明。

## 教程：运行 dbt 项目 jaffle_shop {#tutorial-run-dbt-project-jaffle-shop}

如果你刚开始接触 dbt，{{{ .lake }}} 建议你先完成官方 dbt 教程：<https://github.com/dbt-labs/jaffle_shop>。开始之前，请按照[安装 tidbcloudlake-dbt](#install-tidbcloudlake-dbt)中的说明安装 dbt 和 tidbcloudlake-dbt。

本教程提供了一个名为 “jaffle_shop” 的示例 dbt 项目，帮助你通过实践熟悉 dbt 工具。通过在默认的全局 profile（`~/.dbt/profiles.yml`）中配置连接到你的 {{{ .lake }}} 实例所需的信息，该项目会直接在你的 {{{ .lake }}} 数据库中生成 dbt models 中定义的表和视图。以下是一个连接到 {{{ .lake }}} 实例的 `profiles.yml` 文件示例：

```yml title="~/.dbt/profiles.yml"
jaffle_shop_lake:
  target: dev
  outputs:
    dev:
      type: tidbcloudlake
      host: tnxxxx.gw.aws-us-east-2.default.tidbcloud.com
      port: 443
      schema: sjh_dbt
      user: <username>
      pass: ********
      warehouse: default
      secure: true
```

有关配置和使用该适配器的更多信息，请参见 [lake-dbt repository](https://github.com/tidbcloud/lake-dbt)。