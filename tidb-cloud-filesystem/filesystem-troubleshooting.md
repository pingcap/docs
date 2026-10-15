---
title: 排查 TiDB Cloud Filesystem 故障
summary: 了解如何诊断文件系统 Token、Region、运行时、挂载和访问故障，并选择安全的恢复路径。
---

# 排查 TiDB Cloud Filesystem 故障

使用以下症状来诊断文件系统访问和挂载故障。仅在需要时添加 `--debug`，并在分享输出前检查其中已脱敏的内容。关于 CLI 安装、API key 身份验证、Starter 或 SQL 故障，请参见[排查 TiDB Cloud CLI 故障](/ai/ti/reference/ti-troubleshooting.md)。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 文件系统 Token 缺失 {#file-system-token-is-missing}

对于一个干净的沙箱环境，请提供 Token 和 Region。`ti` 会从 Token 推导出文件系统 ID：

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

文件系统 Token 不是 TiDB Cloud API 私钥。提供 Token 时，`TI_FS_FILE_SYSTEM_ID` 是可选的；仅当你希望 `ti` 验证单独分发的 ID 是否与该 Token 匹配时，才需要设置它。

如果已知 Token，但当前机器上未存储该 Token，请先导入它，然后选择推导出的 ID：

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region <filesystem-region-code>
ti fs list-files --file-system-id <file-system-id> --path /
```

如果所有已知 Token 都已丢失或被（权限）回收，请使用 TiDB Cloud API key 生成另一个所有者 Token：

```bash
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name recovery \
  --ttl 24h
```

新的明文 Token 只会在响应中出现一次。请安全保存它，或者添加 `--store-locally` 以在当前机器上选中它。

## 文件系统 Token 被拒绝 {#file-system-token-is-rejected}

文件操作返回 HTTP 401 或 `invalid API key` 错误，可能表示文件系统 Token 已被禁用、已过期、已在另一台机器上刷新，或已被（权限）回收。在此上下文中，`API key` 可能指的是文件系统 Token；这并不一定表示你的 TiDB Cloud API key 有问题。请使用 TiDB Cloud API key 检查 Token 元信息：

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

Token 名称不是唯一的，因此在执行启用、禁用或删除操作时，请使用此输出中的不可变 `token_id`。较早创建或导入、且不带 Token 生命周期元信息的凭据仍然可能有效，但它不会出现在此列表中，且 `ti` 不会猜测其匹配关系。

在启用、禁用、删除或刷新 Token 后，请等待大约 10 秒，让身份验证缓存收敛。

如果刷新操作报告 `fs.token_refresh_ambiguous`，表示响应已丢失，结果未知。旧 Token 可能仍然可用（如果轮换从未提交），也可能已经失效，而替换 Token 无法恢复。不要使用旧 Token 重试刷新。请改用 TiDB Cloud 凭据生成一个独立的所有者 Token。

如果你在传入文件系统 Token 时，文件命令报告 `invalid API key` 且退出码为 1，请先检查 Token 状态，再检查你的 API key 对。即使 API key 对正确，被删除或禁用的 Token 也会产生此消息。

如果 Token 变异操作报告 `fs.token_mount_active`，请停止使用该挂载的应用程序，关闭打开的文件，并使用错误中给出的精确路径执行卸载：

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

CLI 错误消息会建议先运行 `drain-file-system`，但优雅的 FUSE 卸载本身就会刷写待处理写入，因此无需单独执行刷写。在将退出状态 `0` 视为已完成刷写的证明之前，请检查挂载日志中是否存在 `reason=force_quit`；参见[卸载返回成功，但挂载进程异常退出](#unmount-returns-success-but-the-mount-process-exits-abnormally)。WebDAV 不支持 `drain-file-system`；对于 WebDAV，请使用优雅卸载。

然后重试 Token 操作。另一台机器上的挂载在本地不可见；请与那台机器单独协调轮换操作。

## 范围受限 Token 访问被拒绝 {#scoped-token-access-is-denied}

在其作用域之外使用范围受限 Token 时，命令会以退出码 1 退出，并报告以下两种消息之一。大多数命令会报告 `fs access denied`。`ti fs copy-file` 则可能报告空的 `HTTP 403:`。

在此上下文中，这两种消息都表示该 Token 不允许在此路径上执行此操作。它们都不是连接问题，也不表示 Token 无效。在做任何更改之前，请先检查该 Token 允许的内容：

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

将 Token 的作用域与你使用的路径和操作进行比较。`search` 还要求具备 `read` 权限。除非允许路径是 `/`，否则范围受限 Token 不能列出文件系统根目录。范围受限 Token 不能扩大自身权限，因此请使用所有者 Token 生成一个具有所需操作权限的新范围受限 Token，而不是尝试修改现有 Token。

## 文件系统选择缺失 {#file-system-selection-is-missing}

使用 TiDB Cloud API key 列出已配置 Region 中的远程资源，并显式选择一个：

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

或者，在当前 shell 中为后续命令选择该文件系统：

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

即使本地只存储了一个 Token，也要显式选择一个文件系统。请提供其 ID，或提供能够标识它的 Token。

## 文件系统 Region 不受支持 {#file-system-region-is-unsupported}

你安装的 `ti` 版本可能不支持为文件系统访问配置的 Region。请检查[支持的区域](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions)。请在你的配置（Profile）中，或通过命令的 `--region` 选择受支持的 Region；不要配置原始服务器 URL。

## 文件系统运行时缺失或不兼容 {#file-system-runtime-is-missing-or-incompatible}

发布安装程序会将捆绑的文件系统运行时组件放在 `ti` 旁边。你不需要直接调用此运行时。当 CLI 报告运行时组件缺失时，请重新运行当前安装程序：

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

验证 `PATH` 解析到的是预期的 `ti`：

```bash
command -v ti
ti --version
```

不要随意复制一个独立的运行时二进制文件到该位置。

## 文件系统创建达到配额 {#file-system-creation-reaches-quota}

如果创建操作返回配额或容量错误，请在重试前先列出已配置 Region 中现有的文件系统：

```bash
ti fs list-file-systems --output text
```

不要为了让自动化流程通过而删除无关的文件系统。如果错误链接到 TiDB Cloud 计费页面并提示需要支付方式，请先按照该指引操作，再重试。

## 挂载未就绪 {#mount-does-not-become-ready}

当后台挂载成功启动时，CLI 会输出结果，而不会显示运行时启动消息。如果启动失败或超时，请检查错误中报告路径下的日志。确认以下事项：

- 挂载路径存在且可写。
- 没有现有挂载正在使用该路径。
- 文件系统 Token 和 Region 有效。
- 已安装 FUSE 前置条件或 WebDAV 辅助程序。
- 远程 Region 可达。

在 macOS 上，即使安装了 macFUSE，`ti` 默认也使用 WebDAV。layer 和 checkpoint 挂载需要 FUSE。若要为文件系统挂载显式请求 FUSE：

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux 需要 FUSE 支持、`fuse3` 软件包以及对 `/dev/fuse` 的访问权限。Windows 不支持文件系统和 Vault 挂载；请改用 `ti fs` 数据平面命令或非挂载的 Vault 命令。

## 挂载成功，但文件访问假死 {#mount-succeeds-but-file-access-hangs}

`mounted` 结果确认挂载启动已完成，但并不能证明后续文件读写一定成功。目录列表也可能成功，而读取文件时发生假死。

对于一个已知的小型测试文件，请使用以下步骤：

1. 如果挂载后的读或写在 30 秒后仍未返回，请使用 Ctrl+C 中断该命令。如果它仍然阻塞，请在挂载之外打开另一个终端进行诊断。不要在该挂载上启动额外负载。
2. 使用相同的 Token 和 Region，通过 `ti fs read-file --path "<remote-file-path>"` 读取同一个文件。如果挂载使用了 `--remote-path`，请在远程文件路径中包含该前缀。如果此读取也失败，请先解决报告的身份验证、Region 或服务错误。如果成功，请将诊断重点放在本地挂载路径上。
3. 记录 `ti --version`、操作系统版本、所选驱动、耗时，以及可用时的挂载诊断日志。不要包含 Token 或文件内容。在 macOS 上，即使安装了 macFUSE，文件系统挂载默认也使用 WebDAV；在复现问题时，请指定 `--driver webdav` 或 `--driver fuse`。layer 和 checkpoint 挂载需要 FUSE。
4. 停止使用该挂载的应用程序，关闭打开的文件，并将任何位于该挂载内的 shell 的工作目录切换到其外部路径。然后尝试正常卸载：

    ```bash
    ti fs unmount-file-system --mount-path /path/to/workspace
    ```

5. 成功卸载后，使用直接 CLI 读取验证任何必要的写入。在调查挂载问题期间，请继续使用直接的 `ti fs` 命令，并在使用替代挂载前验证文件 I/O。

不要对 WebDAV 使用 `drain-file-system`。如果卸载失败或远程数据缺失，请保留机器和本地挂载数据以便恢复。不要把删除缓存或强制卸载当作常规重试手段：待处理写入可能仍然只存在于本地。上文提到的 30 秒截止时间只是针对小文件冒烟测试的诊断限制，并非服务延时保证。

## Ubuntu 26.04 在 `/workspace` 下拒绝 FUSE 挂载 {#ubuntu-2604-rejects-a-fuse-mount-under-workspace}

Ubuntu 26.04 会对 `fusermount3` 应用 AppArmor 配置文件。其默认挂载路径允许列表不包含 `/workspace`，因此 root 用户和非 root 用户都可能收到以下错误：

```text
/usr/bin/fusermount3: mount failed: Permission denied
```

确认该拒绝：

```bash
sudo journalctl -k --since "10 minutes ago" |
  grep 'profile="fusermount3"'
```

如果日志项中包含 `operation="mount"`、`name="/workspace/"` 和 `info="failed mntpnt match"`，则说明是此限制导致。请改为挂载到 `$HOME` 或 `/mnt` 下：

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

更改 `/workspace` 的所有者或模式并不能绕过 AppArmor。如果路径无法更改，请按照[Ubuntu 26.04 挂载路径限制](/tidb-cloud-filesystem/filesystem-mount-linux.md#ubuntu-2604-mount-path-restrictions)中的说明，在 `/etc/apparmor.d/local/fusermount3` 中添加显式的 `/workspace` 挂载和卸载规则。

## 进程崩溃后挂载变为 stale {#mount-becomes-stale-after-a-process-crash}

如果 companion 在未优雅卸载的情况下被杀死，FUSE 访问可能返回 `EIO` 或 `Transport endpoint is not connected`。请先停止那些仍打开文件的进程，然后尝试：

```bash
ti fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

如果希望在没有残留 locator 时清理操作也能成功，请使用 `--ignore-absent`。突然清理无法保证恢复已删除本地磁盘上的待写入数据。

## 卸载报告 busy {#unmount-reports-busy}

关闭编辑器、工作目录位于挂载点内的 shell，以及其他仍持有打开文件句柄的进程，然后重试：

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

优雅的 FUSE 卸载会自动刷写待写入数据，但前提是挂载进程正常退出。在依赖 `unmount-file-system` 返回 `0` 退出状态之前，请检查挂载日志中是否有 `reason=force_quit`；参见[卸载返回成功，但挂载进程异常退出](#unmount-returns-success-but-the-mount-process-exits-abnormally)。单独运行 `drain-file-system` 不会关闭打开的文件，也无法解决 busy 挂载。它的用途是在保持挂载运行的同时刷写待写入数据。WebDAV 不支持 drain。

## 卸载返回成功，但挂载进程异常退出 {#unmount-returns-success-but-the-mount-process-exits-abnormally}

在 `ti v0.2.6` 中，即使后台进程报告 `late pending drain`，随后出现 `reason=force_quit` 且退出码为 `1`，layer 或 checkpoint 挂载仍可能在大约 30 秒后返回 `unmounted`。这种行为已在以下场景中观察到：从 layer 读取一个小文件后，以及对 layer 挂载执行写入、fsync 和 drain 后。

此问题同样存在于捆绑的运行时 `60b63d6` 中，该运行时与 `ti` v0.2.7 一起使用。CLI 和捆绑运行时具有各自独立的版本，因此不能仅凭 CLI 版本判断挂载是否受影响。关于修复状态，请参见[捆绑挂载运行时修复（Drive9 #1002）](https://github.com/mem9-ai/drive9/pull/1002)。

在依赖 layer 或 checkpoint 卸载结果之前，请检查其后台挂载日志。在 `ti` v0.2.7 中，成功执行 `mount-file-system` 命令后不会显示日志路径。默认情况下，你可以使用以下命令查找日志：

```bash
find "$HOME/.ti/drive9-home" -type f -path '*/drive9/mount-logs/mount-*.log'
```

在 Linux 上，如果设置了 `XDG_CACHE_HOME`，请改为检查 `$XDG_CACHE_HOME/drive9/mount-logs`。将日志与挂载路径及挂载时间对应起来，然后查找 `late pending drain`、`reason=force_quit` 或后台进程非零退出码。

如果出现上述任一情况：

1. 将该结果视为异常下线，并保持机器和本地缓存可用。
2. 使用带 `--layer-id` 的直接 CLI 读取来验证所需的 layer 文件。对于已提交的更改，请在不选择 layer 的情况下读取基础文件系统。要验证 checkpoint，请使用相同的 `--layer-ref` 和 `--checkpoint-id` 将其挂载到新的本地路径，然后再次读取所需文件。你也可以将可写 layer 重新挂载到新路径，以独立于先前挂载来验证其内容。
3. 在验证完成之前，不要提交或丢弃该 layer，也不要删除本地状态。报告问题时，请附上 CLI 版本和已脱敏的挂载日志。

## 退出码 {#exit-codes}

`ti fs` 使用以下退出码。自动化程序可以基于这些退出码进行分支处理，而不是匹配错误文本。

| 代码 | 含义 | 处理方式 |
| --- | --- | --- |
| 0 | 成功 | 继续。 |
| 1 | 运行时或远程 API 错误 | 阅读消息并处理所报告的运行时、网络或服务错误。范围受限 Token 拒绝以及某些其他服务错误也使用此代码。 |
| 2 | 本地用法、验证或配置错误 | 修正命令或配置（Profile）。例如：未知标记、缺少必需输入、不受支持的 Region，或权限过宽的 token 文件。 |
| 3 | 身份验证失败 | 检查 Token 或 API key 对。 |
| 4 | 账户缺少执行该操作的权限 | 联系组织管理员。这不同于范围受限 Token 拒绝，后者返回退出码 1。 |
| 5 | 请求中指定的文件系统、Token 或其他资源不存在 | 检查 ID。文件系统内不存在的路径会返回 1，而不是 5。 |

已删除或已禁用的文件系统 Token 是上述表格中的一个异常：文件命令返回退出码 1，而不是 3。参见[文件系统 Token 被拒绝](#file-system-token-is-rejected)。

## 报告问题 {#report-a-problem}

请提供 `ti` 版本、操作系统和架构、命令名称、稳定的错误码以及已脱敏的日志。切勿包含 API keys、文件系统或 Vault Token、数据库密码、包含私有数据的 SQL，或文件内容。请在 [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues) 报告问题。