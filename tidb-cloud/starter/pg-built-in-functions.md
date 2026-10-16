---
title: PostgreSQL 内置函数
summary: 了解 PostgreSQL 兼容的 TiDB Cloud Starter 支持的内置函数。
---

# PostgreSQL 内置函数

PostgreSQL 兼容的 {{{ .starter }}} 为常见的字符串、数值、日期和时间、聚合、窗口、JSON、数组、正则表达式、序列以及系统操作提供内置函数。

## 字符串函数 {#string-functions}

支持以下常见字符串函数：

| Function | Description |
| --- | --- |
| `UPPER(text)` | 将文本转换为大写。 |
| `LOWER(text)` | 将文本转换为小写。 |
| `LENGTH(text)` | 返回字符数。 |
| `CHAR_LENGTH(text)` | 返回字符数。 |
| `LEFT(text, n)` | 返回前 `n` 个字符。 |
| `RIGHT(text, n)` | 返回后 `n` 个字符。 |
| `TRIM(text)` | 移除首尾空格或指定字符。 |
| `BTRIM(text [, chars])` | 移除两端的字符。 |
| `LTRIM(text [, chars])` | 移除左侧的字符。 |
| `RTRIM(text [, chars])` | 移除右侧的字符。 |
| `LPAD(text, length [, fill])` | 在左侧填充文本。 |
| `RPAD(text, length [, fill])` | 在右侧填充文本。 |
| `REPEAT(text, n)` | 重复一个字符串。 |
| `REVERSE(text)` | 反转一个字符串。 |
| `INITCAP(text)` | 将每个单词的首字母转换为大写。 |
| `ASCII(text)` | 返回第一个字符的字符编码。 |
| `CHR(int)` | 根据字符编码返回对应字符。 |
| `STRPOS(text, substring)` | 返回子字符串基于 1 的位置。 |
| `POSITION(substring IN text)` | `STRPOS` 的 SQL 标准写法。 |
| `SPLIT_PART(text, delimiter, field)` | 切分文本并返回其中一个字段。 |
| `TRANSLATE(text, from, to)` | 替换单个字符。 |
| `OVERLAY(...)` | 替换字符串的一部分。 |
| `STARTS_WITH(text, prefix)` | 检查文本是否以前缀开头。 |
| `CONCAT(...)` | 拼接值，并忽略 `NULL` 参数。 |
| `CONCAT_WS(separator, ...)` | 使用分隔符拼接值。 |
| `SUBSTRING(...)` | 提取子字符串。 |
| `REPLACE(text, from, to)` | 替换子字符串的出现位置。 |
| `FORMAT(format, ...)` | 使用 PostgreSQL 风格的格式说明符格式化字符串。 |
| `QUOTE_IDENT(text)` | 在必要时为 SQL 标识符加引号。 |
| `QUOTE_LITERAL(text)` | 为 SQL 字面量加引号。 |
| `QUOTE_NULLABLE(text)` | 为 SQL 字面量加引号，并在输入为空值时返回字符串 `NULL`。 |

例如：

```sql
SELECT
    UPPER('hello') AS upper_text,
    LENGTH('PostgreSQL') AS text_length,
    CONCAT_WS('-', '2026', '09', '19') AS date_text,
    SPLIT_PART('a,b,c', ',', 2) AS second_part;
```

## 数学函数 {#mathematical-functions}

支持以下常见数学函数：

| 函数 | 描述 |
| --- | --- |
| `ABS(x)` | 返回绝对值。 |
| `CEIL(x)` / `CEILING(x)` | 向上舍入到最接近的整数。 |
| `FLOOR(x)` | 向下舍入到最接近的整数。 |
| `ROUND(x [, scale])` | 对数值进行四舍五入。 |
| `TRUNC(x [, scale])` | 截断数值。 |
| `SQRT(x)` | 返回平方根。 |
| `CBRT(x)` | 返回立方根。 |
| `POWER(x, y)` | 返回 `x` 的 `y` 次幂。 |
| `EXP(x)` | 返回指数值。 |
| `LN(x)` | 返回自然对数。 |
| `LOG(x)` | 返回对数。 |
| `MOD(x, y)` | 返回余数。 |
| `SIGN(x)` | 返回数字的符号。 |

例如：

```sql
SELECT
    ABS(-42),
    ROUND(4.567, 2),
    SQRT(16),
    POWER(2, 8);
```

## 日期和时间函数 {#date-and-time-functions}

支持以下常见日期和时间函数及表达式：

