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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc organization list-projects --page-size 50 --output text
tdc organization list-projects --query 'projects[?type == `tidbx_virtual`].id' --output text
```
