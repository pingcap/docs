---
title: Raw Queries
summary: Learn how to use raw queries in your application.
---

# Raw Queries

This document introduces how to use raw SQL queries in your application.

## Operate data with raw SQL

You can use `client.execute()` method to execute `INSERT`, `UPDATE`, `DELETE` and other data manipulation SQL statements.

```python
client.execute("INSERT INTO chunks(text, user_id) VALUES ('sample text', 5)")
```

### SQL injection prevention

Both the `execute()` and `query()` methods support the **Parameterized SQL** feature, which helps you avoid [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) while building dynamic SQL statements.

```python
client.execute(
    "INSERT INTO chunks(text, user_id) VALUES (:text, :user_id)",
    {
        "text": "sample text",
        "user_id": 6,
    },
)
```

## Query data with rawSQL

You can use `client.query()` method to execute `SELECT`, `SHOW` and other query SQL statements.

### Output query result

The `client.query()` method will return a `SQLQueryResult` instance with some helper methods:

- `to_pydantic()`
- `to_list()`
- `to_pandas()`
- `to_rows()`
- `scalar()`


#### As Pydantic model

The `to_pydantic()` method will return a list of Pydantic models.

```python
client.query("SELECT id, text, user_id FROM chunks").to_pydantic()
```

#### As SQLAlchemy result rows

The `to_rows()` method will return a list of tuple, every tuple represent of one row of data.

```python
client.query("SHOW TABLES;").to_rows()
```

#### As list of dict

The `to_list()` method will convert the query result into a list of dict.

```python
client.query(
    "SELECT id, text, user_id FROM chunks WHERE user_id = :user_id",
    {
        "user_id": 3
    }
).to_list()
```

#### As pandas DataFrame

The `to_pandas()` method to convert the query result to a `pandas.DataFrame`, which is displayed as human-friendly style on the notebook:

```python
client.query("SELECT id, text, user_id FROM chunks").to_pandas()
```

#### As scalar value

The `scalar()` method will return the first column of the first row of the result set.

```python
client.query("SELECT COUNT(*) FROM chunks;").scalar()
```