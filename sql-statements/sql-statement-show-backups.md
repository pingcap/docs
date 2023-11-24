---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [BACKUPS|RESTORES] for the TiDB database.
---

# [バックアップ|復元]を表示 {#show-backups-restores}

これらのステートメントは、TiDB インスタンス上で実行された、キューに入れられ、実行中、および最近終了したすべてのタスク[`BACKUP`](/sql-statements/sql-statement-backup.md)および[`RESTORE`](/sql-statements/sql-statement-restore.md)リストを表示します。

どちらのステートメントも実行するには`SUPER`権限が必要です。

`BACKUP`タスクをクエリするには`SHOW BACKUPS`使用し、 `RESTORE`タスクをクエリするには`SHOW RESTORES`使用します。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

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

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

バックアップが完了する前に、新しい接続で`SHOW BACKUPS`を実行します。

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

上記の結果の最初の行は次のように説明されます。

| カラム              | 説明                                                              |
| :--------------- | :-------------------------------------------------------------- |
| `Destination`    | 宛先 URL (秘密キーの漏洩を避けるためにすべてのパラメータが削除されています)                       |
| `State`          | タスクの状態                                                          |
| `Progress`       | 現在の状態の推定進捗状況 (パーセンテージ)                                          |
| `Queue_time`     | タスクがキューに入れられたとき                                                 |
| `Execution_time` | タスクが開始されたとき。タスクをキューに入れる場合、値は`0000-00-00 00:00:00`です。            |
| `Finish_time`    | タスクが終了したときのタイムスタンプ。タスクをキューに入れて実行する場合、値は`0000-00-00 00:00:00`です。 |
| `Connection`     | このタスクを実行する接続 ID                                                 |
| `Message`        | 詳細を含むメッセージ                                                      |

考えられる状態は次のとおりです。

| 州      | 説明          |
| :----- | :---------- |
| バックアップ | バックアップの作成   |
| 待って    | 実行を待っています   |
| チェックサム | チェックサム操作の実行 |

接続 ID を使用して、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメント経由でバックアップ/復元タスクをキャンセルできます。

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### フィルタリング {#filtering}

`LIKE`句を使用して、宛先 URL をワイルドカード式と照合してタスクを除外します。

```sql
SHOW BACKUPS LIKE 's3://%';
```

列でフィルターするには`WHERE`句を使用します。

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元する](/sql-statements/sql-statement-restore.md)
