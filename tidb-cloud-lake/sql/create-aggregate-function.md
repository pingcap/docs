---
title: CREATE AGGREGATE FUNCTION
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.799"/>

Creates a user-defined aggregate function (UDAF) that runs inside Databend's JavaScript or Python runtime.

### Supported Languages

- `javascript`
- `python`

## Syntax

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

| Parameter | Description |
| --- | --- |
| `<function_name>` | Name of the aggregate function. |
| `<parameter_list>` | Optional comma-separated list of input parameters and types (for example `value DOUBLE`). |
| `STATE { <state_field_list> }` | Struct definition that Databend stores between partial/final aggregation steps (for example `STATE { sum DOUBLE, count DOUBLE }`). |
| `<return_type>` | Data type returned by the aggregate (`DOUBLE`, `INT`, etc.). |
| `LANGUAGE` | Runtime used to execute the script. Supported values: `javascript`, `python`. |
| `IMPORTS` / `PACKAGES` | Optional lists for shipping extra files (imports) or PyPI packages (Python only). |
| `<language_specific_code>` | Script body that must expose `create_state`, `accumulate`, `merge`, and `finish` entry points. |
| `DESC` | Optional description. |

The script must implement these functions:

- `create_state()` – allocate and return an initial state object.
- `accumulate(state, *args)` – update the state for each input row.
- `merge(state1, state2)` – merge two partial states.
- `finish(state)` – produce the final result (return `None` for SQL `NULL`).

## Access control requirements

| Privilege | Object Type   | Description    |
|:----------|:--------------|:---------------|
| SUPER     | Global, Table | Operates a UDF |

To create a user-defined function, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the SUPER [privilege](/guides/security/access-control/privileges).

## Examples

### Python average UDAF

The following Python aggregate computes the average of a column:

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

### JavaScript average UDAF

The next example shows the same calculation implemented in JavaScript:

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
