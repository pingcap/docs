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

- When TLS is disabled, specify this option to clean up previously generated certificates.
- Data type: `BOOLEAN`
- If this option is not specified, old certificates might be reused when TLS is enabled again.

### --force

- Forces the process of enabling or disabling TLS, regardless of the current TLS status of the cluster.
- Data type: `BOOLEAN`
- If this option is not specified, the operation will be skipped when the current state matches the requested state.

### --reload-certificate

- When TLS is enabled, specify this option to regenerate certificates.
- Data type: `BOOLEAN`
- If this option is not specified, new certificates will not be generated if certificates already exist.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

Execution logs of the tiup-cluster command.
