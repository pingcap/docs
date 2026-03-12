---
title: Connection
---

## What is Connection?

A connection in Databend refers to a designated configuration that encapsulates the details required to interact with an external storage service. It serves as a centralized and reusable set of parameters, such as access credentials, endpoint URLs, and storage types, facilitating the integration of Databend with various storage services.

Connection can be utilized for creating external stages, external tables, and attaching tables, offering a streamlined and modular approach to managing and accessing data stored in external storage services through Databend.

## Connection Management

| Command | Description |
|---------|-------------|
| [CREATE CONNECTION](create-connection.md) | Creates a new connection to an external storage service |
| [DROP CONNECTION](drop-connection.md) | Removes an existing connection |

## Connection Information

| Command | Description |
|---------|-------------|
| [DESCRIBE CONNECTION](desc-connection.md) | Shows details of a specific connection |
| [SHOW CONNECTIONS](show-connections.md) | Lists all connections in the current database |

### Usage Examples

The examples in this section initially create a connection with the credentials necessary for connecting to Amazon S3. Subsequently, they utilize this established connection to create an external stage and attach an existing table. 

This statement initiates a connection to Amazon S3, specifying essential connection parameters:

```sql
CREATE CONNECTION toronto 
    STORAGE_TYPE = 's3' 
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

```

#### Example 1: Creating External Stage with Connection

The following example creates an external stage using the previously defined connection named 'toronto':

```sql
CREATE STAGE my_s3_stage 
    URL = 's3://databend-toronto' 
    CONNECTION = (CONNECTION_NAME = 'toronto');


-- Equivalent to the following statement without using a connection:

CREATE STAGE my_s3_stage 
    URL = 's3://databend-toronto' 
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>' 
    );

```

#### Example 2: Attaching Table with Connection

The [ATTACH TABLE](../01-table/92-attach-table.md) page offers [Examples](../01-table/92-attach-table.md#examples) demonstrating how to connect a new table in Databend Cloud with an existing table in Databend, where data is stored within an Amazon S3 bucket named "databend-toronto". In each example, Step 3 can be streamlined using the previously defined connection named 'toronto':

```sql title='Databend Cloud:'
ATTACH TABLE employees_backup 
    's3://databend-toronto/1/216/' 
    CONNECTION = (CONNECTION_NAME = 'toronto');

```

```sql title='Databend Cloud:'
ATTACH TABLE population_readonly 
    's3://databend-toronto/1/556/' 
    CONNECTION = (CONNECTION_NAME = 'toronto') 
    READ_ONLY;

```

#### Example 3: Creating External Table with Connection

This example demonstrates the creation of an external table named 'BOOKS' using the previously defined connection named 'toronto':

```sql
CREATE TABLE BOOKS (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
) 
's3://databend-toronto' 
CONNECTION = (CONNECTION_NAME = 'toronto');

```
