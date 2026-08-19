---
title: ti fs generate-file-system-token
summary: Generate an additional owner token for one TiDB Cloud Filesystem.
---

# ti fs generate-file-system-token

Generates an owner token for one Filesystem by using TiDB Cloud API credentials. An existing FS token cannot authorize owner-token generation. The plaintext `fs_token` appears only in the successful response and cannot be recovered through the list command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs generate-file-system-token
  --file-system-id <string>
  --token-name <string>
  (--ttl <duration> | --no-expiration)
  [--dry-run]
  [--replace]
  [--store-locally]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem that owns the token. FS tokens cannot replace this option or authorize owner-token generation. This option is required.
- `--token-name <string>`: Set an operational token name of at most 64 bytes. Names are not unique. This option is required.
- `--ttl <duration>`: Set a positive lifetime in whole seconds, up to 365 days. Specify exactly one of `--ttl` and `--no-expiration`.
- `--no-expiration`: Create a token without an expiry. Specify exactly one of `--ttl` and `--no-expiration`.
- `--store-locally`: Store and select the generated token for this profile and Filesystem.
- `--replace`: Replace an existing selected local token. Requires `--store-locally` and does not revoke the previous remote token.
- `--dry-run`: Validate credentials, region, lifetime, and local storage preconditions without generating a token.

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
- [`ti fs list-file-system-tokens`](/ai/ti/reference/commands/fs/ti-fs-list-file-system-tokens.md)
