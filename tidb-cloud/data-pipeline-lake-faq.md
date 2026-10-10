---
title: Data Pipeline FAQ
summary: Frequently asked questions about TiDB Cloud Data Pipeline to TiDB Cloud Lake, including external stages, event-driven ingestion, and billing.
---

# Data Pipeline FAQ

This document answers common questions about TiDB Cloud Data Pipeline to TiDB Cloud Lake.

## Why does a data pipeline require an external stage?

The external stage is required for reliability. Because both sides work through the stage instead of transferring data directly, the write rate on the TiDB Cloud side is decoupled from the consumption rate of TiDB Cloud Lake:

- Under high write throughput, change data is durably stored in the stage and remains available for TiDB Cloud Lake to load, even if loading into TiDB Cloud Lake is delayed or interrupted.
- The stage buffers the write load and prevents temporary differences between the data production and ingestion rates from directly affecting TiDB Cloud Lake ingestion.
- The ingestion frequency on the TiDB Cloud Lake side is decoupled from the write rate, which gives you a way to control the cost on the TiDB Cloud Lake side.

## Do I need to enable event-driven ingestion with an SQS queue?

Enable event-driven ingestion when you need **lower data latency** than the default polling mode provides.

In the default mode, the Data Pipeline relies on the interval at which the changefeed flushes incremental data to the external stage and the interval at which TiDB Cloud Lake scans the stage for new data. For {{{ .premium }}} and {{{ .byoc }}}, the configured **Sync Interval** is the end-to-end latency target across these stages.

In event-driven mode, the changefeed still flushes data to the external stage on its configured interval, but each flush also triggers an **S3 event notification** to an SQS queue. The SQS notification enables TiDB Cloud Lake to detect new data sooner instead of waiting for the next scheduled scan.

**Tradeoff:** In event-driven mode, TiDB Cloud Lake can ingest new data more frequently, which can keep the warehouse in an **active** state for longer. This increases the warehouse hosting cost.

## Does a data pipeline incur additional TiDB Cloud Lake charges?

A data pipeline does not introduce a separate billing category. The cost comes from the existing components involved in the pipeline:

- **Export** (one-time): billed for the full snapshot export.
- **Changefeed** (ongoing): if incremental replication is enabled, billed for the changefeed resources used for continuous replication.
- **TiDB Cloud Lake** (ongoing): billed for data storage and warehouse compute. For details, see [TiDB Cloud Lake Pricing & Billing](https://docs.pingcap.com/tidbcloudlake/pricing-billing/).
