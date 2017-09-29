---
title: JSON Functions
category: user guide
---

# JSON Functions

| Function Name and Syntactic Sugar | Example  | Description  |
| ---------- | -------- | ------------------ |
| [JSON_EXTRACT][json_extract] | JSON_EXTRACT(doc, path)  | Return a subdocument that the path corresponds to from the JSON document  |
| [JSON_UNQUOTE][json_unquote] | JSON_UNQUOTE(doc)  |  Remove the quotation marks outside the JSON document |
| [JSON_TYPE][json_type]   | JSON_TYPE(doc)   | Check the type of the content in the JSON document |
| [JSON_SET][json_set]    | JSON_SET(doc, path, value)   | Set up a subdocument for a path in the JSON document  |
| [JSON_INSERT][json_insert]   | JSON_INSERT(doc, path, value)  | Insert a subdocument into a path in the JSON document |
| [JSON_REPLACE][json_replace] | JSON_REPLACE(doc, path, value) |  Replace the subdocument under a path in the JSON document |
| [JSON_REMOVE][json_remove]   | JSON_REMOVE(doc, path)      |  Remove the subdocument under a path in the JSON document |
| [JSON_MERGE][json_merge]     | JSON_MERGE(doc1, doc2, doc3)   |  Merge multiple JSON documents into a single array type document |
| [JSON_OBJECT][json_object]   | JSON_OBJECT(k1, v1, k2, v2)    | Create a JSON document based on a series of K/V pairs  |
| [JSON_ARRAY][json_array]     | JSON_ARRAY(doc1, doc2, doc3)   | Create a JSON document based on a series of elements    |
| -> | doc->'$.a[3]'  | The syntactic sugar of `JSON_EXTRACT(doc, '$.a[3]')`   |
| ->> | doc->>'$.a[3]'   | The syntactic sugar of `JSON_UNQUOTE(JSONJSON_EXTRACT(doc, '$.a[3]'))` |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
