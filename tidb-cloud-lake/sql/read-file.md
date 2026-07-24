---
title: READ_FILE
summary: Reads a file from a stage and returns its raw bytes.
---

# READ_FILE

Reads a file from a stage and returns its contents as raw bytes.

`READ_FILE` is useful when you want to package staged assets such as documents, images, or model inputs into downstream datasets, for example when unloading training data to Lance.

## Syntax

```sql
READ_FILE('@<stage>/<path-to-file>')
READ_FILE('@<stage>', '<path-to-file>')
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `@<stage>/<path-to-file>` | Full stage file path. The expression must resolve to a stage file path that starts with `@`. |
| `@<stage>` | Stage name in the two-argument form. Use a constant stage reference such as `@assets`. |
| `<path-to-file>` | File path relative to the stage. This can be a string literal, column, or expression that resolves to a string. |

## Return Type

`BINARY`

If any argument is `NULL`, the result is `NULL`.

## Usage Notes

- `READ_FILE` reads files from a stage. It does not read local files from the {{{ .lake }}} server.
- The target must be a file, not a directory.
- The caller must have permission to read the stage.

## Examples

Read a file with the full stage path:

```sql
SELECT TO_HEX(READ_FILE('@data/csv/prefix/ab.csv'));
```

Result:

```text
31
```

Read a file with a stage name plus a relative path:

```sql
SELECT TO_HEX(READ_FILE('@data', 'csv/prefix/ab.csv'));
```

Result:

```text
31
```

Read multiple files by combining a constant stage with per-row relative paths:

```sql
CREATE OR REPLACE TABLE read_file_rel_paths(path STRING);

INSERT INTO read_file_rel_paths VALUES
  ('csv/prefix/ab.csv'),
  ('csv/prefix/ab/cd.csv'),
  (NULL);

SELECT path, TO_HEX(READ_FILE('@data', path))
FROM read_file_rel_paths
ORDER BY path;
```

Result:

```text
+----------------------+--------------------------------+
| path                 | to_hex(read_file('@data',path)) |
+----------------------+--------------------------------+
| csv/prefix/ab.csv    | 31                             |
| csv/prefix/ab/cd.csv | 32                             |
| NULL                 | NULL                           |
+----------------------+--------------------------------+
```
