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

> **Note:**
>
> Currently, the `tiup cluster tls` command supports enabling or disabling TLS only for clusters with a single PD node. For clusters with multiple PD nodes, executing the `tiup cluster tls` command directly returns an error, because switching the TLS status can cause communication exceptions between PD nodes. To enable or disable TLS for a cluster with multiple PD nodes, first [`scale-in`](/tiup/tiup-component-cluster-scale-in.md) the PD nodes to one node, and then execute the `tiup cluster tls` command.

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
