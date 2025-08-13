---
title: 使用 Cluster 资源（已弃用）
summary: 了解如何使用 cluster 资源创建和修改 TiDB Cloud 集群。
---

# 使用 Cluster 资源（已弃用）

> **Warning:**
>
> 从 [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) v0.4.0 开始，`tidbcloud_cluster` 资源已被弃用。推荐使用 `tidbcloud_dedicated_cluster` 或 `tidbcloud_serverless_cluster` 资源。更多信息请参见 [使用 TiDB Cloud 专属集群资源](/tidb-cloud/terraform-use-dedicated-cluster-resource.md) 或 [使用 TiDB Cloud Serverless 集群资源](/tidb-cloud/terraform-use-serverless-cluster-resource.md)。

你可以在本文档中学习如何使用 `tidbcloud_cluster` 资源管理 TiDB Cloud 集群。

此外，你还将学习如何通过 `tidbcloud_projects` 和 `tidbcloud_cluster_specs` 数据源获取所需信息。

`tidbcloud_cluster` 资源的功能包括：

- 创建 TiDB Cloud Serverless 和 TiDB Cloud 专属集群。
- 修改 TiDB Cloud 专属集群。
- 删除 TiDB Cloud Serverless 和 TiDB Cloud 专属集群。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB 集群都属于一个项目。在创建 TiDB 集群之前，你需要获取要创建集群的项目 ID。

