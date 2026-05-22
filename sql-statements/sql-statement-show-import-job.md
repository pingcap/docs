---
title: SHOW IMPORT JOB
summary: An overview of the usage of SHOW IMPORT JOB in TiDB.
---

# SHOW IMPORT JOB

The `SHOW IMPORT JOB` statement is used to show the IMPORT jobs created in TiDB. This statement can only show jobs created by the current user.

## Required privileges

- `SHOW [RAW] IMPORT JOBS`: if a user has the `SUPER` privilege, this statement shows all import jobs in TiDB. Otherwise, this statement only shows jobs created by the current user.
- `SHOW [RAW] IMPORT JOB <job-id>`: only the creator of an import job or users with the `SUPER` privilege can use this statement to view a specific job.

## Synopsis

```ebnf+diagram
ShowImportJobsStmt ::=
    'SHOW' RawOpt? 'IMPORT' 'JOBS' ShowLikeOrWhereOpt?

ShowImportJobStmt ::=
    'SHOW' RawOpt? 'IMPORT' 'JOB' JobID

RawOpt ::=
    'RAW'

ShowLikeOrWhereOpt ::=
    'LIKE' SimpleExpr
|   'WHERE' Expression
```

The output fields of the `SHOW IMPORT JOB` statement are described as follows:

| Column           | Description             |
|------------------|-------------------------|
| Job_ID           | The ID of the task                  |
| Group_Key        | The group key of the task                  |
| Data_Source      | Information about the data source                  |
| Target_Table     | The name of the target table                     |
| Table_ID         | The ID of the target table                     |
| Phase            | The current phase of the job, including `importing`, `validating`, and `add-index` |
| Status           | The current status of the job, including `pending` (means created but not started yet), `running`, `canceled`, `failed`, and `finished` |
| Source_File_Size | The size of the source file  |
| Imported_Rows | The number of data rows that have been read and written to the target table  |
| Result_Message   | If the import fails, this field returns the error message. Otherwise, it is empty.|
| Create_Time      | The time when the task is created                 |
| Start_Time       | The time when the task is started                     |
| End_Time         | The time when the task is ended            |
| Created_By       | The name of the database user who creates the task         |
| Last_Update_Time       | The time when the task is last updated         |
| Cur_Step       | The specific sequential processing step of this job         |
| Cur_Step_Processed_Size       | The amount of data that has been processed within the current step         |
| Cur_Step_Total_Size       | The total size of the data to be processed in the current step         |
| Cur_Step_Progress_Pct       | The estimated completion percentage of the current step        |
| Cur_Step_Speed       | The current data processing speed         |
| Cur_Step_ETA       | The estimated time remaining for the current step to complete       |

## Filtering import jobs

Only `SHOW [RAW] IMPORT JOBS` supports filtering import jobs with a `WHERE` clause. `SHOW [RAW] IMPORT JOB <job-id>` does not support a `WHERE` clause.

The `WHERE` clause can reference the output fields of `SHOW IMPORT JOBS`, including `Job_ID`, `Group_Key`, `Data_Source`, `Target_Table`, `Table_ID`, `Phase`, `Status`, `Source_File_Size`, `Imported_Rows`, `Result_Message`, `Create_Time`, `Start_Time`, `End_Time`, `Created_By`, `Last_Update_Time`, `Cur_Step`, `Cur_Step_Processed_Size`, `Cur_Step_Total_Size`, `Cur_Step_Progress_Pct`, `Cur_Step_Speed`, and `Cur_Step_ETA`.

## Example

Show all import jobs that the current user can view:

```sql
SHOW IMPORT JOBS;
```

Show a specific import job by job ID:

```sql
SHOW IMPORT JOB 2;
```

Filter import jobs by output fields:

```sql
SHOW IMPORT JOBS WHERE Group_Key = 'user_group';
```

You can also add the `RAW` keyword before `IMPORT`:

```sql
SHOW RAW IMPORT JOBS;
```

```sql
SHOW RAW IMPORT JOBS WHERE Group_Key = 'user_group';
```

```sql
SHOW RAW IMPORT JOB 2;
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`SHOW IMPORT GROUP`](/sql-statements/sql-statement-show-import-group.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
