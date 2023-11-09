---
title: Import Data into TiDB Cloud via MySQL Commands in Terminal
summary: Learn how to import Data into TiDB Cloud via MySQL CLI.
---

# Import MySQL Data via MySQL Commands in Terminal

## Prerequisites:

Before you can import MySQL data to TiDB Cloud, you should have the following prerequisites in place:

- Access to your TiDB Cloud Cluster.
- Necessary connection details obtained from the TiDB Cloud portal.
- An initial password created for your TiDB user (if not already done).
- TiDB cluster connection information.

## Steps:

### 1. Connect to your TiDB Cloud Cluster

1. Access the TiDB Cloud portal and obtain the necessary connection details.
2. Create an initial password for your TiDB cluster if you haven't already.
3. Select your connect options: Choose 'Endpoint Type' as 'Public', select 'Connect With' as 'MySQL CLI' and choose the operating system you are using. Obtain the cluster connection information.

### 2. Install MySQL Command Line Client

You need to have MySQL Command Line Client installed on your local machine. You can download it from the official MySQL website if it's not already installed.

### 3. Define Table and Insert Sample Data

Before importing data, you need to prepare the table structure and insert real sample data into it. Here's an example using a hypothetical "products" table:

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

### 4. Import Data from SQL File

1. Provide a real SQL file (e.g., `product_data.sql`) that contains the data you want to import. This SQL file should contain INSERT statements with real data.

2. Use the following command to import data from the SQL file:

```bash
mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p <your_password> < product_data.sql
```
> **Note:**
> The default database name used here is 'test', and you can either manually create your own database or use the 'create database' command in an SQL file.

### 5. Import Data from CSV File

1. Create a database and schema in TiDB to match your data import needs.

2. Provide a sample CSV file (e.g., `product_data.csv`) that contains the data you want to import. Here's an example of what your sample CSV file might look like:

    **product_data.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3. Use the following command to import data from the CSV file:

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products 
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

4. Make sure to adjust the paths, table name ('products' in this example), and other specifics according to your actual data and setup.

> **Note:**
> Replace '<your_username>', '<your_host>', '<your_password>', '<your_csv_path>', '<your_ca_path>', and other placeholders with your actual information, and replace the sample CSV data with your real dataset as needed.
> For more syntax details about `LOAD DATA LOCAL INFILE`, please refer to: [MySQL Official Documentation](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)
