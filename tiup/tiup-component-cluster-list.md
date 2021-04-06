---
title: tiup cluster list
---

# tiup cluster list

tiup-cluster supports the deployment of multiple clusters using the same central control machine. You can use the `tiup cluster list` command to view which clusters are deployed by the currently logged-in user using this central control machine.

> **Note:**
>
> The deployed cluster data is placed in the `~/.tiup/storage/cluster/clusters/` directory by default, so on the same central control machine, the currently logged-in user cannot view the clusters deployed by other users.

## Syntax

```shell
tiup cluster list [flags]
```

## Options

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- Default: false

## Outputs

Output the table with the following fields:

- Name: the cluster name
- User: the deployment user
- Version: the cluster version
- Path: the path of the cluster deployment data on the central control machine
- PrivateKey: the path of the private key connected to the cluster