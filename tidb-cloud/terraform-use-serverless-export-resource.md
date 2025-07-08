---
title: 使用 TiDB Cloud Serverless 导出资源
summary: 了解如何使用 TiDB Cloud Serverless 导出资源创建和修改 TiDB Cloud Serverless 导出任务。
---

# 使用 TiDB Cloud Serverless 导出资源

本文档描述了如何使用 `tidbcloud_serverless_export` 资源管理 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据导出任务。

`tidbcloud_serverless_export` 资源的功能包括：

- 创建 TiDB Cloud Serverless 数据导出任务
- 导入 TiDB Cloud Serverless 数据导出任务
- 删除 TiDB Cloud Serverless 数据导出任务

> **注意：**
>
> TiDB Cloud Serverless 导出资源无法修改。如果你想更改 TiDB Cloud Serverless 导出资源的配置，需要先删除现有的，然后再创建一个新的。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 创建 TiDB Cloud Serverless 数据导出任务

你可以使用 `tidbcloud_serverless_export` 资源创建 TiDB Cloud Serverless 数据导出任务。

以下示例展示了如何创建一个 TiDB Cloud Serverless 数据导出任务。

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
      public_key = "your_public_key"
      private_key = "your_private_key"
    }

    resource "tidbcloud_serverless_export" "example" {
      cluster_id   = 10476959660988000000
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

    - 若要使用服务器无导出资源，将资源类型设置为 `tidbcloud_serverless_export`
    - 资源名称可以根据需要定义，例如 `example`
    - 资源详情可根据服务器无导出规范信息进行配置
    - 获取服务器无导出规范信息，请参见 [tidbcloud_serverless_export (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_export)

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
        + create

    Terraform will perform the following actions:

        # tidbcloud_serverless_export.example will be created
        + resource "tidbcloud_serverless_export" "example" {
            + cluster_id     = "10476959660988000000"
            + complete_time  = (known after apply)
            + create_time    = (known after apply)
            + created_by     = (known after apply)
            + display_name   = (known after apply)
            + expire_time    = (known after apply)
            + export_id      = (known after apply)
            + export_options = (known after apply)
            + reason         = (known after apply)
            + snapshot_time  = (known after apply)
            + state          = (known after apply)
            + target         = (known after apply)
            + update_time    = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    在上述结果中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，没有资源会被更改或销毁
    - `known after apply` 表示在 `apply` 后你将获得相应的值

4. 如果计划中的内容都没有问题，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_export.example: Creating...
    tidbcloud_serverless_export.example: Creation complete after 1s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
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

对于未由 Terraform 管理的 TiDB Serverless 数据导出任务，你可以通过导入方式让 Terraform 管理它。

导入未由 Terraform 创建的 TiDB Cloud Serverless 数据导出任务的方法如下：

1. 在你的 `.tf` 文件中添加导入块。

    在你的 `.tf` 文件中添加如下导入块，替换 `example` 为你想要的资源名，替换 `${id}` 为 `cluster_id,export_id` 的格式：

    ```
    import {
      to = tidbcloud_serverless_export.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的服务器无导出资源配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。你也可以将此文件的内容移动到你偏好的位置。

    然后，运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_export.example: Importing... 
    tidbcloud_serverless_export.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以用 Terraform 管理导入的导出任务。

## 删除 TiDB Cloud Serverless 数据导出任务

要删除 TiDB Cloud Serverless 数据导出任务，你可以删除 `tidbcloud_serverless_export` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
$ terraform apply
tidbcloud_serverless_export.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_export.example will be destroyed
  # (because tidbcloud_serverless_export.example is not in configuration)
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

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_export.example: Destroying...
tidbcloud_serverless_export.example: Destruction complete after 2s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管资源，因为资源已被清除：

```
$ terraform show
```