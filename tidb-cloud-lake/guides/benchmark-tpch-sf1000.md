---
title: "TPC-H SF1000 (1TB): {{{ .lake }}} Warehouse Size Benchmark"
summary: This guide presents a performance comparison of Small, Medium, and Large {{{ .lake }}} Warehouses using the TPC-H SF1000 dataset. It includes query execution times for each warehouse size and instructions to reproduce the benchmark results.
---

# TPC-H SF1000 (1TB): {{{ .lake }}} Warehouse Size Benchmark

This page compares Small, Medium, and Large {{{ .lake }}} Warehouses on the same TPC-H SF1000 workload. SF1000 is commonly used to represent about 1TB of TPC-H data.

## Dataset Scale

TPC-H Scale Factor 1000 (SF1000) represents approximately 1TB of generated data. The dataset contains about 6 billion rows across the 8 standard TPC-H tables.

| Table | Rows |
|---|---:|
| customer | 150,000,000 |
| lineitem | 6,000,000,000 |
| nation | 25 |
| orders | 1,500,000,000 |
| part | 200,000,000 |
| partsupp | 800,000,000 |
| region | 5 |
| supplier | 10,000,000 |

> **Note:**
>
> TPC Benchmark™ and TPC-H™ are trademarks of the Transaction Processing Performance Council ([TPC](http://www.tpc.org)). This test is inspired by TPC-H, but it is not an official TPC-H result.

## Summary

| Warehouse Size | Total Time | Speedup vs. Small | Speedup vs. Previous Size |
|---|---:|---:|---:|
| Small | 1173.32s | 1.00x | — |
| Medium | 537.93s | 2.18x | 2.18x |
| Large | 285.96s | 4.10x | 1.88x |

![TPC-H SF1000 Warehouse Size Benchmark](/media/tidb-cloud-lake/tpch-sf1000-warehouse-size-benchmark.png)

Medium is about 2.18x faster than Small. Large is about 4.10x faster than Small and completes the full 22-query workload in under 5 minutes.

## Query Details

Unit: seconds. Lower is better.

| Query | Small | Medium | Large | Small → Medium | Medium → Large |
|---:|---:|---:|---:|---:|---:|
| Q1 | 31.61 | 19.93 | 10.33 | 1.59x | 1.93x |
| Q2 | 10.00 | 7.15 | 5.52 | 1.40x | 1.30x |
| Q3 | 73.07 | 24.50 | 17.75 | 2.98x | 1.38x |
| Q4 | 177.60 | 17.22 | 16.39 | 10.31x | 1.05x |
| Q5 | 300.78 | 17.69 | 11.22 | 17.00x | 1.58x |
| Q6 | 13.93 | 4.46 | 2.19 | 3.12x | 2.04x |
| Q7 | 33.08 | 18.08 | 9.78 | 1.83x | 1.85x |
| Q8 | 31.37 | 17.81 | 10.90 | 1.76x | 1.63x |
| Q9 | 102.01 | 45.41 | 29.52 | 2.25x | 1.54x |
| Q10 | 40.84 | 31.18 | 23.05 | 1.31x | 1.35x |
| Q11 | 5.91 | 3.59 | 2.20 | 1.65x | 1.63x |
| Q12 | 23.74 | 11.81 | 8.70 | 2.01x | 1.36x |
| Q13 | 57.78 | 34.52 | 23.78 | 1.67x | 1.45x |
| Q14 | 38.45 | 9.84 | 5.18 | 3.91x | 1.90x |
| Q15 | 13.22 | 8.18 | 4.82 | 1.62x | 1.70x |
| Q16 | 4.77 | 3.25 | 2.27 | 1.47x | 1.43x |
| Q17 | 20.77 | 11.29 | 5.87 | 1.84x | 1.92x |
| Q18 | 90.78 | 158.89 | 17.24 | 0.57x | 9.22x |
| Q19 | 20.36 | 10.86 | 8.22 | 1.87x | 1.32x |
| Q20 | 25.34 | 10.07 | 4.94 | 2.52x | 2.04x |
| Q21 | 52.85 | 64.57 | 61.19 | 0.82x | 1.06x |
| Q22 | 5.06 | 7.64 | 4.90 | 0.66x | 1.56x |
| Total | 1173.32 | 537.93 | 285.96 | 2.18x | 1.88x |

## Notes

The overall workload scales clearly as the Warehouse size increases. Some individual queries may not scale linearly due to query shape, execution plan, scheduling, and cache behavior.
