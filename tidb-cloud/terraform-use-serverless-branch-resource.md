---
title: 使用 `tidbcloud_serverless_branch` 资源
summary: 了解如何使用 serverless branch 资源来创建和修改 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。
---

# 使用 `tidbcloud_serverless_branch` 资源

本文档介绍如何使用 `tidbcloud_serverless_branch` 资源管理 [TiDB Cloud Starter 或 TiDB Cloud Essential 分支](/tidb-cloud/branch-manage.md)。

`tidbcloud_serverless_branch` 资源的功能包括：

- 创建 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。
- 导入 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。
- 删除 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。

> **Note:**
>
> `tidbcloud_serverless_branch` 资源无法被修改。如果你想更改 serverless branch 资源的配置，需要先删除现有资源，再创建一个新的资源。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。
- [创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 创建 TiDB Cloud Starter 或 TiDB Cloud Essential 分支

你可以使用 `tidbcloud_serverless_branch` 资源来创建 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。

以下示例展示了如何创建 TiDB Cloud Starter 或 TiDB Cloud Essential 分支。

1. 为分支创建一个目录并进入该目录。

2. 创建一个 `branch.tf` 文件：

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

    resource "tidbcloud_serverless_branch" "example" {
      cluster_id   = 10581524018573000000
      display_name = "example"
      parent_id = 10581524018573000000
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 要使用 serverless branch 资源，将资源类型设置为 `tidbcloud_serverless_branch`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 资源详情可以根据 serverless branch 规范信息进行配置。
    - 获取 serverless branch 规范信息，请参见 [tidbcloud_serverless_branch (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_branch)。

3. 运行 `terraform apply` 命令。应用资源时，不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_serverless_branch.example will be created
      + resource "tidbcloud_serverless_branch" "example" {
          + annotations         = (known after apply)
          + branch_id           = (known after apply)
          + cluster_id          = "10581524018573000000"
          + create_time         = (known after apply)
          + created_by          = (known after apply)
          + display_name        = "example"
          + endpoints           = (known after apply)
          + parent_display_name = (known after apply)
          + parent_id           = "10581524018573000000"
          + parent_timestamp    = (known after apply)
          + state               = (known after apply)
          + update_time         = (known after apply)
          + user_prefix         = (known after apply)
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
    - `known after apply` 表示在 `apply` 之后你将获得对应的值。

4. 如果你的计划内容没有问题，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_branch.example: Creating...
    tidbcloud_serverless_branch.example: Still creating... [10s elapsed]
    tidbcloud_serverless_branch.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_branch.${resource-name}` 命令检查你的资源状态。前者会显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_serverless_branch.example 
    # tidbcloud_serverless_branch.example:
    resource "tidbcloud_serverless_branch" "example" {
        annotations         = {
            "tidb.cloud/has-set-password" = "false"
        }
        branch_id           = "bran-qt3fij6jufcf5pluot5h000000"
        cluster_id          = "10581524018573000000"
        create_time         = "2025-06-16T07:55:51Z"
        created_by          = "apikey-S2000000"
        display_name        = "example"
        endpoints           = {
            private = {
                aws  = {
                    availability_zone = [
                        "use1-az6",
                    ]
                    service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
                }
                host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
                port = 4000
            }
            public  = {
                disabled = false
                host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
                port     = 4000
            }
        }
        parent_display_name = "test-tf"
        parent_id           = "10581524018573000000"
        parent_timestamp    = "2025-06-16T07:55:51Z"
        state               = "ACTIVE"
        update_time         = "2025-06-16T07:56:49Z"
        user_prefix         = "4ER5SbndR000000"
    }
    ```

## 导入 TiDB Cloud Starter 或 TiDB Cloud Essential 分支

对于未被 Terraform 管理的 TiDB Cloud Starter 或 TiDB Cloud Essential 分支，你可以通过导入操作将其纳入 Terraform 管理。

导入未通过 Terraform 创建的 TiDB Cloud Starter 或 TiDB Cloud Essential 分支，操作如下：

1. 为新的 `tidbcloud_serverless_branch` 资源添加 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你期望的资源名称，将 `${id}` 替换为 `cluster_id,branch_id` 的格式：

    ```
    import {
      to = tidbcloud_serverless_branch.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 `tidbcloud_serverless_branch` 资源生成新的配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_branch.example: Importing... 
    tidbcloud_serverless_branch.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理已导入的分支。

## 删除 TiDB Cloud Starter 或 TiDB Cloud Essential 分支

要删除 TiDB Cloud Starter 或 TiDB Cloud Essential 分支，你可以删除 `tidbcloud_serverless_branch` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

```shell
$ terraform apply
tidbcloud_serverless_branch.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_branch.example will be destroyed
  # (because tidbcloud_serverless_branch.example is not in configuration)
  - resource "tidbcloud_serverless_branch" "example" {
      - annotations         = {
          - "tidb.cloud/has-set-password" = "false"
        } -> null
      - branch_id           = "bran-qt3fij6jufcf5pluot5h000000" -> null
      - cluster_id          = "10581524018573000000" -> null
      - create_time         = "2025-06-16T07:55:51Z" -> null
      - created_by          = "apikey-S2000000" -> null
      - display_name        = "example" -> null
      - endpoints           = {
          - private = {
              - aws  = {
                  - availability_zone = [
                      - "use1-az6",
                    ] -> null
                  - service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000" -> null
                } -> null
              - host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com" -> null
              - port = 4000 -> null
            } -> null
          - public  = {
              - disabled = false -> null
              - host     = "gateway01.us-east-1.prod.aws.tidbcloud.com" -> null
              - port     = 4000 -> null
            } -> null
        } -> null
      - parent_display_name = "test-tf" -> null
      - parent_id           = "10581524018573000000" -> null
      - parent_timestamp    = "2025-06-16T07:55:51Z" -> null
      - state               = "ACTIVE" -> null
      - update_time         = "2025-06-16T07:56:49Z" -> null
      - user_prefix         = "4ER5SbndR000000" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_branch.example: Destroying...
tidbcloud_serverless_branch.example: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会显示任何被管理的资源，因为该资源已被清除：

```
$ terraform show
```