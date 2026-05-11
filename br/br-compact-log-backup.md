---
title: Compact Log Backup
summary: Learn how to improve Point-in-time Recovery (PITR) efficiency by compacting log backups into the SST format.
---

# Compact Log Backup

This document describes how to improve the efficiency of point-in-time recovery ([PITR](/glossary.md#point-in-time-recovery-pitr)) by compacting log backups into the [SST](/glossary.md#static-sorted-table--sorted-string-table-sst) format.

## Overview

Traditional log backups store write operations in a highly unstructured manner, which can lead to the following issues:

- **Reduced recovery performance**: unordered data has to be written to the cluster one by one through the Raft protocol.
- **Write amplification**: all writes must be compacted from L0 to the bottommost level by level.
- **Dependency on full backups**: frequent full backups are required to control the amount of recovery data, which can impact application operations.

Starting from v8.5.5 and v9.0.0, the compact log backup feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

- SST files can be quickly imported into the cluster, **improving recovery performance**.
- Redundant data is removed during compaction, **reducing storage space consumption**.
- You can set longer full backup intervals while ensuring the Recovery Time Objective (RTO), **reducing the impact on applications**.

## Limitations

- Compact log backup is not a replacement for full backups. It must be used in conjunction with periodical full backups. To ensure PITR capability, the compacting process retains all MVCC versions. Failing to perform full backups for a long time can lead to excessive storage usage and might cause issues when restoring data later.
- Currently, compacting backups with local encryption enabled is not supported.

## Use compact log backup

Currently, only manual compaction of log backups is supported, and the process is complex. **It is recommended to use the coming TiDB Operator solution for compacting log backups in production environments.**

### Manual compaction

This section describes the steps for manually compacting log backups.

#### Prerequisites

Manual compaction of log backups requires two tools: `tikv-ctl` and `br`.

#### Step 1: Encode storage to Base64

Execute the following encoding command:

```shell
br operator base64ify --storage "s3://your/log/backup/storage/here" --load-creds
```

> **Note:**
>
> - If the `--load-creds` option is included when you execute the preceding command, the encoded Base64 string contains credential information loaded from the current BR environment. Note to ensure proper security and access control.
> - The `--storage` value matches the storage output from the `log status` command of the log backup task.

#### Step 2: Execute log compaction

With the Base64-encoded storage, you can initiate the compaction using `tikv-ctl`. Note that the default log level of `tikv-ctl` is `warning`. Use `--log-level info` to obtain more detailed information:

```shell
tikv-ctl --log-level info compact-log-backup \
    --from "<start-tso>" --until "<end-tso>" \
    -s 'bAsE64==' -N 8
```

Parameter descriptions:

- `-s`: the Base64-encoded storage string obtained earlier.
- `-N`: the maximum number of concurrent log compaction tasks.
- `--from`: the start timestamp for compaction.
- `--until`: the end timestamp for compaction.

The `--from` and `--until` parameters define the time range for the compaction operation. The compaction operation handles all log files containing write operations within the specified time range, so the generated SST files might include data outside this range.

To obtain the timestamp for a specific point in time, execute the following command:

```shell
echo $(( $(date --date '2004-05-06 15:02:01Z' +%s%3N) << 18 ))
```

> **Note:**
>
> If you are a macOS user, you need to install `coreutils` via Homebrew and use `gdate` instead of `date`.
>
> ```shell
> echo $(( $(gdate --date '2004-05-06 15:02:01Z' +%s%3N) << 18 ))
> ```
