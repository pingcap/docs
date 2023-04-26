---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [BACKUPS|RESTORES] for the TiDB database.
---

# [バックアップ|復元] を表示 {#show-backups-restores}

これらのステートメントは、TiDB インスタンスで実行された、キューに入れられた、実行中の、および最近終了した[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)のすべてのタスクのリストを表示します。

両方のステートメントを実行するには、 `SUPER`特権が必要です。

`SHOW BACKUPS`を使用して`BACKUP`タスクを照会し、 `SHOW RESTORES`を使用して`RESTORE`タスクを照会します。

`br`コマンドライン ツールで開始されたバックアップと復元は表示されません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

1 つの接続で、次のステートメントを実行します。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

バックアップが完了する前に、新しい接続で`SHOW BACKUPS`を実行します。

{{< copyable "" >}}

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

上記の結果の最初の行は、次のように記述されます。

| カラム              | 説明                                                                |
| :--------------- | :---------------------------------------------------------------- |
| `Destination`    | 宛先 URL (秘密鍵の漏洩を防ぐためにすべてのパラメーターが削除されています)                          |
| `State`          | タスクの状態                                                            |
| `Progress`       | パーセンテージとしての現在の状態での推定進行状況                                          |
| `Queue_time`     | タスクがキューに入れられたとき                                                   |
| `Execution_time` | タスクが開始されたとき。タスクをキューに入れる場合、値は`0000-00-00 00:00:00`です。              |
| `Finish_time`    | タスクが終了したときのタイムスタンプ。キューイングおよび実行中のタスクの場合、値は`0000-00-00 00:00:00`です。 |
| `Connection`     | このタスクを実行する接続 ID                                                   |
| `Message`        | 詳細を含むメッセージ                                                        |

可能な状態は次のとおりです。

| 州      | 説明          |
| :----- | :---------- |
| バックアップ | バックアップの作成   |
| 待って    | 実行待ち        |
| チェックサム | チェックサム操作の実行 |

接続 ID を使用して、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを介してバックアップ/復元タスクをキャンセルできます。

{{< copyable "" >}}

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### フィルタリング {#filtering}

`LIKE`句を使用して、宛先 URL をワイルドカード式と照合してタスクを除外します。

{{< copyable "" >}}

```sql
SHOW BACKUPS LIKE 's3://%';
```

`WHERE`句を使用して、列でフィルタリングします。

{{< copyable "" >}}

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [戻す](/sql-statements/sql-statement-restore.md)
