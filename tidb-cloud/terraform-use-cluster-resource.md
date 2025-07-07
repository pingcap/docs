---
title: 使用集群资源（已废弃）
summary: 学习如何使用集群资源创建和修改 TiDB Cloud 集群。
---

# 使用集群资源（已废弃）

> **Warning:**
>
> 从 [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) v0.4.0 起，`tidbcloud_cluster` 资源已被废弃。建议使用 `tidbcloud_dedicated_cluster` 或 `tidbcloud_serverless_cluster` 资源。更多信息请参见 [使用 TiDB Cloud 专用集群资源](/tidb-cloud/terraform-use-dedicated-cluster-resource.md) 或 [使用 TiDB Cloud 无服务器集群资源](/tidb-cloud/terraform-use-serverless-cluster-resource.md)。

本文档介绍如何使用 `tidbcloud_cluster` 资源管理 TiDB Cloud 集群。

此外，你还将学习如何通过 `tidbcloud_projects` 和 `tidbcloud_cluster_specs` 数据源获取必要的信息。

`tidbcloud_cluster` 资源的功能包括：

- 创建 TiDB Cloud 无服务器和专用集群。
- 修改 TiDB Cloud 专用集群。
- 删除 TiDB Cloud 无服务器和专用集群。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。

## 使用 `tidbcloud_projects` 数据源获取项目ID

每个 TiDB 集群都属于一个项目。在创建集群之前，你需要获取你想要创建集群的项目ID。

要查看所有可用项目的信息，可以使用 `tidbcloud_projects` 数据源，示例如下：

