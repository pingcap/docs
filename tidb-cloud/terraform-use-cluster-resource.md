---
title: 使用集群资源（已废弃）
summary: 学习如何使用集群资源创建和修改 TiDB Cloud 集群。
---

# 使用集群资源（已废弃）

> **Warning:**
>
> 从 [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) v0.4.0 开始，`tidbcloud_cluster` 资源已被废弃。建议使用 `tidbcloud_dedicated_cluster` 或 `tidbcloud_serverless_cluster` 资源。更多信息请参见 [使用 TiDB Cloud 专用集群资源](/tidb-cloud/terraform-use-dedicated-cluster-resource.md) 或 [使用 TiDB Cloud 无服务器集群资源](/tidb-cloud/terraform-use-serverless-cluster-resource.md)。

本文档将介绍如何使用 `tidbcloud_cluster` 资源管理 TiDB Cloud 集群。

此外，你还将学习如何通过 `tidbcloud_projects` 和 `tidbcloud_cluster_specs` 数据源获取必要的信息。

`tidbcloud_cluster` 资源的功能包括：

- 创建 TiDB Cloud 无服务器和专用集群。
- 修改 TiDB Cloud 专用集群。
- 删除 TiDB Cloud 无服务器和专用集群。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB 集群都属于一个项目。在创建集群之前，你需要获取你想要创建集群的项目 ID。

要查看所有可用项目的信息，可以使用 `tidbcloud_projects` 数据源，示例如下：

1. 在你 [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加 `data` 和 `output` 块：

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
     sync        = true
   }

   data "tidbcloud_projects" "example_project" {
     page      = 1
     page_size = 10
   }

   output "projects" {
     value = data.tidbcloud_projects.example_project.items
   }
   ```

   - 使用 `data` 块定义 TiDB Cloud 的数据源，包括数据源类型和名称。

      - 若要使用项目数据源，设置类型为 `tidbcloud_projects`。
      - 数据源名称可根据需要定义，例如 "example_project"。
      - `page` 和 `page_size` 属性用于限制最多查询的项目数量。

   - 使用 `output` 块定义要在输出中显示的数据源信息，方便其他 Terraform 配置调用。

      `output` 块的作用类似于编程语言中的返回值。详情请参见 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

   若要获取所有资源和数据源的配置项，请参阅此 [配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令应用配置。确认提示输入 `yes` 以继续。

   若要跳过提示，可以使用 `terraform apply --auto-approve`：

   ```bash
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

现在，你可以从输出中获取所有可用的项目。复制你需要的某个项目 ID。

## 使用 `tidbcloud_cluster_specs` 数据源获取集群规格信息

在创建集群之前，你需要获取集群规格信息，其中包含所有可用的配置值（如支持的云提供商、区域和节点大小）。

要获取集群规格信息，可以使用 `tidbcloud_cluster_specs` 数据源，示例如下：

1. 编辑 `main.tf` 文件，内容如下：

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
     sync        = true
   }
   data "tidbcloud_cluster_specs" "example_cluster_spec" {
   }
   output "cluster_spec" {
     value = data.tidbcloud_cluster_specs.example_cluster_spec.items
   }
   ```

2. 运行 `terraform apply --auto-approve` 命令，即可获取集群规格信息。

以下为部分示例结果，点击展开查看：

<details>
  <summary>集群规格</summary>

```json
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

- `cloud_provider` 表示 TiDB 集群可以托管的云提供商。
- `region` 表示 `cloud_provider` 的区域。
- `node_quantity_range` 显示最小节点数和扩展的步长。
- `node_size` 表示节点的大小。
- `storage_size_gib_range` 显示可以为节点设置的最小和最大存储容量。

## 使用集群资源创建集群

> **Note:**
>
> 在开始之前，请确保你已在 TiDB Cloud 控制台设置了 CIDR。更多信息请参见 [设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

你可以使用 `tidbcloud_cluster` 资源创建集群。

以下示例演示如何创建一个 TiDB Cloud 专用集群。

1. 创建一个集群目录并进入。

2. 创建 `cluster.tf` 文件：

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
     sync        = true
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
           node_size     = "8C16G"
           node_quantity = 1
         }
         tikv = {
           node_size        = "8C32G"
           storage_size_gib = 500
           node_quantity    = 3
         }
       }
     }
   }
   ```

   使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、名称和详细配置。

   - 资源类型设置为 `tidbcloud_cluster`。
   - 资源名称可根据需要定义，例如 `example_cluster`。
   - 资源详细信息根据项目 ID 和集群规格配置。

3. 运行 `terraform apply` 命令。建议不要使用 `terraform apply --auto-approve` 直接应用资源。

   ```bash
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

   如上所示，Terraform 会生成执行计划，描述将要执行的操作：

   - 你可以检查配置与状态的差异。
   - 你也可以看到此次 `apply` 的结果。它会添加一个新资源，没有资源会被更改或销毁。
   - `known after apply` 表示在 `apply` 后会获得的值。

