---
title: TiSpark User Guide
summary: TiSpark を使用して、オンライン トランザクションと分析の両方のワンストップ ソリューションとして機能する HTAP ソリューションを提供します。
---

# TiSpark ユーザーガイド {#tispark-user-guide}

![TiSpark architecture](/media/tispark-architecture.png)

## TiSpark 対TiFlash {#tispark-vs-tiflash}

[ティスパーク](https://github.com/pingcap/tispark) 、TiDB/TiKV 上で Apache Spark を実行し、複雑な OLAP クエリに応答するために構築された薄いレイヤーです。Spark プラットフォームと分散 TiKV クラスターの両方の利点を活用し、分散 OLTP データベースである TiDB にシームレスに接着して、オンライン トランザクションと分析の両方のワンストップ ソリューションとして機能するハイブリッド トランザクション/分析処理 (HTAP) ソリューションを提供します。

[TiFlash](/tiflash/tiflash-overview.md)は、HTAP を有効にする別のツールです。TiFlash と TiSpark はどちらも、複数のホストを使用して OLTP データに対して OLAP クエリを実行できます。TiFlashはデータを列形式で保存するため、より効率的な分析クエリが可能になります。TiFlash と TiSparkは一緒に使用できます。

## TiSparkとは {#what-is-tispark}

TiSpark は、TiKV クラスターと PD クラスターに依存します。また、Spark クラスターを設定する必要があります。このドキュメントでは、TiSpark の設定方法と使用方法について簡単に説明します。Apache Spark に関する基本的な知識が必要です。詳細については、 [Apache Spark ウェブサイト](https://spark.apache.org/docs/latest/index.html)参照してください。

TiSpark は Spark Catalyst Engine と緊密に統合されており、コンピューティングを正確に制御できます。これにより、Spark は TiKV からデータを効率的に読み取ることができます。TiSpark はインデックス シークもサポートしており、高速ポイント クエリを可能にします。TiSpark はコンピューティングを TiKV にプッシュすることでデータ クエリを高速化し、Spark SQL で処理されるデータの量を削減します。同時に、TiSpark は TiDB 組み込み統計を使用して最適なクエリ プランを選択できます。

TiSpark と TiDB を使用すると、ETL を構築および保守することなく、トランザクション タスクと分析タスクの両方を同じプラットフォームで実行できます。これにより、システムアーキテクチャが簡素化され、保守コストが削減されます。

TiDB でのデータ処理には、Spark エコシステムのツールを使用できます。

-   TiSpark: データ分析とETL
-   TiKV: データ取得
-   スケジュールシステム: レポート生成

また、TiSpark は TiKV への分散書き込みをサポートしています。Spark と JDBC を使用した TiDB への書き込みと比較すると、TiKV への分散書き込みではトランザクション (すべてのデータが正常に書き込まれるか、すべての書き込みが失敗するかのいずれか) を実装でき、書き込みが高速になります。

> **警告：**
>
> TiSpark は TiKV に直接アクセスするため、TiDB Server で使用されるアクセス制御メカニズムは TiSpark には適用されません。TiSpark v2.5.0 以降、TiSpark はユーザー認証と承認をサポートしています。詳細については、 [Security](/tispark-overview.md#security)を参照してください。

## 要件 {#requirements}

-   TiSpark は Spark &gt;= 2.3 をサポートします。
-   TiSpark には JDK 1.8 と Scala 2.11/2.12 が必要です。
-   TiSpark は、 `YARN` 、 `Mesos` 、 `Standalone`などの任意の Spark モードで実行されます。

## Sparkの推奨デプロイメント構成 {#recommended-deployment-configurations-of-spark}

> **警告：**
>
> この[ドキュメント](/tispark-deployment-topology.md)で説明されているように、 TiUPを使用して TiSpark をデプロイすることは非推奨になりました。

TiSpark は Spark の TiDB コネクタであるため、使用するには実行中の Spark クラスターが必要です。

このドキュメントでは、Spark の導入に関する基本的なアドバイスを提供します。詳細なハードウェア推奨事項については、 [スパーク公式サイト](https://spark.apache.org/docs/latest/hardware-provisioning.html)を参照してください。

Spark クラスターの独立したデプロイメントの場合:

-   Spark には 32 GB のメモリを割り当てることをお勧めします。オペレーティング システムとバッファ キャッシュ用にメモリの少なくとも 25% を予約してください。
-   Spark には、マシンごとに少なくとも 8 ～ 16 個のコアをプロビジョニングすることをお勧めします。まず、すべての CPU コアを Spark に割り当てる必要があります。

以下は`spark-env.sh`構成に基づく例です。

    SPARK_EXECUTOR_MEMORY = 32g
    SPARK_WORKER_MEMORY = 32g
    SPARK_WORKER_CORES = 8

## TiSparkを入手 {#get-tispark}

TiSpark は、TiKV の読み取りと書き込みの機能を提供する Spark 用のサードパーティ jar パッケージです。

### mysql-connector-j を入手する {#get-mysql-connector-j}

GPL ライセンスの制限により、 `mysql-connector-java`依存関係は提供されなくなりました。

TiSpark の jar の次のバージョンには`mysql-connector-java`含まれなくなります。

-   TiSpark &gt; 3.0.1
-   TiSpark &gt; 2.5.1 (TiSpark 2.5.x 用)
-   TiSpark &gt; 2.4.3 (TiSpark 2.4.x 用)

ただし、TiSpark では書き込みと認証に`mysql-connector-java`必要です。このような場合は、次のいずれかの方法で`mysql-connector-java`手動でインポートする必要があります。

-   `mysql-connector-java` Spark jar ファイルに入力します。

-   Spark ジョブを送信するときに`mysql-connector-java`インポートします。次の例を参照してください。

<!---->

    spark-submit --jars tispark-assembly-3.0_2.12-3.1.0-SNAPSHOT.jar,mysql-connector-java-8.0.29.jar

### TiSparkのバージョンを選択 {#choose-tispark-version}

TiDB と Spark のバージョンに応じて、TiSpark のバージョンを選択できます。

| TiSpark バージョン    | TiDB、TiKV、PD バージョン | Sparkバージョン              | Scalaバージョン |
| ---------------- | ------------------ | ----------------------- | ---------- |
| 2.4.x-scala_2.11 | 5.x、4.x            | 2.3.x、2.4.x             | 2.11       |
| 2.4.x-scala_2.12 | 5.x、4.x            | 2.4.x                   | 2.12       |
| 2.5.x            | 5.x、4.x            | 3.0.x、3.1.x             | 2.12       |
| 3.0.x            | 5.x、4.x            | 3.0.x、3.1.x、3.2.x       | 2.12       |
| 3.1.x            | 6.x、5.x、4.x        | 3.0.x、3.1.x、3.2.x、3.3.x | 2.12       |

TiSpark 2.4.4、2.5.2、3.0.2、3.1.1 は最新の安定バージョンであり、強くお勧めします。

### TiSpark jarを入手する {#get-tispark-jar}

次のいずれかの方法で TiSpark jar を取得できます。

-   [メイヴンセントラル](https://search.maven.org/)から取得して[`pingcap`](http://search.maven.org/#search%7Cga%7C1%7Cpingcap)を検索
-   [TiSparkリリース](https://github.com/pingcap/tispark/releases)から取得
-   以下の手順でソースからビルドします

> **注記：**
>
> 現在、TiSpark をビルドするには java8 のみが選択肢となります。確認するには mvn -version を実行してください。

    git clone https://github.com/pingcap/tispark.git

TiSpark ルート ディレクトリで次のコマンドを実行します。

    // add -Dmaven.test.skip=true to skip the tests
    mvn clean install -Dmaven.test.skip=true
    // or you can add properties to specify spark version
    mvn clean install -Dmaven.test.skip=true -Pspark3.2.1

### TiSpark jar のアーティファクト ID {#tispark-jar-s-artifact-id}

TiSpark のアーティファクト ID は TiSpark のバージョンによって異なります。

| TiSpark バージョン                | アーティファクトID                                      |
| ---------------------------- | ----------------------------------------------- |
| 2.4.x-${scala_version}、2.5.0 | tisparkアセンブリ                                    |
| 2.5.1                        | tispark-アセンブリ-${spark_version}                  |
| 3.0.x、3.1.x                  | tispark-アセンブリ-${spark_version}-${scala_version} |

## はじめる {#getting-started}

このドキュメントでは、spark-shell で TiSpark を使用する方法について説明します。

### spark-shellを起動する {#start-spark-shell}

spark-shell で TiSpark を使用するには:

`spark-defaults.conf`に次の設定を追加します。

    spark.sql.extensions  org.apache.spark.sql.TiExtensions
    spark.tispark.pd.addresses  ${your_pd_address}
    spark.sql.catalog.tidb_catalog  org.apache.spark.sql.catalyst.catalog.TiCatalog
    spark.sql.catalog.tidb_catalog.pd.addresses  ${your_pd_address}

`--jars`オプションで spark-shell を起動します。

    spark-shell --jars tispark-assembly-{version}.jar

### TiSparkバージョンを入手 {#get-tispark-version}

spark-shell で次のコマンドを実行すると、TiSpark のバージョン情報を取得できます。

```scala
spark.sql("select ti_version()").collect
```

### TiSparkを使用してデータを読み取る {#read-data-using-tispark}

Spark SQL を使用して TiKV からデータを読み取ることができます。

```scala
spark.sql("use tidb_catalog")
spark.sql("select count(*) from ${database}.${table}").show
```

### TiSparkを使用してデータを書き込む {#write-data-using-tispark}

Spark DataSource API を使用して、 ACIDが保証される TiKV にデータを書き込むことができます。

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

詳細は[データ ソース API ユーザー ガイド](https://github.com/pingcap/tispark/blob/master/docs/features/datasource_api_userguide.md)参照してください。

TiSpark 3.1 以降では、Spark SQL を使用して記述することもできます。詳細については、 [挿入SQL](https://github.com/pingcap/tispark/blob/master/docs/features/insert_sql_userguide.md)参照してください。

### JDBC データソースを使用してデータを書き込む {#write-data-using-jdbc-datasource}

TiSpark を使用せずに、Spark JDBC を使用して TiDB に書き込むこともできます。

これは TiSpark の範囲外です。このドキュメントでは例のみを示します。詳細については、 [JDBC から他のデータベースへ](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)を参照してください。

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

TiDB OOM につながる可能性のある大規模な単一トランザクションを回避し、 `ISOLATION LEVEL does not support`エラーも回避するには、 `isolationLevel` `NONE`に設定します (TiDB は現在`REPEATABLE-READ`のみをサポートしています)。

### TiSparkを使用してデータを削除する {#delete-data-using-tispark}

Spark SQL を使用して TiKV からデータを削除できます。

    spark.sql("use tidb_catalog")
    spark.sql("delete from ${database}.${table} where xxx")

詳細は[機能を削除](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)参照してください。

### 他のデータソースを操作する {#work-with-other-data-sources}

次のように複数のカタログを使用して、異なるデータ ソースからデータを読み取ることができます。

    // Read from Hive
    spark.sql("select * from spark_catalog.default.t").show

    // Join Hive tables and TiDB tables
    spark.sql("select t1.id,t2.id from spark_catalog.default.t t1 left join tidb_catalog.test.t t2").show

## TiSpark 構成 {#tispark-configurations}

次の表の構成は、 `spark-defaults.conf`と一緒に使用することも、他の Spark 構成プロパティと同じ方法で渡すこともできます。

| 鍵                                               | デフォルト値           | 説明                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spark.tispark.pd.addresses`                    | `127.0.0.1:2379` | カンマで区切られた PD クラスターのアドレス。                                                                                                                                                                                                                                                                                                               |
| `spark.tispark.grpc.framesize`                  | `2147483647`     | gRPC 応答の最大フレーム サイズ (バイト単位) (デフォルトは 2G)。                                                                                                                                                                                                                                                                                                |
| `spark.tispark.grpc.timeout_in_sec`             | `10`             | gRPC タイムアウト時間（秒単位）。                                                                                                                                                                                                                                                                                                                    |
| `spark.tispark.plan.allow_agg_pushdown`         | `true`           | 集約が TiKV にプッシュダウンできるかどうか (TiKV ノードがビジーの場合)。                                                                                                                                                                                                                                                                                            |
| `spark.tispark.plan.allow_index_read`           | `true`           | 計画時にインデックスが有効になっているかどうか (TiKV に大きな負荷がかかる可能性があります)。                                                                                                                                                                                                                                                                                     |
| `spark.tispark.index.scan_batch_size`           | `20000`          | 同時インデックススキャンのバッチ内の行キーの数。                                                                                                                                                                                                                                                                                                               |
| `spark.tispark.index.scan_concurrency`          | `5`              | 行キーを取得するインデックス スキャンのスレッドの最大数 (各 JVM 内のタスク間で共有)。                                                                                                                                                                                                                                                                                        |
| `spark.tispark.table.scan_concurrency`          | `512`            | テーブルスキャンのスレッドの最大数 (各 JVM 内のタスク間で共有されます)。                                                                                                                                                                                                                                                                                               |
| `spark.tispark.request.command.priority`        | `Low`            | 値のオプションは`Low` 、 `Normal` 、 `High`です。この設定は、TiKV で割り当てられたリソースに影響します。OLTP ワークロードが妨げられないため、 `Low`推奨されます。                                                                                                                                                                                                                                   |
| `spark.tispark.coprocess.codec_format`          | `chblock`        | コプロセッサのデフォルトのコーデック形式を保持します。使用可能なオプションは`default` 、 `chblock` 、 `chunk`です。                                                                                                                                                                                                                                                               |
| `spark.tispark.coprocess.streaming`             | `false`          | レスポンスの取得にストリーミングを使用するかどうか (実験的)。                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.plan.unsupported_pushdown_exprs` |                  | カンマで区切られた式のリスト。非常に古いバージョンの TiKV を使用している場合、サポートされていない一部の式のプッシュダウンを無効にすることができます。                                                                                                                                                                                                                                                         |
| `spark.tispark.plan.downgrade.index_threshold`  | `1000000000`     | 1 つのリージョンでのインデックス スキャンの範囲が元のリクエストでこの制限を超える場合、このリージョンのリクエストを計画されたインデックス スキャンではなくテーブル スキャンにダウングレードします。デフォルトでは、ダウングレードは無効になっています。                                                                                                                                                                                                         |
| `spark.tispark.show_rowid`                      | `false`          | ID が存在する場合に行 ID を表示するかどうか。                                                                                                                                                                                                                                                                                                             |
| `spark.tispark.db_prefix`                       |                  | TiDB 内のすべてのデータベースの追加プレフィックスを示す文字列。この文字列は、TiDB 内のデータベースを同じ名前の Hive データベースと区別します。                                                                                                                                                                                                                                                        |
| `spark.tispark.request.isolation.level`         | `SI`             | 基礎となる TiDB クラスターのロックを解決するかどうか。「RC」を使用すると、 `tso`より小さいレコードの最新バージョンが取得され、ロックは無視されます。「SI」を使用すると、解決されたロックがコミットされたか中止されたかに応じて、ロックが解決され、レコードが取得されます。                                                                                                                                                                                          |
| `spark.tispark.coprocessor.chunk_batch_size`    | `1024`           | コプロセッサから取得された行。                                                                                                                                                                                                                                                                                                                        |
| `spark.tispark.isolation_read_engines`          | `tikv,tiflash`   | TiSpark の読み取り可能なエンジンのリスト (カンマ区切り)。リストされていないストレージ エンジンは読み取られません。                                                                                                                                                                                                                                                                        |
| `spark.tispark.stale_read`                      | オプション            | 古い読み取りタイムスタンプ (ミリ秒)。詳細については[ここ](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)参照してください。                                                                                                                                                                                                                   |
| `spark.tispark.tikv.tls_enable`                 | `false`          | TiSpark TLS を有効にするかどうか。                                                                                                                                                                                                                                                                                                                |
| `spark.tispark.tikv.trust_cert_collection`      |                  | リモート PD の証明書を検証するために使用される、TiKV クライアントの信頼された証明書 (例: `/home/tispark/config/root.pem` 。ファイルには、X.509 証明書コレクションが含まれている必要があります。                                                                                                                                                                                                              |
| `spark.tispark.tikv.key_cert_chain`             |                  | TiKV クライアントの X.509 証明書チェーン ファイル (例: `/home/tispark/config/client.pem` 。                                                                                                                                                                                                                                                                |
| `spark.tispark.tikv.key_file`                   |                  | TiKV クライアントの PKCS#8 秘密鍵ファイル (例: `/home/tispark/client_pkcs8.key` 。                                                                                                                                                                                                                                                                     |
| `spark.tispark.tikv.jks_enable`                 | `false`          | X.509 証明書の代わりに JAVA キー ストアを使用するかどうか。                                                                                                                                                                                                                                                                                                   |
| `spark.tispark.tikv.jks_trust_path`             |                  | `keytool`によって生成された、TiKV クライアント用の JKS 形式の証明書 (例: `/home/tispark/config/tikv-truststore` 。                                                                                                                                                                                                                                               |
| `spark.tispark.tikv.jks_trust_password`         |                  | `spark.tispark.tikv.jks_trust_path`のパスワード。                                                                                                                                                                                                                                                                                             |
| `spark.tispark.tikv.jks_key_path`               |                  | `keytool`によって生成された TiKV クライアントの JKS 形式キー (例: `/home/tispark/config/tikv-clientstore` 。                                                                                                                                                                                                                                                 |
| `spark.tispark.tikv.jks_key_password`           |                  | `spark.tispark.tikv.jks_key_path`のパスワード。                                                                                                                                                                                                                                                                                               |
| `spark.tispark.jdbc.tls_enable`                 | `false`          | JDBC コネクタを使用するときに TLS を有効にするかどうか。                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.jdbc.server_cert_store`          |                  | JDBC の信頼できる証明書。これは、 `keytool`によって生成されたJavaキーストア (JKS) 形式の証明書です (例: `/home/tispark/config/jdbc-truststore` 。デフォルト値は &quot;&quot; で、これは TiSpark が TiDBサーバーを検証しないことを意味します。                                                                                                                                                                |
| `spark.tispark.jdbc.server_cert_password`       |                  | `spark.tispark.jdbc.server_cert_store`のパスワード。                                                                                                                                                                                                                                                                                          |
| `spark.tispark.jdbc.client_cert_store`          |                  | JDBC の PKCS#12 証明書。これは`keytool`によって生成された JKS 形式の証明書です (例: `/home/tispark/config/jdbc-clientstore` 。デフォルトは &quot;&quot; で、これは TiDBサーバーがTiSpark を検証しないことを意味します。                                                                                                                                                                          |
| `spark.tispark.jdbc.client_cert_password`       |                  | `spark.tispark.jdbc.client_cert_store`のパスワード。                                                                                                                                                                                                                                                                                          |
| `spark.tispark.tikv.tls_reload_interval`        | `10s`            | 再読み込みする証明書があるかどうかを確認する間隔。デフォルト値は`10s` (10 秒) です。                                                                                                                                                                                                                                                                                       |
| `spark.tispark.tikv.conn_recycle_time`          | `60s`            | TiKV を使用して期限切れの接続を消去する間隔。証明書の再読み込みが有効になっている場合にのみ有効になります。デフォルト値は`60s` (60 秒) です。                                                                                                                                                                                                                                                        |
| `spark.tispark.host_mapping`                    |                  | パブリック IP アドレスとイントラネット IP アドレス間のマッピングを構成するために使用されるルート マップ。TiDB クラスターがイントラネット上で実行されている場合、外部の Spark クラスターがアクセスできるように、イントラネット IP アドレスのセットをパブリック IP アドレスにマッピングできます。形式は`{Intranet IP1}:{Public IP1};{Intranet IP2}:{Public IP2}`です (例: `192.168.0.2:8.8.8.8;192.168.0.3:9.9.9.9` )。                                                          |
| `spark.tispark.new_collation_enable`            |                  | TiDB で[新しい照合順序](https://docs.pingcap.com/tidb/stable/character-set-and-collation#new-framework-for-collations)が有効になっている場合、この構成は`true`に設定できます。TiDB で`new collation`有効になっていない場合、この構成は`false`に設定できます。この項目が構成されていない場合、TiSpark は TiDB のバージョンに基づいて`new collation`自動的に構成します。構成ルールは次のとおりです。TiDB バージョンが v6.0.0 以上の場合は`true` 、それ以外の場合は`false`です。 |
| `spark.tispark.replica_read`                    | `leader`         | 読み取るレプリカのタイプ。値のオプションは`leader` 、 `follower` 、 `learner`です。複数のタイプを同時に指定することができ、TiSpark は順序に従ってタイプを選択します。                                                                                                                                                                                                                                 |
| `spark.tispark.replica_read.label`              |                  | ターゲット TiKV ノードのラベル。形式は`label_x=value_x,label_y=value_y`で、項目は論理積で接続されます。                                                                                                                                                                                                                                                                |

### TLS 構成 {#tls-configurations}

TiSpark TLS には、TiKV クライアント TLS と JDBC コネクタ TLS の 2 つの部分があります。TiSpark で TLS を有効にするには、両方を構成する必要があります。1 `spark.tispark.tikv.xxx` 、PD および TiKVサーバーとの TLS 接続を作成するために TiKV クライアントに使用されます。3 `spark.tispark.jdbc.xxx` 、TLS 接続で TiDBサーバーに接続するために JDBC に使用されます。

TiSpark TLS が有効になっている場合は、 `tikv.trust_cert_collection` 、 `tikv.key_cert_chain` 、 `tikv.key_file`の構成で X.509 証明書を構成するか、 `tikv.jks_enable` 、 `tikv.jks_trust_path` 、 `tikv.jks_key_path`で JKS 証明書を構成する必要があります。 `jdbc.server_cert_store`と`jdbc.client_cert_store`オプションです。

TiSpark は TLSv1.2 と TLSv1.3 のみをサポートします。

-   以下は、TiKV クライアントで X.509 証明書を使用して TLS 構成を開く例です。

<!---->

    spark.tispark.tikv.tls_enable                                  true
    spark.tispark.tikv.trust_cert_collection                       /home/tispark/root.pem
    spark.tispark.tikv.key_cert_chain                              /home/tispark/client.pem
    spark.tispark.tikv.key_file                                    /home/tispark/client.key

-   以下は、TiKV クライアントで JKS 構成を使用して TLS を有効にする例です。

<!---->

    spark.tispark.tikv.tls_enable                                  true
    spark.tispark.tikv.jks_enable                                  true
    spark.tispark.tikv.jks_key_path                                /home/tispark/config/tikv-truststore
    spark.tispark.tikv.jks_key_password                            tikv_trustore_password
    spark.tispark.tikv.jks_trust_path                              /home/tispark/config/tikv-clientstore
    spark.tispark.tikv.jks_trust_password                          tikv_clientstore_password

JKS 証明書と X.509 証明書の両方が設定されている場合、JKS の優先順位が高くなります。つまり、TLS ビルダーは JKS 証明書を最初に使用します。したがって、共通の PEM 証明書だけを使用する場合は、 `spark.tispark.tikv.jks_enable=true`設定しないでください。

-   以下は、JDBC コネクタで TLS を有効にする例です。

<!---->

    spark.tispark.jdbc.tls_enable                                  true
    spark.tispark.jdbc.server_cert_store                           /home/tispark/jdbc-truststore
    spark.tispark.jdbc.server_cert_password                        jdbc_truststore_password
    spark.tispark.jdbc.client_cert_store                           /home/tispark/jdbc-clientstore
    spark.tispark.jdbc.client_cert_password                        jdbc_clientstore_password

-   TiDB TLSを開く方法の詳細については、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)参照してください。
-   JAVA キーストアの生成方法の詳細については、 [SSL を使用した安全な接続](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-using-ssl.html)参照してください。

### Log4j の設定 {#log4j-configuration}

`spark-shell`または`spark-sql`を起動してクエリを実行すると、次の警告が表示される場合があります。

    Failed to get database ****, returning NoSuchObjectException
    Failed to get database ****, returning NoSuchObjectException

ここで、 `****`データベース名です。

この警告は無害であり、Spark が独自のカタログで`****`を見つけられないために発生します。これらの警告は無視してかまいません。

ミュートするには、次のテキストを`${SPARK_HOME}/conf/log4j.properties`に追加します。

    # tispark disable "WARN ObjectStore:568 - Failed to get database"
    log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR

### タイムゾーンの設定 {#time-zone-configuration}

`-Duser.timezone`システム プロパティ (たとえば、 `-Duser.timezone=GMT-7` ) を使用してタイム ゾーンを設定します。これは`Timestamp`タイプに影響します。

`spark.sql.session.timeZone`使用しないでください。

## 特徴 {#features}

TiSpark の主な機能は次のとおりです。

| 機能サポート                    | TiSpark 2.4.x | TiSpark 2.5.x | TiSpark 3.0.x | TiSpark 3.1.x |
| ------------------------- | ------------- | ------------- | ------------- | ------------- |
| tidb_catalog なしの SQL 選択   | ✔             | ✔             |               |               |
| tidb_catalog を使用した SQL 選択 |               | ✔             | ✔             | ✔             |
| データフレームの追加                | ✔             | ✔             | ✔             | ✔             |
| DataFrameの読み取り            | ✔             | ✔             | ✔             | ✔             |
| SQL 表示データベース              | ✔             | ✔             | ✔             | ✔             |
| SQL 表示テーブル                | ✔             | ✔             | ✔             | ✔             |
| SQL認証                     |               | ✔             | ✔             | ✔             |
| SQL 削除                    |               |               | ✔             | ✔             |
| SQL 挿入                    |               |               |               | ✔             |
| TLS                       |               |               | ✔             | ✔             |
| データフレーム認証                 |               |               |               | ✔             |

### 式インデックスのサポート {#support-for-expression-index}

TiDB v5.0 は[表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)サポートします。

TiSpark は現在、 `expression index`テーブルからのデータの取得をサポートしていますが、 `expression index` TiSpark のプランナーでは使用されません。

### TiFlashの操作 {#work-with-tiflash}

TiSpark は、構成`spark.tispark.isolation_read_engines`を介してTiFlashからデータを読み取ることができます。

### パーティションテーブルのサポート {#support-for-partitioned-tables}

**TiDBからパーティションテーブルを読み取る**

TiSpark は、TiDB から範囲パーティション テーブルとハッシュ パーティション テーブルを読み取ることができます。

現在、TiSpark は MySQL/TiDB パーティション テーブル構文`select col_name from table_name partition(partition_name)`をサポートしていません。ただし、 `where`条件を使用してパーティションをフィルターすることは可能です。

TiSpark は、テーブルに関連付けられたパーティション タイプとパーティション式に応じて、パーティション プルーニングを適用するかどうかを決定します。

TiSpark は、パーティション式が次のいずれかの場合にのみ、範囲パーティション分割にパーティション プルーニングを適用します。

-   列式
-   `YEAR($argument)`引数は列であり、その型は datetime または datetime として解析できる文字列リテラルです。

パーティション プルーニングが適用できない場合、TiSpark の読み取りはすべてのパーティションに対してテーブル スキャンを実行することと同じです。

**パーティションテーブルに書き込む**

現在、TiSpark は、次の条件下でのみ、範囲パーティション テーブルとハッシュ パーティション テーブルへのデータの書き込みをサポートしています。

-   パーティション式は列式です。
-   パーティション式は`YEAR($argument)`で、引数は列であり、その型は datetime または datetime として解析できる文字列リテラルです。

パーティション テーブルに書き込むには、次の 2 つの方法があります。

-   データソース API を使用して、置換および追加のセマンティクスをサポートするパーティション テーブルに書き込みます。
-   Spark SQL で delete ステートメントを使用します。

> **注記：**
>
> 現在、TiSpark は、utf8mb4_bin照合順序が有効になっているパーティション テーブルへの書き込みのみをサポートしています。

### Security {#security}

TiSpark v2.5.0 以降のバージョンを使用している場合は、TiDB を使用して TiSpark ユーザーを認証および承認できます。

認証と承認機能はデフォルトでは無効になっています。有効にするには、Spark 構成ファイル`spark-defaults.conf`に次の構成を追加します。

    // Enable authentication and authorization
    spark.sql.auth.enable true

    // Configure TiDB information
    spark.sql.tidb.addr $your_tidb_server_address
    spark.sql.tidb.port $your_tidb_server_port
    spark.sql.tidb.user $your_tidb_server_user
    spark.sql.tidb.password $your_tidb_server_password

詳細については[TiDBサーバーを介した認可と認証](https://github.com/pingcap/tispark/blob/master/docs/features/authorization_userguide.md)参照してください。

### その他の機能 {#other-features}

-   [押し下げる](https://github.com/pingcap/tispark/blob/master/docs/features/push_down.md)
-   [TiSparkで削除](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md)
-   [古い読み物](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md)
-   [複数のカタログを備えたTiSpark](https://github.com/pingcap/tispark/wiki/TiSpark-with-multiple-catalogs)
-   [ティスパークTLS](#tls-configurations)
-   [TiSparkプラン](https://github.com/pingcap/tispark/blob/master/docs/features/query_execution_plan_in_TiSpark.md)

## 統計情報 {#statistics-information}

TiSpark は統計情報を次の目的で使用します。

-   最小の推定コストでクエリ プランで使用するインデックスを決定します。
-   効率的なブロードキャスト参加を可能にする小さなテーブル ブロードキャスト。

TiSpark が統計情報にアクセスできるようにするには、関連するテーブルが分析されていることを確認してください。

テーブルを分析する方法の詳細については、 [統計入門](/statistics.md)参照してください。

TiSpark 2.0 以降では、統計情報はデフォルトで自動的に読み込まれます。

## FAQ {#faq}

[TiSparkFAQ](https://github.com/pingcap/tispark/wiki/TiSpark-FAQ)参照。
