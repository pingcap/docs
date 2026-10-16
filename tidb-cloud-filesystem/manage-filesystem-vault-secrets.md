---
title: 管理文件系统的 Vault Secret
summary: 了解如何存储和轮转 Vault Secret、向特定字段授予临时访问权限、在进程中使用它们，以及回收访问权限。
aliases: ['/zh/ai/manage-filesystem-vault-secrets']
---

# 管理文件系统的 Vault Secret

在 TiDB Cloud Filesystem 中，你可以使用文件系统的 Vault 来存储凭证和其他敏感值，而不是存放在普通文件系统文件中。你可以仅向应用程序、自动化流程或代理授予其所需字段的临时访问权限，而无需给予其对整个文件系统的广泛访问权限。

委派工作流可以读取这些字段，将它们注入到进程中，或通过只读挂载访问它们。所有者可以审计并回收访问权限。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 可以访问一个测试文件系统。运行 `ti fs-vault list-secrets` 检查是否已存在名为 `db-prod` 的 Secret。如果存在，请选择其他名称，并在下面的名称、路径和授权作用域中一致地将 `db-prod` 替换掉，或者使用另一个测试文件系统。
- 使用 Bash 或 Zsh。请保持所有者的 shell 处于打开状态，以便后续清理步骤可以使用下面创建的临时目录。
- 让 `ti` 可以访问该文件系统及其所有者 Token。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

所有者 Token 用于创建和替换 Secret、创建和回收授权，以及查看审计事件。Vault 委派 Token 仅提供其授权所允许的 Secret 访问权限。

请将所有者 Token 和 Vault 委派 Token 都视为凭证。不要在日志、源代码管理、共享终端输出或命令行参数中暴露它们。

## 创建 Secret {#create-a-secret}

一个 Vault Secret 可以包含多个具名字段。例如，一个数据库 Secret 可能包含连接 URL 和密码。

