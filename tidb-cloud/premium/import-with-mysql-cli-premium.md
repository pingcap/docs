---
title: 使用 MySQL 命令行客户端将数据导入到 {{{ .premium }}}
summary: 了解如何使用 MySQL 命令行客户端 (`mysql`) 将小型 CSV 或 SQL 文件导入到 {{{ .premium }}} 实例。
---

# 使用 MySQL 命令行客户端将数据导入到 {{{ .premium }}}

本文介绍如何使用 [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) (`mysql`) 将数据导入到 {{{ .premium }}}。以下各节提供了从 SQL 或 CSV 文件导入数据的分步说明。此过程执行的是逻辑导入，即 MySQL 命令行客户端会从你的本地机器向 TiDB Cloud 重放 SQL 语句。

> **Tip:**
>
> - 逻辑导入最适合相对较小的 SQL 或 CSV 文件。若要从云存储进行更快的并行导入，或处理来自 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出的多个文件，请参见 [Import CSV Files from Cloud Storage into {{{ .premium }}}](/tidb-cloud/premium/import-csv-files-premium.md)。
> - 对于 {{{ .starter }}} 或 Essential，请参见 [Import Data into {{{ .starter }}} or Essential via MySQL CLI](/tidb-cloud/import-with-mysql-cli-serverless.md)。
> - 对于 {{{ .dedicated }}}，请参见 [Import Data into {{{ .dedicated }}} via MySQL CLI](/tidb-cloud/import-with-mysql-cli.md)。

## 前提条件 {#prerequisites}

在通过 MySQL 命令行客户端将数据导入到 {{{ .premium }}} 实例之前，你需要满足以下前提条件：

- 你可以访问你的 {{{ .premium }}} 实例。
- 在本地计算机上安装 MySQL 命令行客户端 (`mysql`)。

## 步骤 1. 连接到你的 {{{ .premium }}} 实例 {#step-1-connect-to-your-premium-instance}

使用 MySQL 命令行客户端连接到你的 {{{ .premium }}} 实例。如果这是你第一次连接，请执行以下步骤来配置网络连接并生成 TiDB SQL `root` 用户密码：

1. 登录 [TiDB Cloud console](https://tidbcloud.com/)，并导航到 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。然后，点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。

2. 点击右上角的 **Connect**。此时会显示连接对话框。

3. 确保连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Connect With** 设置为 `MySQL CLI`。
    - **Operating System** 与你的环境匹配。

    > **Note:**
    >
    > 默认情况下，{{{ .premium }}} 实例的公共端点是禁用的。如果你没有看到 `Public` 选项，请在实例详情页（**Network** 选项卡下）启用公共端点，或联系组织管理员先启用它，然后再继续。

4. 点击 **Generate Password** 以创建一个随机密码。如果你已经配置了密码，请复用该凭据，或在继续之前轮换该密码。

## 步骤 2. 定义目标数据库和表结构 {#step-2-define-the-target-database-and-table-schema}

在导入数据之前，创建与你的数据集匹配的目标表结构。

以下是一个示例 SQL 文件（`products-schema.sql`），用于创建示例数据库和表。请根据你的环境更新数据库名或表名。

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);
```

在你的 {{{ .premium }}} 实例上运行该 schema 文件，以便在下一步加载数据之前，数据库和表已经存在。

## 步骤 3. 从 SQL 或 CSV 文件导入数据 {#step-3-import-data-from-an-sql-or-csv-file}

使用 MySQL 命令行客户端将数据加载到你在步骤 2 中创建的 schema 中。根据需要将占位符替换为你自己的文件路径、凭据和数据集，然后按照与你的源格式匹配的工作流进行操作。

<SimpleTab>
<div label="From an SQL file">

执行以下操作以从 SQL 文件导入数据：

1. 提供一个 SQL 文件（例如 `products.sql`），其中包含你要导入的数据。该 SQL 文件必须包含带有数据的 `INSERT` 语句，类似如下：

    ```sql
    INSERT INTO products (product_id, product_name, price) VALUES
        (1, 'Laptop', 999.99),
        (2, 'Smartphone', 499.99),
        (3, 'Tablet', 299.99);
    ```

2. 使用以下命令从 SQL 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> < products.sql
    ```

    将占位符值（例如 `<your_username>`、`<your_instance_host>`、`<your_password>`、`<your_ca_path>` 以及 SQL 文件名）替换为你自己的连接信息和文件路径。

> **Note:**
>
> 示例 schema 创建了一个 `test` 数据库，命令中使用的是 `-D test`。如果你计划导入到其他数据库，请同时修改 schema 文件和 `-D` 参数。

<Important>

你用于认证的 SQL 用户必须具有所需权限（例如 `CREATE` 和 `INSERT`），才能定义表并将数据加载到目标数据库中。

</Important>

</div>
<div label="From a CSV file">

执行以下操作以从 CSV 文件导入数据：

1. 确保目标数据库和表已存在于 TiDB 中（例如你在步骤 2 中创建的 `products` 表）。

2. 提供一个示例 CSV 文件（例如 `products.csv`），其中包含你要导入的数据。示例如下：

    **products.csv:**

    ```csv
    product_id,product_name,price
    1,Laptop,999.99
    2,Smartphone,499.99
    3,Tablet,299.99
    ```

3. 使用以下命令从 CSV 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> \
      -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
          FIELDS TERMINATED BY ','
          LINES TERMINATED BY '\n'
          IGNORE 1 LINES (product_id, product_name, price);"
    ```

    将占位符值（例如 `<your_username>`、`<your_instance_host>`、`<your_password>`、`<your_ca_path>`、`<your_csv_path>` 以及表名）替换为你自己的连接信息和数据集路径。

> **Note:**
>
> 有关 `LOAD DATA LOCAL INFILE` 的更多语法细节，请参见 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)。

</div>
</SimpleTab>

## 步骤 4. 验证已导入的数据 {#step-4-validate-the-imported-data}

导入完成后，运行基本查询以验证是否存在预期的行，并确认数据正确无误。

使用 MySQL 命令行客户端连接到同一个数据库，并运行验证查询，例如统计行数和检查示例记录：

```bash
mysql --comments --connect-timeout 150 \
  -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
  --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
  -p<your_password> \
  -e "SELECT COUNT(*) AS row_count FROM products; \
      SELECT * FROM products ORDER BY product_id LIMIT 5;"
```

预期输出（示例）：

```text
+-----------+
| row_count |
+-----------+
|         3 |
+-----------+
+------------+---------------+--------+
| product_id | product_name  | price  |
+------------+---------------+--------+
|          1 | Laptop        | 999.99 |
|          2 | Smartphone    | 499.99 |
|          3 | Tablet        | 299.99 |
+------------+---------------+--------+
```

将占位符值替换为你自己的连接信息，并根据你的数据集结构调整验证查询。