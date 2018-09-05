---
title: Bikeshare Example Database
summary: Install the Bikeshare Example Database
---

# Bikeshare Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from 
Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

## Downloading all data files

The system data is available [for download](https://s3.amazonaws.com/capitalbikeshare-data/index.html) in zip files organized per year.  Downloading and extracting all files requires approximately 3GB of disk space.  To download all files at once using a bash script:

```

mkdir -p bikeshare-data && cd bikeshare-data

for YEAR in 2010 2011 2012 2013 2014 2015 2016 2017; do
 wget https://s3.amazonaws.com/capitalbikeshare-data/${YEAR}-capitalbikeshare-tripdata.zip
 unzip ${YEAR}-capitalbikeshare-tripdata.zip
done;

```

## Load data into MySQL

The system data can be imported to MySQL using the following schema:

```
CREATE DATABASE bikeshare;
USE bikeshare;

CREATE TABLE trips (
 trip_id bigint NOT NULL PRIMARY KEY auto_increment,
 duration integer not null,
 start_date datetime,
 end_date datetime,
 start_station_number integer,
 start_station varchar(255),
 end_station_number integer,
 end_station varchar(255),
 bike_number varchar(255),
 member_type varchar(255)
);
```
You can import files indivudally using the example `LOAD DATA` command here, or import all files using the bash loop below:

```
LOAD DATA LOCAL INFILE '2017Q1-capitalbikeshare-tripdata.csv' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
(duration, start_date, end_date, start_station_number, start_station, 
end_station_number, end_station, bike_number, member_type);
```

### Import all files

To import all `*.csv` files into TiDB in a bash loop:

```
for FILE in `ls *.csv`; do
 echo "== $FILE =="
 mysql bikeshare -e "LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```
