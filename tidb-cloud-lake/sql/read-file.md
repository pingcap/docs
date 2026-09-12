---
title: READ_FILE
summary: 从 stage 读取文件并返回其原始字节。
---

# READ_FILE

从 stage 读取文件，并将其内容作为原始字节返回。

当你希望将已暂存的资源（如文档、镜像或模型输入）打包到下游数据集中时，`READ_FILE` 非常有用，例如将训练数据卸载到 Lance 时。

## 语法 {#syntax}

```sql
READ_FILE('@<stage>/<path-to-file>')
READ_FILE('@<stage>', '<path-to-file>')
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `@<stage>/<path-to-file>` | 完整的 stage 文件路径。该表达式必须解析为以 `@` 开头的 stage 文件路径。 |
| `@<stage>` | 双参数形式中的 stage 名称。使用常量 stage 引用，例如 `@assets`。 |
| `<path-to-file>` | 相对于 stage 的文件路径。可以是字符串字面量、列，或解析为字符串的表达式。 |

## 返回类型 {#return-type}

`BINARY`

如果任一参数为 `NULL`，结果为 `NULL`。

## 使用说明 {#usage-notes}

- `READ_FILE` 从 stage 读取文件。它不会读取 {{{ .lake }}} server 上的本地文件。
- 目标必须是文件，而不是目录。
- 调用方必须具有读取该 stage 的权限。

## 示例 {#examples}

使用完整的 stage 路径读取文件：

```sql
SELECT TO_HEX(READ_FILE('@data/csv/prefix/ab.csv'));
```

结果：

```text
31
```

使用 stage 名称加相对路径读取文件：

```sql
SELECT TO_HEX(READ_FILE('@data', 'csv/prefix/ab.csv'));
```

结果：

```text
31
```

通过将常量 stage 与每行的相对路径组合来读取多个文件：

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

结果：

```text
+----------------------+--------------------------------+
| path                 | to_hex(read_file('@data',path)) |
+----------------------+--------------------------------+
| csv/prefix/ab.csv    | 31                             |
| csv/prefix/ab/cd.csv | 32                             |
| NULL                 | NULL                           |
+----------------------+--------------------------------+
```