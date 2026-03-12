---
title: EXPLAIN PERF
---

import FunctionDescription from '@site/src/components/FunctionDescription';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<FunctionDescription description="Introduced or updated: v1.2.765"/>

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

<img alt="graphs" src="https://github.com/user-attachments/assets/07acfefa-a1c3-4c00-8c43-8ca1aafc3224"/>

If the query finishes very quickly, it may not collect enough data, resulting in an empty flame graph.
