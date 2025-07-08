---
title: 使用 TiDB Cloud 专用网络容器资源
summary: 了解如何使用 TiDB Cloud 专用网络容器资源创建和修改 TiDB Cloud 专用网络容器。
---

# 使用 TiDB Cloud 专用网络容器资源

本文档描述了如何使用 `tidbcloud_dedicated_network_container` 资源管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 网络容器。

网络容器是一种逻辑网络资源，允许你为特定项目和区域定义并管理一个 CIDR 块（IP 地址范围）。该 CIDR 块用于为 TiDB Cloud Dedicated 集群创建 VPC，并且在该区域设置 VPC 对等连接之前是必需的。

在向某个区域添加 VPC 对等请求之前，必须先为该区域设置 CIDR 块并创建一个初始的 TiDB Cloud Dedicated 集群。一旦第一个集群创建完成，TiDB Cloud 会自动创建相关联的 VPC，从而使你能够与应用程序的 VPC 建立对等连接。

`tidbcloud_dedicated_network_container` 资源的功能包括：

- 创建 TiDB Cloud Dedicated 网络容器。
- 导入 TiDB Cloud Dedicated 网络容器。
- 删除 TiDB Cloud Dedicated 网络容器。

> **注意：**
>
> 如果状态为 `ACTIVE`，则不能修改或删除 TiDB Cloud Dedicated 网络容器。在应用 `tidbcloud_network_container` 资源配置之前，请确保配置正确。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。

## 创建 TiDB Cloud Dedicated 网络容器

你可以使用 `tidbcloud_dedicated_network_container` 资源创建 TiDB Cloud Dedicated 网络容器。

以下示例演示如何创建一个 TiDB Cloud Dedicated 网络容器。

1. 创建一个用于 TiDB Cloud Dedicated 网络容器的目录并进入。

2. 创建 `network_container.tf` 文件：

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

    resource "tidbcloud_dedicated_network_container" "example" {
      project_id = "1372813089454000000"
      region_id = "aws-ap-northeast-2"
      cidr_notation = "172.16.16.0/21"
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

    - 若要使用 TiDB Cloud Dedicated 网络容器资源，资源类型设为 `tidbcloud_dedicated_network_container`。
    - 资源名称可根据需要定义，例如 `example`。
    - 如果不清楚如何获取必需参数的值，请参见 [为区域设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。
    - 关于 TiDB Cloud Dedicated 网络容器的详细规格，请参见 [tidbcloud_dedicated_network_container (资源)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_network_container)。

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
      + create

    Terraform 将执行以下操作：

        # tidbcloud_dedicated_network_container.example 将被创建
        + resource "tidbcloud_dedicated_network_container" "example" {
            + cidr_notation        = "172.16.16.0/21"
            + cloud_provider       = (应用后已知)
            + labels               = (应用后已知)
            + network_container_id = (应用后已知)
            + project_id           = "1372813089454543324"
            + region_display_name  = (应用后已知)
            + region_id            = "aws-ap-northeast-2"
            + state                = (应用后已知)
            + vpc_id               = (应用后已知)
        }

    计划：添加 1 个资源，变更 0 个资源，销毁 0 个资源。

    是否执行这些操作？
        Terraform 将执行上述操作。
        只接受输入 'yes' 以确认。

        输入一个值：
    ```

    在上述输出中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，且不会变更或销毁任何资源。
    - `known after apply` 表示在 `apply` 后会得到相应的值。

4. 如果一切看起来都正常，输入 `yes` 继续：

    ```shell
    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值: yes

    tidbcloud_dedicated_network_container.example: 正在创建...
    tidbcloud_dedicated_network_container.example: 4秒后创建完成
    ```

    资源的状态将保持 `INACTIVE`，直到你在该区域创建一个 TiDB Cloud Dedicated 集群。之后，状态会变为 `ACTIVE`。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_network_container.${资源名}` 命令检查资源状态。前者显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_dedicated_network_container.example          
    # tidbcloud_dedicated_network_container.example:
    resource "tidbcloud_dedicated_network_container" "example" {
        cidr_notation        = "172.16.16.0/21"
        cloud_provider       = "aws"
        labels               = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        network_container_id = "1934235512696000000"
        project_id           = "1372813089454000000"
        region_display_name  = "Seoul (ap-northeast-2)"
        region_id            = "aws-ap-northeast-2"
        state                = "INACTIVE"
        vpc_id               = null
    }
    ```

## 导入一个 TiDB Cloud Dedicated 网络容器

对于未由 Terraform 管理的 TiDB Cloud Dedicated 网络容器，你可以通过导入来让 Terraform 管理它。

例如，可以导入一个非由 Terraform 创建的网络容器。

1. 在你的 `.tf` 文件中添加导入块，替换 `example` 为你想要的资源名，`${id}` 替换为 `cluster_id,network_container_id` 格式：

    ```
    import {
      to = tidbcloud_dedicated_network_container.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud Dedicated 网络容器资源配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    不要在前述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

    这样会在当前目录生成 `generated.tf` 文件，包含导入资源的配置。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。也可以将其内容移动到你偏好的位置。

    然后运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_network_container.example: 导入中... [id=10423692645683000000,example]
    tidbcloud_dedicated_network_container.example: 导入完成 [id=10423692645683000000,example]

    应用完成！共导入资源：1 个，新增：0 个，变更：0 个，销毁：0 个。
    ```

现在你可以用 Terraform 管理导入的 TiDB Cloud Dedicated 网络容器。

## 删除一个 TiDB Cloud Dedicated 网络容器

要删除一个 TiDB Cloud Dedicated 集群，可以删除 `tidbcloud_dedicated_cluster` 资源的配置，然后运行 `terraform apply` 来销毁资源。但必须确保 TiDB Cloud Dedicated 网络容器的状态不是 `ACTIVE`。如果是 `ACTIVE`，则不能删除。

如果状态为 `INACTIVE`，可以运行以下命令删除：

```shell
  $ terraform apply
  tidbcloud_dedicated_network_container.example: 正在刷新状态...

  Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
    - destroy

  Terraform 将执行以下操作：

    # tidbcloud_dedicated_network_container.example 将被销毁
    # （因为配置中已移除该资源）
    - resource "tidbcloud_dedicated_network_container" "example" {
        - cidr_notation        = "172.16.16.0/21" -> null
        - cloud_provider       = "aws" -> null
        - labels               = {
            - "tidb.cloud/project" = "1372813089454000000"
          } -> null
        - network_container_id = "1934235512696000000" -> null
        - project_id           = "1372813089454000000" -> null
        - region_display_name  = "Seoul (ap-northeast-2)" -> null
        - region_id            = "aws-ap-northeast-2" -> null
        - state                = "INACTIVE" -> null
          # （隐藏1个未变更的属性）
      }

  计划：不添加资源，变更 0 个资源，销毁 1 个资源。

  是否执行这些操作？
    Terraform 将执行上述操作。
    只接受输入 'yes' 以确认。

    输入一个值：yes

  tidbcloud_dedicated_network_container.example: 正在销毁...
  tidbcloud_dedicated_network_container.example: 2秒后销毁完成

  应用完成！资源：0 个新增，0 个变更，1 个销毁。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管资源，因为资源已被清除：

```
$ terraform show
```