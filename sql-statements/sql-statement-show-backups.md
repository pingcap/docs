---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるSHOW [BACKUPS|RESTORES]の使用方法の概要。
---

# [バックアップ|復元]を表示 {#show-backups-restores}

これらのステートメントは、TiDBインスタンスで実行された、キューに入っている、実行中の、および最近完了したすべての[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)タスクのリストを示します。

どちらのステートメントも、実行するには`SUPER`権限が必要です。

`SHOW BACKUPS`を使用して`BACKUP`タスクを照会し、 `SHOW RESTORES`を使用して`RESTORE`タスクを照会します。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

`br`コマンドラインツールを使用して開始されたバックアップとリストアは表示されません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

1つの接続で、次のステートメントを実行します。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

バックアップが完了する前に、新しい接続で`SHOW BACKUPS`を実行してください。

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| Destination                    | State   | Progress | Queue_time          | Execution_time      | Finish_time | Connection | Message |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 | NULL    |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
1 row in set (0.00 sec)
```

上記の結果の最初の行は、次のように説明されています。

| カラム              | 説明                                                                |
| :--------------- | :---------------------------------------------------------------- |
| `Destination`    | 宛先URL（秘密鍵の漏洩を防ぐため、すべてのパラメータは削除済み）                                 |
| `State`          | タスクの状況                                                            |
| `Progress`       | 現状における推定進捗率（パーセント）                                                |
| `Queue_time`     | タスクがキューに入れられたとき                                                   |
| `Execution_time` | タスクが開始されたとき、キューイングタスクの値は`0000-00-00 00:00:00`です。                  |
| `Finish_time`    | タスクが完了したときのタイムスタンプ。キューイングおよび実行中のタスクの場合、値は`0000-00-00 00:00:00`です。 |
| `Connection`     | このタスクを実行している接続ID                                                  |
| `Message`        | 詳細を添えたメッセージ                                                       |

考えられる状態は以下のとおりです。

| 州      | 説明           |
| :----- | :----------- |
| バックアップ | バックアップを作成する  |
| 待って    | 処刑を待っている     |
| チェックサム | チェックサム操作を実行中 |

接続IDは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してバックアップ/リストアタスクをキャンセルするために使用できます。

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### フィルタリング {#filtering}

`LIKE`句を使用して、宛先URLをワイルドカード式と照合することでタスクをフィルタリングします。

```sql
SHOW BACKUPS LIKE 's3://%';
```

`WHERE`句を使用して、列でフィルタリングします。

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元する](/sql-statements/sql-statement-restore.md)
