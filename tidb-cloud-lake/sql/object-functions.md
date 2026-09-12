---
title: 对象函数
summary: 本节提供 {{{ .lake }}} 中对象函数的参考信息。对象函数支持从 JSON 对象数据结构中创建、操作和提取信息。
---

# 对象函数

本节提供 {{{ .lake }}} 中对象函数的参考信息。对象函数支持从 JSON 对象数据结构中创建、操作和提取信息。

## 对象构造 {#object-construction}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md) | 从键值对创建 JSON 对象 | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` → `{"name":"John","age":30}` |
| [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md) | 创建 JSON 对象并保留空值 | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', null)` → `{"a":1,"b":null}` |

## 对象信息 {#object-information}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [OBJECT_KEYS](/tidb-cloud-lake/sql/object-keys.md) | 以数组形式返回 JSON 对象中的所有键 | `OBJECT_KEYS({"name":"John","age":30})` → `["name","age"]` |

## 对象修改 {#object-modification}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [OBJECT_INSERT](/tidb-cloud-lake/sql/object-insert.md) | 在 JSON 对象中插入或修改键值对 | `OBJECT_INSERT({"name":"John"}, "age", 30)` → `{"name":"John","age":30}` |
| [OBJECT_DELETE](/tidb-cloud-lake/sql/object-delete.md) | 从 JSON 对象中移除键值对 | `OBJECT_DELETE({"name":"John","age":30}, "age")` → `{"name":"John"}` |

## 对象选择 {#object-selection}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [OBJECT_PICK](/tidb-cloud-lake/sql/object-pick.md) | 创建仅包含指定键的新对象 | `OBJECT_PICK({"a":1,"b":2,"c":3}, ["a","c"])` → `{"a":1,"c":3}` |