4. 如果一切正常，输入 `yes` 继续：

   ```bash
   Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

     Enter a value: yes

   tidbcloud_cluster.example_cluster: Creating...
   tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

   Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
   ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_cluster.${resource-name}` 查看资源状态。前者显示所有资源和数据源的状态。

   ```bash
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

   集群状态为 `CREATING`，此时需要等待其变为 `AVAILABLE`，通常至少需要 10 分钟。

6. 若要查看最新状态，运行 `terraform refresh` 更新状态，然后再次运行 `terraform state show tidbcloud_cluster.${resource-name}`。

   ```bash
   $ terraform refresh

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

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
       status         = "AVAILABLE"
   }
   ```

当状态变为 `AVAILABLE` 时，表示你的 TiDB 集群已创建完成并可以使用。

## 修改 TiDB Cloud 专用集群

对于 TiDB Cloud 专用集群，你可以通过 Terraform 管理集群资源，包括：

- 添加 TiFlash 组件
- 扩展集群规模
- 暂停或恢复集群

### 添加 TiFlash 组件

1. 在你 [创建集群](#创建集群-使用集群资源) 时的 `cluster.tf` 文件中，向 `components` 字段添加 `tiflash` 配置。

   例如：

   ```hcl
       components = {
         tidb = {
           node_size     = "8C16G"
           node_quantity = 1
         }
         tikv = {
           node_size        = "8C32G"
           storage_size_gib = 500
           node_quantity    = 3
         }
         tiflash = {
           node_size        = "8C64G"
           storage_size_gib = 500
           node_quantity    = 1
         }
       }
   ```

2. 运行 `terraform apply`：

   ```bash
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform 使用选定的提供者生成以下执行计划。资源操作用符号表示：
     ~ in-place 更新

   Terraform 将执行以下操作：

     # tidbcloud_cluster.example_cluster 将原地更新
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             ~ components     = {
                 + tiflash = {
                     + node_quantity    = 1
                     + node_size        = "8C64G"
                     + storage_size_gib = 500
                   }
                   # (2 个未变更的属性隐藏)
               }
               # (3 个未变更的属性隐藏)
             }
             id             = "1379661944630234067"
             name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (已知在应用后)
             # (4 个未变更的属性隐藏)
         }

   计划：0 添加，1 修改，0 删除。

   你是否要执行这些操作？
     Terraform 将执行上述操作。
     只接受输入 'yes' 以确认。

     输入一个值：
   ```

   如上执行计划所示，TiFlash 将被添加，资源将被修改。

3. 如果计划无误，输入 `yes` 继续：

   ```bash
     Enter a value: yes

   tidbcloud_cluster.example_cluster: 正在修改... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: 2 秒后完成修改 [id=1379661944630234067]

   应用完成！资源：0 添加，1 修改，0 删除。
   ```

4. 使用 `terraform state show tidbcloud_cluster.${资源名}` 查看状态：

   ```bash
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
               # (1 个未变更的元素隐藏)
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

状态为 `MODIFYING` 表示集群正在变更中。等待一段时间，状态会变为 `AVAILABLE`。

### 扩展 TiDB 集群规模

你可以在集群状态为 `AVAILABLE` 时进行扩展。

