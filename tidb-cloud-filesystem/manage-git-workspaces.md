---
title: 在 TiDB Cloud Filesystem 上管理 Git 工作树
summary: 了解如何将 Git 仓库克隆到已挂载的 TiDB Cloud Filesystem 中、加速大型仓库的初始化，以及管理链接工作树。
aliases: ['/zh/ai/manage-git-workspaces']
---

# 在 TiDB Cloud Filesystem 上管理 Git 工作树

将 Git 仓库克隆到 FUSE 挂载中，并使用常规 Git 命令进行操作。对于大型仓库，无 blob 克隆可让你在所有文件内容下载完成之前就开始工作。链接工作树可为不同分支提供独立的工作目录，而无需再次克隆。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 通过 FUSE [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)。WebDAV 挂载不支持 Git 工作树。
- 使已挂载的文件系统以及具有所需权限的 Token 可供 `ti` 使用。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。
- 安装 Git，并为你要使用的仓库配置身份验证。

本指南中的所有 Git 工作树都创建在已挂载文件系统路径内。

## 克隆 Git 仓库 {#clone-a-git-repository}

指定仓库 URL 以及挂载目录内的目标路径：

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

该仓库会被克隆到 `/path/to/workspace/tidb`。

对于大型仓库，可使用 `--blobless` 在所有文件内容下载完成之前开始工作：

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless
```

使用 `--blobless` 时，`ti` 会先下载仓库结构和 Git 元信息。默认情况下，`--hydrate auto` 会在你工作的同时在后台下载剩余的文件内容。若要禁用后台 hydration，请指定 `--hydrate off`。

如果你需要在克隆命令返回前完成所有文件内容的下载，还可以指定 `--hydrate sync`：

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

## 完成无 blob 工作树的下载 {#finish-downloading-a-blobless-workspace}

在执行需要完整仓库文件内容的任务之前，请等待无 blob 工作树中剩余的下载完成：

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

这个过程称为 hydration，它会下载缺失的 Git 数据，同时不会丢弃你的文件更改。

如果克隆或 hydration 失败，请在重试前检查 CLI 错误和诊断日志。参见[排查 TiDB Cloud Filesystem 故障](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。

## 创建链接工作树 {#create-a-linked-worktree}

如果你希望为另一个分支使用单独的工作目录，而无需再次克隆仓库，可以使用链接工作树。新的工作树会与基础工作区共享 Git 数据。

例如，为新的 `feature-x` 分支创建一个工作树：

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

创建工作树后，可在 `/path/to/workspace/tidb-feature` 中使用常规 Git 命令：

```shell
git -C /path/to/workspace/tidb-feature status
```

有关其他选项（例如在特定提交上创建 detached worktree），请参见 [`add-git-worktree` 命令参考](/ai/ti/reference/ti-fs-git-add-git-worktree.md)。

## 删除链接工作树 {#remove-a-linked-worktree}

当你不再需要某个链接工作树时，可以将其删除：

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

删除链接工作树不会删除基础工作区，也不会删除其他工作树共享的 Git 数据。

如果该工作树包含未提交的更改，命令会拒绝删除它。请在删除工作树前提交或保留你需要的更改。

仅当你确认可以丢弃未提交的更改时，才使用 `--force`：

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature \
  --force
```

## 离开机器前保留工作内容 {#preserve-work-before-leaving-a-machine}

使用 `--mount-profile coding-agent` 时，`.git` 等 Git 元信息会保留在本地机器上。仅进行本地提交并不能保证这些历史记录可在另一台机器上恢复。执行刷写或卸载也不会传输这些本地 Git 元信息。请通过推送到 Git 远端，或使用下文的元信息归档工作流来保留历史记录。

在删除临时机器之前：

