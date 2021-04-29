---
title: tiup dm template
---

# tiup dm template

Before deploying the cluster, you need to prepare a [topology file](/tiup/tiup-dm-topology-reference.md) of the cluster. TiUP has a built-in topology file template, and users can modify this template to generate the final topology file. You can output the template content built in TiUP using the `tiup dm template` command.

## Syntax

```shell
tiup dm template [flags]
```

If this option is not specified, the output default template contains the following instances:

- 3 DM-master instances
- 3 DM-worker instances
- 1 Prometheus instance
- 1 Grafana instance
- 1 Alertmanager instance

## 选项

### --full

- Outputs a detailed topology template that is annotated with configurable parameters. To enable this option, add it to the command.
- If this option is not specified, the simplest topology template is output by default.

### -h, --help

Prints the help information.

## Output

Outputs the topology template according to the specified options, which can be redirected to the topology file for deployment.
