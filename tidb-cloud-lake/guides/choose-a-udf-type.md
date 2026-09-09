---
title: Choose a User-Defined Function Type
summary: Learn how to choose a SQL, aggregate, table, or external UDF in TiDB Cloud Lake based on return shape, runtime, and operations.
---

# Choose a User-Defined Function Type

User-defined functions (UDFs) let you package reusable logic that is not available as a built-in SQL function. They can standardize business rules, simplify complex queries, implement custom aggregations, expand values into rows, or connect SQL queries to independently hosted Python services.

Before creating a UDF, check the [SQL Function Reference](/tidb-cloud-lake/sql/sql-function-reference.md). Built-in functions usually provide the simplest implementation, the lowest execution overhead, and the smallest operational burden.

## Why use UDFs

As analytical workloads grow, the same transformations often appear across many queries. Copying an expression into every query makes it harder to keep behavior consistent and to roll out changes safely.

UDFs are useful for the following tasks:

- standardizing data cleaning, validation, and business calculations;
- encapsulating a parameterized SQL query;
- implementing a custom aggregation that needs intermediate state;
- calling Python libraries, proprietary logic, or machine learning models;
- scaling specialized compute independently from the warehouse.

A UDF should have one clear responsibility. Data movement, scheduling, streaming state, joins across continuous event streams, and workflow orchestration belong in the corresponding Lake SQL, Stream, Task, or integration feature instead of inside a UDF.

## Understand the UDF ecosystem

{{{ .lake }}} provides several UDF execution models. They differ in return shape, language, hosting, and operational responsibility.

| UDF type | Implementation | Output | Hosting | Typical use |
| --- | --- | --- | --- | --- |
| SQL scalar UDF | SQL expression | One value for each input row | Managed by {{{ .lake }}} | Formatting, calculations, and reusable conditions |
| Script scalar UDF | Python or JavaScript | One value for each input row | Managed by {{{ .lake }}} | Business rules, validation, and structured data processing |
| WebAssembly scalar UDF | WebAssembly module | One value for each input row | Managed by {{{ .lake }}} | Compute-intensive logic compiled to WebAssembly |
| Aggregate UDF | Python or JavaScript | One value for each group | Managed by {{{ .lake }}} | Custom stateful aggregation |
| SQL table UDF | SQL query | A result set | Managed by {{{ .lake }}} | Reusable parameterized queries |
| External scalar UDF | Python UDF Server | One value for each input row | Hosted by you | Libraries, models, and proprietary services |
| External table UDF | Python UDF Server | Multiple columns or rows | Hosted by you | Tokenization, expansion, and record generation |

An aggregate UDF and a table UDF solve different problems. An aggregate UDF consumes multiple rows and returns one value. A table UDF returns a result set. {{{ .lake }}} does not provide a Python table aggregate UDF that combines both execution models.

## Choose the simplest execution model

Use the following order when selecting an implementation:

1. Use a built-in function when one already provides the required behavior.
2. Use a SQL scalar or table UDF when SQL can express the logic clearly.
3. Use an embedded Python or JavaScript scalar UDF for script logic that should run inside {{{ .lake }}}.
4. Use WebAssembly for compute-intensive scalar logic delivered as a compiled module.
5. Use an aggregate UDF when the calculation requires custom aggregation state.
6. Use an external UDF when the logic depends on remote services, GPUs, or independent scaling.

The following questions can help narrow the choice:

| Question | Recommended option |
| --- | --- |
| Can one SQL expression produce the result? | SQL scalar UDF |
| Does row-level logic need Python or JavaScript? | Script scalar UDF |
| Is a compiled, portable module required for compute-intensive row-level logic? | WebAssembly scalar UDF |
| Does a SQL query need to return multiple rows? | SQL table UDF |
| Must multiple input rows be combined into one custom result? | Aggregate UDF |
| Does one input need to produce multiple Python-generated rows? | External table UDF |
| Does the logic require a Python package, model, network call, or separate compute? | External scalar or table UDF |

## Use SQL scalar UDFs for reusable transformations

A SQL scalar UDF maps each input row to one value. It is a good fit for calculations, string normalization, and conditional business rules.

### Normalize phone numbers

The following function removes formatting characters so that downstream queries use one phone number representation:

