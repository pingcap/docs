---
title: READ_FILE
summary: Reads the content of a file from a stage and returns it as a BINARY value. This is useful for loading raw file content (images, PDFs, binary data, etc.) directly into a table column.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.882"/>

Reads the content of a file from a stage and returns it as a `BINARY` value. This is useful for loading raw file content (images, PDFs, binary data, etc.) directly into a table column.

## Syntax

```sql
-- Single argument: combined stage and file path
READ_FILE('<stage_path>')

-- Two arguments: separate stage and relative file path
READ_FILE('<stage>', '<file_path>')
```

## Parameters

| Parameter     | Description                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------------- |
| `stage_path`  | A combined stage and file path starting with `@`, e.g., `'@my_stage/path/to/file.png'`.                      |
| `stage`       | The stage name starting with `@`, e.g., `'@my_stage'`. The stage is validated at bind time when it is a constant. |
| `file_path`   | The relative file path within the stage, e.g., `'path/to/file.png'`.                                         |

## Return Type

`BINARY`. Returns `NULL` if any argument is `NULL`.

## Examples

### Reading a single file

```sql
-- Read a file using a combined stage path
SELECT to_hex(read_file('@my_stage/data/file.csv'));

-- Read a file using separate stage and path arguments
SELECT to_hex(read_file('@my_stage', 'data/file.csv'));
```

### Reading files from a table column

```sql
-- Create a table with file paths
CREATE TABLE file_paths(path STRING);
INSERT INTO file_paths VALUES
    ('@my_stage/images/01.png'),
    ('@my_stage/images/02.png'),
    (NULL);

-- Read all files referenced in the table
SELECT path, to_hex(read_file(path)) AS content_hex FROM file_paths;

┌──────────────────────────────────────────────────┐
│           path           │       content_hex      │
├──────────────────────────┼────────────────────────┤
│ @my_stage/images/01.png  │ 89504e47...            │
│ @my_stage/images/02.png  │ 89504e47...            │
│ NULL                     │ NULL                   │
└──────────────────────────────────────────────────┘
```

### Using two-argument form with relative paths

```sql
-- Create a table with relative file paths
CREATE TABLE rel_paths(path STRING);
INSERT INTO rel_paths VALUES
    ('data/file1.csv'),
    ('data/file2.csv');

-- Read files using a fixed stage and relative paths from the table
SELECT path, to_hex(read_file('@my_stage', path)) AS content_hex FROM rel_paths;
```
