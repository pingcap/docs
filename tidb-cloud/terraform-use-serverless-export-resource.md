---
title: 使用 `tidbcloud_serverless_export` 资源
summary: 了解如何使用 `tidbcloud_serverless_export` 资源为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群创建和修改数据导出任务。
---

# 使用 `tidbcloud_serverless_export` 资源

本文档介绍如何使用 `tidbcloud_serverless_export` 资源管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务。

`tidbcloud_serverless_export` 资源的功能包括：

- 为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群创建数据导出任务。
- 导入 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务。
- 删除 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务。

> **Note:**
>
> `tidbcloud_serverless_export` 资源无法被修改。如果你想更改 `tidbcloud_serverless_export` 资源的配置，需要先删除现有资源，然后重新创建。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。
- [创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群创建数据导出任务

你可以使用 `tidbcloud_serverless_export` 资源为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群创建数据导出任务。

1. 为导出任务创建一个目录并进入该目录。

2. 为数据导出任务创建一个 `export.tf` 文件。

    以下是 `export.tf` 文件的示例：

    ```
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

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 要使用 serverless 导出资源，将资源类型设置为 `tidbcloud_serverless_export`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 资源详情可以根据 serverless 导出规范信息进行配置。
    - 获取 serverless 导出规范信息，请参见 [tidbcloud_serverless_export (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_export)。

3. 运行 `terraform apply` 命令。应用资源时，不建议使用 `terraform apply --auto-approve`。

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

    在上述结果中，Terraform 为你生成了一个执行计划，描述了 Terraform 将要执行的操作：

    - 你可以检查配置与当前状态之间的差异。
    - 你还可以看到本次 `apply` 的结果。它将新增一个资源，不会有资源被更改或销毁。
    - `known after apply` 表示你将在 `apply` 后获得对应的值。

4. 如果你的计划没有问题，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_export.example: Creating...
    tidbcloud_serverless_export.example: Creation complete after 1s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    在本示例中，`tidbcloud_serverless_export.example` 资源将创建一个导出任务，用于导出整个集群的数据。

    该资源是异步的。你可以使用 `terraform refresh` 获取其最新状态。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_export.${resource-name}` 命令检查资源的状态。前者会显示所有资源和数据源的状态。

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

## 导入 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务

如果某个 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务未被 Terraform 管理，你可以通过导入将其纳入 Terraform 管理。

1. 为新的 `tidbcloud_serverless_export` 资源添加一个 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你期望的资源名称，将 `${id}` 替换为 `cluster_id,export_id` 的格式：

    ```
    import {
      to = tidbcloud_serverless_export.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 serverless export 资源生成新的配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_export.example: Importing... 
    tidbcloud_serverless_export.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理已导入的导出任务。

## 删除 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务

要删除 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的数据导出任务，你可以删除 `tidbcloud_serverless_export` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

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

现在，如果你运行 `terraform show` 命令，将不会显示任何被管理的资源，因为该资源已被清除：

```
$ terraform show
```