---
title: Import Example Database
summary: Install the Bikeshare example database.
---

# Import Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

## Download all data files

The system data is available [for download in .zip files](https://s3.amazonaws.com/capitalbikeshare-data/index.html) organized per year. Downloading and extracting all files requires approximately 3GB of disk space. To download all files for years 2010-2017 using a bash script:

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## Load data into TiDB

You can import the system data into TiDB using the following method.

1. Rename the CSV files.

    ```bash
    i=1; for csv in *csv; do mv $csv bikeshare.trips.$(printf "%03d" $i).csv; i=$((i+1)); done
    ```

2. Create the database and table.

    ```sql
    CREATE SCHEMA bikeshare;
    USE bikeshare;
    CREATE TABLE trips (
      `trip_id` BIGINT NOT NULL PRIMARY KEY AUTO_RANDOM,
      `duration` INT NOT NULL,
      `start date` DATETIME,
      `end date` DATETIME,
      `start station number` INT,
      `start station` VARCHAR(255),
      `end station number` INT,
      `end station` VARCHAR(255),
      `bike number` VARCHAR(255),
      `member type` VARCHAR(255)
    );
    ```

3. Create a `tidb-lightning.toml` file as follows:

    ```toml
    [tikv-importer]
    backend = "tidb"

    [mydumper]
    no-schema = true
    data-source-dir = "~/bikeshare-data"

    [mydumper.csv]
    header = true

    [tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = "very_secret"
    ```

4. Run the following command.

    ```shell
    tiup tidb-lightning -c tidb-lightning.toml
    ```
