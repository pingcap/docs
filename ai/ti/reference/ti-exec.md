---
title: ti exec
summary: Run remote commands against a TiDB Cloud Filesystem, preserve workspace files, select execution options, and handle failures safely.
---

# ti exec

`ti exec` runs a command against a TiDB Cloud Filesystem without mounting the Filesystem locally. Output streams to your terminal; the remote exit status is preserved.

> **Note:**
>
> Runtime is available only in AWS Oregon (`us-west-2`) and AWS N. Virginia (`us-east-1`). Use `aws-us-west-2` or `aws-us-east-1` as the CLI region code. You need a Runtime-enabled Filesystem in one of these regions. CLI support for `ti exec` does not enable Runtime on the server.

> **Warning:**
>
> Validation of the preview `ti exec` feature is incomplete. A timeout or cancellation request can return an unknown outcome (`255`) without confirming whether the command has stopped. Verify the result before deciding whether to run the command again.

## Prerequisites

- Install TiDB Cloud CLI **v0.2.11 or later** with an up-to-date `ti-drive9` companion. Earlier `ti` releases do not include `ti exec`. Run `ti --version` to check your installed version.
- [Create a Filesystem](/ai/ti/reference/ti-fs-create-file-system.md) in a supported region and retain its ID and owner token.
- Use a locally stored token for that ID, or set `TI_FS_TOKEN` in your environment. Prefer the environment variable over `--fs-token` to avoid exposing it in arguments. A delegated Vault token cannot run commands. Path-scoped tokens cannot mount a sandbox.
- `ti exec --help` checks only that the local command exists. It does not verify the companion or remote Runtime. Both must support exec.

### Upgrade an existing installation

Before upgrading, stop writers and unmount any Filesystem or Vault mounts. On macOS or Linux with a user-owned installation of `ti`, update to the latest release and verify the version:

```bash
ti update
ti --version
ti exec --help
```

When `ti update` installs a different `ti` version, it also replaces the `ti-drive9` companion. If `ti` is already at the requested version, the updater does not refresh the companion. To refresh an outdated companion on macOS or Linux, rerun the shell installer; use `--install-dir` to retain a custom installation directory.

On Windows, rerun the PowerShell installer; in-place self-update is unsupported. For installation steps, see [Install TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli).

## Syntax and execution

```text
ti exec [options] [--] command [arg...]
ti exec [options] 'shell command line'
```

Put `ti` options before the remote command. Arguments after it, including `--help`, belong to the remote command. A single shell command line is interpreted by `/bin/sh -c`; multiple arguments are passed directly.

The server selects the execution backend. Commands supported by the lightweight shell executor can run without starting a sandbox. Other commands use a sandbox before execution begins. Shell syntax alone does not determine the backend. A command that has started is never retried on another backend after failure.

The Filesystem is available at `/workspace`. Files outside `/workspace` are temporary. `--fresh` starts a new sandbox while keeping Filesystem data. `-w` chooses a working directory; it does not restrict access to that directory.

## Example: process and read back a file

Requires Bash locally and Python 3 remotely.

```bash
export TI_REGION_CODE=aws-us-east-1
export TI_FS_FILE_SYSTEM_ID='<file-system-id>'
workdir="runtime-demo-$(date +%s)"
ti fs create-directory --path "/$workdir"

# Inspect the directory without permitting writes.
ti exec --read-only -w "$workdir" ls

# Process data remotely and save the result in the Filesystem.
ti exec -w "$workdir" python3 -c \
  'from pathlib import Path; Path("result.txt").write_text("total=42\n")'

# Start a new sandbox and read the saved result.
ti exec --fresh -w "$workdir" cat result.txt
```

Expected output:

```text
total=42
```

Verify independently, then remove the example directory:

```bash
ti fs read-file --path "/$workdir/result.txt"
ti fs delete-file --path "/$workdir" --recursive
```

## Options

| Option | Description |
| --- | --- |
| `--file-system-id ID` | Select a Filesystem. Alternatively, set `TI_FS_FILE_SYSTEM_ID` or supply a token that contains the ID. |
| `--fs-token TOKEN` | Supply a token. Prefer `TI_FS_TOKEN`. Otherwise, use the selected Filesystem's locally stored token. |
| `-w`, `--workspace PATH` | Choose a remote working directory. Defaults to the matching local FUSE directory, or the Filesystem root. |
| `-C`, `--cwd DIR` | Choose a subdirectory within that working directory. |
| `-e`, `--env KEY[=VALUE]` | Set a remote variable; a bare key copies its local value. Repeatable. |
| `-t`, `--timeout DURATION` | Set a deadline, such as `30s` or `10m`. The server can impose a shorter limit. |
| `--fresh` | Start a new sandbox instead of reusing one. |
| `--layer REF` | Use a layer ID, name, or tag reference. |
| `--read-only` | Prevent writes to the Filesystem during execution. |
| `-v`, `--verbose` | Show execution details on standard error. |

Inside a matching local FUSE mount, omitting `-w` uploads pending local writes and follows the current directory. Explicit `-w` does not upload local changes first. For a WebDAV mount, pass `-w` explicitly.

## Failures and limitations

A completed command returns its exact exit status. With an up-to-date `ti-drive9` companion, interpret the following statuses together with the error message:

| Exit status | Meaning |
| --- | --- |
| `124` | The command timed out and was stopped. |
| `125` | The executor failed. Output or writes might be partial. |
| `126` | The command is not executable. |
| `127` | The command was not found. |
| `130` | Cancellation before execution, confirmed cancellation, or detachment after a second Ctrl-C. This status alone does not prove that a remote command stopped. |
| `255` | The outcome is unknown. This can also occur after a timeout or cancellation request. |

Commands can themselves return these numbers, so the exit status alone does not identify the cause.

- Remote stdin and interactive terminals are unsupported. `--output`, `--query`, and `--dry-run` are unsupported.
- Press Ctrl-C once to request cancellation and wait for confirmation. Pressing it again detaches; the command might still be running.
- If the outcome is unknown, inspect the Filesystem before deciding whether to run the command again. Disconnection or a missing execution record does not prove that execution stopped. `ti exec` never retries automatically.
