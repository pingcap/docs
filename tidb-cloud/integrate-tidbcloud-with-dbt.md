---
title: Integrate TiDB Cloud with dbt
summary: TiDB Cloudにおけるdbtのユースケースについて学びましょう。
---

# TiDB Cloudとdbtを統合する {#integrate-tidb-cloud-with-dbt}

データ[データ構築ツール（dbt）](https://www.getdbt.com/)は、分析エンジニアがSQL文を使用してデータウェアハウス内のデータを変換するのに役立つ、人気の高いオープンソースのデータ変換ツールです。dbt [dbt-tidb](https://github.com/pingcap/dbt-tidb)プラグインを使用すると、 TiDB Cloudを使用する分析エンジニアは、テーブルやビューの作成プロセスを気にすることなく、SQLを使用してフォームを直接作成し、データを照合できます。

このドキュメントでは、dbtプロジェクトを例として、 TiDB Cloudでdbtを使用する方法を紹介します。

## ステップ1：dbtとdbt-tidbをインストールする {#step-1-install-dbt-and-dbt-tidb}

dbtとdbt-tidbは、たった1つのコマンドでインストールできます。以下のコマンドでは、dbt-tidbをインストールする際に、dbtが依存関係としてインストールされます。

```shell
pip install dbt-tidb
```

dbt を個別にインストールすることもできます。 dbt ドキュメントの[dbtのインストール方法](https://docs.getdbt.com/docs/get-started/installation)参照してください。

## ステップ2：デモプロジェクトを作成する {#step-2-create-a-demo-project}

dbt の機能を試すには、dbt-lab が提供するデモプロジェクト[ジャッフルショップ](https://github.com/dbt-labs/jaffle_shop)を利用できます。 GitHub から直接プロジェクトのクローンを作成できます。

```shell
git clone https://github.com/dbt-labs/jaffle_shop && \
cd jaffle_shop
```

`jaffle_shop`ディレクトリ内のすべてのファイルは、次のように構成されています。

```shell
.
├── LICENSE
├── README.md
├── dbt_project.yml
├── etc
│    ├── dbdiagram_definition.txt
│    └── jaffle_shop_erd.png
├── models
│    ├── customers.sql
│    ├── docs.md
│    ├── orders.sql
│    ├── overview.md
│    ├── schema.yml
│    └── staging
│        ├── schema.yml
│        ├── stg_customers.sql
│        ├── stg_orders.sql
│        └── stg_payments.sql
└── seeds
    ├── raw_customers.csv
    ├── raw_orders.csv
    └── raw_payments.csv
```

このディレクトリ内:

-   `dbt_project.yml`は dbt プロジェクト構成ファイルであり、プロジェクト名とデータベース構成ファイルの情報が含まれています。

-   `models`ディレクトリには、プロジェクトの SQL モデルとテーブル スキーマが含まれています。このセクションはデータ アナリストが作成します。モデルの詳細については、 [SQLモデル](https://docs.getdbt.com/docs/build/sql-models)を参照してください。

-   `seeds`ディレクトリには、データベース エクスポート ツールによってダンプされた CSV ファイルが保存されます。たとえば、 Dumplingを通じて[TiDB Cloudデータをエクスポートする](https://docs.pingcap.com/tidbcloud/export-data-from-tidb-cloud)できます。 `jaffle_shop`プロジェクトでは、これらの CSV ファイルが処理される生データとして使用されます。

## ステップ3：プロジェクトの設定 {#step-3-configure-the-project}

プロジェクトを設定するには、以下の手順に従ってください。

1.  グローバル設定を完了してください。

    [プロフィール項目の説明](#description-of-profile-fields)を参照し、デフォルトのグローバル プロファイル`~/.dbt/profiles.yml`編集して、 TiDB Cloudとの接続を構成できます。

    ```shell
    sudo vi ~/.dbt/profiles.yml
    ```

    エディタで、以下の設定を追加します。

    ```yaml
     jaffle_shop_tidb:                                                 # Project name
       target: dev                                                     # Target
       outputs:
         dev:
           type: tidb                                                  # The specific adapter to use
           server: gateway01.ap-southeast-1.prod.aws.tidbcloud.com     # The TiDB Cloud clusters' endpoint to connect to
           port: 4000                                                  # The port to use
           schema: analytics                                           # Specify the schema (database) to normalize data into
           username: xxxxxxxxxxx.root                                  # The username to use to connect to the TiDB Cloud clusters
           password: "your_password"                                   # The password to use for authenticating to the TiDB Cloud clusters
    ```

    TiDB Cloud コンソールの接続ダイアログから`server` 、 `port` 、および`username`の値を取得できます。ダイアログを開くには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットの<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターの名前をクリックして概要ページに移動し、右上隅の**Connect**をクリックします。

2.  プロジェクトの設定を完了してください。

    jaffle_shop プロジェクトディレクトリで、プロジェクト設定ファイル`dbt_project.yml`を編集し、 `profile`フィールドを`jaffle_shop_tidb`に変更します。この設定により、プロジェクトは`~/.dbt/profiles.yml`ファイルで指定されているとおりにデータベースからクエリを実行できるようになります。

    ```shell
    vi dbt_project.yml
    ```

    エディタで、以下のように設定を更新してください。

    ```yaml
    name: 'jaffle_shop'

    config-version: 2
    version: '0.1'

    profile: 'jaffle_shop_tidb'                   # note the modification here

    model-paths: ["models"]                       # model path
    seed-paths: ["seeds"]                         # seed path
    test-paths: ["tests"]
    analysis-paths: ["analysis"]
    macro-paths: ["macros"]

    target-path: "target"
    clean-targets:
        - "target"
        - "dbt_modules"
        - "logs"

    require-dbt-version: [">=1.0.0", "<2.0.0"]

    models:
      jaffle_shop:
          materialized: table            # *.sql which in models/ would be materialized to table
          staging:
            materialized: view           # *.sql which in models/staging/ would bt materialized to view
    ```

3.  設定を確認してください。

    以下のコマンドを実行して、データベースとプロジェクトの設定が正しいかどうかを確認してください。

    ```shell
    dbt debug
    ```

## ステップ4：（オプション）CSVファイルを読み込む {#step-4-optional-load-csv-files}

> **注記：**
>
> この手順は任意です。処理対象のデータが既にターゲットデータベースに存在する場合は、この手順をスキップできます。

プロジェクトの作成と設定が完了したので、次はCSVデータをロードし、ターゲットデータベースにCSVをテーブルとして具体化する段階です。

1.  CSVデータを読み込み、対象データベースにテーブルとしてCSVデータを作成します。

    ```shell
    dbt seed
    ```

    以下は出力例です。

    ```shell
    Running with dbt=1.0.1
    Partial parse save file not found. Starting full parse.
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 172 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 3 START seed file analytics.raw_customers.................................. [RUN]
    1 of 3 OK loaded seed file analytics.raw_customers.............................. [INSERT 100 in 0.19s]
    2 of 3 START seed file analytics.raw_orders..................................... [RUN]
    2 of 3 OK loaded seed file analytics.raw_orders................................. [INSERT 99 in 0.14s]
    3 of 3 START seed file analytics.raw_payments................................... [RUN]
    3 of 3 OK loaded seed file analytics.raw_payments............................... [INSERT 113 in 0.24s]
    ```

    結果からわかるように、シードファイルが起動され、 `analytics.raw_customers` 、 `analytics.raw_orders` 、および`analytics.raw_payments` 。

2.  TiDB Cloudで結果を確認してください。

    `show databases`コマンドは、dbt が作成した新しい`analytics`データベースを一覧表示します。 `show tables`コマンドは、 `analytics`データベースに、作成したテーブルに対応する 3 つのテーブルが存在することを示します。

    ```sql
    mysql> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | INFORMATION_SCHEMA |
    | METRICS_SCHEMA     |
    | PERFORMANCE_SCHEMA |
    | analytics          |
    | io_replicate       |
    | mysql              |
    | test               |
    +--------------------+
    7 rows in set (0.00 sec)

    mysql> USE ANALYTICS;
    mysql> SHOW TABLES;
    +---------------------+
    | Tables_in_analytics |
    +---------------------+
    | raw_customers       |
    | raw_orders          |
    | raw_payments        |
    +---------------------+
    3 rows in set (0.00 sec)

    mysql> SELECT * FROM raw_customers LIMIT 10;
    +------+------------+-----------+
    | id   | first_name | last_name |
    +------+------------+-----------+
    |    1 | Michael    | P.        |
    |    2 | Shawn      | M.        |
    |    3 | Kathleen   | P.        |
    |    4 | Jimmy      | C.        |
    |    5 | Katherine  | R.        |
    |    6 | Sarah      | R.        |
    |    7 | Martin     | M.        |
    |    8 | Frank      | R.        |
    |    9 | Jennifer   | F.        |
    |   10 | Henry      | W.        |
    +------+------------+-----------+
    10 rows in set (0.10 sec)
    ```

## ステップ5：データの変換 {#step-5-transform-data}

これで、設定済みのプロジェクトを実行してデータ変換を完了する準備が整いました。

1.  データ変換を完了するには、dbtプロジェクトを実行してください。

    ```shell
    dbt run
    ```

    以下は出力例です。

    ```shell
    Running with dbt=1.0.1
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 170 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 5 START view model analytics.stg_customers................................. [RUN]
    1 of 5 OK created view model analytics.stg_customers............................ [SUCCESS 0 in 0.31s]
    2 of 5 START view model analytics.stg_orders.................................... [RUN]
    2 of 5 OK created view model analytics.stg_orders............................... [SUCCESS 0 in 0.23s]
    3 of 5 START view model analytics.stg_payments.................................. [RUN]
    3 of 5 OK created view model analytics.stg_payments............................. [SUCCESS 0 in 0.29s]
    4 of 5 START table model analytics.customers.................................... [RUN]
    4 of 5 OK created table model analytics.customers............................... [SUCCESS 0 in 0.76s]
    5 of 5 START table model analytics.orders....................................... [RUN]
    5 of 5 OK created table model analytics.orders.................................. [SUCCESS 0 in 0.63s]

    Finished running 3 view models, 2 table models in 2.27s.

    Completed successfully

    Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5
    ```

    結果によると、2 つのテーブル ( `analytics.customers`と`analytics.orders` ) と 3 つのビュー ( `analytics.stg_customers` 、 `analytics.stg_orders` 、および`analytics.stg_payments` ) が正常に作成されました。

2.  TiDB Cloudにアクセスして、変換が成功したことを確認してください。

    ```sql
    mysql> USE ANALYTICS;
    mysql> SHOW TABLES;
    +---------------------+
    | Tables_in_analytics |
    +---------------------+
    | customers           |
    | orders              |
    | raw_customers       |
    | raw_orders          |
    | raw_payments        |
    | stg_customers       |
    | stg_orders          |
    | stg_payments        |
    +---------------------+
    8 rows in set (0.00 sec)

    mysql> SELECT * FROM customers LIMIT 10;
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    | customer_id | first_name | last_name | first_order | most_recent_order | number_of_orders | customer_lifetime_value |
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    |           1 | Michael    | P.        | 2018-01-01  | 2018-02-10        |                2 |                 33.0000 |
    |           2 | Shawn      | M.        | 2018-01-11  | 2018-01-11        |                1 |                 23.0000 |
    |           3 | Kathleen   | P.        | 2018-01-02  | 2018-03-11        |                3 |                 65.0000 |
    |           4 | Jimmy      | C.        | NULL        | NULL              |             NULL |                    NULL |
    |           5 | Katherine  | R.        | NULL        | NULL              |             NULL |                    NULL |
    |           6 | Sarah      | R.        | 2018-02-19  | 2018-02-19        |                1 |                  8.0000 |
    |           7 | Martin     | M.        | 2018-01-14  | 2018-01-14        |                1 |                 26.0000 |
    |           8 | Frank      | R.        | 2018-01-29  | 2018-03-12        |                2 |                 45.0000 |
    |           9 | Jennifer   | F.        | 2018-03-17  | 2018-03-17        |                1 |                 30.0000 |
    |          10 | Henry      | W.        | NULL        | NULL              |             NULL |                    NULL |
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    10 rows in set (0.00 sec)
    ```

    出力結果を見ると、新たに5つのテーブルまたはビューが追加され、それらのテーブルまたはビュー内のデータが変換されたことがわかります。この例では、顧客テーブルのデータの一部のみが表示されています。

## ステップ6：ドキュメントを生成する {#step-6-generate-the-document}

dbtを使用すると、プロジェクト全体の構造を表示し、すべてのテーブルとビューを説明する視覚的なドキュメントを生成できます。

視覚的なドキュメントを生成するには、以下の手順に従ってください。

1.  ドキュメントを生成する：

    ```shell
    dbt docs generate
    ```

2.  サーバーを起動します：

    ```shell
    dbt docs serve
    ```

3.  ブラウザからドキュメントにアクセスするには、 [http://localhost:8080](http://localhost:8080)にアクセスしてください。

## プロフィール項目の説明 {#description-of-profile-fields}

| オプション      | 説明                                  | 必須？   | 例                                                 |
| ---------- | ----------------------------------- | ----- | ------------------------------------------------- |
| `type`     | 使用する特定のアダプター                        | 必須    | `tidb`                                            |
| `server`   | 接続するTiDBエンドポイント                     | 必須    | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` |
| `port`     | 使用するポート                             | 必須    | `4000`                                            |
| `schema`   | データを正規化するためのスキーマ（データベース）            | 必須    | `analytics`                                       |
| `username` | TiDB Cloudクラスターに接続するために使用するユーザー名    | 必須    | `xxxxxxxxxxx.root`                                |
| `password` | TiDB Cloudクラスターへの認証に使用するパスワード       | 必須    | `"your_password"`                                 |
| `retries`  | TiDB Cloudクラスターへの接続の再試行回数（デフォルトは1回） | オプション | `2`                                               |

## サポートされている関数 {#supported-functions}

dbt-tidb では、以下の関数を直接使用できます。使用方法については、 [dbt-util](https://github.com/dbt-labs/dbt-utils)参照してください。

以下の関数がサポートされています。

-   `bool_or`
-   `cast_bool_to_text`
-   `dateadd`
-   `datediff` 。なお、 `datediff`は dbt-util とは少し異なります。切り上げではなく切り捨てが行われます。
-   `date_trunc`
-   `hash`
-   `safe_cast`
-   `split_part`
-   `last_day`
-   `cast_bool_to_text`
-   `concat`
-   `escape_single_quotes`
-   `except`
-   `intersect`
-   `length`
-   `position`
-   `replace`
-   `right`
