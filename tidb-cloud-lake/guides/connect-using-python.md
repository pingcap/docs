---
title: 使用 Python 连接 TiDB Cloud Lake
summary: 本页介绍如何使用 Python 连接 TiDB Cloud Lake。
---

# 使用 Python 连接 TiDB Cloud Lake

使用我们支持同步和异步操作的官方驱动，通过 Python 连接 {{{ .lake }}}。

## 快速开始 {#quick-start}

选择你偏好的方式：

| 软件包 | 最适合 | 安装 |
|---------|----------|-------------|
| **tidbcloudlake-driver** | 直接进行数据库操作，async/await | `pip install tidbcloudlake-driver` |

**Connection String**：有关 DSN 格式和示例，请参见[驱动概览](/tidb-cloud-lake/guides/driver-overview.md)。

---

## tidbcloudlake-driver {#tidbcloudlake-driver}

### 特性 {#features}

- ✅ **原生性能**：直接连接到 {{{ .lake }}}
- ✅ **支持 Async/Sync**：可根据你的编程风格进行选择
- ✅ **兼容 PEP 249**：标准 Python DB API
- ✅ **类型安全**：完整的 Python 类型映射

### 同步用法 {#synchronous-usage}

```python
from tidbcloudlake_driver import BlockingLakeClient

# Connect and execute
client = BlockingLakeClient('<your-dsn>')
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
    # row is a tidbcloudlake_driver.Row object
    # Access by column name
    print(f"id: {row['id']}, name: {row['name']}")

cursor.close()
```

### 使用 Row 对象 {#working-with-row-objects}

`Row` 对象支持多种访问模式和方法：

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

### 异步用法 {#asynchronous-usage}

```python
import asyncio
from tidbcloudlake_driver import AsyncLakeClient

async def main():
    client = AsyncLakeClient('lake://root:root@localhost:8000/?sslmode=disable')
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

## 数据类型映射 {#data-type-mappings}

| {{{ .lake }}} | Python | 说明 |
|----------|--------|-------|
| **数值类型** | | |
| `BOOLEAN` | `bool` | |
| `TINYINT` | `int` | |
| `SMALLINT` | `int` | |
| `INT` | `int` | |
| `BIGINT` | `int` | |
| `FLOAT` | `float` | |
| `DOUBLE` | `float` | |
| `DECIMAL` | `decimal.Decimal` | 保留精度 |
| **日期/时间** | | |
| `DATE` | `datetime.date` | |
| `TIMESTAMP` | `datetime.datetime` | |
| `INTERVAL` | `datetime.timedelta` | |
| **文本/二进制** | | |
| `VARCHAR` | `str` | UTF-8 编码 |
| `BINARY` | `bytes` | |
| **复杂类型** | | |
| `ARRAY` | `list` | 支持嵌套结构 |
| `TUPLE` | `tuple` | |
| `MAP` | `dict` | |
| `VARIANT` | `str` | JSON 编码 |
| `BITMAP` | `str` | Base64 编码 |
| `GEOMETRY` | `str` | WKT 格式 |

## 资源 {#resources}

- **PyPI**: [tidbcloudlake-driver](https://pypi.org/project/tidbcloudlake-driver/)
- **GitHub**: [tidbcloudlake-driver](https://github.com/tidbcloud/lakesql/tree/main/bindings/python)