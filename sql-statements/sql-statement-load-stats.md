---
title: LOAD STATS
summary: An overview of the usage of LOAD STATS for the TiDB database.
---

# 統計のロード {#load-stats}

`LOAD STATS`ステートメントは、統計をTiDBにロードするために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 例 {#examples}

アドレス`http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}`にアクセスして、TiDBインスタンスの統計をダウンロードできます。

`LOAD STATS ${stats_path}`を使用して、特定の統計ファイルをロードすることもできます。

`${stats_path}`は、絶対パスまたは相対パスにすることができます。相対パスを使用する場合、対応するファイルは`tidb-server`が開始されたパスから始まります。次に例を示します。

{{< copyable "" >}}

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [統計](/statistics.md)
