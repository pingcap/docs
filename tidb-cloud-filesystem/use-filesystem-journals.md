---
title: Use Journals in a File System
summary: Learn how to create file system journals, record workflow events, paginate read and search results, and verify the recorded history.
aliases: ['/ai/use-filesystem-journals']
---

# Use Journals in a File System

In TiDB Cloud Filesystem, you can use a file system journal to keep an ordered, persistent record of agent and automation events, such as task starts, completions, and handoffs. You can read or search the entries to trace what happened and which agent performed each action.

Entries are append-only: you can add events but cannot modify existing entries. A hash chain links the entries so you can verify their integrity and order.

Store artifacts and working files as regular files in the file system. A journal records events; it does not replay actions or replace workflow outputs.

> **Note:**
>
> The current `ti` CLI does not provide a command to delete individual journals. Do not record secrets or other data that you might need to remove later.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing file system in TiDB Cloud Filesystem.
- Make the file system and its token available to `ti`. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

## Create a journal

Create a journal for the workflow you want to record:

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

The service generates a journal ID when you omit it. Save the returned ID for appending, reading, and verifying entries.

The journal kind, title, and actor provide context that can also help you find related workflow records later.

## Append entries

Append an event to the journal:

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --idempotency-key review-started \
  --entry-json '{"type":"review_started"}'
```

Each entry needs a `type`, unless you provide one with `--entry-type`. You can also include fields such as `summary`, `actor`, and `occurred_at`.

Reuse the same `--idempotency-key` when retrying this event to avoid duplicate entries. Use a new key for a different event.

For all supported fields and input formats, see the [`append-journal-entries` reference](/ai/ti/reference/ti-fs-journal-append-journal-entries.md).

## Read and search entries

### Read one journal

To review the history of one journal, read its entries:

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>"
```

Entries are returned in sequence order, with at most 100 entries per call by default. For the next page, replace `<last-seq>` with the last returned entry's `seq`:

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>" \
  --after-seq "<last-seq>" \
  --limit 100
```

Continue from each page's last sequence until a successful response has an empty `entries` array. If a request fails, retry from the same sequence. An active journal can receive more entries while you read; pagination does not create a snapshot.

### Search across journals

Find `review_started` events across journals in the selected file system:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100
```

Search defaults to at most 100 matches per call. Pass the last match's `cursor` to the next request, keeping the same filters:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100 \
  --cursor "<last-match-cursor>"
```

Continue until a successful response has an empty `matches` array. If a request fails, retry with the same cursor. To limit the search to a fixed time range, supply RFC3339 `--since` and `--until` values and keep them unchanged across pages.

For a single page of full entry contents, add `--include-entries`. Omit it when paginating: that output does not retain match cursors.

To retrieve a matched entry separately, use `read-journal-entries` with its `journal_id`, set `--after-seq` to one less than the entry's `seq`, and set `--limit 1`. For example, to read the entry at sequence `42`, use `--after-seq 41 --limit 1`.

## Verify a journal

To check that the stored journal history is internally consistent, verify its hash chain:

```shell
ti fs-journal verify-journal \
  --journal-id "<journal-id>"
```

A successful verification confirms that the stored sequence and hash chain are consistent. It does not confirm the accuracy of events reported by an agent or application.

## What's next

- [Record an Agent Workflow in a File System Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md) for an end-to-end agent workflow example.
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md) for all journal commands and options.
