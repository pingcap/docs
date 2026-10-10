---
title: Object Functions
summary: このセクションでは、{{{ .lake }}} のオブジェクト関数に関するリファレンス情報を提供します。オブジェクト関数を使用すると、JSON オブジェクトデータ構造の作成、操作、および情報の抽出が可能です。
---

# Object Functions

このセクションでは、{{{ .lake }}} のオブジェクト関数に関するリファレンス情報を提供します。オブジェクト関数を使用すると、JSON オブジェクトデータ構造の作成、操作、および情報の抽出が可能です。

## オブジェクトの構築 {#object-construction}

| Function | 説明 | 例 |
|----------|-------------|---------|
| [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md) | キーと値のペアから JSON オブジェクトを作成します | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` → `{"name":"John","age":30}` |
| [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md) | null 値を保持したまま JSON オブジェクトを作成します | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', null)` → `{"a":1,"b":null}` |

## オブジェクト情報 {#object-information}

| Function | 説明 | 例 |
|----------|-------------|---------|
| [OBJECT_KEYS](/tidb-cloud-lake/sql/object-keys.md) | JSON オブジェクトのすべてのキーを配列として返します | `OBJECT_KEYS({"name":"John","age":30})` → `["name","age"]` |

## オブジェクトの変更 {#object-modification}

| Function | 説明 | 例 |
|----------|-------------|---------|
| [OBJECT_INSERT](/tidb-cloud-lake/sql/object-insert.md) | JSON オブジェクトにキーと値のペアを挿入または更新します | `OBJECT_INSERT({"name":"John"}, "age", 30)` → `{"name":"John","age":30}` |
| [OBJECT_DELETE](/tidb-cloud-lake/sql/object-delete.md) | JSON オブジェクトからキーと値のペアを削除します | `OBJECT_DELETE({"name":"John","age":30}, "age")` → `{"name":"John"}` |

## オブジェクトの選択 {#object-selection}

| Function | 説明 | 例 |
|----------|-------------|---------|
| [OBJECT_PICK](/tidb-cloud-lake/sql/object-pick.md) | 指定したキーのみを含む新しいオブジェクトを作成します | `OBJECT_PICK({"a":1,"b":2,"c":3}, ["a","c"])` → `{"a":1,"c":3}` |