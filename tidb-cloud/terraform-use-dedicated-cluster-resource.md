---
title: 使用 `tidbcloud_dedicated_cluster` 资源
summary: 了解如何使用 `tidbcloud_dedicated_cluster` 资源来创建和修改 TiDB Cloud 专属集群。
---

# 使用 `tidbcloud_dedicated_cluster` 资源

本文档介绍如何使用 `tidbcloud_dedicated_cluster` 资源管理 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

此外，你还将学习如何通过 `tidbcloud_projects` 数据源获取所需信息，并使用 `tidbcloud_dedicated_node_group` 资源管理 TiDB Cloud 专属集群的 TiDB 节点组。

`tidbcloud_dedicated_cluster` 资源的功能包括：

- 创建 TiDB Cloud 专属集群
- 修改 TiDB Cloud 专属集群
- 导入 TiDB Cloud 专属集群
- 删除 TiDB Cloud 专属集群

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB Cloud 专属集群都属于一个项目。在创建 TiDB Cloud 专属集群之前，你需要获取要创建集群的项目 ID。如果未指定 `project_id`，则会使用默认项目。

要获取所有可用项目的信息，可以按如下方式使用 `tidbcloud_projects` 数据源：

1. 在你 [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加如下 `data` 和 `output` 块：

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

    data "tidbcloud_projects" "example_project" {
      page      = 1
      page_size = 10
    }

    output "projects" {
      value = data.tidbcloud_projects.example_project.items
    }
    ```

    - 使用 `data` 块定义 TiDB Cloud 的数据源，包括数据源类型和数据源名称。

        - 若要使用项目数据源，将数据源类型设置为 `tidbcloud_projects`。
        - 数据源名称可根据需要自定义，例如 `"example_project"`。
        - 对于 `tidbcloud_projects` 数据源，可以使用 `page` 和 `page_size` 属性限制你想要查看的最大项目数量。

    - 使用 `output` 块定义要在输出中显示的数据源信息，并将信息暴露给其他 Terraform 配置使用。

        `output` 块的作用类似于编程语言中的返回值。更多信息请参见 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

    若要获取所有资源和数据源的可用配置，请参见 [Terraform provider 配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令以应用配置。你需要在确认提示时输入 `yes` 以继续。

    若要跳过提示，可使用 `terraform apply --auto-approve`：

    ```shell
    $ terraform apply --auto-approve

    Changes to Outputs:
      + projects = [
          + {
              + cluster_count    = 0
              + create_timestamp = "1649154426"
              + id               = "1372813089191000000"
              + name             = "test1"
              + org_id           = "1372813089189000000"
              + user_count       = 1
            },
          + {
              + cluster_count    = 1
              + create_timestamp = "1640602740"
              + id               = "1372813089189000000"
              + name             = "default project"
              + org_id           = "1372813089189000000"
              + user_count       = 1
            },
        ]

    You can apply this plan to save these new output values to the Terraform state, without changing any real infrastructure.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

    Outputs:

    projects = tolist([
      {
        "cluster_count" = 0
        "create_timestamp" = "1649154426"
        "id" = "1372813089100000000"
        "name" = "test1"
        "org_id" = "1372813089100000000"
        "user_count" = 1
      },
      {
        "cluster_count" = 1
        "create_timestamp" = "1640602740"
        "id" = "1372813089100000001"
        "name" = "default project"
        "org_id" = "1372813089100000000"
        "user_count" = 1
      },
    ])
    ```

现在，你可以从输出中获取所有可用项目。复制你需要的项目 ID。

## 创建 TiDB Cloud 专属集群

> **Note:**
>
> - 在开始之前，请确保你已在 [TiDB Cloud 控制台](https://tidbcloud.com) 设置了 CIDR。更多信息请参见 [设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。
> - 你也可以 [创建 `dedicated_network_container` 资源](/tidb-cloud/terraform-use-dedicated-network-container-resource.md) 来管理你的 CIDR。

你可以按如下方式使用 `tidbcloud_dedicated_cluster` 资源创建 TiDB Cloud 专属集群：

1. 为集群创建一个目录并进入该目录。

2. 创建 `cluster.tf` 文件：

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

    resource "tidbcloud_dedicated_cluster" "example_cluster" {
      display_name  = "your_display_name"
      region_id     = "your_region_id"
      port          = 4000
      root_password = "your_root_password"
      tidb_node_setting = {
       node_spec_key = "2C4G"
       node_count    = 1
      }
      tikv_node_setting = {
       node_spec_key   = "2C4G"
       node_count      = 3
       storage_size_gi = 60
       storage_type    = "Standard"
      }
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 若要使用 `tidbcloud_dedicated_cluster` 资源，将资源类型设置为 `tidbcloud_dedicated_cluster`。
    - 资源名称可根据需要自定义，例如 `example_cluster`。
    - 资源详情可根据项目 ID 及 TiDB Cloud 专属集群的规格信息进行配置。
    - 获取 TiDB Cloud 专属集群规格信息，请参见 [tidbcloud_dedicated_cluster (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_cluster)。

3. 运行 `terraform apply` 命令。应用资源时不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform will perform the following actions:

      # tidbcloud_dedicated_cluster.example_cluster will be created
      + resource "tidbcloud_dedicated_cluster" "example_cluster" {
          + annotations         = (known after apply)
          + cloud_provider      = (known after apply)
          + cluster_id          = (known after apply)
          + create_time         = (known after apply)
          + created_by          = (known after apply)
          + display_name        = "test-tf"
          + labels              = (known after apply)
          + pause_plan          = (known after apply)
          + port                = 4000
          + project_id          = (known after apply)
          + region_display_name = (known after apply)
          + region_id           = "aws-us-west-2"
          + state               = (known after apply)
          + tidb_node_setting   = {
              + endpoints               = (known after apply)
              + is_default_group        = (known after apply)
              + node_count              = 1
              + node_group_display_name = (known after apply)
              + node_group_id           = (known after apply)
              + node_spec_display_name  = (known after apply)
              + node_spec_key           = "2C4G"
              + public_endpoint_setting = (known after apply)
              + state                   = (known after apply)
            }
          + tikv_node_setting   = {
              + node_count             = 3
              + node_spec_display_name = (known after apply)
              + node_spec_key          = "2C4G"
              + storage_size_gi        = 60
              + storage_type           = "Standard"
            }
          + update_time         = (known after apply)
          + version             = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    在上述结果中，Terraform 会为你生成一个执行计划，描述 Terraform 将要执行的操作：

    - 你可以检查配置与当前状态之间的差异。
    - 你也可以看到本次 `apply` 的结果。将新增一个资源，不会有资源被更改或销毁。
    - `known after apply` 表示你将在 `apply` 后获得该值。

4. 如果计划中的内容无误，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Creating...
    tidbcloud_dedicated_cluster.example_cluster: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    创建 TiDB Cloud 专属集群通常至少需要 10 分钟。

5. 使用 `terraform show` 或 `terraform state show tidbcloud_dedicated_cluster.${resource-name}` 命令检查资源状态。前者会显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_dedicated_cluster.example_cluster

    # tidbcloud_dedicated_cluster.example_cluster:
    resource "tidbcloud_dedicated_cluster" "example_cluster" {
        annotations         = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        cloud_provider      = "aws"
        cluster_id          = "1379661944600000000"
        create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
        created_by          = "apikey-XXXXXXXX"
        display_name        = "test-tf"
        labels              = {
            "tidb.cloud/organization" = "60000"
            "tidb.cloud/project"      = "3100000"
        }
        port                = 4000
        project_id          = "3100000"
        region_display_name = "Oregon (us-west-2)"
        region_id           = "aws-us-west-2"
        state               = "ACTIVE"
        tidb_node_setting   = {
            endpoints               = [
                {
                    connection_type = "PUBLIC"
                    host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "VPC_PEERING"
                    host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "PRIVATE_ENDPOINT"
                    host            = null
                    port            = 4000
                },
            ]
            is_default_group        = true
            node_count              = 1
            node_group_display_name = "DefaultGroup"
            node_group_id           = "1931960832833000000"
            node_spec_display_name  = "2 vCPU, 4 GiB beta"
            node_spec_key           = "2C4G"
            state                   = "ACTIVE"
        }
        tikv_node_setting   = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Standard"
        }
        update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
        version             = "v7.5.6"
    }
    ```

6. 如果你想从远端同步状态，运行 `terraform refresh` 命令以更新状态，然后运行 `terraform state show tidbcloud_dedicated_cluster.${resource-name}` 命令查看状态。

    ```shell
    $ terraform refresh

    tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

    $ terraform state show tidbcloud_dedicated_cluster.example_cluster

    # tidbcloud_dedicated_cluster.example_cluster:
    resource "tidbcloud_dedicated_cluster" "example_cluster" {
        annotations         = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        cloud_provider      = "aws"
        cluster_id          = "10528940229200000000"
        create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
        created_by          = "apikey-XXXXXXXX"
        display_name        = "test-tf"
        labels              = {
            "tidb.cloud/organization" = "60000"
            "tidb.cloud/project"      = "3190000"
        }
        port                = 4000
        project_id          = "3190000"
        region_display_name = "Oregon (us-west-2)"
        region_id           = "aws-us-west-2"
        state               = "ACTIVE"
        tidb_node_setting   = {
            endpoints               = [
                {
                    connection_type = "PUBLIC"
                    host            = "tidb.taiqixxxxxxx.clusters.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "VPC_PEERING"
                    host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "PRIVATE_ENDPOINT"
                    host            = "privatelink-19319608.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
            ]
            is_default_group        = true
            node_count              = 1
            node_group_display_name = "DefaultGroup"
            node_group_id           = "1931960832800000000"
            node_spec_display_name  = "2 vCPU, 4 GiB beta"
            node_spec_key           = "2C4G"
            public_endpoint_setting = {
                enabled        = false
                ip_access_list = []
            }
            state                   = "ACTIVE"
        }
        tikv_node_setting   = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Standard"
        }
        update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
        version             = "v7.5.6"
    }
    ```

## 修改 TiDB Cloud 专属集群

对于 TiDB Cloud 专属集群，你可以通过 Terraform 管理资源，包括：

- 为集群添加 TiFlash 组件
- 对集群进行扩缩容
- 暂停或恢复集群
- 为集群添加 [TiDB 节点组](/tidb-cloud/tidb-node-group-overview.md)
- 更新集群的 TiDB 节点组
- 删除集群的 TiDB 节点组

### 添加 TiFlash 组件

1. 在 [创建集群](#create-a-tidb-cloud-dedicated-cluster) 时使用的 `cluster.tf` 文件中，添加 `tiflash_node_setting` 配置。

    例如：

    ```
    tiflash_node_setting = {
      node_spec_key = "2C4G"
      node_count = 3
      storage_size_gi = 60
    }
    ```

2. 运行 `terraform apply` 命令：

    ```shell
    $ terraform apply

    tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
          ~ annotations          = {
              - "tidb.cloud/available-features" = "DELEGATE_USER,DISABLE_PUBLIC_LB,PRIVATELINK"
              - "tidb.cloud/has-set-password"   = "false"
            } -> (known after apply)
          ~ labels               = {
              - "tidb.cloud/organization" = "60000"
              - "tidb.cloud/project"      = "3190000"
            } -> (known after apply)
          + pause_plan           = (known after apply)
          ~ state                = "ACTIVE" -> (known after apply)
          ~ tidb_node_setting    = {
              ~ endpoints               = [
                  - {
                      - connection_type = "PUBLIC"
                      - host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "VPC_PEERING"
                      - host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "PRIVATE_ENDPOINT"
                      - host            = "privatelink-19320029.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                ] -> (known after apply)
              ~ node_spec_display_name  = "2 vCPU, 4 GiB" -> (known after apply)
              ~ state                   = "ACTIVE" -> (known after apply)
                # (6 unchanged attributes hidden)
            }
          + tiflash_node_setting = {
              + node_count             = 3
              + node_spec_display_name = (known after apply)
              + node_spec_key          = "2C4G"
              + storage_size_gi        = 60
              + storage_type           = (known after apply)
            }
          ~ tikv_node_setting    = {
              ~ node_spec_display_name = "2 vCPU, 4 GiB" -> (known after apply)
              ~ storage_type           = "Standard" -> (known after apply)
                # (3 unchanged attributes hidden)
            }
          ~ update_time          = "2025-06-06 09:19:01.548 +0000 UTC" -> (known after apply)
          ~ version              = "v7.5.6" -> (known after apply)
            # (9 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes
    ```

    在上述执行计划中，将会添加 TiFlash，且有一个资源会被更改。

3. 如果计划中的内容无误，输入 `yes` 继续：

    ```shell
      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_dedicated_cluster.${resource-name}` 检查状态：

    ```
    $ terraform state show tidbcloud_dedicated_cluster.example_cluster

    # tidbcloud_dedicated_cluster.example_cluster:
    resource "tidbcloud_dedicated_cluster" "example_cluster" {
        annotations         = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        cloud_provider      = "aws"
        cluster_id          = "1379661944600000000"
        create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
        created_by          = "apikey-XXXXXXXX"
        display_name        = "test-tf"
        labels              = {
            "tidb.cloud/organization" = "60000"
            "tidb.cloud/project"      = "3100000"
        }
        port                = 4000
        project_id          = "3100000"
        region_display_name = "Oregon (us-west-2)"
        region_id           = "aws-us-west-2"
        state               = "ACTIVE"
        tidb_node_setting   = {
            endpoints               = [
                {
                    connection_type = "PUBLIC"
                    host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "VPC_PEERING"
                    host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "PRIVATE_ENDPOINT"
                    host            = null
                    port            = 4000
                },
            ]
            is_default_group        = true
            node_count              = 1
            node_group_display_name = "DefaultGroup"
            node_group_id           = "1931960832833000000"
            node_spec_display_name  = "2 vCPU, 4 GiB beta"
            node_spec_key           = "2C4G"
            state                   = "ACTIVE"
        }
        tiflash_node_setting = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Basic"
        }
        tikv_node_setting   = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Standard"
        }
        update_time         = "2025-06-06 08:31:42.974 +0000 UTC"
        version             = "v7.5.6"
    }
    ```

`MODIFYING` 状态表示集群正在被修改。修改完成后状态会变为 `ACTIVE`。

### 集群扩缩容

当集群状态为 `ACTIVE` 时，你可以对 TiDB Cloud 专属集群进行扩缩容。

1. 在 [创建集群](#create-a-tidb-cloud-dedicated-cluster) 时使用的 `cluster.tf` 文件中，编辑 `tidb_node_setting`、`tikv_node_setting` 和 `tiflash_node_setting` 的配置。

    例如，若要增加 1 个 TiDB 节点、3 个 TiKV 节点（TiKV 节点数需为 3 的倍数，因为其扩缩容步长为 3），以及 1 个 TiFlash 节点，可以按如下方式编辑配置：

    ```
     tidb_node_setting = {
       node_spec_key = "8C16G"
       node_count = 2
     }
     tikv_node_setting = {
       node_spec_key = "8C32G"
       node_count = 6
       storage_size_gi = 200
     }
     tiflash_node_setting = {
       node_spec_key = "8C64G"
       node_count = 4
       storage_size_gi = 200
     }
    ```

2. 运行 `terraform apply` 命令并在确认时输入 `yes`：

    ```
    tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
          ~ annotations          = {
              - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
              - "tidb.cloud/has-set-password"   = "false"
            } -> (known after apply)
          ~ labels               = {
              - "tidb.cloud/organization" = "60205"
              - "tidb.cloud/project"      = "3199728"
            } -> (known after apply)
          + pause_plan           = (known after apply)
          ~ state                = "ACTIVE" -> (known after apply)
          ~ tidb_node_setting    = {
              ~ endpoints               = [
                  - {
                      - connection_type = "PUBLIC"
                      - host            = "tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "VPC_PEERING"
                      - host            = "private-tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "PRIVATE_ENDPOINT"
                      - host            = "privatelink-19320029.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                ] -> (known after apply)
              ~ node_count              = 3 -> 2
              ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
              ~ state                   = "ACTIVE" -> (known after apply)
                # (5 unchanged attributes hidden)
            }
          ~ tiflash_node_setting = {
              ~ node_count             = 3 -> 4
              ~ node_spec_display_name = "8 vCPU, 64 GiB" -> (known after apply)
              ~ storage_type           = "Basic" -> (known after apply)
                # (2 unchanged attributes hidden)
            }
          ~ tikv_node_setting    = {
              ~ node_count             = 3 -> 6
              ~ node_spec_display_name = "8 vCPU, 32 GiB" -> (known after apply)
              ~ storage_type           = "Standard" -> (known after apply)
                # (2 unchanged attributes hidden)
            }
          ~ update_time          = "2025-06-09 09:29:25.678 +0000 UTC" -> (known after apply)
          ~ version              = "v7.5.6" -> (known after apply)
            # (9 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

等待过程结束。扩缩容完成后，状态会变为 `ACTIVE`。

### 暂停或恢复集群

当集群状态为 `ACTIVE` 时可以暂停集群，状态为 `PAUSED` 时可以恢复集群。

- 设置 `paused = true` 可暂停集群。
- 设置 `paused = false` 可恢复集群。

1. 在 [创建集群](#create-a-tidb-cloud-dedicated-cluster) 时使用的 `cluster.tf` 文件中，添加 `pause = true` 配置：

    ```
    paused = true
    ```

2. 运行 `terraform apply` 命令并在检查计划后输入 `yes`：

    ```shell
    $ terraform apply

     tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

     Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
       ~ update in-place

     Terraform will perform the following actions:

       # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
       ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
           ~ annotations          = {
               - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
               - "tidb.cloud/has-set-password"   = "false"
             } -> (known after apply)
           ~ labels               = {
               - "tidb.cloud/organization" = "60205"
               - "tidb.cloud/project"      = "3199728"
             } -> (known after apply)
           + pause_plan           = (known after apply)
           + paused               = true
           ~ state                = "ACTIVE" -> (known after apply)
           ~ tidb_node_setting    = {
               ~ endpoints               = [
                   - {
                       - connection_type = "PUBLIC"
                       - host            = "tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                   - {
                       - connection_type = "VPC_PEERING"
                       - host            = "private-tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                   - {
                       - connection_type = "PRIVATE_ENDPOINT"
                       - host            = "privatelink-19320029.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                 ] -> (known after apply)
               ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
               ~ state                   = "ACTIVE" -> (known after apply)
                 # (6 unchanged attributes hidden)
             }
           ~ tiflash_node_setting = {
               ~ node_spec_display_name = "8 vCPU, 64 GiB" -> (known after apply)
               ~ storage_type           = "Basic" -> (known after apply)
                 # (3 unchanged attributes hidden)
             }
           ~ tikv_node_setting    = {
               ~ node_spec_display_name = "8 vCPU, 32 GiB" -> (known after apply)
               ~ storage_type           = "Standard" -> (known after apply)
                 # (3 unchanged attributes hidden)
             }
           ~ update_time          = "2025-06-09 10:01:59.65 +0000 UTC" -> (known after apply)
           ~ version              = "v7.5.6" -> (known after apply)
             # (9 unchanged attributes hidden)
       }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

   Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
   ```

3. 使用 `terraform state show tidbcloud_dedicated_cluster.${resource-name}` 命令检查状态：

    ```
    $ terraform state show tidbcloud_dedicate_cluster.example_cluster

    resource "tidbcloud_dedicated_cluster" "example_cluster" {
         annotations         = {
             "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
             "tidb.cloud/has-set-password"   = "false"
         }
         cloud_provider      = "aws"
         cluster_id          = "1379661944600000000"
         create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
         created_by          = "apikey-XXXXXXXX"
         display_name        = "test-tf"
         labels              = {
             "tidb.cloud/organization" = "60000"
             "tidb.cloud/project"      = "3100000"
         } 
         paused              = true
         port                = 4000
         project_id          = "3100000"
         region_display_name = "Oregon (us-west-2)"
         region_id           = "aws-us-west-2"
         state               = "PAUSED"
         tidb_node_setting   = {
             endpoints               = [
                 {
                     connection_type = "PUBLIC"
                     host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                     port            = 4000
                 },
                 {
                     connection_type = "VPC_PEERING"
                     host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                     port            = 4000
                 },
                 {
                     connection_type = "PRIVATE_ENDPOINT"
                     host            = null
                     port            = 4000
                 },
             ]
             is_default_group        = true
             node_count              = 1
             node_group_display_name = "DefaultGroup"
             node_group_id           = "1931960832833000000"
             node_spec_display_name  = "2 vCPU, 4 GiB beta"
             node_spec_key           = "2C4G"
             state                   = "ACTIVE"
         }
         tikv_node_setting   = {
             node_count             = 3
             node_spec_display_name = "2 vCPU, 4 GiB"
             node_spec_key          = "2C4G"
             storage_size_gi        = 60
             storage_type           = "Standard"
         }
         update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
         version             = "v7.5.6"
     }
    ```

4. 当你需要恢复集群时，将 `paused = false`：

    ```
    paused = false
    ```

5. 运行 `terraform apply` 命令并输入 `yes` 确认。稍等片刻，状态最终会变为 `ACTIVE`。

### 为集群添加 TiDB 节点组

当集群状态为 `ACTIVE` 时，你可以为集群添加 TiDB 节点组。

1. 在 [创建集群](#create-a-tidb-cloud-dedicated-cluster) 时使用的 `cluster.tf` 文件中，添加 `tidbcloud_dedicated_node_group` 配置。

    例如，若要添加一个包含 3 个节点的 TiDB 节点组，可以按如下方式编辑配置：

    ```
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
        node_count = 3
        display_name = "test-node-group"
    }
    ```

2. 运行 `terraform apply` 命令并输入 `yes` 确认：

    ```shell
    $ terraform apply
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     + create

    Terraform will perform the following actions:

     # tidbcloud_dedicated_node_group.example_group will be created
     + resource "tidbcloud_dedicated_node_group" "example_group" {
         + cluster_id              = "10526169210080596964"
         + display_name            = "test-node-group2"
         + endpoints               = (known after apply)
         + is_default_group        = (known after apply)
         + node_count              = 3
         + node_group_id           = (known after apply)
         + node_spec_display_name  = (known after apply)
         + node_spec_key           = (known after apply)
         + public_endpoint_setting = (known after apply)
         + state                   = (known after apply)
       }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_node_group.example_group: Creating...
    tidbcloud_dedicated_node_group.example_group: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

3. 使用 `terraform state show tidbcloud_dedicated_node_group.${resource-name}` 命令检查状态：

    ```shell
    $ terraform state show tidbcloud_dedicated_node_group.example_group
    tidbcloud_dedicated_node_group.example_group:
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id             = "10526169210000000000"
        display_name           = "test-node-group"
        endpoints              = [
            {
                connection_type = "PUBLIC"
                host            = null
                port            = 0
            },
            {
                connection_type = "VPC_PEERING"
                host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                port            = 4000
            },
            {
                connection_type = "PRIVATE_ENDPOINT"
                host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                port            = 4000
            },
        ]
        is_default_group       = false
        node_count             = 3
        node_group_id          = "1932038361900000000"
        node_spec_display_name = "8 vCPU, 16 GiB"
        node_spec_key          = "8C16G"
        state                  = "ACTIVE"
    }
    ```

### 更新集群的 TiDB 节点组

当节点组状态为 `ACTIVE` 时，你可以更新集群的 TiDB 节点组。

1. 在 [创建集群](#create-a-tidb-cloud-dedicated-cluster) 时使用的 `cluster.tf` 文件中，编辑 `tidbcloud_dedicated_node_group` 的配置。

    例如，将节点数更改为 `1`，可按如下方式编辑配置：

    ```
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
        node_count = 1
        display_name = "test-node-group"
    }
    ```

2. 运行 `terraform apply` 命令并输入 `yes` 确认：

    ```shell
    $ terraform apply
    tidbcloud_dedicated_node_group.example_group: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_dedicated_node_group.example_group will be updated in-place
      ~ resource "tidbcloud_dedicated_node_group" "example_group" {
          ~ endpoints               = [
              - {
                  - connection_type = "PUBLIC"
                  - port            = 0
                    # (1 unchanged attribute hidden)
                },
              - {
                  - connection_type = "VPC_PEERING"
                  - host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
              - {
                  - connection_type = "PRIVATE_ENDPOINT"
                  - host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
            ] -> (known after apply)
          ~ node_count              = 3 -> 1
          ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
          ~ node_spec_key           = "8C16G" -> (known after apply)
          ~ state                   = "ACTIVE" -> (known after apply)
            # (5 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_node_group.example_group: Modifying...
    tidbcloud_dedicated_node_group.example_group: Still modifying... [10s elapsed]
    tidbcloud_dedicated_node_group.example_group: Modifications complete after 24s

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

### 删除集群的 TiDB 节点组

要删除集群的 TiDB 节点组，可以删除 `dedicated_node_group` 资源的配置，然后使用 `terraform apply` 命令销毁资源：

  ```shell
    $ terraform apply
    tidbcloud_dedicated_node_group.example_group: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      - destroy

    Terraform will perform the following actions:

      # tidbcloud_dedicated_node_group.example_group will be destroyed
      # (because tidbcloud_dedicated_node_group.example_group is not in configuration)
      - resource "tidbcloud_dedicated_node_group" "example_group" {
          - cluster_id              = "10526169210000000000" -> null
          - display_name            = "test-node-group" -> null
          - endpoints               = [
              - {
                  - connection_type = "PUBLIC"
                  - port            = 0
                    # (1 unchanged attribute hidden)
                },
              - {
                  - connection_type = "VPC_PEERING"
                  - host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
              - {
                  - connection_type = "PRIVATE_ENDPOINT"
                  - host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
            ] -> null
          - is_default_group        = false -> null
          - node_count              = 1 -> null
          - node_group_id           = "1932038361900000000" -> null
          - node_spec_display_name  = "8 vCPU, 16 GiB" -> null
          - node_spec_key           = "8C16G" -> null
          - public_endpoint_setting = {
              - enabled        = false -> null
              - ip_access_list = [] -> null
            } -> null
          - state                   = "PAUSED" -> null
        }

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_node_group.example_group: Destroying...
    tidbcloud_dedicated_node_group.example_group: Destruction complete after 3s

    Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
  ```

现在，如果你运行 `terraform show` 命令，将不会有任何内容输出，因为资源已被清除：

```
$ terraform show
```

## 导入集群

对于未被 Terraform 管理的 TiDB 集群，你可以通过导入的方式让 Terraform 管理它。

导入未由 Terraform 创建的集群，操作如下：

1. 为新的 `tidbcloud_dedicated_cluster` 资源添加 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你想要的资源名称，将 `${id}` 替换为集群 ID：

    ```
    import {
      to = tidbcloud_dedicated_cluster.example_cluster
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 `tidbcloud_dedicated_cluster` 资源生成新的配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会报错。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_dedicated_cluster.example_cluster: Importing... 
    tidbcloud_dedicated_cluster.example_cluster: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理已导入的集群。

## 删除 TiDB Cloud 专属集群

要删除 TiDB Cloud 专属集群，可以删除 `tidbcloud_dedicated_cluster` 资源的配置，然后使用 `terraform apply` 命令销毁资源：

```shell
  $ terraform apply
  tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy
   Terraform will perform the following actions:

    # tidbcloud_dedicated_cluster.example_cluster will be destroyed
    # (because tidbcloud_dedicated_cluster.example_cluster is not in configuration)
    - resource "tidbcloud_dedicated_cluster" "example_cluster" {
        - annotations          = {
            - "tidb.cloud/available-features" = "DELEGATE_USER,DISABLE_PUBLIC_LB,PRIVATELINK"
            - "tidb.cloud/has-set-password"   = "false"
          } -> null
        - cloud_provider       = "aws" -> null
        - cluster_id           = "10526169210000000000" -> null
        - create_time          = "2025-06-06 09:12:55.396 +0000 UTC" -> null
        - created_by           = "apikey-K1R3JIC0" -> null
        - display_name         = "test-tf" -> null
        - labels               = {
            - "tidb.cloud/organization" = "60000"
            - "tidb.cloud/project"      = "3100000"
          } -> null
        - paused               = false -> null
        - port                 = 4000 -> null
        - project_id           = "3100000" -> null
        - region_display_name  = "Oregon (us-west-2)" -> null
        - region_id            = "aws-us-west-2" -> null
        - state                = "ACTIVE" -> null
        - tidb_node_setting    = {
            - endpoints               = [
                - {
                    - connection_type = "PUBLIC"
                    - host            = "tidb.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
                - {
                    - connection_type = "VPC_PEERING"
                    - host            = "private-tidb.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
                - {
                    - connection_type = "PRIVATE_ENDPOINT"
                    - host            = "privatelink-19320000.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
              ] -> null
            - is_default_group        = true -> null
            - node_count              = 2 -> null
            - node_group_display_name = "DefaultGroup" -> null
            - node_group_id           = "1932002964533000000" -> null
            - node_spec_display_name  = "8 vCPU, 16 GiB" -> null
            - node_spec_key           = "8C16G" -> null
            - public_endpoint_setting = {
                - enabled        = true -> null
                - ip_access_list = [
                    - {
                        - cidr_notation = "0.0.0.0/32"
                          # (1 unchanged attribute hidden)
                      },
                  ] -> null
              } -> null
            - state                   = "ACTIVE" -> null
          } -> null
        - tiflash_node_setting = {
            - node_count             = 4 -> null
            - node_spec_display_name = "8 vCPU, 64 GiB" -> null
            - node_spec_key          = "8C64G" -> null
            - storage_size_gi        = 200 -> null
            - storage_type           = "Basic" -> null
          } -> null
        - tikv_node_setting    = {
            - node_count             = 6 -> null
            - node_spec_display_name = "8 vCPU, 32 GiB" -> null
            - node_spec_key          = "8C32G" -> null
            - storage_size_gi        = 200 -> null
            - storage_type           = "Standard" -> null
          } -> null
        - update_time          = "2025-06-06 14:15:29.609 +0000 UTC" -> null
        - version              = "v7.5.6" -> null
      }

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Destroying...
    tidbcloud_dedicated_cluster.example_cluster: Destruction complete after 3s

    Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
  ```

现在，如果你运行 `terraform show` 命令，将不会显示任何受管资源，因为资源已被清除：

```
$ terraform show
```