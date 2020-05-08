---
title: Create a Private Mirror
summary: Learn how to create a private mirror.
category: tools
---

# Create a Private Mirror

When creating a private cloud, usually, you need to use an isolated network environment, where the official mirror of TiUP is not accessible. Therefore, you can create a private mirror, which is mainly implemented by the `mirrors` component. You can also use `mirrors` for offline deployment.

## `mirrors` description

Execute the following command to get the help documentation of the `mirrors` component:

{{< copyable "shell-regular" >}}

```bash
tiup mirrors --help
```

```
Starting component `mirrors`: /Users/joshua/.tiup/components/mirrors/v0.0.1/mirrors
Build a local mirrors and download all selected components
Usage:
  tiup mirrors <target-dir> [global-version] [flags]
Examples:
  tiup mirrors local-path --arch amd64,arm --os linux,darwin    # Specify the architectures and OSs
  tiup mirrors local-path --full                                # Build a full local mirrors
  tiup mirrors local-path --tikv v4                             # Specify the version via prefix
  tiup mirrors local-path --tidb all --pd all                   # Download all version for specific component
Flags:
      --overwrite                   Overwrite the exists tarball
  -f, --full                        Build a full mirrors repository
  -a, --arch strings                Specify the downloading architecture (default [amd64])
  -o, --os strings                  Specify the downloading os (default [linux,darwin])
      --tidb strings                Specify the versions for component tidb
      --tikv strings                Specify the versions for component tikv
      --pd strings                  Specify the versions for component pd
      --playground strings          Specify the versions for component playground
      --client strings              Specify the versions for component client
      --prometheus strings          Specify the versions for component prometheus
      --package strings             Specify the versions for component package
      --grafana strings             Specify the versions for component grafana
      --alertmanager strings        Specify the versions for component alertmanager
      --blackbox_exporter strings   Specify the versions for component blackbox_exporter
      --node_exporter strings       Specify the versions for component node_exporter
      --pushgateway strings         Specify the versions for component pushgateway
      --tiflash strings             Specify the versions for component tiflash
      --drainer strings             Specify the versions for component drainer
      --pump strings                Specify the versions for component pump
      --cluster strings             Specify the versions for component cluster
      --mirrors strings             Specify the versions for component mirrors
      --bench strings               Specify the versions for component bench
      --insight strings             Specify the versions for component insight
      --doc strings                 Specify the versions for component doc
      --ctl strings                 Specify the versions for component ctl
  -h, --help                        help for tiup
```

The basic use of the `tiup mirrors` command is as follows:

{{< copyable "shell-regular" >}}

```bash
tiup mirrors <target-dir> [global-version] [flags]
```

- `target-dir`: The directory which stores cloned data.
- `global-version`: Used to quickly set a global version for all components.

The `tiup mirrors` command provides a number of optional flags (might be more in the future). These flags can be divided into four categories according to their purposes:

- Determines whether to override local packages

    The `--overwrite` flag determines whether to override the local package with the package of the official mirror, if the specified `<target-dir>` contains the package you need to download. If you set this flag, the local package is overridden.

- Determines whether to use the full clone

    If you specify the `--full` flag, you can clone the official mirror completely.

    > **Note:**
    >
    > If `--full` and the other flags are not specified, only some meta information is cloned.

- Determines whether to clone packages from the specific platform

    If you only clone packages from one or more specific platforms, use `-os` and `-arch` to specify the platform. For example:

    - Execute the `tiup mirros <target-dir> --os=linux` command to clone for linux.
    - Execute the `tiup mirros <target-dir> --arch=amd64` command to clone for amd64.
    - Execute the `tiup mirros <target-dir> --os=linux --arch=amd64` command to clone for linux/amd64.

- Determines whether to clone the specific version of the packages

    If you clone only one version (not all versions) of a component, use `--<component>=<version>` to specify the version. For example:

    - Execute the `tiup mirrors <target-dir> --tidb v4` command to clone the v4 version of TiDB.
    - Execute the `tiup mirros <target-dir> --tidb v4 --tikv all` command to clone the v4 version of TiDB, as well as all versions of TiKV.
    - Execute the `tiup mirrors <target-dir> v4.0.0-rc` command to clone the v4.0.0-rc version of all components in a cluster.

## Usage examples

This section introduces the usage examples of `mirrors`, including offline installation of a TiDB cluster, and the creation of a private mirror.

### Offline install a TiDB cluster using TiUP

If you want to offline install a TiDB cluster of the v4.0.0-rc version in an isolated environment, take the following steps:

1. Pull the required components on a machine connected to the external network:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup mirrors package --os=linux v4.0.0-rc
    ```

    Then you can create a `package` directory in the current directory. The `package` directory contains necessary components packages to start a cluster.

2. Use the `tar` command to archive the components packages and send it to the central control machine that is in the isolated environment:

    {{< copyable "shell-regular" >}}

    ```bash
    tar czvf package.tar.gz package
    ```

    Then `package.tar.gz` is an isolated, offline environment.

3. After sending the package to the central control machine of the target cluster, execute the following command to install TiUP:

    {{< copyable "shell-regular" >}}

    ```bash
    tar xzvf package.tar.gz
    cd package
    sh local_install.sh
    ```

4. Follow the instructions to finish the installation of TiUP, and then deploy the TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```bash
    export TIUP_MIRRORS=/path/to/mirror
    tiup cluster deploy <cluster-name> <cluster-version> <topology-file>
    tiup cluster start <cluster-name>
    ```

    `/path/to/mirror` refers to where `<target-dir>` (in `tiup mirrors <target-dir>`) is. If `/tmp/package` refers to where `<target-dir>` is, execute the following command instead:

    {{< copyable "shell-regular" >}}

    ```bash
    export TIUP_MIRRORS=/tmp/package
    ```

After you complete the deployment, refer to [Deploy and Maintain the TiDB Online Cluster Using TiUP](/reference/tools/tiup/cluster.md) for more details of the cluster operations.

### Create a private mirror

The process of creating a private mirror is similar to that of creating an offline installer. The only difference is that you need to upload the content of the `package` directory to CDN or a file server. Execute the following command to create a private mirror:

{{< copyable "shell-regular" >}}

```bash
cd package
python -m SimpleHTTPServer 8000
```

Now you have created a private mirror at <http://127.0.0.1:8000>.

Then execute the following command to install TiUP using the private mirror:

{{< copyable "shell-regular" >}}

```bash
export TIUP_MIRRORS=http://127.0.0.1:8000
curl $TIUP_MIRRORS/install.sh | sh
```

After importing the `PATH` variable, you can start to use TiUP. Make sure that the `TIUP_MIRRORS` variable points to the private mirror.
