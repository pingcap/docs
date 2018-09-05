---
title: Bikeshare Example Database
summary: Install the Bikeshare Example Database
---

# Bikeshare Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from 
Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

Installation of the sample database can be automated as follows:

```

for YEAR in "2010 2011 2012 2013 2014 2015 2016 2017"; do
 wget https://s3.amazonaws.com/capitalbikeshare-data/$YEAR-capitalbikeshare-tripdata.zip
 unzip $YEAR-capitalbikeshare-tripdata.zip
done;

```
