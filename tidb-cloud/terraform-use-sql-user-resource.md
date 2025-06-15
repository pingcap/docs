---
title: Use SQL User Resource
summary: Learn how to use the SQL user resource to create and modify a TiDB Cloud SQL user.
---

# Use SQL User Resource

You can learn how to manage a TiDB Cloud SQL user with the `tidbcloud_sql_user` resource in this document.

The features of the `tidbcloud_sql_user` resource include the following:

- Create TiDB Cloud SQL Users.
- Modify TiDB Cloud SQL Users.
- Import TiDB Cloud SQL Users.
- Delete TiDB Cloud SQL Users.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) at least v0.4.0.
- Create a TiDB Cloud Dedicated or Serverless cluster. For more information, see [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/terraform-use-dedicated-cluster-resource.md) or [Create a TiDB Cloud Serverless Cluster](/tidb-cloud/terraform-use-serverless-cluster-resource.md).

## Create a SQL user using the SQL user resource

You can create a SQL user using the `tidbcloud_sql_user` resource.

The following example shows how to create a TiDB Cloud SQL user.

1. Create a directory for the SQL user and enter it.

2. Create a `sql_user.tf` file:
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

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the SQL user resource, set the resource type as `tidbcloud_sql_user`.
    - For the resource name, you can define it according to your need. For example, `example`.
    - For serverless cluster SQL users, the `user_name` and builtin role `role_readonly` and `role_readwrite` should start with user prefix, you can get the user prefix by running the `tidbcloud_serverless_cluster` data source.

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

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

   As in the above result, Terraform generates an execution plan for you, which describes the actions Terraform will take:

   - You can check the difference between the configurations and the states.
   - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
   - The `known after apply` shows that you will get the value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_sql_user.example: Creating...
    tidbcloud_sql_user.example: Creation complete after 2s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. Use the `terraform show` or `terraform state show tidbcloud_sql_user.${resource-name}` command to inspect the state of your resource. The former will show the states of all resources and data sources.

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

## Modify a TiDB Cloud SQL User

For a TiDB Cloud SQL user, you can use Terraform to manage SQL user resources as follows:

- Change the password or user roles of a SQL user.
- Delete a SQL user.

### Change the password or user roles of a SQL user

1. In the `sql_user.tf` file that is used when you [create the SQL user](#create-a-sql-user-using-the-sql-user-resource), change the `password`, 'builtin-role`, and `custom_roles`.

    For example:

    ```
    resource "tidbcloud_sql_user" "example" {
      cluster_id = 10423692645600000000
      user_name = "example_user"
      password = "updated_example_password"
      builtin_role = "role_readonly"
    }
    ```

2. Run the `terraform apply` command:

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

    As in the above execution plan, password and builtin role will be changed.

3. If everything in your plan looks fine, type `yes` to continue:

    ```shell
      Enter a value: yes

    tidbcloud_sql_user.example: Modifying...
    tidbcloud_sql_user.example: Modifications complete after 2s

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. Use `terraform state show tidbcloud_sql_user.${resource-name}` to see the state:

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

The `builtin_role` is changed to `role_readonly`, the `password` is not shown because it is a sensitive value.

## Import a SQL User

For a TiDB Cloud SQL user that is not managed by Terraform, you can use Terraform to manage it just by importing it.

For example, you can import a SQL user that is not created by Terraform.

1. Add an import block for the new dedicated SQL user resource

- Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,user_name`:

    ```
    import {
      to = tidbcloud_sql_user.example
      id = "10423692645683000000,example_user"
    }
    ```
2. Generate the new configuration file

Generate the new configuration file for the new SQL user resource according to the import block:

  ```shell
  terraform plan -generate-config-out=generated.tf
  ```

Do not specify an existing `.tf` file name in the preceding command. Otherwise, Terraform will return an error.

Then the `generated.tf` file is created in the current directory, which contains the configuration of the imported resource. But the provider will throw an error because the required argument `password` is not set. You can replace the value of `password` argument to the `tidbcloud_sql_user` resource in the generated configuration file.

3. Review and apply the generated configuration

Review the generated configuration file to ensure it meets your needs. Optionally, you can move the contents of this file to your preferred location.

Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

  ```shell
  tidbcloud_sql_user.example: Importing... [id=10423692645600000000,example_user]
  tidbcloud_sql_user.example: Import complete [id=10423692645600000000,example_user]

  Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
  ```

Now you can manage the imported SQL user with Terraform.

## Delete a SQL User

To delete a SQL user, you can delete the configuration of the `tidbcloud_sql_user` resource, then use the `terraform apply` command to destroy the resource:
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
Now, if you run the `terraform show` command, you will get nothing because the resource has been cleared:

```
$ terraform show
```