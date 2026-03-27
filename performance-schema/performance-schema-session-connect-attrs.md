---
title: SESSION_CONNECT_ATTRS
summary: Learn the `SESSION_CONNECT_ATTRS` performance_schema table.
---

# SESSION\_CONNECT\_ATTRS

The `SESSION_CONNECT_ATTRS` table provides information about connection attributes. Session attributes are key-value pairs that are sent by the client when establishing a connection.

Common attributes:

| Attribute Name    | Example       | Description                |
|-------------------|---------------|----------------------------|
| `_client_name`    | `libmysql`    | Client library name        |
| `_client_version` | `8.0.33`      | Client library version     |
| `_os`             | `Linux`       | Operating System           |
| `_pid`            | `712927`      | Process ID                 |
| `_platform`       | `x86_64`      | CPU Architecture           |
| `program_name`    | `mysqlsh`     | Program name               |

You can view the columns of the `SESSION_CONNECT_ATTRS` table as follows:

{{< copyable "sql" >}}

```sql
USE performance_schema;
DESCRIBE session_connect_attrs;
```

```
+------------------+-----------------+------+------+---------+-------+
| Field            | Type            | Null | Key  | Default | Extra |
+------------------+-----------------+------+------+---------+-------+
| PROCESSLIST_ID   | bigint unsigned | NO   |      | NULL    |       |
| ATTR_NAME        | varchar(32)     | NO   |      | NULL    |       |
| ATTR_VALUE       | varchar(1024)   | YES  |      | NULL    |       |
| ORDINAL_POSITION | int             | YES  |      | NULL    |       |
+------------------+-----------------+------+------+---------+-------+
```

You can view the information on session attributes stored in the `SESSION_CONNECT_ATTRS` table as follows:

{{< copyable "sql" >}}

```sql
USE performance_schema;
TABLE SESSION_CONNECT_ATTRS;
```

```
+----------------+-----------------+------------+------------------+
| PROCESSLIST_ID | ATTR_NAME       | ATTR_VALUE | ORDINAL_POSITION |
+----------------+-----------------+------------+------------------+
|        2097154 | _client_name    | libmysql   |                0 |
|        2097154 | _client_version | 8.5.0      |                1 |
|        2097154 | _os             | Linux      |                2 |
|        2097154 | _pid            | 1299203    |                3 |
|        2097154 | _platform       | x86_64     |                4 |
|        2097154 | program_name    | mysqlsh    |                5 |
+----------------+-----------------+------------+------------------+
```

Fields in the `SESSION_CONNECT_ATTRS` table are described as follows:

* `PROCESSLIST_ID`: Processlist ID of the session.
* `ATTR_NAME`: Attribute name.
* `ATTR_VALUE`: Attribute value.
* `ORDINAL_POSITION`: Ordinal position of the name/value pair.

## Size limit and truncation

TiDB uses the [`performance_schema_session_connect_attrs_size`](/system-variables.md#performance_schema_session_connect_attrs_size-new-in-v900) global system variable to control the maximum total size of connection attributes per session.

- Default value: `4096` bytes
- Range: `[-1, 65536]`
- `-1` means no configured limit, and TiDB treats it as up to `65536` bytes.
- `0`, means that TiDB does not retain client-provided session connection attributes, which effectively disables recording session attributes.

When the total size exceeds this limit, TiDB truncates excess attributes and adds `_truncated` to indicate the number of truncated bytes.

The accepted connection attributes are also written to the `Session_connect_attrs` field in the slow log and can be queried from [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) and `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`. To control the payload size written to the slow log, adjust `performance_schema_session_connect_attrs_size`.

TiDB also enforces a hard limit of 1 MiB on connection attribute payload in handshake packets. If this hard limit is exceeded, the connection is rejected.