要查看所有可用项目的信息，可以按如下方式使用 `tidbcloud_projects` 数据源：

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
     sync = true
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
      - 数据源名称可根据需要自定义，例如 "example_project"。
      - 对于 `tidbcloud_projects` 数据源，可以通过 `page` 和 `page_size` 属性限制你要查询的最大项目数。

   - 使用 `output` 块定义要在输出中显示的数据源信息，并将信息暴露给其他 Terraform 配置使用。

      `output` 块的作用类似于编程语言中的返回值。详见 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

   要获取所有资源和数据源的可用配置项，请参见此 [配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令以应用配置。你需要在确认提示时输入 `yes` 以继续。

   若要跳过提示，可使用 `terraform apply --auto-approve`：

   ```
   $ terraform apply --auto-approve

   Changes to Outputs:
     + projects = [
         + {
             + cluster_count    = 0
             + create_timestamp = "1649154426"
             + id               = "1372813089191121286"
             + name             = "test1"
             + org_id           = "1372813089189921287"
             + user_count       = 1
           },
         + {
             + cluster_count    = 1
             + create_timestamp = "1640602740"
             + id               = "1372813089189561287"
             + name             = "default project"
             + org_id           = "1372813089189921287"
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
       "id" = "1372813089191121286"
       "name" = "test1"
       "org_id" = "1372813089189921287"
       "user_count" = 1
     },
     {
       "cluster_count" = 1
       "create_timestamp" = "1640602740"
       "id" = "1372813089189561287"
       "name" = "default project"
       "org_id" = "1372813089189921287"
       "user_count" = 1
     },
   ])
   ```

现在，你可以从输出中获取所有可用项目。复制你需要的项目 ID。

## 使用 `tidbcloud_cluster_specs` 数据源获取集群规格信息

在创建集群之前，你需要获取集群规格信息，其中包含所有可用的配置值（如支持的云服务商、区域和节点规格）。

要获取集群规格信息，可以按如下方式使用 `tidbcloud_cluster_specs` 数据源：

1. 按如下方式编辑 `main.tf` 文件：

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
      sync = true
    }
    data "tidbcloud_cluster_specs" "example_cluster_spec" {
    }
    output "cluster_spec" {
      value = data.tidbcloud_cluster_specs.example_cluster_spec.items
    }
    ```

2. 运行 `terraform apply --auto-approve` 命令，你将获得集群规格信息。

    点击下方行可参考部分示例结果。

    <details>
      <summary>Cluster specification</summary>

    ```
    {
        "cloud_provider" = "AWS"
        "cluster_type" = "DEDICATED"
        "region" = "eu-central-1"
        "tidb" = tolist([
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "4C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "8C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "16C32G"
          },
        ])
        "tiflash" = tolist([
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "16C128G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
        ])
        "tikv" = tolist([
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "4C16G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 200
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C32G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "16C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
        ])
      }
    ```

    </details>

在结果中：

- `cloud_provider` 表示 TiDB 集群可部署的云服务商。
- `region` 表示 `cloud_provider` 的区域。
- `node_quantity_range` 显示节点数量的最小值和扩容步长。
- `node_size` 表示节点规格。
- `storage_size_gib_range` 显示你可为节点设置的最小和最大存储空间。

## 使用 cluster 资源创建集群

> **Note:**
>
> 在开始之前，请确保你已在 TiDB Cloud 控制台设置了 CIDR。更多信息请参见 [设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

你可以使用 `tidbcloud_cluster` 资源创建集群。

以下示例展示如何创建一个 TiDB Cloud 专属集群。

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
     sync = true
   }

    resource "tidbcloud_cluster" "example_cluster" {
      project_id     = "1372813089189561287"
      name           = "firstCluster"
      cluster_type   = "DEDICATED"
      cloud_provider = "AWS"
      region         = "eu-central-1"
      config = {
        root_password = "Your_root_password1."
        port = 4000
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500,
            node_quantity : 3
          }
        }
      }
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 若要使用集群资源，将资源类型设置为 `tidbcloud_cluster`。
    - 资源名称可根据需要自定义，例如 `example_cluster`。
    - 资源详情可根据项目 ID 和集群规格信息进行配置。

3. 运行 `terraform apply` 命令。应用资源时不推荐使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be created
      + resource "tidbcloud_cluster" "example_cluster" {
          + cloud_provider = "AWS"
          + cluster_type   = "DEDICATED"
          + config         = {
              + components     = {
                  + tidb = {
                      + node_quantity = 1
                      + node_size     = "8C16G"
                    }
                  + tikv = {
                      + node_quantity    = 3
                      + node_size        = "8C32G"
                      + storage_size_gib = 500
                    }
                }
              + ip_access_list = [
                  + {
                      + cidr        = "0.0.0.0/0"
                      + description = "all"
                    },
                ]
              + port           = 4000
              + root_password  = "Your_root_password1."
            }
          + id             = (known after apply)
          + name           = "firstCluster"
          + project_id     = "1372813089189561287"
          + region         = "eu-central-1"
          + status         = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

   如上所示，Terraform 会为你生成一个执行计划，描述将要执行的操作：

   - 你可以检查配置与当前状态的差异。
   - 你还可以看到本次 `apply` 的结果。将新增一个资源，不会有资源被更改或销毁。
   - `known after apply` 表示你将在 `apply` 后获得该值。

4. 如果计划中的内容无误，输入 `yes` 继续：

    ```
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Creating...
    tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查资源状态。前者会显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "CREATING"
    }
    ```

    此时集群状态为 `CREATING`。你需要等待其变为 `AVAILABLE`，通常至少需要 10 分钟。

6. 如果你想查看最新状态，运行 `terraform refresh` 命令以更新状态，然后运行 `terraform state show tidbcloud_cluster.${resource-name}` 命令显示状态。

    ```
    $ terraform refresh

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    $ terraform state show tidbcloud_cluster.example_cluste

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

当状态为 `AVAILABLE` 时，表示你的 TiDB 集群已创建并可用。

## 修改 TiDB Cloud 专属集群

对于 TiDB Cloud 专属集群，你可以通过 Terraform 管理集群资源，包括：

- 为集群添加 TiFlash 组件。
- 扩容集群。
- 暂停或恢复集群。

### 添加 TiFlash 组件

