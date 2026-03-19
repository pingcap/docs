---
title: Stage Overview
summary: A stage is a virtual location where data files reside. Files in a stage can be queried directly or loaded into a table. Alternatively, you can unload data from a table into a stage as a file.
---

# Stage Overview

In {{{ .lake-short }}}, a stage is a virtual location where data files reside. Files in a stage can be queried directly or loaded into a table. Alternatively, you can unload data from a table into a stage as a file. The beauty of using a stage is that you can access it for data loading and unloading as conveniently as you would with folders on your computer. Just as when you put a file in a folder, you don't necessarily need to know its exact location on your hard disk. When accessing a file in a stage, you only need to specify the stage name and the file name, such as `@mystage/mydatafile.csv`, rather than specifying its location in the bucket of your object storage. Similar to folders on your computer, you can create as many stages as you need in {{{ .lake-short }}}. However, it's important to note that a stage cannot contain another stage. Each stage operates independently and does not encompass other stages.

Utilizing a stage for loading data also improves the efficiency of uploading, managing, and filtering your data files. With [BendSQL](/tidb-cloud-lake/guides/connect-using-bendsql.md), you can easily upload or download files to or from a stage using a single command. When loading data into {{{ .lake-short }}}, you can directly specify a stage in the COPY INTO command, allowing the command to read and even filter data files from that stage. Similarly, when exporting data from {{{ .lake-short }}}, you can dump your data files into a stage.

## Stage Types

Based on the actual storage location and accessibility, stages can be categorized into these types: Internal Stage, External Stage, and User Stage. The following table summarizes the characteristics of different stage types in {{{ .lake-short }}}, including their storage locations, accessibility, and recommended usage scenarios:

|                      | User Stage                         | Internal Stage                                   | External Stage                                                                                                |
|----------------------|------------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Storage Location** | Internal object storage ({{{ .lake-short }}}) | Internal object storage ({{{ .lake-short }}})               | External object storage (e.g., S3, Azure)                                                                     |
| **Creation Method**  | Automatically created              | Manually created via: `CREATE STAGE stage_name;` | Manually created via: `CREATE STAGE stage_name` `'s3://bucket/prefix/'` `CONNECTION=(endpoint_url='x', ...);` |
| **Access Control**   | Only accessible by the user        | Can be shared with other users or roles          | Can be shared with other users or roles                                                                       |
| **Drop Stage**       | Not allowed                        | Deletes the stage and clears files in it         | Deletes only the stage; files in the external location are retained                                           |
| **File Upload**      | Must upload files to {{{ .lake-short }}}      | Must upload files to {{{ .lake-short }}}                    | No upload needed; used to read or unload data from/to external storage                                        |
| **Usage Scenario**   | Personal/private data              | Team/shared data                                 | External data integration or unloading                                                                        |
| **Path Format**      | `@~/`                              | `@stage_name/`                                   | `@stage_name/`                                                                                                |

### Internal Stage

Files in an internal stage are actually stored in the object storage where {{{ .lake-short }}} resides. An internal stage is accessible to all users within your organization, allowing each user to utilize the stage for their data loading or export tasks. Similar to creating a folder, specifying a name is necessary when creating a stage. Below is an example of creating an internal stage with the [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) command:

```sql
-- Create an internal stage named my_internal_stage
CREATE STAGE my_internal_stage;
```

### External Stage

An external stage enables you to specify an object storage location outside of where {{{ .lake-short }}} resides. For instance, if you have datasets in a Google Cloud Storage container, you can create an external stage using that container. When creating an external stage, you must provide connection information for {{{ .lake-short }}} to connect to the external location.

Below is an example of creating an external stage. Let's say you have datasets in an Amazon S3 bucket named `databend-doc`:

![alt text](/media/tidb-cloud-lake/external-stage.png)

You can create an external stage with the [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) command to connect {{{ .lake-short }}} to that bucket:

```sql
-- Create an external stage named my_external_stage
CREATE STAGE my_external_stage
    URL = 's3://databend-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<YOUR-KEY-ID>',
        SECRET_ACCESS_KEY = '<YOUR-SECRET-KEY>'
    );
```

Once the external stage is created, you can access the datasets from {{{ .lake-short }}}. For example, to list the files:

```sql
LIST @my_external_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │                 md5                │         last_modified         │      creator     │
├───────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ Inventory.csv │  57585 │ "0cd02fb636a22ba9f4ae4d24555a7d68" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
│ Products.csv  │  42987 │ "570e5cbf6a4b6e7e9a258094192f4784" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Please note that the external storage must be one of the object storage solutions supported by {{{ .lake-short }}}. The [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) command page provides examples on how to specify connection information for commonly used object storage solutions.

### User Stage

The user stage can be considered a special type of internal stage: Files in the user stage are stored in the object storage where {{{ .lake-short }}} resides but cannot be accessed by other users. Each user has their own user stage out-of-the-box, and you do not need to create or name your user stage before use. Additionally, you cannot remove your user stage.

The user stage can serve as a convenient repository for your data files that do not need to be shared with others. To access your user stage, use `@~`. For example, to list all the files in your stage:

```sql
LIST @~;
```

## Managing Stages

{{{ .lake-short }}} provides a variety of commands to assist you in managing stages and the files staged within them:

| Command                                                      | Description                                                                                                                                                                                                                          | Applies to User Stage | Applies to Internal Stage | Applies to External Stage |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------- | ------------------------- |
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | Creates an internal or external stage.                                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md)     | Removes an internal or external stage.                                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md)     | Shows the properties of an internal or external stage.                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [LIST](/tidb-cloud-lake/sql/list-stage-files.md)           | Returns a list of the staged files in a stage. Alternatively, the table function [LIST_STAGE](/tidb-cloud-lake/sql/list-stage.md) offers similar functionality with added flexibility to obtain specific file information | Yes                   | Yes                       | Yes                       |
| [REMOVE](/tidb-cloud-lake/sql/remove-stage-files.md)       | Removes staged files from a stage.                                                                                                                                                                                                   | Yes                   | Yes                       | Yes                       |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md)   | Returns a list of the created internal and external stages.                                                                                                                                                                          | No                    | Yes                       | Yes                       |
