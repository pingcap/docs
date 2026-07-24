---
title: tdc fs-journal verify-journal
summary: Verify a Filesystem journal hash chain.
---

# tdc fs-journal verify-journal

Verifies the integrity of one journal hash chain.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-journal verify-journal
    --journal-id <string>
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--version]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-journal verify-journal --journal-id jrn-demo
tdc fs-journal verify-journal --journal-id jrn-demo --output text
```
