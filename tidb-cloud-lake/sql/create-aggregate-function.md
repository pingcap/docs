---
title: CREATE AGGREGATE FUNCTION
summary: {{{ .lake }}} の JavaScript または Python ランタイム内で実行されるユーザー定義集計関数（UDAF）を作成します。
---

# CREATE AGGREGATE FUNCTION

{{{ .lake }}} の JavaScript または Python ランタイム内で実行されるユーザー定義集計関数（UDAF）を作成します。

## サポートされる言語 {#supported-languages}

- `javascript`
- `python`

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    ( [ <parameter_list> ] )
    STATE { <state_field_list> }
    RETURNS <return_type>
    LANGUAGE <language_name>
    [ IMPORTS = (<stage_files>) ]
    [ PACKAGES = (<python_packages>) ]
AS $$
<language_specific_code>
$$
[ DESC='<description>' ]
```

| パラメーター | 説明 |
| --- | --- |
| `<function_name>` | 集計関数の名前です。 |
| `<parameter_list>` | 省略可能な、カンマ区切りの入力パラメーターと型のリストです（例: `value DOUBLE`）。 |
| `STATE { <state_field_list> }` | {{{ .lake }}} が部分集計/最終集計の各ステップ間で保持する構造体定義です（例: `STATE { sum DOUBLE, count DOUBLE }`）。 |
| `<return_type>` | 集計が返すデータ型です（`DOUBLE`、`INT` など）。 |
| `LANGUAGE` | スクリプトの実行に使用するランタイムです。サポートされる値: `javascript`、`python`。 |
| `IMPORTS` / `PACKAGES` | 追加ファイル（imports）または PyPI パッケージ（Python のみ）を含めるための省略可能なリストです。 |
| `<language_specific_code>` | `create_state`、`accumulate`、`merge`、`finish` のエントリーポイントを公開する必要があるスクリプト本体です。 |
| `DESC` | 省略可能な説明です。 |

スクリプトでは、次の関数を実装する必要があります。

- `create_state()` – 初期状態オブジェクトを割り当てて返します。
- `accumulate(state, *args)` – 各入力行に対して状態を更新します。
- `merge(state1, state2)` – 2 つの部分状態をマージします。
- `finish(state)` – 最終結果を生成します（SQL の `NULL` を返す場合は `None` を返します）。

## アクセス制御要件 {#access-control-requirements}

| 権限 | オブジェクトタイプ   | 説明    |
|:----------|:--------------|:---------------|
| SUPER     | グローバル、テーブル | UDF を操作する |

ユーザー定義関数を作成するには、操作を実行するユーザー、または [current_role](/tidb-cloud-lake/guides/roles.md) が SUPER [privilege](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

## 例 {#examples}

### Python average UDAF {#python-average-udaf}

次の Python 集計は、カラムの平均を計算します。

```sql
CREATE OR REPLACE FUNCTION py_avg (value DOUBLE)
    STATE { sum DOUBLE, count DOUBLE }
    RETURNS DOUBLE
    LANGUAGE python
AS $$
class State:
    def __init__(self):
        self.sum = 0.0
        self.count = 0.0

def create_state():
    return State()

def accumulate(state, value):
    if value is not None:
        state.sum += value
        state.count += 1
    return state

def merge(state1, state2):
    state1.sum += state2.sum
    state1.count += state2.count
    return state1

def finish(state):
    if state.count == 0:
        return None
    return state.sum / state.count
$$;

SELECT py_avg(number) AS avg_val FROM numbers(5);
```

```
+---------+
| avg_val |
+---------+
|       2 |
+---------+
```

### JavaScript average UDAF {#javascript-average-udaf}

次の例は、同じ計算を JavaScript で実装したものです。

```sql
CREATE OR REPLACE FUNCTION js_avg (value DOUBLE)
    STATE { sum DOUBLE, count DOUBLE }
    RETURNS DOUBLE
    LANGUAGE javascript
AS $$
export function create_state() {
    return { sum: 0, count: 0 };
}

export function accumulate(state, value) {
    if (value !== null) {
        state.sum += value;
        state.count += 1;
    }
    return state;
}

export function merge(state1, state2) {
    state1.sum += state2.sum;
    state1.count += state2.count;
    return state1;
}

export function finish(state) {
    if (state.count === 0) {
        return null;
    }
    return state.sum / state.count;
}
$$;

SELECT js_avg(number) AS avg_val FROM numbers(5);
```

```
+---------+
| avg_val |
+---------+
|       2 |
+---------+
```