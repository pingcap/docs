---
title: 在多台机器之间共享文件系统
summary: 了解如何通过为每个接收方使用单独的范围受限 Token 在多台机器之间共享文件，验证权限，并独立回收访问权限。
aliases: ['/zh/ai/ti-share-filesystem-across-machines-example']
---

# 在多台机器之间共享文件系统

在 TiDB Cloud Filesystem 中，你可以与其他用户、机器、CI 作业或 agent 共享文件，而无需在不同环境之间复制文件。为每个接收方分配单独的范围受限 Token，以按路径和操作限制访问，并且可以在不影响其他接收方的情况下回收某个接收方的访问权限。

本指南将向你展示如何为某个目录授权 24 小时的只读访问、验证接收方的权限，然后回收该 Token。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口如有变更，恕不另行通知。

## 前提条件 {#prerequisites}

开始之前，请确保：

- 你拥有现有文件系统的所有者 Token，并且知道其 Region。
- 在所有者环境和接收方环境中都已[安装 TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 你有一个安全通道（例如 secret manager）用于传输范围受限 Token。

请使用 Bash 或 Zsh。在整个教程过程中，保持两个独立的 shell 打开：一个是在可信机器上的**owner shell**，用于创建和回收 Token；另一个是**recipient shell**，用于测试访问。接收方不需要你的所有者 Token 或 TiDB Cloud API 密钥。

对于 CI 或 agent，请将相应的 Token 注入每个环境的 `TI_FS_TOKEN`，而不是运行交互式输入提示。按如下所示设置 Region，并清除 `TI_FS_FILE_SYSTEM_ID`。在两个环境中都保留 `share_path`，并在所有者环境中保留 `reviewer_token_id`，直到清理完成。

在 owner shell 中，设置 Region 并在提示时加载所有者 Token。输入内容会被隐藏：

```bash
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'Owner token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

在完成访问权限回收之前，请将所有者 Token 保留在 `TI_FS_TOKEN` 中。它既用于文件操作认证，也用于 Token 管理。关于其他认证方式，请参见[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md#inspect-and-change-token-status)。

## 向特定文件授予访问权限 {#give-access-to-specific-files}

在 owner shell 中：

1. 创建一个唯一目录并上传示例文件：

    ```bash
    share_path="/sharing-example-$(date +%s)-$$"
    ti fs create-directory --path "$share_path"
    printf 'Shared review sample\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/summary.txt"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    `read-file` 的预期输出为：`Shared review sample`。如果有任何错误，请先解决后再继续。

2. 创建一个仅允许读取和列出该目录内容的 Token：

    ```bash
    ti fs generate-file-system-scoped-token \
      --subject reviewer \
      --ttl 24h \
      --allow "$share_path:read,list"
    ```

    请安全保存返回的 `fs_token`；它只会在签发时显示一次。还要保存返回的 `token_id`，以便后续回收：

    ```bash
    reviewer_token_id="<returned-token-id>"
    ```

3. 通过你的安全通道，将范围受限 Token、Region code 以及 `share_path` 的精确值发送给接收方。请妥善保管所有者 Token，不要泄露。如果你是通过挂载点修改文件，请在发送访问信息之前先[验证这些修改已准备好共享](#make-sure-updates-are-ready-to-share)。

请为每个接收方创建单独的范围受限 Token，以便你可以独立回收访问权限。关于其他权限组合，请参见[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

## 从另一台机器访问共享文件 {#access-the-shared-files-from-another-machine}

在 recipient shell 中：

1. 设置 Region 和共享路径，并在提示时加载范围受限 Token：

    ```bash
    unset TI_FS_FILE_SYSTEM_ID
    export TI_REGION_CODE="<filesystem-region-code>"
    share_path="<shared-directory-path>"
    printf 'Scoped token: '
    read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
    ```

    使用所有者提供的 Region 和精确目录路径。该 Token 会标识文件系统；无需复制文件系统 ID 或 CLI 配置（Profile）。

2. 列出目录并读取文件：

    ```bash
    ti fs list-files --path "$share_path"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    `read-file` 的预期输出为：`Shared review sample`。

3. 检查写入操作以及对目录外部的访问是否被拒绝：

    ```bash
    printf 'This write must be rejected\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/denied-write.txt"
    ti fs list-files --path /
    ```

    预期每个命令都会返回授权错误。其他错误不能证明权限配置正确。如果任一操作成功，请先回收该 Token，再继续后续步骤。

在 owner shell 中，确认 `ti fs describe-file --path "$share_path/denied-write.txt"` 报告该文件不存在。

### 挂载共享目录（可选） {#mount-the-shared-directory-optional}

以下命令适用于 Linux FUSE 或安装了 macFUSE 的 macOS。在未安装 macFUSE 的 Mac 上，请使用 `--driver webdav`，并从该命令中省略 `--read-only`：WebDAV 不接受该选项。范围受限 Token 仍会在服务端强制执行只读访问。请参见[挂载前提条件](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method)。

在 recipient shell 中，挂载共享目录：

```bash
review_mount="$(mktemp -d "$HOME/ti-fs-review.XXXXXX")"
ti fs mount-file-system \
  --remote-path "$share_path" \
  --mount-path "$review_mount" \
  --driver fuse \
  --read-only
```

读取示例文件：

```bash
cat "$review_mount/summary.txt"
```

预期输出：`Shared review sample`。如果读取耗时超过 30 秒，请中断操作并按照[挂载故障排查](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs)进行处理。

范围受限 Token 会在服务端强制执行只读访问。FUSE 的 `--read-only` 选项也会阻止通过此本地挂载进行写入。

## 确保更新已准备好共享 {#make-sure-updates-are-ready-to-share}

对于后续通过挂载点写入的工作流，在将文件交给其他用户之前，请先关闭文件并[安全完成写入](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。对于 FUSE，请对刷写挂载点或成功卸载。对于 WebDAV，请正常卸载；不支持刷写。然后通过直接执行 `ti fs read-file` 请求来验证更新后的文件。

避免对同一文件进行并发写入：更改不会自动合并。当用户需要隔离的工作空间时，请使用[Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md)。

## 停止共享访问权限 {#stop-sharing-access}

请按顺序完成以下步骤：

1. **Recipient：**停止使用共享文件的应用程序。如果你挂载了该目录，请先卸载：

    ```bash
    ti fs unmount-file-system --mount-path "$review_mount"
    ```

    保持范围受限 Token 已设置，以便执行第 3 步中的验证。

2. **Owner：**在原始 owner shell 中，使用创建时保存的 ID 回收该 Token：

    ```bash
    ti fs delete-file-system-token --token-id "$reviewer_token_id"
    ```

    此命令接受 TiDB Cloud API 凭据或所有者 Token，并且所有者 Token 必须通过 `TI_FS_TOKEN` 或 `--fs-token` 传入。如果所有者 Token 仅通过 `import-file-system-token` 保存到本地凭据中，则此处会忽略它，随后 `delete-file-system-token` 和 `list-file-system-tokens` 都会以退出码 `3` 结束，并要求提供 API 凭据。要查看 Token 元信息，请使用 `ti fs list-file-system-tokens --output text`。

3. **Recipient：**等待大约 10 秒，让认证缓存完成更新，然后使用相同的范围受限 Token 再次读取：

    ```bash
    ti fs read-file --path "$share_path/summary.txt"
    ```

    预期会出现认证或授权错误。如果读取仍然成功，请核对已回收的 Token ID，并在缓存间隔后重试。网络错误不能证明回收已生效。

    确认回收后，清除 Token：

    ```bash
    unset TI_FS_TOKEN TI_REGION_CODE
    ```

    如果你挂载了该示例，请使用 `rmdir "$review_mount"` 删除其空的本地目录。

4. **Owner：**删除示例目录并确认其已不存在：

    ```bash
    ti fs delete-file --path "${share_path:?Set the example directory first}" --recursive
    ti fs describe-file --path "$share_path"
    ```

    预期 `describe-file` 会返回 not-found 错误。

回收操作不会影响文件系统本身或其他 Token。它无法删除接收方已经下载或缓存的文件。仅清除环境变量并不会回收 Token。

## 接下来做什么 {#what-s-next}

- 参考[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)，创建、轮转、禁用或回收 Token。
- 参考[TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md)，在将更改应用到底层文件系统之前独立进行修改。
- 参考[Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)，了解使用共享文件系统数据的工作流。