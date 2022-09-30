---
title: Cluster Resource
summary: Learn how to use cluster resource
---

# Cluster Resource

> **Note:**
>
> Make sure you have followed the [Get TiDB Cloud provider](/tidb-cloud/terraform/tidbcloud-provider.md)

## Get projectId with project data source

Let us get all the projects by project data source first:

- Use `data` block to define the data source of tidbcloud, it consists of the data source type and the data source name. In this example, data source type is `tidbcloud_project` and the name is `example_project`. The prefix of the type maps to the name of the provider.
- Use `output` block to get the information, and expose information for other Terraform configurations to use. It is similar to return values in programming languages. See [terraform doc](https://www.terraform.io/language/values/outputs) for more detail

Besides, you can find all the supported configs for the data source and resource [here](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

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

Then you can apply the configuration with the `terraform apply`, you need to type `yes` at the confirmation prompt to proceed. Use `terraform apply --auto-approve` to skip the type.

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

Now, you get all the available projects, copy one of the id you need. Here we use the default project's ID.

## Get cluster spec info with cluster-spec data source

Before creating a TiDB cluster, you may need to get the available config values (providers, regions and so on.) by cluster-spec Data Source:

```
data "tidbcloud_cluster_spec" "example_cluster_spec" {
}

output "cluster_spec" {
  value = data.tidbcloud_cluster_spec.example_cluster_spec.items
}
```

Execute the `terraform apply --auto-approve`, we will get all the specifications. Here we show a part of the results:

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

- `cloud_provider` is the cloud provider on which your TiDB cluster is hosted
- `region` is the region of cloud_provider
- `node_quantity_range` shows the min quantity of the node and the step if you want to scale the node
- `node_size` is the size of the node
- `storage_size_gib_range` shows the min and max storage you can set to the node

## Create a dedicated cluster with cluster resource

> Make sure you have set a Project CIDR on TiDB Cloud console first.

Now, you can create a dedicated cluster with the projectId and the spec info:

- Use `resource` block to define the resource of tidbcloud, it consists of the resource type and the resource name. In this example, resource type is `tidbcloud_cluster` and the name is `example_cluster`

Once again, you can find all the supported configs for the data source and resource [here](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)

Here I give an example for tidbcloud_cluster:

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

Execute `terraform apply`, it is not recommended to use `terraform apply --auto-approve` when you apply a resource.

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

- You can check the diff between the configuration and the state
- You can also see the results of this `apply`: it will add a new resource, and no resource will be changed or destroyed
- The `known after apply` shows that you will get the value after `apply`

If everything is in your plan, type the `yes` to continue:

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_cluster.example_cluster: Creating...
tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

```

Use `terraform show` or `terraform state show tidbcloud_cluster.example_cluster` to inspect the state of your resource. The former will show all the states (all the resources and the data source).

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

The status of the cluster is CREATING, we need to wait until it changes to `AVAILABLE`, it usually takes 10+ minutes.

Once you want to check the status, execute `terraform refresh` to update the state, then use `terraform state show tidbcloud_cluster.example_cluster` to check the status.

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

## Change the dedicated cluster

We can also use terraform to manage the resource. As for cluster resource, we can:

- Increase TiFlash component for the dedicated cluster
- Scale the TiDB cluster
- Pause or resume the cluster

**Increase TiFlash component**

First, add tiflash config in components:

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

Then, execute `terraform apply`:

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

Check the plan, you will find tiflash is added. And one resource will be changed after apply. Type `yes`:

```
  Enter a value: yes

tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

Use `terraform state show tidbcloud_cluster.example_cluster` to see the status:

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

The `MODIFYING` status shows the cluster is changing now. Wait for a moment, the status will be changed to `AVAILABLE`.

**Scale the TiDB cluster**

After the status is `AVAILABLE`, let us try to scale the TiDB cluster.

Add one node for TiDB and TiFlash, TiKV needs to add at least 3 nodes for its step is 3.

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

**Pause or resume the cluster**

The cluster can also be paused when the status is `AVAILABLE` or be resumed when the status is `PAUSED`.

- set `paused = true` to pause the cluster
- set `paused = false` to resume the cluster

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