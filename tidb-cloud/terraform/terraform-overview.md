---
title: Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform
---

# Overview

TiDB Cloud already automate many database operations, and with our Open API you can programmatically handle additional operations like deployment, scaling, and restore.

If you are looking to a simplified ways to automate resource provisioning and your infrastructure workflow. I propose trying out our TiDB Cloud Terraform provider with the capabilities:

- Get your project information
- Get cluster spec information, like supported cloud_provider, region, node size and so on
- Mange your developer tier and dedicated tier, including create, scale, paused and resume the cluster
- Create and Delete the backup for your cluster
- Create the restore task for your cluster

## Requirements

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/): compatible with TiDB Cloud release 20220927
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Go](https://golang.org/doc/install) >= 1.18 (if you want to build the provider plugin)

## Supports

[Resources](https://www.terraform.io/language/resources) and [Data sources](https://www.terraform.io/language/data-sources) are the important elements in the Terraform language.

TiDB Cloud supports the following Resources and Data sources:

Resources

- cluster
- backup (not support update)
- restore (not support update and delete)

Data sources

- project
- cluster spec
- restore
- backup

You can get all the available configuration for the resources and data sources in this [doc](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)