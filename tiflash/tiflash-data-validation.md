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

The validation mechanism builds upon the DeltaTree File (DTFile). The numeric values of `storage.format_version` are TiFlash storage format identifiers. They are not the same as the DTFile validation generations described in this document. The DTFile validation mechanism has three generations:

| Version | State | Validation mechanism | Notes |
| :-- | :-- | :-- |:-- |
| V1 | Deprecated | Hashes are embedded in data files. | |
| V2 | Default for versions < v6.0.0 | Hashes are embedded in data files. | Compared to V1, V2 adds statistics of column data. |
| V3 | Default for versions >= v6.0.0 | V3 contains metadata and token data checksum, and supports multiple hash algorithms. | New in v5.4.0. |

In current releases, `storage.format_version` supports values from `2` to `7`. Different `storage.format_version` values can share the same DTFile validation generation while changing other TiFlash storage components. For the current value options and defaults of `storage.format_version`, see [TiFlash configuration file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file).

DTFile is stored in the `stable` folder in the data file directory. All formats currently enabled are in folder format, which means the data is stored in multiple files under a folder with a name like `dmf_<file id>`.

### Use data validation

TiFlash supports both automatic and manual data validation:

* Automatic data validation:
    * The DTFile validation generations on this page are not a simple count of `storage.format_version` values.
    * To view the current defaults and value options of `storage.format_version`, refer to [TiFlash configuration file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). However, the default configuration is verified by tests and therefore recommended.
* Manual data validation. Refer to [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect).

> **Warning:**
>
> After you enable the V3 validation mechanism, the newly generated DTFile cannot be directly read by TiFlash earlier than v5.4.0. Since v5.4.0, TiFlash supports both V2 and V3 and does not actively upgrade or downgrade versions. If you need to upgrade or downgrade versions for existing files, you need to manually [switch versions](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

### Validation tool

In addition to automatic data validation performed when TiFlash reads data, a tool for manually checking data integrity is introduced in v5.4.0. For details, refer to [DTTool](/tiflash/tiflash-command-line-flags.md#dttool-inspect).
