---
title: 在文件系统中使用 Journals
summary: 了解如何创建文件系统日志（Journal）、记录工作流事件、对读取和搜索结果进行分页，以及验证已记录的历史。
aliases: ['/zh/ai/use-filesystem-journals']
---

# 在文件系统中使用 Journals

在 TiDB Cloud Filesystem 中，你可以使用文件系统日志（Journal）来按顺序、持久地记录 agent 和自动化事件，例如任务开始、完成和交接。你可以读取或搜索这些条目，以追踪发生了什么，以及每个操作是由哪个 agent 执行的。

条目是仅追加的：你可以添加事件，但不能修改已有条目。条目之间通过哈希链关联，因此你可以验证其完整性和顺序。

将产物和工作文件作为文件系统中的常规文件存储。日志（Journal）用于记录事件；它不会重放操作，也不会替代工作流输出。

> **Note:**
>
> 当前的 `ti` CLI 不提供删除单个日志（Journal）的命令。请不要记录 Secret 或其他你之后可能需要删除的数据。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 你可以访问 TiDB Cloud Filesystem 中一个现有的文件系统。
- 使该文件系统及其 Token 可供 `ti` 使用。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

## 创建日志（Journal） {#create-a-journal}

为你要记录的工作流创建一个日志（Journal）：

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

如果你省略日志 ID，服务会自动生成一个。请保存返回的 ID，以便后续追加、读取和验证条目。

日志类型、标题和 actor 可提供上下文信息，也有助于你稍后查找相关的工作流记录。

## 追加条目 {#append-entries}

向日志（Journal）追加一个事件：

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --idempotency-key review-started \
  --entry-json '{"type":"review_started"}'
```

每个条目都需要一个 `type`，除非你通过 `--entry-type` 提供。你还可以包含 `summary`、`actor` 和 `occurred_at` 等字段。

重试此事件时，复用相同的 `--idempotency-key` 以避免重复条目。对于不同事件，请使用新的 key。

有关所有支持的字段和输入格式，请参见 [`append-journal-entries` 参考文档](/ai/ti/reference/ti-fs-journal-append-journal-entries.md)。

## 读取和搜索条目 {#read-and-search-entries}

### 读取单个日志（Journal） {#read-one-journal}

要查看某个日志（Journal）的历史记录，请读取其条目：

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>"
```

默认情况下，条目会按顺序返回，每次调用最多返回 100 条。要获取下一页，请将 `<last-seq>` 替换为上一页最后一个返回条目的 `seq`：

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>" \
  --after-seq "<last-seq>" \
  --limit 100
```

从每一页的最后一个序号继续读取，直到某次成功响应返回空的 `entries` 数组为止。如果请求失败，请从相同序号重试。你在读取时，活动中的日志（Journal）仍可能接收更多条目；分页不会创建快照。

### 跨日志（Journal）搜索 {#search-across-journals}

在所选文件系统中的多个日志（Journal）里查找 `review_started` 事件：

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100
```

默认情况下，搜索每次调用最多返回 100 个匹配项。将最后一个匹配项的 `cursor` 传给下一次请求，并保持相同的过滤条件：

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100 \
  --cursor "<last-match-cursor>"
```

持续进行，直到某次成功响应返回空的 `matches` 数组为止。如果请求失败，请使用相同的 cursor 重试。若要将搜索限制在固定时间范围内，请提供 RFC3339 格式的 `--since` 和 `--until` 值，并在分页过程中保持不变。

如果要获取包含完整条目内容的单页结果，请添加 `--include-entries`。分页时请省略该选项：这种输出不会保留匹配项 cursor。

若要单独获取某个匹配条目，请使用其 `journal_id` 调用 `read-journal-entries`，将 `--after-seq` 设置为该条目 `seq` 减一后的值，并将 `--limit` 设置为 `1`。例如，要读取序号为 `42` 的条目，请使用 `--after-seq 41 --limit 1`。

## 验证日志（Journal） {#verify-a-journal}

要检查已存储的日志（Journal）历史在内部是否一致，请验证其哈希链：

```shell
ti fs-journal verify-journal \
  --journal-id "<journal-id>"
```

验证成功表示已存储的序列和哈希链是一致的。但这并不能确认 agent 或应用程序所报告事件的准确性。

## 后续操作 {#what-s-next}

- [在文件系统日志中记录 Agent 工作流](/ai/ti/guides/ti-journal-agent-workflow-example.md)，查看端到端的 agent 工作流示例。
- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)，查看所有日志（Journal）命令和选项。