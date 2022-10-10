---
title: TiDB Cloud Terraform Provider Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform
---

# TiDB Cloud Terraform Provider Overview

As a fully managed service of TiDB, TiDB Cloud can automate database maintenance operations. With the [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta), you can programmatically handle operations such as deployment, scaling, and restore.

If you are looking for a simplified way to automate resource provisioning and your infrastructure workflow. You can try out our [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud), which provides you with the following capabilities:

- Get your project information.
- Get cluster specification information, such as supported cloud provider, region, and node size.
- Manage your TiDB cluster, including creating, scaling, pausing, and resuming a cluster.
- Create and delete a backup for your cluster.
- Create a restore task for your cluster.

## Requirements

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Go](https://golang.org/doc/install) >= 1.18 (if you want to build the provider plugin)

## Supported resources and data sources

[Resources](https://www.terraform.io/language/resources) and [Data sources](https://www.terraform.io/language/data-sources) are the two most important elements in the Terraform language.

TiDB Cloud supports the following resources and data sources:

Resources

- `cluster`
- `backup` (`update` is not supported)
- `restore` (`update` and `delete` are not supported)

Data sources

- `project`
- `cluster spec`
- `restore`
- `backup`

You can get all the available configurations for the resources and data sources in this [document](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

## Next step

To start using TiDB Cloud Terraform Provider, refer to the following documents:

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform/tidbcloud-provider.md)
- [Cluster Resource](/tidb-cloud/terraform/cluster-resource.md)
- [Backup Resource](/tidb-cloud/terraform/backup-resource.md)
- [Restore Resource](/tidb-cloud/terraform/restore-resource.md)