1. 使用以下方法之一保留 Git 历史记录：
    - 提交并推送到可写的 Git 远端。然后从独立克隆或 fetch 的结果中，验证预期的提交 ID 是否可用。
    - 如果无法推送，请使用 [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md)，并通过显式的 `--path` 值指定所需的本地 Git 元信息；对于链接工作树，还包括基础仓库的元信息。然后在单独环境中使用 [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) 进行恢复，并比较提交 ID 和工作文件。若路径发生变化，请先使用 [`git worktree repair`](https://git-scm.com/docs/git-worktree) 修复工作树连接。可运行示例请参见[将未推送的工作区恢复到另一台机器](#recover-an-unpushed-workspace-to-another-machine)。
2. 另外保留任何必需的未跟踪文件或已忽略文件；推送只会保留已提交的内容。
3. [安全卸载](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished)。在恢复检查通过之前，请保留原始磁盘。

有关每种挂载预设在本地保留的数据，请参见[挂载预设和本地叠加层](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)。

## 将未推送的工作区恢复到另一台机器 {#recover-an-unpushed-workspace-to-another-machine}

本示例展示了如何在不推送到远端的情况下，将一个包含链接工作树的进行中 Git 工作区迁移到另一台机器。它会将基础仓库的 Git 元信息和链接工作树各自的工作树元信息一起打包到远程归档中，在第二台机器上恢复，修复工作树链接，并通过比较提交 ID 来确认传输成功。

本示例假设源机器使用了 `--mount-profile coding-agent`，并生成了本页前文所述的目录布局：

```text
/path/to/workspace/tidb              (base repository, contains .git/)
/path/to/workspace/tidb-feature      (linked worktree, contains .git file pointing at the base)
```

### 在源机器上 {#on-the-source-machine}

1. 记录提交 ID，以便后续比较：

    ```shell
    (cd /path/to/workspace/tidb && git rev-parse HEAD) | tee /tmp/tidb-base.sha
    (cd /path/to/workspace/tidb-feature && git rev-parse HEAD) | tee /tmp/tidb-feature.sha
    ```

2. 停止写入方并刷写待处理的写入，以便在打包前将已缓存的 blob 持久化：

    ```shell
    ti fs drain-file-system --mount-path /path/to/workspace
    ```

3. 打包仅存在于本地叠加层中的 Git 元信息。`coding-agent` 会将 `.git` 保留在远程命名空间之外，因此必须显式列出基础仓库的 `.git` 目录以及每个链接工作树的 `.git/worktrees/<name>` 子目录。将你需要保留的未跟踪文件或已忽略文件（例如 `.env` 或虚拟环境）也一并包含到同一个归档中。`--archive-path` 是远程文件系统中存储归档的路径；请选择工作树之外的位置，例如 `/packs/`：

    ```shell
    ti fs pack-file-system \
      --mount-path /path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst \
      --path tidb/.git \
      --path tidb/.git/worktrees/tidb-feature \
      --path tidb-feature/.git \
      --path tidb/.env
    ```

    `--path` 的值是相对于挂载路径的。对于你想保留的每个目录或文件，都要重复指定 `--path`。未列出的未跟踪文件或已忽略文件不会在目标机器上恢复。

4. [安全卸载](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished)。在目标机器确认恢复成功之前，请保持源磁盘可用。

### 在（部署）目标机器上 {#on-the-target-machine}

1. 在目标路径挂载相同的文件系统，并使用相同的配置（Profile）。目标路径可以与源路径不同；下面的修复步骤会修正已链接工作树中保存的路径。

    ```shell
    mkdir -p /new/path/to/workspace
    ti fs mount-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --driver fuse
    ```

2. 将打包的元信息恢复到新挂载点的本地叠加层中：

    ```shell
    ti fs unpack-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst
    ```

3. 如果挂载路径与源路径不同，请在其中运行任何 Git 命令之前，先修复已链接工作树的反向引用。请在基础仓库中运行以下命令：

    ```shell
    cd /new/path/to/workspace/tidb
    git worktree repair /new/path/to/workspace/tidb-feature
    git worktree list
    ```

    `git worktree list` 应列出 `tidb` 和 `tidb-feature`，并显示新的路径，且不带 `prunable` 标记。如果基础仓库也发生了移动，请在基础仓库内运行不带参数的 `git worktree repair`，以更新所有已注册的工作树。

4. 验证提交 ID 是否与您在源机器上记录的一致：

    ```shell
    (cd /new/path/to/workspace/tidb && git rev-parse HEAD)
    (cd /new/path/to/workspace/tidb-feature && git rev-parse HEAD)
    ```

    两个输出都必须与源机器上保存的对应 `.sha` 文件一致。如果任一结果不同，请不要删除源磁盘：这说明归档不完整，通常是因为缺少额外的 `--path` 值。请在源机器上使用缺失路径重新运行 `pack-file-system`，然后再次解包。

5. 只有在两个提交 ID 都匹配，并且您保留的所有未跟踪文件都能在目标工作区中正常读取之后，才能删除源机器。

> **Warning:**
>
> `pack-file-system` 只会打包您列出的路径。它不会自行检测已链接的工作树或被 `.gitignore` 忽略的文件。如果您在打包前添加或删除了已链接工作树，请相应更新 `--path` 列表，并始终包含每个工作树自己的 `.git` 文件，以及基础仓库下对应的 `.git/worktrees/<name>` 子目录。

## 接下来做什么 {#what-s-next}

- [在 TiDB Cloud Filesystem 上为 Agents 准备 Git 工作区](/ai/ti/guides/ti-git-workspace-for-agents-example.md)，了解使用 blobless cloning 和后台 hydration 的 agent 工作流。
- [TiDB Cloud Filesystem Git CLI 命令参考](/ai/ti/reference/ti-filesystem-git.md)，查看所有 `ti fs-git` 命令和选项。