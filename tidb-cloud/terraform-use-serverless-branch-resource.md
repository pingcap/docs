---
title: 使用 TiDB Cloud Serverless 分支资源
summary: 了解如何使用 serverless 分支资源创建和修改 TiDB Cloud Serverless 分支。
---

# 使用 TiDB Cloud Serverless 分支资源

本文档描述了如何使用 `tidbcloud_serverless_branch` 资源管理 [TiDB Cloud Serverless 分支](/tidb-cloud/branch-manage.md)。

`tidbcloud_serverless_branch` 资源的功能包括：

- 创建 TiDB Cloud Serverless 分支
- 导入 TiDB Cloud Serverless 分支
- 删除 TiDB Cloud Serverless 分支

> **注意：**
>
> TiDB Cloud Serverless 分支资源无法修改。如果你想更改 serverless 分支资源的配置，需要删除现有的资源并创建一个新的。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 创建 TiDB Cloud Serverless 分支

你可以使用 `tidbcloud_serverless_branch` 资源创建 TiDB Cloud Serverless 分支。

以下示例展示了如何创建一个 TiDB Cloud Serverless 分支。

1. 创建一个分支目录并进入。

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

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详细信息。

    - 若要使用 serverless 分支资源，将资源类型设置为 `tidbcloud_serverless_branch`
    - 资源名称可根据需要定义，例如 `example`
    - 资源详细信息可根据 serverless 分支规范信息进行配置
    - 获取 serverless 分支规范信息，请参见 [tidbcloud_serverless_branch (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_branch)

3. 运行 `terraform apply` 命令。建议不要使用 `terraform apply --auto-approve` 直接应用资源。

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

    在上述结果中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，不会更改或销毁任何资源
    - `known after apply` 表示在 `apply` 后你将获得相应的值

4. 如果计划中的内容都没有问题，输入 `yes` 继续：

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

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_branch.${resource-name}` 命令检查资源状态。前者显示所有资源和数据源的状态。

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

## 导入 TiDB Cloud Serverless 分支

对于未由 Terraform 管理的 TiDB Cloud Serverless 分支，你可以通过导入来让 Terraform 管理它。

导入未由 Terraform 创建的 TiDB Cloud Serverless 分支的方法如下：

1. 在你的 `.tf` 文件中添加导入块。

    将以下导入块添加到你的 `.tf` 文件中，替换 `example` 为你希望的资源名，`${id}` 替换为 `cluster_id,branch_id` 格式：

    ```
    import {
      to = tidbcloud_serverless_branch.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud Serverless 分支资源配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以将此文件的内容移动到你偏好的位置。

    然后，运行 `terraform apply` 以导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_branch.example: Importing... 
    tidbcloud_serverless_branch.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以用 Terraform 管理导入的分支。

## 删除 TiDB Cloud Serverless 分支

要删除 TiDB Cloud Serverless 分支，你可以删除 `tidbcloud_serverless_branch` 资源的配置，然后运行 `terraform apply` 来销毁资源：

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

现在，如果你运行 `terraform show` 命令，将不会显示任何托管的资源，因为资源已被清除：

```
$ terraform show
```