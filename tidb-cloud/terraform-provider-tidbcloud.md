---
title: Terraform
summary: Create, manage, and update your TiDB Cloud resources through Terraform
---

- [Requirements](#requirements)
- [Support](#support)
- [Set up](#set-up)
- [Create an API key](#create-an-api-key)
- [Get TiDB Cloud provider](#get-tidb-cloud-provider)
- [Config the provider](#config-the-provider)
- [Get projectId with project Data Source](#get-projectid-with-project-data-source)
- [Get cluster spec info with cluster-spec Data Source](#get-cluster-spec-info-with-cluster-spec-data-source)
- [Create a dedicated cluster with cluster resource](#create-a-dedicated-cluster-with-cluster-resource)
- [Change the dedicated cluster](#change-the-dedicated-cluster)
- [Create a backup with backup resource](#create-a-backup-with-backup-resource)
- [Create a restore task with restore resource](#create-a-restore-task-with-restore-resource)
- [Import the restore cluster](#import-the-restore-cluster)
- [Destroy the dedicated cluster](#destroy-the-dedicated-cluster)

## Requirements

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Go](https://golang.org/doc/install) >= 1.18 (if you want to build the provider plugin)

## Support

Resources

- cluster
- backup
- restore

DataSource

- project
- cluster spec
- restore
- backup

## Set up

TiDB Cloud provider has released to terraform registry. All you need to do is install terraform (>=1.0).

For Mac user, you can install it with Homebrew.

First, install the HashiCorp tap, a repository of all our Homebrew packages.

```shell
brew tap hashicorp/tap
```

Now, install Terraform with hashicorp/tap/terraform.

```shell
brew install hashicorp/tap/terraform
```

See [terraform doc](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started) for other installation methods.

## Create an API key

The TiDB Cloud API uses HTTP Digest Authentication. It protects your private key from being sent over the network.

However, terraform-provider-tidbcloud does not support managing API key now. So you need to create the API key in the [console](https://tidbcloud.com/console/clusters).

Turn to [TiDB Cloud API doc](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) for help if you meet any problems.

## Get TiDB Cloud provider

Create a main.tf file:

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
```

- The `source` attribute defines the provider which will be downloaded from [Terraform Registry](https://registry.terraform.io/) by default
- The `version` attribute is optional which defines the version of the provider, it will use the latest version by default
- The `required_version` is optional which defines the version of the terraform, it will use the latest version by default

To get the TiDB Cloud provider, execute `terraform init`. It will download the provider from terraform registry.

```
$ terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of tidbcloud/tidbcloud from the dependency lock file
- Using previously-installed tidbcloud/tidbcloud v0.0.1

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

## Config the provider

You need to config the provider like:

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
```

username and password are the API key's public key and private key, you can also pass them with the environment:

```
export TIDBCLOUD_USERNAME = ${public_key}
export TIDBCLOUD_PASSWORD = ${private_key}
```

Now, you can use the tidbcloud provider.

## Get projectId with project Data Source

Let us get all the projects by project data source first:

- Use `data` block to define the data source of tidbcloud, it consists of the data source type and the data source name. In this example, data source type is `tidbcloud_project` and the name is `example_project`. The prefix of the type maps to the name of the provider.
- Use `output` block to get the information, and expose information for other Terraform configurations to use. It is similar to return values in programming languages. See [official doc](https://www.terraform.io/language/values/outputs) for more detail

Besides, you can find all the supported configs for the data source and resource [here](https://github.com/tidbcloud/terraform-provider-tidbcloud/tree/main/docs).

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

## Get cluster spec info with cluster-spec Data Source

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

Once again, you can find all the supported configs for the data source and resource [here](https://github.com/tidbcloud/terraform-provider-tidbcloud/tree/main/docs)

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

Execute `terraform apply` and type `yes` after check:

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

execute `terraform apply` and type `yes` after check:

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

Now, resume the cluster by set `paused = false`:

```
config = {
    paused = false
    root_password = "Your_root_password1."
    port          = 4000
    ...
  }
```

After apply you will find the status turns to `RESUMING`:

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

## Create a backup with backup resource

You have created and managed a dedicated cluster with terraform now.

Next, you will create a backup for the cluster by the backup resource.

First, copy the following config:

```
resource "tidbcloud_backup" "example_backup" {
  project_id  = "1372813089189561287"
  cluster_id  = "1379661944630234067"
  name        = "firstBackup"
  description = "create by terraform"
}
```

You can also get project_id and cluster_id from the cluster resource like:

```
resource "tidbcloud_backup" "example_backup" {
  project_id  = tidbcloud_cluster.example_cluster.project_id
  cluster_id  = tidbcloud_cluster.example_cluster.id
  name        = "firstBackup"
  description = "create by terraform"
}
```

Here we use the second config and execute `terraform apply`:

```
$ terraform apply

tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # tidbcloud_backup.example_backup will be created
  + resource "tidbcloud_backup" "example_backup" {
      + cluster_id       = "1379661944630234067"
      + create_timestamp = (known after apply)
      + description      = "create by terraform"
      + id               = (known after apply)
      + name             = "firstBackup"
      + project_id       = "1372813089189561287"
      + size             = (known after apply)
      + status           = (known after apply)
      + type             = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: 
```

Type `yes` to create a backup:

```
  Enter a value: yes

tidbcloud_backup.example_backup: Creating...
tidbcloud_backup.example_backup: Creation complete after 2s [id=1350048]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

```

Use `terraform state show tidbcloud_backup.example_backup` to check the state of the backup:

```
$ terraform state show tidbcloud_backup.example_backup

# tidbcloud_backup.example_backup:
resource "tidbcloud_backup" "example_backup" {
    cluster_id       = "1379661944630234067"
    create_timestamp = "2022-08-26T07:56:10Z"
    description      = "create by terraform"
    id               = "1350048"
    name             = "firstBackup"
    project_id       = "1372813089189561287"
    size             = "0"
    status           = "PENDING"
    type             = "MANUAL"
}
```

Wait for some minutes and use `terraform refersh`  to update the states:

```
$ terraform refresh  
tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
tidbcloud_backup.example_backup: Refreshing state... [id=1350048]
$ terraform state show tidbcloud_backup.example_backup
# tidbcloud_backup.example_backup:
resource "tidbcloud_backup" "example_backup" {
    cluster_id       = "1379661944630234067"
    create_timestamp = "2022-08-26T07:56:10Z"
    description      = "create by terraform"
    id               = "1350048"
    name             = "firstBackup"
    project_id       = "1372813089189561287"
    size             = "198775"
    status           = "SUCCESS"
    type             = "MANUAL"
}

```

Congratulations. You have create a backup for your cluster. Pay attention that the backup can not be updated.

## Create a restore task with restore resource

You have created a dedicated cluster and have a backup of the cluster.

Now, it is time to create a restore task by restore resource. With it, you can restore a cluster according to a backup.

Here is the config for restore resource. Note that you can only restore data from a smaller node size to a larger node size:

```

resource "tidbcloud_restore" "example_restore" {
  project_id = tidbcloud_cluster.example_cluster.project_id
  backup_id  = tidbcloud_backup.example_backup.id
  name       = "restoreCluster"
  config = {
    root_password = "Your_root_password1."
    port          = 4000
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
  }
}
```

Execute `terraform apply` and type `yes`:

```
$ terraform apply
tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
tidbcloud_backup.example_backup: Refreshing state... [id=1350048]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # tidbcloud_restore.example_restore will be created
  + resource "tidbcloud_restore" "example_restore" {
      + backup_id        = "1350048"
      + cluster          = {
          + id     = (known after apply)
          + name   = (known after apply)
          + status = (known after apply)
        }
      + cluster_id       = (known after apply)
      + config           = {
          + components    = {
              + tidb    = {
                  + node_quantity = 2
                  + node_size     = "8C16G"
                }
              + tiflash = {
                  + node_quantity    = 2
                  + node_size        = "8C64G"
                  + storage_size_gib = 500
                }
              + tikv    = {
                  + node_quantity    = 6
                  + node_size        = "8C32G"
                  + storage_size_gib = 500
                }
            }
          + port          = 4000
          + root_password = "Your_root_password1."
        }
      + create_timestamp = (known after apply)
      + error_message    = (known after apply)
      + id               = (known after apply)
      + name             = "restoreCluster"
      + project_id       = "1372813089189561287"
      + status           = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_restore.example_restore: Creating...
tidbcloud_restore.example_restore: Creation complete after 1s [id=780114]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Check the state of the restore task with `terraform state show tidbcloud_restore.example_restore`:

```
$ terraform state show tidbcloud_restore.example_restore

# tidbcloud_restore.example_restore:
resource "tidbcloud_restore" "example_restore" {
    backup_id        = "1350048"
    cluster          = {
        id     = "1379661944630264072"
        name   = "restoreCluster"
        status = "INITIALIZING"
    }
    cluster_id       = "1379661944630234067"
    config           = {
        components    = {
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
        port          = 4000
        root_password = "Your_root_password1."
    }
    create_timestamp = "2022-08-26T08:16:33Z"
    id               = "780114"
    name             = "restoreCluster"
    project_id       = "1372813089189561287"
    status           = "PENDING"
}
```

You can see the restore task's status is `PENDING` and the cluster's status is `INITIALIZING`.

After the cluster is `AVAILABLE`, the restore task will be `RUNNING` and turn to `SUCCESS` at last.

It is everything ok? No, the bad news is the restored cluster is not managed by terraform.

Don't worry, we can solve it in the next section.

## Import the restore cluster

We can manage a cluster with terraform by import even if it is not created by terraform.

Let us import the cluster which is created by the restore task in the last section.

First add a cluster resource like:

```
resource "tidbcloud_cluster" "restore_cluster1" {}
```

Then import the cluster by `terraform import tidbcloud_cluster.restore_cluster1 projectId,clusterId`, you can get the projectId and clusterId by restore resource:

```
$ terraform import tidbcloud_cluster.restore_cluster1 1372813089189561287,1379661944630264072

tidbcloud_cluster.restore_cluster1: Importing from ID "1372813089189561287,1379661944630264072"...
tidbcloud_cluster.restore_cluster1: Import prepared!
  Prepared tidbcloud_cluster for import
tidbcloud_cluster.restore_cluster1: Refreshing state... [id=1379661944630264072]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
```

Use `terraform state show tidbcloud_cluster.restore_cluster1` to get the state of the cluster:

```
$ terraform state show tidbcloud_cluster.restore_cluster1

# tidbcloud_cluster.restore_cluster1:
resource "tidbcloud_cluster" "restore_cluster1" {
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

In order to manage it, you can copy it to your config file. Remember to delete the status and id, for they are computed by terraform and can not be set in the config:

```
resource "tidbcloud_cluster" "restore_cluster1" {
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

You can use `terraform fmt` to format your config file:

```
$ terraform fmt 

main.tf
```

To ensure the consistency of the config and state, you can execute `terraform plan` or `terraform apply`. If you see `No changes`, the import is successful.

```
$ terraform apply

tidbcloud_cluster.restore_cluster1: Refreshing state... [id=1379661944630264072]
tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
tidbcloud_backup.example_backup: Refreshing state... [id=1350048]
tidbcloud_restore.example_restore: Refreshing state... [id=780114]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Now you can manage the cluster created by the restore task.

## Destroy the dedicated cluster

To destroy the resource, you can simply use `terraform destroy` and type `yes`. Don't worry about the order of deletion, terraform will generate a DAG based on the dependencies automatically.

```
$ terraform destroy

Plan: 0 to add, 0 to change, 4 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

tidbcloud_cluster.restore_cluster1: Destroying... [id=1379661944630264072]
tidbcloud_cluster.restore_cluster1: Destruction complete after 2s
tidbcloud_restore.example_restore: Destroying... [id=780114]
tidbcloud_restore.example_restore: Destruction complete after 0s
tidbcloud_backup.example_backup: Destroying... [id=1350048]
tidbcloud_backup.example_backup: Destruction complete after 2s
tidbcloud_cluster.example_cluster: Destroying... [id=1379661944630234067]
tidbcloud_cluster.example_cluster: Destruction complete after 0s
╷
│ Warning: Unsupported
│ 
│ restore can't be delete
╵

Destroy complete! Resources: 4 destroyed.
```

Note that a warning is appeared for restore can't be deleted.

If you execute `terraform show`, you will find nothing for all the states is cleared:

```
$ terraform show

```