---
title: SESSION_CONNECT_ATTRS
summary: SESSION_CONNECT_ATTRS` パフォーマンス スキーマ テーブルについて学習します。
---

# セッション接続属性 {#session-connect-attrs}

`SESSION_CONNECT_ATTRS`の表は、接続属性に関する情報を提供します。セッション属性は、接続を確立するときにクライアントによって送信されるキーと値のペアです。

共通の属性:

| 属性名               | 例          | 説明                |
| ----------------- | ---------- | ----------------- |
| `_client_name`    | `libmysql` | クライアントライブラリ名      |
| `_client_version` | `8.0.33`   | クライアントライブラリのバージョン |
| `_os`             | `Linux`    | オペレーティング·システム     |
| `_pid`            | `712927`   | プロセスID            |
| `_platform`       | `x86_64`   | CPUアーキテクチャ        |
| `program_name`    | `mysqlsh`  | プログラム名            |

`SESSION_CONNECT_ATTRS`のテーブルの列は次のように表示できます。

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

`SESSION_CONNECT_ATTRS`テーブルに保存されているセッション属性の情報は、次のように表示できます。

```sql
USE performance_schema;
TABLE SESSION_CONNECT_ATTRS;
```

    +----------------+-----------------+------------+------------------+
    | PROCESSLIST_ID | ATTR_NAME       | ATTR_VALUE | ORDINAL_POSITION |
    +----------------+-----------------+------------+------------------+
    |        2097154 | _client_name    | libmysql   |                0 |
    |        2097154 | _client_version | 8.1.1      |                1 |
    |        2097154 | _os             | Linux      |                2 |
    |        2097154 | _pid            | 1299203    |                3 |
    |        2097154 | _platform       | x86_64     |                4 |
    |        2097154 | program_name    | mysqlsh    |                5 |
    +----------------+-----------------+------------+------------------+

`SESSION_CONNECT_ATTRS`のテーブル内のフィールドは次のように説明されます。

-   `PROCESSLIST_ID` : セッションのプロセスリスト ID。
-   `ATTR_NAME` : 属性名。
-   `ATTR_VALUE` : 属性値。
-   `ORDINAL_POSITION` : 名前/値のペアの順序位置。
