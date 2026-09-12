---
title: CREATE AGGREGATE FUNCTION
summary: 创建在 {{{ .lake }}} 的 JavaScript 或 Python 运行时中运行的用户定义聚合函数（UDAF）。
---

# CREATE AGGREGATE FUNCTION

创建在 {{{ .lake }}} 的 JavaScript 或 Python 运行时中运行的用户定义聚合函数（UDAF）。

## 支持的语言 {#supported-languages}

- `javascript`
- `python`

## 语法 {#syntax}

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

| 参数 | 描述 |
| --- | --- |
| `<function_name>` | 聚合函数的名称。 |
| `<parameter_list>` | 可选的、以逗号分隔的输入参数及其类型列表（例如 `value DOUBLE`）。 |
| `STATE { <state_field_list> }` | {{{ .lake }}} 在部分/最终聚合步骤之间存储的结构体定义（例如 `STATE { sum DOUBLE, count DOUBLE }`）。 |
| `<return_type>` | 聚合返回的数据类型（`DOUBLE`、`INT` 等）。 |
| `LANGUAGE` | 用于执行脚本的运行时。支持的值：`javascript`、`python`。 |
| `IMPORTS` / `PACKAGES` | 可选列表，用于附带额外文件（imports）或 PyPI 包（仅 Python）。 |
| `<language_specific_code>` | 脚本主体，必须暴露 `create_state`、`accumulate`、`merge` 和 `finish` 入口点。 |
| `DESC` | 可选描述。 |

脚本必须实现以下函数：

- `create_state()` – 分配并返回一个初始状态对象。
- `accumulate(state, *args)` – 针对每一行输入修改状态。
- `merge(state1, state2)` – 合并两个部分状态。
- `finish(state)` – 生成最终结果（对 SQL `NULL` 返回 `None`）。

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型   | 描述    |
|:----------|:--------------|:---------------|
| SUPER     | 全局, Table | 操作 UDF |

要创建用户定义函数，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 SUPER [权限](/tidb-cloud-lake/guides/privileges.md)。

## 示例 {#examples}

### Python average UDAF {#python-average-udaf}

以下 Python 聚合用于计算某一列的平均值：

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

下一个示例展示了如何用 JavaScript 实现相同的计算：

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