1. 在你 [创建集群](#创建集群-使用集群资源) 时的 `cluster.tf` 文件中，编辑 `components` 配置。

   例如，为 TiDB 添加一个节点，为 TiKV 添加 3 个节点（TiKV 节点数必须是 3 的倍数，步长为 3，可从 [集群规格](#获取集群规格信息-使用-tidbcloud_cluster_specs-数据源) 获取信息），为 TiFlash 添加一个节点，可以如下配置：

   ```hcl
       components = {
         tidb = {
           node_size     = "8C16G"
           node_quantity = 2
         }
         tikv = {
           node_size        = "8C32G"
           storage_size_gib = 500
           node_quantity    = 6
         }
         tiflash = {
           node_size        = "8C64G"
           storage_size_gib = 500
           node_quantity    = 2
         }
       }
   ```

2. 运行 `terraform apply`，确认后输入 `yes`：

   ```bash
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform 使用选定的提供者生成以下执行计划。资源操作用符号表示：
     ~ in-place 更新

   Terraform 将执行以下操作：

     # tidbcloud_cluster.example_cluster 将原地更新
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             ~ components     = {
                 ~ tidb    = {
                     ~ node_quantity = 1 -> 2
                       # (未变更的属性隐藏)
                   }
                 ~ tiflash = {
                     ~ node_quantity = 1 -> 2
                       # (未变更的属性隐藏)
                   }
                 ~ tikv    = {
                     ~ node_quantity = 3 -> 6
                       # (未变更的属性隐藏)
                   }
               }
               # (未变更的属性隐藏)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (已知在应用后)
           # (未变更的属性隐藏)
       }

   计划：0 添加，1 修改，0 删除。

   你是否要执行这些操作？
     Terraform 将执行上述操作。
     只接受输入 'yes' 以确认。

     输入一个值：yes

   tidbcloud_cluster.example_cluster: 正在修改... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: 2 秒后完成修改 [id=1379661944630234067]

   应用完成！资源：0 添加，1 修改，0 删除。
   ```

等待状态由 `MODIFYING` 转变为 `AVAILABLE`。

### 暂停或恢复集群

你可以在集群状态为 `AVAILABLE` 时暂停，状态为 `PAUSED` 时恢复。

- 设置 `paused = true` 来暂停集群。
- 设置 `paused = false` 来恢复集群。

1. 在你 [创建集群](#创建集群-使用集群资源) 时的 `cluster.tf` 文件中，向 `config` 添加 `pause = true`：

   ```hcl
   config = {
       paused = true
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

2. 运行 `terraform apply`，确认后输入 `yes`：

   ```bash
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform 使用选定的提供者生成以下执行计划。资源操作用符号表示：
     ~ in-place 更新

   Terraform 将执行以下操作：

     # tidbcloud_cluster.example_cluster 将原地更新
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             + paused         = true
               # (4 个未变更的属性隐藏)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (已知在应用后)
           # (4 个未变更的属性隐藏)
       }

   计划：0 添加，1 修改，0 删除。

   你是否要执行这些操作？
     Terraform 将执行上述操作。
     只接受输入 'yes' 以确认。

     输入一个值：yes

   tidbcloud_cluster.example_cluster: 正在修改... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: 2 秒后完成修改 [id=1379661944630234067]

   应用完成！资源：0 添加，1 修改，0 删除。
   ```

3. 使用 `terraform state show tidbcloud_cluster.${资源名}` 查看状态：

   ```bash
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
               # (1 个未变更的元素隐藏)
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

4. 若要恢复集群，将 `paused = false`：

   ```hcl
   config = {
       paused = false
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

5. 运行 `terraform apply`，确认后输入 `yes`。使用 `terraform state show` 查看状态时，状态会变为 `RESUMING`：

   ```bash
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
               # (1 个未变更的元素隐藏)
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

等待一段时间后，使用 `terraform refresh` 更新状态，状态最终会变为 `AVAILABLE`。

至此，你已使用 Terraform 创建并管理了 TiDB Cloud 专用集群。接下来，可以尝试通过我们的 [备份资源](/tidb-cloud/terraform-use-backup-resource.md) 创建集群备份。

## 导入集群

对于未由 Terraform 管理的 TiDB 集群，你可以通过导入方式让 Terraform 管理它。

例如，可以导入未由 Terraform 创建的集群，或导入 [由恢复资源创建的集群](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task)。

1. 创建 `import_cluster.tf` 文件，内容如下：

   ```hcl
   terraform {
    required_providers {
      tidbcloud = {
        source = "tidbcloud/tidbcloud"
      }
    }
   }
   resource "tidbcloud_cluster" "import_cluster" {}
   ```

2. 使用 `terraform import tidbcloud_cluster.import_cluster projectId,clusterId` 导入集群：

   例如：

   ```bash
   $ terraform import tidbcloud_cluster.import_cluster 1372813089189561287,1379661944630264072

   tidbcloud_cluster.import_cluster: 正在从 ID "1372813089189561287,1379661944630264072" 导入...
   tidbcloud_cluster.import_cluster: 导入准备完毕！
     已准备好导入 tidbcloud_cluster
   tidbcloud_cluster.import_cluster: 正在刷新状态... [id=1379661944630264072]

   导入成功！

   上述导入的资源已显示在上方。这些资源现已在你的 Terraform 状态中，从此由 Terraform 管理。
   ```

3. 运行 `terraform state show tidbcloud_cluster.import_cluster` 查看集群状态：

   ```bash
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

4. 若要由 Terraform 管理此集群，可将导入的输出内容复制到配置文件中。注意删除 `id` 和 `status` 行，因为它们由 Terraform 控制：

   ```hcl
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

5. 使用 `terraform fmt` 格式化配置文件：

   ```bash
   $ terraform fmt
   ```

6. 运行 `terraform plan` 或 `terraform apply`，确保没有差异，说明导入成功。

   ```bash
   $ terraform apply

   tidbcloud_cluster.import_cluster: 正在刷新状态... [id=1379661944630264072]

   无变化。你的基础设施与配置匹配。

   Terraform 已比较你的实际基础设施与配置，未发现差异，无需更改。

   应用完成！资源：0 添加，0 更改，0 删除。
   ```

现在，你可以用 Terraform 管理该集群。

## 删除集群

要删除集群，进入对应的集群目录（即包含 `cluster.tf` 文件的目录），运行：

```bash
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

你确定要删除所有资源吗？
Terraform 将删除你管理的所有基础设施，如上所示。
此操作无法撤销。只接受输入 'yes' 以确认。

输入一个值：yes
```

运行后，资源会被销毁。如果你运行 `terraform show`，将显示为空，因为资源已被清除：

```bash
$ terraform show
```