---
title: SHOW AFFINITY
summary: TiDB データベースに対する SHOW AFFINITY の使用法の概要。
---

# アフィニティを表示<span class="version-mark">v8.5.5 の新機能</span> {#show-affinity-span-class-version-mark-new-in-v8-5-5-span}

`SHOW AFFINITY`文は、 `AFFINITY`オプションで設定されたテーブルの[親和性](/table-affinity.md)スケジュール情報と、PD によって現在記録されているターゲット レプリカ分散を表示します。

## 概要 {#synopsis}

```ebnf+diagram
ShowAffinityStmt ::=
    "SHOW" "AFFINITY" ShowLikeOrWhereOpt
```

`SHOW AFFINITY` `LIKE`または`WHERE`句を使用してテーブル名をフィルタリングすることをサポートします。

## 例 {#examples}

次の例では、アフィニティ スケジュールを有効にした 2 つのテーブルを作成し、そのスケジュール情報を表示する方法を示します。

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
CREATE TABLE tp1 (a INT) AFFINITY = 'partition' PARTITION BY HASH(a) PARTITIONS 2;

SHOW AFFINITY;
```

出力例は次のとおりです。

```sql
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| Db_name | Table_name | Partition_name | Leader_store_id | Voter_store_ids  | Status   | Region_count | Affinity_region_count|
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| test    | t1         | NULL           | 1               | 1,2,3            | Stable   |            8 |                    8 |
| test    | tp1        | p0             | 4               | 4,5,6            | Preparing|            4 |                    2 |
| test    | tp1        | p1             | 4               | 4,5,6            | Preparing|            3 |                    2 |
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
```

各列の意味は次のとおりです。

-   `Leader_store_id` 、 `Voter_store_ids` : PDによって記録されたTiKVストアのID。テーブルまたはパーティションのターゲットLeaderとVoterレプリカをホストするストアを示します。アフィニティグループのターゲットレプリカの場所が決定されていない場合、または[`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855) `0`に設定されている場合、値は`NULL`と表示されます。
-   `Status` : アフィニティスケジューリングの現在の状態を示します。可能な値は次のとおりです。
    -   `Pending` : リーダーまたは投票者がまだ決定されていない場合など、PD はテーブルまたはパーティションのアフィニティ スケジューリングを開始していません。
    -   `Preparing` : PD はアフィニティ要件を満たすように領域をスケジュールしています。
    -   `Stable` : すべてのリージョンが目標配布に到達しました。
-   `Region_count` : アフィニティ グループ内の現在のリージョン数。
-   `Affinity_region_count` : 現在アフィニティレプリカ分散要件を満たしているリージョンの数。
    -   `Affinity_region_count` `Region_count`未満の場合、一部のリージョンがアフィニティに基づいてレプリカのスケジュールをまだ完了していないことを示します。
    -   `Affinity_region_count` `Region_count`に等しい場合、アフィニティに基づくレプリカのスケジューリングが完了していることを示します。つまり、関連するすべてのリージョンの分散がアフィニティ要件を満たしていることを意味します。ただし、これは関連するリージョンのマージ操作が完了したことを示すものではありません。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
-   [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
