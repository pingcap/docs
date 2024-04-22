---
title: CANCEL IMPORT
summary: TiDBのCANCEL IMPORTステートメントは、データインポートジョブをキャンセルするために使用されます。キャンセルするには、インポートジョブの作成者であるか、SUPER権限を持っている必要があります。例えば、IDが1のインポートジョブをキャンセルするには、CANCEL IMPORT JOB 1;と実行します。このステートメントはMySQL構文に対するTiDBの拡張機能であり、関連するステートメントにはIMPORT INTOとSHOW IMPORT JOBがあります。
---

# インポートのキャンセル {#cancel-import}

`CANCEL IMPORT`ステートメントは、TiDB で作成されたデータ インポート ジョブをキャンセルするために使用されます。

<!-- Support note for TiDB Cloud:

This TiDB statement is not applicable to TiDB Cloud.

-->

## 必要な権限 {#required-privileges}

データ インポート ジョブをキャンセルするには、インポート ジョブの作成者であるか、 `SUPER`権限を持っている必要があります。

## あらすじ {#synopsis}

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## 例 {#example}

ID が`1`のインポート ジョブをキャンセルするには、次のステートメントを実行します。

```sql
CANCEL IMPORT JOB 1;
```

出力は次のとおりです。

    Query OK, 0 rows affected (0.01 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
-   [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)
