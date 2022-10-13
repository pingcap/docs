---
title: TiDB with dbt
summary: Learn the use cases of dbt in TiDB.
---

# TiDB with dbt

[Data build tool (dbt)](https://www.getdbt.com/) is a popular open-source data transformation tool that enables analytics engineers to transform data in their warehouses through SQL statements. Through the [dbt-tidb](https://github.com/pingcap/dbt-tidb) plug-in, analytics engineers working with TiDB can directly create forms and match data through SQL without having to think about the process of creating tables or views.

Here we use the official dbt tutorial as an example to introduce the use of TiDB in dbt together.

The software used in this example and its version requirements:
- TiDB 5.3 or upper
- dbt 1.01 or upper
- dbt-tidb 1.0.0

## Installation

Installing dbt and dbt-tidb requires only one command because dbt is installed as a dependency when we install dbt-tidb.

```shell
pip install dbt-tidb
```

## Creating project: jaffle shop

The jaffle_shop is a project provided by dbt-lab to demonstrate dbt functionality.

```shell
git clone https://github.com/dbt-labs/jaffle_shop
cd jaffle_shop
```

## Configuring project

### Global configurations

dbt has a default global profile: `~/.dbt/profiles.yml`, which we first set up in the user directory and configured the connection information for the TiDB database.

```shell
vi ~/.dbt/profiles.yml

 jaffle_shop_tidb:                      # project name
  target: dev                           # target
  outputs:
    dev:
      type: tidb                        # adapter type
      server: 127.0.0.1                  
      port: 4000                         
      schema: analytics                 # database name
      username: root                     
      password: ""                       
```

**Description of Configurations**

| Option           | Description                                           | Required? | Example                        |
|------------------|-------------------------------------------------------|-----------|--------------------------------|
| type             | The specific adapter to use                           | Required  | `tidb`                         |
| server           | The server (hostname) to connect to                   | Required  | `yourorg.tidb.com`             |
| port             | The port to use                                       | Required  | `4000`                         |
| schema           | Specify the schema (database) to build models into    | Required  | `analytics`                    |
| username         | The username to use to connect to the server          | Required  | `dbt_admin`                    |
| password         | The password to use for authenticating to the server  | Required  | `correct-horse-battery-staple` |
| retries          | The retry times for connection to TiDB (1 in default) | Optional  | `2`                            |

### Project configurations

In the jaffle_shop project directory, the project configuration file `dbt_project.yml` is available. Change the `profile` configuration item to `jaffle_shop_tidb`, which is the project name in `profiles.yml`. Then, the project will query the database connection configuration in the `~/.dbt/profiles.yml file`.

```shell
vi dbt_project.yml 

name: 'jaffle_shop'

config-version: 2
version: '0.1'

profile: 'jaffle_shop_tidb'                   # note the modification here

model-paths: ["models"]                       # model path
seed-paths: ["seeds"]                         # seed path
test-paths: ["tests"]                         
analysis-paths: ["analysis"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
    - "target"
    - "dbt_modules"
    - "logs"

require-dbt-version: [">=1.0.0", "<2.0.0"]

models:
  jaffle_shop:
      materialized: table            # *.sql which in models/ would be materialized to table
      staging:           
        materialized: view           # *.sql which in models/staging/ would bt materialized to view
```

### Verify the configuration

You can run the following command to check whether the database and project configuration is correct.

```shell
dbt debug
```

## Loading CSV

Load the CSV data and materialize the CSV as a table in the target database. 

> **Note:** 
> 
> In general, dbt projects do not need this step because the data for your pending projects is in the database.

```shell
dbt seed
```

## Running

```shell
dbt run
```

Go to the TiDB database to verify that the creation is successful.

```shell
mysql -h <your_TiDB_host> -u <user_name> -P <port>
```

The result illustrates that five more tables or views, such as `customers`, have been added, and the data in the tables or views have been transformed. Only part of `customers` data is shown here.

```sql
mysql> show tables;
+---------------------+
| Tables_in_analytics |
+---------------------+
| customers           |
| orders              |
| raw_customers       |
| raw_orders          |
| raw_payments        |
| stg_customers       |
| stg_orders          |
| stg_payments        |
+---------------------+
8 rows in set (0.00 sec)

mysql> select * from customers;
+-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
| customer_id | first_name | last_name | first_order | most_recent_order | number_of_orders | customer_lifetime_value |
+-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
|           1 | Michael    | P.        | 2018-01-01  | 2018-02-10        |                2 |                 33.0000 |
|           2 | Shawn      | M.        | 2018-01-11  | 2018-01-11        |                1 |                 23.0000 |
|           3 | Kathleen   | P.        | 2018-01-02  | 2018-03-11        |                3 |                 65.0000 |
|           4 | Jimmy      | C.        | NULL        | NULL              |             NULL |                    NULL |
|           5 | Katherine  | R.        | NULL        | NULL              |             NULL |                    NULL |
|           6 | Sarah      | R.        | 2018-02-19  | 2018-02-19        |                1 |                  8.0000 |
|           7 | Martin     | M.        | 2018-01-14  | 2018-01-14        |                1 |                 26.0000 |
|           8 | Frank      | R.        | 2018-01-29  | 2018-03-12        |                2 |                 45.0000 |
....
```

## Generating doc

dbt also supports the generation of visual documents, using the following command.

```
dbt docs generate
dbt docs serve
```

The document, which contains the overall structure of the jaffle_shop project and a description of all the tables and views, can be viewed at [http://localhost:8080](http://localhost:8080).

## Supports and Limitations

|     TiDB 4.X     | TiDB 5.0 ~ 5.2 | TiDB >= 5.3 |           Feature           |
|:----------------:|:--------------:|:-----------:|:---------------------------:|
|        ✅         |       ✅        |      ✅      |    Table materialization    |
|        ✅         |       ✅        |      ✅      |    View materialization     |
|        ❌         |       ❌        |      ✅      | Incremental materialization |
|        ❌         |       ✅        |      ✅      |  Ephemeral materialization  |
|        ✅         |       ✅        |      ✅      |            Seeds            |
|        ✅         |       ✅        |      ✅      |           Sources           |
|        ✅         |       ✅        |      ✅      |      Custom data tests      |
|        ✅         |       ✅        |      ✅      |        Docs generate        |
|        ❌         |       ❌        |      ✅      |          Snapshots          |
|        ✅         |       ✅        |      ✅      |      Connection retry       |
|        ✅         |       ✅        |      ✅      |            Grant            |

> **Note:**
> * TiDB 4.0 ~ 5.0 does not support [CTE](https://docs.pingcap.com/tidb/dev/sql-statement-with), you should avoid using `WITH` in your SQL code.
> * TiDB 4.0 ~ 5.2 does not support creating a [temporary table or view](https://docs.pingcap.com/tidb/v5.2/sql-statement-create-table#:~:text=sec\)-,MySQL%20compatibility,-TiDB%20does%20not).
> * TiDB 4.X does not support using SQL func in `CREATE VIEW`, avoid it in your SQL code. You can find more detail [here](https://github.com/pingcap/tidb/pull/27252).

## Supported functions

cross-db macros are moved from dbt-utils into dbt-core, so you can use the following functions directly, see [dbt-util](https://github.com/dbt-labs/dbt-utils) on how to use them.

- bool_or
- cast_bool_to_text
- dateadd
- datediff
- date_trunc
- hash
- safe_cast
- split_part
- last_day
- cast_bool_to_text
- concat
- escape_single_quotes
- except
- intersect
- length
- position
- replace
- right
- listagg (not support yet)

> pay attention that datediff is a little different from dbt-util that it will round down rather than round up.