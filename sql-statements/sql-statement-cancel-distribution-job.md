---
title: CANCEL DISTRIBUTION JOB
summary: TiDB での CANCEL DISTRIBUTION JOB の使用法の概要。
---

# 配布ジョブのキャンセル<span class="version-mark">v8.5.4 の新機能</span> {#cancel-distribution-job-span-class-version-mark-new-in-v8-5-4-span}

`CANCEL DISTRIBUTION JOB`ステートメントは、TiDB の[`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)ステートメントを使用して作成されたリージョンスケジュール タスクをキャンセルするために使用されます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

</CustomContent>

## 概要 {#synopsis}

```ebnf+diagram
CancelDistributionJobsStmt ::=
    'CANCEL' 'DISTRIBUTION' 'JOB' JobID
```

## 例 {#examples}

次の例では、ID `1`の配布ジョブをキャンセルします。

```sql
CANCEL DISTRIBUTION JOB 1;
```

出力は次のようになります。

    Query OK, 0 rows affected (0.01 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
