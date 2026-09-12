---
title: 序列函数
summary: 本节提供 {{{ .lake }}} 中序列函数的参考信息。序列函数可用于操作序列对象，这些对象会生成唯一的、自增的数值。
---

# 序列函数

本节提供 {{{ .lake }}} 中序列函数的参考信息。序列函数可用于操作序列对象，这些对象会生成唯一的、自增的数值。

## 可用的序列函数 {#available-sequence-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [NEXTVAL](/tidb-cloud-lake/sql/nextval.md) | 获取序列中的下一个值 | `NEXTVAL(my_sequence)` |