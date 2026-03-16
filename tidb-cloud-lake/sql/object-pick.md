---
title: OBJECT_PICK
title_includes: JSON_OBJECT_PICK
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>


Creates a new JSON object containing only the specified keys from the input JSON object. If a specified key doesn't exist in the input object, it is omitted from the result.

## Aliases

- `JSON_OBJECT_PICK`

## Syntax

```sql
OBJECT_PICK(<json_object>, <key1> [, <key2>, ...])
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| json_object | A JSON object (VARIANT type) from which to pick keys. |
| key1, key2, ... | One or more string literals representing the keys to be included in the result object. |

## Return Type

Returns a VARIANT containing a new JSON object with only the specified keys and their corresponding values.

## Examples

Pick a single key:
```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"c":3}'::VARIANT, 'a');
-- Result: {"a":1}
```

Pick multiple keys:
```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'b');
-- Result: {"a":1,"b":2}
```

Pick with non-existent key (non-existent keys are ignored):
```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'c');
-- Result: {"a":1}
```
