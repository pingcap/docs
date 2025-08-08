---
title: Import Example Database
summary: Bikeshare サンプル データベースをインストールします。
---

# サンプルデータベースのインポート {#import-example-database}

TiDB マニュアルで使用されている例では、 [キャピタル・バイクシェア・データライセンス契約](https://www.capitalbikeshare.com/data-license-agreement)でリリースされた Capital Bikeshare の[システムデータ](https://www.capitalbikeshare.com/system-data)使用されています。

## すべてのデータファイルをダウンロードする {#download-all-data-files}

システムデータは年ごとに[.zipファイルでダウンロード可能](https://s3.amazonaws.com/capitalbikeshare-data/index.html)整理されて提供されます。すべてのファイルをダウンロードして解凍するには、約3GBのディスク容量が必要です。bashスクリプトを使用して2010年から2017年までのすべてのファイルをダウンロードするには、以下のコマンドを実行します。

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## TiDBにデータをロードする {#load-data-into-tidb}

次の方法を使用して、システム データを TiDB にインポートできます。

1.  CSV ファイルの名前を変更します。

    ```bash
    i=1; for csv in *csv; do mv $csv bikeshare.trips.$(printf "%03d" $i).csv; i=$((i+1)); done
    ```

2.  データベースとテーブルを作成します。

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

3.  次のように`tidb-lightning.toml`ファイルを作成します。

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

4.  次のコマンドを実行します。

    ```shell
    tiup tidb-lightning -c tidb-lightning.toml
    ```
