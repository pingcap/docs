---
title: SHOW IMPORT JOB
summary: An overview of the usage of SHOW IMPORT JOB in TiDB.
---

# SHOW IMPORT JOB

The `SHOW IMPORT JOB` statement is used to show `IMPORT` jobs created in TiDB.

It supports the following two forms:

- `SHOW IMPORT JOBS`
- `SHOW IMPORT JOB <job-id>`

## Required privileges

- `SHOW IMPORT JOBS`: by default, this statement only shows jobs created by the current user. To view all import jobs, you need the `SUPER` privilege.
- `SHOW IMPORT JOB <job-id>`: only the creator of an import job or users with the `SUPER` privilege can use this statement to view a specific job.

## Synopsis

```ebnf+diagram
ShowImportJobsStmt ::=
    'SHOW' 'IMPORT' 'JOBS' ShowLikeOrWhereOpt?

ShowImportJobStmt ::=
    'SHOW' 'IMPORT' 'JOB' JobID

ShowLikeOrWhereOpt ::=
    'LIKE' SimpleExpr
|   'WHERE' Expression
```

The output fields of the `SHOW IMPORT JOB` statement are described as follows:

| Column           | Description             |
|------------------|-------------------------|
| Job_ID           | The ID of the job                  |
| Group_Key        | The group key of the job                  |
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
| Last_Update_Time       | The time when the job was last updated         |
| Cur_Step       | The specific sequential processing step of this job         |
| Cur_Step_Processed_Size       | The amount of data that has been processed within the current step         |
| Cur_Step_Total_Size       | The total size of the data to be processed in the current step         |
| Cur_Step_Progress_Pct       | The estimated completion percentage of the current step        |
| Cur_Step_Speed       | The current data processing speed         |
| Cur_Step_ETA       | The estimated time remaining for the current step to complete       |

## Filter import jobs

Only `SHOW IMPORT JOBS` supports filtering import jobs with a `WHERE` or `LIKE` clause. `SHOW IMPORT JOB <job-id>` does not support these clauses.

The `WHERE` clause can reference the output fields of `SHOW IMPORT JOBS`, including `Job_ID`, `Group_Key`, `Data_Source`, `Target_Table`, `Table_ID`, `Phase`, `Status`, `Source_File_Size`, `Imported_Rows`, `Result_Message`, `Create_Time`, `Start_Time`, `End_Time`, `Created_By`, `Last_Update_Time`, `Cur_Step`, `Cur_Step_Processed_Size`, `Cur_Step_Total_Size`, `Cur_Step_Progress_Pct`, `Cur_Step_Speed`, and `Cur_Step_ETA`.

The `LIKE` clause matches its pattern only against the first column `Job_ID` (compared as a string). For example, `SHOW IMPORT JOBS LIKE '%1'` returns the jobs whose `Job_ID` ends with `1`.

## Example

Show all import jobs that the current user can view:

```sql
SHOW IMPORT JOBS;
```

Show a specific import job by job ID:

```sql
SHOW IMPORT JOB 2;
```

The output is as follows:

| Job_ID | Group_Key | Data_Source | Target_Table | Table_ID | Phase | Status | Source_File_Size | Imported_Rows | Result_Message | Create_Time | Start_Time | End_Time | Created_By | Last_Update_Time | Cur_Step | Cur_Step_Processed_Size | Cur_Step_Total_Size | Cur_Step_Progress_Pct | Cur_Step_Speed | Cur_Step_ETA |
|--------|-----------|-------------|--------------|----------|-------|--------|------------------|---------------|----------------|-------------|------------|----------|------------|------------------|----------|-------------------------|---------------------|-----------------------|----------------|--------------|
| 2 | import_group_1 | /path/to/file.csv | `test`.`bar` | 118 | global-sorting | running | 277.5GiB | 0 |  | 2025-07-09 10:40:18.580706 | 2025-07-09 10:40:19.092528 | NULL | root@% | 2025-07-09 10:47:15 | encode | 4.55GB | 298GB | 1 | 10.96MB/s | 07:26:03 |

Filter import jobs by output fields:

```sql
SHOW IMPORT JOBS WHERE Group_Key = 'user_group';
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`SHOW IMPORT GROUP`](/sql-statements/sql-statement-show-import-group.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
