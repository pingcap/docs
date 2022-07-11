---
title: Import Example Database
summary: Install the Bikeshare example database.
---

# サンプルデータベースのインポート {#import-example-database}

TiDBマニュアルで使用されている例は、 [CapitalBikeshareデータライセンス契約](https://www.capitalbikeshare.com/data-license-agreement)の下でリリースされたCapitalBikeshareの[システムデータ](https://www.capitalbikeshare.com/system-data)を使用しています。

## すべてのデータファイルをダウンロードする {#download-all-data-files}

システムデータは、1年に[.zipファイルでダウンロードする](https://s3.amazonaws.com/capitalbikeshare-data/index.html)編成されて利用できます。すべてのファイルをダウンロードして抽出するには、約3GBのディスク容量が必要です。 bashスクリプトを使用して2010〜2017年のすべてのファイルをダウンロードするには：

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## TiDBにデータをロードする {#load-data-into-tidb}

システムデータは、次のスキーマを使用してTiDBにインポートできます。

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

ここで例`LOAD DATA`のコマンドを使用してファイルを個別にインポートするか、以下のbashループを使用してすべてのファイルをインポートできます。

```sql
SET tidb_dml_batch_size = 20000;
LOAD DATA LOCAL INFILE '2017Q1-capitalbikeshare-tripdata.csv' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
(duration, start_date, end_date, start_station_number, start_station,
end_station_number, end_station, bike_number, member_type);
```

### すべてのファイルをインポートする {#import-all-files}

> **ノート：**
>
> MySQLクライアントを起動するときは、 `--local-infile=1`オプションを使用します。

`*.csv`のファイルすべてをbashループでTiDBにインポートするには：

```bash
for FILE in *.csv; do
 echo "== $FILE =="
 mysql bikeshare --local-infile=1 -e "SET tidb_dml_batch_size = 20000; LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```
