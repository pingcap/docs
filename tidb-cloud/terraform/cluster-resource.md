---
title: Cluster Resource
summary: Learn how to use cluster resource
---

# Cluster Resource

You can learn how to create and modify a TiDB Cloud cluster with cluster resource in this doc.

Besides, you will also learn how to get the necessary information from project data source and cluster-spec data source in this doc.

> **Note:**
>
> Make sure you have followed the instructions in [Get TiDB Cloud Terraform provider](/tidb-cloud/terraform/tidbcloud-provider.md).

## Get projectId from project data source

Let us get all the projects by project data source first:

- Use the `data` block to define the data source of TiDB Cloud. It consists of the data source type and the data source name. In this example, the data source type is `tidbcloud_project` and the name is `example_project`. The prefix of the type maps to the name of the provider.
- Use the `output` block to get the information, and expose the information for other Terraform configurations to use. It works similarly to returned values in programming languages. See [Terraform documentation](https://www.terraform.io/language/values/outputs) for more details.

By the way, you can find all the supported configurations for the data sources and resources [here](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

```
terraform {
  required_providers {
    tidbcloud = {
      source = "tidbcloud/tidbcloud"
      version = "~> 0.0.1"
    }
  }
  required_version = ">= 1.0.0"
}

provider "tidbcloud" {
  username = "fake_username"
  password = "fake_password"
}

data "tidbcloud_project" "example_project" {
  page      = 1
  page_size = 10
}

output "projects" {
  value = data.tidbcloud_project.example_project.items
}
```

Run `terraform apply` command to apply the configurations. You need to type `yes` at the confirmation prompt to proceed.

To skip the prompt, use `terraform apply --auto-approve`:

```shell
$ terraform apply --auto-approve
data.tidbcloud_project.example_project: Reading...
data.tidbcloud_project.example_project: Read complete after 1s [id=just for test]

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

Now, you will get all the available projects, copy one of the projectId you need. Here we use the default project's ID.

## Get cluster specification information with cluster-spec data source

Before creating a TiDB cluster, you may need to get the available configuration values (cloud providers, regions, and so on.) by the cluster-spec data source:

```
data "tidbcloud_cluster_spec" "example_cluster_spec" {
}

output "cluster_spec" {
  value = data.tidbcloud_cluster_spec.example_cluster_spec.items
}
```

Run the `terraform apply --auto-approve` command and you will get all the specifications. 

The following is a part of the results for your reference.

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
        "node_size" = "2C8G"
      },
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
        "node_size" = "2C8G"
        "storage_size_gib_range" = {
          "max" = 500
          "min" = 200
        }
      },
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

- `cloud_provider` is the cloud provider on which your TiDB cluster is hosted.
- `region` is the region of `cloud_provider`.
- `node_quantity_range` shows the minimum quantity of the node and the step if you want to scale the node.
- `node_size` is the size of a node.
- `storage_size_gib_range` shows the minimum and maximum storage size you can set for a node.

## Create a Dedicated Tier with cluster resource

> **Note:**
>
> Before you begin, make sure that you have set a Project CIDR in the TiDB Cloud console.

Then, you can create a Dedicated Tier cluster with the projectId and the spec info using cluster resource.

1. Use the `resource` block to define the resource of TiDB Cloud. It consists of the resource type and the resource name. In this example, the resource type is `tidbcloud_cluster` and the name is `example_cluster`.

    ```
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

2. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply
    data.tidbcloud_project.example_project: Reading...
    data.tidbcloud_project.example_project: Read complete after 1s [id=just for test]
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
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

    Terraform will generate an execution plan for you:

   - You can check the difference between the configurations and the states.
   - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
   - The `known after apply` shows that you will get the value after `apply`.

3. If everything is in your plan, type `yes` to continue:

    ```
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.
    
      Enter a value: yes
    
    tidbcloud_cluster.example_cluster: Creating...
    tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]
    
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    
    ```

4. Use the `terraform show` or `terraform state show tidbcloud_cluster.example_cluster` command to inspect the state of your resource. The former will show all the states (all the resources and the data source).

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

    The status of the cluster is `CREATING`. In this case, you need to wait until it changes to `AVAILABLE`, which usually takes 10 minutes at least.

5. If you want to check the latest status, run the `terraform refresh` command to update the state, and then run the `terraform state show tidbcloud_cluster.example_cluster` command to display the status.

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

Congratulations. Your cluster is available now.

## Modify the Dedicated Tier cluster

You can use Terraform to manage cluster resources as follows:

- Increase TiFlash component for the dedicated cluster.
- Scale the TiDB cluster.
- Pause or resume the cluster.

### Increase TiFlash component

1. Add TiFlash configuration in components:

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

2. Run `terraform apply` command:

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

3. By checking the plan, you will find that TiFlash is added. And one resource will be changed after `terraform apply`. Then type `yes` to confirm:

    ```
      Enter a value: yes
    
    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]
    
    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. Use `terraform state show tidbcloud_cluster.example_cluster` to see the status:

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

The `MODIFYING` status indicates that the cluster is changing now. Wait for a moment. The status will be changed to `AVAILABLE`.

### Scale a TiDB cluster

You can scale a TiDB cluster when its status is `AVAILABLE`.

For example, to add 1 node for TiDB, 3 nodes for TiKV (TiKV needs to add at least 3 nodes for its step is 3, you can get this information in cluster-spec data source), and 1 node for TiFlash, you can update the configurations as follows:

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

Run the `terraform apply` command and type `yes` after check:

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

Wait for the status from `MODIFYING` to `AVAILABLE`.

### Pause or resume a cluster

You can pause a cluster when its status is `AVAILABLE` or resume a cluster when its status is `PAUSED`.

- Set `paused = true` to pause a cluster.
- Set `paused = false` to resume a cluster.

```
config = {
    paused = true
    root_password = "Your_root_password1."
    port          = 4000
    ...
  }
```

Run the `terraform apply` command and type `yes` after check:

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

Use the `terraform state show tidbcloud_cluster.example_cluster` to check the status:

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

Now, resume the cluster by setting `paused = false`:

```
config = {
    paused = false
    root_password = "Your_root_password1."
    port          = 4000
    ...
  }
```

After `apply`, you will find the status turns to `RESUMING`:

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

Wait for a moment, the status will be changed to `AVAILABLE` again.

Now, you have created and managed a Dedicated Tier cluster with Terraform. Next, you can create a backup of the cluster by the [backup resource](/tidb-cloud/terraform/backup-resource.md).


## Destroy cluster

Run `terraform destroy` command to destroy the cluster resource:

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

Now, if you run the `terraform show` command, you will get nothing because the resource have been cleared:

```
$ terraform show
```

