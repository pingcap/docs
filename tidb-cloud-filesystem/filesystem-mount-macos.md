---
title: 在 macOS 上挂载文件系统
summary: 了解如何在 macOS 上使用 WebDAV 或 macFUSE 挂载 TiDB Cloud 文件系统、验证文件访问并安全卸载。
---

# 在 macOS 上挂载文件系统

在 macOS 上，你可以将 TiDB Cloud 文件系统挂载为本地目录，并使用常用的应用程序和工具访问其中的文件。请选择以下挂载方式之一：

- **WebDAV**：推荐用于大多数工作流。无需额外安装挂载软件。
- **macFUSE**：支持挂载 layer 或 checkpoint、创建本地只读挂载，以及在不卸载文件系统的情况下刷写待处理写入。你需要安装 [macFUSE](https://macfuse.github.io/)。

如果你未指定 `--driver` 选项，TiDB Cloud CLI (`ti`) 在 macOS 上会使用 WebDAV 挂载文件系统，即使已安装 macFUSE 也是如此。要使用 FUSE，请指定 `--driver fuse`。挂载 layer 和 checkpoint 始终需要 FUSE。本指南中的示例都会显式指定 `--driver`，以便你清楚使用的是哪种挂载方式。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 已有一个现成的 TiDB Cloud 文件系统。如果还没有，请参见[创建并使用文件系统](/tidb-cloud-filesystem/filesystem-quick-start.md#step-3-create-and-use-a-file-system)。
- 确保 `ti` 已配置为使用有效 Token 访问文件系统。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

    要列出和读取文件，你的 Token 需要对远程目录具有 `list` 和 `read` 权限。创建或修改文件还需要 `write`；删除文件需要 `delete`。下面的 WebDAV 验证过程使用所有者 Token，或具有这四种权限的范围受限 Token。对于只读访问，请参见[使用 WebDAV 进行只读访问](/tidb-cloud-filesystem/filesystem-mount-macos.md#use-webdav-for-read-only-access)。

## 使用 WebDAV 挂载 {#mount-with-webdav}

对于大多数工作流，使用 WebDAV 挂载文件系统即可，无需安装额外的挂载软件。

请使用 Bash 或 Zsh，并在整个 WebDAV 操作过程中保持同一个 shell 会话打开，以便示例中的变量始终可用。

1. 准备本地挂载目录。如果 `$HOME/workspace` 上已经挂载了文件系统，请在复用该目录前先卸载：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    然后，如果目录不存在则创建它：

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. 选择远程目录，并上传一个小的示例文件以验证远程读取。如果你的 Token 仅授予对某个特定远程目录的访问权限，请将下面的 `/` 替换为该目录，例如 `/workspace`：

    ```bash
    remote_path="/"
    test_file="mount-check-$(date +%s)-$$.txt"
    printf 'Hello from the service\n' | ti fs copy-file \
      --from-stdin --to-remote "${remote_path%/}/$test_file"
    ```

    生成的文件名有助于避免覆盖现有文件。仅在上传成功后继续。

3. 使用 WebDAV 挂载文件系统：

    ```bash
    ti fs mount-file-system \
      --remote-path "$remote_path" \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    所选远程目录会成为本地挂载的根目录。例如，如果 `remote_path="/workspace"`，则可以通过 `$HOME/workspace` 访问远程 `/workspace` 目录。详情请参见[仅挂载文件系统的一部分](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system)。

    挂载会在后台运行，直到你将其卸载。关闭终端不会卸载它。

4. 通过本地挂载列出文件并读取已上传的示例文件：

    ```bash
    ls "$HOME/workspace"
    cat "$HOME/workspace/$test_file"
    ```

    `cat` 的预期输出：

    ```text
    Hello from the service
    ```

    仅查看目录列表并不能确认文件读取功能正常。如果某个文件操作耗时超过 30 秒，请使用 Ctrl+C 中断，并在继续之前参见[挂载成功，但文件访问假死](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs)。

    读取成功后，通过挂载点修改该示例文件：

    ```bash
    printf 'Hello from macOS\n' > "$HOME/workspace/$test_file"
    ```

5. 完成后，先停止应用程序向挂载点写入，关闭已打开的文件，然后卸载文件系统：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    WebDAV 不支持 `drain-file-system`。如果卸载失败，请保留机器和本地挂载数据可用，并在继续之前参见[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。

6. 成功卸载后，验证修改是否已同步到服务端：

    ```bash
    ti fs read-file --path "${remote_path%/}/$test_file"
    ```

    预期输出：

    ```text
    Hello from macOS
    ```

    验证成功后，删除该示例文件：

    ```bash
    ti fs delete-file --path "${remote_path%/}/$test_file"
    ```

卸载只会移除本地挂载，不会删除文件系统或其中的数据。

> **Note:**
>
> 在 Finder 中浏览挂载点时，无论使用 WebDAV 还是 FUSE，都可能会在文件系统中创建 `.DS_Store` 文件和 `._` 伴生文件。这些文件在卸载后仍会保留、占用存储空间、计入文件数量，并且对有权访问同一路径的用户可见。
>
> 如果你不想保留这些文件，请从对应的远程目录中删除它们。例如，对于文件系统根目录：
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### 使用 WebDAV 进行只读访问 {#use-webdav-for-read-only-access}

WebDAV 不支持 `--read-only` 选项。

要通过 WebDAV 强制实现只读访问，请使用仅具有 `read` 和 `list` 权限的范围受限 Token，并在不使用 `--read-only` 的情况下正常挂载。该 Token 会在服务端强制执行只读访问。

示例请参见[挂载共享目录](/tidb-cloud-filesystem/filesystem-sharing.md#mount-the-shared-directory-optional)。

如果你需要让本地挂载本身就是只读的，请使用 macFUSE 并指定 `--driver fuse --read-only`。

## 使用 macFUSE 挂载 {#mount-with-macfuse}

当你需要以下 FUSE 功能时，请使用 FUSE 而不是 WebDAV：

- 挂载 layer 或 checkpoint。
- 创建本地只读挂载。
- 在保持挂载运行的同时，使用 `drain-file-system` 刷写待处理写入。

要在 macOS 上使用 macFUSE 挂载文件系统，请按以下步骤操作：

1. 安装 [macFUSE](https://macfuse.github.io/)，并完成你的 macOS 版本所需的所有安装或安全批准步骤。

    安装 `ti` 不会安装 macFUSE。

2. 准备本地挂载目录。如果 `$HOME/workspace` 上已经挂载了文件系统，请先卸载后再复用该目录：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    然后，如果目录不存在，则创建该目录：

    ```bash
    mkdir -p "$HOME/workspace"
    ```

3. 根据你需要的远程目录和访问模式选择 FUSE 挂载命令。只运行符合你需求的命令。

    要使用 FUSE 挂载文件系统根目录，请执行：

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    挂载会在后台运行，直到你将其卸载。关闭终端不会将其卸载。

    运行 FUSE 挂载以及访问该挂载的应用程序时，应使用同一个操作系统用户。

    如果你的 Token 仅被授权访问某个特定远程目录，请使用 `--remote-path` 指定该目录。例如，要挂载 `/workspace` 而不是文件系统根目录，请使用：

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    更多信息，请参见[仅挂载文件系统的一部分](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system)。

    要将本地挂载设为只读，请在所选挂载命令中添加 `--read-only`。例如，要以只读方式挂载文件系统根目录，请使用：

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse \
      --read-only
    ```

    layer 和 checkpoint 挂载必须使用 FUSE，并且 checkpoint 挂载始终为只读。详情请参见[管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)。

4. 完成后，先停止应用程序向挂载写入，关闭已打开的文件，然后卸载：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    成功的 FUSE 卸载会刷写待处理写入。正常卸载前无需运行 `drain-file-system`。如果挂载日志报告 `force_quit` 或待处理写入，请参见 [FUSE 写入行为](/tidb-cloud-filesystem/filesystem-mount.md#fuse-write-behavior)。

卸载会移除本地挂载，但不会删除文件系统或其中的数据。

> **Note:**
>
> 在 Finder 中浏览挂载（无论是 WebDAV 还是 FUSE）时，可能会在文件系统中创建 `.DS_Store` 文件和 `._` 伴生文件。这些文件在卸载后仍会保留，会占用存储空间，会计入文件数量，并且对有权访问相同路径的用户可见。
>
> 如果你不想保留这些文件，请从对应的远程目录中删除它们。例如，对于文件系统根目录：
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### 在不卸载的情况下刷写 FUSE 写入 {#flush-fuse-writes-without-unmounting}

如果你需要让待处理写入到达文件系统，同时保持 FUSE 挂载继续运行，请先停止应用程序向相关文件写入，并关闭这些文件。然后对刷写该挂载：

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

成功刷写表示待处理写入已经到达文件系统，同时挂载仍保持运行。

如果刷写超时或返回错误，请保持挂载和机器可用，解决错误，并在结束会话或将这些修改提供给其他用户或环境之前验证这些文件。

WebDAV 不支持 `drain-file-system`。命令语法请参见 [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md)。

## 挂载问题排查 {#troubleshoot-mount-issues}

如果 WebDAV 挂载启动失败：

- 确保本地挂载目录存在且可写。
- 确保没有其他挂载已在使用同一个本地目录。
- 检查 `ti` 报告的诊断日志路径，以查看底层错误。

如果 FUSE 挂载启动失败：

- 确保已安装 macFUSE。
- 完成 macFUSE 所需的所有 macOS 安全批准步骤。
- 确保挂载和访问它的应用程序以同一个操作系统用户运行。
- 确保没有其他挂载已在使用同一个本地目录。
- 检查 `ti` 报告的诊断日志路径。

如果某个文件操作耗时超过 30 秒，请使用 Ctrl+C 中断它，并参见[挂载成功，但文件访问假死](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs)。

如果卸载失败，请保持挂载进程和机器继续运行，直到你解决错误并验证所需文件已到达文件系统。在待处理写入可能仍然存在时，不要移除本地挂载数据。

有关更多挂载错误，请参见[排查 TiDB Cloud Filesystem 问题](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。

## 后续操作 {#what-s-next}

- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)，了解只读挂载、仅挂载文件系统的一部分以及其他常见挂载选项。
- [管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)，了解如何通过 FUSE 使用 layers 和 checkpoints。
- [跨机器共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)，为其他用户或环境提供对文件系统的访问。