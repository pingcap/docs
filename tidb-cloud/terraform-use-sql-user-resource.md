---
title: 使用 SQL 用户资源
summary: 学习如何使用 SQL 用户资源创建和修改 TiDB Cloud SQL 用户。
---

# 使用 SQL 用户资源

本文档介绍如何使用 `tidbcloud_sql_user` 资源管理 TiDB Cloud SQL 用户。

`tidbcloud_sql_user` 资源的功能包括：

- 创建 TiDB Cloud SQL 用户
- 修改 TiDB Cloud SQL 用户
- 导入 TiDB Cloud SQL 用户
- 删除 TiDB Cloud SQL 用户

## 前提条件

- [获取 TiDB Cloud Terraform 提供者](/tidb-cloud/terraform-get-tidbcloud-provider.md) 版本 v0.4.0 或更高
- [创建 TiDB Cloud 专用集群](/tidb-cloud/create-tidb-cluster.md) 或 [TiDB Cloud 无服务器集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 创建 SQL 用户

你可以使用 `tidbcloud_sql_user` 资源创建 SQL 用户。

以下示例展示如何创建一个 TiDB Cloud SQL 用户。

1. 创建一个存放 SQL 用户的目录并进入。

2. 创建 `sql_user.tf` 文件：

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
    }

    resource "tidbcloud_sql_user" "example" {
      cluster_id   = "your_cluster_id"
      user_name    = "example_user"
      password     = "example_password"
      builtin_role = "role_admin"
    }
    ```

    使用 `resource` 块定义 TiDB Cloud 资源，包括资源类型、资源名称和资源详情。

    - 若要使用 SQL 用户资源，资源类型设为 `tidbcloud_sql_user`。
    - 资源名称可根据需要定义，例如 `example`。
    - 对于 TiDB Cloud 无服务器集群中的 SQL 用户，`user_name` 和内置角色 `role_readonly` 及 `role_readwrite` 必须以用户前缀开头，可以通过运行 `tidbcloud_serverless_cluster` 数据源获取用户前缀。
    - 获取 SQL 用户详细信息，请参见 [`tidbcloud_sql_user` (资源)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/sql_user)。

3. 运行 `terraform apply` 命令。建议不要在应用资源时使用 `terraform apply --auto-approve`。

    ```shell
    $ terraform apply

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
      + 创建

    Terraform 将执行以下操作：

      # tidbcloud_sql_user.example 将被创建
      + resource "tidbcloud_sql_user" "example" {
          + auth_method  = （应用后已知）
          + builtin_role = "role_admin"
          + cluster_id   = "10423692645600000000"
          + password     = （敏感值）
          + user_name    = "example_user"
        }

    计划：新增1个，修改0个，销毁0个。

    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：
    ```

    在上述输出中，Terraform 为你生成了执行计划，描述了 Terraform 将采取的操作：

    - 你可以检查配置与状态之间的差异。
    - 你还可以查看此次 `apply` 的结果。它会添加一个新资源，且没有资源被修改或销毁。
    - `known after apply` 表示在 `apply` 后你将获得对应的值。

4. 如果计划中的内容都没有问题，输入 `yes` 继续：

    ```shell
    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：yes

    tidbcloud_sql_user.example：创建中...
    tidbcloud_sql_user.example：2秒后创建完成

    应用完成！资源：新增1个，修改0个，销毁0个。
    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_sql_user.${资源名}` 命令检查资源状态。前者显示所有资源和数据源的状态。

    ```shell
    $ terraform state show tidbcloud_sql_user.example
      # tidbcloud_sql_user.example:
      resource "tidbcloud_sql_user" "example" {
          builtin_role = "role_admin"
          cluster_id   = "10423692645600000000"
          password     = （敏感值）
          user_name    = "example_user"
      }
    ```

## 更改 SQL 用户的密码或角色

你可以使用 Terraform 更改 SQL 用户的密码或角色，步骤如下：

1. 在用于 [创建 SQL 用户](#创建 SQL 用户) 的 `sql_user.tf` 文件中，修改 `password`、`builtin_role` 和 `custom_roles`（如适用）。

    例如：

    ```hcl
    resource "tidbcloud_sql_user" "example" {
      cluster_id   = 10423692645600000000
      user_name    = "example_user"
      password     = "updated_example_password"
      builtin_role = "role_readonly"
    }
    ```

2. 运行 `terraform apply` 命令：

    ```shell
    $ terraform apply

    tidbcloud_sql_user.example：刷新状态...

    Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
      ~ 仅更新

    Terraform 将执行以下操作：

      # tidbcloud_sql_user.example 将被就地更新
      ~ resource "tidbcloud_sql_user" "example" {
          + auth_method  = （应用后已知）
          ~ builtin_role = "role_admin" -> "role_readonly"
          ~ password     = （敏感值）
            # （隐藏了2个未变更的属性）
        }

    计划：新增0个，变更1个，销毁0个。

    是否执行这些操作？
      Terraform 将执行上述操作。
      只接受输入 'yes' 以确认。

      输入一个值：yes
    ```

    在上述执行计划中，密码和内置角色将被更改。

3. 如果计划内容都没有问题，输入 `yes` 继续：

    ```shell
      输入一个值：yes

    tidbcloud_sql_user.example：修改中...
    tidbcloud_sql_user.example：2秒后修改完成

    应用完成！资源：新增0个，变更1个，销毁0个。
    ```

4. 使用 `terraform state show tidbcloud_sql_user.${资源名}` 查看状态：

    ```
    $ terraform state show tidbcloud_sql_user.example
    # tidbcloud_sql_user.example:
    resource "tidbcloud_sql_user" "example" {
        builtin_role = "role_readonly"
        cluster_id   = "10423692645600000000"
        password     = （敏感值）
        user_name    = "example_user"
    }
    ```

内置角色已更改为 `role_readonly`。密码未显示，因为它是敏感值。

## 导入 SQL 用户

对于未由 Terraform 管理的 TiDB Cloud SQL 用户，可以通过导入方式让 Terraform 管理它。

例如，可以按如下方式导入未由 Terraform 创建的 SQL 用户：

1. 添加导入块到你的 `.tf` 文件中，替换 `example` 为你想要的资源名，`$ {id}` 替换为 `cluster_id,user_name` 格式：

    ```hcl
    import {
      to = tidbcloud_sql_user.example
      id = "${id}"
    }
    ```

2. 生成新的配置文件

    根据导入块，生成新 SQL 用户资源的配置文件：

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

    这样会在当前目录生成 `generated.tf` 文件，包含导入资源的配置。但由于未设置必需参数 `password`，提供者会报错。你可以在生成的配置文件中为 `tidbcloud_sql_user` 资源的 `password` 参数赋值。

3. 审查并应用生成的配置

    审查生成的配置文件，确保符合你的需求。也可以将其内容移动到你偏好的位置。

    然后运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

    ```shell
    tidbcloud_sql_user.example：导入中... [id=10423692645600000000,example_user]
    tidbcloud_sql_user.example：导入完成 [id=10423692645600000000,example_user]

    应用完成！资源：导入1个，新增0个，变更0个，销毁0个。
    ```

现在你可以用 Terraform 管理导入的 SQL 用户。

## 删除 SQL 用户

要删除 SQL 用户，可以删除 `tidbcloud_sql_user` 资源的配置，然后运行 `terraform apply` 来销毁资源：

```shell
  $ terraform apply
  tidbcloud_sql_user.example：刷新状态...

  Terraform 使用所选提供者生成以下执行计划。资源操作用以下符号表示：
    - 销毁

  Terraform 将执行以下操作：

    # tidbcloud_sql_user.example 将被销毁
    # （因为配置中没有 tidbcloud_sql_user.example）
    - resource "tidbcloud_sql_user" "example" {
        - builtin_role = "role_readonly" -> null
        - cluster_id   = "10423692645600000000" -> null
        - password     = （敏感值） -> null
        - user_name    = "example_user" -> null
      }

  计划：新增0个，变更0个，销毁1个。

  是否执行这些操作？
    Terraform 将执行上述操作。
    只接受输入 'yes' 以确认。

    输入一个值：yes

  tidbcloud_sql_user.example：销毁中...
  tidbcloud_sql_user.example：3秒后销毁完成

  应用完成！资源：新增0个，变更0个，销毁1个。
```

现在，如果你运行 `terraform show` 命令，将不会显示任何内容，因为资源已被清除：

```
$ terraform show
```