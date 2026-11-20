---
title: TiFlash Data Validation
summary: Learn the data validation mechanism and tools for TiFlash.
---

# TiFlash Data validation

This document introduces the data validation mechanism and tools for TiFlash.

Data corruptions are usually caused by serious hardware failures. In such cases, even if you attempt to manually recover data, your data become less reliable.

To ensure data integrity, by default, TiFlash performs basic data validation on data files, using the `City128` algorithm. In the event of any data validation failure, TiFlash immediately reports an error and exits, avoiding secondary disasters caused by inconsistent data. At this time, you need to manually intervene and replicate the data again before you can restore the TiFlash node.

Starting from v5.4.0, TiFlash introduces more advanced data validation features. TiFlash uses the `XXH3` algorithm by default and allows you to customize the validation frame and algorithm.

## Validation mechanism

The DeltaTree File (DTFile) is the storage file that persists TiFlash data on disk. The TiFlash data validation mechanism is based on DTFile and currently has three versions:

| Data validation mechanism version | State | Validation mechanism | Notes |
| :-- | :-- | :-- |:-- |
| V1 | Deprecated | Hashes are embedded in data files. | |
| V2 | Default validation mechanism for versions < v6.0.0 | Hashes are embedded in data files. | Compared with V1, V2 adds statistics of column data. |
| V3 | Default validation mechanism for versions >= v6.0.0 | Contains metadata, records data validation information, and supports multiple hash algorithms. | Introduced in v5.4.0. |

> **Note:**
>
> V1, V2, and V3 in the preceding table refer to the versions of the validation mechanism that TiFlash uses to validate DTFile data. They are not the values of the DTFile storage format setting [`storage.format_version`](/tiflash/tiflash-configuration.md#format_version).

DTFile is stored in the `stable` folder in the data file directory. All formats currently enabled are in folder format, which means the data is stored in multiple files under a folder with a name like `dmf_<file id>`.

### Use data validation

TiFlash supports both automatic and manual data validation:

* Automatic data validation:

    For DTFiles with different [`storage.format_version`](/tiflash/tiflash-configuration.md#format_version) values, TiFlash might use different versions of the data validation mechanism:

    - For DTFiles with `storage.format_version` set to `2`, TiFlash uses the V2 validation mechanism. Before TiFlash v6.0.0, the default value of `storage.format_version` was `2`, so TiFlash used the V2 validation mechanism by default.
    - For DTFiles with `storage.format_version` set to `3` or later, TiFlash uses the V3 validation mechanism. Since TiFlash v6.0.0, the default value of `storage.format_version` has been `3` or later, so TiFlash uses the V3 validation mechanism by default.
    - To view the current defaults and value options of `storage.format_version`, refer to [TiFlash configuration file](/tiflash/tiflash-configuration.md#format_version). The default configuration is verified by tests and is recommended.
* Manual data validation. Refer to [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect).

> **Warning:**
>
> After you enable the V3 validation mechanism, the newly generated DTFile cannot be directly read by TiFlash earlier than v5.4.0. Since v5.4.0, TiFlash supports both the V2 and V3 validation mechanisms and does not actively upgrade or downgrade versions. If you need to upgrade to a new version or roll back to an earlier version, you need to manually [switch versions](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

### Validation tool

In addition to automatic data validation performed when TiFlash reads data, a tool for manually checking data integrity is introduced in v5.4.0. For details, refer to [DTTool](/tiflash/tiflash-command-line-flags.md#dttool-inspect).
