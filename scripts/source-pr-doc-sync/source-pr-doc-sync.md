# Source PR Docs Sync Automation

This document describes how to operate the source-PR docs sync workflow that maps merged code PRs to docs-cn update PRs.

## Overview

The workflow file is `.github/workflows/source-pr-doc-sync.yml`.

It runs in two stages:

1. `scan`: collect candidate source PRs that might require docs updates.
2. `create-pr-per-source`: create one docs-cn PR per source PR candidate.

The workflow supports three trigger modes:

- Scheduled run (every Monday 01:00 Asia/Shanghai).
- Manual run (`workflow_dispatch`).
- Event-driven run (`repository_dispatch` with `docs-sync-source-pr`).

## Required Secrets

Configure these repository secrets in `pingcap/docs`:

- `DOCS_CN_BOT_TOKEN`: GitHub token with write access to `pingcap/docs-cn`.

The workflow uses this token for:

- scanning source repositories through GitHub API
- checking out `pingcap/docs-cn`
- creating/updating docs-cn PRs

## Environment Configuration

Main workflow env values:

- `SOURCE_ORG`: source org to scan (default `pingcap`)
- `EXCLUDED_REPOS`: repos excluded from source scan (default `pingcap/docs,pingcap/docs-cn`)
- `EXTRA_REPOS`: extra repos always included (default `tikv/tikv,tikv/pd`)
- `DOCS_CN_BASE_BRANCH`: fallback docs-cn branch
- `TARGET_BRANCH_MAP`: source branch -> target docs-cn branch map

Section insertion preferences are configured in:

- `scripts/source-pr-doc-sync/section-preferences.json`

## Trigger Modes

### 1. Scheduled

No action needed. GitHub Actions runs automatically every Monday.

### 2. Manual (`workflow_dispatch`)

Optional inputs:

- `source_repo`: run for one source repo only (example: `pingcap/tidb`)
- `source_pr_number`: run for one source PR only
- `max_candidates_per_run`: max docs-cn PRs per run (default: `50`)

If `source_repo` and `source_pr_number` are both provided, the workflow runs in single-PR mode.

### 3. Event-driven (`repository_dispatch`)

Event type:

- `docs-sync-source-pr`

Client payload example:

```json
{
  "source_repo": "pingcap/tidb",
  "source_pr_number": "12345",
  "max_candidates_per_run": "1"
}
```

Example command:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.github.com/repos/pingcap/docs/dispatches \
  -d '{
    "event_type": "docs-sync-source-pr",
    "client_payload": {
      "source_repo": "pingcap/tidb",
      "source_pr_number": "12345",
      "max_candidates_per_run": "1"
    }
  }'
```

## Artifacts and Outputs

The `scan` job generates:

- a markdown report (`source-pr-doc-check-<start>_to_<end>.md`)
- a json report (`source-pr-doc-check-<start>_to_<end>.json`)
- candidate matrix output for downstream matrix jobs

The `create-pr-per-source` job:

- downloads scan artifacts
- applies docs changes for one source PR (prefer inserting under matched in-page sections, fallback to file end)
- skips PR creation if there are no docs-cn file changes

## Idempotency and PR Granularity

Current design is per-source-PR:

- one source PR -> one docs-cn PR
- no mixed aggregate PR

This improves:

- reviewer ownership clarity
- branch/cherry-pick alignment
- failure isolation

## Common Operations

### Rerun one failed source PR

Use `workflow_dispatch`:

- `source_repo=<repo>`
- `source_pr_number=<number>`
- `max_candidates_per_run=1`

### Reduce run load

Set `max_candidates_per_run` to a smaller value (for example, `10`).

### Adjust branch mapping

Edit `TARGET_BRANCH_MAP` in workflow env.

### Adjust in-page insertion behavior

Edit `scripts/source-pr-doc-sync/section-preferences.json`:

- `path_to_preferred_sections`: per-path heading preference list
- `default_preferred_sections`: fallback heading preference list

## Troubleshooting

### No docs-cn PR created

Possible reasons:

- candidate score did not meet threshold
- mapped docs files were not found
- script produced no actual file diff

Check:

- `scan` job logs and report json
- `create-pr-per-source` logs (`No docs-cn file changes detected...`)

### 401/403 API errors

Possible reasons:

- invalid token
- missing repo permissions
- token cannot access target repos

Check:

- `DOCS_CN_BOT_TOKEN` value and scopes
- whether token has access to both source repos and `pingcap/docs-cn`

### Branch checkout failure in docs-cn

Possible reasons:

- `TARGET_BRANCH_MAP` points to a non-existent target branch

Check:

- target branch exists in `pingcap/docs-cn`
- mapping keys match source PR base branch values

## Files in This Automation

- `.github/workflows/source-pr-doc-sync.yml`
- `scripts/source-pr-doc-sync/collect_source_pr_doc_candidates.py`
- `scripts/source-pr-doc-sync/apply_source_pr_docs_cn_updates.py`
