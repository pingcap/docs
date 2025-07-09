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

    - 若要使用 TiDB Cloud Dedicated 网络容器资源，设置资源类型为 `tidbcloud_dedicated_network_container`。
    - 资源名称可以根据需要定义，例如 `example`。
    - 如果不知道如何获取必需参数的值，请参见 [为区域设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。
    - 关于 TiDB Cloud Dedicated 网络容器的详细规格，请参见 [tidbcloud_dedicated_network_container (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_network_container)。

3. 运行 `terraform apply` 命令。建议在应用资源时不要使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_network_container.example will be created
        + resource "tidbcloud_dedicated_network_container" "example" {
            + cidr_notation        = "172.16.16.0/21"
            + cloud_provider       = (known after apply)
            + labels               = (known after apply)
            + network_container_id = (known after apply)
            + project_id           = "1372813089454543324"
            + region_display_name  = (known after apply)
            + region_id            = "aws-ap-northeast-2"
            + state                = (known after apply)
            + vpc_id               = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    在上述输出中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，且不会更改或删除任何资源。
    - `known after apply` 表示在 `apply` 后会获得对应的值。

4. 如果一切正常，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_network_container.example: Creating...
    tidbcloud_dedicated_network_container.example: Creation complete after 4s
    ```

    资源的状态将保持为 `INACTIVE`，直到你在该区域创建一个 TiDB Cloud Dedicated 集群。之后，状态会变为 `ACTIVE`。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_network_container.${resource-name}` 命令检查资源状态。前者显示所有资源和数据源的状态。

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

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

    这样会在当前目录生成 `generated.tf` 文件，包含导入资源的配置。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。也可以将其内容移动到你偏好的位置。

    然后运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_network_container.example: Importing... [id=10423692645683000000,example]
    tidbcloud_dedicated_network_container.example: Import complete [id=10423692645683000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以用 Terraform 管理导入的 TiDB Cloud Dedicated 网络容器。

## 删除一个 TiDB Cloud Dedicated 网络容器

要删除一个 TiDB Cloud Dedicated 集群，可以删除 `tidbcloud_dedicated_cluster` 资源的配置，然后运行 `terraform apply` 来销毁资源。但必须确保该 TiDB Cloud Dedicated 网络容器的状态不是 `ACTIVE`。如果是 `ACTIVE`，则不能删除。

如果状态为 `INACTIVE`，可以运行以下命令删除：

```shell
  $ terraform apply
  tidbcloud_dedicated_network_container.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_dedicated_network_container.example will be destroyed
    # (because tidbcloud_dedicated_network_container.example is not in configuration)
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
          # (1 unchanged attribute hidden)
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_dedicated_network_container.example: Destroying...
  tidbcloud_dedicated_network_container.example: Destruction complete after 2s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管资源，因为资源已被清除：

```
$ terraform show
```