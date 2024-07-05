---
title: tiup cluster patch
summary: The `tiup cluster patch` command allows for dynamic replacement of binaries in a running cluster. It uploads the binary package, stops the target service, replaces the binary, and starts the service. Preparation involves packing the binary package and using options like `--overwrite`, `--transfer-timeout`, `-N, --node`, `-R, --role`, and `--offline`. The output is the execution log of the tiup-cluster.
---

# tiup cluster patch

If you need to dynamically replace the binaries of a service while the cluster is running (namely, keep the cluster available during the replacement process), you can use the `tiup cluster patch` command. After the command is executed, TiUP does the following things:

- Uploads the binary package for replacement to the target machine.
- If the target service is a storage service such as TiKV, TiFlash, or TiDB Binlog, TiUP first takes the related nodes offline via the API.
- Stops the target service.
- Unpacks the binary package and replace the service.
- Starts the target service.

## Syntax

```shell
tiup cluster patch <cluster-name> <package-path> [flags]
```

- `<cluster-name>`: The name of the cluster to be operated.
- `<package-path>`: The path to the binary package used for replacement.

### Preparation

Before running the `tiup cluster patch` command, you need to pack the binary package required. Take the following steps:

1. Determine the following variables:

    - `${component}`: the name of the component to be replaced (such as `tidb`, `tikv`, or `pd`).
    - `${version}`: the version of the component (such as `v8.1.0` or `v7.5.1`).
    - `${os}`: the operating system (`linux`).
    - `${arch}`: the platform on which the component runs (`amd64`, `arm64`).

2. Download the current component package using the command:

    ```shell
    wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz
    ```

3. Create a temporary directory to pack files and change to it:

    ```shell
    mkdir -p /tmp/package && cd /tmp/package
    ```

4. Extract the original binary package:

    ```shell
    tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz
    ```

5. Check out the file structure in the temporary directory:

    ```shell
    find .
    ```

6. Copy the binary files or configuration files to their corresponding locations in the temporary directory.
7. Pack all files in the temporary directory:

    ```shell
    tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *
    ```

After you have completed the preceding steps, you can use `/tmp/${component}-hotfix-${os}-${arch}.tar.gz` as the `<package-path>` in the `tiup cluster patch` command.

## Options

### --overwrite

- After you patch a certain component (such as TiDB or TiKV), when the tiup cluster scales out the component, TiUP uses the original component version by default. To use the version that you patch when the cluster scales out in the future, you need to specified the option `--overwrite` in the command.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### --transfer-timeout

- When restarting the PD or TiKV service, TiKV/PD first transfers the leader of the node to be restarted to another node. Because the transfer process takes some time, you can use the option `--transfer-timeout` to set the maximum waiting time (in seconds). After the timeout, TiUP directly restarts the service.
- Data type: `UINT`
- If this option is not specified, TiUP directly restarts the service after waiting for `600` seconds.

> **Note:**
>
> If TiUP directly restarts the service after the timeout, the service performance might jitter.

### -N, --node

- Specifies nodes to be replaced. The value of this option is a comma-separated list of node IDs. You can get the node ID from the first column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified, TiUP does not select any nodes to replace by default.

> **Note:**
>
> If the option `-R, --role` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### -R, --role

- Specifies the roles to be replaced. The value of this option is a comma-separated list of the roles of the nodes. You can get the role deployed on a node from the second column of the [cluster status table](/tiup/tiup-component-cluster-display.md) returned by the `tiup cluster display` command.
- Data type: `STRINGS`
- If this option is not specified, TiUP does not select any roles to replace by default.

> **Note:**
>
> If the option `-N, --node` is specified at the same time, TiUP then replaces service nodes that match both the requirements of `-N, --node` and `-R, --role`.

### --offline

- Declares that the current cluster is not running. When the option is specified, TiUP does not evict the service leader to another node or restart the service, but only replaces the binary files of cluster components.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

### -h, --help

- Prints help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Outputs

The execution log of the tiup-cluster.

[<< Back to the previous page - TiUP Cluster command list](/tiup/tiup-component-cluster.md#command-list)
