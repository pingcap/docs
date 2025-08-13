---
title: 使用 SQL 用户资源
summary: 了解如何使用 SQL 用户资源在 TiDB Cloud 中创建和修改 SQL 用户。
---

# 使用 SQL 用户资源

本文档介绍如何使用 `tidbcloud_sql_user` 资源管理 TiDB Cloud SQL 用户。

`tidbcloud_sql_user` 资源的功能包括：

- 创建 TiDB Cloud SQL 用户。
- 修改 TiDB Cloud SQL 用户。
- 导入 TiDB Cloud SQL 用户。
- 删除 TiDB Cloud SQL 用户。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 或更高版本。
- [创建 TiDB Cloud 专属集群](/tidb-cloud/create-tidb-cluster.md) 或 [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 创建 SQL 用户

你可以使用 `tidbcloud_sql_user` 资源来创建 SQL 用户。

以下示例展示了如何创建一个 TiDB Cloud SQL 用户。

1. 为 SQL 用户创建一个目录并进入该目录。

2. 创建一个 `sql_user.tf` 文件：

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

    resource "tidbcloud_sql_user" "example" {
      cluster_id   = "your_cluster_id"
      user_name    = "example_user"
      password     = "example_password"
      builtin_role = "role_admin"
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详情。

    - 要使用 SQL 用户资源，需要将资源类型设置为 `tidbcloud_sql_user`。
    - 资源名称可以根据需要自定义，例如 `example`。
    - 对于 TiDB Cloud Serverless 集群中的 SQL 用户，`user_name` 以及内置角色 `role_readonly` 和 `role_readwrite` 必须以用户前缀开头，你可以通过运行 `tidbcloud_serverless_cluster` 数据源获取用户前缀。
    - 获取 SQL 用户的详细配置信息，请参见 [`tidbcloud_sql_user` (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/sql_user)。

3. 运行 `terraform apply` 命令。应用资源时，不建议使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_sql_user.example will be created
      + resource "tidbcloud_sql_user" "example" {
          + auth_method  = (known after apply)
          + builtin_role = "role_admin"
          + cluster_id   = "10423692645600000000"
          + password     = (sensitive value)
          + user_name    = "example_user"
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

4. 如果你的计划内容无误，输入 `yes` 继续：

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_sql_user.example: Creating...
    tidbcloud_sql_user.example: Creation complete after 2s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_sql_user.${resource-name}` 命令检查资源的状态。前者会显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_sql_user.example                 
      # tidbcloud_sql_user.example:
      resource "tidbcloud_sql_user" "example" {
          builtin_role = "role_admin"
          cluster_id   = "10423692645600000000"
          password     = (sensitive value)
          user_name    = "example_user"
      }
    ```

## 修改 SQL 用户的密码或用户角色

你可以通过 Terraform 修改 SQL 用户的密码或用户角色，方法如下：

1. 在你 [创建 SQL 用户](#create-a-sql-user) 时使用的 `sql_user.tf` 文件中，修改 `password`、`builtin_role` 以及（如适用）`custom_roles`。

    例如：

    ```
    resource "tidbcloud_sql_user" "example" {
      cluster_id = 10423692645600000000
      user_name = "example_user"
      password = "updated_example_password"
      builtin_role = "role_readonly"
    }
    ```

2. 运行 `terraform apply` 命令：

    ```shell
    $ terraform apply

    tidbcloud_sql_user.example: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_sql_user.example will be updated in-place
      ~ resource "tidbcloud_sql_user" "example" {
          + auth_method  = (known after apply)
          ~ builtin_role = "role_admin" -> "role_readonly"
          ~ password     = (sensitive value)
            # (2 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    ```

    在上述执行计划中，密码和内置角色将会被更改。

3. 如果你的计划内容无误，输入 `yes` 继续：

    ```shell
      Enter a value: yes

    tidbcloud_sql_user.example: Modifying...
    tidbcloud_sql_user.example: Modifications complete after 2s

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_sql_user.${resource-name}` 检查状态：

    ```
    $ terraform state show tidbcloud_sql_user.example
    # tidbcloud_sql_user.example:
    resource "tidbcloud_sql_user" "example" {
        builtin_role = "role_readonly"
        cluster_id   = "10423692645600000000"
        password     = (sensitive value)
        user_name    = "example_user"
    }
    ```

`builtin_role` 已更改为 `role_readonly`。`password` 未显示，因为它是敏感值。

## 导入 SQL 用户

对于未被 Terraform 管理的 TiDB Cloud SQL 用户，你可以通过导入的方式让 Terraform 管理它。

例如，你可以按如下方式导入一个非 Terraform 创建的 SQL 用户：

1. 为新的 SQL 用户资源添加 import 块

    在你的 `.tf` 文件中添加如下 import 块，将 `example` 替换为你期望的资源名称，将 `${id}` 替换为 `cluster_id,user_name` 的格式：

    ```
    import {
      to = tidbcloud_sql_user.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件

    根据 import 块为新的 SQL 用户资源生成配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上述命令中不要指定已存在的 `.tf` 文件名，否则 Terraform 会返回错误。

    然后，当前目录下会生成 `generated.tf` 文件，包含了被导入资源的配置信息。但由于未设置必需参数 `password`，provider 会抛出错误。你可以在生成的配置文件中为 `tidbcloud_sql_user` 资源的 `password` 参数赋值。

3. 审查并应用生成的配置

    审查生成的配置文件，确保其符合你的需求。你也可以选择将该文件内容移动到你喜欢的位置。

    然后，运行 `terraform apply` 导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_sql_user.example: Importing... [id=10423692645600000000,example_user]
    tidbcloud_sql_user.example: Import complete [id=10423692645600000000,example_user]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理被导入的 SQL 用户。

## 删除 SQL 用户

要删除 SQL 用户，你可以删除 `tidbcloud_sql_user` 资源的配置，然后使用 `terraform apply` 命令销毁该资源：

```shell
  $ terraform apply
  tidbcloud_sql_user.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_sql_user.example will be destroyed
    # (because tidbcloud_sql_user.example is not in configuration)
    - resource "tidbcloud_sql_user" "example" {
        - builtin_role = "role_readonly" -> null
        - cluster_id   = "10423692645600000000" -> null
        - password     = (sensitive value) -> null
        - user_name    = "example_user" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_sql_user.example: Destroying...
  tidbcloud_sql_user.example: Destruction complete after 3s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

现在，如果你运行 `terraform show` 命令，将不会有任何输出，因为资源已被清除：

```
$ terraform show
```