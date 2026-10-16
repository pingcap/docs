---
title: 通过 CLI 开始使用 TiDB Cloud Filesystem
summary: 了解如何创建持久化的 TiDB Cloud 文件系统、读写文件，以及可选地通过本地挂载访问这些文件。
---

# 通过 CLI 开始使用 TiDB Cloud Filesystem

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) 是一个持久化、共享的云文件系统，适用于应用程序、自动化流程和 AI 代理。文件可独立于创建它们的机器或进程持续可用，因此你可以在不同会话和环境之间复用同一个工作空间。

本快速入门将指导你如何通过 TiDB Cloud CLI 创建文件系统、写入和读取文件，以及可选地将其挂载为本地目录。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

开始之前，请先在 [TiDB Cloud console](https://tidbcloud.com/) 的 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 TiDB Cloud API 公钥和私钥。这些密钥必须为你的组织授予 `Organization Owner` 访问权限。

如果已经有人向你提供了文件系统 Token，请跳过资源创建步骤，直接参考[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

在 macOS 和 Linux 上使用 Bash 或 Zsh，在 Windows 上使用 PowerShell。在整个教程过程中，请保持使用同一个 shell。如果代理会为每条命令启动一个新的 shell，请将环境变量和保存的路径值传递给每个 shell。

## Step 1. 安装 TiDB Cloud CLI {#step-1-install-tidb-cloud-cli}

选择你的操作系统：

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. 安装 TiDB Cloud CLI：

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. 将 `ti` 添加到当前 shell，并检查版本：

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    ti --version
    ```

3. 如需让 `ti` 在新终端中也可用，请将其添加到你的 shell 配置文件中。对于 Zsh：

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    ```

    对于 Bash，请将相同的 `export` 行添加到你的终端所使用的启动文件中，Linux 上通常是 `~/.bashrc`，macOS 上通常是 `~/.bash_profile`。

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. 安装 TiDB Cloud CLI：

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. 将 `ti` 添加到当前 PowerShell 会话，并检查版本：

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"

    ti --version
    ```

</div>

</SimpleTab>

如需了解 Windows 上永久设置 `PATH` 的方法及其他安装选项，请参见[安装、配置和更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。

## Step 2. 配置 TiDB Cloud CLI {#step-2-configure-tidb-cloud-cli}

选择一个你希望存储文件的[支持的区域](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions)，例如 `aws-us-west-2`。免费套餐允许每个 Region 创建一个文件系统。如果你的组织在该 Region 中已经有一个文件系统，请[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)、选择另一个 Region，或[添加支付方式](https://tidbcloud.com/org-settings/billing/payments)。

1. 运行交互式配置：

    ```bash
    ti configure
    ```

2. 提供以下信息：

    - 你选择的 Region。
    - 你的 TiDB Cloud API 公钥和私钥。

CLI 会将你的凭证和默认 Region 保存在本地。下一步中的创建命令会使用该 Region。

> **Tip:**
>
> 对于 CI 或代理，建议改用非交互式配置。请从 Secret 管理器中注入 `TIDB_CLOUD_PUBLIC_KEY` 和 `TIDB_CLOUD_PRIVATE_KEY`，设置 `TI_REGION_CODE`，然后运行 `ti configure --non-interactive`。更多信息，请参见[为自动化配置](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation)。

## Step 3. 创建并使用文件系统 {#step-3-create-and-use-a-file-system}

1. 创建文件系统：

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait
    ```

    复制返回的 `file_system_id`，供下一步使用。CLI 会在本地保存该文件系统的所有者 Token 和 Region，因此在同一台机器上你无需再次输入 Token。

    > **Note:**
    >
    > 如果你需要从另一台机器访问该文件系统，还需要保存返回的 `fs_token` 和 `region_code`。所有者 Token 拥有完整访问权限且不会过期，因此请妥善保管。若需受限访问，请参见[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

2. 选择你的新文件系统。将 `<file-system-id>` 替换为返回的 `file_system_id`：

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    $env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
    ```

    </div>

    </SimpleTab>

3. 创建目录、上传示例文件，并将其读回：

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    ti fs create-directory --path /quick-start
    printf 'Hello from TiDB Cloud Filesystem\n' | ti fs copy-file \
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    ti fs create-directory --path /quick-start
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    </SimpleTab>

    `read-file` 的预期输出如下：

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    现在，你的第一个文件已经存储在 TiDB Cloud Filesystem 中。若要从其他环境访问它，请参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。若要向其他用户、应用程序或代理提供访问权限，请参见[共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)。

## 第 4 步：挂载文件系统（可选） {#step-4-mount-the-file-system-optional}

如果你的应用需要本地文件路径，请挂载文件系统。Windows 不支持挂载。如果你使用的是 Windows，或者只需要 CLI 访问，请跳转到[第 5 步](#step-5-clean-up-the-example-optional)。

1. 为挂载创建一个空的本地目录：

    ```bash
    mount_dir="$(mktemp -d "$HOME/ti-fs-quick-start.XXXXXX")"
    ```

2. 使用适用于你的操作系统的命令挂载 `/quick-start` 目录：

    <SimpleTab>

    <div label="macOS WebDAV">

    此命令使用 macOS 内置的 WebDAV 支持：

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver webdav
    ```

    </div>

    <div label="Linux FUSE">

    Linux 需要 `fuse3` 软件包以及对 `/dev/fuse` 的访问权限。如有需要，请先参考[安装 FUSE 用户态工具](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools)，再运行挂载命令。

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver fuse
    ```

    </div>

    </SimpleTab>

3. 使用本地路径读取你的文件：

    ```bash
    cat "$mount_dir/hello.txt"
    ```

    预期输出：

    ```text
    Hello from TiDB Cloud Filesystem
    ```

有关写入验证和故障排查，请参见[在使用挂载前进行验证](/tidb-cloud-filesystem/filesystem-mount.md#verify-a-mount-before-using-it)。

## 第 5 步：清理示例（可选） {#step-5-clean-up-the-example-optional}

如果你在第 4 步中挂载了目录，请先关闭正在使用该目录的应用，然后卸载并删除空的本地挂载目录：

```bash
ti fs unmount-file-system --mount-path "$mount_dir"
rmdir "$mount_dir"
```

如果卸载失败，请先按照[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)中的说明操作，再继续后续步骤。

删除示例目录及其文件。此命令适用于所有受支持的操作系统：

```shell
ti fs delete-file --path /quick-start --recursive
```

该文件系统及其 Token 仍可继续复用。要删除整个文件系统，请参见[删除文件系统](/tidb-cloud-filesystem/manage-filesystem-resources.md#delete-a-file-system)。

## 后续操作 {#what-s-next}

- [访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)，以复用本地存储的凭据或从其他环境连接。
- [为自动化进行配置](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation)，为 CI 作业或代理设置 CLI 凭据。
- [在 TiDB Cloud Filesystem 中管理文件系统](/tidb-cloud-filesystem/manage-filesystem-resources.md)，以检查和管理你的文件系统。
- [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)，以创建、检查和管理用于访问文件系统的 Token。
- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)，以通过本地目录访问其中的文件。
- [共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)，以便另一台机器、用户、应用或代理也能访问相同的文件。
- [管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)，以隔离、审查并应用文件变更。