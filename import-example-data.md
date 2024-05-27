---
title: Import Example Database
summary: Bikeshare サンプル データベースをインストールします。
---

# サンプルデータベースのインポート {#import-example-database}

TiDB マニュアルで使用されている例では、 [キャピタル・バイクシェア・データライセンス契約](https://www.capitalbikeshare.com/data-license-agreement)でリリースされた Capital Bikeshare の[システムデータ](https://www.capitalbikeshare.com/system-data)使用されています。

## すべてのデータファイルをダウンロード {#download-all-data-files}

システム データは、1 年ごとに[.zipファイルでダウンロード](https://s3.amazonaws.com/capitalbikeshare-data/index.html)提供されます。すべてのファイルをダウンロードして解凍するには、約 3 GB のディスク領域が必要です。bash スクリプトを使用して 2010 年から 2017 年までのすべてのファイルをダウンロードするには、次の操作を実行します。

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## TiDBにデータをロードする {#load-data-into-tidb}

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

ここでの例`LOAD DATA`コマンドを使用してファイルを個別にインポートすることも、以下の bash ループを使用してすべてのファイルをインポートすることもできます。

```sql
LOAD DATA LOCAL INFILE '2017Q1-capitalbikeshare-tripdata.csv' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
(duration, start_date, end_date, start_station_number, start_station,
end_station_number, end_station, bike_number, member_type);
```

### すべてのファイルをインポート {#import-all-files}

> **注記：**
>
> MySQL クライアントを起動するときは、 `--local-infile=1`オプションを使用します。

bash ループで`*.csv`ファイルすべてを TiDB にインポートするには:

```bash
for FILE in *.csv; do
 echo "== $FILE =="
 mysql bikeshare --local-infile=1 -e "LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```
