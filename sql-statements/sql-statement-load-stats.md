---
title: LOAD STATS
summary: LOAD STATSステートメントは、TiDBに統計をロードするために使用されます。TiDBサーバーレスクラスターでは使用できません。LOAD STATS ${stats_path}を使用して特定の統計ファイルをロードすることもできます。絶対パスまたは相対パスにすることができます。相対パスを使用する場合は、tidb-serverで始まるパスから該当するファイルが検索されます。このステートメントは、MySQL構文に対するTiDB拡張機能です。統計を参照するには、統計を参照してください。
---

# 負荷統計 {#load-stats}

`LOAD STATS`ステートメントは、統計を TiDB にロードするために使用されます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 例 {#examples}

アドレス`http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}`にアクセスして、TiDB インスタンスの統計をダウンロードできます。

`LOAD STATS ${stats_path}`を使用して特定の統計ファイルをロードすることもできます。

`${stats_path}`絶対パスまたは相対パスにすることができます。相対パスを使用する場合は、 `tidb-server`で始まるパスから該当するファイルが検索されます。以下に例を示します。

```sql
LOAD STATS '/tmp/stats.json';
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [統計](/statistics.md)
