---
title: Common misuses of TiDB Lightning
category: reference
---

# Common misuses of TiDB Lightning

This article introduces common error scenarios in using [TiDB Lightning](/v3.0/reference/tools/tidb-lightning/overview.md) and corresponding solutions.

## error：`checksum mismatched remote vs local`

The following error was encountered during data import:

```log
Error: checksum mismatched remote vs local => (checksum: 3828723015727756136 vs 7895534721177712659) (total_kvs: 1221416844 vs 1501500000) (total_bytes:237660308510 vs 292158203078)
```

### Reasons

* TiDB Lightning has been used to import data previously. This means the data was not cleaned in the corresponding [checkpoint](/v3.0/reference/tools/tidb-lightning/checkpoints.md). You can check first launch log in TiDB Lightning to confirm:

    * `[checkpoint] driver = file`. If the log corresponding to TiDB Lightning data import shows `open checkpoint file failed, going to create a new one`, then `checkpoint` is cleaned properly. Otherwise, the remaining data may lead to imported data missing.
    * `[checkpoint] driver = mysql`. You can use TiDB API`curl http://{TiDBIP}:10080/schema/{checkpoint.schema}/{checkpoint.table}` to query the creation time of corresponding `checkpoint table`, and then confirm whether the remaining data is cleaned.

* TiDB Lightning imported conflicting data from data sources.
    * Data in different rows have the same primary key or unique key.

### Solutions

* Delete data from tables with `checksum mismatch` error.

    ```
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

* Find a way to detect whether there is conflict data in the data sources. TiDB Lightning generally processes large amounts of data, so there is no effective conflict detection tool or solution in place.