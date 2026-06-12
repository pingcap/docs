---
name: source-pr-doc-sync
description: Detect merged source code PRs that likely impact docs, then create one docs-cn PR per source PR with branch-aware mapping, optional event-driven single-PR mode, and operational safeguards.
---

# Source PR Docs Sync

Use this skill when you need to sync documentation updates from merged source code PRs to `pingcap/docs-cn` with one target PR per source PR.

## Default behavior

- Do not aggregate multiple source PRs into one docs-cn PR.
- Always preserve source-to-target traceability (`source repo`, `source PR`, `source base branch`, `target docs-cn branch`).
- Prefer branch mapping over fallback defaults when mapping is configured.
- Skip PR creation when no docs-cn file changes are produced.

## Load this context first

- `.ai/shared/repo-conventions.md`
- `.ai/shared/writing-style.md`
- `scripts/source-pr-doc-sync/source-pr-doc-sync.md`
- `.github/workflows/source-pr-doc-sync.yml`

## Workflow components

- Candidate collector:
  - `scripts/source-pr-doc-sync/collect_source_pr_doc_candidates.py`
- Per-source updater:
  - `scripts/source-pr-doc-sync/apply_source_pr_docs_cn_updates.py`
- Orchestration workflow:
  - `.github/workflows/source-pr-doc-sync.yml`

## Trigger modes

### 1. Scheduled mode

- Triggered weekly (Monday 01:00 Asia/Shanghai).
- Scans source repositories and builds candidate matrix.
- Creates docs-cn PRs per source PR candidate.

### 2. Manual mode (`workflow_dispatch`)

Optional inputs:

- `source_repo`
- `source_pr_number`
- `max_candidates_per_run`

If both `source_repo` and `source_pr_number` are provided, run in single-source-PR mode.

### 3. Event-driven mode (`repository_dispatch`)

Supported event:

- `docs-sync-source-pr`

Use event payload fields:

- `source_repo`
- `source_pr_number`
- `max_candidates_per_run` (optional)

## Required configuration

### Secrets

- `DOCS_CN_BOT_TOKEN` (must have write access to `pingcap/docs-cn`)

### Main environment variables

- `SOURCE_ORG`
- `EXCLUDED_REPOS`
- `EXTRA_REPOS`
- `DOCS_CN_BASE_BRANCH`
- `TARGET_BRANCH_MAP`
- `MAX_CANDIDATES_PER_RUN`
- `FORCE_SOURCE_REPO`
- `FORCE_SOURCE_PR_NUMBER`

## Step-by-step execution

## Step 1. Collect source PR candidates

Run:

```bash
python scripts/source-pr-doc-sync/collect_source_pr_doc_candidates.py
```

This step:

- Scans merged PRs in the configured time window.
- Scores doc-impact likelihood via label/keyword/path heuristics.
- Produces report artifacts and matrix-ready candidate output.

## Step 2. Build per-source-PR matrix

- Read `candidates_matrix` output from Step 1.
- Each matrix row must represent exactly one source PR.
- Resolve target docs-cn branch from `TARGET_BRANCH_MAP`, fallback to `DOCS_CN_BASE_BRANCH`.

## Step 3. Apply docs-cn updates for one source PR

Run:

```bash
python scripts/source-pr-doc-sync/apply_source_pr_docs_cn_updates.py \
  --report-json "<candidate-json-path>" \
  --docs-cn-dir "<docs-cn-local-path>" \
  --source-repo "<owner/repo>" \
  --source-pr-number "<pr-number>"
```

This step:

- Locates one source PR candidate from the report.
- Applies mapped docs-cn edits for that candidate only.
- Writes per-candidate apply summary into `docs-cn`.

## Step 4. Create docs-cn PR

- Create one docs-cn PR per source PR candidate.
- Include source traceability fields in PR body.
- Skip PR creation when no file diff exists in `docs-cn`.

## Safety and scope rules

- Do not mix multiple source PRs in one docs-cn PR.
- Do not bypass branch mapping when source branch is known.
- Do not force-create empty docs-cn PRs.
- Keep changes scoped to mapped docs files for the selected source PR.

## Outputs

- Candidate report markdown (scan summary)
- Candidate report json (machine-readable source PR list)
- One docs-cn PR per candidate source PR
- Per-candidate apply summary json in `docs-cn`

## Troubleshooting

- 401/403:
  - verify `DOCS_CN_BOT_TOKEN` validity and repository permissions.
- No candidate PRs:
  - verify scan window, repository filters, and heuristics thresholds.
- No docs-cn PR created for a candidate:
  - verify mapped target files exist and check no-change skip logs.
- Wrong target branch:
  - verify `TARGET_BRANCH_MAP` keys exactly match source PR base branch names.
