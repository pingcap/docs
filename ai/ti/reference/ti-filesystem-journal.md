---
title: TiDB Cloud Filesystem Journal CLI Command Reference
summary: Reference every `ti fs-journal` command for creating, appending, reading, searching, and verifying journals.
---

# TiDB Cloud Filesystem Journal CLI Command Reference

`ti fs-journal` provides an append-only, verifiable ledger for agent and workflow events. Unlike a mutable text file, a journal assigns ordered sequence numbers, supports structured search, and maintains a hash chain that can detect alteration.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
ti fs-journal
├── create-journal
├── append-journal-entries
├── read-journal-entries
├── search-journal-entries
└── verify-journal
```

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `create-journal` | Creates a journal with an optional caller-provided ID, kind, actor, title, and labels. | `ti fs-journal create-journal --journal-kind agent --title "review task" --actor agent:reviewer` |
| `append-journal-entries` | Appends JSON entries from repeatable flags, JSON Lines stdin, or a JSON array. | `ti fs-journal append-journal-entries --journal-id jrn-demo --entry-json '{"type":"task.started"}'` |
| `read-journal-entries` | Reads ordered entries after a sequence number. | `ti fs-journal read-journal-entries --journal-id jrn-demo --after-seq 0 --limit 100` |
| `search-journal-entries` | Searches journals and entries by type, kind, actor, status, subject, label, or time. | `ti fs-journal search-journal-entries --entry-type task.started --include-entries` |
| `verify-journal` | Recalculates and verifies one journal's ordered hash chain. | `ti fs-journal verify-journal --journal-id jrn-demo --output text` |

## Prerequisites

Select a Filesystem by ID with locally stored credentials, or provide only `TI_FS_TOKEN` and `TI_REGION_CODE`; `TI_FS_FILE_SYSTEM_ID` is an optional assertion.

## Create a journal

```bash
ti fs-journal create-journal \
  --journal-id jrn-demo \
  --journal-kind agent \
  --title "demo task" \
  --actor agent:ti \
  --label env=dev
```

`--journal-id` is optional and generated when omitted. Labels are repeatable.

## Append entries

Append one or more JSON objects:

```bash
ti fs-journal append-journal-entries \
  --journal-id jrn-demo \
  --entry-json '{"type":"task.started","status":"running"}' \
  --entry-json '{"type":"tool.called","tool":"ti"}'
```

Use `--entry-type` as a default for entries without `type`, and add `--source` or repeatable `--subject` metadata. `--idempotency-key` makes a retry deterministic; the CLI generates one when omitted.

For pipelines, send JSON Lines on stdin, or use `--json-array` for a JSON array.

## Read and search

Read entries after a sequence:

```bash
ti fs-journal read-journal-entries \
  --journal-id jrn-demo \
  --after-seq 0 \
  --limit 100
```

Search across journals:

```bash
ti fs-journal search-journal-entries \
  --entry-type task.started \
  --journal-kind agent \
  --label env=dev \
  --include-entries
```

Search also supports status, actor, subject, `--since`, `--until`, `--limit`, and pagination cursor filters.

## Verify integrity

```bash
ti fs-journal verify-journal \
  --journal-id jrn-demo \
  --output text
```

Verification recalculates the ordered hash chain and reports whether the entries are internally consistent. It does not assert that the event payload was truthful when originally appended.

## What's next

- [Record an Agent Workflow in a Journal](/ai/ti/reference/ti-journal-agent-workflow-example.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
