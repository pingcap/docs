---
title: 使用 `tidbcloud_dedicated_vpc_peering` 资源
summary: 了解如何使用 `tidbcloud_dedicated_vpc_peering` 资源来创建和修改 TiDB Cloud Dedicated VPC Peering。
---

# 使用 `tidbcloud_dedicated_vpc_peering` 资源

本文档介绍如何通过 `tidbcloud_dedicated_vpc_peering` 资源管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) VPC Peering。

`tidbcloud_dedicated_vpc_peering` 资源的功能包括：

- 创建 TiDB Cloud Dedicated VPC Peering。
- 导入 TiDB Cloud Dedicated VPC Peering。
- 删除 TiDB Cloud Dedicated VPC Peering。

> **注意：**
>
> `tidbcloud_dedicated_vpc_peering` 资源无法被修改。如果你想更改 TiDB Cloud Dedicated VPC Peering 的配置，需要先删除现有的 Peering，然后重新创建。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。

## 创建 TiDB Cloud Dedicated VPC Peering

你可以使用 `tidbcloud_dedicated_vpc_peering` 资源来创建 TiDB Cloud Dedicated VPC Peering。

以下示例展示了如何创建 TiDB Cloud Dedicated VPC Peering。

1. 为 TiDB Cloud Dedicated VPC Peering 创建一个目录，并进入该目录。

2. 创建一个 `vpc_peering.tf` 文件：

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

    resource "tidbcloud_dedicated_vpc_peering" "example" {
      tidb_cloud_region_id = "your_tidb_cloud_region_id"
      customer_region_id   = "your_customer_region_id"
      customer_account_id  = "your_customer_account_id"
      customer_vpc_id      = "your_customer_vpc_id"
      customer_vpc_cidr    = "your_customer_vpc_cidr"
    }
    ```

    使用 `resource` 块来定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 要使用 `tidbcloud_dedicated_vpc_peering` 资源，需将资源类型设置为 `tidbcloud_dedicated_vpc_peering`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 如果你不知道如何获取必需参数的值，请参阅 [通过 VPC Peering 连接 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md)。
    - 如需获取 TiDB Cloud Dedicated VPC Peering 规范信息，请参阅 [tidbcloud_dedicated_vpc_peering (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_vpc_peering)。

3. 运行 `terraform apply` 命令。应用资源时不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
        + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_vpc_peering.example will be created
        + resource "tidbcloud_dedicated_vpc_peering" "example" {
            + aws_vpc_peering_connection_id = (known after apply)
            + customer_account_id           = "986330900000"
            + customer_region_id            = "aws-us-west-2"
            + customer_vpc_cidr             = "172.16.32.0/21"
            + customer_vpc_id               = "vpc-0c0c7d59702000000"
            + labels                        = (known after apply)
            + project_id                    = (known after apply)
            + state                         = (known after apply)
            + tidb_cloud_account_id         = (known after apply)
            + tidb_cloud_cloud_provider     = (known after apply)
            + tidb_cloud_region_id          = "aws-us-west-2"
            + tidb_cloud_vpc_cidr           = (known after apply)
            + tidb_cloud_vpc_id             = (known after apply)
            + vpc_peering_id                = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    在上述结果中，Terraform 为你生成了一个执行计划，描述了 Terraform 将要执行的操作：

    - 你可以检查配置与状态之间的差异。
    - 你还可以看到本次 `apply` 的结果。它将新增一个资源，不会有资源被更改或销毁。
    - `known after apply` 表示在 `apply` 后你将获得对应的值。

4. 如果你的计划没有问题，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_vpc_peering.example: Creating...
    tidbcloud_dedicated_vpc_peering.example: Still creating... [10s elapsed]
    ```

    资源的状态会保持为 `Creating`，直到你在云服务商控制台中批准 VPC Peering 连接。批准后，你可以参考 [批准并配置 VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md#step-2-approve-and-configure-the-vpc-peering)，状态会变为 `Active`。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_vpc_peering.${resource-name}` 命令检查资源的状态。前者会显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_dedicated_vpc_peering.example
    # tidbcloud_dedicated_vpc_peering.example:
    resource "tidbcloud_dedicated_vpc_peering" "example" {
        aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000"
        customer_account_id           = "986330900000"
        customer_region_id            = "aws-us-west-2"
        customer_vpc_cidr             = "172.16.32.0/21"
        customer_vpc_id               = "vpc-0c0c7d59702000000"
        labels                        = {
            "tidb.cloud/project" = "1372813089187000000"
        }
        project_id                    = "13728130891870000000"
        state                         = "ACTIVE"
        tidb_cloud_account_id         = "380838400000"
        tidb_cloud_cloud_provider     = "aws"
        tidb_cloud_region_id          = "aws-us-west-2"
        tidb_cloud_vpc_cidr           = "10.250.0.0/16"
        tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000"
        vpc_peering_id                = "aws-1934187953894000000"
    }
    ```

## 导入 TiDB Cloud Dedicated VPC Peering

对于未被 Terraform 管理的 TiDB Cloud Dedicated VPC Peering，你可以通过导入将其纳入 Terraform 管理。

例如，你可以导入一个不是通过 Terraform 创建的 VPC Peering。

1. 为新的 `tidbcloud_dedicated_vpc_peering` 资源添加 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你期望的资源名称，将 `${vpc_peering_id}` 替换为实际的 VPC Peering ID。

    ```
    import {
      to = tidbcloud_dedicated_vpc_peering.example
      id = "${vpc_peering_id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 `tidbcloud_dedicated_vpc_peering` 资源生成新的配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

    然后，当前目录下会生成 `generated.tf` 文件，包含了被导入资源的配置信息。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_vpc_peering.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_vpc_peering.example: Import complete [id=aws-19341879538940000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理被导入的 TiDB Cloud Dedicated VPC Peering。

## 删除 TiDB Cloud Dedicated VPC Peering

要删除 TiDB Cloud Dedicated VPC Peering，可以删除 `tidbcloud_dedicated_vpc_peering` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

```shell
  $ terraform apply
  tidbcloud_dedicated_vpc_peering.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

  Terraform will perform the following actions:

  # tidbcloud_dedicated_vpc_peering.example will be destroyed
  # (because tidbcloud_dedicated_vpc_peering.example is not in configuration)
  - resource "tidbcloud_dedicated_vpc_peering" "example" {
      - aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000" -> null
      - customer_account_id           = "986330900000" -> null
      - customer_region_id            = "aws-us-west-2" -> null
      - customer_vpc_cidr             = "172.16.32.0/21" -> null
      - customer_vpc_id               = "vpc-0c0c7d59702000000" -> null
      - labels                        = {
          - "tidb.cloud/project" = "1372813089187000000"
          } -> null
      - project_id                    = "1372813089187000000" -> null
      - state                         = "ACTIVE" -> null
      - tidb_cloud_account_id         = "380838000000" -> null
      - tidb_cloud_cloud_provider     = "aws" -> null
      - tidb_cloud_region_id          = "aws-us-west-2" -> null
      - tidb_cloud_vpc_cidr           = "10.250.0.0/16" -> null
      - tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000" -> null
      - vpc_peering_id                = "aws-1934187953894000000" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

  tidbcloud_dedicated_vpc_peering.example: Destroying...
  tidbcloud_dedicated_vpc_peering.example: Destruction complete after 1s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

此时，如果你运行 `terraform show` 命令，将不会有任何输出，因为资源已被清除：

```
$ terraform show
```