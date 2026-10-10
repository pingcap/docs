---
title: OBJECT_PICK
summary: 入力 JSON オブジェクトから指定したキーのみを含む新しい JSON オブジェクトを作成します。指定したキーが入力オブジェクトに存在しない場合、そのキーは結果から省略されます。
---

# OBJECT_PICK

入力 JSON オブジェクトから指定したキーのみを含む新しい JSON オブジェクトを作成します。指定したキーが入力オブジェクトに存在しない場合、そのキーは結果から省略されます。

## エイリアス {#aliases}

- `JSON_OBJECT_PICK`

## 構文 {#syntax}

```sql
OBJECT_PICK(<json_object>, <key1> [, <key2>, ...])
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| json_object | キーを抽出する対象の JSON オブジェクト（VARIANT 型）です。 |
| key1, key2, ... | 結果オブジェクトに含めるキーを表す 1 つ以上の文字列リテラルです。 |

## 戻り値の型 {#return-type}

指定したキーとそれに対応する値のみを含む新しい JSON オブジェクトを格納した VARIANT を返します。

## 例 {#examples}

単一のキーを抽出します。

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"c":3}'::VARIANT, 'a');
-- Result: {"a":1}
```

複数のキーを抽出します。

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'b');
-- Result: {"a":1,"b":2}
```

存在しないキーを指定して抽出します（存在しないキーは無視されます）。

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'c');
-- Result: {"a":1}
```