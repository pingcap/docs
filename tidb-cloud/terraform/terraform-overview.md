---
title: Terraform Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform
---

# Terraform Overview

As a fully managed service of TiDB, TiDB Cloud can automate database maintenance operations. With the [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta), you can programmatically handle more operations such as deployment, scaling, and restore.

If you are looking for a simplified way to automate resource provisioning and your infrastructure workflow. You can try out our [TiDB Cloud Terraform provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud), which provides you with the following capabilities:

- Get your project information.
- Get cluster spec information, like supported cloud_provider, region, node size and so on.
- Manage your TiDB cluster, including creating, scaling, pausing and resuming a cluster.
- Create and delete the backup for your cluster.
- Create the restore task for your cluster.

## Requirements

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/release-notes): compatible with TiDB Cloud that is released at September 27, 2022
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Go](https://golang.org/doc/install) >= 1.18 (if you want to build the provider plugin)

## Supports

[Resources](https://www.terraform.io/language/resources) and [Data sources](https://www.terraform.io/language/data-sources) are the two most important elements in the Terraform language.

TiDB Cloud supports the following Resources and Data sources:

Resources

- `cluster`
- `backup` (`update` is not supported)
- `restore` (`update` and `delete` are not supported)

Data sources

- `project`
- `cluster spec`
- `restore`
- `backup`

You can get all the available configurations for the resources and data sources in this [document](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)