---
title: TiDB Serverless Export (Beta)
summary: Learn how to export from TiDB Serverless.
---

# TiDB Serverless Export (Beta)

TiDB Serverless Export (Beta) is a service that allows you to export data from a TiDB Serverless cluster to local or an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

You can also export data with `MySQL shell`, `TiDB Dumpling`, or other tools. However, TiDB Serverless Export provides a more convenient and efficient way to export data from a TiDB Serverless cluster. It brings the following benefits:

- Convenience: Export service provides a simple and easy-to-use way to export data from a TiDB Serverless cluster. You don't need additional tools or resources.
- Isolation: Export service uses separate computing resources, which is isolated from the computing resources used by your online services
- Consistency: Export service ensures the consistency of the exported data without locking, which will not affect your online services.

## Features

- Supports exporting data to local and [Amazon S3](https://aws.amazon.com/s3/). Please Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) if your want to export to other storage services.
- Support exporting a specific database or table.
- Support exporting as CSV or SQL format.

## Export to local

You can only export one table at a time when you export data to local. The exported data will be saved in the stashing area and expired after two days, please download the data in time.

> **Note:**
>
> We recommend you export to S3 or other supported storage services if you want to export a large amount of data.

<SimpleTab>

<div label="Export With CLI">


1. Export a specific table from a TiDB Serverless cluster to local.

   ```sh
   ticloud serverless export create -c <cluster-id> --databsae <database> --table <table>
   ```

2. Download the exported data after the export is succeeded.

   ```sh
   ticloud serverless export download -c <cluster-id> -e <export-id>
   ```

</div>

<div label="Export On Console">

Not supported yet.

</div>

</SimpleTab>

## Export to S3

You can export data directly to your own S3 bucket with the credentials.

<SimpleTab>

<div label="Export With CLI">

Export all data from a TiDB Serverless cluster to S3.

```sh
ticloud serverless export create -c <cluster-id> --bucket-uri <bucket-uri> --access-key-id <access-key-id> --secret-access-key <secret-access-key>
```

</div>

<div label="Export On Console">

Not supported yet.

</div>

</SimpleTab>

## Pricing

You will only be charged for a successful or canceled export.

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process.