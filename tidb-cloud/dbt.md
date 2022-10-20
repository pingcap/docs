---
title: Transform Data by dbt
summary: Learn the use cases of dbt in TiDB.
---

# Transform Data by dbt

[Data build tool (dbt)](https://www.getdbt.com/) is a popular open-source data transformation tool that enables analytics engineers to transform data in their warehouses through SQL statements. Through the [dbt-tidb](https://github.com/pingcap/dbt-tidb) plug-in, analytics engineers working with TiDB can directly create forms and match data through SQL without having to think about the process of creating tables or views.

Here we use the official dbt tutorial as an example to introduce the use of TiDB in dbt together. Before you try any of the steps below, make sure the following items are installed:

- TiDB 5.3 or upper
- dbt 1.01 or upper
- dbt-tidb 1.0.0

## Step 1: install dbt and dbt-tidb

Installing dbt and dbt-tidb requires only one command because dbt is installed as a dependency when we install dbt-tidb.

```shell
pip install dbt-tidb
```

You can also install dbt separately. Please refer to [How to install dbt](https://docs.getdbt.com/docs/get-started/installation) in the dbt documentation.

## Step 2: create project: jaffle shop

The jaffle_shop is a project provided by dbt-lab to demonstrate dbt functionality. You can get the project directly from GitHub:

```shell
git clone https://github.com/dbt-labs/jaffle_shop
cd jaffle_shop
```

All files in the jaffle_shop project directory are structured as follows.

```shell
tree
.
├── LICENSE
├── README.md
├── dbt_project.yml
├── etc
│    ├── dbdiagram_definition.txt
│    └── jaffle_shop_erd.png
├── models
│    ├── customers.sql
│    ├── docs.md
│    ├── orders.sql
│    ├── overview.md
│    ├── schema.yml
│    └── staging
│        ├── schema.yml
│        ├── stg_customers.sql
│        ├── stg_orders.sql
│        └── stg_payments.sql
└── seeds
    ├── raw_customers.csv
    ├── raw_orders.csv
    └── raw_payments.csv
```

- **dbt_project.yml** is the dbt project configuration file, which holds the project name and database configuration file information.
- **The models directory** contains the project’s SQL models and table schemas. Note that the data analyst at your company writes this section. To learn more about models, see [dbt Docs](https://docs.getdbt.com/docs/build/sql-models).
- **The seed directory** stores CSV files that are dumped from database export tools. For example, TiDB can export the table data into CSV files through [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview). In the jaffle shop project, these CSV files are used as raw data to be processed.

## Step 3: configure the project

To configure the project:

1. Complete the global configuration. In the user directory, edit the default global profile, `~/.dbt/profiles.yml` to configure the connection with TiDB:

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

2. Complete the project configuration. In the jaffle_shop project directory, enter the project configuration file `dbt_project.yml` and change the profile field to `jaffle_shop_tidb`. This configuration allows the project to query from the database as specified in the `~/.dbt/profiles.yml` file.

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

3. Verify the configuration. Run the following command to check whether the database and project configuration is correct.

    ```shell
    dbt debug
    ```

## Step 4: load CSV files

Now that you have successfully created and configured the project, it’s time to load the CSV data and materialize the CSV as a table in the target database. Note that this step is not generally required for a dbt project because the data items for processing are already in the database.

1. Load the CSV data and materialize the CSV as a table in the target database.

    > **Note:**
    >
    > In general, dbt projects do not need this step because the data for your pending projects is in the database.

    ```shell
    dbt seed
    ```

    This displays the following:

    ```shell
    Running with dbt=1.0.1
    Partial parse save file not found. Starting full parse.
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 172 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 3 START seed file analytics.raw_customers.................................. [RUN]
    1 of 3 OK loaded seed file analytics.raw_customers.............................. [INSERT 100 in 0.19s]
    2 of 3 START seed file analytics.raw_orders..................................... [RUN]
    2 of 3 OK loaded seed file analytics.raw_orders................................. [INSERT 99 in 0.14s]
    3 of 3 START seed file analytics.raw_payments................................... [RUN]
    3 of 3 OK loaded seed file analytics.raw_payments............................... [INSERT 113 in 0.24s]
    ```

    As you can see in the results, the seed file was started and loaded into three tables: `analytics.raw_customers`, `analytics.raw_orders`, and `analytics.raw_payments`.

2. Verify the results in TiDB. The show databases command lists the new analytics database that dbt created. The show tables command indicates that there are three tables in the analytics database, corresponding to the ones we created above.

    ```sql
    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | INFORMATION_SCHEMA |
    | METRICS_SCHEMA     |
    | PERFORMANCE_SCHEMA |
    | analytics          |
    | io_replicate       |
    | mysql              |
    | test               |
    +--------------------+
    7 rows in set (0.00 sec)

    mysql> use analytics;
    mysql> show tables;
    +---------------------+
    | Tables_in_analytics |
    +---------------------+
    | raw_customers       |
    | raw_orders          |
    | raw_payments        |
    +---------------------+
    3 rows in set (0.00 sec)
    ```

## Step 5: run the project

Now you are ready to run the configured projects and finish the data transformation.

1. Run the dbt project to finish the data transformation:

    ```shell
    dbt run
    ```
    This displays the following:

    ```
    Running with dbt=1.0.1
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 170 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 5 START view model analytics.stg_customers................................. [RUN]
    1 of 5 OK created view model analytics.stg_customers............................ [SUCCESS 0 in 0.31s]
    2 of 5 START view model analytics.stg_orders.................................... [RUN]
    2 of 5 OK created view model analytics.stg_orders............................... [SUCCESS 0 in 0.23s]
    3 of 5 START view model analytics.stg_payments.................................. [RUN]
    3 of 5 OK created view model analytics.stg_payments............................. [SUCCESS 0 in 0.29s]
    4 of 5 START table model analytics.customers.................................... [RUN]
    4 of 5 OK created table model analytics.customers............................... [SUCCESS 0 in 0.76s]
    5 of 5 START table model analytics.orders....................................... [RUN]
    5 of 5 OK created table model analytics.orders.................................. [SUCCESS 0 in 0.63s]

    Finished running 3 view models, 2 table models in 2.27s.

    Completed successfully

    Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5
    ```

    The result shows three views (`analytics.stg_customers`, `analytics.stg_orders`, and `analytics.stg_payments`) and two tables (`analytics.customers` and `analytics.orders`) were created successfully.

2. Go to the TiDB database to verify that the creation is successful.

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

    mysql> select * from customers limit 10;
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
    |           9 | Jennifer   | F.        | 2018-03-17  | 2018-03-17        |                1 |                 30.0000 |
    |          10 | Henry      | W.        | NULL        | NULL              |             NULL |                    NULL |
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    10 rows in set (0.00 sec)
    ```

    The output shows that five more tables or views have been added, and the data in the tables or views has been transformed. Note that only part of the data from the customer table is shown here.

## Step 6: generate the doc

dbt lets you generate visual documents that display the overall structure of the project and describe all the tables and views. To generate visual documents:

1. Generate the document:

    ```shell
    dbt docs generate
    ```

2. Start the server:

    ```shell
    dbt docs serve
    ```

3. To access the document view from your browser, navigate to [http://localhost:8080](http://localhost:8080).


## Description of profile fields

| Option           | Description                                           | Required? | Example                        |
|------------------|-------------------------------------------------------|-----------|--------------------------------|
| type             | The specific adapter to use                           | Required  | `tidb`                         |
| server           | The server (hostname) to connect to                   | Required  | `yourorg.tidb.com`             |
| port             | The port to use                                       | Required  | `4000`                         |
| schema           | Specify the schema (database) to build models into    | Required  | `analytics`                    |
| username         | The username to use to connect to the server          | Required  | `dbt_admin`                    |
| password         | The password to use for authenticating to the server  | Required  | `correct-horse-battery-staple` |
| retries          | The retry times for connection to TiDB (1 in default) | Optional  | `2`                            |

## Supported features

|     TiDB 4.X     | TiDB 5.0 ~ 5.2 | TiDB >= 5.3 |           Feature           |
|:----------------:|:--------------:|:-----------:|:---------------------------:|
|        ✅         |       ✅        |      ✅      |    Table materialization    |
|        ✅         |       ✅        |      ✅      |    View materialization     |
|        ❌         |       ❌        |      ✅      | Incremental materialization |
|        ❌         |       ✅        |      ✅      |  Ephemeral materialization  |
|        ✅         |       ✅        |      ✅      |            Seeds            |
|        ✅         |       ✅        |      ✅      |           Sources           |
|        ✅         |       ✅        |      ✅      |      Custom data tests      |
|        ✅         |       ✅        |      ✅      |        Docs generation       |
|        ❌         |       ❌        |      ✅      |          Snapshots          |
|        ✅         |       ✅        |      ✅      |      Connection retry       |
|        ✅         |       ✅        |      ✅      |            Grant            |

> **Note:**
> * TiDB 4.0 ~ 5.0 does not support [CTE](https://docs.pingcap.com/tidb/dev/sql-statement-with), you should avoid using `WITH` in your SQL code.
> * TiDB 4.0 ~ 5.2 does not support creating a [temporary table or view](https://docs.pingcap.com/tidb/v5.2/sql-statement-create-table).
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
- listagg (not supported yet)

> pay attention that datediff is a little different from dbt-util that it will round down rather than round up.