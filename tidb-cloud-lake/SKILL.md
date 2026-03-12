---
name: databend-to-tidb-cloud-lake-migration
description: "Migrate documentation from databend-docs (Docusaurus) to TiDB Cloud Lake (Gatsby). Use this skill when the user asks to move, migrate, port, or convert Databend documentation into the TiDB Cloud Lake docs repo.
---

# Databend → TiDB Cloud Lake Documentation Migration

## Overview

This skill migrates documentation from **databend-docs** (Docusaurus-based) into the **TiDB Cloud Lake** product section of a Gatsby-based TiDB Cloud documentation site. The source of truth is the `main` branch of the databend-docs repository.

All work MUST be done on the **`cloud-lake-dir`** branch of the TiDB Cloud docs repo.

## Step-by-Step Workflow

Execute the following steps **in order**. Each step has a verification checkpoint — do not proceed until the checkpoint passes.

### Step 1: Copy Markdown Files

**Goal:** Flatten all Markdown files from the Databend guides into a single directory in the TiDB Cloud Lake repo.

**Actions:**

1. Identify all `.md` files recursively under `/databend-docs/docs/en/sql-reference/`.
2. Copy every remaining `.md` file into `/docs/tidb-cloud-lake/sql/` — **flat, no subfolders**. All files go directly into this single directory regardless of their original subdirectory structure.
3. If two source files have the same filename but come from different subdirectories, flag a conflict and list both paths for the user to resolve before proceeding.

**Checkpoint:** Run `find /docs/tidb-cloud-lake/sql/ -type d` and confirm only the `sql/` directory itself exists (no subdirectories). Confirm zero files originate from `20-self-hosted`.

### Step 2: Rename Markdown Files

**Goal:** Normalize all filenames to a clean `a-b-c.md` kebab-case format.

**Rules:**

- All lowercase letters only.
- Words separated by hyphens (`-`).
- No underscores (`_`), no double underscores (`__`).
- No numbers. Remove all numeric prefixes (e.g., `01-`, `10-`) and any other numbers.
- No capitalized letters.
- Read the `title:` field from each file's YAML front matter. Extract meaningful **keywords** from the title and use those as the new filename.
  - Example: A file with `title: "Loading Data from Amazon S3"` → `loading-data-amazon-s3.md`
  - Example: A file with `title: "Query Overview"` → `query-overview.md`
- Strip common filler words (`a`, `an`, `the`, `and`, `or`, `for`, `with`, `from`, `to`, `in`, `of`) unless removing them makes the name ambiguous.

**Checkpoint:** Run a script to verify: no uppercase letters, no underscores, no numbers, no double-hyphens in any filename under `/docs/tidb-cloud-lake/sql/`.

### Step 3: Build the TOC (Table of Contents)

**Goal:** Create the `## Reference` section in `docs/TOC-tidb-cloud-lake.md`, matching the navigation structure from the Databend SQL Reference page.

**Actions:**

1. Fetch the left navigation (table of contents) from <https://docs.databend.com/sql> to understand the section ordering and hierarchy.
2. Map every copied-and-renamed Markdown file to its place in this navigation hierarchy.
3. Write the `## Reference` section in `docs/TOC-tidb-cloud-lake.md` using the **exact same list format** as `docs/TOC-tidb-cloud-starter.md`.

**TOC Format Reference** (from `TOC-tidb-cloud-starter.md`):

```markdown
# Table of Contents

## GET STARTED

- Why TiDB Cloud
  - [Introduction](/tidb-cloud/tidb-cloud-intro.md)

## REFERENCE

- SQL Reference
  - [Overview](/tidb-cloud/tidb-cloud-sql-ref.md)
```

**Apply this format to the REFERENCE section:**

```markdown
## REFERENCE

- SQL Reference
  - [Overview](/tidb-cloud-lake/guides/loading-data-overview.md)
  - [Amazon S3](/tidb-cloud-lake/guides/loading-data-amazon-s3.md)
  - [Google Cloud Storage](/tidb-cloud-lake/guides/loading-data-gcs.md)
```

**Key rules:**

- Section headers use `##` (e.g., `## Reference`).
- Category names are unlinked plain text list items (`- Loading Data`).
- Individual pages are indented linked list items (`  - [Page Title](/tidb-cloud-lake/guides/filename.md)`).
- The link path must use the **renamed** filename from Step 2.
- Preserve the same ordering as the Databend Guides navigation.

**Checkpoint:** Every `.md` file in `/docs/tidb-cloud-lake/sql/` must appear exactly once in the TOC. Run a cross-reference script to find orphaned files (in dir but not in TOC) and dangling references (in TOC but no file).
