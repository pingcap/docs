---
title: BendSQL
summary: BendSQL is a command line tool that has been designed specifically for Databend. It allows users to establish a connection with Databend and execute queries directly from a CLI window.
---
[BendSQL](https://github.com/databendlabs/bendsql) is a command line tool that has been designed specifically for Databend. It allows users to establish a connection with Databend and execute queries directly from a CLI window.

BendSQL is particularly useful for those who prefer a command line interface and need to work with Databend on a regular basis. With BendSQL, users can easily and efficiently manage their databases, tables, and data, and perform a wide range of queries and operations with ease.

## Installing BendSQL

BendSQL offers multiple installation options to suit different platforms and preferences. Choose your preferred method from the sections below or download the installation package from the [BendSQL release page](https://github.com/databendlabs/bendsql/releases) to install it manually.

### Shell Script

BendSQL provides a convenient Shell script for installation. You can choose between two options:

#### Default Installation

Install BendSQL to the user's home directory (~/.bendsql):

```bash
curl -fsSL https://repo.databend.com/install/bendsql.sh | bash
```

```bash title='Example:'
# highlight-next-line
curl -fsSL https://repo.databend.com/install/bendsql.sh | bash

                                  B E N D S Q L
                                    Installer

--------------------------------------------------------------------------------
Website: https://databend.com
Docs: https://docs.databend.com
Github: https://github.com/databendlabs/bendsql
--------------------------------------------------------------------------------

>>> We'll be installing BendSQL via a pre-built archive at https://repo.databend.com/bendsql/v0.22.2/
>>> Ready to proceed? (y/n)

>>> Please enter y or n.
>>> y

--------------------------------------------------------------------------------

>>> Downloading BendSQL via https://repo.databend.com/bendsql/v0.22.2/bendsql-aarch64-apple-darwin.tar.gz ✓
>>> Unpacking archive to /Users/eric/.bendsql ... ✓
>>> Adding BendSQL path to /Users/eric/.zprofile ✓
>>> Adding BendSQL path to /Users/eric/.profile ✓
>>> Install succeeded! 🚀
>>> To start BendSQL:

    bendsql --help

>>> More information at https://github.com/databendlabs/bendsql
```

#### Custom Installation with `--prefix`

Install BendSQL to a specified directory (e.g., /usr/local):

```bash
curl -fsSL https://repo.databend.com/install/bendsql.sh | bash -s -- -y --prefix /usr/local
```

```bash title='Example:'
# highlight-next-line
curl -fsSL https://repo.databend.com/install/bendsql.sh | bash -s -- -y --prefix /usr/local
                                  B E N D S Q L
                                    Installer

--------------------------------------------------------------------------------
Website: https://databend.com
Docs: https://docs.databend.com
Github: https://github.com/databendlabs/bendsql
--------------------------------------------------------------------------------

>>> Downloading BendSQL via https://repo.databend.com/bendsql/v0.22.2/bendsql-aarch64-apple-darwin.tar.gz ✓
>>> Unpacking archive to /usr/local ... ✓
>>> Install succeeded! 🚀
>>> To start BendSQL:

    bendsql --help

>>> More information at https://github.com/databendlabs/bendsql
```

### Homebrew (for macOS)

BendSQL can be easily installed on macOS using Homebrew with a simple command:

```bash
brew install databendcloud/homebrew-tap/bendsql
```

### Apt (for Ubuntu/Debian)

On Ubuntu and Debian systems, BendSQL can be installed via the Apt package manager. Choose the appropriate instructions based on the distribution version.

#### DEB822-STYLE format (Ubuntu-22.04/Debian-12 and later)

```bash
sudo curl -L -o /etc/apt/sources.list.d/databend.sources https://repo.databend.com/deb/databend.sources
```

#### Old format (Ubuntu-20.04/Debian-11 and earlier)

```bash
sudo curl -L -o /usr/share/keyrings/databend-keyring.gpg https://repo.databend.com/deb/databend.gpg
sudo curl -L -o /etc/apt/sources.list.d/databend.list https://repo.databend.com/deb/databend.list
```

Finally, update the package list and install BendSQL:

```bash
sudo apt update
sudo apt install bendsql
```

### Cargo (Rust Package Manager)

To install BendSQL using Cargo, utilize the `cargo-binstall` tool or build from source using the provided command.

> **Note:**
>
> Before installing with Cargo, make sure you have the full Rust toolchain and the `cargo` command installed on your computer. If you don't, follow the installation guide at [https://rustup.rs/](https://rustup.rs/).

**Using cargo-binstall**

Please refer to [Cargo B(inary)Install - Installation](https://github.com/cargo-bins/cargo-binstall#installation) to install `cargo-binstall` and enable the `cargo binstall <crate-name>` subcommand.

```bash
cargo binstall bendsql
```

**Building from Source**

When building from source, some dependencies may involve compiling C/C++ code. Ensure that you have the GCC/G++ or Clang toolchain installed on your computer.

```bash
cargo install bendsql
```

## User Authentication

If you are connecting to a self-hosted Databend instance, you can use the admin users specified in the [databend-query.toml](https://github.com/databendlabs/databend/blob/main/scripts/distribution/configs/databend-query.toml) configuration file, or you can connect using an SQL user created with the [CREATE USER](/tidb-cloud-lake/sql/create-user.md) command.

For connections to Databend Cloud, you can use the default `cloudapp` user or an SQL user created with the [CREATE USER](/tidb-cloud-lake/sql/create-user.md) command. Please note that the user account you use to log in to the [Databend Cloud console](https://app.databend.com) cannot be used for connecting to Databend Cloud.

## Connecting with BendSQL

BendSQL allows you to connect to both Databend Cloud and self-hosted Databend instances.

### Customize Connections with a DSN 

A DSN (Data Source Name) is a simple yet powerful way to configure and manage your Databend connection in BendSQL using a single URI-style string. This method allows you to embed your credentials and connection settings directly into your environment, streamlining the connection process.

#### DSN Format and Parameters

```bash title='DSN Format'
databend[+flight]://user[:password]@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

| Common DSN Parameters | Description                          |
|-----------------------|--------------------------------------|
| `tenant`              | Tenant ID, Databend Cloud only.      |
| `warehouse`           | Warehouse name, Databend Cloud only. |
| `sslmode`             | Set to `disable` if not using TLS.   |
| `tls_ca_file`         | Custom root CA certificate path.     |
| `connect_timeout`     | Connect timeout in seconds.          |

| RestAPI Client Parameters   | Description                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `wait_time_secs`            | Request wait time for page, default is `1`.                                                                                   |
| `max_rows_in_buffer`        | Maximum rows for page buffer.                                                                                                 |
| `max_rows_per_page`         | Maximum response rows for a single page.                                                                                      |
| `page_request_timeout_secs` | Timeout for a single page request, default is `30`.                                                                           |
| `presign`                   | Enable presign for data loading. Options: `auto`, `detect`, `on`, `off`. Default is `auto` (only enabled for Databend Cloud). |

| FlightSQL Client Parameters | Description                                                          |
|-----------------------------|----------------------------------------------------------------------|
| `query_timeout`             | Query timeout in seconds.                                            |
| `tcp_nodelay`               | Defaults to `true`.                                                  |
| `tcp_keepalive`             | TCP keepalive in seconds (default is `3600`, set to `0` to disable). |
| `http2_keep_alive_interval` | Keep-alive interval in seconds, default is `300`.                    |
| `keep_alive_timeout`        | Keep-alive timeout in seconds, default is `20`.                      |
| `keep_alive_while_idle`     | Defaults to `true`.                                                  |

#### DSN Examples

```bash
# Local connection using HTTP API with presign detection
databend://root:@localhost:8000/?sslmode=disable&presign=detect

# Databend Cloud connection with tenant and warehouse info
databend://user1:password1@tnxxxx--default.gw.aws-us-east-2.default.databend.com:443/benchmark?enable_dphyp=1

# Local connection using FlightSQL API
databend+flight://root:@localhost:8900/database1?connect_timeout=10
```

### Connect to Databend Cloud

The best practice for connecting to Databend Cloud is to obtain your DSN from Databend Cloud and export it as an environment variable. To obtain your DSN:

1. Log in to Databend Cloud and click **Connect** on the **Overview** page.

2. Select the database and warehouse you want to connect to.

3. Your DSN will be automatically generated in the **Examples** section. Below the DSN, you'll find a BendSQL snippet that exports the DSN as an environment variable named `BENDSQL_DSN` and launches BendSQL with the correct configuration. You can copy and paste it directly into your terminal.

  ```bash title='Example'
  export BENDSQL_DSN="databend://cloudapp:******@tn3ftqihs.gw.aws-us-east-2.default.databend.com:443/information_schema?warehouse=small-xy2t"
  bendsql
  ```

### Connect to Self-hosted Databend

You can connect to a self-hosted Databend instance using either BendSQL command-line arguments or a DSN.

#### Option 1: Use BendSQL Arguments

```bash
bendsql --host <HOST> --port <PORT> --user <USER> --password <PASSWORD> --database <DATABASE>
```

This example connects to a Databend instance running locally on port `8000` using `eric` as the user:

```bash title='Example'
bendsql --host 127.0.0.1 --port 8000 --user eric --password abc123
```

#### Option 2: Use a DSN

You can also define the connection using a DSN and export it as the `BENDSQL_DSN` environment variable:

```bash title='Example'
export BENDSQL_DSN="databend://eric:abc123@localhost:8000/?sslmode=disable"
bendsql
```

## BendSQL Settings

BendSQL provides a range of settings that allow you to define how query results are presented:

| Setting              | Description                                                                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `display_pretty_sql` | When set to `true`, SQL queries will be formatted in a visually appealing manner, making them easier to read and understand.                                |
| `prompt`             | The prompt displayed in the command line interface, typically indicating the user, warehouse, and database being accessed.                                  |
| `progress_color`     | Specifies the color used for progress indicators, such as when executing queries that take some time to complete.                                           |
| `show_progress`      | When set to `true`, progress indicators will be displayed to show the progress of long-running queries or operations.                                       |
| `show_stats`         | If `true`, query statistics such as execution time, rows read, and bytes processed will be displayed after executing each query.                            |
| `max_display_rows`   | Sets the maximum number of rows that will be displayed in the output of a query result.                                                                     |
| `max_col_width`      | Sets the maximum width in characters of each column's display rendering. A value smaller than 3 disables the limit.                                         |
| `max_width`          | Sets the maximum width in characters of the entire display output. A value of 0 defaults to the width of the terminal window.                               |
| `output_format`      | Sets the format used to display query results (`table`, `csv`, `tsv`, `null`).                                                                              |
| `expand`             | Controls whether the output of a query is displayed as individual records or in a tabular format. Available values: `on`, `off`, and `auto`.                |
| `multi_line`         | Determines whether multi-line input for SQL queries is allowed. When set to `true`, queries can span multiple lines for better readability.                 |
| `replace_newline`    | Specifies whether newline characters in the output of query results should be replaced with spaces. This can prevent unintended line breaks in the display. |

For details of each setting, please refer to the reference information below:

#### `display_pretty_sql`

The `display_pretty_sql` setting controls whether SQL queries are displayed in a visually formatted manner or not. When set to `false`, as in the first query below, SQL queries are not formatted for visual appeal. In contrast, when set to `true`, as in the second query, SQL queries are formatted in a visually appealing manner, making them easier to read and understand.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set display_pretty_sql false
root@localhost:8000/default> SELECT TO_STRING(ST_ASGEOJSON(ST_GEOMETRYFROMWKT('SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'))) AS pipeline_geojson;
┌─────────────────────────────────────────────────────────────────────────┐
│                             pipeline_geojson                            │
│                                  String                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ {"coordinates":[[400000,6000000],[401000,6010000]],"type":"LineString"} │
└─────────────────────────────────────────────────────────────────────────┘
1 row read in 0.063 sec. Processed 1 row, 1 B (15.76 rows/s, 15 B/s)

// highlight-next-line
root@localhost:8000/default> !set display_pretty_sql true
root@localhost:8000/default> SELECT TO_STRING(ST_ASGEOJSON(ST_GEOMETRYFROMWKT('SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'))) AS pipeline_geojson;

SELECT
  TO_STRING(
    ST_ASGEOJSON(
      ST_GEOMETRYFROMWKT(
        'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
      )
    )
  ) AS pipeline_geojson

┌─────────────────────────────────────────────────────────────────────────┐
│                             pipeline_geojson                            │
│                                  String                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ {"coordinates":[[400000,6000000],[401000,6010000]],"type":"LineString"} │
└─────────────────────────────────────────────────────────────────────────┘
1 row read in 0.087 sec. Processed 1 row, 1 B (11.44 rows/s, 11 B/s)
```

#### `prompt`

The `prompt` setting controls the format of the command line interface prompt. In the example below, it was initially set to display the user and warehouse (`{user}@{warehouse}`). After updating it to `{user}@{warehouse}/{database}`, the prompt now includes the user, warehouse, and database.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set prompt {user}@{warehouse}
root@localhost:8000 !configs
Settings {
    display_pretty_sql: true,
    prompt: "{user}@{warehouse}",
    progress_color: "cyan",
    show_progress: true,
    show_stats: true,
    max_display_rows: 40,
    max_col_width: 1048576,
    max_width: 1048576,
    output_format: Table,
    quote_style: Necessary,
    expand: Off,
    time: None,
    multi_line: true,
    replace_newline: true,
}
// highlight-next-line
root@localhost:8000 !set prompt {user}@{warehouse}/{database}
root@localhost:8000/default
```

#### `progress_color`

The `progress_color` setting controls the color used for progress indicators during query execution. In this example, the color has been set to `blue`:

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set progress_color blue
```

#### `show_progress`

When set to `true`, progress information is displayed during the execution of a query. The progress information includes the number of rows processed, the total number of rows in the query, the processing speed in rows per second, the amount of memory processed, and the processing speed in memory per second.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set show_progress true
root@localhost:8000/default> select * from numbers(1000000000000000);
⠁ [00:00:08] Processing 18.02 million/1 quadrillion (2.21 million rows/s), 137.50 MiB/7.11 PiB (16.88 MiB/s) ░
```

#### `show_stats`

The `show_stats` setting controls whether query statistics are displayed after executing each query. When set to `false`, as the first query in the example below, query statistics are not displayed. In contrast, when set to `true`, as in the second query, query statistics such as execution time, rows read, and bytes processed are displayed after executing each query.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set show_stats false
root@localhost:8000/default> select now();
┌────────────────────────────┐
│            now()           │
│          Timestamp         │
├────────────────────────────┤
│ 2024-04-23 23:27:11.538673 │
└────────────────────────────┘
// highlight-next-line
root@localhost:8000/default> !set show_stats true
root@localhost:8000/default> select now();
┌────────────────────────────┐
│            now()           │
│          Timestamp         │
├────────────────────────────┤
│ 2024-04-23 23:49:04.754296 │
└────────────────────────────┘
1 row read in 0.045 sec. Processed 1 row, 1 B (22.26 rows/s, 22 B/s)
```

#### `max_display_rows`

The `max_display_rows` setting controls the maximum number of rows displayed in the output of a query result. When set to `5` in the example below, only up to 5 rows are displayed in the query result. The remaining rows are indicated with (5 shown).

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set max_display_rows 5
root@localhost:8000/default> SELECT * FROM system.configs;
┌──────────────────────────────────────────────────────┐
│   group   │       name       │  value  │ description │
│   String  │      String      │  String │    String   │
├───────────┼──────────────────┼─────────┼─────────────┤
│ query     │ tenant_id        │ default │             │
│ query     │ cluster_id       │ default │             │
│ query     │ num_cpus         │ 0       │             │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ storage   │ cos.endpoint_url │         │             │
│ storage   │ cos.root         │         │             │
│ 176 rows  │                  │         │             │
│ (5 shown) │                  │         │             │
└──────────────────────────────────────────────────────┘
176 rows read in 0.059 sec. Processed 176 rows, 10.36 KiB (2.98 thousand rows/s, 175.46 KiB/s)
```

#### `max_col_width` & `max_width`

The settings `max_col_width` and `max_width` specify the maximum permitted width in characters for individual columns and the entire display output, respectively. The following example sets column display width to 10 characters and the entire display width to 100 characters:

```sql title='Example:'
// highlight-next-line
root@localhost:8000/default> .max_col_width 10
// highlight-next-line
root@localhost:8000/default> .max_width 100
root@localhost:8000/default> select * from system.settings;
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│    name    │  value  │ default │   range  │  level  │            description            │  type  │
│   String   │  String │  String │  String  │  String │               String              │ String │
├────────────┼─────────┼─────────┼──────────┼─────────┼───────────────────────────────────┼────────┤
│ acquire... │ 15      │ 15      │ None     │ DEFAULT │ Sets the maximum timeout in se... │ UInt64 │
│ aggrega... │ 0       │ 0       │ None     │ DEFAULT │ Sets the maximum amount of mem... │ UInt64 │
│ aggrega... │ 0       │ 0       │ [0, 100] │ DEFAULT │ Sets the maximum memory ratio ... │ UInt64 │
│ auto_co... │ 50      │ 50      │ None     │ DEFAULT │ Threshold for triggering auto ... │ UInt64 │
│ collation  │ utf8    │ utf8    │ ["utf8"] │ DEFAULT │ Sets the character collation. ... │ String │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ storage... │ 1048576 │ 1048576 │ None     │ DEFAULT │ Sets the byte size of the buff... │ UInt64 │
│ table_l... │ 10      │ 10      │ None     │ DEFAULT │ Sets the seconds that the tabl... │ UInt64 │
│ timezone   │ UTC     │ UTC     │ None     │ DEFAULT │ Sets the timezone.                │ String │
│ unquote... │ 0       │ 0       │ None     │ DEFAULT │ Determines whether Databend tr... │ UInt64 │
│ use_par... │ 0       │ 0       │ [0, 1]   │ DEFAULT │ This setting is deprecated        │ UInt64 │
│ 96 rows    │         │         │          │         │                                   │        │
│ (10 shown) │         │         │          │         │                                   │        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
96 rows read in 0.040 sec. Processed 96 rows, 16.52 KiB (2.38 thousand rows/s, 410.18 KiB/s)
```

#### `output_format`

By setting the `output_format` to `table`, `csv`, `tsv`, or `null`, you can control the format of the query result. The `table` format presents the result in a tabular format with column headers, while the `csv` and `tsv` formats provide comma-separated values and tab-separated values respectively, and the `null` format suppresses the output formatting altogether.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set output_format table
root@localhost:8000/default> show users;
┌────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │  auth_type  │ is_configured │  default_role │ disabled │
│ String │  String  │    String   │     String    │     String    │  Boolean │
├────────┼──────────┼─────────────┼───────────────┼───────────────┼──────────┤
│ root   │ %        │ no_password │ YES           │ account_admin │ false    │
└────────────────────────────────────────────────────────────────────────────┘
1 row read in 0.032 sec. Processed 1 row, 113 B (31.02 rows/s, 3.42 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format csv
root@localhost:8000/default> show users;
root,%,no_password,YES,account_admin,false
1 row read in 0.062 sec. Processed 1 row, 113 B (16.03 rows/s, 1.77 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format tsv
root@localhost:8000/default> show users;
root	%	no_password	YES	account_admin	false
1 row read in 0.076 sec. Processed 1 row, 113 B (13.16 rows/s, 1.45 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format null
root@localhost:8000/default> show users;
1 row read in 0.036 sec. Processed 1 row, 113 B (28.1 rows/s, 3.10 KiB/s)
```

#### `expand`

The `expand` setting controls whether the output of a query is displayed as individual records or in a tabular format. When the `expand` setting is set to `auto`, the system automatically determines how to display the output based on the number of rows returned by the query. If the query returns only one row, the output is displayed as a single record.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set expand on
root@localhost:8000/default> show users;
-[ RECORD 1 ]-----------------------------------
         name: root
     hostname: %
    auth_type: no_password
is_configured: YES
 default_role: account_admin
     disabled: false

1 row read in 0.055 sec. Processed 1 row, 113 B (18.34 rows/s, 2.02 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set expand off
root@localhost:8000/default> show users;
┌────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │  auth_type  │ is_configured │  default_role │ disabled │
│ String │  String  │    String   │     String    │     String    │  Boolean │
├────────┼──────────┼─────────────┼───────────────┼───────────────┼──────────┤
│ root   │ %        │ no_password │ YES           │ account_admin │ false    │
└────────────────────────────────────────────────────────────────────────────┘
1 row read in 0.046 sec. Processed 1 row, 113 B (21.62 rows/s, 2.39 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set expand auto
root@localhost:8000/default> show users;
-[ RECORD 1 ]-----------------------------------
         name: root
     hostname: %
    auth_type: no_password
is_configured: YES
 default_role: account_admin
     disabled: false

1 row read in 0.037 sec. Processed 1 row, 113 B (26.75 rows/s, 2.95 KiB/s)
```

#### `multi_line`

When the `multi_line` setting is set to `true`, allowing input to be entered across multiple lines. As a result, the SQL query is entered with each clause on a separate line for improved readability and organization.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set multi_line true;
root@localhost:8000/default> SELECT *
> FROM system.configs;
┌──────────────────────────────────────────────────────┐
│   group   │       name       │  value  │ description │
│   String  │      String      │  String │    String   │
├───────────┼──────────────────┼─────────┼─────────────┤
│ query     │ tenant_id        │ default │             │
│ query     │ cluster_id       │ default │             │
│ query     │ num_cpus         │ 0       │             │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ storage   │ cos.endpoint_url │         │             │
│ storage   │ cos.root         │         │             │
│ 176 rows  │                  │         │             │
│ (5 shown) │                  │         │             │
└──────────────────────────────────────────────────────┘
176 rows read in 0.060 sec. Processed 176 rows, 10.36 KiB (2.91 thousand rows/s, 171.39 KiB/s)
```

#### `replace_newline`

The `replace_newline` setting determines whether newline characters (\n) are replaced with the literal string (\\n) in the output. In the example below, the `replace_newline` setting is set to `true`. As a result, when the string 'Hello\nWorld' is selected, the newline character (\n) is replaced with the literal string (\\n). So, instead of displaying the newline character, the output displays 'Hello\nWorld' as 'Hello\\nWorld':

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set replace_newline true
root@localhost:8000/default> SELECT 'Hello\nWorld' AS message;
┌──────────────┐
│    message   │
│    String    │
├──────────────┤
│ Hello\nWorld │
└──────────────┘
1 row read in 0.056 sec. Processed 1 row, 1 B (18 rows/s, 17 B/s)

// highlight-next-line
root@localhost:8000/default> !set replace_newline false;
root@localhost:8000/default> SELECT 'Hello\nWorld' AS message;
┌─────────┐
│ message │
│  String │
├─────────┤
│ Hello   │
│ World   │
└─────────┘
1 row read in 0.067 sec. Processed 1 row, 1 B (14.87 rows/s, 14 B/s)
```

### Configuring BendSQL Settings

You have the following options to configure a BendSQL setting:

- Use the `!set <setting> <value>` command. For more information, see [Utility Commands](#utility-commands).

- Add and configure a setting in the configuration file `~/.config/bendsql/config.toml`. To do so, open the file and add your setting under the `[settings]` section. The following example sets the `max_display_rows` to 10 and `max_width` to 100:

```toml title='Example:'
...
[settings]
max_display_rows = 10
max_width = 100
...
```

- Configure a setting at runtime by launching BendSQL and then specifying the setting in the format `.<setting> <value>`. Please note that settings configured in this way only take effect in the current session.

```shell title='Example:'
root@localhost:8000/default> .max_display_rows 10
root@localhost:8000/default> .max_width 100
```

## Utility Commands

BendSQL provides users with a variety of commands to streamline their workflow and customize their experience. Here's an overview of the commands available in BendSQL:

| Command                  | Description                        |
| ------------------------ | ---------------------------------- |
| `!exit`                  | Exits BendSQL.                     |
| `!quit`                  | Exits BendSQL.                     |
| `!configs`               | Displays current BendSQL settings. |
| `!set <setting> <value>` | Modifies a BendSQL setting.        |
| `!source <sql_file>`     | Executes a SQL file.               |

For examples of each command, please refer to the reference information below:

#### `!exit`

Disconnects from Databend and exits BendSQL.

```shell title='Example:'
➜  ~ bendsql
Welcome to BendSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to Databend Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !exit
Bye~
```

#### `!quit`

Disconnects from Databend and exits BendSQL.

```shell title='Example:'
➜  ~ bendsql
Welcome to BendSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to Databend Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !quit
Bye~
➜  ~
```

#### `!configs`

Displays the current BendSQL settings.

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !configs
Settings {
    display_pretty_sql: true,
    prompt: "{user}@{warehouse}/{database}> ",
    progress_color: "cyan",
    show_progress: true,
    show_stats: true,
    max_display_rows: 40,
    max_col_width: 1048576,
    max_width: 1048576,
    output_format: Table,
    quote_style: Necessary,
    expand: Off,
    time: None,
    multi_line: true,
    replace_newline: true,
}
```

#### `!set <setting> <value>`

Modifies a BendSQL setting.

```shell title='Example:'
root@localhost:8000/default> !set display_pretty_sql false
```

#### `!source <sql_file>`

Executes a SQL file.

```shell title='Example:'
➜  ~ more ./desktop/test.sql
CREATE TABLE test_table (
    id INT,
    name VARCHAR(50)
);

INSERT INTO test_table (id, name) VALUES (1, 'Alice');
INSERT INTO test_table (id, name) VALUES (2, 'Bob');
INSERT INTO test_table (id, name) VALUES (3, 'Charlie');
➜  ~ bendsql
Welcome to BendSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to Databend Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !source ./desktop/test.sql
root@localhost:8000/default> SELECT * FROM test_table;

SELECT
  *
FROM
  test_table

┌────────────────────────────────────┐
│        id       │       name       │
│ Nullable(Int32) │ Nullable(String) │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
│               3 │ Charlie          │
└────────────────────────────────────┘
3 rows read in 0.064 sec. Processed 3 rows, 81 B (46.79 rows/s, 1.23 KiB/s)
```
