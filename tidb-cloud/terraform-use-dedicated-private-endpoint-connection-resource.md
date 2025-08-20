---
title: 使用 `tidbcloud_dedicated_private_endpoint_connection` 资源
summary: 了解如何使用 `tidbcloud_dedicated_private_endpoint_connection` 资源来创建和修改 TiDB Cloud Dedicated 私有终端节点连接。
---

# 使用 `tidbcloud_dedicated_private_endpoint_connection` 资源

本文档介绍如何使用 `tidbcloud_dedicated_private_endpoint_connection` 资源来管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 私有终端节点连接。

`tidbcloud_dedicated_private_endpoint_connection` 资源的功能包括：

- 创建 TiDB Cloud Dedicated 私有终端节点连接。
- 导入 TiDB Cloud Dedicated 私有终端节点连接。
- 删除 TiDB Cloud Dedicated 私有终端节点连接。

> **注意：**
>
> `tidbcloud_dedicated_private_endpoint_connection` 资源无法被修改。如果你想修改 TiDB Cloud Dedicated 私有终端节点连接，需要先删除现有连接，然后重新创建一个新的连接。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。
- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

## 创建 TiDB Cloud Dedicated 私有终端节点连接

你可以使用 `tidbcloud_dedicated_private_endpoint_connection` 资源来创建 TiDB Cloud Dedicated 私有终端节点连接。

以下示例展示了如何创建 TiDB Cloud Dedicated 私有终端节点连接。

1. 为 TiDB Cloud Dedicated 私有终端节点连接创建一个目录并进入该目录。

2. 创建一个 `private_endpoint_connection.tf` 文件：

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

    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
      cluster_id = "your_cluster_id"
      node_group_id = "your_node_group_id"
      endpoint_id = "your_endpoint_id"
    }
    ```

    使用 `resource` 块来定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 要使用 `tidbcloud_dedicated_private_endpoint_connection` 资源，需要将资源类型设置为 `tidbcloud_dedicated_private_endpoint_connection`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 如果你不知道如何获取所需参数的值，请参见 [通过 AWS 私有终端节点连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
    - 如需获取 TiDB Cloud Dedicated 私有终端节点连接的详细配置信息，请参见 [tidbcloud_private_endpoint_connection (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_private_endpoint_connection)。

3. 运行 `terraform apply` 命令。应用资源时，不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_private_endpoint_connection.example will be created
        + resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
            + account_id                     = (known after apply)
            + cloud_provider                 = (known after apply)
            + cluster_display_name           = (known after apply)
            + cluster_id                     = "10757937805044000000"
            + endpoint_id                    = "vpce-03367e9618000000"
            + endpoint_state                 = (known after apply)
            + host                           = (known after apply)
            + labels                         = (known after apply)
            + message                        = (known after apply)
            + node_group_id                  = "1934178998036000000"
            + port                           = (known after apply)
            + private_endpoint_connection_id = (known after apply)
            + private_link_service_name      = (known after apply)
            + region_display_name            = (known after apply)
            + region_id                      = (known after apply)
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

4. 如果你确认计划中的内容无误，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_private_endpoint_connection.example: Creating...
    tidbcloud_dedicated_private_endpoint_connection.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_private_endpoint_connection.${resource-name}` 命令来查看资源的状态。前者会显示所有资源和数据源的状态。

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

## 导入 TiDB Cloud Dedicated 私有终端节点连接

对于未被 Terraform 管理的 TiDB Cloud Dedicated 私有终端节点连接，你可以通过导入的方式让 Terraform 开始管理它。

1. 为新的 `tidbcloud_dedicated_private_endpoint_connection` 资源添加 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你期望的资源名称，将 `${id}` 替换为 `cluster_id,dedicated_private_endpoint_connection_id` 的格式：

    ```
    import {
      to = tidbcloud_dedicated_private_endpoint_connection.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 `tidbcloud_dedicated_private_endpoint_connection` 资源生成新的配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

    然后，当前目录下会生成 `generated.tf` 文件，包含了被导入资源的配置信息。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_private_endpoint_connection.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_private_endpoint_connection.example: Import complete [id=aws-19341879538940000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

    现在你可以使用 Terraform 管理被导入的 TiDB Cloud Dedicated 私有终端节点连接了。

## 删除 TiDB Cloud Dedicated 私有终端节点连接

要删除 TiDB Cloud Dedicated 私有终端节点连接，你可以删除 `tidbcloud_dedicated_private_endpoint_connection` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

```shell
  $ terraform apply
  tidbcloud_dedicated_private_endpoint_connection.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

  Terraform will perform the following actions:

  # tidbcloud_dedicated_private_endpoint_connection.example will be destroyed
  # (because tidbcloud_dedicated_private_endpoint_connection.example is not in configuration)
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

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

  tidbcloud_dedicated_private_endpoint_connection.example: Destroying...
  tidbcloud_dedicated_private_endpoint_connection.example: Destruction complete after 1s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会有任何输出，因为该资源已被清除：

```
$ terraform show
```