---
title: Use TiDB Cloud Serverless Cluster Resource
summary: Learn how to use the TiDB Cloud Serverless cluster resource to create and modify a TiDB Cloud Serverless cluster.
---

# Use TiDB Cloud Serverless Cluster Resource

This document describes how to manage a [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) cluster with the `tidbcloud_serverless_cluster` resource.

In addition, you will also learn how to get the necessary information with the `tidbcloud_projects` data source.

The features of the `tidbcloud_serverless_cluster` resource include the following:

- Create TiDB Cloud Serverless clusters.
- Modify TiDB Cloud Serverless clusters.
- Import TiDB Cloud Serverless clusters.
- Delete TiDB Cloud Serverless clusters.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.

## Get project IDs using the `tidbcloud_projects` data source

Each TiDB cluster belongs to a project. Before creating a TiDB Cloud Serverless cluster, you need to obtain the ID of the project where you want to create the cluster. If no `project_id` is specified, the default project will be used.

To retrieve the information about all available projects, use the `tidbcloud_projects` data source as follows:

1. In the `main.tf` file created when you [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md), add the `data` and `output` blocks as follows:

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

    - Use the `data` block to define the data source of TiDB Cloud, including the data source type and the data source name.

        - To use the projects data source, set the data source type as `tidbcloud_projects`.
        - For the data source name, you can define it as needed. For example, `"example_project"`.
        - For the `tidbcloud_projects` data source, you can use the `page` and `page_size` attributes to limit the maximum number of projects you want to check.

    - Use the `output` block to define the data source information to be displayed in the output, and expose the information for other Terraform configurations to use.

        The `output` block works similarly to returned values in programming languages. See [Terraform documentation](https://www.terraform.io/language/values/outputs) for more details.

    To get all the available configurations for the resources and data sources, see the [Terraform provider configuration documentation](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

2. Run the `terraform apply` command to apply the configurations. You need to type `yes` at the confirmation prompt to proceed.

    To skip the prompt, use `terraform apply --auto-approve`:

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

Now, you can get all the available projects from the output. Copy one of the project IDs that you need.

## Create a TiDB Cloud Serverless cluster

You can create a TiDB Cloud Serverless cluster using the `tidbcloud_serverless_cluster` resource.

The following example shows how to create a TiDB Cloud Serverless cluster.

1. Create a directory for the cluster and enter it.

2. Create a `cluster.tf` file:

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

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the TiDB Cloud Serverless cluster resource, set the resource type as `tidbcloud_serverless_cluster`.
    - For the resource name, you can define it as needed. For example, `example`.
    - For the resource details, you can configure them according to the Project ID and the TiDB Cloud Serverless cluster specification information.
    - To get the TiDB Cloud Serverless cluster specification information, see [tidbcloud_serverless_cluster (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_cluster).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

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

    In the preceding result, Terraform generates an execution plan for you, which describes the actions that Terraform will take:

    - You can check the differences between the configurations and the states.
    - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
    - `known after apply` indicates that you will get the corresponding value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_cluster.example: Creating...
    tidbcloud_serverless_cluster.example: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. Use the `terraform show` or `terraform state show tidbcloud_serverless_cluster.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

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

## Modify a TiDB Cloud Serverless cluster

For a TiDB Cloud Serverless cluster, you can use Terraform to manage resources. The arguments that you can modify include:

- `display_name`: The display name of the cluster.
- `spending_limit`: The spending limit of the cluster.
- `endpoints.public.disabled`: Whether to disable the public endpoint.
- `automated_backup_policy.start_time`: The UTC time of day in `HH:mm` format when the automated backup starts.

To modify a TiDB Cloud Serverless cluster, you can modify the configuration of the `tidbcloud_serverless_cluster` resource, then use the `terraform apply` command to apply the changes. For example, you can modify the `display_name` and `spending_limit` as follows:

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

Then, run the `terraform apply` command to apply the changes:

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

Then, you can use the `terraform show` or `terraform state show tidbcloud_serverless_cluster.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

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

## Import a TiDB Cloud Serverless cluster

For a TiDB Cloud Serverless cluster that is not managed by Terraform, you can use Terraform to manage it just by importing it.

Import a TiDB Cloud Serverless cluster that is not created by Terraform as follows:

1. Add an import block for the new TiDB Cloud Serverless cluster resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the cluster ID:

    ```
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new TiDB Cloud Serverless cluster resource according to the import block:

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    Do not specify an existing `.tf` filename in the preceding command. Otherwise, Terraform will return an error.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_serverless_cluster.example: Importing... 
    tidbcloud_serverless_cluster.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported cluster with Terraform.

## Delete a TiDB Cloud Serverless cluster

To delete a TiDB Cloud Serverless cluster, you can delete the configuration of the `tidbcloud_serverless_cluster` resource, then use the `terraform apply` command to destroy the resource:

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

Now, if you run the `terraform show` command, it will show no managed resources because the resource has been cleared:

```
$ terraform show
```