1. 在 [创建集群](#create-a-cluster-using-the-cluster-resource) 时使用的 `cluster.tf` 文件中，在 `components` 字段添加 `tiflash` 配置。

    例如：

    ```
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 3
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 1
          }
        }
    ```

2. 运行 `terraform apply` 命令：

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              ~ components     = {
                  + tiflash = {
                      + node_quantity    = 1
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                    # (2 unchanged attributes hidden)
                }
                # (3 unchanged attributes hidden)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (known after apply)
            # (4 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:

    ```

    如上执行计划，TiFlash 将被添加，并有一个资源被更改。

3. 如果计划无误，输入 `yes` 继续：

    ```
      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_cluster.${resource-name}` 查看状态：

    ```
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb    = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 1
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "MODIFYING"
    }
    ```

`MODIFYING` 状态表示集群正在变更。稍等片刻，状态会变为 `AVAILABLE`。

### 扩容 TiDB 集群

当集群状态为 `AVAILABLE` 时，你可以扩容 TiDB 集群。

1. 在 [创建集群](#create-a-cluster-using-the-cluster-resource) 时使用的 `cluster.tf` 文件中，编辑 `components` 配置。

    例如，若要为 TiDB 增加 1 个节点，为 TiKV 增加 3 个节点（TiKV 节点数需为 3 的倍数，因为步长为 3。你可以 [从集群规格获取此信息](#get-cluster-specification-information-using-the-tidbcloud_cluster_specs-data-source)），为 TiFlash 增加 1 个节点，可按如下方式编辑配置：

   ```
       components = {
         tidb = {
           node_size : "8C16G"
           node_quantity : 2
         }
         tikv = {
           node_size : "8C32G"
           storage_size_gib : 500
           node_quantity : 6
         }
         tiflash = {
           node_size : "8C64G"
           storage_size_gib : 500
           node_quantity : 2
         }
       }
   ```

2. 运行 `terraform apply` 命令并输入 `yes` 进行确认：

   ```
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     ~ update in-place

   Terraform will perform the following actions:

     # tidbcloud_cluster.example_cluster will be updated in-place
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             ~ components     = {
                 ~ tidb    = {
                     ~ node_quantity = 1 -> 2
                       # (1 unchanged attribute hidden)
                   }
                 ~ tiflash = {
                     ~ node_quantity    = 1 -> 2
                       # (2 unchanged attributes hidden)
                   }
                 ~ tikv    = {
                     ~ node_quantity    = 3 -> 6
                       # (2 unchanged attributes hidden)
                   }
               }
               # (3 unchanged attributes hidden)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (known after apply)
           # (4 unchanged attributes hidden)
       }

   Plan: 0 to add, 1 to change, 0 to destroy.

   Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

     Enter a value: yes

   tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

   Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
   ```

等待状态从 `MODIFYING` 变为 `AVAILABLE`。

### 暂停或恢复集群

当集群状态为 `AVAILABLE` 时你可以暂停集群，状态为 `PAUSED` 时可以恢复集群。

- 设置 `paused = true` 可暂停集群。
- 设置 `paused = false` 可恢复集群。

1. 在 [创建集群](#create-a-cluster-using-the-cluster-resource) 时使用的 `cluster.tf` 文件中，在 `config` 配置中添加 `pause = true`：

   ```
   config = {
       paused = true
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

2. 运行 `terraform apply` 命令并检查后输入 `yes`：

   ```
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     ~ update in-place

   Terraform will perform the following actions:

     # tidbcloud_cluster.example_cluster will be updated in-place
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             + paused         = true
               # (4 unchanged attributes hidden)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (known after apply)
           # (4 unchanged attributes hidden)
       }

   Plan: 0 to add, 1 to change, 0 to destroy.

   Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

     Enter a value: yes

   tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

   Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
   ```

3. 使用 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查状态：

   ```
   $ terraform state show tidbcloud_cluster.example_cluster

   # tidbcloud_cluster.example_cluster:
   resource "tidbcloud_cluster" "example_cluster" {
       cloud_provider = "AWS"
       cluster_type   = "DEDICATED"
       config         = {
           components     = {
               tidb    = {
                   node_quantity = 2
                   node_size     = "8C16G"
               }
               tiflash = {
                   node_quantity    = 2
                   node_size        = "8C64G"
                   storage_size_gib = 500
               }
               tikv    = {
                   node_quantity    = 6
                   node_size        = "8C32G"
                   storage_size_gib = 500
               }
           }
           ip_access_list = [
               # (1 unchanged element hidden)
           ]
           paused         = true
           port           = 4000
           root_password  = "Your_root_password1."
       }
       id             = "1379661944630234067"
       name           = "firstCluster"
       project_id     = "1372813089189561287"
       region         = "eu-central-1"
       status         = "PAUSED"
   }
   ```

4. 需要恢复集群时，将 `paused = false`：

   ```
   config = {
       paused = false
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

5. 运行 `terraform apply` 命令并输入 `yes` 进行确认。使用 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查状态，你会发现状态变为 `RESUMING`：

   ```
   # tidbcloud_cluster.example_cluster:
   resource "tidbcloud_cluster" "example_cluster" {
       cloud_provider = "AWS"
       cluster_type   = "DEDICATED"
       config         = {
           components     = {
               tidb    = {
                   node_quantity = 2
                   node_size     = "8C16G"
               }
               tiflash = {
                   node_quantity    = 2
                   node_size        = "8C64G"
                   storage_size_gib = 500
               }
               tikv    = {
                   node_quantity    = 6
                   node_size        = "8C32G"
                   storage_size_gib = 500
               }
           }
           ip_access_list = [
               # (1 unchanged element hidden)
           ]
           paused         = false
           port           = 4000
           root_password  = "Your_root_password1."
       }
       id             = "1379661944630234067"
       name           = "firstCluster"
       project_id     = "1372813089189561287"
       region         = "eu-central-1"
       status         = "RESUMING"
   }
   ```

6. 稍等片刻后，使用 `terraform refersh` 命令更新状态，最终状态会变为 `AVAILABLE`。

现在，你已经使用 Terraform 创建并管理了 TiDB Cloud 专属集群。接下来，你可以尝试通过我们的 [备份资源](/tidb-cloud/terraform-use-backup-resource.md) 为集群创建备份。

## 导入集群

对于未被 Terraform 管理的 TiDB 集群，你可以通过导入的方式让 Terraform 管理它。

例如，你可以导入一个非 Terraform 创建的集群，或导入一个 [通过 restore 资源创建的集群](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task)。

1. 创建 `import_cluster.tf` 文件如下：

    ```
    terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
       }
     }
   }
    resource "tidbcloud_cluster" "import_cluster" {}
    ```

2. 通过 `terraform import tidbcloud_cluster.import_cluster projectId,clusterId` 导入集群：

   例如：

    ```
    $ terraform import tidbcloud_cluster.import_cluster 1372813089189561287,1379661944630264072

    tidbcloud_cluster.import_cluster: Importing from ID "1372813089189561287,1379661944630264072"...
    tidbcloud_cluster.import_cluster: Import prepared!
      Prepared tidbcloud_cluster for import
    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    Import successful!

    The resources that were imported are shown above. These resources are now in
    your Terraform state and will henceforth be managed by Terraform.
    ```

3. 运行 `terraform state show tidbcloud_cluster.import_cluster` 命令检查集群状态：

    ```
    $ terraform state show tidbcloud_cluster.import_cluster

    # tidbcloud_cluster.import_cluster:
    resource "tidbcloud_cluster" "import_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            port       = 4000
        }
        id             = "1379661944630264072"
        name           = "restoreCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

