---
title: JSON_TYPEOF
summary: 返回 JSON 结构最外层的类型。
---

# JSON_TYPEOF

返回 JSON 结构最外层的类型。

## 语法 {#syntax}

```sql
JSON_TYPEOF(<json_string>)
```

## 返回类型 {#return-type}

json_typeof 函数（或类似函数）的返回类型是一个字符串，用于指示已解析 JSON 值的数据类型。可能的返回值包括：`'null'`、`'boolean'`、`'string'`、`'number'`、`'array'` 和 `'object'`。

## 示例 {#examples}

```sql
-- 解析一个值为 NULL 的 JSON 值
SELECT JSON_TYPEOF(PARSE_JSON(NULL));

--
json_typeof(parse_json(null))|
-----------------------------+
                             |

-- 解析一个值为字符串 'null' 的 JSON 值
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