---
title: tiup cluster import
---

# tiup cluster import

Before TiDB 4.0, clusters were usually deployed using TiDB Ansible. From TiDB 4.0 onwards, TiUP Cluster provides the `import` command to transfer these clusters to the tiup-cluster component for the management.

> **Note:**
>
> + After importing the TiDB Ansible configuration to TiUP for the management, do not use TiDB Ansible for cluster operations anymore. Otherwise, conflicts might be caused due to inconsistent meta information.
> + The `import` command does not support the import of the following clusters. If the clusters deployed using TiDB Ansible are in any of the following scenarios, do not use the `import` command.
> + Clusters with TLS encryption enabled
> + Pure KV clusters (clusters without TiDB instances)
> + Clusters with `Kafka` enabled
> + Clusters with `Spark` enabled
> + Clusters with TiDB Lightning/Importer enabled
> + Clusters still using the old `push` mode to collect monitoring metrics (if you keep the default mode `pull` unchanged, using the `import` command is supported)
> + Clusters in which the non-default ports (the ports configured in the `group_vars` directory are compatible) are separately configured in the `inventory.ini` configuration file using `node_exporter_port` / `blackbox_exporter_port`

## Syntax

```sh
tiup cluster import [flags]
```

## Options

### -d, --dir ${string}

- Data type: `STRING`
- Specifies the directory where TiDB Ansible is located.
- If you do not specify this option in the command, the current directory is regarded as the directory where TiDB Ansible is located.

### --ansible-config ${string}

- Data type: `STRING`
- Specifies the path of the Ansible configuration file.
- If you do not specify this option in the command, the default path `. /ansible.cfg` is used in the import.

### --inventory ${string}

- Data type: `STRING`
- Specifies the name of the Ansible inventory file.
- If you do not specify this option in the command, the default name `inventory.ini` is used in the import.

### --no-backup

- Data type: `BOOLEAN`
- Controls whether to disable the backup of files in the directory where TiDB Ansible is located.
- If you do not specify this option in the command, after a successful import, everything in the directory specified by the `-dir` option is backed up to the `${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup` directory. If there are multiple inventory files (which indicates multiple clusters are deployed) in this directory, it is recommended to include this option in the `import` command to disable the default backup step.

### --rename ${string}

- Data type: `STRING`
- Renames the imported cluster. 
- If you do not specify this option in the command, the cluster_name specified in inventory is used as the cluster name.

### -h, --help

- Data type: `BOOLEAN`
- Shows the help information.
- If you do not specify this option in the command, the default value is `false` so the help information is not shown.

## Output

Shows the logs of the import process.
