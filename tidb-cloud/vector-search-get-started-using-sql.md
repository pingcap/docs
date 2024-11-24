---
title: Get Started with Vector Search via SQL
summary: Learn how to quickly get started with Vector Search in TiDB using SQL statements to power your generative AI applications.
---

# Get Started with Vector Search via SQL

TiDB extends MySQL syntax to support [Vector Search](/tidb-cloud/vector-search-overview.md) and introduce new [Vector data types](/tidb-cloud/vector-search-data-types.md) and several [vector functions](/tidb-cloud/vector-search-functions-and-operators.md).

This tutorial demonstrates how to get started with TiDB Vector Search just using SQL statements. You will learn how to use the [MySQL command-line client](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) to complete the following operations:

- Connect to your TiDB cluster.
- Create a vector table.
- Store vector embeddings.
- Perform vector search queries.

> **Note**
>
> TiDB Vector Search is only available for TiDB (>= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

## Prerequisites

To complete this tutorial, you need:

- [MySQL command-line client](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) (MySQL CLI) installed on your machine.
- A TiDB Cloud Serverless cluster. Follow [creating a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create your own TiDB Cloud cluster if you don't have one.

## Get started

### Step 1. Connect to the TiDB cluster

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **MySQL CLI** from the **Connect With** drop-down list and keep the default setting of the **Connection Type** as **Public**.

4. If you have not set a password yet, click **Generate Password** to generate a random password.

5. Copy the connection command and paste it into your terminal. The following is an example for macOS:

   ```bash
   mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
   ```

### Step 2. Create a vector table

When creating a table, you can define a column as a [vector](/tidb-cloud/vector-search-overview.md#vector-embedding) column by specifying the `VECTOR` data type.

For example, to create a table `embedded_documents` with a three-dimensional `VECTOR` column, execute the following SQL statements using your MySQL CLI:

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- Column to store the original content of the document.
    document  TEXT,
    -- Column to store the vector representation of the document.
    embedding VECTOR(3)
);
```

The expected output is as follows:

```text
Query OK, 0 rows affected (0.27 sec)
```

### Step 3. Insert vector embeddings to the table

Insert three documents with their [vector embeddings](/tidb-cloud/vector-search-overview.md#vector-embedding) into the `embedded_documents` table:

```sql
INSERT INTO embedded_documents
VALUES
    (1, 'dog', '[1,2,1]'),
    (2, 'fish', '[1,2,4]'),
    (3, 'tree', '[1,0,0]');
```

The expected output is as follows:

```
Query OK, 3 rows affected (0.15 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

> **Note**
>
> This example simplifies the dimensions of the vector embeddings and uses only 3-dimensional vectors for demonstration purposes.
>
> In real-world applications, [embedding models](/tidb-cloud/vector-search-overview.md#embedding-model) often produce vector embeddings with hundreds or thousands of dimensions.

### Step 4. Query the vector table

To verify that the documents have been inserted correctly, query the `embedded_documents` table:

```sql
SELECT * FROM embedded_documents;
```

The expected output is as follows:

```sql
+----+----------+-----------+
| id | document | embedding |
+----+----------+-----------+
|  1 | dog      | [1,2,1]   |
|  2 | fish     | [1,2,4]   |
|  3 | tree     | [1,0,0]   |
+----+----------+-----------+
3 rows in set (0.15 sec)
```

### Step 5. Perform a vector search query

Similar to full-text search, users provide search terms to the application when using vector search.

In this example, the search term is "a swimming animal", and its corresponding vector embedding is assumed to be `[1,2,3]`. In practical applications, you need to use an embedding model to convert the user's search term into a vector embedding.

Execute the following SQL statement, and TiDB will identify the top three documents closest to `[1,2,3]` by calculating and sorting the cosine distances (`vec_cosine_distance`) between the vector embeddings in the table.

```sql
SELECT id, document, vec_cosine_distance(embedding, '[1,2,3]') AS distance
FROM embedded_documents
ORDER BY distance
LIMIT 3;
```

The expected output is as follows:

```plain
+----+----------+---------------------+
| id | document | distance            |
+----+----------+---------------------+
|  2 | fish     | 0.00853986601633272 |
|  1 | dog      | 0.12712843905603044 |
|  3 | tree     |  0.7327387580875756 |
+----+----------+---------------------+
3 rows in set (0.15 sec)
```

The three terms in the search results are sorted by their respective distance from the queried vector: the smaller the distance, the more relevant the corresponding `document`.

Therefore, according to the output, the swimming animal is most likely a fish, or a dog with a gift for swimming.

## See also

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
