---
title: 使用 TiDB Cloud Serverless 集群资源
summary: 了解如何使用 TiDB Cloud Serverless 集群资源创建和修改 TiDB Cloud Serverless 集群。
---

# 使用 TiDB Cloud Serverless 集群资源

本文档介绍如何使用 `tidbcloud_serverless_cluster` 资源管理 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

此外，你还将学习如何通过 `tidbcloud_projects` 数据源获取必要的信息。

`tidbcloud_serverless_cluster` 资源的功能包括：

- 创建 TiDB Cloud Serverless 集群
- 修改 TiDB Cloud Serverless 集群
- 导入 TiDB Cloud Serverless 集群
- 删除 TiDB Cloud Serverless 集群

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB 集群都属于一个项目。在创建 TiDB Cloud Serverless 集群之前，你需要获取你想要创建集群的项目 ID。如果没有指定 `project_id`，则会使用默认项目。

要检索所有可用项目的信息，使用如下的 `tidbcloud_projects` 数据源：

1. 在你 [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加 `data` 和 `output` 块如下：

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

    data "tidbcloud_projects" "example_project" {
      page      = 1
      page_size = 10
    }

    output "projects" {
      value = data.tidbcloud_projects.example_project.items
    }
    ```

    - 使用 `data` 块定义 TiDB Cloud 的数据源，包括数据源类型和数据源名称。

        - 若要使用项目数据源，设置数据源类型为 `tidbcloud_projects`。
        - 数据源名称可以根据需要定义，例如 `"example_project"`。
        - `tidbcloud_projects` 数据源支持 `page` 和 `page_size` 属性，用于限制最多检索的项目数量。

    - 使用 `output` 块定义要在输出中显示的数据源信息，并将信息暴露给其他 Terraform 配置使用。

        `output` 块的作用类似于编程语言中的返回值。详情请参见 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

    若要获取所有资源和数据源的配置项，请参阅 [Terraform provider 配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令应用配置。你需要在确认提示中输入 `yes` 以继续。

    若要跳过提示，可以使用 `terraform apply --auto-approve`：

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

    你可以应用此计划，将这些新的输出值保存到 Terraform 状态中，而不会更改任何实际基础设施。

    计划已完成！资源：0 添加，0 更改，0 删除。

    输出：

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

现在，你可以从输出中获取所有可用的项目。复制你需要的某个项目 ID。

## 创建 TiDB Cloud Serverless 集群

你可以使用 `tidbcloud_serverless_cluster` 资源创建 TiDB Cloud Serverless 集群。

以下示例演示如何创建一个 TiDB Cloud Serverless 集群。

1. 创建一个目录用于集群，并进入该目录。

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
      public_key = "your_public_key"
      private_key = "your_private_key"
    }

    resource "tidbcloud_serverless_cluster" "example" {
      project_id = "1372813089454000000"
      display_name = "test-tf"
      spending_limit = {
        monthly = 1
      }
      region = {
        name = "regions/aws-us-east-1"
      }
    }
    ```

    - 使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

        - 若要使用 TiDB Cloud Serverless 集群资源，设置资源类型为 `tidbcloud_serverless_cluster`。
        - 资源名称可以根据需要定义，例如 `example`。
        - 资源详情可根据项目 ID 和 TiDB Cloud Serverless 集群规格信息进行配置。
        - 获取 TiDB Cloud Serverless 集群规格信息，请参见 [tidbcloud_serverless_cluster (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_cluster)。

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选的提供者生成以下执行计划。资源操作用以下符号表示：
      + 创建

    Terraform 将执行以下操作：

        # tidbcloud_serverless_cluster.example 将被创建
        + resource "tidbcloud_serverless_cluster" "example" {
            + annotations             = (应用后已知)
            + automated_backup_policy = (应用后已知)
            + cluster_id              = (应用后已知)
            + create_time             = (应用后已知)
            + created_by              = (应用后已知)
            + display_name            = "test-tf"
            + encryption_config       = (应用后已知)
            + endpoints               = (应用后已知)
            + labels                  = (应用后已知)
            + project_id              = "1372813089454000000"
            + region                  = {
                + cloud_provider = (应用后已知)
                + display_name   = (应用后已知)
                + name           = "regions/aws-us-east-1"
                + region_id      = (应用后已知)
            }
            + spending_limit          = {
                + monthly = 1
            }
            + state                   = (应用后已知)
            + update_time             = (应用后已知)
            + user_prefix             = (应用后已知)
            + version                 = (应用后已知)
        }

    计划：添加 1 个，修改 0 个，删除 0 个。

    你是否要执行这些操作？
        Terraform 将执行上述操作。
        只接受输入 `yes` 以确认。

        输入一个值：
    ```

    在上述结果中，Terraform 为你生成了一个执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你还可以查看此次 `apply` 的结果。它会添加一个新资源，不会更改或删除任何资源。
    - `应用后已知` 表示你将在 `apply` 后获得相应的值。

4. 如果一切看起来都正常，输入 `yes` 继续：

    ```shell
    是否要执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 `yes` 以确认。

      输入一个值：yes

    tidbcloud_serverless_cluster.example：创建中...
    tidbcloud_serverless_cluster.example：仍在创建中...[已过 10 秒]

    计划已完成！资源：1 添加，0 更改，0 删除。
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_cluster.${resource-name}` 命令检查资源状态。前者显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_serverless_cluster.example

    # tidbcloud_serverless_cluster.example:
    resource "tidbcloud_serverless_cluster" "example" {
        annotations             = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        automated_backup_policy = {
            retention_days = 14
            start_time     = "07:00"
        }
        cluster_id              = "10145794214536000000"
        create_time             = "2025-06-16T07:04:41Z"
        created_by              = "apikey-S2000000"
        display_name            = "test-tf"
        encryption_config       = {
            enhanced_encryption_enabled = false
        }
        endpoints               = {
            private = {
                aws  = {
                    availability_zone = [
                        "use1-az6",
                    ]
                    service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
                }
                host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
                port = 4000
            }
            public  = {
                disabled = false
                host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
                port     = 4000
            }
        }
        labels                  = {
            "tidb.cloud/organization" = "1372813089187000000"
            "tidb.cloud/project"      = "1372813089454000000"
        }
        project_id              = "1372813089454000000"
        region                  = {
            cloud_provider = "aws"
            display_name   = "N. Virginia (us-east-1)"
            name           = "regions/aws-us-east-1"
            region_id      = "us-east-1"
        }
        spending_limit          = {
            monthly = 1
        }
        state                   = "ACTIVE"
        update_time             = "2025-06-16T07:04:48Z"
        user_prefix             = "KhSDGqQ3P000000"
        version                 = "v7.5.2"
    }
    ```

## 修改 TiDB Cloud Serverless 集群

对于 TiDB Cloud Serverless 集群，你可以用 Terraform 管理资源。可以修改的参数包括：

- `display_name`：集群的显示名称
- `spending_limit`：集群的消费限制
- `endpoints.public.disabled`：是否禁用公共端点
- `automated_backup_policy.start_time`：自动备份开始的 UTC 时间（`HH:mm` 格式）

要修改 TiDB Cloud Serverless 集群，可以修改 `tidbcloud_serverless_cluster` 资源的配置，然后运行 `terraform apply` 来应用更改。例如，可以如下修改 `display_name` 和 `spending_limit`：

```hcl
resource "tidbcloud_serverless_cluster" "example" {
  project_id = "1372813089454000000"
  display_name = "test-tf-modified"
  spending_limit = {
    monthly = 2
  }
  region = {
    name = "regions/aws-us-east-1"
  }
}
```

然后，运行 `terraform apply` 来应用更改：

```shell
$ terraform apply

tidbcloud_serverless_cluster.example：刷新状态...

Terraform 使用所选的提供者生成以下执行计划。资源操作用以下符号表示：
  ~ 更新（就地）

Terraform 将执行以下操作：

  # tidbcloud_serverless_cluster.example 将被就地更新
  ~ resource "tidbcloud_serverless_cluster" "example" {
      ~ annotations             = {
          - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
          - "tidb.cloud/has-set-password"   = "false"
        } -> (应用后已知)
      ~ display_name            = "test-tf" -> "test-tf-modified"
      ~ labels                  = {
          - "tidb.cloud/organization" = "1372813089187041280"
          - "tidb.cloud/project"      = "1372813089454543324"
        } -> (应用后已知)
      ~ spending_limit          = {
          ~ monthly = 1 -> 2
        }
      ~ state                   = "ACTIVE" -> (应用后已知)
      ~ update_time             = "2025-06-16T07:04:57Z" -> (应用后已知)
      ~ version                 = "v7.5.2" -> (应用后已知)
        # 其他未变更的属性隐藏
    }

计划：添加 0 个，更改 1 个，删除 0 个。

你是否要执行这些操作？
  Terraform 将执行上述操作。
  只接受输入 `yes` 以确认。

  输入一个值：yes

tidbcloud_serverless_cluster.example：修改中...
tidbcloud_serverless_cluster.example：修改完成，耗时 8 秒

计划已完成！资源：0 添加，1 更改，0 删除。
```

然后，你可以用 `terraform show` 或 `terraform state show tidbcloud_serverless_cluster.${resource-name}` 命令检查资源状态。前者显示所有资源和数据源的状态。

```shell
$ terraform state show tidbcloud_serverless_cluster.example
# tidbcloud_serverless_cluster.example:
resource "tidbcloud_serverless_cluster" "example" {
    annotations             = {
        "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
        "tidb.cloud/has-set-password"   = "false"
    }
    automated_backup_policy = {
        retention_days = 14
        start_time     = "07:00"
    }
    cluster_id              = "10145794214536000000"
    create_time             = "2025-06-16T07:04:41Z"
    created_by              = "apikey-S2000000"
    display_name            = "test-tf-modified"
    encryption_config       = {
        enhanced_encryption_enabled = false
    }
    endpoints               = {
        private = {
            aws  = {
                availability_zone = [
                    "use1-az6",
                ]
                service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
            }
            host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
            port = 4000
        }
        public  = {
            disabled = false
            host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
            port     = 4000
        }
    }
    labels                  = {
        "tidb.cloud/organization" = "1372813089187000000"
        "tidb.cloud/project"      = "1372813089454000000"
    }
    project_id              = "1372813089454000000"
    region                  = {
        cloud_provider = "aws"
        display_name   = "N. Virginia (us-east-1)"
        name           = "regions/aws-us-east-1"
        region_id      = "us-east-1"
    }
    spending_limit          = {
        monthly = 2
    }
    state                   = "ACTIVE"
    update_time             = "2025-06-16T07:04:57Z"
    user_prefix             = "KhSDGqQ3P000000"
    version                 = "v7.5.2"
}
```

## 导入一个 TiDB Cloud Serverless 集群

对于未由 Terraform 管理的 TiDB Cloud Serverless 集群，你可以通过导入的方式让 Terraform 管理它。

导入未由 Terraform 创建的 TiDB Cloud Serverless 集群的方法如下：

1. 在你的 `.tf` 文件中添加导入块。

    在 `.tf` 文件中添加如下导入块，替换 `example` 为你希望的资源名，`${id}` 替换为集群 ID：

    ```hcl
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据导入块，生成新的 TiDB Cloud Serverless 集群资源配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保符合你的需求。你也可以将此文件的内容移动到你偏好的位置。

    然后，运行 `terraform apply` 以导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_cluster.example：导入中...
    tidbcloud_serverless_cluster.example：导入完成

    计划已完成！资源：1 导入，0 添加，0 更改，0 删除。
    ```

现在，你可以用 Terraform 管理导入的集群。

## 删除一个 TiDB Cloud Serverless 集群

要删除 TiDB Cloud Serverless 集群，你可以删除 `tidbcloud_serverless_cluster` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
$ terraform apply
tidbcloud_serverless_cluster.example：刷新状态...

Terraform 使用所选的提供者生成以下执行计划。资源操作用以下符号表示：
  - 删除

Terraform 将执行以下操作：

  # tidbcloud_serverless_cluster.example 将被销毁
  # （因为 `tidbcloud_serverless_cluster.example` 不在配置中）
  - resource "tidbcloud_serverless_cluster" "example" {
      - annotations             = {
          - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
          - "tidb.cloud/has-set-password"   = "false"
        } -> null
      - automated_backup_policy = {
          - retention_days = 14 -> null
          - start_time     = "07:00" -> null
        } -> null
      - cluster_id              = "10145794214536000000" -> null
      - create_time             = "2025-06-16T07:04:41Z" -> null
      - created_by              = "apikey-S2000000" -> null
      - display_name            = "test-tf-modified" -> null
      - encryption_config       = {
          - enhanced_encryption_enabled = false -> null
        } -> null
      - endpoints               = {
          - private = {
              - aws  = {
                  - availability_zone = [
                      - "use1-az6",
                    ] -> null
                  - service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000" -> null
                } -> null
              - host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com" -> null
              - port = 4000 -> null
            } -> null
          - public  = {
              - disabled = false -> null
              - host     = "gateway01.us-east-1.prod.aws.tidbcloud.com" -> null
              - port     = 4000 -> null
            } -> null
        } -> null
      - labels                  = {
          - "tidb.cloud/organization" = "1372813089187000000"
          - "tidb.cloud/project"      = "1372813089454000000"
        } -> null
      - project_id              = "1372813089454000000" -> null
      - region                  = {
          - cloud_provider = "aws" -> null
          - display_name   = "N. Virginia (us-east-1)" -> null
          - name           = "regions/aws-us-east-1" -> null
          - region_id      = "us-east-1" -> null
        } -> null
      - spending_limit          = {
          - monthly = 2 -> null
        } -> null
      - state                   = "ACTIVE" -> null
      - update_time             = "2025-06-16T07:04:57Z" -> null
      - user_prefix             = "KhSDGqQ3P000000" -> null
      - version                 = "v7.5.2" -> null
    }

计划：0 添加，0 更改，1 删除。

你是否要执行这些操作？
  Terraform 将执行上述操作。
  只接受输入 `yes` 以确认。

  输入一个值：yes

tidbcloud_serverless_cluster.example：销毁中...
tidbcloud_serverless_cluster.example：已在 1 秒后完成销毁

计划已完成！资源：0 添加，0 更改，1 删除。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何托管的资源，因为资源已被清除：

```
$ terraform show
```