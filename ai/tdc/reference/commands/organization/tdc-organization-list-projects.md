---
title: tdc organization list-projects
summary: List TiDB Cloud projects accessible to the configured API key.
---

# tdc organization list-projects

Lists projects accessible to the configured TiDB Cloud API key, with optional pagination.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc organization list-projects
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## Options

- `--help`: Display help information.
- `--page-size <int32>`: Number of projects to request; 0 uses the API default.
- `--page-token <string>`: Page token returned by a previous list-projects call.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List projects as text

```bash
tdc organization list-projects --page-size 50 --output text
```

### Return virtual project IDs

```bash
tdc organization list-projects --query 'projects[?type == `tidbx_virtual`].id' --output text
```
