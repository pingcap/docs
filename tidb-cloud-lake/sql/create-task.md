---
title: CREATE TASK
summary: CREATE TASK ステートメントは、指定した SQL ステートメントをスケジュールベースまたは DAG ベースのタスクグラフで実行する新しいタスクを定義するために使用されます。
---

# CREATE TASK

CREATE TASK ステートメントは、指定した SQL ステートメントをスケジュールベースまたは DAG ベースのタスクグラフで実行する新しいタスクを定義するために使用されます。

**NOTICE:** この機能は、{{{ .lake }}} でのみ追加設定なしですぐに利用できます。

## Syntax {#syntax}

```sql
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
 WAREHOUSE = <string>
 SCHEDULE = { <num> MINUTE | <num> SECOND | USING CRON <expr> <time_zone> }
 [ AFTER <string>
 [ WHEN <boolean_expr> ]
 [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
 [ ERROR_INTEGRATION = <string> ]
 [ COMMENT = '<string_literal>' ]
 [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
AS
{ <sql_statement>
| BEGIN
    <sql_statement>;
    [ <sql_statement>; ... ]
  END;
}
```

複数の SQL ステートメントは `BEGIN ... END;` ブロックで囲むことで、タスクがそれらをスクリプトとして順番に実行します。

| パラメータ | 説明 |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IF NOT EXISTS                                    | 任意。指定した場合、同じ名前のタスクがまだ存在しないときにのみタスクが作成されます。 |
| name                                             | タスク名です。これは必須フィールドです。 |
| WAREHOUSE                                        | 必須。タスクで使用する仮想 Warehouse を指定します。 |
| SCHEDULE                                         | 必須。タスクの実行スケジュールを定義します。分単位、またはタイムゾーン付きの CRON 式で指定できます。 |
| SUSPEND_TASK_AFTER_NUM_FAILURES                  | 任意。連続して失敗した回数がこの値に達すると、タスクは自動的に一時停止されます。 |
| AFTER                                            | このタスクの開始前に完了している必要があるタスクの一覧です。 |
| WHEN boolean_expr                                | タスクを実行するために true である必要がある条件です。 |
| [ERROR_INTEGRATION](/tidb-cloud-lake/sql/notification.md) | 任意。特定の [task error payload](/tidb-cloud-lake/sql/task-error-notification-payload.md) を適用したタスクエラー通知に使用する notification integration の名前です。 |
| COMMENT                                          | 任意。タスクのコメントまたは説明として使用される文字列リテラルです。 |
| session_parameter                                | 任意。タスク実行時に使用するセッションパラメータを指定します。セッションパラメータは、CREATE TASK ステートメント内で他のすべてのタスクパラメータの後に配置する必要があります。 |
| sql                                              | タスクが実行する SQL ステートメントです。単一のステートメント、または `BEGIN ... END;` で囲まれたスクリプトを指定できます。これは必須フィールドです。 |

### Usage Notes {#usage-notes}

- 単独タスク、またはタスク DAG のルートタスクにはスケジュールを定義する必要があります。そうしない場合、タスクは EXECUTE TASK を使用して手動実行したときにのみ実行されます。
- DAG 内の子タスクにはスケジュールを指定できません。
- タスク作成後、タスク定義で指定したパラメータに基づいて実行されるようにするには、ALTER TASK … RESUME を実行する必要があります。
- Condition では `<boolean_expression>` の一部のみがサポートされます。

    タスクの WHEN 句では、以下がサポートされます。

    - [STREAM_STATUS](/tidb-cloud-lake/sql/stream-status.md) は SQL 式内での評価に対応しています。この関数は、指定した stream に変更追跡データが含まれているかどうかを示します。この関数を使用すると、現在の実行を開始する前に、指定した stream に変更データが含まれているかどうかを評価できます。結果が FALSE の場合、タスクは実行されません。
    - AND、OR、NOT などのブール演算子。
    - 数値型、文字列型、ブール型の間のキャスト。
    - 等しい、等しくない、より大きい、より小さいなどの比較演算子。

> **Note:**
>
> Warning: タスクで STREAM_STATUS を使用する場合、stream を参照するときはデータベース名を含める必要があります（例: `STREAM_STATUS('mydb.stream_name')`）。

- 単一のテーブル stream から変更データを消費する複数のタスクは、それぞれ異なる差分を取得します。タスクが DML ステートメントを使用して stream 内の変更データを消費すると、stream のオフセットが進みます。その変更データは次のタスクでは消費できなくなります。現時点では、1 つの stream の変更データを消費するのは 1 つのタスクのみにすることを推奨します。同じテーブルに対して複数の stream を作成し、それぞれを異なるタスクで消費できます。
- タスクは各実行ごとにリトライされません。各実行は直列です。各スクリプト SQL は 1 つずつ実行され、並列実行は行われません。これにより、タスク実行の順序と依存関係が維持されます。
- 間隔ベースのタスクは、固定された間隔のタイミングに厳密に従います。つまり、現在のタスク実行時間が間隔単位を超えた場合、次のタスクは直ちに実行されます。そうでない場合、次のタスクは次の間隔単位がトリガーされるまで待機します。たとえば、1 秒間隔で定義されたタスクで、1 回の実行に 1.5 秒かかる場合、次のタスクは直ちに実行されます。1 回の実行に 0.5 秒しかかからない場合、次のタスクは次の 1 秒間隔の開始まで待機します。
- セッションパラメータはタスク作成時に指定できますが、後から ALTER TASK ステートメントを使用して変更することもできます。例:

  ```sql
  ALTER TASK simple_task SET
      enable_query_result_cache = 1,
      query_result_cache_min_execute_secs = 5;
  ```

### Important Notes on Cron Expressions {#important-notes-on-cron-expressions}

- `SCHEDULE` パラメータで使用する cron 式には、**ちょうど 6 つのフィールド**を含める必要があります。
- 各フィールドは次を表します。
  1. **Second** (0-59)
  2. **Minute** (0-59)
  3. **Hour** (0-23)
  4. **Day of the Month** (1-31)
  5. **Month** (1-12 or JAN-DEC)
  6. **Day of the Week** (0-6, where 0 is Sunday, or SUN-SAT)

#### Example Cron Expressions {#example-cron-expressions}

- **Pacific Time の毎日午前 9:00:00:**
    - `USING CRON '0 0 9 * * *' 'America/Los_Angeles'`

- **毎分:**
    - `USING CRON '0 * * * * *' 'UTC'`
    - これは毎分の開始時にタスクを実行します。

- **毎時 15 分:**
    - `USING CRON '0 15 * * * *' 'UTC'`
    - これは毎時 15 分にタスクを実行します。

- **毎週月曜日の 12:00:00 PM:**
    - `USING CRON '0 0 12 * * 1' 'UTC'`
    - これは毎週月曜日の正午にタスクを実行します。

- **毎月 1 日の午前 0 時:**
    - `USING CRON '0 0 0 1 * *' 'UTC'`
    - これは毎月 1 日の午前 0 時にタスクを実行します。

- **平日の毎日午前 8:30:00:**
    - `USING CRON '0 30 8 * * 1-5' 'UTC'`
    - これは平日（月曜日から金曜日）の毎日午前 8:30 にタスクを実行します。

## Usage Examples {#usage-examples}

### CRON Schedule {#cron-schedule}

```sql
CREATE TASK my_daily_task
 WAREHOUSE = 'compute_wh'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 COMMENT = 'Daily summary task'
AS
 INSERT INTO summary_table SELECT * FROM source_table;
```

この例では、`my_daily_task` という名前のタスクを作成しています。このタスクは **compute_wh** Warehouse を使用して、source_table から summary_table にデータを挿入する SQL ステートメントを実行します。タスクは **CRON 式** を使用して、**Pacific Time の毎日午前 9 時** に実行されるようスケジュールされています。

### Multiple Statements {#multiple-statements}

```sql
CREATE TASK IF NOT EXISTS nightly_refresh
 WAREHOUSE = 'etl'
 SCHEDULE = USING CRON '0 0 2 * * *' 'UTC'
AS
BEGIN
    DELETE FROM staging.events WHERE event_time < DATEADD(DAY, -1, CURRENT_TIMESTAMP());
    INSERT INTO mart.events SELECT * FROM staging.events;
END;
```

この例では、`nightly_refresh` という名前のタスクを作成し、複数のステートメントを含むスクリプトを実行します。スクリプトは `BEGIN ... END;` で囲まれているため、タスクが実行されるたびに DELETE が INSERT より先に実行されます。

### Dynamic SQL (EXECUTE IMMEDIATE) {#dynamic-sql-execute-immediate}

```sql
CREATE OR REPLACE TASK log_ingestion
  WAREHOUSE = 'default'
  SCHEDULE = 1 MINUTE
AS
EXECUTE IMMEDIATE $$
BEGIN
    LET path := CONCAT('@mylog/', DATE_FORMAT(CURRENT_DATE - INTERVAL 3 DAY, '%m/%d/'));

    LET sql := CONCAT(
        'COPY INTO logs.web_logs FROM ', path,
        ' PATTERN = ''.*[.]gz'' FILE_FORMAT = (type = NDJSON compression = AUTO) MAX_FILES = 10000'
    );

    EXECUTE IMMEDIATE :sql;
END;
$$;
```

この例では、毎分実行されるタスクを作成しています。このタスクは **3 日前** の stage パス（たとえば `@mylog/12/15/`）を動的に計算し、`COPY INTO` ステートメントを組み立てて、`EXECUTE IMMEDIATE` で実行します。

### Automatic Suspension {#automatic-suspension}

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'system'
 SCHEDULE = 2 MINUTE
 SUSPEND_TASK_AFTER_NUM_FAILURES = 3
AS
 INSERT INTO compaction_test.test VALUES((1));
```

この例では、`mytask` という名前のタスクを、まだ存在しない場合に作成します。このタスクは **system** Warehouse に割り当てられ、**2 分ごと** に実行されるようスケジュールされています。**3 回連続で失敗** すると、**自動的に一時停止** されます。このタスクは compaction_test.test テーブルに対して INSERT 操作を実行します。

### Second-Level Scheduling {#second-level-scheduling}

```sql
CREATE TASK IF NOT EXISTS daily_sales_summary
 WAREHOUSE = 'analytics'
 SCHEDULE = 30 SECOND
AS
 SELECT sales_date, SUM(amount) AS daily_total
 FROM sales_data
 GROUP BY sales_date;
```

この例では、`daily_sales_summary` という名前のタスクを **秒単位スケジューリング** で作成しています。このタスクは **30 SECOND ごと** に実行されるようスケジュールされています。タスクは **analytics** Warehouse を使用し、sales_data テーブルのデータを集計して日次売上サマリーを計算します。

### タスクの依存関係 {#task-dependencies}

```sql
CREATE TASK IF NOT EXISTS process_orders
 WAREHOUSE = 'etl'
 AFTER task1
AS
 INSERT INTO data_warehouse.orders SELECT * FROM staging.orders;
```

この例では、`process_orders` という名前のタスクを作成し、**task1** と **task2** が**正常に完了した後**に実行されるよう定義しています。これは、タスクの **Directed Acyclic Graph (DAG)** における**依存関係**を作成するのに役立ちます。このタスクは **etl** Warehouse を使用し、staging 領域からデータ Warehouse にデータを転送します。

> Tip: AFLTER パラメータを使用する場合、SCHEDULE パラメータを設定する必要はありません。

### 条件付き実行 {#conditional-execution}

```sql
CREATE TASK IF NOT EXISTS hourly_data_cleanup
 WAREHOUSE = 'maintenance'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 WHEN STREAM_STATUS('db1.change_stream') = TRUE
AS
 DELETE FROM archived_data
 WHERE archived_date < DATEADD(HOUR, -24, CURRENT_TIMESTAMP());

```

この例では、`hourly_data_cleanup` という名前のタスクを作成しています。このタスクは **maintenance** Warehouse を使用し、**1 時間ごと**に実行されるようスケジュールされています。このタスクは、`archived_data` テーブルから 24 時間より古いデータを削除します。また、`db1.change_stream` に変更データが含まれているかどうかを **STREAM_STATUS** 関数で確認し、**条件が満たされた場合のみ**実行されます。

### エラー統合 {#error-integration}

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'mywh'
 SCHEDULE = 30 SECOND
 ERROR_INTEGRATION = 'myerror'
AS
 BEGIN
    BEGIN;
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
    DELETE FROM mytable WHERE ts < DATEADD(MINUTE, -5, CURRENT_TIMESTAMP());
    COMMIT;
 END;
```

この例では、`mytask` という名前のタスクを作成しています。このタスクは **mywh** Warehouse を使用し、**30 秒ごと**に実行されるようスケジュールされています。このタスクは、INSERT 文と DELETE 文を含む **BEGIN ブロック**を実行します。両方の文の実行後に、タスクはトランザクションをコミットします。タスクが失敗すると、**myerror** という名前の **error integration** がトリガーされます。

### セッションパラメータ {#session-parameters}

```sql
CREATE TASK IF NOT EXISTS cache_enabled_task
 WAREHOUSE = 'analytics'
 SCHEDULE = 5 MINUTE
 COMMENT = 'Task with query result cache enabled'
 enable_query_result_cache = 1,
 query_result_cache_min_execute_secs = 5
AS
 SELECT SUM(amount) AS total_sales
 FROM sales_data
 WHERE transaction_date >= DATEADD(DAY, -7, CURRENT_DATE())
 GROUP BY product_category;
```

この例では、クエリ結果キャッシュを有効にする**セッションパラメータ**付きで、`cache_enabled_task` という名前のタスクを作成しています。このタスクは **5 分ごと**に実行されるようスケジュールされ、**analytics** Warehouse を使用します。セッションパラメータ **`enable_query_result_cache = 1`** と **`query_result_cache_min_execute_secs = 5`** は、**他のすべてのタスクパラメータの後に**指定されており、実行に少なくとも 5 秒かかるクエリに対してクエリ結果キャッシュを有効にします。これにより、基になるデータが変更されていない場合、同じタスクの後続実行で**パフォーマンスを向上**できます。

### タスク実行履歴を表示する {#view-task-run-history}

タスクがいつ、どのように実行されたかを確認するには、`TASK_HISTORY()` テーブル関数を使用します。

```sql
SELECT *
FROM TASK_HISTORY(
  TASK_NAME   => 'daily_sales_summary',
  RESULT_LIMIT => 20
)
ORDER BY scheduled_time DESC;
```

時間範囲や DAG 内のルートタスク ID によるフィルタリングを含むすべてのオプションについては、[TASK HISTORY](/tidb-cloud-lake/sql/table-functions.md) を参照してください。