---
title: 管理文件系统 Token
summary: 了解如何导入、创建、限定作用域、检查、轮转和（权限）回收文件系统 Token，以控制用户和自动化程序的访问。
aliases: ['/zh/ai/manage-filesystem-tokens']
---

# 管理文件系统 Token

在 TiDB Cloud Filesystem 中，你可以使用文件系统 Token 为用户、应用程序和自动化程序授予对文件系统的访问权限，而无需共享你的 TiDB Cloud API 凭据。

- [所有者 Token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens)授予对文件系统的完全访问权限。
- [范围受限 Token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens)将访问限制在特定路径和操作上。

## 前提条件 {#prerequisites}

开始之前，请确保：

- 你可以访问 TiDB Cloud Filesystem 中现有的文件系统。如果还没有，请按照[通过控制台快速开始](/tidb-cloud-filesystem/filesystem-quick-start-console.md)或[通过 CLI 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)创建一个。
- 对于 CLI 操作，请先[安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。

要使用 CLI 列出、启用、禁用或删除 Token，请通过 `TI_FS_TOKEN` 或 `--fs-token` 提供一个所有者 Token，或者使用 TiDB Cloud API 凭据并显式指定 `--file-system-id`。这些操作不会自动使用本地存储的 Token。范围受限 Token 的生成可以使用本地存储的所有者 Token。下面各节会说明额外要求。

> **Note:**
>
> 请安全存储文件系统 Token。创建或刷新 Token 时，其明文只会返回一次，之后无法再次获取。

## 导入现有 Token {#import-an-existing-token}

如果你已经拥有一个文件系统 Token，包括在 TiDB Cloud 控制台创建文件系统时显示的默认所有者 Token，请将其明文保存到安全文件中，并将其导入到本地 CLI 凭据存储中：

```shell
ti fs import-file-system-token --from-file ./fs-token --region "<file-system-region>"
```

CLI 会验证该 Token，从中提取文件系统 ID，验证连通性，并将 Token 存储到本地。如果该 Token 仍可通过 `TI_FS_TOKEN` 使用，则无需导入也可以将其用于 CLI 命令。

## 生成所有者 Token {#generate-an-owner-token}

在创建文件系统时，TiDB Cloud 控制台会提供一个所有者 Token。若要生成额外的所有者 Token，请使用 CLI。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

在你创建文件系统时，TiDB Cloud 控制台会创建一个默认的所有者 Token。其明文只会显示在 **Your File System is Ready!** 对话框中。

若要获取额外的所有者 Token，请使用 **CLI** 页签。

</div>

<div label="CLI" value="cli">

当你使用 CLI 创建文件系统时，它会返回一个不过期的所有者 Token，将其存储到本地，并在后续命令中使用它。

当另一个受信任环境需要完全访问权限时，可以生成额外的所有者 Token。

要生成额外的所有者 Token，请先配置 TiDB Cloud API 凭据并获取文件系统 ID。

生成 Token，并安全保存其一次性返回的明文响应：

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h \
  --query fs_token \
  --output text > ./ci-token
```

`--query fs_token --output text` 会仅输出 Token 值本身，这正是 `import-file-system-token --from-file` 所期望的格式。如果不使用这些选项，该命令会输出完整的 JSON 响应，导入该文件时会因 `invalid FS token format` 而失败。后续（权限）回收该 Token 所需的 Token ID，可随时通过 `ti fs list-file-system-tokens` 获取。

CLI 默认不会将生成的 Token 存储到本地。若要将其存储到本地，请在前述命令中添加 `--store-locally`。如果该文件系统已存储了其他 Token，还需要同时添加 `--replace`。

</div>

</SimpleTab>

## 生成并委派范围受限 Token {#generate-and-delegate-a-scoped-token}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 生成范围受限 Token，并将其提供给其他用户、应用程序或代理。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

如果你希望将 Token 限制到特定目录，请在生成 Token 之前先创建该目录。

1. 在 TiDB Cloud 控制台中，进入 [**File Systems**](https://tidbcloud.com/filesystems) 页面，选择云服务提供商和 Region，然后点击目标文件系统的名称。
2. 在文件系统概览页中，点击左侧导航栏中的 **Access Tokens**。
3. 在右上角点击 **Create Token**。
4. 通过提供以下信息来配置 Token：

    - **Token name**：输入 Token 名称。
    - **Access path (optional)**：指定访问路径，以将 Token 的访问限制到特定目录。如果将该路径留空，则 Token 适用于 `/`。
    - **Expiration**：选择 Token 的过期时间。默认值为一小时。
    - **Permission**：仅选择该 Token 所需的操作。详情请参见[授权](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens)。

5. 点击 **Create**。
6. 在显示的对话框中，复制 Token 并在点击 **Done** 之前安全保存。其明文只会显示一次。

将该 Token 和文件系统 Region 提供给接收环境。如果使用限制到某个目录的 Token 进行挂载，请将 CLI 的 `--remote-path` 选项设置为该目录。

</div>

<div label="CLI" value="cli">

在受信任的机器上，使用所有者 Token 生成范围受限 Token。通过 `--fs-token` 或 `TI_FS_TOKEN` 提供所有者 Token，或者使用为所选文件系统本地存储的所有者 Token。

在使用以下示例之前，如果远程 `/workspace` 目录不存在，请先创建它。使用本地存储的所有者 Token，为代理授予该目录中的文件读、列出和写入权限：

```shell
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

通过 Secret 管理器传输该 Token。在接收环境中，提供范围受限 Token 和文件系统 Region：

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<filesystem-region-code>"

ti fs list-files --path /workspace
```

`--allow` 的值使用 `<path>:<comma-separated-operations>` 格式。支持的操作包括 `read`、`list`、`search`、`write` 和 `delete`；其中 `search` 需要 `read`。在此示例中，该 Token 允许对 `/workspace` 下执行 `read`、`list` 和 `write` 操作。

要使用此 Token 挂载该目录，请指定 `--remote-path /workspace`。限制为 `/workspace` 的 Token 不能挂载文件系统根目录 `/`。

有关范围受限权限和凭据选择的更多信息，请参见[授权](/tidb-cloud-filesystem/filesystem-authorization.md)。

</div>

</SimpleTab>

## 检查并更改 Token 状态 {#inspect-and-change-token-status}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 查看 Token 详情，并激活或停用 Token。

> **Warning:**
>
> 在停用、轮转或删除被活动挂载使用的 Token 之前，请先停止向该挂载写入数据的应用程序，并成功卸载该挂载。CLI 可以检测已知的本地挂载，但无法发现其他机器上的挂载。在更改 Token 之前，请与这些机器协调。更多信息，请参见[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. 在 TiDB Cloud 控制台中，进入 [**File Systems**](https://tidbcloud.com/filesystems) 页面，选择云服务提供商和 Region，然后点击目标文件系统的名称。
2. 在文件系统概览页中，点击左侧导航栏中的 **Access Tokens**。
3. 在 **Access Tokens** 页面中，你可以查看每个 Token 的 ID、状态、访问路径、权限、过期时间和创建时间。
4. 若要暂停某个 Token，请在目标 Token 所在行点击 **...**，然后选择 **Deactivate**。若要恢复已停用的 Token，请点击 **...**，然后选择 **Activate**。

</div>

<div label="CLI" value="cli">

对于仅使用所有者 Token 的环境，在运行以下命令之前，请将 `TI_FS_TOKEN` 设置为所有者 Token，并将 `TI_REGION_CODE` 设置为文件系统所在的 Region。请将管理凭据与提供给接收方的范围受限 Token 分开。范围受限 Token 不能管理其他 Token。

列出文件系统 Token 的非 Secret 元信息：

```shell
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

输出中不包含 Token 明文。如果你丢失了所有者 Token，请使用 TiDB Cloud API 凭据生成替代 Token。你无法通过列出 Token 来恢复原始 Token。

使用 [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) 可临时暂停 Token，使用 [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) 可恢复 Token。它们分别对应控制台中的 **Deactivate** 和 **Activate**。

在使用所有者 Token 认证时，这两个命令只能更改范围受限 Token。若要启用或禁用所有者 Token，请使用 TiDB Cloud API 凭据，指定 `--file-system-id`，并取消设置 `TI_FS_TOKEN`，以免其覆盖 API 凭据。该请求不要提供 `--fs-token`。在验证访问之前，请等待大约 10 秒使更改生效。

</div>

</SimpleTab>

## 轮转或回收 Token {#rotate-or-revoke-a-token}

要轮转 Token，请使用 CLI，因为 TiDB Cloud 控制台不提供 `refresh-file-system-token` 操作。要回收 Token，可以使用 CLI 或控制台。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

要在 TiDB Cloud 控制台中替换范围受限 Token，请先[创建一个新的 Token](#generate-and-delegate-a-scoped-token)，并为其设置所需的路径、权限和过期时间。在停用旧 Token 之前，先分发并验证新 Token。然后，进入目标 Filesystem 的 **Access Tokens** 页面，找到旧 Token 所在行，点击 **...**，然后选择 **Delete**。

要替换所有者 Token，请先[使用 CLI 生成另一个所有者 Token](#generate-an-owner-token)，然后再在 TiDB Cloud 控制台中删除旧 Token。

</div>

<div label="CLI" value="cli">

使用 [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) 轮转文件系统 Token。

当你刷新本地存储的 Token 时，CLI 会自动更新本地凭证。当你刷新通过 `--fs-token` 或 `TI_FS_TOKEN` 提供的 Token 时，CLI 会在命令输出中返回新的 Token，而不会将其存储到本地。

> **Note:**
>
> 如果刷新请求超时，服务可能已经轮转了 Token，但没有将新值返回给你。不要使用旧 Token 重试。请使用 TiDB Cloud API 凭证生成新的所有者 Token。

在停用某个 Token 之前，请先分发并验证其替代 Token。然后，使用其 token ID 回收旧 Token：

```shell
ti fs delete-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-id "<token-id>"
```

如果被删除的 Token 与本地存储的 Token 匹配，CLI 会自动移除本地凭证。Token 变更可能需要一些时间才能传播到授权缓存中。

禁用或回收所有者 Token 不会自动回收基于它生成的范围受限 Token。必要时，请单独检查并回收这些范围受限 Token。

</div>

</SimpleTab>

## 后续操作 {#what-s-next}

- [共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)
- [了解自动化和 AI agent 工作流](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)