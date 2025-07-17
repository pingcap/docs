---
title: TiDB Data Type
summary: 了解 TiDB 中的 JSON 数据类型。
---

# JSON Data Type

TiDB 支持 `JSON` (JavaScript Object Notation) 数据类型，适用于存储半结构化数据。与将 `JSON` 格式字符串存储在字符串列中相比，`JSON` 数据类型具有以下优势：

- 使用二进制格式进行序列化。内部格式允许快速访问 `JSON` 文档元素。
- 自动验证存储在 `JSON` 列中的 JSON 文档。只有有效的文档才能被存储。

`JSON` 列，像其他二进制类型的列一样，不会被直接索引，但你可以以生成列的形式对 `JSON` 文档中的字段建立索引：

```sql
CREATE TABLE city (
    id INT PRIMARY KEY,
    detail JSON,
    population INT AS (JSON_EXTRACT(detail, '$.population')),
    index index_name (population)
    );
INSERT INTO city (id,detail) VALUES (1, '{"name": "Beijing", "population": 100}');
SELECT id FROM city WHERE population >= 100;
```

更多信息，请参见 [JSON Functions](/functions-and-operators/json-functions.md) 和 [Generated Columns](/generated-columns.md)。

## JSON 值类型

JSON 文档中的值具有类型。这在 [`JSON_TYPE`()](/functions-and-operators/json-functions/json-functions-return.md#json_type) 的输出中可以看到。

| 类型             | 示例                        |
|------------------|------------------------------|
| ARRAY            | `[]`                         |
| BIT              |                              |
| BLOB             | `0x616263`                   |
| BOOLEAN          | `true`                       |
| DATE             | `"2025-06-14"`               |
| DATETIME         | `"2025-06-14 09:05:10.000000"` |
| DOUBLE           | `1.14`                       |
| INTEGER          | `5`                          |
| NULL             | `null`                       |
| OBJECT           | `{}`                         |
| OPAQUE           |                              |
| STRING           | `"foobar"`                   |
| TIME             | `"09:10:00.000000"`          |
| UNSIGNED INTEGER | `9223372036854776000`        |

## 限制

- 目前，TiDB 仅支持将有限的 `JSON` 函数下推到 TiFlash。更多信息，请参见 [Push-down expressions](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)。
- TiDB Backup & Restore (BR) 在 v6.3.0 版本中改变了 `JSON` 列数据的编码方式。因此，不建议使用 BR 将包含 `JSON` 列的数据还原到早于 v6.3.0 的 TiDB 集群。
- 不要使用任何复制工具复制包含非标准 `JSON` 数据类型（如 `DATE`、`DATETIME` 和 `TIME`）的数据。

## MySQL 兼容性

- 当你用 `BINARY` 类型创建 `JSON` 列并存入数据时，MySQL 目前会误将数据标记为 `STRING` 类型，而 TiDB 会正确处理为 `BINARY` 类型。

    ```sql
    CREATE TABLE test(a json);
    INSERT INTO test SELECT json_objectagg('a', b'01010101');

    -- 在 TiDB 中，执行以下 SQL 语句会返回 `0, 0`。在 MySQL 中，执行相同 SQL 会返回 `0, 1`。
    mysql> SELECT JSON_EXTRACT(JSON_OBJECT('a', b'01010101'), '$.a') = "base64:type15:VQ==" AS r1, JSON_EXTRACT(a, '$.a') = "base64:type15:VQ==" AS r2 FROM test;
    +------+------+
    | r1   | r2   |
    +------+------+
    |    0 |    0 |
    +------+------+
    1 row in set (0.01 sec)
    ```

    更多信息，请参见 issue [#37443](https://github.com/pingcap/tidb/issues/37443)。

- 当将数据类型从 `ENUM` 或 `SET` 转换为 `JSON` 时，TiDB 会检查数据格式的正确性。例如，在 TiDB 中执行以下 SQL 语句会返回错误。

    ```sql
    CREATE TABLE t(e ENUM('a'));
    INSERT INTO t VALUES ('a');
    mysql> SELECT CAST(e AS JSON) FROM t;
    ERROR 3140 (22032): Invalid JSON text: The document root must not be followed by other values.
    ```

    更多信息，请参见 issue [#9999](https://github.com/pingcap/tidb/issues/9999)。

- 在 TiDB 中，你可以使用 `ORDER BY` 对 JSON 数组或 JSON 对象进行排序。

    在 MySQL 中，如果你用 `ORDER BY` 对 JSON 数组或 JSON 对象排序，MySQL 会返回警告，且排序结果与比较操作的结果不一致：

    ```sql
    CREATE TABLE t(j JSON);
    INSERT INTO t VALUES ('[1,2,3,4]');
    INSERT INTO t VALUES ('[5]');

    mysql> SELECT j FROM t WHERE j < JSON_ARRAY(5);
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    +--------------+
    1 row in set (0.00 sec)

    -- 在 TiDB 中，执行以下 SQL 语句会返回正确的排序结果。在 MySQL 中，执行会返回 "This version of MySQL doesn't yet support 'sorting of non-scalar JSON values'." 警告，且排序结果与 `<` 比较的结果不一致。
    mysql> SELECT j FROM t ORDER BY j;
    +--------------+
    | j            |
    +--------------+
    | [1, 2, 3, 4] |
    | [5]          |
    +--------------+
    2 rows in set (0.00 sec)
    ```

    更多信息，请参见 issue [#37506](https://github.com/pingcap/tidb/issues/37506)。

- 当你向 `JSON` 列插入数据时，TiDB 会隐式将数据值转换为 `JSON` 类型。

    ```sql
    CREATE TABLE t(col JSON);

    -- 在 TiDB 中，以下 INSERT 语句执行成功。在 MySQL 中，执行会返回 "Invalid JSON text" 错误。
    INSERT INTO t VALUES (3);
    ```

关于 `JSON` 数据类型的更多信息，请参见 [JSON functions](/functions-and-operators/json-functions.md) 和 [Generated Columns](/generated-columns.md)。