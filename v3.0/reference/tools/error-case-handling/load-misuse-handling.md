---
title: Common misuses during full data import
category: reference
---

# Common misuses during full data import

This article introduces the common error scenarios caused by using [Loader](/v3.0/reference/tools/loader.md) or [TiDB Data Migration](/dev/reference/tools/data-migration/overview.md) (DM) to import full data, the causes and solutions of which are also provided.

## Error: ``Try adjusting the `max_allowed_packet` variable``

The following error was encountered during full data import.

```
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

### Reasons

* Both MySQL client and MySQL/TiDB Server have `max_allowed_packet` quotas. If any `max_allowed_packet` quota is violated, the client receives a corresponding error message. Currently, the latest version of Syncer, Loader, DM and TiDB Server all have a default `max_allowed_packet` quota of `64M`.
    * Please use the latest version, or the latest stable version of the tool. [Click here to download](/dev/reference/tools/download.md).
* Full data import processing module in Loader or DM Loader do not support the segementation of  `dump sqls` files. It is because Mydumper uses the simplest code to implement, as stated in the comment `* Poor man's data dump code *`. If you segment files in Loader or DM, you will need a complete parser based on `TiDB parser` to handle data segmentation, which will cause the following problems:
    * High workload
    * High complexity with poor correctness
    * Performance drop

### Solutions

* For the above reasons, it is recommended to execute `-s, --statement-size` statement which Mydumper offered to control the size of `Insert Statement`: `Attempted size of INSERT statement in bytes, default 1000000`.

    According to the default configuration of `--statement-size`, the size of `Insert Statement` is as close as `1M`. The default configuration ensures this problem will not occur in most cases.

    Sometimes the following `WARN` log will appear during dump to indicate that the table of dump may be a wide table. The `WARN` log itself will not affect dump process.

    ```
    Row bigger than statement_size for xxx
    ```

* If a single row of a wide table exceeds 64M, the following two configurations need to be modified and enabled.
    * Execute `set @@global.max_allowed_packet=134217728` (`134217728 = 128M`) in TiDB Server.
    * Add statements like `max-allowed-packet=128M` according to the configurations of Loader or db in DM task, and then restart the progress or task.