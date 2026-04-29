---
title: Docs JSON API (Experimental)
summary: Provide a structured JSON API for TiDB docs with topic and feature filters.
---

# Docs JSON API (Experimental)

This API layer exposes structured metadata for markdown docs.

## Why

- Query docs by feature token (for example, `tidb_max_dist_task_nodes`)
- Query docs by topic/category
- Return structured schema instead of raw markdown only
- Keep list APIs fast by default, and fetch full content on demand

## Data schema

Each doc record includes:

- `id`
- `path`
- `title`
- `summary`
- `product`
- `topics`
- `features`
- `headings`
- `frontMatter`
- `frontMatterRaw`
- `updatedAt`

## Build index

```bash
npm run docs-api:build
```

Default output file: `tmp/docs-api-index.json`

## Run API server

```bash
npm run docs-api:serve
```

Default host and port: `127.0.0.1:3000`

## Endpoints

- `GET /healthz`
- `GET /schema`
- `GET /topics`
- `GET /features`
- `GET /features?prefix=tidb_`
- `GET /docs`
- `GET /docs?feature=tidb_max_dist_task_nodes`
- `GET /docs?topic=tidb-cloud`
- `GET /docs?q=resource control`
- `GET /docs?feature=tidb_max_dist_task_nodes&limit=10&offset=0`
- `GET /docs?topic=tidb-cloud&includeContent=true` (returns markdown content in list response)
- `GET /docs/content?path=tidb-cloud/backup-and-restore.md`
- `GET /docs/content?id=tidb-cloud/backup-and-restore`
- `GET /reload` (reload in-memory index)

## Search and performance behavior

- `q` uses path, title, summary, and full-text matching.
- `/docs` does **not** return full markdown content by default.
- Use `/docs/content` to fetch full markdown content for a single document.
- If needed, set `includeContent=true` on `/docs` for small result sets.

## Environment variables

- `DOCS_API_HOST` (default `127.0.0.1`)
- `DOCS_API_PORT` (default `3000`)
- `DOCS_API_SOURCE_DIR` (default: if `../docs-staging` exists, use it; otherwise current working directory)
- `DOCS_API_INDEX_FILE` (optional prebuilt JSON index path)

## Source priority

The API loads markdown files from the source directory in this order:

1. `DOCS_API_SOURCE_DIR` (if set)
2. `../docs-staging` (if exists)
3. current working directory

Template variables in markdown such as `{{{ .starter }}}` are replaced using `variables.json` in the selected source directory.
