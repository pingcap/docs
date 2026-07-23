---
title: CANCEL DISTRIBUTION JOB
summary: TiDBにおけるCANCEL DISTRIBUTION JOBの使用方法の概要。
---

# CANCEL DISTRIBUTION JOB <span class="version-mark">New in v8.5.4 and v9.0.0</span> {#cancel-distribution-job-new-in-v854}

`CANCEL DISTRIBUTION JOB`ステートメントは、TiDB の[`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)ステートメントを使用して作成されたリージョンスケジューリング タスクをキャンセルするために使用されます。

> **Note:**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## 概要 {#synopsis}

```ebnf+diagram
CancelDistributionJobsStmt ::=
    'CANCEL' 'DISTRIBUTION' 'JOB' JobID
```

## 例 {#examples}

次の例では、IDが`1`の配布ジョブをキャンセルします。

```sql
CANCEL DISTRIBUTION JOB 1;
```

出力は以下のとおりです。

    Query OK, 0 rows affected (0.01 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 参照 {#see-also}

-   [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)