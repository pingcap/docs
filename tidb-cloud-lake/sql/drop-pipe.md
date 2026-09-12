---
title: DROP PIPE
summary: "了解如何使用 DROP PIPE 命令删除 {{{ .lake }}} 中的数据摄取管道。"
---

# DROP PIPE

删除一个管道。

## 语法 {#syntax}

```sql
DROP PIPE [ IF EXISTS ] <name>
```

## 示例 {#example}

```sql
DROP PIPE IF EXISTS my_pipe;
```