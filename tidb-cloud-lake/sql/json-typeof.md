---
title: JSON_TYPEOF
summary: JSON 構造の最上位レベルの型を返します。
---

# JSON_TYPEOF

JSON 構造の最上位レベルの型を返します。

## 構文 {#syntax}

```sql
JSON_TYPEOF(<json_string>)
```

## 戻り値の型 {#return-type}

json_typeof 関数（または同様の関数）の戻り値の型は、解析された JSON 値のデータ型を示す文字列です。返される可能性のある値は、`'null'`、`'boolean'`、`'string'`、`'number'`、`'array'`、`'object'` です。

## 例 {#examples}

```sql
-- NULL の JSON 値を解析する
SELECT JSON_TYPEOF(PARSE_JSON(NULL));

--
json_typeof(parse_json(null))|
-----------------------------+
                             |

-- 文字列 'null' である JSON 値を解析する
SELECT JSON_TYPEOF(PARSE_JSON('null'));

--
json_typeof(parse_json('null'))|
-------------------------------+
null                           |

SELECT JSON_TYPEOF(PARSE_JSON('true'));

--
json_typeof(parse_json('true'))|
-------------------------------+
boolean                        |

SELECT JSON_TYPEOF(PARSE_JSON('"Datalake"'));

--
json_typeof(parse_json('"datalake"'))|
-------------------------------------+
string                               |

SELECT JSON_TYPEOF(PARSE_JSON('-1.23'));

--
json_typeof(parse_json('-1.23'))|
--------------------------------+
number                          |

SELECT JSON_TYPEOF(PARSE_JSON('[1,2,3]'));

--
json_typeof(parse_json('[1,2,3]'))|
----------------------------------+
array                             |

SELECT JSON_TYPEOF(PARSE_JSON('{"name": "Alice", "age": 30}'));

--
json_typeof(parse_json('{"name": "alice", "age": 30}'))|
-------------------------------------------------------+
object                                                 |
```