先将每个字段值写入各自的本地文件，然后通过 `@` 前缀将这些文件传给 `create-secret`。使用 `read -r -s` 将每个值读入变量，并使用 `printf '%s'` 写入，这样该值既不会进入 shell 历史记录，也不会附带末尾换行符。`create-secret` 和 `replace-secret` 接受以换行符结尾的值并报告成功，但后续 [`run-with-secret`](#inject-a-secret-into-a-process) 会拒绝注入该值，并报错 `refusing to inject (EACCES)`。编辑器和 `echo` 会添加末尾换行符；`printf '%s'` 不会。

```shell
umask 077
secret_dir="$(mktemp -d)"

printf 'DB_URL: ' >&2
read -r -s DB_URL_VALUE
printf '\n' >&2
printf '%s' "$DB_URL_VALUE" > "$secret_dir/DB_URL"

printf 'PASSWORD: ' >&2
read -r -s PASSWORD_VALUE
printf '\n' >&2
printf '%s' "$PASSWORD_VALUE" > "$secret_dir/PASSWORD"

unset DB_URL_VALUE PASSWORD_VALUE
```

创建一个名为 `db-prod` 的 Secret：

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field "DB_URL=@$secret_dir/DB_URL" \
  --field "PASSWORD=@$secret_dir/PASSWORD"
```

`@` 前缀告诉 `ti` 从本地文件读取字段值。建议对每个字段都使用这种方式，因为如果直接写成 `--field DB_URL=mysql://example`，该值会出现在 shell 历史记录和进程列表中。

某些 Vault 命令通过名称标识 Secret，例如 `db-prod`。而对特定 Secret 路径进行操作的命令（如 `replace-secret` 和 `run-with-secret`）则使用其完整 Vault 路径。例如，`db-prod` 的 Vault 路径是 `/n/vault/db-prod`。

### 读取 Secret 值 {#read-a-secret-value}

`read-secret` 会返回明文 Secret 值。仅在你确实需要直接获取该值时使用它，并确保其输出不会被写入日志或其他非预期位置。

例如，只读取 `DB_URL` 字段：

```shell
ti fs-vault read-secret \
  --secret-name db-prod \
  --field DB_URL \
  --format raw
```

当应用程序需要 Secret 时，建议优先选择[将其注入到进程中](#inject-a-secret-into-a-process)，而不是自行读取和处理明文值。

## 轮转 Secret {#rotate-a-secret}

`replace-secret` 会替换 Secret 中的所有字段，而不仅仅是值发生变化的那个字段。

要轮转 `DB_URL`，请使用与[创建 Secret](#create-a-secret)中相同的 `read -r -s` 和 `printf '%s'` 模式，覆盖临时目录中的对应文件。保留 `PASSWORD` 文件，以便替换后仍保留该字段：

```shell
printf 'New DB_URL: ' >&2
read -r -s DB_URL_VALUE
printf '\n' >&2
printf '%s' "$DB_URL_VALUE" > "$secret_dir/DB_URL"
unset DB_URL_VALUE

ti fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory "$secret_dir"
```

目录中的每个文件都会成为替换后 Secret 中的一个字段。任何未包含在该目录中的现有字段都不会被保留。`replace-secret` 接受以换行符结尾的值并报告成功；真正的失败会在之后 `run-with-secret` 拒绝注入该值时才出现，因此这里仍应继续使用 `printf '%s'`，而不是 `echo` 或编辑器。

请不要将这些本地文件纳入源代码管理，并在不再需要时将其删除。详情参见 [`replace-secret` 参考文档](/ai/ti/reference/ti-fs-vault-replace-secret.md)。

## 委派有限访问权限 {#delegate-limited-access}

不要共享文件系统所有者 Token，而是为其他用户、应用程序或代理所需的 Secret 字段创建一个短期有效的授权。

例如，以下授权允许 `deploy-agent` 在 10 分钟内仅读取 `DB_URL` 字段：

```shell
ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m
```

该命令会返回一个 Vault 委派 Token 和一个授权 ID。仅将该委派 Token 提供给需要该 Secret 的工作流，并保留授权 ID，以便在必要时可以在其过期前回收该授权。

在使用委派 Secret 的独立环境中，将该 Token 作为 `TI_VAULT_TOKEN` 提供。同时，将 `TI_FS_FILE_SYSTEM_ID` 设置为文件系统 ID，并将 `TI_REGION_CODE` 设置为其 region code。仅凭 Vault 委派 Token 本身无法标识文件系统。避免将该 Token 直接放在命令行参数中，因为命令参数可能会出现在 shell 历史记录或进程列表中。

## 将 Secret 注入到进程中 {#inject-a-secret-into-a-process}

如果应用程序可以通过环境变量接收凭证，请使用 `run-with-secret`，使允许访问的 Secret 字段仅对其子进程可用：

```shell
ti fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- <command>
```

每个允许访问的 Secret 字段都会变成一个同名环境变量。在本示例的 `db-prod/DB_URL` 授权下，`ti` 会将 `DB_URL` 注入到子进程中，但不会注入 `PASSWORD`。

`ti` 使用的 Vault 凭证不会传递给子进程。这样，应用程序就可以使用 Secret，而无需将其明文值写入文件。

与 `run-with-secret` 一起使用的字段名必须匹配 `[A-Z_][A-Z0-9_]*`。对于计划注入到进程中的 Secret，请使用大写、环境变量风格的字段名。

## 将 Secret 作为只读文件挂载 {#mount-secrets-as-read-only-files}

如果应用程序期望以文件而不是环境变量的形式接收凭证，你可以选择在 Linux 或 macOS 上通过只读 FUSE 挂载暴露允许访问的 Vault 字段。

请在回收授权之前、且其 Token 仍然有效时使用此选项。无论你是否持有所有者 Token，`mount-vault` 始终都需要 Vault 委派 Token。如果你只有所有者 Token，请先按[委派有限访问权限](#delegate-limited-access)中的说明为自己创建一个授权。将委派 Token 作为 `TI_VAULT_TOKEN` 提供，并按上述说明设置文件系统 ID 和 region。然后创建本地挂载目录并挂载 Vault：

```shell
mkdir -p /path/to/vault

ti fs-vault mount-vault \
  --mount-path /path/to/vault
```

允许访问的 Secret 字段会作为文件出现在挂载路径下。例如：

```text
/path/to/vault/db-prod/DB_URL
```

能够访问该挂载的进程都可以读取允许访问的 Secret 值，因此请将对该挂载的访问限制在预期工作负载范围内。

在卸载之前，请先下线正在使用这些已挂载 Secret 的进程：

```shell
ti fs-vault unmount-vault \
  --mount-path /path/to/vault
```

Vault 挂载需要 FUSE，且在 Windows 上不可用。直接读取 Secret 和 `run-with-secret` 不需要挂载。

## 审计并回收访问权限 {#audit-and-revoke-access}

回到所有者环境中，查看 `deploy-agent` 最近对 `db-prod` 的访问情况：

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20
```

当不再需要委派访问时，使用 `create-grant` 返回的授权 ID 回收该授权：

```shell
ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason task-complete
```

回收授权会阻止委派 Token 为新的操作授予权限。它无法移除某个进程已经读取过的 Secret 值。

在将该授权视为已退役之前，请先在委派环境中验证回收结果。在设置了 `TI_VAULT_TOKEN` 为委派 Token 的 shell 中，等待大约 10 秒以便认证缓存更新，然后使用同一个 Token 重试一个原本允许的操作：

```shell
ti fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- printenv DB_URL
```

预期会出现认证或授权错误（例如 `unauthorized`、`permission denied` 或 `grant revoked`）。如果该命令仍然返回 Secret 值，请确认你向 `delete-grant` 传入了正确的授权 ID，等待超过缓存间隔后再重试。网络错误、超时或文件系统缺失错误都不能确认已回收；只有明确的认证失败才可以。

如果该授权是通过 Vault 挂载授予访问权限的，请先卸载委派侧的 Vault 挂载，然后使用同一个 Token 重新挂载。一个仍在运行的 Vault 挂载会在委派侧保持其授权状态，不会在每次读取时重新检查该授权。

## 清理示例 {#clean-up-the-example}

在卸载并回收示例授权后，删除测试 Secret 和临时文件：

```shell
ti fs-vault delete-secret --secret-name db-prod
rm "$secret_dir/DB_URL" "$secret_dir/PASSWORD"
rmdir "$secret_dir"
```

## 安全建议 {#security-recommendations}

- 仅向工作流所需的 Secret 字段授权访问，并使用尽可能短的 TTL。
- 如果应用程序可以通过环境变量接收凭证，优先使用 `run-with-secret`。
- 不要在日志、源代码版本控制或命令行参数中暴露所有者 Token 或委托 Token。
- 当任务完成或不再需要访问时，及时回收授权。

## 后续内容 {#what-s-next}

- [将 File System Vault Secrets 委托给 Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)