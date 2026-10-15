---
title: 挂载文件系统
summary: 了解何时挂载文件系统、应使用哪种挂载方法，以及文件系统挂载的能力和限制。
aliases: ['/zh/ai/mount-filesystem']
---

# 挂载文件系统

在 TiDB Cloud Filesystem 中，当编辑器、应用程序、agent 或其他工具需要本地文件路径时，你可以将文件系统挂载为本地目录。挂载后，这些工具就可以通过本地文件操作来读写远程文件。

如果只需通过 CLI 访问，请使用 [`ti fs` 命令](/tidb-cloud-filesystem/work-with-filesystem-data.md) 来读取、复制、整理和搜索文件，而无需挂载。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 选择挂载方法 {#choose-a-mount-method}

可用的挂载方法取决于你的环境：

| 环境 | 挂载方法 | 指南 |
| --- | --- | --- |
| Linux | FUSE | [在 Linux 上挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-linux.md) |
| macOS | 一般文件访问使用 WebDAV，或使用 macFUSE 的 FUSE 以支持 FUSE 特有功能 | [在 macOS 上挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-macos.md) |
| Linux 上的 Docker | FUSE，需要访问 `/dev/fuse` 并授予额外的容器权限 | [在 Docker 中挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-docker.md) |

Windows 不支持原生文件系统挂载。在 Windows 上，请改用直接命令，例如 `ti fs copy-file`、`ti fs read-file` 和 `ti fs list-files`。

在 macOS 上，WebDAV 足以满足一般文件访问需求，且不需要额外的挂载软件。对于挂载 layer 或 checkpoint、使用 `--read-only` 创建本地只读挂载，以及使用 `drain-file-system` 等功能，则必须使用 FUSE。

## 不配置 profile 直接使用 Token {#use-a-token-without-configuring-a-profile}

有了文件系统 Token 和 Region 后，你无需配置 `ti` 配置（Profile），也无需提供 TiDB Cloud API key，即可访问文件：

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

然后按照适用于你环境的指南进行操作。该 Token 用于标识文件系统，并限制当前环境可访问的路径和可执行的操作。请将该 Token 视为 Secret 妥善保管。

## 常见挂载能力 {#common-mount-capabilities}

文件系统挂载支持多种选项，可改变通过本地挂载暴露的内容：

### 仅挂载文件系统的一部分 {#mount-only-part-of-the-file-system}

默认情况下，挂载会暴露文件系统根目录 `/`。你可以改用 `--remote-path` 来仅暴露特定的远程目录。当范围受限 Token 只授权访问某个特定路径时，这种方式也很有用。

### 创建只读挂载 {#create-a-read-only-mount}

使用 `--driver fuse --read-only` 可防止通过 FUSE 挂载进行写入。WebDAV 不支持此选项。若要在挂载和 CLI 命令之间统一强制只读访问，请使用仅具有 `read` 和 `list` 权限的范围受限 Token。挂载选项不会改变 Token 权限。

### 挂载 layer 和 checkpoint {#mount-layers-and-checkpoints}

layer 和 checkpoint 需要使用 FUSE。checkpoint 挂载始终为只读。

有关 layer 和 checkpoint 的工作流，请参见[管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)。

## 使用前验证挂载 {#verify-a-mount-before-using-it}

挂载命令成功执行或目录列表能够显示，并不能证明文件读写一定正常。请读取一个已通过 `ti fs copy-file` 上传的已知小文件。对于可写挂载，请写入一个新的测试文件，关闭该文件，并成功卸载挂载。然后通过 `ti fs read-file` 读取该文件，以确认写入已到达服务端。完整示例请参见 [Linux 验证步骤](/tidb-cloud-filesystem/filesystem-mount-linux.md#mount-and-verify-the-file-system) 或 [macOS WebDAV 验证步骤](/tidb-cloud-filesystem/filesystem-mount-macos.md#mount-with-webdav)。

如果小文件检查在 30 秒后仍未返回，请中断该操作，并按照[挂载成功，但文件访问假死](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs)进行排查。在验证通过之前，不要在该挂载上启动应用程序。

## 安全结束使用 {#finish-safely}

### 完成后卸载 {#unmount-when-you-are-finished}

停止应用程序向挂载目录写入，关闭已打开的文件，并按照你的平台指南运行 `ti fs unmount-file-system`。正常的 FUSE 卸载会在停止挂载前刷写待处理的写入。在移除机器或其本地缓存之前，请通过直接 CLI 读取来验证所需文件。卸载只会移除本地挂载，不会删除文件系统或其中的数据。

### FUSE 写入行为 {#fuse-write-behavior}

FUSE 挂载在将写入发送到服务之前，可能会先在本地进行缓冲。正常卸载已包含刷写，因此你无需先运行 `drain-file-system`。如果挂载日志在卸载后报告 `force_quit` 或仍有待处理写入，请按照[卸载返回成功但挂载进程异常退出](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally)进行处理。

仅当你需要在保持挂载运行的同时，让待处理写入到达文件系统时，才使用 `drain-file-system`，例如在创建 checkpoint 之前，或在需要让另一个环境可访问已更新文件时。

WebDAV 挂载不支持 `drain-file-system`。

> **Warning:**
>
> 如果 FUSE 刷写或卸载失败，请保持挂载和机器可用，直到你解决错误并验证所需文件已到达文件系统。某些待处理写入可能仍然只存在于该机器上。

## 接下来做什么 {#what-s-next}

选择适用于你环境的指南：

- [在 Linux 上挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-linux.md)
- [在 macOS 上挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-macos.md)
- [在 Docker 中挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-docker.md)

有关所有挂载选项，请参见 [`mount-file-system` 命令参考](/ai/ti/reference/ti-fs-mount-file-system.md)。