| 函数或表达式 | 描述 |
| --- | --- |
| `CURRENT_DATE` | 返回当前日期。 |
| `CURRENT_TIME` | 返回当前时间。 |
| `CURRENT_TIMESTAMP` | 返回当前时间戳。 |
| `LOCALTIME` | 返回当前本地时间。 |
| `LOCALTIMESTAMP` | 返回当前本地时间戳。 |
| `NOW()` | 返回当前事务时间戳。 |
| `DATE_TRUNC(field, value)` | 将日期或时间戳截断到指定单位。 |
| `DATE_PART(field, value)` | 提取一个日期或时间字段。 |
| `EXTRACT(field FROM value)` | 提取日期或时间字段的 SQL 标准写法。 |
| `AGE(timestamp [, timestamp])` | 返回时间戳之间的符号化时间间隔。 |
| `MAKE_DATE(year, month, day)` | 构造一个日期。 |
| `MAKE_INTERVAL(...)` | 构造一个时间间隔。 |

例如：

```sql
SELECT
    CURRENT_DATE,
    NOW(),
    DATE_TRUNC('day', NOW()),
    EXTRACT(YEAR FROM CURRENT_DATE);
```

也支持使用 `INTERVAL` 进行日期和时间运算：

```sql
SELECT NOW() - INTERVAL '7 days';
```

## 设置示例数据 {#set-up-sample-data}

以下各节中的一些示例会查询示例表。在运行这些示例之前，请先创建所需的表，并将示例数据插入到测试数据库中。

本页中的表定义与其他示例中的表定义不同。如果你的测试数据库中已经包含下方所示名称的表，请为本页使用单独的测试数据库。

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    nickname TEXT,
    active BOOLEAN,
    score INTEGER
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary NUMERIC
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMP
);

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    settings JSONB
);

INSERT INTO users (id, name, nickname, active, score) VALUES
    (1, 'Alice', 'Ali', true, 100),
    (2, 'Bob', NULL, false, 0),
    (3, 'Charlie', NULL, true, 85);

INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'Alice', 'Engineering', 90000),
    (2, 'Bob', 'Engineering', 85000),
    (3, 'Charlie', 'Sales', 75000);

INSERT INTO events (id, created_at) VALUES
    (1, '2026-09-01 10:00:00'),
    (2, '2026-09-02 11:00:00'),
    (3, '2026-09-03 12:00:00');

INSERT INTO profiles (id, settings) VALUES
    (1, '{"theme": "dark", "active": true}'::jsonb),
    (2, '{"theme": "light", "active": false}'::jsonb);
```

在执行基于表的示例之前，请先运行一次上述设置。使用字面量值的示例则不需要任何设置。

## 聚合函数 {#aggregate-functions}

支持以下常见聚合函数：

| 函数 | 描述 |
| --- | --- |
| `COUNT(*)` | 统计行数。 |
| `COUNT(expression)` | 统计非空值的数量。 |
| `COUNT(DISTINCT expression)` | 统计不同的非空值数量。 |
| `SUM(expression)` | 返回总和。 |
| `AVG(expression)` | 返回平均值。 |
| `MIN(expression)` | 返回最小值。 |
| `MAX(expression)` | 返回最大值。 |
| `STRING_AGG(expression, delimiter)` | 使用分隔符连接各个值。 |
| `ARRAY_AGG(expression)` | 将值聚合为数组。 |
| `JSON_AGG(expression)` | 将值聚合为 JSON 数组。 |
| `JSONB_AGG(expression)` | 将值聚合为 JSONB 数组。 |
| `JSON_OBJECT_AGG(key, value)` | 将键值对聚合为 JSON 对象。 |
| `JSONB_OBJECT_AGG(key, value)` | 将键值对聚合为 JSONB 对象。 |
| `BOOL_AND(expression)` | 如果所有非空输入都为 true，则返回 true。 |
| `BOOL_OR(expression)` | 如果任一非空输入为 true，则返回 true。 |

例如：

```sql
SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary,
    MAX(salary) AS maximum_salary
FROM employees
GROUP BY department;
```

支持聚合 `FILTER`：

```sql
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## 窗口函数 {#window-functions}

与 PostgreSQL 兼容的 {{{ .starter }}} 支持常见的排名窗口函数和值访问窗口函数。

### 排名函数 {#ranking-functions}

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `NTILE()`
- `PERCENT_RANK()`
- `CUME_DIST()`

例如：

```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees;
```

### 值访问函数 {#value-access-functions}

- `LAG()`
- `LEAD()`
- `FIRST_VALUE()`
- `LAST_VALUE()`
- `NTH_VALUE()`

例如：

```sql
SELECT
    id,
    created_at,
    LAG(created_at) OVER (ORDER BY created_at) AS previous_created_at
FROM events;
```

