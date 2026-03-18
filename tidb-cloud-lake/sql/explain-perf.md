---
title: EXPLAIN PERF
summary: Profiles query CPU usage and returns an HTML flame graph collected from all cluster nodes.
---

> **Note:**
>
> Introduced or updated in v1.2.765.

`EXPLAIN PERF` captures stack traces to perform CPU profiling. This command returns an HTML file containing flame graphs generated from data collected from all nodes in the current cluster. You can directly open this HTML file in your browser.

It is helpful to analyze query performance and help identify bottlenecks.

## Syntax

```sql
EXPLAIN PERF <statement>
```

## Examples

```shell
bendsql --quote-style never --query="EXPLAIN PERF SELECT avg(number) FROM numbers(10000000)" > demo.html
```

Then, you can open the `demo.html` file in your browser to view the flame graphs:

<img alt="graphs" src="/media/tidb-cloud-lake/remote-914114962b44-07acfefa-a1c3-4c00-8c43-8ca1aafc3224"/>

If the query finishes very quickly, it may not collect enough data, resulting in an empty flame graph.
