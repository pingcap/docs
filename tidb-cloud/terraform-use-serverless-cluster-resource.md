---
title: 使用 `tidbcloud_serverless_cluster` 资源
summary: 了解如何使用 `tidbcloud_serverless_cluster` 资源来创建和修改 TiDB Cloud Starter 集群。
---

# 使用 `tidbcloud_serverless_cluster` 资源

本文档介绍了如何使用 `tidbcloud_serverless_cluster` 资源管理 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群。

你还将学习如何通过 `tidbcloud_projects` 数据源获取所需的信息。

`tidbcloud_serverless_cluster` 资源的功能包括：

- 创建 TiDB Cloud Starter 集群
- 修改 TiDB Cloud Starter 集群
- 导入 TiDB Cloud Starter 集群
- 删除 TiDB Cloud Starter 集群

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB 集群都属于一个项目。在创建 TiDB Cloud Starter 集群之前，你需要获取要创建集群的项目 ID。如果未指定 `project_id`，则会使用默认项目。

要检索所有可用项目的信息，可以按如下方式使用 `tidbcloud_projects` 数据源：

1. 在你 [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加如下的 `data` 和 `output` 块：

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
        - 数据源名称可以根据需要自定义，例如 `"example_project"`。
        - 对于 `tidbcloud_projects` 数据源，可以使用 `page` 和 `page_size` 属性来限制你想要查看的最大项目数量。

    - 使用 `output` 块定义要在输出中显示的数据源信息，并将这些信息暴露给其他 Terraform 配置使用。

        `output` 块的作用类似于编程语言中的返回值。更多细节可参考 [Terraform 官方文档](https://www.terraform.io/language/values/outputs)。

    若要获取所有资源和数据源的可用配置，请参阅 [Terraform provider 配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令以应用配置。你需要在确认提示时输入 `yes` 以继续。

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

现在，你可以从输出中获取所有可用的项目。复制你需要的项目 ID。

## 创建 TiDB Cloud Starter 集群

你可以使用 `tidbcloud_serverless_cluster` 资源来创建 TiDB Cloud Starter 集群。

1. 为集群创建一个目录并进入该目录。

2. 创建一个 `cluster.tf` 文件。

    以下是 `cluster.tf` 文件的示例：

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

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 若要使用 `tidbcloud_serverless_cluster` 资源，将资源类型设置为 `tidbcloud_serverless_cluster`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 资源详情可根据项目 ID 及 [`tidbcloud_serverless_cluster` 规范](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_cluster) 进行配置。

3. 运行 `terraform apply` 命令。应用资源时不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_serverless_cluster.example will be created
        + resource "tidbcloud_serverless_cluster" "example" {
            + annotations             = (known after apply)
            + automated_backup_policy = (known after apply)
            + cluster_id              = (known after apply)
            + create_time             = (known after apply)
            + created_by              = (known after apply)
            + display_name            = "test-tf"
            + encryption_config       = (known after apply)
            + endpoints               = (known after apply)
            + labels                  = (known after apply)
            + project_id              = "1372813089454000000"
            + region                  = {
                + cloud_provider = (known after apply)
                + display_name   = (known after apply)
                + name           = "regions/aws-us-east-1"
                + region_id      = (known after apply)
            }
            + spending_limit          = {
                + monthly = 1
            }
            + state                   = (known after apply)
            + update_time             = (known after apply)
            + user_prefix             = (known after apply)
            + version                 = (known after apply)
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
    - `known after apply` 表示你将在 `apply` 后获得对应的值。

4. 如果你的计划没有问题，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_cluster.example: Creating...
    tidbcloud_serverless_cluster.example: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_serverless_cluster.${resource-name}` 命令检查资源的状态。前者会显示所有资源和数据源的状态。

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

## 修改 TiDB Cloud Starter 集群

对于 TiDB Cloud Starter 集群，你可以使用 Terraform 管理资源。可修改的参数包括：

- `display_name`：集群的显示名称
- `spending_limit`：集群的消费上限
- `endpoints.public.disabled`：是否禁用公网连接
- `automated_backup_policy.start_time`：自动备份开始的 UTC 时间，格式为 `HH:mm`

要修改 TiDB Cloud Starter 集群，可以修改 `tidbcloud_serverless_cluster` 资源的配置，然后使用 `terraform apply` 命令应用更改。例如，你可以如下修改 `display_name` 和 `spending_limit`：

```
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

然后，运行 `terraform apply` 命令应用更改：

```shell
$ terraform apply

tidbcloud_serverless_cluster.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # tidbcloud_serverless_cluster.example will be updated in-place
  ~ resource "tidbcloud_serverless_cluster" "example" {
      ~ annotations             = {
          - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
          - "tidb.cloud/has-set-password"   = "false"
        } -> (known after apply)
      ~ display_name            = "test-tf" -> "test-tf-modified"
      ~ labels                  = {
          - "tidb.cloud/organization" = "1372813089187041280"
          - "tidb.cloud/project"      = "1372813089454543324"
        } -> (known after apply)
      ~ spending_limit          = {
          ~ monthly = 1 -> 2
        }
      ~ state                   = "ACTIVE" -> (known after apply)
      ~ update_time             = "2025-06-16T07:04:57Z" -> (known after apply)
      ~ version                 = "v7.5.2" -> (known after apply)
        # (9 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_cluster.example: Modifying...
tidbcloud_serverless_cluster.example: Modifications complete after 8s

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

然后，你可以使用 `terraform show` 或 `terraform state show tidbcloud_serverless_cluster.${resource-name}` 命令检查资源的状态。前者会显示所有资源和数据源的状态。

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

## 导入 TiDB Cloud Starter 集群

对于未被 Terraform 管理的 TiDB Cloud Starter 集群，你可以通过导入将其纳入 Terraform 管理。

1. 为新的 `tidbcloud_serverless_cluster` 资源添加 import 块。

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你想要的资源名称，将 `${id}` 替换为集群 ID：

    ```
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件。

    根据 import 块为新的 `tidbcloud_serverless_cluster` 资源生成新的配置文件：

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

3. 审查并应用生成的配置。

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_serverless_cluster.example: Importing... 
    tidbcloud_serverless_cluster.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理已导入的集群。

## 删除 TiDB Cloud Starter 集群

要删除 TiDB Cloud Starter 集群，可以删除 `tidbcloud_serverless_cluster` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

```shell
$ terraform apply
tidbcloud_serverless_cluster.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_cluster.example will be destroyed
  # (because tidbcloud_serverless_cluster.example is not in configuration)
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

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_cluster.example: Destroying...
tidbcloud_serverless_cluster.example: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会显示任何受管资源，因为该资源已被销毁：

```
$ terraform show
```