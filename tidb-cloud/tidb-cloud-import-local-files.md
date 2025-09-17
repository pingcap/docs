---
title: 将本地文件导入 TiDB Cloud Starter 或 Essential
summary: 了解如何将本地文件导入 TiDB Cloud Starter 或 TiDB Cloud Essential。
---

# 将本地文件导入 TiDB Cloud Starter 或 Essential

你可以直接将本地文件导入 TiDB Cloud Starter 或 TiDB Cloud Essential。只需几步简单操作即可完成任务配置，你的本地 CSV 数据就会被快速导入到 TiDB 集群中。使用此方法，无需提供云存储和凭证，整个导入过程快速且流畅。

目前，该方法支持每个任务导入一个 CSV 文件到现有的空表或新建表中。

## 限制

- 目前，TiDB Cloud 仅支持每个任务导入一个大小不超过 250 MiB 的本地 CSV 文件。
- 本地文件导入仅支持 TiDB Cloud Starter 和 TiDB Cloud Essential 集群，不支持 TiDB Cloud Dedicated 集群。
- 你不能同时运行多个导入任务。

## 导入本地文件

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并导航到项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 在 **Import** 页面，你可以直接将本地文件拖拽到上传区域，或点击 **Upload a local file** 选择并上传目标本地文件。请注意，每个任务只能上传一个小于 250 MiB 的 CSV 文件。如果你的本地文件大于 250 MiB，请参见 [如何导入大于 250 MiB 的本地文件？](#how-to-import-a-local-file-larger-than-250-mib)。

3. 在 **Destination** 部分，选择目标数据库和目标表，或直接输入名称以创建新数据库或新表。名称只能包含 Unicode BMP（基本多文种平面）中的字符，不能包含空字符 `\u0000` 和空白字符，且长度最多为 64 个字符。点击 **Define Table**，会显示 **Table Definition** 部分。

4. 检查数据表。

    你可以看到可配置的数据表列列表。每一行显示 TiDB Cloud 推断出的表列名、推断出的表列类型，以及来自 CSV 文件的预览数据。

    - 如果你将数据导入 TiDB Cloud 中的现有表，列列表会从表定义中提取，预览数据会按列名映射到对应的列。
    - 如果你需要新建表，列列表会从 CSV 文件中提取，列类型由 TiDB Cloud 推断。例如，如果预览数据全为整数，则推断的列类型为整数。

5. 配置列名和数据类型。

    如果 CSV 文件的第一行记录了列名，请确保已勾选 **Use first row as column name**，该选项默认勾选。

    如果 CSV 文件没有列名行，请不要勾选 **Use first row as column name**。此时：

    - 如果目标表已存在，CSV 文件中的列会按顺序导入到目标表。多余的列会被截断，缺失的列会用默认值填充。
    - 如果需要 TiDB Cloud 创建目标表，请为每一列输入名称。列名需满足以下要求：

        * 名称只能由 Unicode BMP 字符组成，不能包含空字符 `\u0000` 和空白字符。
        * 名称长度必须小于 65 个字符。

        你也可以根据需要更改数据类型。

    > **Note:**
    >
    > 当你将 CSV 文件导入 TiDB Cloud 中的现有表且目标表的列多于源文件时，额外的列会根据不同情况进行处理：
    > - 如果额外的列不是主键或唯一键，不会报错，这些额外的列会被填充为其 [默认值](/data-type-default-values.md)。
    > - 如果额外的列是主键或唯一键，且没有 `auto_increment` 或 `auto_random` 属性，则会报错。此时建议选择以下策略之一：
    >   - 提供包含这些主键或唯一键列的源文件。
    >   - 修改目标表的主键和唯一键列，使其与源文件中的现有列匹配。
    >   - 将主键或唯一键列的属性设置为 `auto_increment` 或 `auto_random`。

6. 对于新建的目标表，你可以设置主键。你可以选择某一列作为主键，或选择多列创建复合主键。复合主键会按照你选择列名的顺序组成。

    > **Note:**
    >
    > 表的主键为聚簇索引，创建后无法删除。

7. 如有需要，可编辑 CSV 配置。

   你也可以点击 **Edit CSV configuration**，对反斜杠转义、分隔符和定界符等进行更细致的配置。关于 CSV 配置的更多信息，请参见 [导入数据的 CSV 配置](/tidb-cloud/csv-config-for-import-data.md)。

8. 点击 **Start Import**。

    你可以在 **Import Task Detail** 页面查看导入进度。如果有警告或失败的任务，可以查看详情并进行处理。

9. 导入任务完成后，你可以点击 **Explore your data by SQL Editor**，通过 SQL 查询已导入的数据。关于如何使用 SQL Editor 的更多信息，请参见 [使用 AI 辅助 SQL Editor 探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

10. 在 **Import** 页面，你可以点击 **...** > **View**，在 **Action** 列查看导入任务详情。

## 常见问题

### TiDB Cloud 的 Import 功能是否只能导入指定的部分列？

不能。目前，使用 Import 功能时，只能将 CSV 文件的所有列导入到现有表中。

如果只想导入指定的部分列，可以使用 MySQL 客户端连接 TiDB 集群，然后通过 [`LOAD DATA`](https://docs.pingcap.com/tidb/stable/sql-statement-load-data) 指定要导入的列。例如：

```sql
CREATE TABLE `import_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
LOAD DATA LOCAL INFILE 'load.txt' INTO TABLE import_test FIELDS TERMINATED BY ',' (name, address);
```

如果你使用 `mysql` 并遇到 `ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`，可以在连接字符串中添加 `--local-infile=true`。

### 为什么将数据导入 TiDB Cloud 后，无法查询带有保留关键字的列？

如果列名是 TiDB 的保留 [关键字](/keywords.md)，在查询该列时需要用反引号 `` ` `` 包裹列名。例如，如果列名为 `order`，则需要用 `` `order` `` 进行查询。

### 如何导入大于 250 MiB 的本地文件？

如果文件大于 250 MiB，可以使用 [TiDB Cloud CLI](/tidb-cloud/get-started-with-cli.md) 进行导入。更多信息请参见 [`ticloud serverless import start`](/tidb-cloud/ticloud-import-start.md)。

另外，你也可以使用 `split [-l ${line_count}]` 工具将其拆分为多个小文件（仅适用于 Linux 或 macOS）。例如，运行 `split -l 100000 tidb-01.csv small_files`，即可按行数 100000 拆分名为 `tidb-01.csv` 的文件，拆分后的文件名为 `small_files${suffix}`。然后，你可以将这些小文件逐个导入 TiDB Cloud。

参考如下脚本：

```bash
#!/bin/bash
n=$1
file_path=$2
file_extension="${file_path##*.}"
file_name="${file_path%.*}"
total_lines=$(wc -l < $file_path)
lines_per_file=$(( (total_lines + n - 1) / n ))
split -d -a 1 -l $lines_per_file $file_path $file_name.
for (( i=0; i<$n; i++ ))
do
    mv $file_name.$i $file_name.$i.$file_extension
done
```

你可以输入 `n` 和文件名，然后运行该脚本。脚本会将文件平均分为 `n` 份，并保留原有文件扩展名。例如：

```bash
> sh ./split.sh 3 mytest.customer.csv
> ls -h | grep mytest
mytest.customer.0.csv
mytest.customer.1.csv
mytest.customer.2.csv
mytest.customer.csv
```