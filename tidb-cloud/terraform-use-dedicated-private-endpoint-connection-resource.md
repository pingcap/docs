---
title: 使用 TiDB Cloud Dedicated Private Endpoint 连接资源
summary: 了解如何使用 TiDB Cloud Dedicated 私有端点连接资源来创建和修改 TiDB Cloud Dedicated 私有端点连接。
---

# 使用 TiDB Cloud Dedicated Private Endpoint 连接资源

本文描述了如何使用 `tidbcloud_dedicated_private_endpoint_connection` 资源管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 私有端点连接。

`tidbcloud_dedicated_private_endpoint_connection` 资源的功能包括：

- 创建 TiDB Cloud Dedicated 私有端点连接。
- 导入 TiDB Cloud Dedicated 私有端点连接。
- 删除 TiDB Cloud Dedicated 私有端点连接。

> **Note:**
>
> TiDB Cloud Dedicated 私有端点连接资源不能被修改。如果你想修改一个 TiDB Cloud Dedicated 私有端点连接，需要先删除现有的，然后再创建一个新的。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。
- [创建一个 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

## 创建一个 TiDB Cloud Dedicated 私有端点连接

你可以使用 `tidbcloud_dedicated_private_endpoint_connection` 资源创建 TiDB Cloud Dedicated 私有端点连接。

以下示例展示了如何创建一个 TiDB Cloud Dedicated 私有端点连接。

1. 创建一个用于 TiDB Cloud Dedicated 私有端点连接的目录并进入。

2. 创建 `private_endpoint_connection.tf` 文件：

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

    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
      cluster_id = "your_cluster_id"
      node_group_id = "your_node_group_id"
      endpoint_id = "your_endpoint_id"
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

    - 若要使用 TiDB Cloud Dedicated 私有端点连接资源，资源类型设为 `tidbcloud_dedicated_private_endpoint_connection`。
    - 资源名称可以根据需要定义，例如 `example`。
    - 如果不知道如何获取必需参数的值，请参见 [通过私有端点连接到 AWS 上的 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
    - 获取 TiDB Cloud Dedicated 私有端点连接规格信息，请参见 [tidbcloud_private_endpoint_connection (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_private_endpoint_connection)。

3. 运行 `terraform apply` 命令。建议在应用资源时不要使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
      + create

    Terraform 将执行以下操作：

        # tidbcloud_dedicated_private_endpoint_connection.example 将被创建
        + resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
            + account_id                     = (应用后已知)
            + cloud_provider                 = (应用后已知)
            + cluster_display_name           = (应用后已知)
            + cluster_id                     = "10757937805044000000"
            + endpoint_id                    = "vpce-03367e9618000000"
            + endpoint_state                 = (应用后已知)
            + host                           = (应用后已知)
            + labels                         = (应用后已知)
            + message                        = (应用后已知)
            + node_group_id                  = "1934178998036000000"
            + port                           = (应用后已知)
            + private_endpoint_connection_id = (应用后已知)
            + private_link_service_name      = (应用后已知)
            + region_display_name            = (应用后已知)
            + region_id                      = (应用后已知)
        }

    计划：添加 1 个资源，修改 0 个资源，删除 0 个资源。

    你是否要执行这些操作？
        Terraform 将执行上述操作。
        只接受输入 'yes' 以确认。

        输入一个值：
    ```

    在上述输出中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，不会更改或删除任何资源。
    - `应用后已知` 表示你在 `apply` 后会获得对应的值。

4. 如果计划中的内容都没有问题，输入 `yes` 继续：

    ```shell
    你是否要执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：yes

    tidbcloud_dedicated_private_endpoint_connection.example: Creating...
    tidbcloud_dedicated_private_endpoint_connection.example: Creation complete after 10s

    应用完成！资源：1 个已添加，0 个已更改，0 个已删除。
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_private_endpoint_connection.${resource-name}` 命令检查资源状态。前者显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_dedicated_private_endpoint_connection.example
    # tidbcloud_dedicated_private_endpoint_connection.example:
    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
        cloud_provider                 = "aws"
        cluster_display_name           = "test-tf"
        cluster_id                     = "10757937805044000000"
        endpoint_id                    = "vpce-03367e96180000000"
        endpoint_state                 = "ACTIVE"
        host                           = "privatelink-19341000.ubkypd000000.clusters.tidb-cloud.com"
        labels                         = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist"
        node_group_id                  = "1934178998036000000"
        port                           = 4000
        private_endpoint_connection_id = "1934214559409000000"
        private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000"
        region_display_name            = "Oregon (us-west-2)"
        region_id                      = "aws-us-west-2"
    }
    ```

## 导入一个 TiDB Cloud Dedicated 私有端点连接

对于未由 Terraform 管理的 TiDB Cloud Dedicated 私有端点连接，你可以通过导入开始用 Terraform 管理。

1. 在你的 `.tf` 文件中添加导入块，替换 `example` 为你想要的资源名，`${id}` 替换为 `cluster_id,dedicated_private_endpoint_connection_id` 格式：

    ```
    import {
      to = tidbcloud_dedicated_private_endpoint_connection.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud Dedicated 私有端点连接资源配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    不要在前述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

    这样会在当前目录生成 `generated.tf` 文件，包含导入资源的配置。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。也可以将此文件的内容移动到你偏好的位置。

    然后运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_private_endpoint_connection.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_private_endpoint_connection.example: Import complete [id=aws-19341879538940000000,example]

    应用完成！资源：1 个已导入，0 个已添加，0 个已更改，0 个已删除。
    ```

    现在你可以用 Terraform 管理导入的 TiDB Cloud Dedicated 私有端点连接。

## 删除一个 TiDB Cloud Dedicated 私有端点连接

要删除 TiDB Cloud Dedicated 私有端点连接，可以删除 `tidbcloud_dedicated_private_endpoint_connection` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
  $ terraform apply
  tidbcloud_dedicated_private_endpoint_connection.example: 正在刷新状态...

  Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
  - destroy

  Terraform 将执行以下操作：

  # tidbcloud_dedicated_private_endpoint_connection.example 将被销毁
  # （因为配置中没有 tidbcloud_dedicated_private_endpoint_connection.example）
  - resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
      - cloud_provider                 = "aws" -> null
      - cluster_display_name           = "test-tf" -> null
      - cluster_id                     = "10757937805044000000" -> null
      - endpoint_id                    = "vpce-03367e96180000000" -> null
      - endpoint_state                 = "ACTIVE" -> null
      - host                           = "privatelink-19341000.ubkypd1sx000.clusters.tidb-cloud.com" -> null
      - labels                         = {
          - "tidb.cloud/project" = "1372813089454000000"
          } -> null
      - message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist" -> null
      - node_group_id                  = "1934178998036000000" -> null
      - port                           = 4000 -> null
      - private_endpoint_connection_id = "1934214559409000000" -> null
      - private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000" -> null
      - region_display_name            = "Oregon (us-west-2)" -> null
      - region_id                      = "aws-us-west-2" -> null
      }

  计划：不添加资源，未更改资源，删除 1 个资源。

  你是否要执行这些操作？
  Terraform 将执行上述操作。
  只接受输入 'yes' 以确认。

  输入一个值：yes

  tidbcloud_dedicated_private_endpoint_connection.example: 正在销毁...
  tidbcloud_dedicated_private_endpoint_connection.example: 1 秒后完成销毁

  应用完成！资源：0 个已添加，0 个已更改，1 个已删除。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何内容，因为资源已被清除：

```
$ terraform show
```