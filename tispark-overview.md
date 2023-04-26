---
title: TiSpark User Guide
summary: Use TiSpark to provide an HTAP solution to serve as a one-stop solution for both online transactions and analysis.
---

# TiSpark ユーザーガイド {#tispark-user-guide}

![TiSpark architecture](/media/tispark-architecture.png)

## TiSpark 対TiFlash {#tispark-vs-tiflash}

[ティスパーク](https://github.com/pingcap/tispark)は、TiDB/TiKV 上で Apache Spark を実行して複雑な OLAP クエリに応答するために構築されたシンレイヤーです。 Spark プラットフォームと分散 TiKV クラスターの両方を利用し、分散 OLTP データベースである TiDB にシームレスに接着して、ハイブリッド トランザクション/分析処理 (HTAP) ソリューションを提供し、オンライン トランザクションと分析の両方のワンストップ ソリューションとして機能します。 .

[TiFlash](/tiflash/tiflash-overview.md)は、HTAP を有効にする別のツールです。 TiFlashと TiSpark の両方で、複数のホストを使用して OLTP データに対して OLAP クエリを実行できます。 TiFlash はデータを列形式で格納するため、より効率的な分析クエリが可能になります。 TiFlashと TiSpark は併用できます。

## TiSparkとは {#what-is-tispark}

TiSpark は、TiKV クラスターと PD クラスターに依存します。また、Spark クラスターをセットアップする必要があります。このドキュメントでは、TiSpark のセットアップ方法と使用方法を簡単に紹介します。 Apache Spark の基本的な知識が必要です。詳細については、 [アパッチスパークのウェブサイト](https://spark.apache.org/docs/latest/index.html)を参照してください。

Spark Catalyst Engine と緊密に統合された TiSpark は、コンピューティングを正確に制御します。これにより、Spark は TiKV から効率的にデータを読み取ることができます。 TiSpark は、高速なポイント クエリを可能にするインデックス シークもサポートしています。 TiSpark は、コンピューティングを TiKV にプッシュすることでデータ クエリを高速化し、Spark SQL によって処理されるデータの量を削減します。一方、TiSpark は TiDB の組み込み統計を使用して、最適なクエリ プランを選択できます。

TiSpark と TiDB を使用すると、ETL を構築して維持することなく、トランザクションと分析の両方のタスクを同じプラットフォームで実行できます。これにより、システムアーキテクチャが簡素化され、メンテナンスのコストが削減されます。

TiDB でのデータ処理には、Spark エコシステムのツールを使用できます。

-   TiSpark: データ分析と ETL
-   TiKV: データ検索
-   スケジューリング システム: レポート生成

また、TiSpark は TiKV への分散書き込みをサポートしています。 Spark および JDBC を使用した TiDB への書き込みと比較して、TiKV への分散書き込みはトランザクションを実装でき (すべてのデータが正常に書き込まれるか、すべての書き込みが失敗する)、書き込みが高速になります。

> **警告：**
>
> TiSpark は TiKV に直接アクセスするため、TiDB サーバーで使用されるアクセス制御メカニズムは TiSpark には適用されません。 TiSpark v2.5.0 以降、TiSpark はユーザー認証と承認をサポートしています。詳細については、 [Security](/tispark-overview.md#security)を参照してください。

## 要件 {#requirements}

-   TiSpark は Spark &gt;= 2.3 をサポートします。
-   TiSpark には JDK 1.8 と Scala 2.11/2.12 が必要です。
-   TiSpark は、 `YARN` 、 `Mesos` 、および`Standalone`などの任意の Spark モードで実行されます。

## Spark の推奨デプロイ構成 {#recommended-deployment-configurations-of-spark}

> **警告：**
>
> この[文書](/tispark-deployment-topology.md)で説明されているように、 TiUP を使用して TiSpark をデプロイすることは推奨されていません。

TiSpark は Spark の TiDB コネクタであるため、使用するには実行中の Spark クラスターが必要です。

このドキュメントでは、Spark のデプロイに関する基本的なアドバイスを提供します。詳細なハードウェアの推奨事項については、 [スパーク公式サイト](https://spark.apache.org/docs/latest/hardware-provisioning.html)を参照してください。

Spark クラスターの独立したデプロイの場合:

-   Spark には 32 GB のメモリを割り当てることをお勧めします。オペレーティング システムとバッファ キャッシュ用に少なくとも 25% のメモリを予約します。
-   Spark では、マシンごとに少なくとも 8 から 16 のコアをプロビジョニングすることをお勧めします。まず、すべての CPU コアを Spark に割り当てる必要があります。

以下は、 `spark-env.sh`構成に基づく例です。

```
SPARK_EXECUTOR_MEMORY = 32g
SPARK_WORKER_MEMORY = 32g
SPARK_WORKER_CORES = 8
```

## TiSpark を入手 {#get-tispark}

TiSpark は、TiKV を読み書きする機能を提供する Spark 用のサードパーティの jar パッケージです。

### mysql-connector-j を入手する {#get-mysql-connector-j}

`mysql-connector-java`依存関係は、GPL ライセンスの制限により提供されなくなりました。

次のバージョンの TiSpark の jar には`mysql-connector-java`が含まれなくなります。

-   TiSpark &gt; 3.0.1
-   TiSpark &gt; TiSpark 2.5.x の場合は 2.5.1
-   TiSpark &gt; TiSpark 2.4.x の場合は 2.4.3

ただし、TiSpark は書き込みと認証に`mysql-connector-java`必要です。このような場合、次のいずれかの方法を使用して手動で`mysql-connector-java`インポートする必要があります。

-   `mysql-connector-java`を spark jars ファイルに入れます。

-   Spark ジョブを送信するときに`mysql-connector-java`インポートします。次の例を参照してください。

```
spark-submit --jars tispark-assembly-3.0_2.12-3.1.0-SNAPSHOT.jar,mysql-connector-java-8.0.29.jar
```

### TiSpark のバージョンを選択 {#choose-tispark-version}

TiDB と Spark のバージョンに応じて、TiSpark のバージョンを選択できます。

| TiSpark バージョン    | TiDB、TiKV、PD版 | スパークバージョン               | Scala バージョン |
| ---------------- | ------------- | ----------------------- | ----------- |
| 2.4.x-scala_2.11 | 5.x、4.x       | 2.3.x、2.4.x             | 2.11        |
| 2.4.x-scala_2.12 | 5.x、4.x       | 2.4.x                   | 2.12        |
| 2.5.x            | 5.x、4.x       | 3.0.x、3.1.x             | 2.12        |
| 3.0.x            | 5.x、4.x       | 3.0.x、3.1.x、3.2.x       | 2.12        |
| 3.1.x            | 6.x、5.x、4.x   | 3.0.x、3.1.x、3.2.x、3.3.x | 2.12        |

TiSpark 2.4.4、2.5.2、3.0.2、および 3.1.1 は最新の安定バージョンであり、強くお勧めします。

### TiSpark jar を入手する {#get-tispark-jar}

次のいずれかの方法を使用して、TiSpark jar を取得できます。

-   [セントラル](https://search.maven.org/)から取得してGroupId [![Maven Search](https://img.shields.io/badge/com.pingcap/tispark-green.svg)](http://search.maven.org/#search%7Cga%7C1%7Cpingcap)で検索
-   [TiSpark リリース](https://github.com/pingcap/tispark/releases)から取得
-   以下の手順でソースからビルドします

> **ノート：**
>
> 現在、TiSpark をビルドするための唯一の選択肢は java8 です。mvn -version を実行して確認してください。

```
git clone https://github.com/pingcap/tispark.git
```

TiSpark ルート ディレクトリで次のコマンドを実行します。

```
// add -Dmaven.test.skip=true to skip the tests
mvn clean install -Dmaven.test.skip=true
// or you can add properties to specify spark version
mvn clean install -Dmaven.test.skip=true -Pspark3.2.1
```

### TiSpark jar のアーティファクト ID {#tispark-jar-s-artifact-id}

TiSpark のアーティファクト ID は、TiSpark のバージョンによって異なります。

| TiSpark バージョン                | アーティファクト ID                                        |
| ---------------------------- | -------------------------------------------------- |
| 2.4.x-${scala_version}、2.5.0 | チスパークアセンブリ                                         |
| 2.5.1                        | tispark-assembly-${spark_version}                  |
| 3.0.x、3.1.x                  | tispark-assembly-${spark_version}-${scala_version} |

## 入門 {#getting-started}

このドキュメントでは、spark-shell で TiSpark を使用する方法について説明します。

### スパークシェルを開始 {#start-spark-shell}

spark-shell で TiSpark を使用するには:

`spark-defaults.conf`に次の構成を追加します。

```
spark.sql.extensions  org.apache.spark.sql.TiExtensions
spark.tispark.pd.addresses  ${your_pd_adress}
spark.sql.catalog.tidb_catalog  org.apache.spark.sql.catalyst.catalog.TiCatalog
spark.sql.catalog.tidb_catalog.pd.addresses  ${your_pd_adress}
```

`--jars`オプションで spark-shell を起動します。

```
spark-shell --jars tispark-assembly-{version}.jar
```

### TiSpark のバージョンを入手する {#get-tispark-version}

spark-shell で次のコマンドを実行すると、TiSpark のバージョン情報を取得できます。

```scala
spark.sql("select ti_version()").collect
```

### TiSpark を使用してデータを読み取る {#read-data-using-tispark}

Spark SQL を使用して、TiKV からデータを読み取ることができます。

```scala
spark.sql("use tidb_catalog")
spark.sql("select count(*) from ${database}.${table}").show
```

### TiSpark を使用してデータを書き込む {#write-data-using-tispark}

Spark DataSource API を使用して、 ACIDが保証されている TiKV にデータを書き込むことができます。

```scala
val tidbOptions: Map[String, String] = Map(
  "tidb.addr" -> "127.0.0.1",
  "tidb.password" -> "",
  "tidb.port" -> "4000",
  "tidb.user" -> "root"
)

val customerDF = spark.sql("select * from customer limit 100000")

customerDF.write
.format("tidb")
.option("database", "tpch_test")
.option("table", "cust_test_select")
.options(tidbOptions)
.mode("append")
.save()
```

詳細については[データ ソース API ユーザー ガイド](https://github.com/pingcap/tispark/blob/master/docs/features/datasource_api_userguide.md)参照してください。

TiSpark 3.1 以降、Spark SQL で書くこともできます。詳細については[SQL を挿入](https://github.com/pingcap/tispark/blob/master/docs/features/insert_sql_userguide.md)参照してください。

### JDBC DataSource を使用してデータを書き込む {#write-data-using-jdbc-datasource}

TiSpark を使用せずに、Spark JDBC を使用して TiDB に書き込むこともできます。

これは TiSpark の範囲を超えています。このドキュメントでは、例のみを示します。詳細については、 [JDBC から他のデータベースへ](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)を参照してください。

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// you might need to repartition the source to make it balanced across nodes
// and increase concurrency
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // replace the host and port with yours and be sure to use rewrite batch
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// as tested, setting to `150` is a good practice
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // database name and table name here
.option("isolationLevel", "NONE") // set isolationLevel to NONE
.option("user", "root") // TiDB user here
.save()
```

`isolationLevel`から`NONE`を設定して、TiDB OOM につながる可能性のある大規模な単一トランザクションを回避し、 `ISOLATION LEVEL does not support`エラーも回避します (TiDB は現在`REPEATABLE-READ`のみをサポートしています)。

### TiSpark を使用してデータを削除する {#delete-data-using-tispark}

Spark SQL を使用して、TiKV からデータを削除できます。

```
spark.sql("use tidb_catalog")
spark.sql("delete from ${database}.${table} where xxx")
```

詳細については[フィーチャーを削除](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)参照してください。

### 他のデータ ソースを操作する {#work-with-other-data-sources}

次のように、複数のカタログを使用して、さまざまなデータ ソースからデータを読み取ることができます。

```
// Read from Hive
spark.sql("select * from spark_catalog.default.t").show

// Join Hive tables and TiDB tables
spark.sql("select t1.id,t2.id from spark_catalog.default.t t1 left join tidb_catalog.test.t t2").show
```

## TiSpark 構成 {#tispark-configurations}

次の表の構成は、 `spark-defaults.conf`と組み合わせるか、他の Spark 構成プロパティと同じ方法で渡すことができます。

| 鍵                                               | デフォルト値           | 説明                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spark.tispark.pd.addresses`                    | `127.0.0.1:2379` | カンマで区切られた PD クラスタのアドレス。                                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.grpc.framesize`                  | `2147483647`     | gRPC 応答の最大フレーム サイズ (バイト単位) (デフォルトは 2G)。                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.grpc.timeout_in_sec`             | `10`             | gRPC タイムアウト時間 (秒単位)。                                                                                                                                                                                                                                                                                                                          |
| `spark.tispark.plan.allow_agg_pushdown`         | `true`           | アグリゲーションを TiKV にプッシュできるかどうか (TiKV ノードがビジー状態の場合)。                                                                                                                                                                                                                                                                                              |
| `spark.tispark.plan.allow_index_read`           | `true`           | 計画でインデックスが有効になっているかどうか (TiKV に大きなプレッシャーがかかる可能性があります)。                                                                                                                                                                                                                                                                                         |
| `spark.tispark.index.scan_batch_size`           | `20000`          | 同時インデックス スキャンのバッチ内の行キーの数。                                                                                                                                                                                                                                                                                                                     |
| `spark.tispark.index.scan_concurrency`          | `5`              | 行キーを取得するインデックス スキャンのスレッドの最大数 (各 JVM 内のタスク間で共有)。                                                                                                                                                                                                                                                                                               |
| `spark.tispark.table.scan_concurrency`          | `512`            | テーブル スキャンのスレッドの最大数 (各 JVM 内のタスク間で共有)。                                                                                                                                                                                                                                                                                                         |
| `spark.tispark.request.command.priority`        | `Low`            | 値のオプションは`Low` 、 `Normal` 、 `High`です。この設定は、TiKV で割り当てられるリソースに影響します。 OLTP ワークロードが妨げられないため、 `Low`が推奨されます。                                                                                                                                                                                                                                        |
| `spark.tispark.coprocess.codec_format`          | `chblock`        | コプロセッサーのデフォルトのコーデック形式を保持します。利用可能なオプションは`default` 、 `chblock` 、および`chunk`です。                                                                                                                                                                                                                                                                   |
| `spark.tispark.coprocess.streaming`             | `false`          | 応答の取得にストリーミングを使用するかどうか (実験的)。                                                                                                                                                                                                                                                                                                                 |
| `spark.tispark.plan.unsupported_pushdown_exprs` |                  | 式のコンマ区切りリスト。非常に古いバージョンの TiKV を使用している場合、サポートされていない式のプッシュ ダウンを無効にすることができます。                                                                                                                                                                                                                                                                     |
| `spark.tispark.plan.downgrade.index_threshold`  | `1000000000`     | 1 つのリージョンでのインデックス スキャンの範囲が元のリクエストでこの制限を超えている場合は、このリージョンのリクエストを計画されたインデックス スキャンではなくテーブル スキャンにダウングレードします。デフォルトでは、ダウングレードは無効になっています。                                                                                                                                                                                                             |
| `spark.tispark.show_rowid`                      | `false`          | ID が存在する場合に行 ID を表示するかどうか。                                                                                                                                                                                                                                                                                                                    |
| `spark.tispark.db_prefix`                       |                  | TiDB 内のすべてのデータベースの追加のプレフィックスを示す文字列。この文字列は、TiDB 内のデータベースと同じ名前の Hive データベースを区別します。                                                                                                                                                                                                                                                              |
| `spark.tispark.request.isolation.level`         | `SI`             | 基礎となる TiDB クラスターのロックを解決するかどうか。 「RC」を使用すると、 `tso`より小さいレコードの最新バージョンが取得され、ロックが無視されます。 「SI」を使用すると、解決されたロックがコミットされたか中止されたかに応じて、ロックを解決し、レコードを取得します。                                                                                                                                                                                                 |
| `spark.tispark.coprocessor.chunk_batch_size`    | `1024`           | コプロセッサーからフェッチされた行。                                                                                                                                                                                                                                                                                                                            |
| `spark.tispark.isolation_read_engines`          | `tikv,tiflash`   | コンマ区切りの TiSpark の読み取り可能なエンジンのリスト。リストされていないストレージ エンジンは読み取られません。                                                                                                                                                                                                                                                                                |
| `spark.tispark.stale_read`                      | オプション            | 古い読み取りタイムスタンプ (ミリ秒)。詳細については[ここ](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)参照してください。                                                                                                                                                                                                                          |
| `spark.tispark.tikv.tls_enable`                 | `false`          | TiSpark TLS を有効にするかどうか。                                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.tikv.trust_cert_collection`      |                  | リモート PD の証明書を検証するために使用される TiKV クライアントの信頼できる証明書。たとえば、 `/home/tispark/config/root.pem`ファイルには X.509 証明書コレクションが含まれている必要があります。                                                                                                                                                                                                                     |
| `spark.tispark.tikv.key_cert_chain`             |                  | TiKV クライアント用の X.509 証明書チェーン ファイル (例: `/home/tispark/config/client.pem` 。                                                                                                                                                                                                                                                                      |
| `spark.tispark.tikv.key_file`                   |                  | TiKV クライアント用の PKCS#8 秘密鍵ファイル (例: `/home/tispark/client_pkcs8.key` 。                                                                                                                                                                                                                                                                           |
| `spark.tispark.tikv.jks_enable`                 | `false`          | X.509 証明書の代わりに JAVA キー ストアを使用するかどうか。                                                                                                                                                                                                                                                                                                          |
| `spark.tispark.tikv.jks_trust_path`             |                  | `/home/tispark/config/tikv-truststore`などの`keytool`によって生成される、TiKV クライアント用の JKS 形式の証明書。                                                                                                                                                                                                                                                         |
| `spark.tispark.tikv.jks_trust_password`         |                  | `spark.tispark.tikv.jks_trust_path`のパスワード。                                                                                                                                                                                                                                                                                                    |
| `spark.tispark.tikv.jks_key_path`               |                  | `/home/tispark/config/tikv-clientstore`などの`keytool`によって生成される、TiKV クライアントの JKS 形式のキー。                                                                                                                                                                                                                                                          |
| `spark.tispark.tikv.jks_key_password`           |                  | `spark.tispark.tikv.jks_key_path`のパスワード。                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.jdbc.tls_enable`                 | `false`          | JDBC コネクタの使用時に TLS を有効にするかどうか。                                                                                                                                                                                                                                                                                                                |
| `spark.tispark.jdbc.server_cert_store`          |                  | JDBC の信頼できる証明書。これは、 `keytool` 、たとえば`/home/tispark/config/jdbc-truststore`によって生成されるJavaキーストア (JKS) 形式の証明書です。デフォルト値は &quot;&quot; です。これは、TiSpark が TiDBサーバーを検証しないことを意味します。                                                                                                                                                                      |
| `spark.tispark.jdbc.server_cert_password`       |                  | `spark.tispark.jdbc.server_cert_store`のパスワード。                                                                                                                                                                                                                                                                                                 |
| `spark.tispark.jdbc.client_cert_store`          |                  | JDBC の PKCS#12 証明書。 `keytool` 、たとえば`/home/tispark/config/jdbc-clientstore`によって生成された JKS 形式の証明書です。デフォルトは &quot;&quot; です。これは、TiDBサーバーがTiSpark を検証しないことを意味します。                                                                                                                                                                                  |
| `spark.tispark.jdbc.client_cert_password`       |                  | `spark.tispark.jdbc.client_cert_store`のパスワード。                                                                                                                                                                                                                                                                                                 |
| `spark.tispark.tikv.tls_reload_interval`        | `10s`            | 証明書のリロードがあるかどうかを確認する間隔。デフォルト値は`10s` (10 秒) です。                                                                                                                                                                                                                                                                                                |
| `spark.tispark.tikv.conn_recycle_time`          | `60s`            | TiKV との期限切れの接続をクリーニングする間隔。証明書のリロードが有効になっている場合にのみ有効です。デフォルト値は`60s` (60 秒) です。                                                                                                                                                                                                                                                                  |
| `spark.tispark.host_mapping`                    |                  | パブリック IP アドレスとイントラネット IP アドレス間のマッピングを構成するために使用されるルート マップ。 TiDB クラスターがイントラネットで実行されている場合、外部の Spark クラスターがアクセスできるように、一連のイントラネット IP アドレスをパブリック IP アドレスにマップできます。形式は`{Intranet IP1}:{Public IP1};{Intranet IP2}:{Public IP2}`です。たとえば、 `192.168.0.2:8.8.8.8;192.168.0.3:9.9.9.9`です。                                                                  |
| `spark.tispark.new_collation_enable`            |                  | TiDB で[新しい照合順序](https://docs.pingcap.com/tidb/stable/character-set-and-collation#new-framework-for-collations)が有効になっている場合、この構成を`true`に設定できます。 TiDB で`new collation`が有効になっていない場合、この構成を`false`に設定できます。この項目が構成されていない場合、TiSpark は TiDB のバージョンに基づいて`new collation`自動的に構成します。構成ルールは次のとおりです。TiDB のバージョンが v6.0.0 以上の場合、それは`true`です。それ以外の場合は`false`です。 |

### TLS 構成 {#tls-configurations}

TiSpark TLS には、TiKV クライアント TLS と JDBC コネクタ TLS の 2 つの部分があります。 TiSpark で TLS を有効にするには、両方を構成する必要があります。 `spark.tispark.tikv.xxx` 、TiKV クライアントが PD および TiKVサーバーとの TLS 接続を作成するために使用されます。 `spark.tispark.jdbc.xxx`は JDBC が TLS 接続で TiDBサーバーに接続するために使用されます。

TiSpark TLS が有効になっている場合は、X.509 証明書を`tikv.trust_cert_collection` 、 `tikv.key_cert_chain`および`tikv.key_file`の構成で構成するか、JKS 証明書を`tikv.jks_enable` 、 `tikv.jks_trust_path`および`tikv.jks_key_path`で構成する必要があります。 `jdbc.server_cert_store`と`jdbc.client_cert_store`はオプションです。

TiSpark は TLSv1.2 と TLSv1.3 のみをサポートします。

-   以下は、TiKV クライアントで X.509 証明書を使用して TLS 構成を開く例です。

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.trust_cert_collection                       /home/tispark/root.pem
spark.tispark.tikv.key_cert_chain                              /home/tispark/client.pem
spark.tispark.tikv.key_file                                    /home/tispark/client.key
```

-   以下は、TiKV クライアントの JKS 構成で TLS を有効にする例です。

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.jks_enable                                  true
spark.tispark.tikv.jks_key_path                                /home/tispark/config/tikv-truststore
spark.tispark.tikv.jks_key_password                            tikv_trustore_password
spark.tispark.tikv.jks_trust_path                              /home/tispark/config/tikv-clientstore
spark.tispark.tikv.jks_trust_password                          tikv_clientstore_password
```

JKS と X.509 証明書の両方が構成されている場合、JKS の優先度が高くなります。つまり、TLS ビルダーは最初に JKS 証明書を使用します。したがって、共通の PEM 証明書を使用するだけの場合は、 `spark.tispark.tikv.jks_enable=true`を設定しないでください。

-   以下は、JDBC コネクタで TLS を有効にする例です。

```
spark.tispark.jdbc.tls_enable                                  true
spark.tispark.jdbc.server_cert_store                           /home/tispark/jdbc-truststore
spark.tispark.jdbc.server_cert_password                        jdbc_truststore_password
spark.tispark.jdbc.client_cert_store                           /home/tispark/jdbc-clientstore
spark.tispark.jdbc.client_cert_password                        jdbc_clientstore_password
```

-   TiDB TLS を開く方法の詳細については、 [TiDB クライアントとサーバー間の TLS を有効にする](/enable-tls-between-clients-and-servers.md)を参照してください。
-   JAVA キー ストアの生成方法の詳細については、 [SSL を使用して安全に接続する](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-using-ssl.html)を参照してください。

### Log4j 構成 {#log4j-configuration}

`spark-shell`または`spark-sql`開始してクエリを実行すると、次の警告が表示される場合があります。

```
Failed to get database ****, returning NoSuchObjectException
Failed to get database ****, returning NoSuchObjectException
```

ここで、 `****`はデータベース名です。

警告は無害であり、Spark が独自のカタログで`****`を見つけることができないために発生します。これらの警告は無視してかまいません。

それらをミュートするには、次のテキストを`${SPARK_HOME}/conf/log4j.properties`に追加します。

```
# tispark disable "WARN ObjectStore:568 - Failed to get database"
log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR
```

### タイムゾーンの設定 {#time-zone-configuration}

`-Duser.timezone`システム プロパティ (たとえば、 `-Duser.timezone=GMT-7` ) を使用してタイム ゾーンを設定します。これは`Timestamp`タイプに影響します。

`spark.sql.session.timeZone`を使用しないでください。

## 特徴 {#features}

TiSpark の主な機能は次のとおりです。

| 機能のサポート                    | TiSpark 2.4.x | TiSpark 2.5.x | TiSpark 3.0.x | TiSpark 3.1.x |
| -------------------------- | ------------- | ------------- | ------------- | ------------- |
| tidb_catalog を使用しない SQL 選択 | ✔             | ✔             |               |               |
| tidb_catalog を使用した SQL 選択  |               | ✔             | ✔             | ✔             |
| データフレーム追加                  | ✔             | ✔             | ✔             | ✔             |
| DataFrame 読み取り             | ✔             | ✔             | ✔             | ✔             |
| SQL ショー データベース             | ✔             | ✔             | ✔             | ✔             |
| SQL ショー テーブル               | ✔             | ✔             | ✔             | ✔             |
| SQL 認証                     |               | ✔             | ✔             | ✔             |
| SQL 削除                     |               |               | ✔             | ✔             |
| SQL 挿入                     |               |               |               | ✔             |
| TLS                        |               |               | ✔             | ✔             |
| データフレーム認証                  |               |               |               | ✔             |

### 式インデックスのサポート {#support-for-expression-index}

TiDB v5.0 は[式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)をサポートします。

TiSpark は現在、 `expression index`を使用してテーブルからデータを取得することをサポートしていますが、TiSpark のプランナーは`expression index`使用しません。

### TiFlashで作業する {#work-with-tiflash}

TiSpark は、設定を介してTiFlashからデータを読み取ることができます`spark.tispark.isolation_read_engines` 。

### 分割テーブルのサポート {#support-for-partitioned-tables}

**TiDB から分割されたテーブルを読み取る**

TiSpark は、TiDB からパーティション分割されたテーブルの範囲とハッシュを読み取ることができます。

現在、TiSpark は MySQL/TiDB パーティション テーブル構文をサポートしていません`select col_name from table_name partition(partition_name)` 。ただし、 `where`条件を使用してパーティションをフィルター処理することはできます。

TiSpark は、テーブルに関連付けられているパーティションの種類とパーティション式に従って、パーティションのプルーニングを適用するかどうかを決定します。

TiSpark は、パーティション式が次のいずれかである場合にのみ、レンジ パーティション分割にパーティション プルーニングを適用します。

-   列式
-   `YEAR($argument)`引数は列であり、その型は日時として解析できる日時または文字列リテラルです。

パーティションのプルーニングが適用されない場合、TiSpark の読み取りは、すべてのパーティションに対してテーブル スキャンを実行することと同じです。

**分割テーブルへの書き込み**

現在、TiSpark は、次の条件下で、範囲およびハッシュ パーティション分割されたテーブルへのデータの書き込みのみをサポートしています。

-   パーティション式は列式です。
-   パーティション式は`YEAR($argument)`で、引数は列であり、その型は日時として解析できる日時または文字列リテラルです。

分割されたテーブルに書き込む方法は 2 つあります。

-   データソース API を使用して、置換および追加セマンティクスをサポートするパーティション テーブルに書き込みます。
-   Spark SQL で delete ステートメントを使用します。

> **ノート：**
>
> 現在、TiSpark は、utf8mb4_bin照合順序が有効になっているパーティション分割されたテーブルへの書き込みのみをサポートしています。

### Security {#security}

TiSpark v2.5.0 以降のバージョンを使用している場合は、TiDB を使用して TiSpark ユーザーを認証および承認できます。

認証および承認機能は、デフォルトでは無効になっています。これを有効にするには、次の構成を Spark 構成ファイルに追加します`spark-defaults.conf` 。

```
// Enable authentication and authorization
spark.sql.auth.enable true

// Configure TiDB information
spark.sql.tidb.addr $your_tidb_server_address
spark.sql.tidb.port $your_tidb_server_port
spark.sql.tidb.user $your_tidb_server_user
spark.sql.tidb.password $your_tidb_server_password
```

詳細については、 [TiDBサーバーによる承認と認証](https://github.com/pingcap/tispark/blob/master/docs/features/authorization_userguide.md)を参照してください。

### その他の機能 {#other-features}

-   [押し下げる](https://github.com/pingcap/tispark/blob/master/docs/features/push_down.md)
-   [TiSparkで削除](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)
-   [古い読み取り](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)
-   [複数のカタログを持つ TiSpark](https://github.com/pingcap/tispark/wiki/TiSpark-with-multiple-catalogs)
-   [TiSpark TLS](#tls-configurations)
-   [TiSparkプラン](https://github.com/pingcap/tispark/blob/master/docs/features/query_execution_plan_in_TiSpark.md)

## 統計情報 {#statistics-information}

TiSpark は、次の目的で統計情報を使用します。

-   推定コストが最小のクエリ プランで使用するインデックスを決定する。
-   効率的なブロードキャスト参加を可能にする小さなテーブル ブロードキャスト。

TiSpark が統計情報にアクセスできるようにするには、関連するテーブルが分析されていることを確認してください。

テーブルの分析方法の詳細については、 [統計入門](/statistics.md)参照してください。

TiSpark 2.0 以降、統計情報はデフォルトで自動的にロードされます。

## FAQ {#faq}

[TiSpark FAQ](https://github.com/pingcap/tispark/wiki/TiSpark-FAQ)を参照してください。
