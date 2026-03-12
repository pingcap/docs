---
title: CREATE SCALAR FUNCTION
sidebar_position: 0
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: SQL v1.2.799; Python/JavaScript v1.2.339"/>

Creates a scalar user-defined function (Scalar UDF). The same `CREATE FUNCTION` statement supports two implementation styles:

- **SQL expression**: Logic expressed purely in SQL; no external runtime is required.
- **Python / JavaScript**: Write code and specify the entry point with `HANDLER`.

If you need to call external systems (HTTP/services), see External Function commands.

## Syntax

### SQL (expression)

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name> 
    ( [<parameter_list>] ) 
    RETURNS <return_type>
    AS $$ <expression> $$
    [ DESC='<description>' ]
```

### Python / JavaScript

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

## Parameters

- `<parameter_list>`: Optional comma-separated list of parameters with their types (e.g., `x INT, y FLOAT`)
- `<return_type>`: The data type of the function's return value
- `<language>`: `python`, `javascript`
- `<import_path>`: Stage files to import (e.g., `@s_udf/your_file.zip`)
- `<package_name>`: Packages to install from PyPI (Python only; e.g. `numpy`)
- `<handler_name>`: Name of the function in the code to call
- `<function_code>`: Implementation code in the specified language

## Access control requirements

| Privilege | Object Type   | Description    |
|:----------|:--------------|:---------------|
| SUPER     | Global, Table | Operates a UDF |

To create a user-defined function, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the SUPER [privilege](/guides/security/access-control/privileges).

## SQL

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

## Python

Python runtime requires Databend Enterprise. You can install PyPI packages via `PACKAGES` and import stage files via `IMPORTS`.

### Data type mappings (Python)

| Databend Type | Python Type |
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

### Examples

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

## JavaScript

### Data type mappings (JavaScript)

| Databend Type | JavaScript Type |
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

### Example

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
