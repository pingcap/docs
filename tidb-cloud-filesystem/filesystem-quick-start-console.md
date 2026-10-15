---
title: 通过控制台开始使用 TiDB Cloud Filesystem
summary: 在 TiDB Cloud 控制台中创建一个文件系统，从你的计算机连接到它，写入一个测试文件，并在控制台中查看该文件。
---

# 通过控制台开始使用 TiDB Cloud Filesystem

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) 是一个持久化、共享的云文件系统，适用于应用程序、自动化流程和 AI 代理。文件可独立于创建它们的机器或进程持续可用，因此你可以在不同会话和环境之间复用同一个工作空间。

本快速入门将引导你了解如何通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 创建一个文件系统，将其挂载到 macOS 或 Linux 计算机上，写入一个测试文件，并在控制台中查看其元信息。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 第 1 步：创建文件系统 {#step-1-create-a-file-system}

1. 如果你还没有 TiDB Cloud 账户，请先[注册一个账户](https://tidbcloud.com/free-trial)。
2. 使用你的 TiDB Cloud 账户登录 [TiDB Cloud 控制台](https://tidbcloud.com/)。
3. 在左侧导航栏中，选择你的组织，然后点击 **File Systems**。
4. 在右上角，点击 **Create File System**。
5. 在 **Create File System** 页面，输入文件系统名称，并选择云服务提供商和区域。查看摘要中的使用限制。

    > **Tip:**
    >
    > 对于未绑定信用卡的组织，文件系统限制是固定的。要修改使用限制，请为你的组织添加信用卡。更多信息，请参见[管理 TiDB Cloud Filesystem 使用限制](/tidb-cloud-filesystem/manage-filesystem-limits.md)。

6. 点击 **Create**。当出现 **Your File System is Ready!** 对话框时，请保持该对话框打开，以便进行下一步。

## 第 2 步：挂载文件系统 {#step-2-mount-the-file-system}

在 macOS 或 Linux 上，按照 **Your File System is Ready!** 对话框中的步骤安装 TiDB Cloud CLI 并挂载文件系统。在 Windows 上，请参见[通过 CLI 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)，无需挂载即可操作文件。

1. 安装 TiDB Cloud CLI `ti`。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh
    ```

2. 复制并在同一个 shell 中运行 **Mount Your File System** 下方的命令。该命令会将 `ti` 添加到 `PATH`，设置 `TI_FS_TOKEN`，创建 `~/tidbcloudfs` 目录，并将文件系统挂载到该目录。

    > **Note:**
    >
    > - 挂载命令会在 `TI_FS_TOKEN` 中包含[默认所有者 Token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens)。该 Token 授予对文件系统的完全访问权限，并且只会显示一次。请妥善保存。不要将该命令或 Token 放入日志、issue、聊天消息或源代码管理中。
    > - 在 Linux 上，挂载需要 `fuse3` 以及对 `/dev/fuse` 的访问权限。如有需要，请先按照[安装 FUSE 用户态工具](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools)中的说明操作，再运行挂载命令。

3. 复制并运行 **Start Using It** 下方的命令，以列出已挂载的目录。
4. 点击 **Done** 以打开文件系统概览页面。

你可以在概览页面点击 **Connect** 重新打开连接指引，但之后无法再次获取默认所有者 Token。

## 第 3 步：写入并查看文件 {#step-3-write-and-view-a-file}

挂载文件系统后，使用挂载目录写入并读取一个测试文件。

在挂载目录中写入文件：

```bash
echo 'Hello from TiDB Cloud Filesystem' > ~/tidbcloudfs/hello.txt
cat ~/tidbcloudfs/hello.txt
```

在文件系统左侧导航栏中，点击 **Files**。根目录中会列出 `hello.txt`。你可以搜索该文件，或点击其名称查看其元信息。控制台会显示文件信息，但读取文件内容和修改文件需要使用 TiDB Cloud CLI `ti` 或通过挂载来完成。

## （可选）第 4 步：卸载文件系统 {#optional-step-4-unmount-the-file-system}

如果你不再需要通过挂载目录访问该文件系统，可以将其卸载：

```bash
ti fs unmount-file-system --mount-path ~/tidbcloudfs
```

在 Linux 上，FUSE 可能会在本地缓冲写入，直到成功卸载为止。如果卸载失败，请在离开该机器或删除其本地缓存之前，先按照[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)中的说明操作。

## 后续操作 {#what-s-next}

- [管理文件系统](/tidb-cloud-filesystem/manage-filesystem-resources.md)：检查、重命名或删除文件系统。
- [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)：创建具有受限访问权限的 Token。
- [通过 CLI 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)：了解仅使用 CLI 的创建流程。