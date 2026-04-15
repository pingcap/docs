---
title: DISTRIBUTE TABLE
summary: TiDBデータベースにおけるDISTRIBUTE T​​ABLEの使用方法の概要。
---

# 分散テーブル<span class="version-mark">（v8.5.4の新機能）</span> {#distribute-table-span-class-version-mark-new-in-v8-5-4-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

</CustomContent>

`DISTRIBUTE TABLE`ステートメントは、指定されたテーブルのリージョンを再分配および再スケジュールし、テーブルレベルでバランスの取れた分散を実現します。このステートメントを実行することで、リージョンが少数のTiFlashまたは TiKV ノードに集中するのを防ぎ、テーブル内のリージョンの分散が不均一になる問題を解決できます。

## あらすじ {#synopsis}

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier "TIMEOUT" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"
```

## パラメータの説明 {#parameter-description}

`DISTRIBUTE TABLE`ステートメントを使用してテーブル内のリージョンを再分配する場合、バランスの取れた分配のために、storageエンジン ( TiFlashや TiKV など) とさまざまなRaftロール (Leader、Learner、投票者など) を指定できます。

-   `RULE` : バランス調整とスケジュールを行うRaftロールのリージョンを指定します。オプションの値は`"leader-scatter"` 、 `"peer-scatter"` 、および`"learner-scatter"` 。
-   `ENGINE` :storageエンジンを指定します。オプションの値は`"tikv"`と`"tiflash"` 。
-   `TIMEOUT` : 散布操作のタイムアウト制限を指定します。PD がこの時間内に散布を完了しない場合、散布タスクは自動的に終了します。このパラメーターが指定されていない場合、デフォルト値は`"30m"`です。

## 例 {#examples}

TiKV 上の表`t1`のリーダーの領域を再分配します。

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

TiFlash上の表`t2`内の学習者の領域を再分配します。

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

TiKV 上のテーブル`t3`の`p1`および`p2`パーティション内のピアのリージョンを再分配します。

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

TiFlash 上のテーブル`t4`の`p1`および`p2`TiFlashでLearnerの領域を再分配します。

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

`DISTRIBUTE TABLE`ステートメントを実行してテーブルのリージョンを再分配すると、リージョンの分配結果が PD ホットスポット スケジューラの影響を受ける可能性があります。再分配後、このテーブルのリージョンの分配は時間の経過とともに再び不均衡になる可能性があります。

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
-   [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
-   [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
-   [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)
