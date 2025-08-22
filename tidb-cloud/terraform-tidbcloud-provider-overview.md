---
title: Terraform Integration Overview
summary: 通过 Terraform 创建、管理和更新你的 TiDB Cloud 资源。
---

# Terraform 集成概述

[Terraform](https://www.terraform.io/) 是一款基础设施即代码（Infrastructure as Code, IaC）工具，可以让你在可读性强的配置文件中定义云端和自托管资源，并支持版本管理、复用和共享。

[TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) 是一个插件，允许你使用 Terraform 管理 TiDB Cloud 资源，例如集群、备份和恢复等。

如果你正在寻找一种简单的方式来自动化资源的配置和基础设施工作流，你可以尝试 TiDB Cloud Terraform Provider，它为你提供以下能力：

- 获取你的项目信息。
- 获取集群规格信息，例如支持的云服务商、区域和节点规格。
- 管理你的 TiDB 集群，包括创建、扩容、暂停和恢复集群。
- 为你的集群创建和删除备份。
- 为你的集群创建恢复任务。

## 前置条件

- [一个 TiDB Cloud 账号](https://tidbcloud.com/free-trial)
- [Terraform 版本](https://www.terraform.io/downloads.html) >= 1.0
- [Go 版本](https://golang.org/doc/install) >= 1.18（仅当你需要在本地构建 [TiDB Cloud Terraform Provider](https://github.com/tidbcloud/terraform-provider-tidbcloud) 时需要）

## 支持的资源和数据源

[资源](https://www.terraform.io/language/resources) 和 [数据源](https://www.terraform.io/language/data-sources) 是 Terraform 语言中最重要的两个元素。

TiDB Cloud 支持以下资源和数据源：

- 资源

    - `tidbcloud_cluster`
    - `tidbcloud_backup`
    - `tidbcloud_restore`
    - `tidbcloud_import`

- 数据源

    - `tidbcloud_projects`
    - `tidbcloud_cluster_specs`
    - `tidbcloud_clusters`
    - `tidbcloud_restores`
    - `tidbcloud_backups`

要获取所有可用的资源和数据源的配置信息，请参阅此 [配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

## 下一步

- [了解更多关于 Terraform 的信息](https://www.terraform.io/docs)
- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)
- [使用 `tidbcloud_serverless_cluster` 资源](/tidb-cloud/terraform-use-serverless-cluster-resource.md)
- [使用 `tidbcloud_dedicated_cluster` 资源](/tidb-cloud/terraform-use-dedicated-cluster-resource.md)
- [使用 `tidbcloud_backup` 资源](/tidb-cloud/terraform-use-backup-resource.md)
- [使用 `tidbcloud_restore` 资源](/tidb-cloud/terraform-use-restore-resource.md)