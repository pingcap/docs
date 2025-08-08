---
title: SHOW CONFIG
summary: TiDBデータベースにおけるSHOW CONFIGの使用の概要
---

# 設定を表示 {#show-config}

`SHOW CONFIG`文は、TiDB の様々なコンポーネントの現在の設定を表示するために使用されます。設定変数とシステム変数は異なる次元で作用するため、混同しないように注意してください。システム変数の情報を取得する場合は、 [変数を表示](/sql-statements/sql-statement-show-variables.md)構文を使用してください。

> **注記：**
>
> この機能は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

## 概要 {#synopsis}

```ebnf+diagram
ShowConfigStmt ::=
    "SHOW" "CONFIG" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

すべての構成を表示:

```sql
SHOW CONFIG;
```

    +------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
    | Type | Instance       | Name                                            | Value                                                               |
    +------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
    | tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
    | tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
    | tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
    ...
    120 rows in set (0.01 sec)

`type`が`tidb`である構成を表示します。

```sql
SHOW CONFIG WHERE type = 'tidb' AND name = 'advertise-address';
```

    +------+----------------+-------------------+-----------+
    | Type | Instance       | Name              | Value     |
    +------+----------------+-------------------+-----------+
    | tidb | 127.0.0.1:4000 | advertise-address | 127.0.0.1 |
    +------+----------------+-------------------+-----------+
    1 row in set (0.05 sec)

`LIKE`句を使用して、 `type`が`tidb`である構成を示すこともできます。

```sql
SHOW CONFIG LIKE 'tidb';
```

    +------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
    | Type | Instance       | Name                                            | Value                                                               |
    +------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
    | tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
    | tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
    | tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
    ...
    40 rows in set (0.01 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [変数を表示](/sql-statements/sql-statement-show-variables.md)
