---
title: Filtering
summary: Learn how to use filtering in your application.
---

# Filtering

As a relational database, TiDB supports a rich set of [SQL operators](https://docs.pingcap.com/tidbcloud/operators/) and flexible combinations of filtering conditions for precise queries.

## Overview

You can filter on both scalar fields and JSON fields. Filtering on JSON fields is often used for [metadata filtering](/ai/guides/vector-search.md#metadata-filtering) in vector search.

> **Note:**
>
> For a complete example of filtering, see [Filtering Example](/ai/examples/filtering-with-pytidb.md).

[`pytidb`](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently.

When using `pytidb`, you can apply filtering by passing the **filters** parameter to the `table.query()`, `table.delete()`, `table.update()`, and `table.search()` methods.

The **filters** parameter supports two formats: [Dictionary filters](#dictionary-filters) and [SQL string filters](#sql-string-filters).

## Dictionary filters

`pytidb` lets you define filter conditions using a Python dictionary with operators as the **filters** parameter.

The dictionary structure of **filters** is as follows:

```python
{
    "<key>": {
        "<operator>": <value>
    },
    ...
}
```

- `<key>`: The key can be a column name, a JSON path expression to access a JSON field (see [Metadata filtering](/ai/guides/vector-search.md#metadata-filtering)), or a [logical operator](#logical-operators).
- `<operator>`: The operator can be a [compare operator](#compare-operators) or an [inclusion operator](#inclusion-operators).
- `<value>`: The value can be a scalar value or an array, depending on the operator.

**Example: Filter records where `created_at` is greater than 2024-01-01**

```python
table.query({
    # The `created_at` is a scalar field with DATETIME type
    "created_at": {
        "$gt": "2024-01-01"
    }
})
```

**Example: Filter records where `meta.category` is in the array ["tech", "science"]**

```python
results = (
    table.search("some query", search_type="vector")
        .filter({
            # The `meta` is a JSON field, and its value is a JSON object like {"category": "tech"}
            "meta.category": {
                "$in": ["tech", "science"]
            }
        })
        .limit(10)
        .to_list()
)
```

### Compare operators

You can use the following comparison operators to filter records:

| Operator | Description                       |
|----------|-----------------------------------|
| `$eq`    | Equal to value                    |
| `$ne`    | Not equal to value                |
| `$gt`    | Greater than value                |
| `$gte`   | Greater than or equal to value    |
| `$lt`    | Less than value                   |
| `$lte`   | Less than or equal to value       |

**Example: Filter records where `user_id` equals 1**

```python
{
    "user_id": {
        "$eq": 1
    }
}
```

You can omit the `$eq` operator. The following filter is equivalent to the preceding one:

```python
{
    "user_id": 1
}
```

### Inclusion operators

You can use the following inclusion operators to filter records:

| Operator | Description                       |
|----------|-----------------------------------|
| `$in`    | In array (string, int, or float)  |
| `$nin`   | Not in array (string, int, float) |

**Example: Filter records where `category` is in the array ["tech", "science"]**

```python
{
    "category": {
        "$in": ["tech", "science"]
    }
}
```

### Logical operators

You can use the logical operators `$and` and `$or` to combine multiple filters.

| Operator | Description                                         |
|----------|-----------------------------------------------------|
| `$and`   | Returns results that match **all** filters in the list |
| `$or`    | Returns results that match **any** filter in the list |

**Syntax for `$and` or `$or`:**

```python
{
    "$and|$or": [
        {
            "field_name": {
                <operator>: <value>
            }
        },
        {
            "field_name": {
                <operator>: <value>
            }
        }
        ...
    ]
}
```

**Example: using `$and` to combine multiple filters:**

```python
{
    "$and": [
        {
            "created_at": {
                "$gt": "2024-01-01"
            }
        },
        {
            "meta.category": {
                "$in": ["tech", "science"]
            }
        }
    ]
}
```

## SQL String Filters

You can also use a SQL string as `filters`. The string must be a valid SQL `WHERE` clause (without the `WHERE` keyword) in the TiDB SQL syntax.

**Example: Filter records where `created_at` is greater than 2024-01-01**

```python
results = table.query(
    filters="created_at > '2024-01-01'",
    limit=10
).to_list()
```

**Example: Filter records where the JSON field `meta.category` equals 'tech'**

```python
results = table.query(
    filters="meta->>'$.category' = 'tech'",
    limit=10
).to_list()
```

You can combine multiple conditions using `AND`, `OR`, and parentheses, and use any TiDB-supported [SQL operators](https://docs.pingcap.com/tidbcloud/operators/).

> **Warning:**
>
> When using SQL string filters with dynamic user input, always validate the input to prevent [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) vulnerabilities.
