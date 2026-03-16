---
title: SYSTEM ENABLE / DISABLE EXCEPTION_BACKTRACE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.530"/>

Controls the generation of Rust backtraces in Databend. SYSTEM ENABLE EXCEPTION_BACKTRACE enables backtraces for debugging purposes when a panic occurs, while SYSTEM DISABLE EXCEPTION_BACKTRACE disables them to avoid additional overhead or exposure of sensitive information.

## Syntax

```sql
-- Enable Rust backtraces
SYSTEM ENABLE EXCEPTION_BACKTRACE

-- Disable Rust backtraces
SYSTEM DISABLE EXCEPTION_BACKTRACE
```