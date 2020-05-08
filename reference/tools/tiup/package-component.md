---
title: Package a Component
summary: Learn how to package a component.
category: tools
---

# Package a Component

When you add a new component or add a version of an existing component, you need to use the `tar` command to package the component files and then upload it to the mirror repository. Packaging with `tar` is not difficult. However, it is hard to update the meta information of the repository, because you must avoid destroying the information about existing components during the update.

Therefore, TiUP provides the `package` component, which is used to package the new TiUP component and the directory for generating the component package.

Execute the following command to get the help documentation of the `mirrors` component:

{{< copyable "shell-root" >}}

```bash
tiup package --help
```

```
Package a tiup component and generate package directory

Usage:
  tiup package target [flags]

Flags:
  -C, -- string          Switch the directory before packaging with the tar command. Similar to `tar-C`.
      --arch string      The processor architecture (GOARCH, by default) the component is running on
      --desc string      Component description
      --entry string     Where the component binary files of the component are relative to the package
  -h, --help             Help information
      --hide tiup list   Hide the component from the tiup list
      --name string      Component name
      --os string        The operating system (GOOS, by default) the component is running on
      --release string   Component version
      --standalone       Whether the component can run independently (for example, PD can't, but the playground can)
```

## Usage example: Add the `Hello World` component

This section introduces the development and packaging of the `Hello World` component. The only function of this component is to output the content of its configuration file. The content is "Hello World".

For simplicity, use the bash script to develop this component. The following are the detailed instructions:

1. Create the configuration file for the `Hello World` component. The content is "Hello World".

    {{< copyable "shell-regular" >}}

    ```shell
    cat > config.txt << EOF
    Hello World
    EOF
    ```

2. Create an executable file:

    {{< copyable "shell-regular" >}}

    ```shell
    cat > hello.sh << EOF
    #! /bin/sh
    cat \${TIUP_COMPONENT_INSTALL_DIR}/config.txt
    EOF

    chmod 755 hello.sh
    ```

    The `TIUP_COMPONENT_INSTALL_DIR` environment variable is passed in by TiUP at run time. This variable points to the installation directory of the component.

3. Refer to [Create a Private Image](/reference/tools/tiup/mirrors.md) to create an offline or a private image (You cannot publish your package because currently you cannot use the `publish` feature of the official image). Make sure the `TIUP_MIRRORS` variable points to the image after the image is created.

4. Packaging:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup package hello.sh config.txt --name=hello --entry=hello.sh --release=v0.0.1
    ```

    You can create a `package` directory, where stores the packaged files and the meta information.

5. Upload to the repository:

    You can only upload to your image created in step 3, since currently you cannot publish to the official repository. Execute the following command to copy all files in the `package` directory into `<target-dir>` (in `tiup mirrors <target-dir>`).

    {{< copyable "shell-regular" >}}

    ```bash
    cp package/* path/to/mirror/
    ```

    If the directory created in step 3 happens to be in the current directory and the directory name is `package`, you do not need to copy it manually.

6. Check whether the `Hello World` component is created successfully:

    {{< copyable "shell-root" >}}

    ```bash
    tiup list hello --refresh
    ```

    ```
    Available versions for hello (Last Modified: 2020-04-23T16:45:53+08:00):
    Version  Installed  Release:                   Platforms
    -------  ---------  --------                   ---------
    v0.0.1              2020-04-23T16:51:41+08:00  darwin/amd64
    ```

    {{< copyable "shell-root" >}}

    ```bash
    tiup hello
    ```

    ```
    The component `hello` is not installed; downloading from repository.
    Starting component `hello`: /Users/joshua/.tiup/components/hello/v0.0.1/hello.sh
    Hello World
    ```
