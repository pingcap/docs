---
title: 使用 TiDB Cloud 无服务器分支资源
summary: 了解如何使用无服务器分支资源创建和修改 TiDB Cloud 无服务器分支。
---

# 使用 TiDB Cloud 无服务器分支资源

本文档介绍如何使用 `tidbcloud_serverless_branch` 资源管理 [TiDB Cloud 无服务器分支](/tidb-cloud/branch-manage.md)。

`tidbcloud_serverless_branch` 资源的功能包括：

- 创建 TiDB Cloud 无服务器分支
- 导入 TiDB Cloud 无服务器分支
- 删除 TiDB Cloud 无服务器分支

> **注意：**
>
> TiDB Cloud 无服务器分支资源无法直接修改。如果你想更改无服务器分支资源的配置，需要删除现有资源并创建一个新资源。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 版本 v0.4.0 或更高
- [创建 TiDB Cloud 无服务器集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 创建 TiDB Cloud 无服务器分支

你可以使用 `tidbcloud_serverless_branch` 资源创建 TiDB Cloud 无服务器分支。

以下示例演示如何创建一个 TiDB Cloud 无服务器分支。

1. 创建一个用于分支的目录并进入。

2. 创建 `branch.tf` 文件：

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

    resource "tidbcloud_serverless_branch" "example" {
      cluster_id   = 10581524018573000000
      display_name = "example"
      parent_id    = 10581524018573000000
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详细信息。

    - 若要使用无服务器分支资源，资源类型设为 `tidbcloud_serverless_branch`
    - 资源名称可根据需要定义，例如 `example`
    - 资源详细信息可根据无服务器分支的规范信息进行配置
    - 获取无服务器分支规范信息，请参见 [tidbcloud_serverless_branch (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_branch)

3. 运行 `terraform apply` 命令。建议不要使用 `terraform apply --auto-approve` 直接应用资源。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
      + 创建

    Terraform 将执行以下操作：

      # tidbcloud_serverless_branch.example 将被创建
      + resource "tidbcloud_serverless_branch" "example" {
          + annotations         = (应用后可知)
          + branch_id           = (应用后可知)
          + cluster_id          = "10581524018573000000"
          + create_time         = (应用后可知)
          + created_by          = (应用后可知)
          + display_name        = "example"
          + endpoints           = (应用后可知)
          + parent_display_name = (应用后可知)
          + parent_id           = "10581524018573000000"
          + parent_timestamp    = (应用后可知)
          + state               = (应用后可知)
          + update_time         = (应用后可知)
          + user_prefix         = (应用后可知)
        }

    计划：添加1个，修改0个，销毁0个。

    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：
    ```

    在上述输出中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，不会更改或销毁任何资源
    - `known after apply` 表示在 `apply` 后你将获得对应的值

4. 如果一切看起来正常，输入 `yes` 继续：

    ```shell
    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：yes

    tidbcloud_serverless_branch.example: 创建中...
    tidbcloud_serverless_branch.example: 仍在创建中... [已用时10秒]
    tidbcloud_serverless_branch.example: 10秒后创建完成

    应用完成！资源：添加1个，未更改0个，未销毁0个。
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_branch.${资源名}` 命令检查资源状态。前者显示所有资源和数据源的状态。

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

## 导入一个 TiDB Cloud 无服务器分支

对于未由 Terraform 管理的 TiDB Cloud 无服务器分支，你可以通过导入来让 Terraform 管理它。

导入未由 Terraform 创建的 TiDB Cloud 无服务器分支的方法如下：

1. 在你的 `.tf` 文件中添加导入块，替换 `example` 为你想要的资源名，`${id}` 替换为 `cluster_id,branch_id` 格式：

    ```
    import {
      to = tidbcloud_serverless_branch.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud 无服务器分支资源配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。你也可以将此文件的内容移动到你偏好的位置。

    然后，运行 `terraform apply` 以导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_branch.example: 导入中...
    tidbcloud_serverless_branch.example: 导入完成

    应用完成！资源：导入1个，添加0个，修改0个，销毁0个。
    ```

现在你可以用 Terraform 管理导入的分支。

## 删除一个 TiDB Cloud 无服务器分支

要删除一个 TiDB Cloud 无服务器分支，你可以删除 `tidbcloud_serverless_branch` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
$ terraform apply
tidbcloud_serverless_branch.example: 正在刷新状态...

Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
  - 销毁

Terraform 将执行以下操作：

  # tidbcloud_serverless_branch.example 将被销毁
  # （因为 tidbcloud_serverless_branch.example 不在配置中）
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

计划：不添加，未更改，销毁1个。

是否执行这些操作？
  Terraform 将执行上述操作。
  只接受输入 'yes' 以确认。

  输入一个值：yes

tidbcloud_serverless_branch.example: 正在销毁...
tidbcloud_serverless_branch.example: 1秒后销毁完成

应用完成！资源：未添加，未更改，已销毁1个。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管资源，因为资源已被清除：

```
$ terraform show
```