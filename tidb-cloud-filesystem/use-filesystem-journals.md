---
title: Use TiDB Cloud Filesystem Journals
summary: Learn how to record, read, search, and verify ordered events from agent and automation workflows in a TiDB Cloud Filesystem.
aliases: ['/ai/use-filesystem-journals']
---

# Use TiDB Cloud Filesystem Journals

Use a journal when you need an ordered, persistent record of events from an agent or automation workflow. For example, a journal can record when a task starts or finishes, which agent performed an action, and when work is handed off between agents or processes. You can later read or search these events to understand what happened during the workflow.

Journal entries are append-only: new events are added as new entries, and existing entries cannot be modified. The entries are also linked through a hash chain, which lets you verify that the recorded history remains intact and in order.

This guide shows you how to create a journal, record events, read and search recorded events, and verify the journal history.

Journals are intended for workflow events and history. Store artifacts, working files, and other workflow outputs as regular files in the Filesystem. A journal records what happened; it does not replay workflow actions or replace the files produced by the workflow.

> **Note:**
>
> The current `ti` CLI does not provide a command to delete individual journals. Do not record secrets or other data that you might need to remove later.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing TiDB Cloud Filesystem.
- Make the Filesystem and its token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

## Create a journal

Create a journal for the workflow you want to record:

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

Because no journal ID is specified, the service generates one. Save the returned journal ID—you will use it to append, read, and verify entries in this journal.

The journal kind, title, and actor provide context that can also help you find related workflow records later.

## Append entries

Append an event to the journal:

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --entry-json '{"type":"review_started"}'
```

Each entry needs a `type`, unless you provide one with `--entry-type`. You can also include fields such as `summary`, `actor`, and `occurred_at`.

The example above omits `--idempotency-key` for brevity. If your workflow might retry the same append operation, provide an idempotency key and reuse the same key for every retry. This prevents the retry from recording the same event more than once:

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --idempotency-key review-started \
  --entry-json '{"type":"review_started"}'
```

For all supported fields and input formats, see the [`append-journal-entries` reference](/ai/ti/reference/ti-fs-journal-append-journal-entries.md).

## Read and search entries

To review the history of one journal, read its entries:

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>"
```

Entries are returned in sequence order, so you can follow the workflow in the order it was recorded.

To find events across journals in the selected Filesystem, use `search-journal-entries`. For example, the following command finds `review_started` events and returns their entry contents:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --include-entries
```

Unlike `read-journal-entries`, the search command is not limited to one journal. Use filters such as journal kind, actor, entry type, labels, or time range to narrow the results.

## Verify a journal

To check that the stored journal history is internally consistent, verify its hash chain:

```shell
ti fs-journal verify-journal \
  --journal-id "<journal-id>"
```

A successful verification confirms that the stored sequence and hash chain are consistent.

Hash-chain verification checks the integrity of the recorded journal history. It does not prove that the original event information recorded by an agent or application was accurate.

## What's next

- [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md) for an end-to-end agent workflow example.
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md) for all journal commands and options.
