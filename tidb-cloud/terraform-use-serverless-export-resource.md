---
title: 使用 TiDB Cloud Serverless Export 资源
summary: 了解如何使用 TiDB Cloud Serverless export 资源创建和修改 TiDB Cloud Serverless export 任务。
---

# 使用 TiDB Cloud Serverless Export 资源

本文档介绍如何使用 `tidbcloud_serverless_export` 资源管理 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据导出任务。

`tidbcloud_serverless_export` 资源的功能包括：

- 创建 TiDB Cloud Serverless 数据导出任务
- 导入 TiDB Cloud Serverless 数据导出任务
- 删除 TiDB Cloud Serverless 数据导出任务

> **注意：**
>
> TiDB Cloud Serverless export 资源不能被修改。如果你想更改 TiDB Cloud Serverless export 资源的配置，需要先删除现有的资源，然后再创建一个新的。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 创建 TiDB Cloud Serverless 数据导出任务

你可以使用 `tidbcloud_serverless_export` 资源创建 TiDB Cloud Serverless 数据导出任务。

以下示例演示如何创建一个 TiDB Cloud Serverless 数据导出任务。

1. 创建一个导出目录并进入。

2. 创建 `export.tf` 文件：

    ```hcl
    terraform {
      required_providers {
        tidbcloud = {
          source = "tidbcloud/tidbcloud"
        }
      }
    }

    provider "tidbcloud" {
      public_key  = "your_public_key"
      private_key = "your_private_key"
    }

    resource "tidbcloud_serverless_export" "example" {
      cluster_id = 10476959660988000000
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

    - 若要使用 serverless export 资源，将资源类型设置为 `tidbcloud_serverless_export`
    - 资源名称可以根据需要定义，例如 `example`
    - 资源详情可根据 serverless export 规范信息进行配置
    - 获取 serverless export 规范信息，请参见 [tidbcloud_serverless_export (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_export)

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
        + create

    Terraform 将执行以下操作：

        # tidbcloud_serverless_export.example 将被创建
        + resource "tidbcloud_serverless_export" "example" {
            + cluster_id     = "10476959660988000000"
            + complete_time  = (应用后已知)
            + create_time    = (应用后已知)
            + created_by     = (应用后已知)
            + display_name   = (应用后已知)
            + expire_time    = (应用后已知)
            + export_id      = (应用后已知)
            + export_options = (应用后已知)
            + reason         = (应用后已知)
            + snapshot_time  = (应用后已知)
            + state          = (应用后已知)
            + target         = (应用后已知)
            + update_time    = (应用后已知)
        }

    计划：添加1个，修改0个，销毁0个。

    是否执行这些操作？
        Terraform 将执行上述操作。
        只接受输入 'yes' 以确认。

        输入一个值：
    ```

    在上述输出中，Terraform 为你生成了一个执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，没有资源会被修改或销毁
    - `应用后已知` 表示你在 `apply` 后会获得对应的值

4. 如果一切看起来正常，输入 `yes` 继续：

    ```shell
    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值: yes

    tidbcloud_serverless_export.example: 创建中...
    tidbcloud_serverless_export.example: 1秒后创建完成

    应用完成！资源：添加1个，修改0个，销毁0个。
    ```

    在此示例中，`tidbcloud_serverless_export.example` 资源将创建一个导出任务，用于导出整个集群的数据。

    该资源不具备同步功能。你可以使用 `terraform refresh` 来获取其最新状态。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_export.${资源名}` 命令检查资源状态。前者显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_serverless_export.example
    # tidbcloud_serverless_export.example:
    resource "tidbcloud_serverless_export" "example" {
        cluster_id     = "10476959660988000000"
        create_time    = "2025-06-16T08:54:10Z"
        created_by     = "apikey-S2000000"
        display_name   = "SNAPSHOT_2025-06-16T08:54:10Z"
        export_id      = "exp-ezsli6ugtzg2nkmzaitt000000"
        export_options = {
            compression = "GZIP"
            file_type   = "CSV"
        }
        snapshot_time  = "2025-06-16T08:54:10Z"
        state          = "RUNNING"
        target         = {
            type = "LOCAL"
        }
    }
    ```

## 导入未由 Terraform 管理的 TiDB Cloud Serverless 数据导出任务

对于未由 Terraform 管理的 TiDB Serverless 数据导出任务，你可以通过导入来让 Terraform 管理它。

导入未由 Terraform 创建的 TiDB Cloud Serverless 数据导出任务的方法如下：

1. 在你的 `.tf` 文件中添加导入块。

    在你的 `.tf` 文件中添加如下导入块，替换 `example` 为你希望的资源名，`${id}` 替换为 `cluster_id,export_id` 格式：

    ```
    import {
      to = tidbcloud_serverless_export.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 serverless export 资源配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    不要在前述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。你也可以将此文件的内容移动到你偏好的位置。

    然后，运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_export.example: 导入中...
    tidbcloud_serverless_export.example: 导入完成

    应用完成！资源：导入1个，添加0个，修改0个，销毁0个。
    ```

现在你可以用 Terraform 管理导入的导出任务。

## 删除 TiDB Cloud Serverless 数据导出任务

要删除 TiDB Cloud Serverless 数据导出任务，你可以删除 `tidbcloud_serverless_export` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
$ terraform apply
tidbcloud_serverless_export.example: 刷新状态...

Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
  - destroy

Terraform 将执行以下操作：

  # tidbcloud_serverless_export.example 将被销毁
  # （因为 `tidbcloud_serverless_export.example` 不在配置中）
  - resource "tidbcloud_serverless_export" "example" {
      - cluster_id     = "10476959660988000000" -> null
      - create_time    = "2025-06-16T08:54:10Z" -> null
      - created_by     = "apikey-S2000000" -> null
      - display_name   = "SNAPSHOT_2025-06-16T08:54:10Z" -> null
      - export_id      = "exp-ezsli6ugtzg2nkmzaitt000000" -> null
      - export_options = {
          - compression = "GZIP" -> null
          - file_type   = "CSV" -> null
        } -> null
      - snapshot_time  = "2025-06-16T08:54:10Z" -> null
      - state          = "RUNNING" -> null
      - target         = {
          - type = "LOCAL" -> null
        } -> null
    }

计划：不添加，修改0，销毁1。

是否执行这些操作？
  Terraform 将执行上述操作。
  只接受输入 'yes' 以确认。

  输入一个值: yes

tidbcloud_serverless_export.example: 销毁中...
tidbcloud_serverless_export.example: 2秒后完成销毁

应用完成！资源：0个添加，0个修改，1个销毁。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管资源，因为资源已被清除：

```
$ terraform show
```