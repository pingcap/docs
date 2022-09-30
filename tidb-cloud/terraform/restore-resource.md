---
title: Restore Resource
summary: Learn how to use restore resource
---

# Restore Resource

> **Note:**
>
> Because the backup and restore feature is unavailable for Developer Tier clusters. To use restore resources, make sure that you have created a Dedicated Tier cluster.

## Create a restore task with restore resource

After creating a backup of a cluster, you can restore the cluster by creating a restore task with restore resources.

You can configure a restore resource as follows. Note that you can only restore data from a smaller node size to a larger node size:

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

Run the `terraform apply` command and type `yes`:

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

You can manage a cluster with Terraform by importing the cluster even if it is not created by Terraform.

The following steps show you how to import the cluster created by the restore task in the last section.

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