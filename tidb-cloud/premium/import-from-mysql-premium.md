---
title: Import data into TiDB Cloud Premium via MySQL Command-Line Client
summary: Learn how to import small CSV or SQL files into TiDB Cloud Premium instances using the MySQL Command-Line Client (`mysql`).
---

> **Warning:**
> 
> TiDB Cloud Premium is currently available in **Private Preview** in select AWS regions.  
> 
> If Premium is not yet enabled for your organization, or if you need access in another cloud provider or region, click **Support** in the lower-left corner of the [TiDB Cloud console](https://tidbcloud.com/), or submit a request through the [Contact Us form](https://www.pingcap.com/contact-us) on our website.

# Import data into TiDB Cloud Premium using the MySQL Command-Line Client

This document describes how to import data into TiDB Cloud Premium using the [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) (`mysql`). The following sections provide step-by-step instructions for importing data from SQL or CSV files. These steps use a logical import, meaning the MySQL Command-Line Client replays SQL statements against TiDB Cloud from your local machine.

> **Tip:**
>
> Logical imports are best suited for relatively small SQL or CSV files. For faster, parallel imports from cloud storage or to process multiple files from [Dumpling](/dumpling-overview.md) exports, see [Import CSV files into TiDB Cloud Premium](/tidb-cloud/premium/import-csv-files-premium.md).

## Prerequisites

Before you can import data to a TiDB Cloud Premium instance via the MySQL Command-Line Client, you need the following prerequisites:

- You have access to your TiDB Cloud Premium instance.
- Install the MySQL Command-Line Client (`mysql`) on your local computer.

## Step 1. Connect to your TiDB Cloud Premium instance

Connect to your TiDB instance via the MySQL Command-Line Client. If this is your first time, you will need to configure the network connection and generate the TiDB SQL `root` user password following the steps below.

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and, if applicable, click **Switch to Private Preview** in the lower-left corner to enter the Premium workspace. Then navigate to the [**TiDB Instances**](https://tidbcloud.com/project/instances) page and click the name of your target instance to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`.
    - **Connect With** is set to `MySQL CLI`.
    - **Operating System** matches your environment.

    > **Note:**
    > 
    > Premium clusters ship with the public endpoint disabled by default. If you do not see the `Public` option, enable the public endpoint from the instance details page (in the **Network** tab), or ask an organization admin to enable it before proceeding.

4. Click **Generate Password** to create a random password. If you have already configured a password, reuse that credential or rotate it before proceeding.

## Step 2. Define the target database and table schema

Before importing data, create the target table structure that matches your dataset.

The following is an example SQL file (`products-schema.sql`) that creates a sample database and table. Update the database or table names to match your environment.

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);
```

Run the schema file against your TiDB Cloud Premium instance so the database and table exist before you load data in the next step.

## Step 3. Import data from a SQL or CSV file

Use the MySQL Command-Line Client to load data into the schema you created in Step 2. Replace the placeholders with your own file paths, credentials, and dataset as needed, then follow the workflow that matches your source format.

<SimpleTab>
<div label="From an SQL file">

Do the following to import data from an SQL file:

1. Provide an SQL file (for example, `products.sql`) that contains the data you want to import. This SQL file must include `INSERT` statements with data, similar to the following:

    ```sql
    INSERT INTO products (product_id, product_name, price) VALUES
        (1, 'Laptop', 999.99),
        (2, 'Smartphone', 499.99),
        (3, 'Tablet', 299.99);
    ```

2. Use the following command to import data from the SQL file:

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> < products.sql
    ```

    Replace the placeholder values (for example, `<your_username>`, `<your_instance_host>`, `<your_password>`, `<your_ca_path>`, and the SQL file name) with your own connection details and file path.

> **Note:**
>
> The sample schema creates a `test` database and the commands use `-D test`. Change both the schema file and the `-D` parameter if you plan to import into a different database.

> **Important:**
> 
> The SQL user you authenticate with must have the required privileges (for example, `CREATE` and `INSERT`) to define tables and load data into the target database.

</div>
<div label="From a CSV file">

Do the following to import data from a CSV file:

1. Ensure the target database and table exist in TiDB (for example, the `products` table you created in Step 2).

2. Provide a sample CSV file (for example, `products.csv`) that contains the data you want to import. The following is an example:

    **products.csv:**

    ```csv
    product_id,product_name,price
    1,Laptop,999.99
    2,Smartphone,499.99
    3,Tablet,299.99
    ```

3. Use the following command to import data from the CSV file:

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

    Replace the placeholder values (for example, `<your_username>`, `<your_instance_host>`, `<your_password>`, `<your_ca_path>`, `<your_csv_path>`, and the table name) with your own connection details and dataset paths.

> **Note:**
>
> For more syntax details about `LOAD DATA LOCAL INFILE`, see [`LOAD DATA`](/sql-statements/sql-statement-load-data.md).

</div>
</SimpleTab>

## Step 4. Validate the imported data

After the import completes, run basic queries to confirm that the expected rows are present and the data looks correct.

Use the MySQL Command-Line Client to connect to the same database and run validation queries, such as counting rows and inspecting sample records:

```bash
mysql --comments --connect-timeout 150 \
  -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
  --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
  -p<your_password> \
  -e "SELECT COUNT(*) AS row_count FROM products; \
      SELECT * FROM products ORDER BY product_id LIMIT 5;"
```

Expected output (example):

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

Replace the placeholder values with your own connection details, and adjust the validation queries to suit the shape of your dataset.