```sql
CREATE FUNCTION normalize_phone(phone VARCHAR)
RETURNS VARCHAR
AS $$ REGEXP_REPLACE(phone, '[^0-9]', '') $$;

SELECT normalize_phone('+1 (415) 555-0100');
```

### Apply a discount

The following function centralizes a discount calculation:

```sql
CREATE FUNCTION apply_discount(
    price DECIMAL(10, 2),
    rate DECIMAL(5, 2)
)
RETURNS DECIMAL(10, 2)
AS $$ price * (1 - rate) $$;

SELECT apply_discount(100, 0.15);
```

Use [ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function.md) when the shared business rule changes. Queries that call the function then use the new definition without duplicating the expression.

For complete syntax, see [CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md).

## Use Python scalar UDFs for data processing logic

Python scalar UDFs are useful when the logic needs control flow, the Python standard library, or a package that is awkward to express in SQL.

The following function standardizes whitespace and capitalization in an address:

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
AS $$
def normalize_address(value):
    return " ".join(value.strip().upper().split())
$$;

SELECT normalize_address('  123 Main Street  ');
```

Python UDFs can also use `PACKAGES` for PyPI dependencies and `IMPORTS` for files stored in a stage. Keep dependencies focused so that function environments remain easier to reproduce and maintain.

## Use JavaScript scalar UDFs for JSON transformations

JavaScript is a natural fit for object and JSON transformations, especially when the logic already exists in an application codebase.

The following function normalizes an email address and removes a sensitive field:

```sql
CREATE FUNCTION clean_profile(value VARIANT)
RETURNS VARIANT
LANGUAGE javascript
HANDLER = 'cleanProfile'
AS $$
export function cleanProfile(value) {
    const result = { ...value };
    if (typeof result.email === 'string') {
        result.email = result.email.trim().toLowerCase();
    }
    delete result.ssn;
    return result;
}
$$;
```

Keep the input and return schema stable. A change in the object shape can affect every query that calls the function.

## Use WebAssembly UDFs for compiled logic

WebAssembly UDFs package compiled code as a portable module. They are suitable for compute-intensive scalar logic where a compiled implementation is preferable to a script runtime.

Upload a module that implements the required Arrow UDF interface to a stage, and then register its handler:

```sql
CREATE FUNCTION fib_wasm(value INT)
RETURNS INT
LANGUAGE wasm
HANDLER = 'fib'
AS $$ @my_wasm_stage/arrow_udf_example.wasm $$;

SELECT fib_wasm(10);
```

The module must export the named handler and use SQL-compatible input and output types. Test the compiled artifact with representative values before publishing the function to other users.

## Use aggregate UDFs for custom stateful calculations

An aggregate UDF defines how to:

1. create an initial aggregation state;
2. add each input row to the state;
3. merge partial states produced by distributed execution;
4. convert the final state into one result.

The following Python aggregate adds values. Built-in `SUM` is preferable for this specific calculation, but the example shows the lifecycle required by a custom aggregate:

```sql
CREATE FUNCTION py_total(value BIGINT)
STATE { total BIGINT }
RETURNS BIGINT
LANGUAGE python
AS $$
class State:
    def __init__(self):
        self.total = 0

def create_state():
    return State()

def accumulate(state, value):
    state.total += value
    return state

def merge(left, right):
    left.total += right.total
    return left

def finish(state):
    return state.total
$$;

SELECT py_total(number) FROM numbers(5);
```

Aggregate UDFs support Python and JavaScript. Use them only when built-in aggregate functions cannot express the required state transition or finalization logic. For more examples, see [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md).

## Use SQL table UDFs for reusable result sets

A SQL table UDF encapsulates a SQL query and returns rows and columns. It is useful for reusable filters, small reporting datasets, and parameterized transformations.

```sql
CREATE FUNCTION small_numbers(max_value INT)
RETURNS TABLE(value UINT64, doubled UINT64)
AS $$
    SELECT number AS value, number * 2 AS doubled
    FROM numbers(10)
    WHERE number < max_value
$$;

SELECT * FROM small_numbers(3);
```

The function body is a SQL query. It does not accept `LANGUAGE python`. For Python-generated rows, use an external table UDF.

For complete syntax, see [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md).

## Use external Python UDFs for specialized logic

The [`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) package provides a Python UDF Server for external scalar and table UDFs. The Python process runs on your infrastructure, which lets you use custom packages, proprietary code, GPU compute, and independent scaling.