### 作为窗口函数的聚合函数 {#aggregate-functions-as-window-functions}

以下聚合函数可以与 `OVER` 子句一起使用：

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

例如：

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

其他聚合函数不能用作窗口函数。

## JSON 和 JSONB 函数 {#json-and-jsonb-functions}

支持以下常见 JSON 和 JSONB 函数：

| 函数 | 描述 |
| --- | --- |
| `JSON_TYPEOF(json)` | 返回顶层 JSON 值的类型。 |
| `JSONB_TYPEOF(jsonb)` | 返回顶层 JSONB 值的类型。 |
| `JSON_BUILD_OBJECT(...)` | 根据键值对构建 JSON 对象。 |
| `JSONB_BUILD_OBJECT(...)` | 根据键值对构建 JSONB 对象。 |
| `JSON_BUILD_ARRAY(...)` | 构建 JSON 数组。 |
| `JSONB_BUILD_ARRAY(...)` | 构建 JSONB 数组。 |
| `JSON_ARRAY_LENGTH(json)` | 返回 JSON 数组的长度。 |
| `JSONB_ARRAY_LENGTH(jsonb)` | 返回 JSONB 数组的长度。 |
| `JSON_ARRAY_ELEMENTS(json)` | 将 JSON 数组展开为多行。 |
| `JSONB_ARRAY_ELEMENTS(jsonb)` | 将 JSONB 数组展开为多行。 |
| `JSON_OBJECT_KEYS(json)` | 返回对象的键。 |
| `JSONB_OBJECT_KEYS(jsonb)` | 返回对象的键。 |
| `JSONB_EACH(jsonb)` | 将 JSONB 对象展开为键值行。 |
| `JSONB_SET(jsonb, path, value [, create_missing])` | 替换或插入指定路径上的 JSONB 值。 |

例如：

```sql
SELECT
    JSONB_TYPEOF('{"a":1}'::jsonb),
    JSONB_BUILD_OBJECT('name', 'Alice', 'active', true),
    JSONB_ARRAY_LENGTH('[1,2,3]'::jsonb);
```

### JSON 运算符 {#json-operators}

支持常见的 PostgreSQL JSON 和 JSONB 运算符，包括：

| 运算符 | 描述 |
| --- | --- |
| `->` | 按键或数组索引获取 JSON 值。 |
| `->>` | 以文本形式获取 JSON 值。 |
| `#>` | 按路径获取 JSON 值。 |
| `#>>` | 按路径以文本形式获取 JSON 值。 |
| `@>` | 检查 JSONB 是否包含指定内容。 |
| `<@` | 检查 JSONB 是否被另一个值包含。 |
| `?` | 检查某个键是否存在。 |
| `?|` | 检查列出的任一键是否存在。 |
| `?&` | 检查列出的所有键是否都存在。 |

例如：

```sql
SELECT settings->>'theme'
FROM profiles
WHERE settings @> '{"active":true}';
```

## 数组函数 {#array-functions}

支持以下常见数组函数：

| 函数 | 描述 |
| --- | --- |
| `ARRAY_LENGTH(array, dimension)` | 返回数组某一维度的长度。 |
| `ARRAY_UPPER(array, dimension)` | 返回某一维度的上界。 |
| `ARRAY_LOWER(array, dimension)` | 返回某一维度的下界。 |
| `ARRAY_APPEND(array, element)` | 追加一个元素。 |
| `ARRAY_PREPEND(element, array)` | 在开头添加一个元素。 |
| `ARRAY_CAT(array1, array2)` | 连接数组。 |
| `ARRAY_POSITION(array, element)` | 返回第一个匹配位置。 |
| `ARRAY_POSITIONS(array, element)` | 返回所有匹配位置。 |
| `ARRAY_REMOVE(array, element)` | 删除匹配的元素。 |
| `ARRAY_REPLACE(array, from, to)` | 替换匹配的元素。 |
| `ARRAY_TO_STRING(array, delimiter [, null_string])` | 将数组转换为文本。 |
| `STRING_TO_ARRAY(text, delimiter [, null_string])` | 将文本切分为数组。 |
| `UNNEST(array)` | 将数组展开为多行。 |
| `GENERATE_SUBSCRIPTS(array, dimension)` | 生成有效的数组索引。 |

例如：

```sql
SELECT
    ARRAY_LENGTH(ARRAY['a', 'b', 'c'], 1),
    ARRAY_APPEND(ARRAY['a', 'b'], 'c'),
    ARRAY_POSITION(ARRAY['a', 'b', 'c'], 'b');
```

## 正则表达式函数和操作符 {#regular-expression-functions-and-operators}

