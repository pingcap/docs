---
title: 在 TiDB Cloud Filesystem 中管理文件系统
summary: 了解如何使用 TiDB Cloud 控制台或 TiDB Cloud CLI 管理文件系统、在控制台中重命名文件系统，以及检查 CLI 访问。
aliases: ['/zh/ai/manage-filesystem-resources']
---

# 在 TiDB Cloud Filesystem 中管理文件系统

你可以使用 [TiDB Cloud 控制台](https://tidbcloud.com/) 或 [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) 在 TiDB Cloud Filesystem 中创建、查看和删除文件系统。控制台还支持重命名文件系统；CLI 则提供访问诊断功能。

有关命令语法、（命令行）参数和输出字段，请参见 [`ti fs` 命令参考](/ai/ti/reference/ti-filesystem.md)。

## 前提条件 {#prerequisites}

- 如需使用 [TiDB Cloud 控制台](https://tidbcloud.com/) 管理文件系统，请登录控制台并选择你的组织。
- 如需使用 TiDB Cloud CLI (`ti`) 管理文件系统，请按照[通过 CLI 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)安装 `ti` 并配置访问。

## 创建文件系统 {#create-a-file-system}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 创建文件系统。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)左侧导航栏中，选择你的组织，然后点击 **File Systems**。
2. 在右上角，点击 **Create File System**。
3. 在 **Create File System** 页面，输入文件系统名称，并选择 **Cloud Provider** 和 **Region**。
4. （可选）在摘要中查看并修改使用限制。

    如需修改使用限制，请先为你的组织添加信用卡。若未添加信用卡，则在创建期间无法修改免费额度限制。更多信息，请参见[管理使用限制](/tidb-cloud-filesystem/manage-filesystem-limits.md)。

5. 点击 **Create**。**Your File System is Ready!** 对话框会提供可选步骤，用于安装 TiDB Cloud CLI 以及在 macOS 或 Linux 上挂载文件系统。挂载命令中的默认所有者 Token 只会显示一次；请在关闭对话框前妥善保存。

</div>

<div label="CLI" value="cli">

创建文件系统并等待其就绪：

```shell
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait
```

从输出中，你可以在 `file_system_id` 字段中获取文件系统 ID，并在 `fs_token` 字段中获取文件系统所有者 Token。CLI 会自动将文件系统所有者 Token 存储到本地。

复制返回的 `file_system_id`，并在当前 shell 中为后续命令选择该文件系统：

```shell
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

设置 `TI_FS_FILE_SYSTEM_ID` 后，后续命令即可识别目标文件系统，而无需在每条命令中都指定 `--file-system-id`。对于数据访问命令，CLI 会使用为所选文件系统保存在本地的文件系统 Token。

> **Warning:**
>
> `fs_token` 中的文件系统所有者 Token 明文仅会在 Token 签发时返回一次。请将其视为 Secret，不要在日志、issue 或源码管理中暴露。如果你需要在另一台机器上使用该 Token，或存储备份，请将其安全地保存在 Secret 管理器中。更多信息，请参见[管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

> **Note:**
>
> 请勿在文件系统标签中放入凭证、连接字符串、私有路径或个人数据。

</div>

</SimpleTab>

## 列出并查看文件系统 {#list-and-inspect-file-systems}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 列出文件系统并查看其详细信息。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)左侧导航栏中，选择你的组织，然后点击 **File Systems**。
2. 在 [**File Systems**](https://tidbcloud.com/filesystems) 页面，选择云服务提供商和 Region，以列出该位置中的文件系统。你可以使用 **Search Name** 或 **Status** 缩小列表范围。

如需查看某个文件系统的详细信息，点击其名称进入概览页面。

如需更改其显示名称，点击概览页面右上角的 **...**，然后选择 **Rename**。

</div>

<div label="CLI" value="cli">

列出当前 Region 中可用的文件系统：

```shell
ti fs list-file-systems --output text
```

查看某个文件系统的元信息：

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

如果你使用多个文件系统，可以通过以下任一方式指定目标文件系统：

- 在单条命令中传入 `--file-system-id "<file-system-id>"`。
- 设置 `TI_FS_FILE_SYSTEM_ID`，以便在当前 shell 中为后续命令选择一个文件系统。

CLI 不会根据文件系统数量或本地存储的凭证自动选择文件系统。

当前 CLI 不提供在创建后更改文件系统显示名称或标签的命令。请在创建文件系统时确定这些值。

</div>

</SimpleTab>

## 检查访问 {#check-access}

检查 CLI 是否可以访问某个文件系统：

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

结果包含整体 `status`，并会检查本地凭证、端点选择、随附的文件系统运行时以及远程连接性。

- `passed` 表示所有检查均已成功。
- `warning` 或 `failed` 表示存在需要关注的检查项。

有关常见的访问和连接问题，请参见[排查 TiDB Cloud Filesystem 故障](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。

## 删除文件系统 {#delete-a-file-system}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 删除文件系统。

> **Warning:**
>
> 删除文件系统会永久移除其远程数据。删除前，请停止正在使用该文件系统的应用程序，并成功卸载所有处于活动状态的本地挂载。有关如何安全完成待处理写入的信息，请参见[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. 在 TiDB Cloud 控制台中，打开你组织的 [**File Systems**](https://tidbcloud.com/filesystems) 页面，然后为目标文件系统选择 **Cloud Provider** 和 **Region**。
2. 在目标文件系统所在行中，点击 **...**，然后选择 **Delete**。
3. 在确认对话框中，按 `region/name` 的格式输入要求的 Region 和文件系统名称，然后点击 **I understand, delete it.**

删除是异步进行的。提交请求后，在删除完成之前，该文件系统可能仍会显示，状态为 `deleting`。

</div>

<div label="CLI" value="cli">

按 ID 删除文件系统：

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

文件系统删除是异步进行的。服务接受请求后，CLI 会将文件系统状态报告为 `deleting`，并移除本地存储的对应凭证。该状态表示删除已开始，并不表示远程文件系统及其数据已经被移除。

</div>

</SimpleTab>

## 接下来做什么 {#what-s-next}

- [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)，以生成、委派、轮转或回收文件系统访问权限。
- [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md)，以复制、读取、组织和搜索文件系统数据。
- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)，以通过本地目录访问远程文件。
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)，了解命令语法、（命令行）参数和输出字段。