---
title: Data Pipeline FAQ
summary: Frequently asked questions about TiDB Cloud Data Pipeline to TiDB Cloud Lake, including external stages, event-driven ingestion, and billing.
---

# Data Pipeline FAQ

This document answers common questions about TiDB Cloud Data Pipeline to TiDB Cloud Lake.

## Why does a data pipeline require an external stage?

The external stage is required for reliability. Because both sides work through the stage instead of transferring data directly, the write rate on the TiDB Cloud side is decoupled from the consumption rate of TiDB Cloud Lake:

- Under high write throughput, change data is durably stored in the stage and is not lost, even if loading into TiDB Cloud Lake is delayed or interrupted.
- The stage buffers the write load and relieves the pressure on the TiDB Cloud Lake side.
- The ingestion frequency on the TiDB Cloud Lake side is decoupled from the write rate, which gives you a way to control the cost on the TiDB Cloud Lake side.

## When should I enable event-driven ingestion with an SQS queue?

Enable event-driven ingestion when you need **lower data latency** than the default polling mode provides.

In the default mode, the Data Pipeline relies on two independent polling intervals — one on the Changefeed side (which periodically flushes incremental data to the external stage) and one on the Lake side (which periodically scans the external stage for new data). Because these two intervals do not coordinate, the effective end-to-end latency is higher than either interval alone.

In event-driven mode, the Changefeed still flushes data to the external stage on its configured interval, but each flush also triggers an **S3 event notification** to an SQS queue. Lake subscribes to this queue and loads new data as soon as the notification arrives, eliminating the additional latency caused by its own polling interval.

> **Tradeoff:** In event-driven mode, Lake consumes data more aggressively, which keeps the warehouse in an **active** state more often. This increases the warehouse hosting cost.

## Does a data pipeline incur additional TiDB Cloud Lake charges?

A data pipeline does not introduce a separate billing category. The cost comes from the existing components involved in the pipeline:

1. **Export** (one-time): billed for the full snapshot export.
2. **Changefeed** (ongoing): billed for continuously hourly.
3. **TiDB Cloud Lake** (ongoing): billed for data storage and warehouse compute. For details, see [TiDB Cloud Lake Pricing & Billing](https://docs.pingcap.com/tidbcloudlake/pricing-billing/).
