---
title: tiup cluster tls
summary: The `tiup cluster tls` command is used to enable or disable TLS (Transport Layer Security) between cluster components.
---

# tiup cluster tls

The `tiup cluster tls` command is used to enable TLS (Transport Layer Security) between cluster components. It automatically generates and distributes self-signed certificates to each node in the cluster.

## Syntax

```shell
tiup cluster tls <cluster-name> <enable/disable> [flags]
```

`<cluster-name>` specifies the cluster for which you want to enable or disable TLS.

## Options

### --clean-certificate

- When you disable TLS, use this option to clean up previously generated certificates.
- Data type: `BOOLEAN`
- Default: `false`
- If you do not specify this option, old certificates might be reused when you enable TLS again.

### --force

- Forces enabling or disabling TLS, regardless of the cluster's current TLS status.
- Data type: `BOOLEAN`
- Default: `false`
- If you do not specify this option, the operation is skipped if the cluster is already in the requested state.

### --reload-certificate

- When you enable TLS, use this option to regenerate certificates.
- Data type: `BOOLEAN`
- Default: `false`
- If you do not specify this option, new certificates are not generated if certificates already exist.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- Default: `false`

## Output

Execution logs of the tiup-cluster command.
