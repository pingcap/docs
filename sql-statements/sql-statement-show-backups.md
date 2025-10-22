---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: TiDB データベースに対する SHOW [BACKUPS|RESTORES] の使用法の概要。
---

# 表示 [バックアップ|復元] {#show-backups-restores}

これらのステートメントは、TiDB インスタンスで実行されたキューに入れられたタスク、実行中のタスク、最近完了したタスク[`BACKUP`](/sql-statements/sql-statement-backup.md)と[`RESTORE`](/sql-statements/sql-statement-restore.md)リストを表示します。

どちらのステートメントも、実行には`SUPER`権限が必要です。

`BACKUP`タスクを照会するには`SHOW BACKUPS`使用し、 `RESTORE`タスクを照会するには`SHOW RESTORES`使用します。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

`br`コマンドライン ツールで開始されたバックアップと復元は表示されません。

## 概要 {#synopsis}

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

バックアップが完了する前に、新しい接続で`SHOW BACKUPS`実行します。

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

上記の結果の最初の行は次のように記述されます。

| カラム              | 説明                                                                   |
| :--------------- | :------------------------------------------------------------------- |
| `Destination`    | 宛先 URL（秘密鍵の漏洩を防ぐため、すべてのパラメータを削除）                                     |
| `State`          | タスクの状態                                                               |
| `Progress`       | 現在の状態における進捗状況の推定値（パーセント）                                             |
| `Queue_time`     | タスクがキューに入れられたとき                                                      |
| `Execution_time` | タスクが開始されたとき。キューイングタスクの場合は値は`0000-00-00 00:00:00`です。                  |
| `Finish_time`    | タスクが終了したときのタイムスタンプ。キューイングおよび実行中のタスクの場合、値は`0000-00-00 00:00:00`になります。 |
| `Connection`     | このタスクを実行している接続ID                                                     |
| `Message`        | 詳細を記載したメッセージ                                                         |

可能な状態は次のとおりです:

| 州      | 説明          |
| :----- | :---------- |
| バックアップ | バックアップを作成する |
| 待って    | 実行待ち        |
| チェックサム | チェックサム操作の実行 |

接続 ID は、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを介してバックアップ/復元タスクをキャンセルするために使用できます。

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### フィルタリング {#filtering}

`LIKE`句を使用して、宛先 URL をワイルドカード式と照合し、タスクを除外します。

```sql
SHOW BACKUPS LIKE 's3://%';
```

列でフィルタリングするには、 `WHERE`句を使用します。

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元する](/sql-statements/sql-statement-restore.md)
