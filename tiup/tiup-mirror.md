---
title: Create a Private Mirror
summary: Learn how to create a private mirror.
aliases: ['/tidb/dev/tiup-mirrors','/docs/dev/tiup/tiup-mirrors/','/docs/dev/reference/tools/tiup/mirrors/']
---

# Create a Private Mirror

When creating a private cloud, usually, you need to use an isolated network environment, where the official mirror of TiUP is not accessible. Therefore, you can create a private mirror, which is mainly implemented by the `mirror` command. You can also use the `mirror` command for offline deployment. A private mirror also allows you to use components that you build and package yourself.

## TiUP `mirror` overview

Execute the following command to get the help information of the `mirror` command:

{{< copyable "shell-regular" >}}

```bash
tiup mirror --help
```

```bash
The 'mirror' command is used to manage a component repository for TiUP, you can use
it to create a private repository, or to add new component to an existing repository.
The repository can be used either online or offline.
It also provides some useful utilities to help managing keys, users and versions
of components or the repository itself.

Usage:
  tiup mirror <command> [flags]

Available Commands:
  init        Initialize an empty repository
  sign        Add signatures to a manifest file
  genkey      Generate a new key pair
  clone       Clone a local mirror from remote mirror and download all selected components
  merge       Merge two or more offline mirrors
  publish     Publish a component
  show        Show mirror address
  set         Set mirror address
  modify      Modify published component
  renew       Renew the manifest of a published component.
  grant       grant a new owner
  rotate      Rotate root.json

Global Flags:
      --help                 Help for this command
      --skip-version-check   Skip the strict version check, by default a version must be a valid SemVer string

Use "tiup mirror [command] --help" for more information about a command.
```

## Cloning

The `tiup mirror clone` command is used to build a local mirror. The basic usage is as follows:

{{< copyable "shell-regular" >}}

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

- `target-dir`: used to specify the directory in which cloned data is stored.
- `global-version`: used to quickly set a global version for all components.

The `tiup mirror clone` command provides many optional flags (might provide more in the future). These flags can be divided into the following categories according to their intended usages:

- Determines whether to use prefix matching to match the version when cloning

    If the `--prefix` flag is specified, the version number is matched by prefix for the clone. For example, if you specify `--prefix` as "v5.0.0", then "v5.0.0-rc", and "v5.0.0" are matched.

- Determines whether to use the full clone

    If you specify the `--full` flag, you can clone the official mirror fully.

    > **Note:**
    >
    > If `--full`, `global-version` flags, and the component versions are not specified, only some meta information is cloned.

- Determines whether to clone packages from the specific platform

    If you want to clone packages only for a specific platform, use `-os` and `-arch` to specify the platform. For example:

    - Execute the `tiup mirror clone <target-dir> [global-version] --os=linux` command to clone for linux.
    - Execute the `tiup mirror clone <target-dir> [global-version] --arch=amd64` command to clone for amd64.
    - Execute the `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64` command to clone for linux/amd64.

- Determines whether to clone a specific version of a package

    If you want to clone only one version (not all versions) of a component, use `--<component>=<version>` to specify this version. For example:

    - Execute the `tiup mirror clone <target-dir> --tidb v5.3.0` command to clone the v5.3.0 version of the TiDB component.
    - Execute the `tiup mirror clone <target-dir> --tidb v5.3.0 --tikv all` command to clone the v5.3.0 version of the TiDB component and all versions of the TiKV component.
    - Execute the `tiup mirror clone <target-dir> v5.3.0` command to clone the v5.3.0 version of all components in a cluster.

The cloning sets up signing keys as part of the cloning. It is not needed to do this manually.

### Using the private repo

The repository that is cloned using `tiup mirror clone` can be shared among hosts either by sharing the files via SCP, NFS or by making the repository available over the HTTP or HTTPS protocol. Use `tiup mirror set <location>` to specify the location of the repository.

```bash
tiup mirror set /shared_data/tiup
```

```bash
tiup mirror set https://tiup-mirror.example.com/
```

> **Note:**
>
> On the machine on which you use `tiup mirror clone` setting the mirror will also change the mirror you are cloning from, so you need to reset this by running `tiup mirror set --reset` before updating the private mirror.

Another way of using a mirror is to use the `TIUP_MIRRORS` environment variable. Here is an example for running `tiup list` with a private repository.

```bash
export TIUP_MIRRORS=/shared_data/tiup
tiup list
```

Using `TIUP_MIRRORS` can permanently change the mirror configuration, just like `tiup mirror set`. For details see [tiup issue #651](https://github.com/pingcap/tiup/issues/651).

### Updating a private repo

When running `tiup mirror clone` a second time with the same `target-dir` it will create new manifests and download newly available versions of components if applicable. It will skip downloading existing component versions.

> **Note:**
> 
> As the manifest will be re-created make sure to include all components an all versions (including older ones that were previously downloaded) as otherwise they will be excluded from the manifest.

## Custom repository

A custom repository can be used with TiDB components like TiDB, TiKV or PD that you build yourself. It is also possible to create your own tiup components.

Creating your own components can be done with the `tiup package` command. The instructions for how to do this can be found [here](https://github.com/pingcap/tiup/blob/master/doc/user/package.md).

### Creating a custom repository

To create an empty repository in `/data/mirror`:

```bash
tiup mirror init /data/mirror
```

As part of creating the repository keys will be written to `/data/mirror/keys`.

To create a new private key in `~/.tiup/keys/private.json`:

```bash
tiup mirror genkey
```

Grant `jdoe` with private key `~/.tiup/keys/private.json` ownership of `/data/mirror`

```bash
tiup mirror set /data/mirror
tiup mirror grant jdoe
```

### Working with custom components

First we create a custom component called hello.

```bash
$ cat > hello.c << END
> #include <stdio.h>
int main() {
  printf("hello\n");
  return (0);
}
END
$ gcc hello.c -o hello
$ tiup package hello --entry hello --name hello --release v0.0.1
```

This creates `package/hello-v0.0.1-linux-amd64.tar.gz`.

Then we create a new repository, a private key and then grant ownership to the repository.

```bash
$ tiup mirror init /tmp/m
$ tiup mirror genkey
$ tiup mirror set /tmp/m
$ tiup mirror grant $USER
```

```bash
tiup mirror publish hello v0.0.1 package/hello-v0.0.1-linux-amd64.tar.gz hello
```

And finally we run the component, if it wasn't installed yet it will be downloaded.

```bash
$ tiup hello
```

```
The component `hello` version  is not installed; downloading from repository.
Starting component `hello`: /home/dvaneeden/.tiup/components/hello/v0.0.1/hello
hello
```

With `tiup mirror merge` you can merge a repository with custom components into another one. This assumes that all components in `/data/my_custom_components` are signed by the current `$USER`.

```bash
$ tiup mirror set /data/my_mirror
$ tiup mirror grant $USER
$ tiup mirror merge /data/my_custom_components
```