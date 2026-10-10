---
title: ALTER TASK
summary: ALTER TASK ステートメントは、既存のタスクを変更するために使用されます。
---

# ALTER TASK

ALTER TASK ステートメントは、既存のタスクを変更するために使用されます。

**NOTICE:** この機能は、{{{ .lake }}} でのみそのまま利用できます。

## 構文 {#syntax}

```sql
--- suspend or resume a task
ALTER TASK [ IF EXISTS ] <name> RESUME | SUSPEND

--- change task settings
ALTER TASK [ IF EXISTS ] <name> SET
  [ WAREHOUSE = <string> ]
  [ SCHEDULE = { <number> MINUTE | <number> SECOND | USING CRON <expr> <time_zone> } ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num ]
  [ ERROR_INTEGRATION = <string> ]
   [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
  [ COMMENT = <string> ]

--- change task SQL
ALTER TASK [ IF EXISTS ] <name> MODIFY AS <sql>

--- modify DAG when condition and after condition
ALTER TASK [ IF EXISTS ] <name> REMOVE AFTER <string> | ADD AFTER <string>
--- allow to change condition for task execution
ALTER TASK [ IF EXISTS ] <name> MODIFY WHEN <boolean_expr>
```

| パラメーター                        | 説明                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | 任意。指定した場合、同じ名前のタスクがすでに存在するときにのみ、そのタスクが変更されます。 |
| name                             | タスクの名前です。これは必須フィールドです。                                                       |
| RESUME \| SUSPEND                | タスクを再開または一時停止します。                                                                          |
| SET                              | タスク設定を変更します。各パラメーターの詳細な説明は [Create Task](/tidb-cloud-lake/sql/create-task.md) を参照してください。                                                                               |
| MODIFY AS                        | タスク SQL を変更します。                                                                                     |
| REMOVE AFTER | タスク DAG から先行タスクを削除します。先行タスクが残っていない場合、そのタスクは単独タスクまたはルートタスクになります。 |
| ADD AFTER | タスク DAG に先行タスクを追加します。 |
| MODIFY WHEN | タスク実行の条件を変更します。 |

## 例 {#examples}

```sql
ALTER TASK IF EXISTS mytask SUSPEND;
```

このコマンドは、`mytask` という名前のタスクが存在する場合に、そのタスクを一時停止します。

```sql
ALTER TASK IF EXISTS mytask SET
  WAREHOUSE = 'new_warehouse'
  SCHEDULE = USING CRON '0 12 * * * *' 'UTC';
```

この例では、`mytask` タスクを変更し、その Warehouse を `new_warehouse` に変更し、スケジュールを UTC の正午に毎日実行されるよう更新しています。

```sql
ALTER TASK IF EXISTS mytask MODIFY
AS
INSERT INTO new_table SELECT * FROM source_table;
```

ここでは、`mytask` によって実行される SQL ステートメントを、`source_table` から `new_table` にデータを挿入するものへ変更しています。

```sql
ALTER TASK mytaskchild MODIFY WHEN STREAM_STATUS('stream3') = False;
```

この例では、`mytaskchild` タスクを変更して、その WHEN 条件を変更しています。このタスクは、`'stream3'` に対する `STREAM_STATUS` 関数の評価結果が `False` の場合にのみ実行されます。これは、`'stream3'` に変更データが含まれていないときにタスクが実行されることを意味します。

```sql
ALTER TASK MyTask1 ADD AFTER 'task2';
```

この例では、`MyTask1` タスクに依存関係を追加しています。これにより、このタスクは `'task2'` と `'task3'` の両方が正常に完了した後に実行されるようになります。これは、タスクの有向非巡回グラフ（DAG）内に依存関係を作成します。

```sql
ALTER TASK MyTask1 REMOVE AFTER 'task2';
```

ここでは、`MyTask1` タスクの特定の依存関係を削除しています。このタスクは今後 `'task2'` の後には実行されません。これは、タスク DAG 内の依存関係を変更したい場合に役立ちます。