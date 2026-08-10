---
title: ti organization list-projects
summary: List TiDB Cloud projects accessible to the configured API key.
---

# ti organization list-projects

Lists projects accessible to the configured TiDB Cloud API key, with optional pagination.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti organization list-projects
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## Options

- `--help`: Display help information.
- `--page-size <int32>`: Number of projects to request; 0 uses the API default.
- `--page-token <string>`: Page token returned by a previous list-projects call.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List accessible projects:

    ```bash
    # Return the TiDB Cloud projects available to the configured API key.
    ti organization list-projects --page-size 50
    ```

- Select the virtual project ID:

    ```bash
    # Use a JMESPath query to return only virtual project IDs.
    ti organization list-projects --query 'projects[?type == `tidbx_virtual`].id' --output text
    ```

## Related documentation

- [TiDB Cloud Organization CLI Command Reference](/ai/ti/reference/ti-organization.md)
