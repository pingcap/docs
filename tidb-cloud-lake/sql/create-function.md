---
title: CREATE FUNCTION
summary: 创建一个通过 Flight 调用远程 handler 的外部函数（通常为 Python 或其他服务）。
---

# CREATE FUNCTION

创建一个通过 Flight 调用远程 handler 的外部函数（通常为 Python 或其他服务）。

## 支持的语言 {#supported-languages}

- 由远程服务器决定（通常为 Python，但只要实现了 Flight endpoint，也可以使用任何语言）

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    AS ( <input_param_types> ) RETURNS <return_type> LANGUAGE <language_name>
    HANDLER = '<handler_name>' ADDRESS = '<udf_server_address>'
    [DESC='<description>']
```

| 参数             | 描述                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `<function_name>`     | 函数名称。                                                                        |
| `<lambda_expression>` | 定义函数行为的 lambda 表达式或代码片段。                          |
| `DESC='<description>'`  | UDF 的描述。|
| `<<input_param_names>`| 输入参数名称列表，以逗号分隔。|
| `<<input_param_types>`| 输入参数类型列表，以逗号分隔。|
| `<return_type>`       | 函数的返回类型。                                                                  |
| `LANGUAGE`            | 指定编写函数所使用的语言。可用值：`python`。                    |
| `HANDLER = '<handler_name>'` | 指定函数 handler 的名称。                                               |
| `ADDRESS = '<udf_server_address>'` | 指定 UDF 服务器的地址。                                             |

## 示例 {#examples}

本示例将演示一个完整的端到端配置过程，用于创建一个计算两个整数最大公约数（GCD）的外部函数。

### 第 1 步：设置 Python UDF 服务器 {#step-1-set-up-the-python-udf-server}

安装 `tidbcloudlake-udf` 包：

```bash
pip install tidbcloudlake-udf
```

创建文件 `udf_server.py`，内容如下：

```python
from tidbcloudlake_udf import udf, UDFServer

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

启动服务器：

```bash
python udf_server.py
```

### 第 2 步：在 {{{ .lake }}} 中注册函数 {#step-2-register-the-function-in-lake}

```sql
CREATE FUNCTION gcd AS (INT, INT)
    RETURNS INT
    LANGUAGE python
    HANDLER = 'gcd'
    ADDRESS = 'https://udf.example.com';
```

### 第 3 步：调用函数 {#step-3-call-the-function}

```sql
SELECT gcd(48, 18);
-- Returns: 6

SELECT gcd(100, 75);
-- Returns: 25
```