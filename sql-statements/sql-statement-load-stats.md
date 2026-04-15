---
title: LOAD STATS
summary: TiDBデータベースにおけるLOAD STATSの使用方法の概要。
---

# ロード統計 {#load-stats}

`LOAD STATS`ステートメントは、統計情報を TiDB にロードするために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 例 {#examples}

TiDBインスタンスの統計情報をダウンロードするには、アドレス`http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}`アクセスしてください。

`LOAD STATS ${stats_path}`を使用して、特定の統計ファイルを読み込むこともできます。

`${stats_path}`は絶対パスまたは相対パスを指定できます。相対パスを使用する場合、対応するファイルは`tidb-server`の開始パスから検索されます。以下に例を示します。

```sql
LOAD STATS '/tmp/stats.json';
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [統計](/statistics.md)
