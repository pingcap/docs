---
title: ALTER FUNCTION
summary: 修改外部函数。
---

# ALTER FUNCTION

修改外部函数。

## 语法 {#syntax}

```sql
ALTER FUNCTION [ IF NOT EXISTS ] <function_name>
    AS ( <input_param_types> ) RETURNS <return_type> LANGUAGE <language_name>
    HANDLER = '<handler_name>' ADDRESS = '<udf_server_address>'
    [DESC='<description>']
```

| 参数 | 描述 |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `<function_name>`     | 函数的名称。                                                                        |
| `<lambda_expression>` | 定义函数行为的 lambda 表达式或代码片段。                          |
| `DESC='<description>'`  | UDF 的描述。|
| `<<input_param_names>`| 输入参数名称列表，以逗号分隔。|
| `<<input_param_types>`| 输入参数类型列表，以逗号分隔。|
| `<return_type>`       | 函数的返回类型。                                                                  |
| `LANGUAGE`            | 指定编写函数所使用的语言。可用值：`python`。                    |
| `HANDLER = '<handler_name>'` | 指定函数 handler 的名称。                                               |
| `ADDRESS = '<udf_server_address>'` | 指定 UDF 服务器的地址。                                             |

## 示例 {#examples}

```sql
-- Create an external function
CREATE FUNCTION gcd (INT, INT) RETURNS INT LANGUAGE python HANDLER = 'gcd' ADDRESS = 'https://udf.example.com';

-- Modify the handler of the external function
ALTER FUNCTION gcd (INT, INT) RETURNS INT LANGUAGE python HANDLER = 'gcd_new' ADDRESS = 'https://udf.example.com';
```