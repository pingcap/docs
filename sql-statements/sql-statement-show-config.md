---
title: SHOW CONFIG
summary: Overview of the use of SHOW CONFIG in the TiDB database
---

# 設定を表示 {#show-config}

`SHOW CONFIG`ステートメントは、TiDB のさまざまなコンポーネントの現在の構成を示すために使用されます。構成変数とシステム変数は異なる次元で機能するため、混同しないように注意してください。システム変数情報を取得したい場合は、 [変数を表示](/sql-statements/sql-statement-show-variables.md)構文を使用します。

> **注記：**
>
> この機能は TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

## あらすじ {#synopsis}

**表示手順:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## 例 {#examples}

すべての構成を表示します。

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

`type`が`tidb`である構成を示します。

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

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [変数を表示](/sql-statements/sql-statement-show-variables.md)
