---
title: LOAD STATS
summary: An overview of the usage of LOAD STATS for the TiDB database.
---

# ロード統計 {#load-stats}

`LOAD STATS`ステートメントは、統計を TiDB にロードするために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 例 {#examples}

アドレス`http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}`にアクセスして、TiDB インスタンスの統計をダウンロードできます。

`LOAD STATS ${stats_path}`を使用して、特定の統計ファイルをロードすることもできます。

`${stats_path}`絶対パスまたは相対パスにすることができます。相対パスを使用する場合、対応するファイルは`tidb-server`が始まるパスから検索されます。次に例を示します。

{{< copyable "" >}}

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [統計](/statistics.md)
