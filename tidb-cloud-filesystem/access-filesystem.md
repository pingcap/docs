---
title: 访问现有文件系统
summary: 了解如何从当前机器、另一台机器、CI 作业或代理环境访问现有文件系统。
---

# 访问现有文件系统

在 TiDB Cloud Filesystem 中，你可以使用本地存储的 Token，或使用为另一台机器或环境提供的 Token 来访问现有文件系统：

- 如果你已在当前机器上使用 TiDB Cloud CLI (`ti`) 创建该文件系统，或已导入其 Token，则 CLI 可以使用已存储的 Token。
- 如果你是在另一台机器、CI 作业或代理环境中工作，请为该环境提供文件系统 Token 和 Region。

## 前提条件 {#prerequisites}

开始之前，请先[安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)，并确保你拥有该文件系统的访问权限。有关 owner Token 和范围受限 Token 及其权限的信息，请参见[授权](/tidb-cloud-filesystem/filesystem-authorization.md)。

## 在同一台机器上继续使用文件系统 {#continue-using-a-file-system-on-the-same-machine}

如果你在当前机器上使用 `ti` 创建了该文件系统，或者之前已导入其 Token，则 CLI 已经在本地存储了一个 Token。

环境变量 `TI_FS_TOKEN` 和 `TI_REGION_CODE` 会覆盖本地存储的 Token 和 Region。

清除这些覆盖项，然后选择其 Token 已存储在本地的文件系统：

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
```

</div>

</SimpleTab>

列出文件系统根目录。如果存储的 Token 的作用域限定在某个目录，请将 `/` 替换为该目录的路径：

```shell
ti fs list-files --path /
```

设置 `TI_FS_FILE_SYSTEM_ID` 会为当前 shell 中后续的命令选择该文件系统。它不会更改或（权限）回收任何文件系统 Token。

或者，你也可以为单个命令选择文件系统：

```shell
ti fs list-files --file-system-id "<file-system-id>" --path /
```

## 从其他环境访问文件系统 {#access-a-file-system-from-another-environment}

在其他环境中，请提供 Token 和 Region。对于 CI 或代理，请从 Secret 管理器注入 `TI_FS_TOKEN`，并在每个进程中设置 `TI_REGION_CODE`。跳过输入提示，并清除 `TI_FS_FILE_SYSTEM_ID` 以移除之前的文件系统选择。

在交互式终端中，在提示符处输入 Token；输入内容会被隐藏：

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'File system token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_FILE_SYSTEM_ID -ErrorAction SilentlyContinue
$env:TI_REGION_CODE = "<filesystem-region-code>"
$env:TI_FS_TOKEN = [System.Net.NetworkCredential]::new(
  "", (Read-Host "File system token" -AsSecureString)
).Password
```

</div>

</SimpleTab>

该 Token 用于标识文件系统。你不需要单独的文件系统 ID、已配置的 CLI 配置（Profile），也不需要 TiDB Cloud API keys 即可访问文件。

然后，你可以运行该 Token 所允许的命令。例如：

```shell
ti fs list-files --path "<allowed-path>"
```

范围受限 Token 只能访问其作用域中包含的路径和操作。如果该 Token 是由其他用户或管理员提供给你的，请确认你被允许使用哪些路径和操作。

如果你需要为其他环境创建 Token，请参见[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

## 在文件系统之间切换 {#switch-between-file-systems}

要在本地存储的 Token 之间切换，请清除 Token 和 Region 覆盖项，并更改文件系统 ID：

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<another-file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<another-file-system-id>"
```

</div>

</SimpleTab>

CLI 会使用为所选文件系统存储的 Token 和 Region。`TI_FS_TOKEN` 和 `TI_REGION_CODE` 会覆盖这些值；如果其中任一项仍设置为另一个文件系统或 Region 的值，就会导致不匹配。

一个文件系统可以拥有多个远程 Token，而每个 CLI 配置（Profile）对于每个文件系统最多只存储一个已选择的本地 Token。更改 CLI 使用的文件系统或本地 Token，不会禁用或（权限）回收其他远程 Token。

## 凭据选择 {#credential-selection}

在大多数工作流中，建议使用上述方法之一，而不是在每条命令中都显式指定凭据。

如果存在多个 Token 来源，`ti` 会按以下顺序选择 Token：

1. `--fs-token`
2. `TI_FS_TOKEN`
3. 所选文件系统对应的本地存储 Token

有关完整的文件系统和凭据选择规则，请参见[TiDB Cloud CLI 配置与凭据](/ai/ti/reference/ti-configuration-and-credentials.md#file-system-credentials-and-remote-inventory)。

## 后续操作 {#what-s-next}

- [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)
- [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)