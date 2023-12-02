---
title: SHOW PLUGINS
summary: An overview of the usage of SHOW PLUGINS for the TiDB database.
---

# プラグインを表示 {#show-plugins}

`SHOW PLUGINS` TiDB にインストールされているすべてのプラグインを、各プラグインのステータスとバージョン情報を含めて表示します。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

**表示手順:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## 例 {#examples}

```sql
SHOW PLUGINS;
```

    +-------+--------------+-------+-----------------------------+---------+---------+
    | Name  | Status       | Type  | Library                     | License | Version |
    +-------+--------------+-------+-----------------------------+---------+---------+
    | audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
    +-------+--------------+-------+-----------------------------+---------+---------+
    1 row in set (0.000 sec)

```sql
SHOW PLUGINS LIKE 'a%';
```

    +-------+--------------+-------+-----------------------------+---------+---------+
    | Name  | Status       | Type  | Library                     | License | Version |
    +-------+--------------+-------+-----------------------------+---------+---------+
    | audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
    +-------+--------------+-------+-----------------------------+---------+---------+
    1 row in set (0.000 sec)

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SHOW PLUGINS`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .
