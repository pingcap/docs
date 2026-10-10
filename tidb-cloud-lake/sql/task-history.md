---
title: TASK_HISTORY
summary: 指定した変数に基づいてタスクの実行履歴を表示します。
---

# TASK_HISTORY

指定した変数に基づいてタスクの実行履歴を表示します。

## Syntax {#syntax}

```sql
TASK_HISTORY(
      [ SCHEDULED_TIME_RANGE_START => <constant_expr> ]
      [, SCHEDULED_TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ]
      [, TASK_NAME => '<string>' ]
      [, ERROR_ONLY => { TRUE | FALSE } ]
      [, ROOT_TASK_ID => '<string>'] )
```

## Arguments {#arguments}

すべての引数は省略可能です。

`SCHEDULED_TIME_RANGE_START => <constant_expr>`, `SCHEDULED_TIME_RANGE_END => <constant_expr>`

タスク実行がスケジュールされた時間範囲を指定します（TIMESTAMP_LTZ 形式、過去 7 日以内）。時間範囲が過去 7 日以内に収まっていない場合は、エラーが返されます。

* `SCHEDULED_TIME_RANGE_END` を指定しない場合、この関数はすでに完了したタスク、現在実行中のタスク、または今後実行予定のタスクを返します。
* `SCHEDULED_TIME_RANGE_END` が CURRENT_TIMESTAMP の場合、この関数はすでに完了したタスクまたは現在実行中のタスクを返します。現在時刻の直前に実行されたタスクは、依然として scheduled と判定される可能性がある点に注意してください。
* すでに完了したタスクまたは現在実行中のタスクのみを照会するには、フィルターとして `WHERE query_id IS NOT NULL` を含めてください。TASK_HISTORY の出力にある QUERY_ID カラムは、タスクの実行が開始された場合にのみ値が設定されます。

開始時刻または終了時刻が指定されていない場合は、指定した RESULT_LIMIT の値まで、最新のタスクが返されます。

`RESULT_LIMIT => <integer>`

関数が返す最大行数を指定する数値です。

一致する行数がこの上限を超える場合は、最新のタイムスタンプを持つタスク実行が、指定した上限まで返されます。

範囲: `1` から `10000`

デフォルト: `100`

`TASK_NAME => <string>`

タスクを指定する大文字小文字を区別しない文字列です。修飾されていないタスク名のみサポートされます。指定したタスクの実行のみが返されます。複数のタスクが同じ名前を持つ場合、この関数はそれら各タスクの履歴を返す点に注意してください。

`ERROR_ONLY => { TRUE | FALSE }`

TRUE に設定すると、この関数は失敗したタスク実行またはキャンセルされたタスク実行のみを返します。

`ROOT_TASK_ID => <string>`

タスクグラフ内のルートタスクの一意識別子です。この ID は、同じタスクに対する SHOW TASKS の出力にある ID カラムの値と一致します。ROOT_TASK_ID を指定すると、ルートタスクおよびそのタスクグラフに含まれる子タスクの履歴を表示できます。

## Usage Notes {#usage-notes}

* この関数が返す最大行数は 10,000 行で、RESULT_LIMIT 引数の値で設定します。デフォルト値は 100 です。
* この関数は ACCOUNTADMIN ロールに対してのみ結果を返します。

## Examples {#examples}

```sql
SELECT
  *
FROM TASK_HISTORY() order by scheduled_time;
```

上記の SQL クエリは、TASK_HISTORY 関数からすべてのタスク履歴レコードを取得し、scheduled_time カラムで並べ替えます。（最大 10,000 件）

```sql
SELECT *
  FROM TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START=>TO_TIMESTAMP('2022-01-02T01:12:00-07:00'),
    SCHEDULED_TIME_RANGE_END=>TO_TIMESTAMP('2022-01-02T01:12:30-07:00'))
```

上記の SQL クエリは、TASK_HISTORY 関数から、scheduled time の範囲が '2022-01-02T01:12:00-07:00' に始まり、'2022-01-02T01:12:30-07:00' に終わるすべてのタスク履歴レコードを取得します。つまり、この特定の 30 秒間の時間枠内で実行するようスケジュールされたタスクを返します。結果には、この条件に一致するタスクの詳細が含まれます。