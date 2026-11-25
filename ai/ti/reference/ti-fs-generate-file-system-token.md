---
title: ti fs generate-file-system-token
summary: Generate an additional owner token for one TiDB Cloud Filesystem.
---

# ti fs generate-file-system-token

Generates an owner token for a file system using TiDB Cloud API credentials. The token value appears only in the command output and cannot be retrieved later. Use `--store-locally` to save the token in the local credential store. An existing file system token cannot be used to generate owner tokens.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs generate-file-system-token
  --file-system-id <string>
  --token-name <string>
  (--ttl <duration> | --no-expiration)
  [--dry-run]
  [--help]
  [--replace]
  [--store-locally]
  [--version]
```

## Options

- `--file-system-id <string>`: Specify the file system that owns the token. File system tokens cannot replace this option or authorize owner-token generation. This option is required.
- `--token-name <string>`: Set an operational token name of at most 64 bytes. Names are not unique. This option is required.
- `--ttl <duration>`: Set a positive lifetime in whole seconds, up to 365 days. Specify exactly one of `--ttl` and `--no-expiration`.
- `--no-expiration`: Create a token without an expiry. Specify exactly one of `--ttl` and `--no-expiration`.
- `--store-locally`: Store and select the generated token for this profile and file system.
- `--replace`: Replace an existing selected local token. Requires `--store-locally` and does not revoke the previous remote token.
- `--dry-run`: Validate credentials, region, lifetime, and local storage preconditions without generating a token.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Generate a short-lived token for a CI job:

    ```bash
    # Save the one-time plaintext response in an owner-only file.
    umask 077
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name ci-deploy \
      --ttl 24h > ./ci-token.json
    ```

- Generate a non-expiring token for another machine:

    ```bash
    # Generation does not change the current local selection by default.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name workstation \
      --no-expiration
    ```

- Generate and select a replacement local token:

    ```bash
    # The old remote token remains active until you explicitly disable or delete it.
    ti fs generate-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-name local-owner-v2 \
      --ttl 720h \
      --store-locally \
      --replace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)
