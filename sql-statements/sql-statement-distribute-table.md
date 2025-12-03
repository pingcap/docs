---
title: DISTRIBUTE TABLE
summary: TiDB データベースの DISTRIBUTE TABLE の使用法の概要。
---

# DISTRIBUTE TABLE<span class="version-mark">バージョン8.5.4の新機能</span> {#distribute-table-span-class-version-mark-new-in-v8-5-4-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

</CustomContent>

`DISTRIBUTE TABLE`文は、指定されたテーブルのリージョンを再配分および再スケジュールし、テーブルレベルでバランスの取れた配分を実現します。この文を実行することで、リージョンが少数のTiFlashノードまたは TiKV ノードに集中するのを防ぎ、テーブル内のリージョンの不均一な配分の問題に対処できます。

## 概要 {#synopsis}

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier "TIMEOUT" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"
```

## パラメータの説明 {#parameter-description}

`DISTRIBUTE TABLE`ステートメントを使用してテーブル内のリージョンを再配分する場合、バランスの取れた配分のためにstorageエンジン ( TiFlashや TiKV など) とさまざまなRaftロール ( Leader、 Learner、 Voter など) を指定できます。

-   `RULE` : どのRaftロールのリージョンをバランス調整およびスケジュールするかを指定します。オプションの値は`"leader-scatter"` 、 `"peer-scatter"` 、 `"learner-scatter"`です。
-   `ENGINE` :storageエンジンを指定します。オプションの値は`"tikv"`と`"tiflash"`です。
-   `TIMEOUT` : スキャッタ処理のタイムアウト制限を指定します。PDがこの時間内にスキャッタ処理を完了しない場合、スキャッタタスクは自動的に終了します。このパラメータが指定されていない場合、デフォルト値は`"30m"`です。

## 例 {#examples}

表`t1`のリーダーの地域をTiKVに再分配します。

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 RULE = "leader-scatter" ENGINE = "tikv" TIMEOUT = "1h";
```

    +--------+
    | JOB_ID |
    +--------+
    |    100 |
    +--------+

表`t2`の学習者の領域をTiFlashに再分配します。

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 RULE = "learner-scatter" ENGINE = "tiflash";
```

    +--------+
    | JOB_ID |
    +--------+
    |    101 |
    +--------+

テーブル`t3`の`p1`と`p2`のパーティション内のピアのリージョンを TiKV で再配布します。

```sql
CREATE TABLE t3 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) RULE = "peer-scatter" ENGINE = "tikv";
```

    +--------+
    | JOB_ID |
    +--------+
    |    102 |
    +--------+

Learnerの領域をTiFlash上のテーブル`t4`の`p1`番目と`p2`パーティションに再分配します。

```sql
CREATE TABLE t4 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t4 PARTITION (p1, p2) RULE = "learner-scatter" ENGINE="tiflash";
```

    +--------+
    | JOB_ID |
    +--------+
    |    103 |
    +--------+

## 注記 {#notes}

テーブルのリージョンを再配分するリージョン`DISTRIBUTE TABLE`を実行すると、PD ホットスポット スケジューラの影響を受ける可能性があります。再配分後、このテーブルのリージョン配分は時間の経過とともに再び不均衡になる可能性があります。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
-   [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
-   [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
-   [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)
