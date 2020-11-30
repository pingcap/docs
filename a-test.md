---
title: Distinct Optimization
summary: Introduce the `distinct` optimization in the TiDB query optimizer.
---

# Distinct Optimization

This document introduces the `distinct` optimization in the TiDB query optimizer, including `SELECT DISTINCT` and `DISTINCT` in the aggregate functions.

## Distinct Optimize

The `DISTINCT` modifier specifies removal of duplicate rows from the result set. `SELECT DISTINCT` is transformed to `GROUP BY`, for example：

* Check whether the TiKV process is normal, the network is isolated, and the load is too high, and recover the service as much as possible.
* This document introduces its concept, implementation principles, auto-increment related features and restrictions.

### Distinct Data

The value of this parameter should be between 7 - 10 in github.