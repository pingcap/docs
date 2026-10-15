---
title: 管理文件系统 layer 和 checkpoint
summary: 了解如何创建文件系统 layer、对更改创建 checkpoint 和进行派生、验证隔离，以及提交或丢弃你的工作。
aliases: ['/zh/ai/manage-filesystem-layers']
---

# 管理文件系统 layer 和 checkpoint

在 TiDB Cloud Filesystem 中，layer 会将文件更改与基础文件系统隔离，直到你提交这些更改。你可以使用 checkpoint 保留中间状态，并使用派生来独立探索更改。有关底层概念，请参见[Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md)。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 拥有一个所有者 Token，或一个在现有目录上具有 `read,list,write,delete` 权限的范围受限 Token。示例会在该目录下创建并删除一个子目录。
- 选择文件系统，并使其 Token 可供 `ti` 使用。有关可用的访问方式，请参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。
- 使用 Bash 或 Zsh，并在整个示例过程中保持使用同一个 shell 会话。

## 创建 layer {#create-a-layer}

在你的 Token 作用域内选择一个现有目录。使用所有者 Token 时可使用 `/`，或者将其替换为你的范围受限 Token 允许访问的目录，例如 `/workspace`。为本示例创建一个唯一的子目录：

```shell
parent_path="/"
base_path="${parent_path%/}/layer-example-$(date +%s)-$$"
ti fs create-directory --path "$base_path"
```

然后创建一个 layer：

```shell
ti fs create-layer \
  --base-root-path "$base_path" \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

`--base-root-path` 用于确定 layer 覆盖基础文件系统的哪一部分。

当前 CLI 仅接受 `restore-safe` 作为 `--durability-mode` 的值。有关所有可用选项，请参见 [`create-layer` 命令参考](/ai/ti/reference/ti-fs-create-layer.md)。

保存返回的 `layer_id`，供后续命令使用：

```shell
layer_id="<returned-layer-id>"
```

请使用 ID，而不是 layer 名称，因为 layer 名称可能不是唯一的。

## 使用并检查 layer 更改 {#work-with-and-inspect-layer-changes}

使用返回的 layer ID 向 layer 写入一个示例文件：

```shell
printf 'Layer review proposal\n' | ti fs copy-file \
  --from-stdin \
  --to-remote "$base_path/proposal.md" \
  --layer-id "$layer_id"
```

检查该 layer 及其更改：

```shell
ti fs describe-layer --layer-id "$layer_id"
ti fs diff-layer --layer-id "$layer_id"
```

列出所选文件系统中的所有 layer：

```shell
ti fs list-layers --output text
```

尚未提交的更改会保留在 layer 中。不选择 layer 的文件操作会访问基础文件系统，因此不会显示其中未提交的更改。

只有 `copy-file`、`find-files` 和 `search-file-content` 支持 `--layer-id`。`read-file`、`list-files`、`describe-file`、`delete-file`、`move-file` 和 `create-directory` 始终作用于基础文件系统。要读取 layer 中文件的内容，请按[挂载可写 layer](#mount-a-writable-layer) 或[验证 checkpoint 的文件内容](#create-a-checkpoint)中的说明进行操作。

> **Note:**
>
> 带有 `--layer-id` 的 `copy-file` 不支持递归复制。要将目录树复制到 layer 中，请将该 layer [挂载](#mount-a-writable-layer)为可写的 FUSE 挂载点，并通过挂载路径复制文件。
>
> 不要同时将同一个可写 layer 挂载到多个本地路径。请复用现有挂载，或者先卸载后再将该 layer 挂载到其他位置。
>
> 挂载命令使用 `--layer-ref` 指定 layer，而上述文件命令使用 `--layer-id`。两者都接受相同的 layer 标识符值。

### 挂载可写 layer {#mount-a-writable-layer}

要使用本地工具，请先完成 [FUSE 前提条件](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method)，然后挂载该 layer。WebDAV 不支持 layer 或 checkpoint。

```shell
layer_mount="$(mktemp -d "$HOME/ti-fs-layer.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$layer_mount" \
  --remote-path "$base_path" \
  --layer-ref "$layer_id" \
  --driver fuse
cat "$layer_mount/proposal.md"
```

预期输出：`Layer review proposal`。要验证隔离，请在不选择 layer 的情况下从基础文件系统读取：

```shell
ti fs read-file --path "$base_path/proposal.md"
```

预期会出现 not-found 错误，因为该 layer 尚未提交。如果该文件在基础文件系统中可见，请先停止操作并检查 layer 选择是否正确，然后再继续。

## 创建 checkpoint {#create-a-checkpoint}

checkpoint 会保留 layer 持久历史中的某个时间点。

如果该 layer 已有可写的 FUSE 挂载，请在创建 checkpoint 之前停止写入、关闭打开的文件，并对刷写挂载：

```shell
ti fs drain-file-system \
  --mount-path "$layer_mount"
```

然后创建 checkpoint：

```shell
ti fs create-layer-checkpoint \
  --layer-id "$layer_id" \
  --checkpoint-id seed \
  --label "before review"
