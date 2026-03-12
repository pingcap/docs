---
title: Data Recovery
---
import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='BendSave'/>

This topic explains how to back up and restore data in Databend.

## Time Travel: Easy Access to Past Data

With Databend Time Travel, you can revisit and retrieve data from the past, even if it's been altered or removed. It's perfect for:

- **Getting Back Deleted Data:** Helps you get back important things like tables, databases that were deleted, whether by accident or on purpose.

- **Copying and Saving Past Data:** Lets you copy and save important data from earlier times.

- **Looking at Past Data Use:** Makes it easier to see how data was used or changed at certain times.

### Main Uses of Time Travel

- **Access Past Data**: Look at data from the past, even if it has been changed or deleted.
- **Recover Lost Data**: Bring back tables and databases that were deleted using the [FLASHBACK TABLE](/sql/sql-commands/ddl/table/flashback-table) command.

### Time Travel SQL Extensions

- **SQL Extensions for Time Travel:** Use special SQL clauses like [`AT`](/sql/sql-commands/query-syntax/query-at) in SELECT statements and CREATE commands to specify the exact point in history you want to access.
- **Revive Deleted Data:** Use the `UNDROP` command for tables, databases.

### Setting the Data Retention Period

- **Personal Edition**: Choose between no retention (0 days) or the default of **1 day**.
- **Business Edition and Higher**:
  - For temporary data: Set to 0 or the default of **1 day**.
  - For permanent data: Choose any period from **0 to 90 days**.

:::info Note

Setting a retention period of 0 days means Time Travel won't be available for that data.

:::

### Adjusting Data Retention Time

Change the data keeping time with the `DATA_RETENTION_TIME_IN_DAYS` setting, which is usually 1 day. This decides how long to keep old data.

## Fail-safe: Extra Protection for Your Data

Fail-safe in Databend Cloud is an additional safety feature, different from Time Travel. It's designed to protect your data in case of system issues or security incidents.

### How Fail-safe Works

Fail-safe offers a fixed 7-day recovery window after the Time Travel period ends.

Fail-safe includes:

- **MetaData Recovery:** Uses versioning in the meta-service to recover deleted tables.
- **Data Recovery:** Uses AWS S3's versioning to save data that's been changed or deleted.

:::caution Attention

- Fail-safe is an emergency service, not user-configurable, provided by Databend Cloud.
- It should be used only after other recovery methods don't work.
- Not intended for regular historical data access beyond the Time Travel period.
- For restoring data after big problems, and you can't set it up yourself.
- Recovery times can vary from a few hours to several days, depending on the situation.

:::


## BendSave

BendSave is a command-line tool for backing up and restoring both metadata and actual data files in Databend. It stores backups in S3-compatible object storage, making it ideal for disaster recovery.

### Downloading BendSave

The BendSave binary is distributed as part of the [Databend release packages](https://github.com/databendlabs/databend/releases).

To download:

1. Go to the latest [Databend Releases](https://github.com/databendlabs/databend/releases).

2. Select the release that matches your currently running `databend-query` version.

3. Download and extract the release package.

4. Inside the extracted archive, locate the **bin** directory and find the **databend-bendsave** binary.

### Command Reference

To back up the metadata of a Databend cluster:

```bash
databend-bendsave backup \
  --from <query-config-path> \
  --to <backup-destination>
```

| Parameter | Description                                                             |
|-----------|-------------------------------------------------------------------------|
| from      | Path to the  `databend-query.toml` configuration file.                  |
| to        | Backup destination, e.g.,`s3://backup?endpoint=http://127.0.0.1:9900&access_key_id=xxx&secret_access_key=xxx`.<br/>- It is recommended to use environment variables such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to provide credentials.|

To restore the metadata to a Databend cluster:

```bash
databend-bendsave restore \
  --from <backup-source> \
  --to-query <query-config-path> \
  --to-meta <meta-config-path> \
  --confirm
```

| Parameter | Description                                                           |
|-----------|-----------------------------------------------------------------------|
| from      | Backup source path.                                                   |
| to-query  | Path to the restored `databend-query.toml` configuration file.        |
| to-meta   | Path to the restored `databend-meta.toml` configuration file.         |
| confirm   | Required flag to confirm restoration and avoid accidental overwrites. |

#### Examples

```bash
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

# Backup
./databend-bendsave backup \
  --from ../configs/databend-query.toml \
  --to 's3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1'

# Restore
./databend-bendsave restore \
  --from "s3://backupbucket?endpoint=http://127.0.0.1:9000/&region=us-east-1" \
  --to-query ../configs/databend-query.toml \
  --to-meta ../configs/databend-meta.toml \
  --confirm
```

### Tutorials

- [Backing Up and Restoring Data with BendSave](/tutorials/operate-and-recover/bendsave)
