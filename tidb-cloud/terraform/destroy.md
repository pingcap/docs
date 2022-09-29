---
title: Destroy resource
summary: Learn how to destroy resource
---

# Destroy Resource

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