---
title: 在 Linux 上挂载文件系统
summary: 安装 FUSE 用户态工具，在 Linux 上挂载文件系统，验证访问，并排查常见的挂载权限问题。
---

# 在 Linux 上挂载文件系统

在 Linux 上，TiDB Cloud Filesystem 使用 FUSE 通过本地目录提供文件系统数据。挂载文件系统后，应用程序和工具可以使用普通的本地文件路径访问该文件系统。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口如有变更，恕不另行通知。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 让 `ti` 可以访问该文件系统及其 Token。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。
- 使用可以安装 `fuse3` 软件包的 Linux 主机。对于容器，请改为参考 [Docker and Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md)。

请以同一个操作系统用户运行挂载命令以及访问该挂载的应用程序。

## 安装 FUSE 用户态工具 {#install-fuse-userspace-tools}

1. 在 Ubuntu 或 Debian 上，安装 `fuse3` 软件包：

    ```bash
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends fuse3
    ```

2. 检查是否已安装 FUSE 挂载辅助程序：

    ```bash
    command -v fusermount3
    ```

    该命令会输出 `fusermount3` 的路径，例如：

    ```text
    /usr/bin/fusermount3
    ```

3. 检查 FUSE 设备是否可用：

    ```bash
    ls -l /dev/fuse
    ```

    该命令会显示 `/dev/fuse` 的条目。

如果找不到 `fusermount3`，请确认已安装 `fuse3` 软件包。如果 `/dev/fuse` 不存在，或者挂载时无法使用它，请联系主机管理员启用 FUSE 并为你的用户授予该设备的访问权限。

在其他 Linux 发行版上，请安装提供 `fusermount3` 的 FUSE 软件包，并执行相同的检查。

## 挂载并验证文件系统 {#mount-and-verify-the-file-system}

1. 为挂载创建一个本地目录：

    ```bash
    mkdir -p "$HOME/workspace"
    ```

    请使用与运行访问该挂载的应用程序相同的操作系统用户所拥有的目录。

2. 挂载文件系统：

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    在 Linux 上，`ti` 默认使用 FUSE。

    该命令会等待挂载就绪后再返回。命令返回后，挂载会继续在后台运行，因此关闭终端不会将其卸载。

    挂载成功后，你可以通过 `$HOME/workspace` 访问该文件系统。

    如果你的文件系统 Token 仅授权访问特定的远程路径，请使用以下命令替代前面的挂载命令：

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace"
    ```

    在此示例中，远程 `/workspace` 目录会成为本地挂载的根目录。更多信息，请参见[仅挂载文件系统的一部分](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system)。

    如需阻止通过本地挂载进行写入，请在挂载命令中添加 `--read-only`。例如，将文件系统根目录以只读方式挂载：

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --read-only
    ```

    `--read-only` 选项仅影响此本地挂载。如需在文件系统服务层面强制只读访问，请使用具有只读权限的范围受限 Token。

3. 验证你是否可以访问已挂载的文件系统：

    ```bash
    ls "$HOME/workspace"
    ```

    该命令会列出挂载路径根目录下的文件和目录。

    如果你使用的是可写挂载，并且你的 Token 具有写权限，也可以创建并读取一个测试文件：

    ```bash
    TEST_FILE="mount-check-$(date +%s).txt"

    printf 'Hello from Linux\n' > "$HOME/workspace/$TEST_FILE"
    cat "$HOME/workspace/$TEST_FILE"
    ```

    输出示例：

    ```text
    Hello from Linux
    ```

4. 完成后，请停止向挂载目录写入的应用程序，关闭打开的文件，然后卸载文件系统：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    成功卸载会在停止挂载前刷写待处理的 FUSE 写入。

    如果你创建了上述测试文件，也可以在卸载后选择验证该文件是否可直接从文件系统中访问：

    ```bash
    ti fs read-file --path "/$TEST_FILE"
    ```

    输出示例：

    ```text
    Hello from Linux
    ```

卸载会移除本地挂载，但不会删除文件系统或其中的数据。

> **Warning:**
>
> 如果卸载失败，请保持挂载和机器继续运行，直到你解决错误并验证所需文件已到达文件系统。某些待处理写入可能仍然只存在于该机器上。

## 在不卸载的情况下刷写 FUSE 写入 {#flush-fuse-writes-without-unmounting}

如果你需要在保持挂载运行的同时让待处理写入到达文件系统，请先停止应用程序向相关文件写入并关闭这些文件。然后对刷写该挂载：

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

成功刷写表示待处理写入已到达文件系统，同时挂载仍保持运行。如果刷写超时或返回错误，请保持挂载和机器可用，解决错误，并在结束会话或通知其他用户修改已就绪之前验证这些文件。命令语法请参见 [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md)。

## 排查挂载权限错误 {#troubleshoot-mount-permission-errors}

如果挂载因 `Permission denied` 失败，请按顺序检查以下内容：

1. 确保当前用户对挂载目录具有写权限：

    ```bash
    ls -ld "$HOME/workspace"
    ```

2. 确保 `/dev/fuse` 存在：

    ```bash
    ls -l /dev/fuse
    ```

3. 确保你是以将要运行应用程序的同一个操作系统用户来创建挂载。

    不要以 `root` 身份创建 FUSE 挂载，然后再尝试通过更改挂载目录的所有权来让其他用户访问。应当直接以应用程序用户创建挂载。

4. 检查是否已有其他挂载正在使用相同路径：

    ```bash
    mount | grep "$HOME/workspace"
    ```

    如果列出了某个挂载，请先使用 `ti fs unmount-file-system --mount-path "$HOME/workspace"` 或 `fusermount3 -u "$HOME/workspace"` 将其卸载，然后再创建新的挂载。

5. 如果 `ti` 报告了诊断日志路径，请检查该日志以查看底层错误。

在具有额外安全控制的系统上，例如 AppArmor，即使目录权限看起来正确，操作系统也可能拒绝挂载。

有关更多挂载错误，请参见[排查 TiDB Cloud Filesystem 问题](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。

## Ubuntu 26.04 挂载路径限制 {#ubuntu-2604-mount-path-restrictions}

在 Ubuntu 26.04 上，`fusermount3` 的 AppArmor 配置（Profile）可能会阻止在某些路径上进行 FUSE 挂载。特别是，像 `/workspace` 这样的顶层目录即使文件权限看起来正确，也可能因 `Permission denied` 而挂载失败。

对于本指南中的命令，请使用 `$HOME/workspace` 作为挂载目录，而不要使用 `/workspace`。

将 `/workspace` 的所有者改为其他用户，或以 `root` 身份执行挂载，都无法绕过 AppArmor 的限制。

如果你的应用明确要求使用 `/workspace`，请让主机管理员在 `/etc/apparmor.d/local/fusermount3` 中允许该路径：

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

然后，管理员可以重新加载 AppArmor 配置：

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

配置更新后，请重试在 `/workspace` 上执行挂载。

如需帮助检查失败是否由 AppArmor 导致，请参见[Ubuntu 26.04 拒绝在 `/workspace` 下进行 FUSE 挂载](/tidb-cloud-filesystem/filesystem-troubleshooting.md#ubuntu-2604-rejects-a-fuse-mount-under-workspace)。

## 后续操作 {#what-s-next}

- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)，了解只读挂载、挂载 layer 或 checkpoint，以及其他常见挂载选项。
- [管理文件系统的 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)，了解如何挂载并使用 layer 或 checkpoint。
- [跨机器共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)，为其他用户或环境授予对文件系统的访问权限。