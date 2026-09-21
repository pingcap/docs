---
title: Stage 概述
summary: stage 是一个用于存放数据文件的虚拟位置。stage 中的文件可以直接查询，也可以加载到表中。或者，你也可以将表中的数据以文件形式卸载到 stage 中。
---

# Stage 概述

在 {{{ .lake }}} 中，stage 是一个用于存放数据文件的虚拟位置。stage 中的文件可以直接查询，也可以加载到表中。或者，你也可以将表中的数据以文件形式卸载到 stage 中。使用 stage 的优势在于，你可以像访问计算机上的文件夹一样方便地对其进行数据加载和卸载。就像把文件放进文件夹时，你不一定需要知道它在硬盘上的确切位置一样，访问 stage 中的文件时，你只需要指定 stage 名称和文件名，例如 `@mystage/mydatafile.csv`，而不需要指定它在对象存储 bucket 中的具体位置。与计算机上的文件夹类似，你可以在 {{{ .lake }}} 中根据需要创建任意数量的 stage。不过需要注意的是，一个 stage 不能包含另一个 stage。每个 stage 都是独立运行的，不会包含其他 stage。

使用 stage 进行数据加载还可以提升数据文件上传、管理和筛选的效率。借助 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md)，你可以通过一条命令轻松地将文件上传到 stage，或从 stage 下载文件。将数据加载到 {{{ .lake }}} 时，你可以在 COPY INTO 命令中直接指定 stage，使该命令能够从该 stage 中读取数据文件，甚至对其进行筛选。同样地，从 {{{ .lake }}} 导出数据时，你也可以将数据文件转储到 stage 中。

## stage 类型 {#stage-types}

根据实际存储位置和可访问性，stage 可分为以下几种类型：Internal Stage、External Stage 和 User Stage。下表总结了 {{{ .lake }}} 中不同 stage 类型的特征，包括其存储位置、可访问性以及推荐使用场景：

|                      | 用户 Stage                         | 内部 Stage                                   | 外部 Stage                                                                                                |
|----------------------|------------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **存储位置** | 内部对象存储 ({{{ .lake }}}) | 内部对象存储 ({{{ .lake }}})               | 外部对象存储（例如 S3、Azure）                                                                     |
| **创建方法**  | 自动创建              | 通过以下方式手动创建：`CREATE STAGE stage_name;` | 通过以下方式手动创建：`CREATE STAGE stage_name` `'s3://bucket/prefix/'` `CONNECTION=(endpoint_url='x', ...);` |
| **访问控制**   | 仅用户本人可访问        | 可与其他用户或角色共享          | 可与其他用户或角色共享                                                                       |
| **删除 Stage**       | 不允许                        | 删除 stage 并清空其中的文件         | 仅删除 stage；外部位置中的文件会被保留                                           |
| **文件上传**      | 必须将文件上传到 {{{ .lake }}}      | 必须将文件上传到 {{{ .lake }}}                    | 无需上传；用于从外部存储读取数据或将数据卸载到外部存储                                        |
| **使用场景**   | 个人/私有数据              | 团队/共享数据                                 | 外部数据集成或数据卸载                                                                        |
| **路径格式**      | `@~/`                              | `@stage_name/`                                   | `@stage_name/`                                                                                                |

### Internal Stage {#internal-stage}

Internal Stage 中的文件实际上存储在 {{{ .lake }}} 所在的对象存储中。Internal Stage 可供你所在组织内的所有用户访问，因此每个用户都可以将该 stage 用于数据加载或导出任务。与创建文件夹类似，创建 stage 时需要指定名称。下面是使用 [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) 命令创建 Internal Stage 的示例：

```sql
-- Create an internal stage named my_internal_stage
CREATE STAGE my_internal_stage;
```

### External Stage {#external-stage}

External Stage 允许你指定一个位于 {{{ .lake }}} 所在位置之外的对象存储位置。例如，如果你的数据集位于 Google Cloud Storage 容器中，你可以基于该容器创建一个 External Stage。创建 External Stage 时，你必须提供连接信息，以便 {{{ .lake }}} 连接到该外部位置。

下面是创建 External Stage 的示例。假设你的数据集位于名为 `lake-doc` 的 Amazon S3 bucket 中。

