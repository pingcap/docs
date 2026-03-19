---
title: Connect to TiDB Cloud Lake Using Python
summary: This page describes how to connect to TiDB Cloud Lake using Python.
---

# Connect to TiDB Cloud Lake Using Python

Connect to Databend using Python with our official drivers supporting both synchronous and asynchronous operations.

## Quick Start

Choose your preferred approach:

| Package | Best For | Installation |
|---------|----------|-------------|
| **databend-driver** | Direct database operations, async/await | `pip install databend-driver` |
| **databend-sqlalchemy** | ORM integration, existing SQLAlchemy apps | `pip install databend-sqlalchemy` |

**Connection String**: See [connection strings](/tidb-cloud-lake/guides/connection-overview.md#connection-strings).

---

## databend-driver (Recommended)

### Features
- ✅ **Native Performance**: Direct connection to Databend
- ✅ **Async/Sync Support**: Choose your programming style
- ✅ **PEP 249 Compatible**: Standard Python DB API
- ✅ **Type Safety**: Full Python type mapping

### Synchronous Usage

```python
from databend_driver import BlockingDatabendClient

# Connect and execute
client = BlockingDatabendClient('<your-dsn>')
cursor = client.cursor()

# DDL: Create table
cursor.execute("CREATE TABLE users (id INT, name STRING)")

# Write: Insert data
cursor.execute("INSERT INTO users VALUES (?, ?)", (1, 'Alice'))

# Query: Read data
# Query: Read data
cursor.execute("SELECT * FROM users")

# Get column names
# cursor.description returns a list of tuples, where the first element is the column name
print(f"Columns: {[desc[0] for desc in cursor.description]}")

for row in cursor.fetchall():
    # row is a databend_driver.Row object
    # Access by column name
    print(f"id: {row['id']}, name: {row['name']}")

cursor.close()
```

### Working with Row Objects

The `Row` object supports multiple access patterns and methods:

```python
for row in cursor.fetchall():
    # 1. Access by column name (Recommended)
    print(f"Name: {row['name']}")

    # 2. Access by index
    print(f"First column: {row[0]}")

    # 3. Convert to tuple
    print(f"Values: {row.values()}")

    # 4. Explicit methods
    print(row.get_by_field('name'))
    print(row.get_by_index(0))
```

### Asynchronous Usage

```python
import asyncio
from databend_driver import AsyncDatabendClient

async def main():
    client = AsyncDatabendClient('<your-dsn>')
    conn = await client.get_conn()

    # DDL: Create table
    await conn.exec("CREATE TABLE users (id INT, name STRING)")

    # Write: Insert data
    await conn.exec("INSERT INTO users VALUES (?, ?)", (1, 'Alice'))

    # Query: Read data
    rows = await conn.query_iter("SELECT * FROM users")
    async for row in rows:
        print(row.values())

    await conn.close()

asyncio.run(main())
```

---

## databend-sqlalchemy

For SQLAlchemy ORM integration:

```python
from sqlalchemy import create_engine, text

engine = create_engine('<your-dsn>')
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchall())
```

---

## Data Type Mappings

| Databend | Python | Notes |
|----------|--------|-------|
| **Numeric Types** | | |
| `BOOLEAN` | `bool` | |
| `TINYINT` | `int` | |
| `SMALLINT` | `int` | |
| `INT` | `int` | |
| `BIGINT` | `int` | |
| `FLOAT` | `float` | |
| `DOUBLE` | `float` | |
| `DECIMAL` | `decimal.Decimal` | Precision preserved |
| **Date/Time** | | |
| `DATE` | `datetime.date` | |
| `TIMESTAMP` | `datetime.datetime` | |
| `INTERVAL` | `datetime.timedelta` | |
| **Text/Binary** | | |
| `VARCHAR` | `str` | UTF-8 encoded |
| `BINARY` | `bytes` | |
| **Complex Types** | | |
| `ARRAY` | `list` | Nested structures supported |
| `TUPLE` | `tuple` | |
| `MAP` | `dict` | |
| `VARIANT` | `str` | JSON-encoded |
| `BITMAP` | `str` | Base64-encoded |
| `GEOMETRY` | `str` | WKT format |

## Resources

- **PyPI**: [databend-driver](https://pypi.org/project/databend-driver/) • [databend-sqlalchemy](https://pypi.org/project/databend-sqlalchemy/)
- **GitHub**: [databend-driver](https://github.com/databendlabs/bendsql/tree/main/bindings/python) • [databend-sqlalchemy](https://github.com/databendlabs/databend-sqlalchemy)
