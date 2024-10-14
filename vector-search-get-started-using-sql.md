---
title: Get Started with Vector Search via SQL
summary: Learn how to quickly get started with Vector Search in TiDB using SQL statements to power your generative AI applications.
---

# Get Started with Vector Search via SQL

TiDB extends MySQL syntax to support [Vector Search](/vector-search-overview.md) and introduce new [Vector data types](/vector-search-data-types.md) and several [vector functions](/vector-search-functions-and-operators.md).

This tutorial demonstrates how to get started with TiDB Vector Search just using SQL statements. You will learn how to use the [MySQL command-line client](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) to complete the following operations:

- Connect to your TiDB cluster.
- Create a vector table.
- Store vector embeddings.
- Perform vector search queries.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Prerequisites

To complete this tutorial, you need:

- [MySQL command-line client](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) (MySQL CLI) installed on your machine.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.
- Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Get started

### Step 1. Connect to the TiDB cluster

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **MySQL CLI** from the **Connect With** drop-down list and keep the default setting of the **Connection Type** as **Public**.

4. If you have not set a password yet, click **Generate Password** to generate a random password.

5. Copy the connection command and paste it into your terminal. The following is an example for macOS:

    ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

</div>
<div label="TiDB Self-Managed">

After your TiDB Self-Managed cluster is started, execute your cluster connection command in the terminal.

The following is an example connection command for macOS:

```bash
mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

</SimpleTab>

### Step 2. Create a vector table

When creating a table, you can define a column as a [vector](/vector-search-overview.md#vector-embedding) column by specifying the `VECTOR` data type.

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

Insert three documents with their [vector embeddings](/vector-search-overview.md#vector-embedding) into the `embedded_documents` table:

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
> In real-world applications, [embedding models](/vector-search-overview.md#embedding-model) often produce vector embeddings with hundreds or thousands of dimensions.

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

- [Vector Data Types](/vector-search-data-types.md)
- [Vector Search Index](/vector-search-index.md)
