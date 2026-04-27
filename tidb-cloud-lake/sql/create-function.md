---
title: CREATE FUNCTION
summary: Creates an external function that calls a remote handler over Flight (typically Python or other services).
---

# CREATE FUNCTION

> **Note:**
>
> Introduced or updated in v1.2.339.

Creates an external function that calls a remote handler over Flight (typically Python or other services).

## Supported Languages

- Determined by the remote server (commonly Python, but any language can be used as long as it implements the Flight endpoint)

## Syntax

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    AS ( <input_param_types> ) RETURNS <return_type> LANGUAGE <language_name>
    HANDLER = '<handler_name>' ADDRESS = '<udf_server_address>'
    [DESC='<description>']
```

| Parameter             | Description                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `<function_name>`     | The name of the function.                                                                        |
| `<lambda_expression>` | The lambda expression or code snippet defining the function's behavior.                          |
| `DESC='<description>'`  | Description of the UDF.|
| `<<input_param_names>`| A list of input parameter names. Separated by comma.|
| `<<input_param_types>`| A list of input parameter types. Separated by comma.|
| `<return_type>`       | The return type of the function.                                                                  |
| `LANGUAGE`            | Specifies the language used to write the function. Available values: `python`.                    |
| `HANDLER = '<handler_name>'` | Specifies the name of the function's handler.                                               |
| `ADDRESS = '<udf_server_address>'` | Specifies the address of the UDF server.                                             |

## Examples

This example walks through a complete end-to-end setup for an external function that calculates the greatest common divisor (GCD) of two integers.

### Step 1: Set Up the Python UDF Server

Install the `databend-udf` package:

```bash
pip install databend-udf
```

Create a file `udf_server.py` with the following content:

```python
from databend_udf import udf, UDFServer

@udf(
    input_types=["INT", "INT"],
    result_type="INT",
    skip_null=True,
)
def gcd(x: int, y: int) -> int:
    while y != 0:
        (x, y) = (y, x % y)
    return x

if __name__ == '__main__':
    server = UDFServer("0.0.0.0:8815")
    server.add_function(gcd)
    server.serve()
```

Start the server:

```bash
python udf_server.py
```

### Step 2: Register the Function in {{{ .lake }}}

```sql
CREATE FUNCTION gcd AS (INT, INT)
    RETURNS INT
    LANGUAGE python
    HANDLER = 'gcd'
    ADDRESS = 'http://localhost:8815';
```

### Step 3: Call the Function

```sql
SELECT gcd(48, 18);
-- Returns: 6

SELECT gcd(100, 75);
-- Returns: 25
```
