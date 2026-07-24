---
title: tdc configure
summary: Configure a local tdc profile interactively or non-interactively.
---

# tdc configure

Configures a local tdc profile. Without flags, this is the only interactive tdc command.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc configure
    [--help]
    [--non-interactive]
    [--region-code <string>]
    [--tdc-private-key <string>]
    [--tdc-public-key <string>]
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
tdc configure
TDC_PRIVATE_KEY="<private-key>" tdc configure --profile ci --non-interactive --region-code aws-us-east-1 --tdc-public-key "<public-key>"
```
