---
title: TASK_HISTORY
summary: 根据给定变量显示任务运行历史。
---

# TASK_HISTORY

根据给定变量显示任务运行历史。

## 语法 {#syntax}

```sql
TASK_HISTORY(
      [ SCHEDULED_TIME_RANGE_START => <constant_expr> ]
      [, SCHEDULED_TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ]
      [, TASK_NAME => '<string>' ]
      [, ERROR_ONLY => { TRUE | FALSE } ]
      [, ROOT_TASK_ID => '<string>'] )
```

## 参数 {#arguments}

所有参数都是可选的。

`SCHEDULED_TIME_RANGE_START => <constant_expr>`, `SCHEDULED_TIME_RANGE_END => <constant_expr>`

任务执行被调度的时间范围（TIMESTAMP_LTZ 格式），且必须在最近 7 天内。如果该时间范围不在最近 7 天内，则会返回错误。

* 如果未指定 `SCHEDULED_TIME_RANGE_END`，该函数会返回已经完成、当前正在运行或计划在未来运行的任务。
* 如果 `SCHEDULED_TIME_RANGE_END` 为 CURRENT_TIMESTAMP，该函数会返回已经完成或当前正在运行的任务。注意，在当前时间之前立即执行的任务仍可能被识别为已调度。
* 若仅查询已经完成或当前正在运行的任务，请添加 `WHERE query_id IS NOT NULL` 作为过滤条件。只有当任务开始运行后，TASK_HISTORY 输出中的 QUERY_ID 列才会被填充。

如果未指定开始时间或结束时间，则返回最近的任务，最多返回到指定的 RESULT_LIMIT 值。

`RESULT_LIMIT => <integer>`

用于指定该函数返回的最大行数。

如果匹配的行数大于该限制，则返回时间戳最新的任务执行记录，最多返回到指定限制。

范围：`1` 到 `10000`

默认值：`100`

`TASK_NAME => <string>`

一个不区分大小写的字符串，用于指定任务。仅支持非限定任务名。只返回指定任务的执行记录。注意，如果多个任务具有相同名称，该函数会返回这些任务各自的历史记录。

`ERROR_ONLY => { TRUE | FALSE }`

设置为 TRUE 时，该函数仅返回失败或已取消的任务运行记录。

`ROOT_TASK_ID => <string>`

任务图中根任务的唯一标识符。该 ID 与同一任务在 SHOW TASKS 输出中的 ID 列值一致。指定 `ROOT_TASK_ID` 可显示根任务以及属于该任务图的所有子任务的历史记录。

## 使用说明 {#usage-notes}

* 该函数最多返回 10,000 行，由 RESULT_LIMIT 参数值控制。默认值为 100。
* 该函数仅对 ACCOUNTADMIN 角色返回结果。

## 示例 {#examples}

```sql
SELECT
  *
FROM TASK_HISTORY() order by scheduled_time;
```

上述 SQL 查询从 TASK_HISTORY 函数中检索所有任务历史记录，并按 scheduled_time 列排序。（最多 10,000 条）

```sql
SELECT *
  FROM TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START=>TO_TIMESTAMP('2022-01-02T01:12:00-07:00'),
    SCHEDULED_TIME_RANGE_END=>TO_TIMESTAMP('2022-01-02T01:12:30-07:00'))
```

上述 SQL 查询从 TASK_HISTORY 函数中检索所有任务历史记录，其中调度时间范围从 `'2022-01-02T01:12:00-07:00'` 开始，到 `'2022-01-02T01:12:30-07:00'` 结束。这意味着它将返回在这个特定 30 秒时间窗口内被调度运行的任务。结果将包含符合该条件的任务详细信息。