支持以下正则表达式函数：

| 函数 | 描述 |
| --- | --- |
| `REGEXP_REPLACE(text, pattern, replacement [, flags])` | 替换与正则表达式匹配的文本。 |
| `REGEXP_SPLIT_TO_ARRAY(text, pattern [, flags])` | 使用正则表达式切分文本。 |
| `REGEXP_SPLIT_TO_TABLE(text, pattern [, flags])` | 将文本切分为多行。 |

例如：

```sql
SELECT REGEXP_REPLACE(
    'foo   bar',
    '\s+',
    ' ',
    'g'
);
```

支持以下正则表达式操作符：

| 操作符 | 描述 |
| --- | --- |
| `~` | 大小写敏感匹配。 |
| `~*` | 大小写不敏感匹配。 |
| `!~` | 大小写敏感不匹配。 |
| `!~*` | 大小写不敏感不匹配。 |

例如：

```sql
SELECT 'PostgreSQL' ~* 'postgres';
```

## UUID、编码和哈希函数 {#uuid-encoding-and-hashing-functions}

常见的 UUID、编码和哈希函数包括：

| 函数 | 描述 |
| --- | --- |
| `GEN_RANDOM_UUID()` | 生成一个随机 UUID。 |
| `MD5(text)` | 以十六进制文本形式返回 MD5 哈希值。 |
| `ENCODE(bytea, format)` | 对二进制数据进行编码。 |
| `DECODE(text, format)` | 将文本解码为二进制数据。 |

此外，系统内置了额外的与 `uuid-ossp` 兼容的 UUID 函数，并且可以使用 `CREATE EXTENSION "uuid-ossp"` 来注册该扩展的元信息。

## 序列函数 {#sequence-functions}

支持以下序列函数：

| 函数 | 描述 |
| --- | --- |
| `NEXTVAL(sequence)` | 推进序列并返回新值。 |
| `CURRVAL(sequence)` | 返回当前会话中该序列最近一次由 `NEXTVAL` 返回的值。 |
| `SETVAL(sequence, value [, called])` | 设置当前序列值。 |
| `LASTVAL()` | 返回当前会话中最近一次由 `NEXTVAL` 返回的值。 |

例如：

```sql
CREATE SEQUENCE order_seq START WITH 1000;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT setval('order_seq', 2000);
```

`NEXTVAL` 等序列操作是非事务性的。

## 条件表达式 {#conditional-expressions}

支持以下 PostgreSQL 条件表达式：

- `CASE`
- `COALESCE`
- `NULLIF`
- `GREATEST`
- `LEAST`

例如：

```sql
SELECT
    COALESCE(nickname, name) AS display_name,
    NULLIF(score, 0) AS nonzero_score
FROM users;
```

## 系统和兼容性函数 {#system-and-compatibility-functions}

常见的 PostgreSQL 兼容系统函数包括：

| 函数或表达式 | 描述 |
| --- | --- |
| `CURRENT_USER` | 返回当前角色名称。 |
| `SESSION_USER` | 返回会话用户。 |
| `CURRENT_DATABASE()` | 返回当前数据库。 |
| `CURRENT_SCHEMA()` | 返回当前数据库模式。 |
| `CURRENT_SCHEMAS(boolean)` | 返回当前搜索路径中的数据库模式。 |
| `VERSION()` | 返回与 PostgreSQL 兼容的服务器版本信息。 |
| `PG_TYPEOF(value)` | 返回值的数据类型。 |
| `PG_BACKEND_PID()` | 返回与 PostgreSQL 兼容的后端进程标识符。 |
| `CURRENT_SETTING(name)` | 返回会话参数值。 |

例如：

```sql
SELECT
    CURRENT_USER,
    CURRENT_DATABASE(),
    CURRENT_SCHEMA(),
    PG_TYPEOF(42);
```

## 返回集合的函数 {#set-returning-functions}

某些函数会返回多行。

在 `FROM` 子句中使用 `GENERATE_SERIES()`：

```sql
SELECT value
FROM generate_series(1, 5) AS t(value);
```

`UNNEST()` 可以展开数组：

```sql
SELECT value
FROM unnest(ARRAY['a', 'b', 'c']) AS t(value);
```

对于某些标量函数和返回集合的函数，函数调用位置可能与 PostgreSQL 不同。为保证可移植性，建议像前面的示例那样，在 `FROM` 子句中使用返回集合的函数。

## 扩展特定函数 {#extension-specific-functions}

以下能力提供了额外的 SQL 函数：

- 向量搜索和向量嵌入
- 全文搜索
- HTTP 请求
- Parquet 导入
- UUID 生成

更多信息，参见[PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)。