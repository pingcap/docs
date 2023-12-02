---
title: Import Example Database
summary: Install the Bikeshare example database.
---

# サンプルデータベースのインポート {#import-example-database}

TiDB マニュアルで使用されている例では、Capital Bikeshare の[Capital Bikeshare データライセンス契約](https://www.capitalbikeshare.com/data-license-agreement)の下でリリースされた[システムデータ](https://www.capitalbikeshare.com/system-data)使用しています。

## すべてのデータ ファイルをダウンロードする {#download-all-data-files}

システムデータは1年に[.zip ファイルでダウンロードする場合](https://s3.amazonaws.com/capitalbikeshare-data/index.html)整理してご利用いただけます。すべてのファイルをダウンロードして解凍するには、約 3GB のディスク容量が必要です。 bash スクリプトを使用して 2010 年から 2017 年のすべてのファイルをダウンロードするには:

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## データを TiDB にロードする {#load-data-into-tidb}

システム データは、次のスキーマを使用して TiDB にインポートできます。

```sql
CREATE DATABASE bikeshare;
USE bikeshare;

CREATE TABLE trips (
 trip_id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
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

ここの例`LOAD DATA`コマンドを使用してファイルを個別にインポートすることも、以下の bash ループを使用してすべてのファイルをインポートすることもできます。

```sql
LOAD DATA LOCAL INFILE '2017Q1-capitalbikeshare-tripdata.csv' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
(duration, start_date, end_date, start_station_number, start_station,
end_station_number, end_station, bike_number, member_type);
```

### すべてのファイルをインポートする {#import-all-files}

> **注記：**
>
> MySQL クライアントを起動するときは、 `--local-infile=1`オプションを使用します。

bash ループですべての`*.csv`ファイルを TiDB にインポートするには:

```bash
for FILE in *.csv; do
 echo "== $FILE =="
 mysql bikeshare --local-infile=1 -e "LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```
