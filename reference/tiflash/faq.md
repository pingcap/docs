---
title: TiFlash FAQ
summary: Learn the Frequently Asked Questions and the solutions about TiDB.
category: faq
---

# TiFlash FAQ

This document lists the Frequently Asked Questions and the solutions about TiDB.

## Does TiFlash support direct writes?

Currently, TiFlash does not support direct writes. You can only write to TiKV, and then replicate to TiFlash.

## How can I estimate the storage resources if I want to add TiFlash to an existing cluster?

You can evaluate which tables might require acceleration. The size a single replica of these tables data is roughly equal to the storage resources required by two replicas of TiFlash. Note that you need to take into account the free space required.

## How do TiFlash data be highly available?

TiFlash restores data through TiKV. As long as the corresponding Regions in TiKV are available, TiFlash can perform data restore using these Regions.

## How many replicas does TiFlash recommend to set up?

If you need highly available TiFlash service (rather than highly available data), it is recommended to set up two replicas for TiFlash. If the TiKV replicas are allowed to provide service when TiFlash loses nodes, you can set up a single replica.

## Should I use TiSpark or TiDB server for a query?

It is recommended to use TiDB server if you query a single table with filtering and aggregation, because TiDB server shows better performance on the columnar storage. It is recommended to use TiSpark if you query table joins.
