---
title: Record an Agent Workflow in a TiDB Cloud Filesystem Journal
summary: Create a journal, append structured agent events, search the workflow, and verify the journal hash chain.
---

# Record an Agent Workflow in a TiDB Cloud Filesystem Journal

This workflow records planning, tool calls, tests, retries, and handoffs as a structured, ordered, and verifiable event history. Use it when operators need to reconstruct what happened across workers instead of relying on scattered console output or a mutable status file that shows only the latest state.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

A Filesystem journal stores structured append-only entries with sequence information, searchable fields, optional idempotency keys, and hash-chain verification. Unlike a normal text file, journal entries cannot be edited or truncated after they are written, and producers do not need to implement their own parsing, concurrency, or retry-deduplication mechanism. Agents append semantic events such as `task.started` and `test.finished`; operators can query the workflow and verify the stored chain.

## Prerequisites

Select a Filesystem through a configured profile or FS token environment.

## Step 1. Create the journal

```bash
ti fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## Step 2. Append workflow events

```bash
ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

Specify an idempotency key when the workflow might retry the same append, and reuse that key for every retry of that logical operation. The service then avoids storing duplicate entries. When you omit the option, a new key is generated, which is appropriate for an append that you do not intend to retry.

## Step 3. Read and search

```bash
ti fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

ti fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

The ordered `read-journal-entries` result for `jrn-agent-demo` should include the start, test, and completion events.

> **Note:**
>
> `search-journal-entries` searches all journals in the selected Filesystem because it does not accept a journal ID. Another journal with the same labels and event fields can also match the search in this example.

The `--entry-type` and `--status` filters match the `type` and `status` fields in each `--entry-json` object. In this example, they select the entry whose payload contains `"type":"task.finished"` and `"status":"completed"`.

## Step 4. Verify integrity

```bash
ti fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

A successful result confirms the stored sequence and hash chain are consistent.

## Cleanup

Journals are append-only and currently have no delete command in the public `ti` command surface. For experiments that create disposable journals, use a dedicated test Filesystem and unique journal IDs such as `jrn-test-<run-id>`. Delete the containing Filesystem only when none of its files or journals are still needed.

## Security and operational notes

- Do not put API keys, passwords, SQL text containing secrets, or raw file contents in journal payloads.
- Hash-chain verification detects stored-chain inconsistency; it does not prove the original event was truthful.

## What's next

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
- [Delegate Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)
