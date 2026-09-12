---
title: CREATE SCALAR FUNCTION
summary: 创建标量用户定义函数（Scalar UDF）。同一个 CREATE FUNCTION 语句支持两种实现方式。
---

# CREATE SCALAR FUNCTION

创建标量用户定义函数（Scalar UDF）。同一个 `CREATE FUNCTION` 语句支持两种实现方式：

- **SQL expression**：仅使用 SQL 表达逻辑；不需要外部运行时。
- **Python / JavaScript**：编写代码，并使用 `HANDLER` 指定入口点。

如果你需要调用外部系统（HTTP/服务），请参见 External Function 命令。

## 语法 {#syntax}

### SQL（expression） {#sql-expression}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS <return_type>
    AS $$ <expression> $$
    [ DESC='<description>' ]
```

### Python / JavaScript {#python-javascript}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS <return_type>
    LANGUAGE <language>
    [IMPORTS = ('<import_path>', ...)]
    [PACKAGES = ('<package_name>', ...)]
    HANDLER = '<handler_name>'
    AS $$ <function_code> $$
    [ DESC='<description>' ]
```

## 参数 {#parameters}

- `<parameter_list>`：可选的逗号分隔参数列表及其类型（例如：`x INT, y FLOAT`）
- `<return_type>`：函数返回值的数据类型
- `<language>`：`python`、`javascript`
- `<import_path>`：要导入的 stage 文件（例如：`@s_udf/your_file.zip`）
- `<package_name>`：从 PyPI 安装的包（仅 Python；例如 `numpy`）
- `<handler_name>`：代码中要调用的函数名称
- `<function_code>`：使用指定语言编写的实现代码

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型   | 描述    |
|:----------|:--------------|:---------------|
| SUPER     | 全局, Table | 操作 UDF |

要创建用户定义函数，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 SUPER [权限](/tidb-cloud-lake/guides/privileges.md)。

## SQL {#sql}

```sql
-- Create a function to calculate area of a circle
CREATE OR REPLACE FUNCTION area_of_circle(radius FLOAT)
RETURNS FLOAT
AS $$
  pi() * radius * radius
$$;

-- Create a function to calculate age in years
CREATE OR REPLACE FUNCTION calculate_age(birth_date DATE)
RETURNS INT
AS $$
  date_diff('year', birth_date, now())
$$;

-- Create a function with multiple parameters
CREATE OR REPLACE FUNCTION calculate_bmi(weight_kg FLOAT, height_m FLOAT)
RETURNS FLOAT
AS $$
  weight_kg / (height_m * height_m)
$$;

-- Use the functions
SELECT area_of_circle(5.0) AS circle_area;
SELECT calculate_age(to_date('1990-05-15')) AS age;
SELECT calculate_bmi(70.0, 1.75) AS bmi;
```

## Python {#python}

Python 运行时需要 {{{ .lake }}} Enterprise。你可以通过 `PACKAGES` 安装 PyPI 包，并通过 `IMPORTS` 导入 stage 文件。

### 数据类型映射（Python） {#data-type-mappings-python}

| {{{ .lake }}} 类型 | Python 类型 |
|--------------|-------------|
| NULL | None |
| BOOLEAN | bool |
| INT | int |
| FLOAT/DOUBLE | float |
| DECIMAL | decimal.Decimal |
| VARCHAR | str |
| BINARY | bytes |
| LIST | list |
| MAP | dict |
| STRUCT | object |
| JSON | dict/list |

### 示例 {#examples}

```sql
CREATE OR REPLACE FUNCTION calculate_age_py(VARCHAR)
RETURNS INT
LANGUAGE python
HANDLER = 'calculate_age'
AS $$
from datetime import datetime

def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age
$$;

SELECT calculate_age_py('1990-05-15') AS age;
```

```sql
CREATE OR REPLACE FUNCTION numpy_sqrt(FLOAT)
RETURNS FLOAT
LANGUAGE python
PACKAGES = ('numpy')
HANDLER = 'numpy_sqrt'
AS $$
import numpy as np

def numpy_sqrt(x):
    return float(np.sqrt(x))
$$;

SELECT numpy_sqrt(9.0) AS sqrt_val;
```

## JavaScript {#javascript}

### 数据类型映射（JavaScript） {#data-type-mappings-javascript}

| {{{ .lake }}} 类型 | JavaScript 类型 |
|--------------|----------------|
| NULL | null |
| BOOLEAN | Boolean |
| INT | Number |
| FLOAT/DOUBLE | Number |
| DECIMAL | BigDecimal |
| VARCHAR | String |
| BINARY | Uint8Array |
| DATE/TIMESTAMP | Date |
| ARRAY | Array |
| MAP | Object |
| STRUCT | Object |
| JSON | Object/Array |

### 示例 {#example}

```sql
CREATE OR REPLACE FUNCTION calculate_age_js(VARCHAR)
RETURNS INT
LANGUAGE javascript
HANDLER = 'calculateAge'
AS $$
export function calculateAge(birthDateStr) {
    const birthDate = new Date(birthDateStr);
    const today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    return age;
}
$$;
```

## UDF 的 Worker 管理 {#worker-management-for-udfs}

在 {{{ .lake }}} 中，每个 UDF 都关联一个 **Worker**，用于在沙箱中管理其执行环境。创建 UDF 后，你可能需要管理其 worker，以获得更优的性能和资源利用率。

### 为你的 UDF 创建 Worker {#creating-a-worker-for-your-udf}

```sql
-- Create a worker for your UDF (worker name should match UDF name)
CREATE WORKER calculate_age_js WITH
    size='small',
    auto_suspend='300',
    auto_resume='true';
```

### 管理 Worker 资源 {#managing-worker-resources}

```sql
-- View all workers
SHOW WORKERS;

-- Adjust worker settings
ALTER WORKER calculate_age_js SET size='medium', auto_suspend='600';

-- Add tags for organization
ALTER WORKER calculate_age_js SET TAG
    environment='production',
    team='analytics',
    purpose='age-calculation';
```

### Worker 生命周期 {#worker-lifecycle}

```sql
-- Suspend worker when not in use
ALTER WORKER calculate_age_js SUSPEND;

-- Resume worker when needed
ALTER WORKER calculate_age_js RESUME;

-- Remove worker when UDF is no longer needed
DROP WORKER calculate_age_js;
```

### 环境变量 {#environment-variables}

出于安全原因，UDF 的环境变量需要在云控制台中单独管理。创建 UDF 及其 worker 后，请通过 {{{ .lake }}} 接口配置所需的环境变量。

更多信息，请参见 [Worker 管理](/tidb-cloud-lake/sql/worker-overview.md)。