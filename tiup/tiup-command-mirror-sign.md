---
title: tiup mirror sign
---

# tiup mirror sign

The `tiup mirror sign` command is used to sign the meta-information files (*.json）defined in TiUP [mirror](/tiup/tiup-mirror-reference.md). These meta-information files might be stored on the local file system or remotely stored using the http protocol to provide a signature entry.

## Syntax

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>` is the address of the signed file, which has two forms:

- Network address: start with http or https, such as `http://172.16.5.5:8080/rotate/root.json`
- Local file path: relative path or absolute path

If it is a network address, the address must provide the following functions:

- Support access with `http get`, at this time the complete content of the signed file (including the signatures field) should be returned
- Support access with `http post`, the client adds this signature to the signatures field of the content returned by `http get` and POST to this address

## Options

### -k, --key

- Specifies the location of the private key used for signing the `{component}.json` files.
- Data type: `STRING`
- Default: "${TIUP_HOME}/keys/private.json"

### --timeout

- Specifies the access timeout of the network when signing through the network. The unit is seconds.
- Data type: `int`
- Default: 10

> **Note:**
>
> This option is valid only when `<manifest-file>` is a network address.

## Output

- If the command is executed successfully, there is no output.
- If the file has been signed by the specified key, TiUP reports the error `Error: this manifest file has already been signed by specified key`.
- If the file is not a valid manifest, TiUP reports the error `Error: unmarshal manifest: %s`.