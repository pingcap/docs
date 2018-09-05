---
title: Bikeshare Example Database
summary: Install the Bikeshare Example Database
---

# Bikeshare Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from 
Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

## Downloading all data files

To download and extract all previous years in one step (using a bash script):

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

);
```

### Import all files

To import all *.csv files into TiDB in a bash loop:

```
for FILE in `ls *.csv`; do

done;
``
