---
title: tiup dm list
---

# tiup dm list

`tiup-dm` supports deploying multiple clusters using the same central console. You can use the `tiup dm list` command to check which clusters are deployed using the central console by the currently logged-in user.

> **Note:**
>
> By default, the data of the deployed clusters is stored in the `~/.tiup/storage/dm/clusters/` directory. The currently logged-in user cannot view the clusters deployed by other users on the same central console.

## Syntax

```sh
tiup dm list [flags]
```

## Options

### -h, --help

- Shows the help information in the output.
- Data type: `BOOLEAN`
- Default: false

## Output

A table consisting of the following fields:

- `Name`: the cluster name.
- `User`: the user who deployed the cluster.
- `Version`: the cluster version.
- `Path`: the path of the cluster deployment data on the central control machine.
- `PrivateKey`: the path of the private key to the cluster.