4. 若要通过 Terraform 管理集群，可以将上一步的输出复制到你的配置文件中。注意需要删除 `id` 和 `status` 两行，因为它们将由 Terraform 控制：

    ```
    resource "tidbcloud_cluster" "import_cluster" {
          cloud_provider = "AWS"
          cluster_type   = "DEDICATED"
          config         = {
              components = {
                  tidb    = {
                      node_quantity = 2
                      node_size     = "8C16G"
                  }
                  tiflash = {
                      node_quantity    = 2
                      node_size        = "8C64G"
                      storage_size_gib = 500
                  }
                  tikv    = {
                      node_quantity    = 6
                      node_size        = "8C32G"
                      storage_size_gib = 500
                  }
              }
              port       = 4000
          }
          name           = "restoreCluster"
          project_id     = "1372813089189561287"
          region         = "eu-central-1"
    }
    ```

5. 你可以使用 `terraform fmt` 格式化你的配置文件：

    ```
    $ terraform fmt
    ```

6. 为确保配置与状态一致，可以执行 `terraform plan` 或 `terraform apply`。如果看到 `No changes`，则说明导入成功。

    ```
    $ terraform apply

    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    No changes. Your infrastructure matches the configuration.

    Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理该集群。

## 删除集群

要删除集群，请进入包含对应 `cluster.tf` 文件的集群目录，然后运行 `terraform destroy` 命令销毁集群资源：

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

此时，如果你运行 `terraform show` 命令，将不会有任何输出，因为资源已被清除：

```
$ terraform show
```
