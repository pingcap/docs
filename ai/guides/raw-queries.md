---
title: Raw Queries
summary: Learn how to use raw queries in your application.
---

# Raw Queries

This guide describes how to run raw SQL queries in your application.

## Operate data with raw SQL

Use the `client.execute()` method to execute `INSERT`, `UPDATE`, `DELETE`, and other data-manipulation statements.

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

## Query data with raw SQL

Use the `client.query()` method to execute `SELECT`, `SHOW`, and other query statements.

### Output query result

The `client.query()` method will return a `SQLQueryResult` instance with some helper methods:

- `to_pydantic()`
- `to_list()`
- `to_pandas()`
- `to_rows()`
- `scalar()`

#### As Pydantic model

The `to_pydantic()` method returns a list of Pydantic models.

```python
client.query("SELECT id, text, user_id FROM chunks").to_pydantic()
```

#### As SQLAlchemy result rows

The `to_rows()` method returns a list of tuples, where each tuple represents one row.

```python
client.query("SHOW TABLES;").to_rows()
```

#### As list of dict

The `to_list()` method converts the query result to a list of dictionaries.

```python
client.query(
    "SELECT id, text, user_id FROM chunks WHERE user_id = :user_id",
    {
        "user_id": 3
    }
).to_list()
```

#### As pandas DataFrame

The `to_pandas()` method converts the query result to a `pandas.DataFrame`, which is displayed in a human-friendly format within the notebook:

```python
client.query("SELECT id, text, user_id FROM chunks").to_pandas()
```

#### As scalar value

The `scalar()` method will return the first column of the first row of the result set.

```python
client.query("SELECT COUNT(*) FROM chunks;").scalar()
```