```

要验证 checkpoint 的文件内容，请将其挂载到另一个本地路径：

```shell
checkpoint_mount="$(mktemp -d "$HOME/ti-fs-checkpoint.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$checkpoint_mount" \
  --remote-path "$base_path" \
  --layer-ref "$layer_id" \
  --checkpoint-id seed \
  --driver fuse
cat "$checkpoint_mount/proposal.md"
ti fs unmount-file-system --mount-path "$checkpoint_mount"
```

预期输出：`Layer review proposal`。checkpoint 挂载为只读。如果读取时发生假死，请参见[挂载故障排查](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs)。

> **Warning:**
>
> 在 `ti` v0.2.6 中，以及在使用内置运行时 `60b63d6` 的 v0.2.7 安装中，即使后台进程异常退出，checkpoint 卸载也可能返回 `unmounted`。继续之前请检查挂载日志；如果关闭过程异常，请保留缓存并重新验证 checkpoint 的内容。有关日志位置和恢复步骤，请参见[卸载返回成功但挂载进程异常退出](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally)。

## 派生 layer {#fork-a-layer}

如果你希望基于该 checkpoint 继续独立工作，请派生一个新的可写 layer。否则，请跳转到[提交或丢弃 layer 更改](#commit-or-discard-layer-changes)。

```shell
ti fs fork-layer \
  --parent-layer-ref "$layer_id" \
  --layer-name experiment \
  --checkpoint-id seed
```

单独保存派生后返回的 `layer_id`：

```shell
forked_layer_id="<returned-forked-layer-id>"
```

要检查该派生 layer 固定的祖先链：

```shell
ti fs list-layer-chain --layer-ref "$forked_layer_id"
```

创建派生后，对父 layer 和子 layer 所做的更改彼此独立。

## 提交或丢弃 layer 更改 {#commit-or-discard-layer-changes}

如果该 layer 具有可写的 FUSE 挂载点，请先停止写入方、关闭已打开的文件，并在选择后续操作前将其卸载：

```shell
ti fs unmount-file-system \
  --mount-path "$layer_mount"
```

优雅的卸载会自动刷写待处理的写入。

> **Warning:**
>
> 在 `ti` v0.2.6 中，以及在使用内置运行时 `60b63d6` 的 v0.2.7 安装中，即使后台进程异常退出，layer 卸载也可能返回 `unmounted`。在提交或丢弃该 layer 之前，请检查挂载日志；如果关闭过程异常，请保留缓存并先验证所需文件。有关日志位置和恢复步骤，请参见[卸载返回成功，但挂载进程异常退出](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally)。

选择以下其中一种结果：**commit** 会将更改应用到基础文件系统；**rollback** 会丢弃这些更改。要提交，请执行：

```shell
ti fs commit-layer --layer-id "$layer_id"
```

提交成功后，通过基础文件系统验证内容：

```shell
ti fs read-file --path "$base_path/proposal.md"
```

预期输出：`Layer review proposal`。

提交会将该 layer 的有效更改应用到基础文件系统。如果该 layer 是通过派生另一个 layer 创建的，提交它不会将更改合并回其父 layer。

如果基础文件系统中存在冲突更改，提交可能会失败，而不是自动合并这些更改。在决定如何继续之前，请保留该 layer，并检查其更改以及基础文件系统。

如果你选择丢弃更改，请执行以下命令，而不是提交：

```shell
ti fs rollback-layer --layer-id "$layer_id"
```

回滚会丢弃当前 layer 的更改。它不会将该 layer 重置到更早的 checkpoint。若要从某个 checkpoint 继续，请从该 checkpoint 派生一个新的 layer。

## 删除 layer {#delete-a-layer}

如果你创建了一个派生 layer，请先删除它，再删除其父 layer：

```shell
ti fs delete-layer --layer-ref "$forked_layer_id"
```

然后删除父 layer：

```shell
ti fs delete-layer --layer-ref "$layer_id"
```

删除 layer 会放弃该 layer，但不会立即擦除其全部历史记录。如果该 layer 仍有活动的子孙 layer，默认情况下该命令会失败。

或者，如果要同时放弃某个 layer 及其所有活动的子孙 layer，请使用 `--cascade`：

```shell
ti fs delete-layer \
  --layer-ref "$layer_id" \
  --cascade
```

仅当你也打算放弃这些子孙 layer 时，才使用 `--cascade`。

在卸载示例挂载点并删除示例 layer 后，删除基础目录：

```shell
ti fs delete-file --path "${base_path:?Set the example directory first}" --recursive
ti fs describe-file --path "$base_path"
```

预期 `describe-file` 会返回 not-found 错误。成功卸载后，使用 `rmdir "$layer_mount"` 和 `rmdir "$checkpoint_mount"` 删除你创建的本地目录。删除示例文件不会立即擦除已放弃 layer 的历史记录。

## 接下来做什么 {#what-s-next}

- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)