### Normalize addresses with Python

Install the SDK:

```shell
python3 -m pip install tidbcloudlake-udf
```

Define a handler and start the server:

```python
from tidbcloudlake_udf import UDFServer, udf


@udf(
    input_types=["VARCHAR"],
    result_type="VARCHAR",
    skip_null=True,
)
def normalize_address(value: str) -> str:
    return " ".join(value.strip().upper().split())


if __name__ == "__main__":
    server = UDFServer("0.0.0.0:8815")
    server.add_function(normalize_address)
    server.serve()
```

After deploying and allowlisting the server, register the handler:

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
ADDRESS = 'https://udf.example.com';
```

### Expand text into rows

An external table UDF uses a list of output columns in `result_type`:

```python
@udf(
    input_types=["VARCHAR"],
    result_type=[("token", "VARCHAR")],
    skip_null=True,
)
def split_words(value: str):
    return [{"token": token} for token in value.split()]
```

Register and call the table handler:

```sql
CREATE FUNCTION split_words(value VARCHAR)
RETURNS TABLE(token VARCHAR)
LANGUAGE python
HANDLER = 'split_words'
ADDRESS = 'https://udf.example.com';

SELECT * FROM split_words('external UDF server');
```

For a complete server, deployment, concurrency, and registration workflow, see [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md).

## Deploy external UDFs securely

Before registering an external function:

- Deploy the UDF Server at a public HTTPS endpoint.
- Contact TiDB Cloud Support to add the endpoint hostname to your tenant UDF server allowlist.
- Configure authentication at the gateway, capacity, timeouts, high availability, upgrades, and monitoring.
- Keep credentials in the server deployment environment instead of SQL function definitions.

The SQL `ADDRESS` must contain the public endpoint. The server process can listen on `0.0.0.0` inside its deployment environment, but `localhost` and `0.0.0.0` are not valid addresses for a Cloud query service to call.

External UDFs add network latency. Keep latency-sensitive row-by-row calls small, batch work when possible, and avoid calling the same expensive function repeatedly in one query.

## Compare performance and operations

Performance depends on function complexity, input size, package startup, warehouse resources, network latency, batch size, and UDF Server capacity. Results measured in another product or deployment do not predict Lake performance.

| UDF type | Main overhead | Operational responsibility |
| --- | --- | --- |
| SQL scalar UDF | SQL expression evaluation | Managed by {{{ .lake }}} |
| Python or JavaScript scalar UDF | Script runtime and dependency initialization | Managed by {{{ .lake }}} |
| WebAssembly scalar UDF | Module loading and compiled function execution | Managed by {{{ .lake }}} |
| Aggregate UDF | Script runtime and state serialization | Managed by {{{ .lake }}} |
| SQL table UDF | Query execution | Managed by {{{ .lake }}} |
| External UDF | Network transfer and external compute | Shared between {{{ .lake }}} and your UDF Server deployment |

Benchmark the actual function with representative data and concurrency. Measure query latency, throughput, error handling, cold starts, and external service saturation.

## Follow UDF best practices

- Prefer built-in functions and SQL before introducing a script or service.
- Keep each function deterministic and focused when possible.
- Define NULL behavior explicitly and test nullable inputs.
- Use precise input and return types to avoid unnecessary conversions.
- For aggregate UDFs, make `merge` associative so partial states can be combined safely.
- For external UDFs, use `batch_mode` for batch-oriented libraries and `io_threads` for I/O-bound row processing.
- Set `max_concurrency` to protect external dependencies from overload.
- Treat external handler changes like service API changes and deploy them compatibly with registered SQL definitions.
- Monitor errors, latency, saturation, and dependency health for user-hosted servers.
- Remove unused UDF registrations and server handlers together.

## Get started

Choose the next step based on the required output:

- [CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md) for reusable SQL expressions.
- [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md) for custom Python or JavaScript aggregation state.
- [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md) for reusable SQL result sets.
- [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md) for external Python scalar and table handlers.
- [External AI Functions](/tidb-cloud-lake/guides/external-ai-functions.md) for a model inference example.

## Related resources

- [User-Defined Function](/tidb-cloud-lake/sql/user-defined-function.md)
- [External Function](/tidb-cloud-lake/sql/external-function.md)
- [`tidbcloud/lake-udf` on GitHub](https://github.com/tidbcloud/lake-udf)
