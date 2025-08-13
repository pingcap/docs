---
title: SHOW PLUGINS
summary: TiDB データベースの SHOW PLUGINS の使用法の概要。
---

# プラグインを表示 {#show-plugins}

`SHOW PLUGINS` 、各プラグインのステータスとバージョン情報を含む、TiDB にインストールされているすべてのプラグインを表示します。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

```ebnf+diagram
ShowPluginsStmt ::=
    "SHOW" "PLUGINS" ShowLikeOrWhere?
```

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

TiDBの`SHOW PLUGINS`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [`ADMIN PLUGINS`](/sql-statements/sql-statement-admin.md#admin-plugins-related-statement)
