---
title: CANCEL DISTRIBUTION JOB
summary: TiDBにおけるCANCEL DISTRIBUTION JOBの使用方法の概要。
---

# 配布ジョブのキャンセル<span class="version-mark">（v8.5.4の新機能）</span> {#cancel-distribution-job-span-class-version-mark-new-in-v8-5-4-span}

`CANCEL DISTRIBUTION JOB`ステートメントは、TiDB の[`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)ステートメントを使用して作成されたリージョンスケジューリング タスクをキャンセルするために使用されます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

</CustomContent>

## あらすじ {#synopsis}

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

## 関連項目 {#see-also}

-   [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
