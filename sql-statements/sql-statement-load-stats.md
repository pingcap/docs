---
title: LOAD STATS
summary: TiDB データベースの LOAD STATS の使用法の概要。
---

# 負荷統計 {#load-stats}

`LOAD STATS`ステートメントは、統計を TiDB にロードするために使用されます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 例 {#examples}

アドレス`http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}`アクセスすると、TiDB インスタンスの統計をダウンロードできます。

`LOAD STATS ${stats_path}`使用して特定の統計ファイルを読み込むこともできます。

`${stats_path}`絶対パスでも相対パスでも構いません。相対パスを使用した場合、対応するファイルは`tidb-server`開始するパスから検索されます。以下に例を示します。

```sql
LOAD STATS '/tmp/stats.json';
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [統計](/statistics.md)
