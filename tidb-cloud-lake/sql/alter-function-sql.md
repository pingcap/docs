---
title: ALTER FUNCTION
summary: 外部関数を変更します。
---

# ALTER FUNCTION

外部関数を変更します。

## 構文 {#syntax}

```sql
ALTER FUNCTION [ IF NOT EXISTS ] <function_name>
    AS ( <input_param_types> ) RETURNS <return_type> LANGUAGE <language_name>
    HANDLER = '<handler_name>' ADDRESS = '<udf_server_address>'
    [DESC='<description>']
```

| パラメーター             | 説明                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `<function_name>`     | 関数の名前です。                                                                        |
| `<lambda_expression>` | 関数の動作を定義するラムダ式またはコードスニペットです。                          |
| `DESC='<description>'`  | UDF の説明です。|
| `<<input_param_names>`| 入力パラメーター名の一覧です。カンマで区切ります。|
| `<<input_param_types>`| 入力パラメーター型の一覧です。カンマで区切ります。|
| `<return_type>`       | 戻り値の型です。                                                                  |
| `LANGUAGE`            | 関数の記述に使用する言語を指定します。使用可能な値: `python`。                    |
| `HANDLER = '<handler_name>'` | 関数のハンドラー名を指定します。                                               |
| `ADDRESS = '<udf_server_address>'` | UDF サーバーのアドレスを指定します。                                             |

## 例 {#examples}

```sql
-- Create an external function
CREATE FUNCTION gcd (INT, INT) RETURNS INT LANGUAGE python HANDLER = 'gcd' ADDRESS = 'https://udf.example.com';

-- Modify the handler of the external function
ALTER FUNCTION gcd (INT, INT) RETURNS INT LANGUAGE python HANDLER = 'gcd_new' ADDRESS = 'https://udf.example.com';
```