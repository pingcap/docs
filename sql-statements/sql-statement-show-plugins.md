---
title: SHOW PLUGINS
summary: TiDBデータベースにおけるSHOW PLUGINSの使用方法の概要。
---

# SHOW PLUGINS {#show-plugins}

`SHOW PLUGINS`は、TiDB にインストールされているすべてのプラグインと、各プラグインの状態およびバージョン情報を表示します。

> **Note:**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

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

## MySQLとの互換性 {#mysql-compatibility}

TiDB の`SHOW PLUGINS`ステートメントは、MySQL と完全な互換性があります。互換性の違いを見つけた場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)。

## 参照 {#see-also}

-   [`ADMIN PLUGINS`](/sql-statements/sql-statement-admin.md#admin-plugins-related-statement)
