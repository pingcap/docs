---
title: TiDB Cloud Filesystem Journal CLI Command Reference
summary: Reference every `ti fs-journal` command for creating, appending, reading, searching, and verifying journals.
---

# TiDB Cloud Filesystem Journal CLI Command Reference

`ti fs-journal` provides an append-only, verifiable ledger for agent and workflow events.

## Commands

| Command | Description |
|---|---|
| [`create-journal`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-create-journal.md) | Creates a journal. |
| [`append-journal-entries`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-append-journal-entries.md) | Appends events to a journal. |
| [`read-journal-entries`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-read-journal-entries.md) | Reads journal entries in sequence order. |
| [`search-journal-entries`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-search-journal-entries.md) | Searches journals and entries. |
| [`verify-journal`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-verify-journal.md) | Verifies the journal hash chain. |

## See also

- [Use TiDB Cloud Filesystem Journals](/ai/ti/guides/use-filesystem-journals.md)
- [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/reference/ti-journal-agent-workflow-example.md)
