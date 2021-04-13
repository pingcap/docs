---
title: tiup mirror rotate
---

# tiup mirror rotate

`root.json` is an important file in a TiUP mirror. It stores the public keys needed for the entire system and is the basis of the chain of trust in TiUP. It mainly contains the following parts:

- Signatures of mirror administrators. For an official mirror, there are five signatures. For a default initialized mirror, there are three signatures.
- The public keys used to verify the following files:
    - root.json
    - index.json
    - snapshot.json
    - timestamp.json
- Expiration date of `root.json`. For an official mirror, the expiration date is one year later than the creation date of `root.json`.

For detailed description of TiUP mirror, see [TiUP Mirror Reference](/tiup/tiup-mirror-reference.md).

You need to update `root.json` in the following cases:

- Replace the key of the mirror.
- Update the expiration date of certificate files.

After the content of `root.json` is updated, the file must be re-signed by all administrators, or the client rejects the file. The update process is as follows:

1. Update the content of `root.json`.
2. All administrators sign the new `root.json` file.
3. Update `snapshot.json` to record the version of the new `root.json` file.
4. All administrators sign the new `snapshot.json` file.
5. Update `timestamp.json` to record the hash value of the new `snapshot.json` file.
6. All administrators sign the new `timestamp.json` file.

TiUP uses the command `tiup mirror rotate` to automate the above process.

> **Note:**
>
> + In TiUP versions earlier than v1.3.0, running this command does not returns a correct new `root.json` file. See [#983](https://github.com/pingcap/tiup/issues/983).
> + Before using this command, make sure that all TiUP clients are upgraded to v1.3.0 or later versions.

## Syntax

```shell
tiup mirror rotate [flags]
```

After executing this command, TiUP starts an editor to modify the file content to target value, such as changing the value of the `expires` field to a later date. Then, TiUP changes the `version` field from `N` to `N+1` and saves the file. After the file is saved, TiUP starts a temporary http server and waits for all mirror administrators to sign the file.

For how mirror administrators sign files, refer to [the `sign` command](/tiup/tiup-command-mirror-sign.md).

## Options

### --addr

- Specifies the listening address of the temporary server. You need to make sure that the address is accessible to other mirror administrators so that they can use [the `sign` command](/tiup/tiup-command-mirror-sign.md) to sign the file.
- Data type: `STRING`
- If this option is not specified in the command, TiUP listens to `0.0.0.0:8080` by default.

## Outputs

The current signature status of each mirror administrator.
