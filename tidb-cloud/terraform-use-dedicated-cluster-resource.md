---
title: Use TiDB Cloud Dedicated Cluster Resource
summary: Learn how to use the TiDB Cloud Dedicated cluster resource to create and modify a TiDB Cloud Dedicated cluster.
---

# Use TiDB Cloud Dedicated Cluster Resource

This document describes how to manage a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster with the `tidbcloud_dedicated_cluster` resource.

In addition, you will also learn how to get the necessary information with the `tidbcloud_projects` data source and use the `tidbcloud_dedicated_node_group` resource to manage TiDB node groups of your TiDB Cloud Dedicated cluster.

The features of the `tidbcloud_dedicated_cluster` resource include the following:

- Create TiDB Cloud Dedicated clusters.
- Modify TiDB Cloud Dedicated clusters.
- Import TiDB Cloud Dedicated clusters.
- Delete TiDB Cloud Dedicated clusters.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.

## Get project IDs using the `tidbcloud_projects` data source

Each TiDB Cloud Dedicated cluster belongs to a project. Before creating a TiDB Cloud Dedicated cluster, you need to obtain the ID of the project where you want to create the cluster. If no `project_id` is specified, the default project will be used.

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

        The `output` block works similarly to returned values in programming languages. For more information, see the [Terraform documentation](https://www.terraform.io/language/values/outputs).

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

## Create a TiDB Cloud Dedicated cluster

> **Note:**
>
> - Before you begin, make sure that you have set a CIDR in the [TiDB Cloud console](https://tidbcloud.com). For more information, see [Set a CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region). 
> - You can also [create a `dedicated_network_container` resource](/tidb-cloud/terraform-use-dedicated-network-container-resource.md) to manage your CIDR.

You can create a TiDB Cloud Dedicated cluster using the `tidbcloud_dedicated_cluster` resource as follows:

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

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the TiDB Cloud Dedicated cluster resource, set the resource type as `tidbcloud_dedicated_cluster`.
    - For the resource name, you can define it as needed. For example, `example_cluster`.
    - For the resource details, you can configure them according to the Project ID and the TiDB Cloud Dedicated cluster specification information. 
    - To get the TiDB Cloud Dedicated cluster specification information, see [tidbcloud_dedicated_cluster (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_cluster).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

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

    In the preceding result, Terraform generates an execution plan for you, which describes the actions that Terraform will take:

    - You can check the difference between the configurations and the states.
    - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
    - The `known after apply` shows that you will get the value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Creating...
    tidbcloud_dedicated_cluster.example_cluster: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    It usually takes at least 10 minutes to create a TiDB Cloud Dedicated cluster.

5. Use the `terraform show` or `terraform state show tidbcloud_dedicated_cluster.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

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

6. If you want to synchronize the state from the remote, run the `terraform refresh` command to update the state, and then run the `terraform state show tidbcloud_dedicated_cluster.${resource-name}` command to display the state.

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

## Modify a TiDB Cloud Dedicated cluster

For a TiDB Cloud Dedicated cluster, you can use Terraform to manage resources as follows:

- Add a TiFlash component to the cluster.
- Scale the cluster.
- Pause or resume the cluster.
- Add a [TiDB node group](/tidb-cloud/tidb-node-group-overview.md) to the cluster.
- Update a TiDB node group of the cluster.
- Delete a TiDB node group of the cluster.

### Add a TiFlash component

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-tidb-cloud-dedicated-cluster), add the `tiflash_node_setting` configuration.

    For example:

    ```
    tiflash_node_setting = {
      node_spec_key = "2C4G"
      node_count = 3
      storage_size_gi = 60
    }
    ```

2. Run the `terraform apply` command:

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

    In the preceding execution plan, TiFlash will be added, and one resource will be changed.

3. If everything in your plan looks fine, type `yes` to continue:

    ```shell
      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. Use `terraform state show tidbcloud_dedicated_cluster.${resource-name}` to check the state:

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

The `MODIFYING` state indicates that the cluster is being modified. The state will change to `ACTIVE` once the modification is complete.

### Scale a cluster

You can scale a TiDB Cloud Dedicated cluster when its state is `ACTIVE`.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-tidb-cloud-dedicated-cluster), edit the configurations of `tidb_node_setting`, `tikv_node_setting` and `tiflash_node_setting`.

    For example, to add one more TiDB node, three more TiKV nodes (the number of TiKV nodes needs to be a multiple of 3, because its scaling step is 3), and one more TiFlash node, you can edit the configurations as follows:

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

2. Run the `terraform apply` command and type `yes` for confirmation:

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

Wait for the process to finish. The state will change to `ACTIVE` once the scaling is complete.

### Pause or resume a cluster

You can pause a cluster when its state is `ACTIVE` or resume a cluster when its state is `PAUSED`.

- Set `paused = true` to pause a cluster.
- Set `paused = false` to resume a cluster.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-tidb-cloud-dedicated-cluster), add `pause = true` to the configurations:

    ```
    paused = true
    ```

2. Run the `terraform apply` command and type `yes` after checking the plan:

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

3. Use the `terraform state show tidbcloud_dedicated_cluster.${resource-name}` command to check the state:

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

4. When you need to resume the cluster, set `paused = false`:

    ```
    paused = false
    ```

5. Run the `terraform apply` command and type `yes` for confirmation. Wait for a moment, the state will be changed to `ACTIVE` finally.

### Add a TiDB node group to the cluster

You can add a TiDB node group to the cluster when its state is `ACTIVE`.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-tidb-cloud-dedicated-cluster), add the `tidbcloud_dedicated_node_group` configuration.

    For example, to add a TiDB node group with 3 nodes, you can edit the configurations as follows:

    ```
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
        node_count = 3
        display_name = "test-node-group"
    }
    ```

