---
title: 在 TiDB Cloud Filesystem 中使用文件和目录
summary: 了解如何在控制台中查看文件元信息，以及如何使用 TiDB Cloud CLI 上传、下载、读取、组织和搜索文件。
aliases: ['/zh/ai/work-with-filesystem-data']
---

# 在 TiDB Cloud Filesystem 中使用文件和目录

在 TiDB Cloud Filesystem 中，你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/)中浏览文件和目录元信息，也可以使用 TiDB Cloud CLI (`ti`) 在不挂载文件系统的情况下上传、下载、读取、组织和搜索文件。有关所有命令和选项，请参见 [`ti fs` 参考文档](/ai/ti/reference/ti-filesystem.md)。

如果你将[挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)到本地机器，则可以像使用本地文件系统一样操作文件和目录。

## 前提条件 {#prerequisites}

以下前提条件适用于 CLI 操作。如果你只需要在 TiDB Cloud 控制台中浏览文件元信息，请参见[查看文件](#view-files)。

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- [创建文件系统](/tidb-cloud-filesystem/manage-filesystem-resources.md)或获取现有文件系统的访问权限。
- 选择文件系统，并使其 Token 可供 `ti` 使用。有关可用的访问方式，请参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

## 查看文件 {#view-files}

你可以使用 TiDB Cloud 控制台或 TiDB Cloud CLI 浏览文件和目录并查看其元信息。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你所在组织的 [**File Systems**](https://tidbcloud.com/filesystems) 页面，选择云服务提供商和 region，然后点击目标文件系统的名称。
2. 在左侧导航栏中，点击 **Files**。该页面会列出目录和文件，以及它们的类型、大小和修改时间。
3. 展开目录以浏览其内容，使用 **Search** 过滤当前可见的文件树，或点击文件名查看其元信息。

控制台会显示文件元信息。若要读取文件内容或更改文件和目录，请使用 CLI 命令或[挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)。

</div>

<div label="CLI" value="cli">

列出目录内容：

```shell
ti fs list-files --path /reports --output text
```

输出示例：

```text
NAME       TYPE  SIZE  MTIME
archive    dir   0     0
report.md  file  23    0
```

查看文件或目录的元信息：

```shell
ti fs describe-file --path /reports/report.md
```

</div>

</SimpleTab>

## 上传和下载文件 {#upload-and-download-files}

将本地文件上传到文件系统：

```shell
ti fs copy-file \
  --from-local ./report.md \
  --to-remote /reports/report.md
```

从文件系统下载文件：

```shell
ti fs copy-file \
  --from-remote /reports/report.md \
  --to-local ./downloads/report.md \
  --create-parents
```

你还可以使用 `copy-file` 在文件系统内部复制文件或目录、通过标准输入或标准输出传输数据、向文件追加内容，或恢复中断的传输。

如需递归复制目录，请使用 `--recursive`。有关所有支持的复制操作和选项，请参见 [`copy-file` 参考文档](/ai/ti/reference/ti-fs-copy-file.md)。

## 读取文件 {#read-files}

读取文件的完整内容：

```shell
ti fs read-file --path /reports/report.md
```

该命令会将文件内容直接写入标准输出，而不会将其包装为 JSON。

如果只想读取文件的一部分，请使用 `--offset` 和 `--length`。例如，以下命令读取前 1024 字节：

```shell
ti fs read-file \
  --path /reports/report.md \
  --offset 0 \
  --length 1024
```

## 组织文件和目录 {#organize-files-and-directories}

创建目录：

```shell
ti fs create-directory --path /reports/archive
```

将文件移动到另一路径：

```shell
ti fs move-file \
  --from-remote /draft.md \
  --to-remote /reports/final.md
```

删除文件或目录：

```shell
ti fs delete-file --path /scratch --recursive
```

> **Warning:**
>
> `delete-file --recursive` 会永久删除指定目录及其内容。删除前请验证路径。你可以使用 `--dry-run` 在不删除数据的情况下验证请求。

对于需要 POSIX 风格元信息或链接的工作流，你还可以使用 [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md)、[`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md) 和 [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md)。

## 搜索文件和内容 {#search-files-and-content}

使用 `search-file-content` 按内容查找文件：

```shell
ti fs search-file-content \
  --path /reports \
  --pattern "TODO"
```

`--pattern` 是文本查询，不是正则表达式或 glob 模式。使用 `--limit` 可以控制返回结果的最大数量。

详情请参见 [`search-file-content` 参考文档](/ai/ti/reference/ti-fs-search-file-content.md)。

如果你了解的是文件本身的信息而不是其内容，请使用 `find-files`。你可以按文件名、类型、标签、大小或修改时间进行过滤。

例如，查找带有 `stage=review` 标签的 Markdown 文件：

```shell
ti fs find-files \
  --path /reports \
  --file-name-pattern "*.md" \
  --tag stage=review
```

标签是在上传文件时通过 `copy-file --tag key=value` 设置的。对于同一路径，如果你在后续上传时再次提供 `--tag`，则会替换之前的标签，而不是在其基础上追加。

结果会列出匹配的路径。空表表示没有匹配项，而不是命令执行失败。

有关所有可用过滤条件，请参见 [`find-files` 参考文档](/ai/ti/reference/ti-fs-find-files.md)。

## 在脚本中使用命令输出 {#use-command-output-in-scripts}

在使用命令输出之前，请先检查退出状态。`read-file` 和 `copy-file --to-stdout` 输出的是文件内容流，而不是 CLI 元信息。捕获这些内容时，请将 stderr 与其分开。

在 `ti` v0.2.6 和 v0.2.7 中，`create-directory` 即使在使用 `--output json` 时，也可能会在 JSON 结果之前输出一行 `created ...`。因此，它的输出无法作为单个 JSON 文档进行解析。请先检查退出状态，然后使用 `describe-file` 或 `list-files` 验证目录。在脚本中依赖其输出格式之前，请先检查你已安装版本的实际输出格式。

## 后续操作 {#what-s-next}

- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)，通过本地目录和现有本地工具操作文件系统数据。
- [管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)，在将隔离变更应用到基础文件系统之前先进行创建和检查。
- [在多台机器之间共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)，为另一台机器或环境提供对文件系统的访问权限。
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)，查看完整的命令语法和选项。