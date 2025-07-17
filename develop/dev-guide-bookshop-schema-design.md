---
title: Bookshop 示例应用
summary: Bookshop 是一个在线书店应用，供你购买和评价书籍。你可以通过 TiUP 或 TiDB Cloud 导入表结构和数据。方法 1 使用 TiUP 快速生成并导入示例数据，方法 2 从 Amazon S3 导入数据到 TiDB Cloud。数据库表包括 books、authors、users、ratings、book_authors 和 orders。数据库初始化脚本 `dbinit.sql` 创建了 Bookshop 应用的表结构。
---

# Bookshop 示例应用

Bookshop 是一个虚拟的在线书店应用，你可以在其中购买各种类别的书籍并对已阅读的书籍进行评分。

为了让你在应用开发指南中的阅读更加顺畅，我们基于 [表结构](#description-of-the-tables) 和数据，提供了示例的 SQL 语句。本文件重点介绍导入表结构和数据的方法以及表结构的定义。

## 导入表结构和数据

<CustomContent platform="tidb">

你可以通过 [TiUP](#method-1-via-tiup-demo) 或 [TiDB Cloud 的导入功能](#method-2-via-tidb-cloud-import) 导入 Bookshop 的表结构和数据。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB Cloud，你可以跳过 [Method 1: Via `tiup demo`](#method-1-via-tiup-demo)，直接通过 [TiDB Cloud 的导入功能](#method-2-via-tidb-cloud-import) 导入表结构。

</CustomContent>

### Method 1: Via `tiup demo`

<CustomContent platform="tidb">

如果你的 TiDB 集群是使用 [TiUP](/tiup/tiup-reference.md#tiup-reference) 部署的，或者你可以连接到你的 TiDB 服务器，你可以通过运行以下命令，快速生成并导入 Bookshop 应用的示例数据：

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你的 TiDB 集群是使用 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-reference) 部署的，或者你可以连接到你的 TiDB 服务器，你可以通过运行以下命令，快速生成并导入 Bookshop 应用的示例数据：

</CustomContent>

```shell
tiup demo bookshop prepare
```

默认情况下，此命令会让你的应用连接到地址 `127.0.0.1` 的端口 `4000`，允许你以 `root` 用户无密码登录，并在名为 `bookshop` 的数据库中创建 [表结构](#description-of-the-tables)。

#### 配置连接信息

下表列出了连接参数，你可以根据你的环境修改其默认设置。

| 参数           | 缩写 | 默认值             | 描述                     |
| -------------- | ---- | ------------------ | ------------------------ |
| `--password`   | `-p` | 无                 | 数据库用户密码           |
| `--host`       | `-H` | `127.0.0.1`        | 数据库地址               |
| `--port`       | `-P` | `4000`             | 数据库端口               |
| `--db`         | `-D` | `bookshop`         | 数据库名称               |
| `--user`       | `-U` | `root`             | 数据库用户               |

例如，如果你想连接到 TiDB Cloud 上的数据库，可以这样指定连接信息：

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### 设置数据量

你可以通过配置以下参数，指定每个数据库表要生成的数据量：

| 参数           | 默认值       | 描述                                              |
| -------------- | ------------ | ------------------------------------------------- |
| `--users`     | `10000`      | `users` 表中要生成的行数                          |
| `--authors`   | `20000`      | `authors` 表中要生成的行数                        |
| `--books`     | `20000`      | `books` 表中要生成的行数                          |
| `--orders`    | `300000`     | `orders` 表中要生成的行数                         |
| `--ratings`   | `300000`     | `ratings` 表中要生成的行数                        |

例如，执行以下命令将生成：

- 200,000 行用户信息（通过 `--users` 参数）
- 500,000 行书籍信息（通过 `--books` 参数）
- 100,000 行作者信息（通过 `--authors` 参数）
- 1,000,000 行评分记录（通过 `--ratings` 参数）
- 1,000,000 行订单记录（通过 `--orders` 参数）

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

你可以通过 `--drop-tables` 参数删除原有的表结构。更多参数说明，可以运行 `tiup demo bookshop --help` 获取。

### Method 2: Via TiDB Cloud 导入

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/) ，进入你的项目的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面。

        > **Tip:**
        >
        > 如果你有多个项目，可以点击左下角的 <MDSvgIcon name="icon-left-projects" /> ，切换到其他项目。

    2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Import**。

2. 选择 **Import data from Cloud Storage**，然后点击 **Amazon S3**。

3. 在 **Import Data from Amazon S3** 页面，配置以下源数据信息：

    - **Import File Count**：对于 {{{ .starter }} }，选择 **Multiple files**。此字段在 TiDB Cloud Dedicated 中不可用。
    - **Included Schema Files**：选择 **Yes**。
    - **Data Format**：选择 **SQL**。
    - **Folder URI**：输入 `s3://developer.pingcap.com/bookshop/`。
    - **Bucket Access**：选择 **AWS Role ARN**。
    - **Role ARN**：输入 `arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access`。

    在此示例中，提前生成了以下数据：

    - 200,000 行用户信息
    - 500,000 行书籍信息
    - 100,000 行作者信息
    - 1,000,000 行评分记录
    - 1,000,000 行订单记录

4. 点击 **Connect** > **Start Import** 开始导入流程，等待 TiDB Cloud 完成导入。

关于如何导入或迁移数据到 TiDB Cloud 的更多信息，请参见 [TiDB Cloud Migration Overview](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview)。

### 查看数据导入状态

导入完成后，你可以执行以下 SQL 语句，查看每个表的数据量信息：

```sql
SELECT
    CONCAT(table_schema,'.',table_name) AS 'Table Name',
    table_rows AS 'Number of Rows',
    CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size',
    CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size',
    CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS 'Total'
FROM
    information_schema.TABLES
WHERE table_schema LIKE 'bookshop';
```

结果如下：

```
+-----------------------+----------------+-----------+------------+---------+
| Table Name            | Number of Rows | Data Size | Index Size | Total   |
+-----------------------+----------------+-----------+------------+---------+
| bookshop.orders       |        1000000 | 0.0373G   | 0.0075G    | 0.0447G |
| bookshop.book_authors |        1000000 | 0.0149G   | 0.0149G    | 0.0298G |
| bookshop.ratings      |        4000000 | 0.1192G   | 0.1192G    | 0.2384G |
| bookshop.authors      |         100000 | 0.0043G   | 0.0000G    | 0.0043G |
| bookshop.users        |         195348 | 0.0048G   | 0.0021G    | 0.0069G |
| bookshop.books        |        1000000 | 0.0546G   | 0.0000G    | 0.0546G |
+-----------------------+----------------+-----------+------------+---------+
```

## 表结构说明

本节详细介绍 Bookshop 应用的数据库表。

### `books` 表

存储书籍的基本信息。

| 字段名       | 类型          | 描述                     |
|--------------|---------------|--------------------------|
| id           | bigint        | 书籍的唯一 ID            |
| title        | varchar(100)  | 书名                     |
| type         | enum          | 书籍类型（例如，杂志、动画、教学辅助） |
| stock        | bigint        | 库存                     |
| price        | decimal(15,2) | 价格                     |
| published_at | datetime      | 出版日期                 |

### `authors` 表

存储作者的基本信息。

| 字段名     | 类型          | 描述                     |
|------------|---------------|--------------------------|
| id         | bigint        | 作者的唯一 ID            |
| name       | varchar(100)  | 作者姓名                 |
| gender     | tinyint       | 性别（0：女，1：男，NULL：未知） |
| birth_year | smallint      | 出生年份                 |
| death_year | smallint      | 去世年份                 |

### `users` 表

存储 Bookshop 用户信息。

| 字段名     | 类型          | 描述                     |
|------------|---------------|--------------------------|
| id         | bigint        | 用户的唯一 ID            |
| balance    | decimal(15,2) | 账户余额                 |
| nickname   | varchar(100)  | 昵称                     |

### `ratings` 表

存储用户对书籍的评分记录。

| 字段名     | 类型     | 描述                                              |
|------------|----------|--------------------------------------------------|
| book_id    | bigint   | 书籍的唯一 ID（关联 [books](#books-table)）   |
| user_id    | bigint   | 用户的唯一标识（关联 [users](#users-table)）  |
| score      | tinyint  | 用户评分（1-5）                                   |
| rated_at   | datetime | 评分时间                                          |

### `book_authors` 表

作者可能会写多本书，一本书也可能由多位作者合作。本表存储书籍与作者的对应关系。

| 字段名     | 类型       | 描述                                              |
|------------|------------|--------------------------------------------------|
| book_id    | bigint     | 书籍的唯一 ID（关联 [books](#books-table)）   |
| author_id  | bigint     | 作者的唯一 ID（关联 [authors](#authors-table)） |

### `orders` 表

存储用户的购买信息。

| 字段名     | 类型       | 描述                                              |
|------------|------------|--------------------------------------------------|
| id         | bigint     | 订单的唯一 ID                                    |
| book_id    | bigint     | 书籍的唯一 ID（关联 [books](#books-table)）   |
| user_id    | bigint     | 用户的唯一标识（关联 [users](#users-table)）  |
| quantity   | tinyint    | 购买数量                                         |
| ordered_at | datetime   | 购买时间                                         |

## 数据库初始化脚本 `dbinit.sql`

如果你想手动创建 Bookshop 应用的数据库表结构，可以运行以下 SQL 语句：

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint DEFAULT NULL,
  `birth_year` smallint DEFAULT NULL,
  `death_year` smallint DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`ratings`;
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `score` tinyint NOT NULL,
  `rated_at` datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED,
  UNIQUE KEY `uniq_book_user_idx` (`book_id`,`user_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;

DROP TABLE IF EXISTS `bookshop`.`users`;
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.0',
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`orders`;
CREATE TABLE `bookshop`.`orders` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `quality` tinyint NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>