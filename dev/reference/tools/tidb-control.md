---
title: TiDB Controller User Guide
summary: Use TiDB Controller to obtain TiDB status information for debugging.
category: reference
aliases: ['/docs/tools/tidb-controller/']
---

# TiDB Controller User Guide

TiDB Controller is a command line tool of TiDB, usually used to obtain the status information of TiDB for debugging.

## Compile from source code

- Compilation environment requirement: [Go](https://golang.org/) Version 1.7 or later
- Compilation procedures: Go to the root directory of the [TiDB Controller project](https://github.com/pingcap/tidb-ctl), use the `make` command to compile, and generate `tidb-ctl`.
- Compilation documentation: you can find the help files in the `doc` directory; if the help files are lost or you want to update them, use the `make doc` command to generate the help files.

## Usage introduction

The usage of `tidb-ctl` consists of command (including subcommand), option, and flag.

- command: characters without `-` or `--`
- option: characters with `-` or `--`
- flag: characters exactly following the command or option, passing value to the command or option

Usage example: `tidb-ctl schema in mysql -n db`

- `schema`: the command
- `in`: the subcommand of schema
- `mysql`: the flag of `in`
- `-n`: the option
- `db`: the flag of `-n`

### Get help

Use `tidb-ctl -h/--help` to get the help information. `tidb-ctl` consists of multiple layers of commands. You can use `-h/--help` to get the help information of `tidb-ctl` and all other subcommands.

### Connect

```
tidb-ctl -H/--host {TiDB service address} -P/--port {TiDB service port}
`tidb-ctl` has 4 connection related parameters, which are:
```

- `--host`: TiDB Service address
- `--port`: TiDB Service port
- `--pdhost`: PD Service address
- `--pdport`: PD Service port

`--pdhost` and `--pdport` are mainly used for the `etcd` subcommand, for example: `tidb-ctl etcd ddlinfo`. If you do not add an address and port, the default value will be used. The default address of the TiDB/PD service is 127.0.0.1 (the service address can only use the IP address). The default port of the TiDB service port is 10080, and the default port of the PD service port is 2379. **The connection option is a global option and applies to all of the following commands.**

Currently, TiDB Controller supports the following subcommands. You could obtain the usage of them using the `tidb-ctl SUBCOMMAND --help` command.

- `tidb-ctl base64decode`: BASE64 decode
- `tidb-ctl decoder`: For KEY decode
- `tidb-ctl etcd`: For operating etcd
- `tidb-ctl log`: Format the log file to expand the single-line stack information
- `tidb-ctl mvcc`: MVCC information
- `tidb-ctl region`: Region information
- `tidb-ctl schema`: Schema information
- `tidb-ctl table`: Table information

### Examples

The following example shows how to obtain the schema information:

Use `tidb-ctl schema -h` to get the help information of the subcommands. `schema` has two subcommands: `in` and `tid`.

- `in` is used to obtain the table schema of all tables in the database through the database name.
- `tid` is used to obtain the table schema through the unique `table_id` in the whole database.

#### The `in` command

You can also use `tidb-ctl schema in -h/--help` to get the help information of the `in` subcommand.

##### Basic usage

```
tidb-ctl schema in {database name}
```

For example, `tidb-ctl schema in mysql` returns the following result:

```json
[
    {
        "id": 13,
        "name": {
            "O": "columns_priv",
            "L": "columns_priv"
        },
              ...
        "update_timestamp": 399494726837600268,
        "ShardRowIDBits": 0,
        "Partition": null
    }
]
```

The result is long and displayed in JSON. The above result is a truncated one.

- If you want to specify the table name, use `tidb-ctl schema in {database} -n {table name}` to filter.

    For example, `tidb-ctl schema in mysql -n db` returns the table schema of the `db` table in the `mysql` database:

    ```json
    {
        "id": 9,
        "name": {
            "O": "db",
            "L": "db"
        },
        ...
        "Partition": null
    }
    ```

    The above result is a truncated one, too.
    If the TiDB address in use is not the default address and port, you can use the command line argument `--host`, `--port` option, such as: `tidb-ctl --host 172.16.55.88 --port 8898 schema in mysql -n db`.

#### base64decode subcommand

`base64decode` is used to decode base64 data.

```shell
tidb-ctl base64decode [base64_data]
tidb-ctl base64decode [db_name.table_name] [base64_data]
tidb-ctl base64decode [table_id] [base64_data]
```

- Execute the following SQL to prepare the environment.

    ```sql
    use test;
    create table t (a int, b varchar(20),c datetime default current_timestamp , d timestamp default current_timestamp, unique index(a));
    insert into t (a,b,c) values(1,"哈哈 hello",NULL);
    alter table t add column e varchar(20);
    ```

- Obtian mvcc data using http api interface

    ```shell
    ▶ curl "http://$IP:10080/mvcc/index/test/t/a/1?a=1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306449994645510,
        "commit_ts": 407306449994645513,
        "short_value": "AAAAAAAAAAE="    # unique index a stores the handle id of the corresponding row.
       }
      ]
     }
    }%

    ▶ curl "http://$IP:10080/mvcc/key/test/t/1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306588892692486,
        "commit_ts": 407306588892692489,
        "short_value": "CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk="  # Row data that handle id is 1.
       }
      ]
     }
    }% 
    ```

- Decode handle id (uint64) using `base64decode`.

  ```shell
  ▶ tidb-ctl base64decode AAAAAAAAAAE=
  hex: 0000000000000001
  uint64: 1
  ```

- Decode row data using `base64decode`.

    ```shell
    ▶ ./tidb-ctl base64decode test.t CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data

    # if the table id of test.t is 60, you can also use below command to do the same thing.
    ▶ ./tidb-ctl base64decode 60 CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data
    ```

#### decoder subcommand

- The following example shows how to decode row key. Decoding index key is similar to that.

    ```shell
    ▶ ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

- The following example shows how to decode value.

    ```shell
    ▶ ./tidb-ctl decoder -f value -k AhZoZWxsbyB3b3JsZAiAEA==
    type: bytes, value: hello world
    type: bigint, value: 1024
    ```

#### etcd subcommand

- `tidb-ctl etcd ddlinfo` is used to obtain DDL information.
- `tidb-ctl etcd putkey KEY VALUE` is used to add KEY VALUE to etcd (All the KEY are added to the `/tidb/ddl/all_schema_versions/`).

    ```shell
    tidb-ctl etcd putkey "foo" "bar"
    ```

    Actually, a Key-value pair is added to the etcd whose KEY is `/tidb/ddl/all_schema_versions/foo` and VALUE is `bar`.

- `tidb-ctl etcd delkey` deletes the KEY in etcd. Only those KEY start with `/tidb/ddl/fg/owner/` and `/tidb/ddl/all_schema_versions/` are permitted to be deleted.

    ```shell
    tidb-ctl etcd delkey "/tidb/ddl/fg/owner/foo"
    tidb-ctl etcd delkey "/tidb/ddl/all_schema_versions/bar"
    ```

#### log subcommand

The erro log of TiDB is wiritten in one line. You could use `tidb-ctl log` to change its format to multiple lines.

- If you want to specify the server address, use the `-H -P` option.

    For example, `tidb-ctl -H 127.0.0.1 -P 10080 schema in mysql -n db`.
