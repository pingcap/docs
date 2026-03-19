---
title: ARRAY_INTERSECTION
summary: Returns the common elements between two JSON arrays.
---

# ARRAY_INTERSECTION

> **Note:**
>
> Introduced or updated in v1.2.762.

Returns the common elements between two JSON arrays.

## Aliases

- `JSON_ARRAY_INTERSECTION`

## Syntax

```sql
ARRAY_INTERSECTION(<json_array1>, <json_array2>)
```

## Return Type

JSON array.

## Examples

```sql
-- Find the intersection of two JSON arrays
SELECT ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON);

-[ RECORD 1 ]-----------------------------------
array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT): ["Electronics","Books"]

-- Find the intersection of the result from the first query with a third JSON array using an iterative approach
SELECT ARRAY_INTERSECTION(
    ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON),
    '["Electronics", "Books", "Clothing"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_intersection(array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT), '["Electronics", "Books", "Clothing"]'::VARIANT): ["Electronics","Books"]
```
