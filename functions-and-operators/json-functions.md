---
title: JSON Functions
summary: 了解 JSON 函数。
---

# JSON 函数

你可以使用 JSON 函数来操作 [JSON 数据类型](/data-type-json.md) 中的数据。

## 创建 JSON 值的函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_ARRAY()](/functions-and-operators/json-functions/json-functions-create.md#json_array) | 评估一组（可能为空）值，并返回包含这些值的 JSON 数组 |
| [JSON_OBJECT()](/functions-and-operators/json-functions/json-functions-create.md#json_object) | 评估一组（可能为空）键值对，并返回包含这些键值对的 JSON 对象 |
| [JSON_QUOTE()](/functions-and-operators/json-functions/json-functions-create.md#json_quote) | 将字符串作为带引号的 JSON 值返回 |

## 搜索 JSON 值的函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_CONTAINS()](/functions-and-operators/json-functions/json-functions-search.md#json_contains) | 通过返回 1 或 0 表示给定候选 JSON 文档是否包含在目标 JSON 文档中 |
| [JSON_CONTAINS_PATH()](/functions-and-operators/json-functions/json-functions-search.md#json_contains_path) | 返回 0 或 1，指示 JSON 文档是否在给定路径或路径集合中包含数据 |
| [JSON_EXTRACT()](/functions-and-operators/json-functions/json-functions-search.md#json_extract) | 从 JSON 文档中返回数据，数据由 `path` 参数匹配的部分选取 |
| [->](/functions-and-operators/json-functions/json-functions-search.md#-) | 在评估路径后，从 JSON 列中返回对应的值；是 `JSON_EXTRACT(doc, path_literal)` 的别名 |
| [->>](/functions-and-operators/json-functions/json-functions-search.md#--1) | 在评估路径后，从 JSON 列中返回值并取消引号；是 `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` 的别名 |
| [JSON_KEYS()](/functions-and-operators/json-functions/json-functions-search.md#json_keys) | 返回 JSON 对象顶层值的键，作为 JSON 数组；如果提供路径参数，则返回所选路径的顶层键 |
| [JSON_SEARCH()](/functions-and-operators/json-functions/json-functions-search.md#json_search) | 在 JSON 文档中搜索字符串的一个或所有匹配项 |
| [MEMBER OF()](/functions-and-operators/json-functions/json-functions-search.md#member-of) | 如果传入的值是 JSON 数组的元素，则返回 1，否则返回 0 |
| [JSON_OVERLAPS()](/functions-and-operators/json-functions/json-functions-search.md#json_overlaps) | 指示两个 JSON 文档是否有重叠部分；如果有，返回 1，否则返回 0 |

## 修改 JSON 值的函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_append) | `JSON_ARRAY_APPEND()` 的别名 |
| [JSON_ARRAY_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_append) | 在 JSON 文档中指定数组的末尾追加值，并返回结果 |
| [JSON_ARRAY_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_insert) | 在 JSON 文档的指定位置插入值，并返回结果 |
| [JSON_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_insert) | 在 JSON 文档中插入数据并返回结果 |
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch) | 合并两个或多个 JSON 文档，不保留重复键的值 |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve) | 通过保留所有值合并两个或多个 JSON 文档 |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge) | `JSON_MERGE_PRESERVE()` 的已废弃别名 |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove) | 从 JSON 文档中删除数据并返回结果 |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace) | 替换 JSON 文档中的已有值并返回结果 |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set) | 在 JSON 文档中插入或更新数据并返回结果 |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote) | 取消 JSON 值的引号并返回结果作为字符串 |

## 返回 JSON 值属性的函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_DEPTH()](/functions-and-operators/json-functions/json-functions-return.md#json_depth) | 返回 JSON 文档的最大深度 |
| [JSON_LENGTH()](/functions-and-operators/json-functions/json-functions-return.md#json_length) | 返回 JSON 文档的长度，或如果提供路径参数，则返回路径内值的长度 |
| [JSON_TYPE()](/functions-and-operators/json-functions/json-functions-return.md#json_type) | 返回指示 JSON 值类型的字符串 |
| [JSON_VALID()](/functions-and-operators/json-functions/json-functions-return.md#json_valid) | 检查 json\_doc 是否为有效的 JSON |

## 工具函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_PRETTY()](/functions-and-operators/json-functions/json-functions-utility.md#json_pretty) | 美化格式化 JSON 文档 |
| [JSON_STORAGE_FREE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_free) | 返回在就地更新后，二进制表示的 JSON 值释放的存储空间大小 |
| [JSON_STORAGE_SIZE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_size) | 返回存储 JSON 值所需的近似字节数。由于此值未考虑 TiKV 使用压缩，输出结果与 MySQL 不完全兼容 |

## 聚合函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_ARRAYAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg) | 提供键的聚合 |
| [JSON_OBJECTAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg) | 提供给定键的值的聚合 |

## 校验函数

| 函数名 | 描述 |
| --------- | ----------- |
| [JSON_SCHEMA_VALID()](/functions-and-operators/json-functions/json-functions-validate.md#json_schema_valid) | 根据模式验证 JSON 文档，以确保数据的完整性和一致性 |

## JSONPath

许多 JSON 函数使用 [JSONPath](https://www.rfc-editor.org/rfc/rfc9535.html) 来选择 JSON 文档的部分内容。

| 符号 | 描述 |
| ------ | ----------- |
| `$` | 文档根节点 |
| `.` | 成员选择 |
| `[]` | 数组选择 |
| `*` | 通配符 |
| `**` | 路径通配符 |
| `[<n> to <n>]` | 数组范围选择 |

以下内容以示例 JSON 文档为例，演示如何使用 JSONPath：

```json
{
    "database": {
        "name": "TiDB",
        "features": [
            "distributed",
            "scalable",
            "relational",
            "cloud native"
        ],
        "license": "Apache-2.0 license",
        "versions": [
            {
                "version": "v8.1.0",
                "type": "lts",
                "release_date": "2024-05-24" 
            },
            {
                "version": "v8.0.0",        
                "type": "dmr",
                "release_date": "2024-03-29"
            }
        ]
    },
    "migration_tool": {
        "name": "TiDB Data Migration",
        "features": [
            "MySQL compatible",            
            "Shard merging"
        ],
        "license": "Apache-2.0 license"
    }
}
```

| JSONPath | 描述 | 以 [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 举例 |
| -------- | -------- | -------- |
| `$` | 文档的根节点 | 返回完整文档 |
| `$.database` | `database` 对象 | 返回以 `"database"` 开头的完整结构，不包括 `"migration_tool"` 和其下的结构 |
| `$.database.name` | 数据库的名称 | `"TiDB"` |
| `$.database.features` | 所有数据库特性 | `["distributed", "scalable", "relational", "cloud native"]` |
| `$.database.features[0]` | 第一个数据库特性 | `"distributed"` |
| `$.database.features[2]` | 第三个数据库特性 | `"relational"` |
| `$.database.versions[0].type` | 第一个版本的类型 | `"lts"` |
| `$.database.versions[*].release_date` | 所有版本的发布日期 | `["2024-05-24","2024-03-29"]` |
| `$.*.features` | 两个数组的特性 | `[["distributed", "scalable", "relational", "cloud native"], ["MySQL compatible", "Shard merging"]]` |
| `$**.version` | 所有版本，路径通配符 | `["v8.1.0","v8.0.0"]` |
| `$.database.features[0 to 2]` | 从第一个到第三个的特性范围 | `["scalable","relational"]` |

更多信息请参见 [the IETF draft for JSONPath](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html)。

## 相关链接

* [JSON Data Type](/data-type-json.md)

## 不支持的函数

- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

更多信息请参见 [#14486](https://github.com/pingcap/tidb/issues/14486)。

## MySQL 兼容性

- TiDB 支持大部分 MySQL 8.0 中的 [JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)。