1. 在你 [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加 `data` 和 `output` 块：

   ```
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

   - 使用 `data` 块定义 TiDB Cloud 数据源，包括数据源类型和名称。

      - 若要使用项目数据源，设置 `data` 类型为 `tidbcloud_projects`。
      - 数据源名称可根据需要定义，例如 "example_project"。
      - `tidbcloud_projects` 数据源中，可以使用 `page` 和 `page_size` 属性限制最多查询的项目数量。

   - 使用 `output` 块定义要在输出中显示的数据源信息，供其他 Terraform 配置引用。

      `output` 块的作用类似于编程语言中的返回值。详情请参见 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

   若要获取所有资源和数据源的配置项，请参阅此 [配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令应用配置。确认提示时输入 `yes`。

   若要跳过提示，可以使用 `terraform apply --auto-approve`：

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

   你可以应用此计划，将这些新输出值保存到 Terraform 状态中，而不改变任何实际基础设施。

   计划已完成！资源：0 添加，0 更改，0 删除。

   输出：

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

现在，你可以从输出中获取所有可用的项目。复制你需要的某个项目ID。

## 使用 `tidbcloud_cluster_specs` 数据源获取集群规格信息

在创建集群之前，你需要获取集群规格信息，其中包含所有可用的配置值（如支持的云提供商、区域和节点大小）。

要获取集群规格信息，可以使用 `tidbcloud_cluster_specs` 数据源，示例如下：

1. 编辑 `main.tf` 文件，内容如下：

    ```
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

- `cloud_provider` 表示 TiDB 集群可以托管的云提供商。
- `region` 是 `cloud_provider` 的区域。
- `node_quantity_range` 显示最小节点数和扩展节点的步长。
- `node_size` 是节点的大小。
- `storage_size_gib_range` 显示可以为节点设置的最小和最大存储容量。

## 使用集群资源创建集群

> **Note:**
>
> 在开始之前，确保你已在 TiDB Cloud 控制台设置了 CIDR。更多信息请参见 [设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

你可以使用 `tidbcloud_cluster` 资源创建集群。

以下示例演示如何创建一个 TiDB Cloud 专用集群。

1. 创建一个目录用于存放集群配置，并进入该目录。

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

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和详细配置。

    - 设置资源类型为 `tidbcloud_cluster`。
    - 资源名称可根据需要定义，例如 `example_cluster`。
    - 配置内容根据项目ID和集群规格信息进行调整。

3. 运行 `terraform apply` 命令。建议不要使用 `terraform apply --auto-approve` 直接应用资源。

    ```shell
    $ terraform apply

    Terraform 将执行以下操作：

      # tidbcloud_cluster.example_cluster 将被创建
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

    计划：添加1个，修改0个，删除0个。

    你想执行这些操作吗？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：
    ```

   如上所示，Terraform 会生成一份执行计划，描述将要执行的操作：

   - 你可以检查配置与状态之间的差异。
   - 你也可以查看此次 `apply` 的结果。它会添加一个新资源，资源不会被更改或删除。
   - `known after apply` 表示在 `apply` 后会获得的值。

4. 如果一切看起来都正常，输入 `yes` 继续：

    ```
    你想执行这些操作吗？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：yes

    tidbcloud_cluster.example_cluster: 创建中...
    tidbcloud_cluster.example_cluster: 1秒后创建完成 [id=1379661944630234067]

    申请完成！资源：添加1个，变更0个，删除0个。
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_cluster.${资源名}` 查看资源状态。前者显示所有资源和数据源的状态。

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
                # (1个未变更元素隐藏)
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

   集群状态为 `CREATING`，此时需要等待其变为 `AVAILABLE`，通常至少需要10分钟。

6. 若要查看最新状态，运行 `terraform refresh` 更新状态，然后再次运行 `terraform state show tidbcloud_cluster.${资源名}` 查看。

    ```
    $ terraform refresh

    tidbcloud_cluster.example_cluster: 正在刷新状态... [id=1379661944630234067]

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
                # (1个未变更元素隐藏)
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

当状态变为 `AVAILABLE` 时，表示你的集群已创建完成并可以使用。

## 修改 TiDB Cloud 专用集群

对于 TiDB Cloud 专用集群，你可以通过 Terraform 管理集群资源，包括：

- 添加 TiFlash 组件
- 扩展集群规模
- 暂停或恢复集群

### 添加 TiFlash 组件

1. 在你 [创建集群](#创建集群-使用集群资源) 时的 `cluster.tf` 文件中，向 `components` 字段添加 `tiflash` 配置。

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

    tidbcloud_cluster.example_cluster: 正在刷新状态... [id=1379661944630234067]

    Terraform 使用选定的提供者生成以下执行计划。资源操作由以下符号指示：
      ~ 位置更新

    Terraform 将执行以下操作：

      # tidbcloud_cluster.example_cluster 将被原地更新
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              ~ components     = {
                  + tiflash = {
                      + node_quantity    = 1
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                    # (其他未变更属性隐藏)
                }
                # (其他未变更属性隐藏)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (已知后应用)
            # (其他未变更属性隐藏)
        }

    计划：不添加，变更1，删除0。

    你想执行这些操作吗？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：
    ```

    如上执行计划所示，TiFlash 将被添加，且有一项资源会被更改。

3. 如果一切正常，输入 `yes` 继续：

    ```
      输入一个值：yes

    tidbcloud_cluster.example_cluster: 正在修改... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: 2秒后修改完成 [id=1379661944630234067]

    申请完成！资源：不添加，变更1，删除0。
    ```

4. 使用 `terraform state show tidbcloud_cluster.${资源名}` 查看状态：

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
                # (1个未变更元素隐藏)
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

状态为 `MODIFYING` 表示正在变更中，等待一会儿，状态会变为 `AVAILABLE`。

### 暂停或恢复集群

你可以在集群状态为 `AVAILABLE` 时暂停集群，或在状态为 `PAUSED` 时恢复集群。

- 设置 `paused = true` 来暂停集群。
- 设置 `paused = false` 来恢复集群。

1. 在你 [创建集群](#创建集群-使用集群资源) 时的 `cluster.tf` 文件中，向 `config` 添加 `pause = true`：

   ```
   config = {
       paused = true
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

2. 运行 `terraform apply`，确认后输入 `yes`：

   ```
   $ terraform apply

   tidbcloud_cluster.example_cluster: 正在刷新状态... [id=1379661944630234067]

   Terraform 使用选定的提供者生成以下执行计划。资源操作由以下符号指示：
     ~ 位置更新

   Terraform 将执行以下操作：

     # tidbcloud_cluster.example_cluster 将被原地更新
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             + paused         = true
               # (其他未变更属性隐藏)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (已知后应用)
           # (其他未变更属性隐藏)
       }

   计划：不添加，变更1，删除0。

   你想执行这些操作吗？
     Terraform 将执行上述操作。
     只接受输入 'yes' 以确认。

     输入一个值：yes

   tidbcloud_cluster.example_cluster: 正在修改... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: 2秒后修改完成 [id=1379661944630234067]

   申请完成！资源：不添加，变更1，删除0。
   ```

3. 使用 `terraform state show tidbcloud_cluster.${资源名}` 查看状态：

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
               # (1个未变更元素隐藏)
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

   ```
   config = {
       paused = false
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

5. 运行 `terraform apply`，确认后输入 `yes`。使用 `terraform state show` 查看状态时，状态会变为 `RESUMING`：

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
               # (1个未变更元素隐藏)
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

6. 等待一会儿，运行 `terraform refresh` 更新状态，状态最终会变为 `AVAILABLE`。

至此，你已成功使用 Terraform 创建和管理 TiDB Cloud 专用集群。接下来，你可以尝试通过我们的 [备份资源](/tidb-cloud/terraform-use-backup-resource.md) 创建集群备份。

## 导入集群

对于未由 Terraform 管理的 TiDB 集群，你可以通过导入方式让 Terraform 管理它。

例如，可以导入未由 Terraform 创建的集群，或导入由 [恢复资源](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task) 创建的集群。

1. 创建 `import_cluster.tf` 文件，内容如下：

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

2. 使用 `terraform import tidbcloud_cluster.import_cluster projectId,clusterId` 导入集群：

   例如：

    ```
    $ terraform import tidbcloud_cluster.import_cluster 1372813089189561287,1379661944630264072

    tidbcloud_cluster.import_cluster: 正在从 ID "1372813089189561287,1379661944630264072" 导入...
    tidbcloud_cluster.import_cluster: 导入准备完毕！
      准备好导入 tidbcloud_cluster
    tidbcloud_cluster.import_cluster: 正在刷新状态... [id=1379661944630264072]

    导入成功！

    上述显示的资源已导入。它们现在在你的 Terraform 状态中，从此由 Terraform 管理。
    ```

3. 运行 `terraform state show tidbcloud_cluster.import_cluster` 查看集群状态：

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

4. 若要由 Terraform 管理该集群，可将导入后输出的配置复制到配置文件中。注意删除 `id` 和 `status` 行，因为它们由 Terraform 控制：

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

5. 使用 `terraform fmt` 格式化配置文件：

    ```
    $ terraform fmt
    ```

6. 运行 `terraform plan` 或 `terraform apply`，确保没有差异，说明导入成功。

    ```
    $ terraform apply

    tidbcloud_cluster.import_cluster: 正在刷新状态... [id=1379661944630264072]

    没有变化。你的基础设施与配置匹配。

    Terraform 比较了你的实际基础设施与配置，没有发现差异，因此无需更改。

    申请完成！资源：0 添加，0 更改，0 删除。
    ```

现在，你可以用 Terraform 管理该集群。

## 删除集群

要删除集群，进入对应的集群目录（包含 `cluster.tf` 文件的目录），运行：

```
$ terraform destroy

计划：不添加，变更0，删除1。

你真的要删除所有资源吗？
Terraform 将删除你管理的所有基础设施，如上所示。
此操作无法撤销。只接受输入 'yes' 以确认。

输入一个值：yes
```

运行后，资源会被删除。如果你运行 `terraform show`，将显示为空，因为资源已被清除：

```
$ terraform show
```