---
title: Manage Data Pipeline
summary: Learn how to create and manage a data pipeline that replicates full and incremental data from TiDB Cloud to TiDB Cloud Lake.
---

# Manage Data Pipeline

TiDB Cloud Data Pipeline replicates full data and incremental changes from your TiDB Cloud instance to TiDB Cloud Lake, without requiring a third-party ETL tool. It first exports a full snapshot of the selected source data, and then continuously replicates row changes so that the data in TiDB Cloud Lake stays up to date.

You can use Data Pipeline for the following scenarios:

- **One-time data loading**: export a full snapshot to TiDB Cloud Lake for initial data loading or migration.
- **Continuous data synchronization**: keep TiDB Cloud Lake in sync with your TiDB Cloud instance for analytics and reporting workloads.

## How it works

A data pipeline with continuous replication operates in two phases:

1. **Full snapshot export**: a one-time export of the selected source tables to TiDB Cloud Lake.
2. **Incremental replication**: continuous capture and replication of row changes (inserts, updates, and deletes) so that TiDB Cloud Lake stays current with the source.

You can also configure a pipeline to export only a full snapshot without ongoing replication.

An **external stage** (Amazon S3 or Alibaba Cloud OSS) is used as the intermediate storage between your TiDB Cloud instance and TiDB Cloud Lake. TiDB Cloud writes exported snapshots and captured row changes to the stage, and TiDB Cloud Lake loads data from the stage into the target warehouse. This decouples the write rate from the consumption rate, improving reliability and giving you control over cost and latency.

For more information, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).

## Availability

| Plan | Status |
| ---- | ------ |
| {{{ .premium }}} | Data Pipeline is available in the [TiDB Cloud console](https://tidbcloud.com) in private preview, and it is available upon request. |
| {{{ .dedicated }}} | Data Pipeline is not available in the TiDB Cloud console yet, and manual setup is required. |
| {{{ .essential }}} | Data Pipeline is not available in the TiDB Cloud console yet, and manual setup is required. |

> **Note:**
>
> Data Pipeline currently supports TiDB Cloud Lake as the destination. More destinations will be supported in the future to enable a broader range of data movement and migration scenarios within TiDB Cloud.

## Create a data pipeline

> **Note:**
>
> TiDB Cloud Premium provides the Data Pipeline feature in the TiDB Cloud console. For TiDB Cloud Dedicated and TiDB Cloud Essential, you set up data replication to TiDB Cloud Lake manually.

Refer to the guide for your plan:

- [TiDB Cloud Premium: Set Up a Data Pipeline to TiDB Cloud Lake](/tidb-cloud/data-pipeline-premium-sink-to-lake.md)
- [TiDB Cloud Dedicated: Manually Set Up to Replicate Data to TiDB Cloud Lake](/tidb-cloud/data-pipeline-dedicated-sink-to-lake.md)
- [TiDB Cloud Essential: Manually Set Up to Replicate Data to TiDB Cloud Lake](/tidb-cloud/data-pipeline-essential-sink-to-lake.md)

## View the Data Pipeline page

> **Note:**
>
> The **Data Pipeline** page and the management operations in this section are available for {{{ .premium }}} only. For {{{ .dedicated }}} and {{{ .essential }}}, you configure and maintain the data pipeline manually.

To view and manage your data pipelines, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Data Pipeline** in the left navigation pane. The **Data Pipeline** page is displayed.

On the **Data Pipeline** page, you can create a data pipeline, view a list of existing data pipelines, and operate existing data pipelines, such as pausing, resuming, editing, and deleting a pipeline.

## Manage a data pipeline

### Pause and resume a data pipeline

- **Pause**: stops data replication and marks the pipeline as `Paused`. No data is lost, and the replication progress is preserved. A pipeline cannot be paused while it is being created or while the full snapshot is being exported.
- **Resume**: continues replication from where it was paused, including ingestion into TiDB Cloud Lake.

To pause and resume a data pipeline, navigate to the **Data Pipeline** page of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Pause** or **Resume**.

### Edit a data pipeline

To edit a data pipeline, navigate to the **Data Pipeline** page of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Edit**.

Editing is disabled while a data pipeline is `Running`. Pause the pipeline first, then edit it, and resume it afterwards to apply the changes.

The destination type and the sync mode cannot be changed after the pipeline is created.

> **Note:**
>
> Changing the table filter rules only affects incremental data going forward:
>
> - Tables that are excluded by the new rules no longer receive incremental data. Data that has already been written is kept.
> - Tables that are added by the new rules receive incremental data only. No historical data is backfilled for them.

### Delete a data pipeline

To delete a data pipeline, take the following steps:

1. Navigate to the **Data Pipeline** page of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Delete**.
2. Read the warning and confirm the operation. Deleting a data pipeline:

    - Immediately stops all data replication.
    - Attempts to remove the TiDB Cloud Lake data source and integration task associated with the pipeline. If the removal fails, these resources might remain and require manual cleanup.
    - **Does not** delete the data already written to TiDB Cloud Lake.
    - **Does not** delete the target databases or tables in the warehouse.

This action cannot be undone.

## See also

- For frequently asked questions about Data Pipeline, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).
- For details on DDL, DML, and column type support, see [Data Pipeline SQL Compatibility for TiDB Cloud Lake](/tidb-cloud/data-pipeline-lake-sql-compatibility.md).