你可以使用 [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) 命令创建一个 External Stage，将 {{{ .lake }}} 连接到该 bucket：

```sql
-- Create an external stage named my_external_stage
CREATE STAGE my_external_stage
    URL = 's3://lake-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<YOUR-KEY-ID>',
        SECRET_ACCESS_KEY = '<YOUR-SECRET-KEY>'
    );
```

创建 External Stage 后，你就可以从 {{{ .lake }}} 访问这些数据集。例如，列出文件：

```sql
LIST @my_external_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │                 md5                │         last_modified         │      creator     │
├───────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ Inventory.csv │  57585 │ "0cd02fb636a22ba9f4ae4d24555a7d68" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
│ Products.csv  │  42987 │ "570e5cbf6a4b6e7e9a258094192f4784" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

请注意，外部存储必须是 {{{ .lake }}} 支持的对象存储解决方案之一。[CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) 命令页面提供了如何为常用对象存储解决方案指定连接信息的示例。

### User Stage {#user-stage}

User Stage 可以视为一种特殊类型的 Internal Stage：User Stage 中的文件存储在 {{{ .lake }}} 所在的对象存储中，但其他用户无法访问。每个用户开箱即有自己的 User Stage，使用前无需创建或命名。此外，你也不能删除自己的 User Stage。

对于不需要与他人共享的数据文件，User Stage 可以作为一个方便的仓库。要访问你的 User Stage，请使用 `@~`。例如，列出你的 stage 中的所有文件：

```sql
LIST @~;
```

## 使用 PATTERN 过滤 stage 中的文件 {#filtering-staged-files-with-pattern}

读取、列出、删除或检查 stage 中文件的命令和函数都可以使用 `PATTERN` 通过正则表达式筛选文件。对于 stage 位置，`PATTERN` 匹配的是 `@<stage_name>[/<path>]` 之后的文件路径部分，而不是完整的 stage URI。

> **Note:**
>
> 文件路径中的 Glob 模式（例如 `ontime_200{6,7,8}.csv` 或 `ontime_200[6-8].csv`）仅支持基于 HTTP 的外部位置。S3 和其他对象存储位置不支持文件路径中的 glob 展开——请改用带正则表达式的 `PATTERN`。

例如，对于 `@sales_stage/raw/`，stage 文件 `@sales_stage/raw/year=2025/month=01/sales_20250101.parquet` 会按 `year=2025/month=01/sales_20250101.parquet` 进行匹配：

```sql
LIST @sales_stage/raw/ PATTERN = 'year=2025/month=01/.*[.]parquet';
```

要匹配某个 stage 路径下所有的 `.log` 文件，可以使用如下正则表达式：

```sql
LIST @my_stage PATTERN = '.*[.]log';
```

## 管理 stage {#managing-stages}

{{{ .lake }}} 提供了多种命令，帮助你管理 stage 及其中暂存的文件：

| 命令                                                      | 描述                                                                                                                                                                                                                          | 适用于 User Stage | 适用于 Internal Stage | 适用于 External Stage |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------- | ------------------------- |
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | 创建 Internal Stage 或 External Stage。                                                                                                                                                                                               | 否                    | 是                       | 是                       |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md)     | 删除 Internal Stage 或 External Stage。                                                                                                                                                                                               | 否                    | 是                       | 是                       |
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md)     | 显示 Internal Stage 或 External Stage 的属性。                                                                                                                                                                               | 否                    | 是                       | 是                       |
| [LIST](/tidb-cloud-lake/sql/list-stage-files.md)           | 返回 stage 中暂存文件的列表。或者，表函数 [LIST_STAGE](/tidb-cloud-lake/sql/list-stage.md) 提供了类似功能，并具有更高的灵活性，可用于获取特定文件信息 | 是                   | 是                       | 是                       |
| [REMOVE](/tidb-cloud-lake/sql/remove-stage-files.md)       | 从 stage 中删除暂存文件。                                                                                                                                                                                                   | 是                   | 是                       | 是                       |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md)   | 返回已创建的 Internal Stage 和 External Stage 列表。                                                                                                                                                                          | 否                    | 是                       | 是                       |