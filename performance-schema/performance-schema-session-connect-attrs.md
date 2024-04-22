---
title: SESSION_CONNECT_ATTRS
summary: `SESSION_CONNECT_ATTRS`は、接続属性に関する情報を提供します。セッション属性は、接続の確立時にクライアントによって送信されるキーと値のペアです。共通の属性には、`_client_name`、`_client_version`、`_os`、`_pid`、`_platform`、`program_name`があります。`SESSION_CONNECT_ATTRS`テーブルの列は、`PROCESSLIST_ID`、`ATTR_NAME`、`ATTR_VALUE`、`ORDINAL_POSITION`で構成されています。これにより、セッション属性に関する情報を表示できます。
---

# SESSION_CONNECT_ATTRS {#session-connect-attrs}

表`SESSION_CONNECT_ATTRS`は、接続属性に関する情報を提供します。セッション属性は、接続の確立時にクライアントによって送信されるキーと値のペアです。

共通の属性:

| 属性名               | 例          | 説明                |
| ----------------- | ---------- | ----------------- |
| `_client_name`    | `libmysql` | クライアントライブラリ名      |
| `_client_version` | `8.0.33`   | クライアントライブラリのバージョン |
| `_os`             | `Linux`    | オペレーティング·システム     |
| `_pid`            | `712927`   | プロセスID            |
| `_platform`       | `x86_64`   | CPUアーキテクチャ        |
| `program_name`    | `mysqlsh`  | 番組名               |

`SESSION_CONNECT_ATTRS`テーブルの列は次のように表示できます。

```sql
USE performance_schema;
DESCRIBE session_connect_attrs;
```

    +------------------+---------------------+------+-----+---------+-------+
    | Field            | Type                | Null | Key | Default | Extra |
    +------------------+---------------------+------+-----+---------+-------+
    | PROCESSLIST_ID   | bigint(20) unsigned | NO   |     | NULL    |       |
    | ATTR_NAME        | varchar(32)         | NO   |     | NULL    |       |
    | ATTR_VALUE       | varchar(1024)       | YES  |     | NULL    |       |
    | ORDINAL_POSITION | int(11)             | YES  |     | NULL    |       |
    +------------------+---------------------+------+-----+---------+-------+

`SESSION_CONNECT_ATTRS`テーブルに保存されているセッション属性に関する情報は、次のようにして表示できます。

```sql
USE performance_schema;
TABLE SESSION_CONNECT_ATTRS;
```

    +----------------+-----------------+------------+------------------+
    | PROCESSLIST_ID | ATTR_NAME       | ATTR_VALUE | ORDINAL_POSITION |
    +----------------+-----------------+------------+------------------+
    |        2097154 | _client_name    | libmysql   |                0 |
    |        2097154 | _client_version | 8.1.0      |                1 |
    |        2097154 | _os             | Linux      |                2 |
    |        2097154 | _pid            | 1299203    |                3 |
    |        2097154 | _platform       | x86_64     |                4 |
    |        2097154 | program_name    | mysqlsh    |                5 |
    +----------------+-----------------+------------+------------------+

`SESSION_CONNECT_ATTRS`テーブルのフィールドは次のように説明されています。

-   `PROCESSLIST_ID` : セッションのプロセスリスト ID。
-   `ATTR_NAME` : 属性名。
-   `ATTR_VALUE` : 属性値。
-   `ORDINAL_POSITION` : 名前と値のペアの順序位置。
