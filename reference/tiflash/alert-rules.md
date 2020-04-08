---
title: TiFlash Alert Rules
summary: Learn the alert rules of the TiFlash cluster.
category: reference
---

# TiFlash Alert Rules

This documents introduces the alert rules of the TiFlash cluster.

## `TiFlash_schema_error`

- Alert rule:

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

- Rule description:

    You can get an alert when the schema apply error occurs.

- How to handle:

    The error might be caused by the logical problem. Get in touch with the TiFlash R&D.

## `TiFlash_schema_apply_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

- Rule description:

    You can get an alert when the probability that the apply duration exceeds 20 seconds is over 99%.

- How to handle:

    It might be caused by the internal problems of the TiFlash TMT engine. Get in touch with the TiFlash R&D.

## `TiFlash_raft_read_index_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

- Rule description:

    You can get an alert when the probability that the read index duration exceeds 3 seconds is over 99%.

    > **Note:**
    >
    > `read index` is the kvproto request sent to the TiKV leader. TiKV region retries, busy Store, or network problems might lead to long request time of read index.

- How to handle:

    The frequent retries might be caused by frequent TiKV cluster split events or frequent TiKV cluster migrations. You can check the TiKV cluster status to identify the retry reason.

## `TiFlash_raft_wait_index_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

- Rule description:

    You can get an alert when the probability that the wait time for Region Raft Index in TiFlash exceeds 2 seconds is over 99%.

- How to handle:

    It might be caused by communications problems between TiKV and Proxy. Get in touch with the TiFlash R&D.
