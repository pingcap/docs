---
title: 使用 TiDB Cloud Dedicated VPC Peering 资源
summary: 了解如何使用 TiDB Cloud Dedicated VPC peering 资源来创建和修改 TiDB Cloud Dedicated VPC peering。
---

# 使用 TiDB Cloud Dedicated VPC Peering 资源

本文描述了如何使用 `tidbcloud_dedicated_vpc_peering` 资源管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) VPC 对等连接。

`tidbcloud_dedicated_vpc_peering` 资源的功能包括：

- 创建 TiDB Cloud Dedicated VPC 对等连接
- 导入 TiDB Cloud Dedicated VPC 对等连接
- 删除 TiDB Cloud Dedicated VPC 对等连接

> **注意：**
>
> TiDB Cloud Dedicated VPC 对等连接资源不能被修改。如果你想更改 TiDB Cloud Dedicated VPC 对等连接的配置，需要先删除现有的，然后再创建一个新的。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 版本 v0.4.0 或更高。

## 创建 TiDB Cloud Dedicated VPC 对等连接

你可以使用 `tidbcloud_dedicated_vpc_peering` 资源来创建 TiDB Cloud Dedicated VPC 对等连接。

以下示例展示了如何创建一个 TiDB Cloud Dedicated VPC 对等连接。

1. 创建一个用于 TiDB Cloud Dedicated VPC 对等连接的目录并进入。

2. 创建 `vpc_peering.tf` 文件：

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

    resource "tidbcloud_dedicated_vpc_peering" "example" {
      tidb_cloud_region_id = "your_tidb_cloud_region_id"
      customer_region_id   = "your_customer_region_id"
      customer_account_id  = "your_customer_account_id"
      customer_vpc_id      = "your_customer_vpc_id"
      customer_vpc_cidr    = "your_customer_vpc_cidr"
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详细信息。

    - 若要使用 TiDB Cloud Dedicated VPC 对等连接资源，资源类型设为 `tidbcloud_dedicated_vpc_peering`。
    - 资源名称可以根据需要定义，例如 `example`。
    - 如果不知道如何获取必需参数的值，请参见 [通过 VPC 对等连接连接到 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md)。
    - 获取 TiDB Cloud Dedicated VPC 对等连接的详细信息，请参见 [tidbcloud_dedicated_vpc_peering (资源)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_vpc_peering)。

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
        + create

    Terraform 将执行以下操作：

        # tidbcloud_dedicated_vpc_peering.example 将被创建
        + resource "tidbcloud_dedicated_vpc_peering" "example" {
            + aws_vpc_peering_connection_id = (应用后确定)
            + customer_account_id           = "986330900000"
            + customer_region_id            = "aws-us-west-2"
            + customer_vpc_cidr             = "172.16.32.0/21"
            + customer_vpc_id               = "vpc-0c0c7d59702000000"
            + labels                        = (应用后确定)
            + project_id                    = (应用后确定)
            + state                         = (应用后确定)
            + tidb_cloud_account_id         = (应用后确定)
            + tidb_cloud_cloud_provider     = (应用后确定)
            + tidb_cloud_region_id          = "aws-us-west-2"
            + tidb_cloud_vpc_cidr           = (应用后确定)
            + tidb_cloud_vpc_id             = (应用后确定)
            + vpc_peering_id                = (应用后确定)
        }

    计划：添加1个，修改0个，删除0个。

    是否执行这些操作？
        Terraform 将执行上述操作。
        只接受 'yes' 以确认。

        输入一个值：
    ```

    在上述输出中，Terraform 为你生成了一个执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你还可以查看此次 `apply` 的结果。它会添加一个新资源，不会更改或删除任何资源。
    - `known after apply` 表示在 `apply` 后你将获得相应的值。

4. 如果一切看起来正常，输入 `yes` 继续：

    ```shell
    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受 'yes' 以确认。

      输入一个值：yes

    tidbcloud_dedicated_vpc_peering.example: 创建中...
    tidbcloud_dedicated_vpc_peering.example: 仍在创建中... [已用时10秒]
    ```

    资源的状态将保持为 `Creating`，直到你在云提供商控制台中批准 VPC 对等连接。批准后，可以参考 [批准并配置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md#step-2-approve-and-configure-the-vpc-peering)，状态将变为 `Active`。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_vpc_peering.${资源名}` 命令检查资源状态。前者显示所有资源和数据源的状态。

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

## 导入 TiDB Cloud Dedicated VPC 对等连接

对于未由 Terraform 管理的 TiDB Cloud Dedicated VPC 对等连接，你可以通过导入来让 Terraform 管理它。

例如，可以导入一个非由 Terraform 创建的 VPC 对等连接。

1. 在你的 `.tf` 文件中添加导入块，替换 `example` 为你想要的资源名，`${id}` 替换为 `cluster_id,vpc_peering_id` 格式：

    ```
    import {
      to = tidbcloud_dedicated_vpc_peering.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud Dedicated VPC 对等连接资源配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    不要在前述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

    这样会在当前目录生成 `generated.tf` 文件，包含导入资源的配置。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。也可以将此文件的内容移动到你偏好的位置。

    然后运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_vpc_peering.example: 正在导入... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_vpc_peering.example: 导入完成 [id=aws-19341879538940000000,example]

    应用完成！共导入资源：1个，新增：0个，变更：0个，删除：0个。
    ```

现在你可以用 Terraform 管理导入的 TiDB Cloud Dedicated VPC 对等连接。

## 删除 TiDB Cloud Dedicated VPC 对等连接

要删除 TiDB Cloud Dedicated VPC 对等连接，可以删除 `tidbcloud_dedicated_vpc_peering` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
  $ terraform apply
  tidbcloud_dedicated_vpc_peering.example: 正在刷新状态...

  Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
  - destroy

  Terraform 将执行以下操作：

  # tidbcloud_dedicated_vpc_peering.example 将被销毁
  # （因为配置中没有 tidbcloud_dedicated_vpc_peering.example）
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

  计划：添加0个，修改0个，删除1个。

  是否执行这些操作？
  Terraform 将执行上述操作。
  只接受 'yes' 以确认。

  输入一个值：yes

  tidbcloud_dedicated_vpc_peering.example: 正在销毁...
  tidbcloud_dedicated_vpc_peering.example: 1秒后销毁完成

  应用完成！资源：0个新增，0个变更，1个销毁。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何内容，因为资源已被清除：

```
$ terraform show
```