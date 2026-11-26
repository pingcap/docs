---
title: Manage Data Source Configurations in TiDB Data Migration
summary: Learn how to manage upstream MySQL instances in TiDB Data Migration.
---

# Manage Data Source Configurations in TiDB Data Migration

This document introduces how to manage data source configurations, including encrypting the MySQL password, operating the data source, and changing the bindings between upstream MySQL instances and DM-workers using [dmctl](/dm/dmctl-introduction.md).

## Encrypt the database password

In DM configuration files, it is recommended to use the password encrypted with dmctl. For one original password, the encrypted password is different after each encryption.

> **Note:**
>
> Starting from v8.0.0, you must configure [`secret-key-path`](/dm/dm-master-configuration-file.md) for DM-master before using the `dmctl encrypt` command.

{{< copyable "shell-regular" >}}

```bash
./dmctl encrypt 'abc!@#123'
```

```
MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
```

## Operate data source

You can use the `operate-source` command to load, list or remove the data source configurations to the DM cluster.

{{< copyable "" >}}

```bash
help operate-source
```

```
`create`/`stop`/`show` upstream MySQL/MariaDB source.

Usage:
  dmctl operate-source <operate-type> [config-file ...] [--print-sample-config] [flags]

Flags:
  -h, --help                  help for operate-source
  -p, --print-sample-config   print sample config file of source

Global Flags:
  -s, --source strings   MySQL Source ID
```

### Flags description

+ `create`: Creates one or more upstream database sources. When creating multiple data sources fails, DM rolls back to the state where the command was not executed.

+ `stop`: Stops one or more upstream database sources. When stopping multiple data sources fails, some data sources might be stopped.

+ `show`: Shows the added data source and the corresponding DM-worker.

+ `config-file`: Specifies the file path of `source.yaml` and can pass multiple file paths.

+ `--print-sample-config`: Prints the sample configuration file. This parameter ignores other parameters.

### Usage example

Use the following `operate-source` command to create a data source in the DM cluster based on the configuration in `source.yaml`:

{{< copyable "" >}}

```bash
operate-source create ./source.yaml
```

For the configuration of `source.yaml`, refer to [Upstream Database Configuration File Introduction](/dm/dm-source-configuration-file.md).

The following is an example of the returned result:

{{< copyable "" >}}

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

### Check data source configurations

> **Note:**
>
> The `config` command is only supported in DM v6.0 and later versions. For earlier versions, you must use the `get-config` command.

If you know the `source-id`, you can run `dmctl --master-addr <master-addr> config source <source-id>` to get the data source configuration. The following example checks the command result before saving the YAML. It writes to a temporary file and replaces the output file only after a successful lookup, so an invalid `source-id` or a failed `dmctl` command does not overwrite an existing file. Replace the example address and source ID with your own values. The `cfg` output masks the password as `******`; restore the actual password before using the saved YAML to create a data source.

```bash
( set -o pipefail
output_file="source-config-output.yaml"
tmp_file=$(mktemp "${output_file}.tmp.XXXXXX") || exit 1

if dmctl --master-addr 127.0.0.1:8261 config source mysql-replica-01 \
    | jq -er 'if .result then .cfg else error(.msg) end' > "$tmp_file"; then
  mv "$tmp_file" "$output_file" || { rm -f "$tmp_file"; exit 1; }
else
  rm -f "$tmp_file"
  exit 1
fi )
```

Before DM v6.0, use `get-config source <source-id>` instead of `config source <source-id>`.

{{< copyable "" >}}

```bash
config source mysql-replica-01
```

```
{
  "result": true,
    "msg": "",
    "cfg": "enable-gtid: false
      flavor: mysql
      source-id: mysql-replica-01
      from:
        host: 127.0.0.1
        port: 8407
        user: root
        password: '******'
}
```

If you don't know the `source-id`, you can run `dmctl --master-addr <master-addr> operate-source show` to list all data sources first.

{{< copyable "" >}}

```bash
operate-source show
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "source is added but there is no free worker to bound",
            "source": "mysql-replica-02",
            "worker": ""
        },
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

## Change the bindings between upstream MySQL instances and DM-workers

You can use the `transfer-source` command to change the bindings between upstream MySQL instances and DM-workers.

{{< copyable "" >}}

```bash
help transfer-source
```

```
Transfers an upstream MySQL/MariaDB source to a free worker.
Usage:
  dmctl transfer-source <source-id> <worker-id> [flags]
Flags:
  -h, --help   help for transfer-source
Global Flags:
  -s, --source strings   MySQL Source ID.
```

Before transferring, DM checks whether the worker to be unbound still has running tasks. If the worker has any running tasks, you need to [pause the tasks](/dm/dm-pause-task.md) first, change the binding, and then [resume the tasks](/dm/dm-resume-task.md).

### Usage example

If you do not know the bindings of DM-workers, you can run `dmctl --master-addr <master-addr> list-member --worker` to list the current bindings of all workers.

{{< copyable "" >}}

```bash
list-member --worker
```

```
{
    "result": true,
    "msg": "",
    "members": [
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "dm-worker-1",
                        "addr": "127.0.0.1:8262",
                        "stage": "bound",
                        "source": "mysql-replica-01"
                    },
                    {
                        "name": "dm-worker-2",
                        "addr": "127.0.0.1:8263",
                        "stage": "free",
                        "source": ""
                    }
                ]
            }
        }
    ]
}
```

In the above example, `mysql-replica-01` is bound to `dm-worker-1`. The below command transfers the binding worker of `mysql-replica-01` to `dm-worker-2`.

{{< copyable "" >}}

```bash
transfer-source mysql-replica-01 dm-worker-2
```

```
{
    "result": true,
    "msg": ""
}
```

Check whether the command takes effect by running `dmctl --master-addr <master-addr> list-member --worker`.

{{< copyable "" >}}

```bash
list-member --worker
```

```
{
    "result": true,
    "msg": "",
    "members": [
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "dm-worker-1",
                        "addr": "127.0.0.1:8262",
                        "stage": "free",
                        "source": ""
                    },
                    {
                        "name": "dm-worker-2",
                        "addr": "127.0.0.1:8263",
                        "stage": "bound",
                        "source": "mysql-replica-01"
                    }
                ]
            }
        }
    ]
}
```
