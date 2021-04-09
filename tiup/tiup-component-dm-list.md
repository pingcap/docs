---
title: tiup dm list
---

# tiup dm list

`tiup-dm` supports deploying multiple clusters with the same central console. You can use the command `tiup dm list` to check which clusters are deployed using the central console by the currently logged-in user.

> **Note:**
> 
> By default, the data of the deployed clusters is stored in the `~/.tiup/storage/dm/clusters/` directory. The currently logged-in user cannot view the clusters deployed by other users on the same central console.

## Syntax

```sh
tiup dm list [flags]
```

## Options

### -h, --help (boolean, default false)

Show help information in the output.

## Output

The output is a table containing the following fields.

- Name: the cluster name
- User: the user who deployed the cluster
- Version: the cluster version
- Path: the path of the cluster deployment data on the central control machine
- PrivateKey: the path of the private key to the cluster

