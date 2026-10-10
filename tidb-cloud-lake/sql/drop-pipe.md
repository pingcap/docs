---
title: DROP PIPE
summary: "{{{ .lake }}} で DROP PIPE コマンドを使用して取り込みパイプラインを削除する方法を学びます。"
---

# DROP PIPE

pipe を削除します。

## 構文 {#syntax}

```sql
DROP PIPE [ IF EXISTS ] <name>
```

## 例 {#example}

```sql
DROP PIPE IF EXISTS my_pipe;
```