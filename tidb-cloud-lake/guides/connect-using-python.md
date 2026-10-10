---
title: Python を使用して TiDB Cloud Lake に接続する
summary: このページでは、Python を使用して TiDB Cloud Lake に接続する方法について説明します。
---

# Python を使用して TiDB Cloud Lake に接続する

同期処理と非同期処理の両方をサポートする公式ドライバーを使用して、Python から {{{ .lake }}} に接続します。

## クイックスタート {#quick-start}

お好みの方法を選択してください。

| パッケージ | 最適な用途 | インストール |
|---------|----------|-------------|
| **tidbcloudlake-driver** | 直接的なデータベース操作、async/await | `pip install tidbcloudlake-driver` |

**Connection String**: DSN の形式と例については、[ドライバー概要](/tidb-cloud-lake/guides/driver-overview.md) を参照してください。

---

## tidbcloudlake-driver {#tidbcloudlake-driver}

### 機能 {#features}

- ✅ **ネイティブパフォーマンス**: {{{ .lake }}} への直接接続
- ✅ **Async/Sync Support**: プログラミングスタイルに応じて選択可能
- ✅ **PEP 249 Compatible**: 標準の Python DB API
- ✅ **Type Safety**: 完全な Python 型マッピング

### 同期での使用方法 {#synchronous-usage}

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

### Row オブジェクトの操作 {#working-with-row-objects}

`Row` オブジェクトは、複数のアクセスパターンとメソッドをサポートしています。

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

### 非同期での使用方法 {#asynchronous-usage}

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

## データ型マッピング {#data-type-mappings}

| {{{ .lake }}} | Python | 注記 |
|----------|--------|-------|
| **数値型** | | |
| `BOOLEAN` | `bool` | |
| `TINYINT` | `int` | |
| `SMALLINT` | `int` | |
| `INT` | `int` | |
| `BIGINT` | `int` | |
| `FLOAT` | `float` | |
| `DOUBLE` | `float` | |
| `DECIMAL` | `decimal.Decimal` | 精度を保持 |
| **日付/時刻** | | |
| `DATE` | `datetime.date` | |
| `TIMESTAMP` | `datetime.datetime` | |
| `INTERVAL` | `datetime.timedelta` | |
| **テキスト/バイナリ** | | |
| `VARCHAR` | `str` | UTF-8 エンコード |
| `BINARY` | `bytes` | |
| **複合型** | | |
| `ARRAY` | `list` | ネストされた構造をサポート |
| `TUPLE` | `tuple` | |
| `MAP` | `dict` | |
| `VARIANT` | `str` | JSON エンコード |
| `BITMAP` | `str` | Base64 エンコード |
| `GEOMETRY` | `str` | WKT 形式 |

## リソース {#resources}

- **PyPI**: [tidbcloudlake-driver](https://pypi.org/project/tidbcloudlake-driver/)
- **GitHub**: [tidbcloudlake-driver](https://github.com/tidbcloud/lakesql/tree/main/bindings/python)