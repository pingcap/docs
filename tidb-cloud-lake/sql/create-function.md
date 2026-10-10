---
title: CREATE FUNCTION
summary: Flight 経由でリモートハンドラーを呼び出す外部関数を作成します（通常は Python またはその他のサービス）。
---

# CREATE FUNCTION

Flight 経由でリモートハンドラーを呼び出す外部関数を作成します（通常は Python またはその他のサービス）。

## サポートされる言語 {#supported-languages}

- リモートサーバーによって決まります（一般的には Python ですが、Flight エンドポイントを実装していれば任意の言語を使用できます）

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
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
| `<return_type>`       | 関数の戻り値の型です。                                                                  |
| `LANGUAGE`            | 関数の記述に使用する言語を指定します。使用可能な値: `python`。                    |
| `HANDLER = '<handler_name>'` | 関数のハンドラー名を指定します。                                               |
| `ADDRESS = '<udf_server_address>'` | UDF サーバーのアドレスを指定します。                                             |

## 例 {#examples}

この例では、2 つの整数の最大公約数（GCD）を計算する外部関数について、エンドツーエンドの完全なセットアップを説明します。

### ステップ 1: Python UDF サーバーをセットアップする {#step-1-set-up-the-python-udf-server}

`tidbcloudlake-udf` パッケージをインストールします。

```bash
pip install tidbcloudlake-udf
```

次の内容で `udf_server.py` ファイルを作成します。

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

サーバーを起動します。

```bash
python udf_server.py
```

### ステップ 2: {{{ .lake }}} で関数を登録する {#step-2-register-the-function-in-lake}

```sql
CREATE FUNCTION gcd AS (INT, INT)
    RETURNS INT
    LANGUAGE python
    HANDLER = 'gcd'
    ADDRESS = 'https://udf.example.com';
```

### ステップ 3: 関数を呼び出す {#step-3-call-the-function}

```sql
SELECT gcd(48, 18);
-- Returns: 6

SELECT gcd(100, 75);
-- Returns: 25
```