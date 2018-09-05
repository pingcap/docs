---
title: Bikeshare Example Database
summary: Install the Bikeshare Example Database
---

# Bikeshare Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from 
Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

## Downloading all data files

To download and extract all previous years in one step (using a bash script).  This requires approximately 3GB of disk space:

```

mkdir -p bikeshare-data && cd bikeshare-data

for YEAR in 2010 2011 2012 2013 2014 2015 2016 2017; do
 wget https://s3.amazonaws.com/capitalbikeshare-data/${YEAR}-capitalbikeshare-tripdata.zip
 unzip ${YEAR}-capitalbikeshare-tripdata.zip
done;

```

## Create table in TiDB

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

### Import all files

To import all `*.csv` files into TiDB in a bash loop:

```
for FILE in `ls *.csv`; do
 echo "== $FILE =="
 mysql bikeshare -e "LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
(duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```