2. Run the `terraform apply` command and type `yes` for confirmation:

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

3. Use the `terraform state show tidbcloud_dedicated_node_group.${resource-name}` command to check the state:

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

### Update a TiDB node group of the cluster

You can update a TiDB node group of the cluster when its state is `ACTIVE`.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-tidb-cloud-dedicated-cluster), edit the configurations of `tidbcloud_dedicated_node_group`.

    For example, to change the node count to `1`, edit the configurations as follows:

    ```
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
        node_count = 1
        display_name = "test-node-group"
    }
    ```

2. Run the `terraform apply` command and type `yes` for confirmation:

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

### Delete a TiDB node group of the cluster

To delete a TiDB node group of the cluster, you can delete the configuration of the `dedicated_node_group` resource, then use the `terraform apply` command to destroy the resource:

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

Now, if you run the `terraform show` command, you will get nothing because the resource has been cleared:

```
$ terraform show
```

## Import a cluster

For a TiDB cluster that is not managed by Terraform, you can use Terraform to manage it just by importing it.

Import a cluster that is not created by Terraform as follows:

1. Add an import block for the new TiDB Cloud Dedicated cluster resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the cluster ID:

    ```
    import {
      to = tidbcloud_dedicated_cluster.example_cluster
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new TiDB Cloud Dedicated cluster resource according to the import block:

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    Do not specify an existing `.tf` file name in the preceding command. Otherwise, Terraform will return an error.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_dedicated_cluster.example_cluster: Importing... 
    tidbcloud_dedicated_cluster.example_cluster: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported cluster with Terraform.

## Delete a TiDB Cloud Dedicated cluster

To delete a TiDB Cloud Dedicated cluster, you can delete the configuration of the `tidbcloud_dedicated_cluster` resource, then use the `terraform apply` command to destroy the resource:

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

Now, if you run the `terraform show` command, it will show no managed resources because the resource has been cleared:

```
$ terraform show
```
