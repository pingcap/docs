---
title: Tune Region Performance
summary: Introduce how to tune Region performance by adjusting the Region size and how to use bucket to optimize concurrent queries when the Region size is large.
---

# Tune Region Performance

This document introduces how to tune Region performance by adjusting the Region size and how to use bucket to optimize concurrent queries when the Region size is large.

## Overview

TiKV automatically [shards bottom-layered data](/best-practices/tidb-best-practices.md#data-sharding), data is split into multiple Regions, each storing data for a specific key range. When the size of a Region exceeds a threshold, TiKV splits it into two or more Regions.

When processing a large amount of data, TiKV might split too many Regions, resulting in more resources for consumption and [performance regression](/best-practices/massive-regions-best-practices.md#performance-problem). For a fixed amount of data, the largest the Region, the smaller the number of Regions. Since v6.1.0, TiDB supports setting custom Region size. The default size of the Region is 96 MiB, you can reduce the Region number by adjusting it to a larger value.

Enable [Hibernate Region](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances) or [`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval) can also reduce the performance overhead of too many Regions.

## Use `region-split-size` to adjust Region size

> **Warning:**
>
> Currently, customized Region size is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments. The risks are:
>
> + More prone to performance jitter.
> + Query performance regression, especially when querying a large amount of data.
> + The schedule operator slows down.

You can adjust the Region size with [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size). It is recommended to set it to 96 MiB, 128 MiB, 256 MiB. The larger the `region-split-size`, the more jittery the performance will be. It is not recommended to set the Region size over 1 GiB and strongly recommend setting it below 10 GiB. When using TiFlash, the Region size should not exceed 256 MiB. When using the Dumpling tool, the Region size should not exceed 1 GiB and you need to reduce the concurrency after increasing the Region size, otherwise, TiDB might OOM.

## Use bucket to increase concurrency

When the Region size is large, you can set [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610) to `true` to increase the query concurrency. This config divides a Region into several buckets, which is smaller ranges within a Region. The bucket is used as the unit of concurrency query to improve the scan concurrency. You can control the bucket size with [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610), the default value is `96MiB`.