---
title: 通过 MySQL CLI 向 TiDB Cloud Dedicated 导入数据
summary: 了解如何通过 MySQL CLI 向 TiDB Cloud Dedicated 导入数据。
---

# 通过 MySQL CLI 向 TiDB Cloud Dedicated 导入数据

本文档介绍了如何通过 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) 向 TiDB Cloud Dedicated 导入数据。你可以从 SQL 文件或 CSV 文件导入数据。以下章节将分别提供从每种文件类型导入数据的分步说明。

## 前置条件

在你通过 MySQL CLI 向 TiDB Cloud Dedicated 导入数据之前，需要满足以下前置条件：

- 你可以访问你的 TiDB Cloud Dedicated 集群。如果没有，请按照 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md) 的说明创建一个。
- 在你的本地计算机上安装 MySQL CLI。

## 步骤 1. 连接到你的 TiDB Cloud Dedicated 集群

连接到你的 TiDB 集群。

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **IP Access List** 区域的 **Add IP Address**。

4. 在弹窗中，选择 **Allow access from anywhere**，然后点击 **Confirm**。

5. 在右上角，点击 **Connect**，打开连接信息的弹窗。

    有关如何获取连接字符串的更多信息，请参见 [通过公共连接连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

## 步骤 2. 定义表结构并插入示例数据

在导入数据之前，你需要准备表结构，并向其中插入真实的示例数据。以下是一个 SQL 文件（`product_data.sql`）的示例，你可以用它来创建表并插入示例数据：

```sql
-- Create a table in your TiDB database
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);

-- Insert sample data into the table
INSERT INTO products (product_id, product_name, price) VALUES
    (1, 'Laptop', 999.99),
    (2, 'Smartphone', 499.99),
    (3, 'Tablet', 299.99);
```

## 步骤 3. 从 SQL 或 CSV 文件导入数据

你可以从 SQL 文件或 CSV 文件导入数据。以下章节将分别提供从每种文件类型导入数据的分步说明。

<SimpleTab>
<div label="From an SQL file">

按照以下步骤从 SQL 文件导入数据：

1. 提供一个真实的 SQL 文件（例如 `product_data.sql`），其中包含你要导入的数据。该 SQL 文件必须包含带有真实数据的 `INSERT` 语句。

2. 使用以下命令从 SQL 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> < product_data.sql
    ```

> **Note:**
>
> 这里默认使用的数据库名称为 `test`，你可以手动创建自己的数据库，或者在 SQL 文件中使用 `CREATE DATABASE` 命令。

</div>
<div label="From a CSV file">

按照以下步骤从 CSV 文件导入数据：

1. 在 TiDB 中创建数据库和表结构，以满足你的数据导入需求。

2. 提供一个示例 CSV 文件（例如 `product_data.csv`），其中包含你要导入的数据。以下是一个 CSV 文件的示例：

    **product_data.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3. 使用以下命令从 CSV 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

4. 请确保将路径、表名（本例为 `products`）、`<your_username>`、`<your_host>`、`<your_password>`、`<your_csv_path>`、`<your_ca_path>` 以及其他占位符替换为你的实际信息，并根据需要将示例 CSV 数据替换为你的真实数据集。

> **Note:**
>
> 有关 `LOAD DATA LOCAL INFILE` 的更多语法细节，请参见 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)。

</div>
</SimpleTab>