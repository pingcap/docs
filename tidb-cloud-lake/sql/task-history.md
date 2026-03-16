---
title: TASK_HISTORY
---

Displays task running history given variables.

## Syntax
```sql
TASK_HISTORY(
      [ SCHEDULED_TIME_RANGE_START => <constant_expr> ]
      [, SCHEDULED_TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ]
      [, TASK_NAME => '<string>' ]
      [, ERROR_ONLY => { TRUE | FALSE } ]
      [, ROOT_TASK_ID => '<string>'] )
```



## Arguments

All the arguments are optional.

`SCHEDULED_TIME_RANGE_START => <constant_expr>`, `SCHEDULED_TIME_RANGE_END => <constant_expr>`

Time range (in TIMESTAMP_LTZ format), within the last 7 days, in which the task execution was scheduled. If the time range does not fall within the last 7 days, an error is returned.

* If `SCHEDULED_TIME_RANGE_END` is not specified, the function returns those tasks that have already completed, are currently running, or are scheduled in the future.
* If `SCHEDULED_TIME_RANGE_END` is CURRENT_TIMESTAMP, the function returns those tasks that have already completed or are currently running. Note that a task that is executed immediately before the current time might still be identified as scheduled.
* To query only those tasks that have already completed or are currently running, include `WHERE query_id IS NOT NULL` as a filter. The QUERY_ID column in the TASK_HISTORY output is populated only when a task has started running.

If no start or end time is specified, the most recent tasks are returned, up to the specified RESULT_LIMIT value.

`RESULT_LIMIT => <integer>`

A number specifying the maximum number of rows returned by the function.

If the number of matching rows is greater than this limit, the task executions with the most recent timestamp are returned, up to the specified limit.

Range: `1` to `10000`

Default: `100`.

`TASK_NAME => <string>`

A case-insensitive string specifying a task. Only non-qualified task names are supported. Only executions of the specified task are returned. Note that if multiple tasks have the same name, the function returns the history for each of these tasks.

`ERROR_ONLY => { TRUE | FALSE }`

When set to TRUE, this function returns only task runs that failed or were cancelled.

`ROOT_TASK_ID => <string>`

Unique identifier for the root task in a task graph. This ID matches the ID column value in the SHOW TASKS output for the same task. Specify the ROOT_TASK_ID to show the history of the root task and any child tasks that are part of the task graph.

## Usage Notes
* This function returns a maximum of 10,000 rows, set in the RESULT_LIMIT argument value. The default value is 100.
* This function returns results only for the ACCOUNTADMIN role.


## Examples

```sql
SELECT
  *
FROM TASK_HISTORY() order by scheduled_time;
```
The above SQL query retrieves all task history records from the TASK_HISTORY function, ordered by the scheduled_time column.(maximum 10,000)



```sql
SELECT *
  FROM TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START=>TO_TIMESTAMP('2022-01-02T01:12:00-07:00'),
    SCHEDULED_TIME_RANGE_END=>TO_TIMESTAMP('2022-01-02T01:12:30-07:00'))
```

The above SQL query retrieves all task history records from the TASK_HISTORY function where the scheduled time range starts at '2022-01-02T01:12:00-07:00' and ends at '2022-01-02T01:12:30-07:00'. This means it will return the tasks that were scheduled to run within this specific 30-second time window. The result will include details of the tasks that match this criteria.


