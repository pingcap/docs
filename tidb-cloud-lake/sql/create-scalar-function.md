---
title: CREATE SCALAR FUNCTION
summary: スカラー user-defined function（Scalar UDF）を作成します。同じ CREATE FUNCTION ステートメントで 2 つの実装スタイルをサポートします。
---

# CREATE SCALAR FUNCTION

スカラー user-defined function（Scalar UDF）を作成します。同じ `CREATE FUNCTION` ステートメントで、次の 2 つの実装スタイルをサポートします。

- **SQL expression**: ロジックを純粋に SQL で記述します。外部ランタイムは不要です。
- **Python / JavaScript**: コードを記述し、`HANDLER` でエントリポイントを指定します。

外部システム（HTTP/サービス）を呼び出す必要がある場合は、External Function コマンドを参照してください。

## 構文 {#syntax}

### SQL（式） {#sql-expression}

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

## パラメーター {#parameters}

- `<parameter_list>`: パラメーターとその型のオプションのカンマ区切りリスト（例: `x INT, y FLOAT`）
- `<return_type>`: 関数の戻り値のデータ型
- `<language>`: `python`, `javascript`
- `<import_path>`: インポートする stage ファイル（例: `@s_udf/your_file.zip`）
- `<package_name>`: PyPI からインストールするパッケージ（Python のみ。例: `numpy`）
- `<handler_name>`: 呼び出すコード内の関数名
- `<function_code>`: 指定した言語で記述された実装コード

## アクセス制御要件 {#access-control-requirements}

| 権限 | オブジェクトタイプ   | 説明    |
|:----------|:--------------|:---------------|
| SUPER     | グローバル、テーブル | UDF を操作します |

user-defined function を作成するには、操作を実行するユーザー、または [current_role](/tidb-cloud-lake/guides/roles.md) が、SUPER [privilege](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

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

Python ランタイムには {{{ .lake }}} Enterprise が必要です。`PACKAGES` を使用して PyPI パッケージをインストールでき、`IMPORTS` を使用して stage ファイルをインポートできます。

### データ型マッピング（Python） {#data-type-mappings-python}

| {{{ .lake }}} 型 | Python 型 |
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

### 例 {#examples}

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

### データ型マッピング（JavaScript） {#data-type-mappings-javascript}

| {{{ .lake }}} 型 | JavaScript 型 |
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

### 例 {#example}

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

## UDF の Worker 管理 {#worker-management-for-udfs}

{{{ .lake }}} では、各 UDF に sandbox 内の実行環境を管理する関連 **Worker** があります。UDF を作成した後は、パフォーマンスとリソース使用率を最適化するために、その worker を管理する必要がある場合があります。

### UDF 用の Worker を作成する {#creating-a-worker-for-your-udf}

```sql
-- Create a worker for your UDF (worker name should match UDF name)
CREATE WORKER calculate_age_js WITH
    size='small',
    auto_suspend='300',
    auto_resume='true';
```

### Worker リソースを管理する {#managing-worker-resources}

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

### Worker のライフサイクル {#worker-lifecycle}

```sql
-- Suspend worker when not in use
ALTER WORKER calculate_age_js SUSPEND;

-- Resume worker when needed
ALTER WORKER calculate_age_js RESUME;

-- Remove worker when UDF is no longer needed
DROP WORKER calculate_age_js;
```

### 環境変数 {#environment-variables}

セキュリティ上の理由により、UDF の環境変数はクラウドコンソールで個別に管理されます。UDF とその Worker を作成した後、必要な環境変数を {{{ .lake }}} インターフェースから設定してください。

詳細は、[Worker 管理](/tidb-cloud-lake/sql/worker-overview.md) を参照してください。