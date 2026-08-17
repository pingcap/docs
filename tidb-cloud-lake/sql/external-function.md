---
title: External Function
summary: Learn how TiDB Cloud Lake calls independently hosted Python scalar and table UDFs through Apache Arrow Flight over gRPC and HTTP/2.
---

# External Function

External functions let SQL queries call Python logic that runs on infrastructure you operate. The [`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) package provides a UDF Server based on Apache Arrow Flight.

External functions are suitable for Python libraries, model inference, proprietary business logic, GPU workloads, and compute that must scale independently from a warehouse.

## How external functions work

1. You define scalar or table handlers with the `tidbcloudlake_udf.udf` decorator.
2. A `UDFServer` exposes the handlers through Arrow Flight over gRPC/HTTP2.
3. You deploy the server behind a public HTTPS endpoint.
4. TiDB Cloud Support adds the endpoint hostname to your tenant UDF server allowlist.
5. You register each handler with `CREATE FUNCTION` and call it from SQL.

The UDF Server endpoint is not configured in the Lake DSN. The SQL `ADDRESS` identifies the server that the query service calls.

## Supported functions

The Python SDK supports:

- scalar UDFs that return one value for each input row;
- table UDFs that return multiple columns or rows;
- scalar and complex SQL data types, including arrays, maps, tuples, variants, and vectors;
- NULL handling, batch processing, I/O threads, request cancellation, and per-function concurrency limits.

The SDK does not implement aggregate UDF state. Use [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md) for a custom aggregation managed by {{{ .lake }}}.

## Network and operational requirements

- The public endpoint must use HTTPS and support gRPC over HTTP/2.
- Contact TiDB Cloud Support to add the endpoint hostname to the tenant UDF server allowlist before running `CREATE FUNCTION`.
- The server process can bind to `0.0.0.0` inside its deployment environment, but SQL `ADDRESS` must use a hostname that {{{ .lake }}} can reach.
- You are responsible for endpoint authentication, capacity, high availability, monitoring, upgrades, and the Python dependencies used by handlers.

## Management commands

| Command | Description |
| --- | --- |
| [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md) | Registers an external scalar or table handler. |
| [ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function-sql.md) | Changes an external function registration. |
| [DROP FUNCTION](/tidb-cloud-lake/sql/drop-function-sql.md) | Removes an external function registration. |
| [SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md) | Lists registered functions. |

For an AI inference example, see [External AI Functions](/tidb-cloud-lake/guides/external-ai-functions.md).
