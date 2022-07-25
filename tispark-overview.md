---
title: TiSpark User Guide
summary: Use TiSpark to provide an HTAP solution to serve as a one-stop solution for both online transactions and analysis.
---

# TiSparkユーザーガイド {#tispark-user-guide}

![TiSpark architecture](/media/tispark-architecture.png)

[TiSpark](https://github.com/pingcap/tispark)は、TiDB /TiKV上でApacheSparkを実行して、複雑なOLAPクエリに応答するために構築されたシンレイヤーです。 Sparkプラットフォームと分散TiKVクラスタの両方を活用し、分散OLTPデータベースであるTiDBにシームレスに接着して、オンライントランザクションと分析の両方のワンストップソリューションとして機能するハイブリッドトランザクション/分析処理（HTAP）ソリューションを提供します。 。

[TiFlash](/tiflash/tiflash-overview.md)は、HTAPを有効にするもう1つのツールです。 TiFlashとTiSparkはどちらも、複数のホストを使用してOLTPデータに対してOLAPクエリを実行できます。 TiFlashはデータを列形式で保存するため、より効率的な分析クエリが可能になります。 TiFlashとTiSparkは一緒に使用できます。

TiSparkは、TiKVクラスタとPDクラスタに依存しています。また、Sparkクラスタをセットアップする必要があります。このドキュメントでは、TiSparkのセットアップと使用方法について簡単に紹介します。 ApacheSparkの基本的な知識が必要です。詳細については、 [ApacheSparkのWebサイト](https://spark.apache.org/docs/latest/index.html)を参照してください。

TiSparkはSparkCatalystEngineと緊密に統合されており、コンピューティングを正確に制御します。これにより、SparkはTiKVからデータを効率的に読み取ることができます。 TiSparkは、高速ポイントクエリを可能にするインデックスシークもサポートしています。

TiSparkは、Spark SQLによって処理されるデータの量を減らすために、コンピューティングをTiKVにプッシュすることにより、データクエリを高速化します。一方、TiSparkは、TiDBの組み込み統計を使用して、最適なクエリプランを選択できます。

TiSparkとTiDBを使用すると、ETLを構築および保守することなく、同じプラットフォームでトランザクションタスクと分析タスクの両方を実行できます。これにより、システムアーキテクチャが簡素化され、メンテナンスのコストが削減されます。

Sparkエコシステムのツールを使用して、TiDBでのデータ処理を行うことができます。

-   TiSpark：データ分析とETL
-   TiKV：データ検索
-   スケジューリングシステム：レポート生成

また、TiSparkはTiKVへの分散書き込みをサポートしています。 SparkとJDBCを使用したTiDBへの書き込みと比較して、TiKVへの分散書き込みはトランザクションを実装でき（すべてのデータが正常に書き込まれるか、すべての書き込みが失敗します）、書き込みが高速になります。

> **警告：**
>
> TiSparkはTiKVに直接アクセスするため、TiDBサーバーで使用されるアクセス制御メカニズムはTiSparkには適用されません。 TiSpark v2.5.0以降、TiSparkはユーザーの認証と承認をサポートしています。詳細については、 [安全](/tispark-overview.md#security)を参照してください。

## 環境設定 {#environment-setup}

次の表に、サポートされているTiSparkバージョンの互換性情報を示します。必要に応じてTiSparkバージョンを選択できます。

| TiSparkバージョン     | TiDB、TiKV、およびPDバージョン | Sparkバージョン        | Scalaバージョン |
| ---------------- | -------------------- | ----------------- | ---------- |
| 2.4.x-scala_2.11 | 5.x、4.x              | 2.3.x、2.4.x       | 2.11       |
| 2.4.x-scala_2.12 | 5.x、4.x              | 2.4.x             | 2.12       |
| 2.5.x            | 5.x、4.x              | 3.0.x、3.1.x       | 2.12       |
| 3.0.x            | 5.x、4.x              | 3.0.x、3.1.x、3.2.x | 2.12       |

TiSparkは、YARN、Mesos、Standaloneなどの任意のSparkモードで実行されます。

## 推奨される構成 {#recommended-configuration}

このセクションでは、TiKVとTiSparkの独立した展開、SparkとTiSparkの独立した展開、およびTiKVとTiSparkの同時展開の推奨構成について説明します。

TiUPを使用してTiSparkをデプロイする方法の詳細については、 [TiSpark展開トポロジ](/tispark-deployment-topology.md)も参照してください。

### TiKVとTiSparkの独立した展開のConfiguration / コンフィグレーション {#configuration-of-independent-deployment-of-tikv-and-tispark}

TiKVとTiSparkを独立して展開するには、次の推奨事項を参照することをお勧めします。

-   ハードウェア構成
    -   一般的な目的については、TiDBおよびTiKVハードウェア構成[推奨事項](/hardware-and-software-requirements.md#development-and-test-environments)を参照してください。
    -   使用法が分析シナリオに重点を置いている場合は、TiKVノードのメモリを少なくとも64Gに増やすことができます。

### SparkとTiSparkの独立した展開のConfiguration / コンフィグレーション {#configuration-of-independent-deployment-of-spark-and-tispark}

ハードウェアの推奨事項の詳細については、 [Spark公式サイト](https://spark.apache.org/docs/latest/hardware-provisioning.html)を参照してください。以下は、TiSpark構成の概要です。

-   Sparkに32Gメモリを割り当て、オペレーティングシステムとバッファキャッシュ用にメモリの少なくとも25％を予約することをお勧めします。

-   Sparkのマシンごとに少なくとも8〜16コアをプロビジョニングすることをお勧めします。最初に、すべてのCPUコアをSparkに割り当てることができます。

### 共同展開されたTiKVとTiSparkのConfiguration / コンフィグレーション {#configuration-of-co-deployed-tikv-and-tispark}

TiKVとTiSparkを共同展開するには、TiSparkに必要なリソースをTiKVの予約済みリソースに追加し、メモリの25％をシステムに割り当てます。

## TiSparkクラスタをデプロイします {#deploy-the-tispark-cluster}

TiSparkのjarパッケージ[ここ](https://github.com/pingcap/tispark/releases)をダウンロードし、 `$SPARKPATH/jars`フォルダーに配置します。

> **ノート：**
>
> TiSpark v2.1.x以前のバージョンのファイル名は、 `tispark-core-2.1.9-spark_2.4-jar-with-dependencies.jar`のようになります。必要なバージョンの正確なファイル名については、 [GitHubのリリースページ](https://github.com/pingcap/tispark/releases)を確認してください。

以下は、TiSparkv2.4.1をインストールする方法の簡単な例です。

{{< copyable "" >}}

```shell
wget https://github.com/pingcap/tispark/releases/download/v2.4.1/tispark-assembly-2.4.1.jar
mv tispark-assembly-2.4.1.jar $SPARKPATH/jars/
```

`spark-defaults.conf.template`ファイルから`spark-defaults.conf`をコピーします。

{{< copyable "" >}}

```shell
cp conf/spark-defaults.conf.template conf/spark-defaults.conf
```

`spark-defaults.conf`ファイルに、次の行を追加します。

```
spark.tispark.pd.addresses $pd_host:$pd_port
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

`spark.tispark.pd.addresses`の構成では、複数のPDサーバーを配置できます。それぞれのポート番号を指定します。たとえば、ポート2379を使用して`10.16.20.1,10.16.20.2,10.16.20.3`に複数のPDサーバーがある場合は、 `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`として配置します。

> **ノート：**
>
> TiSparkが正しく通信できなかった場合は、ファイアウォールの構成を確認してください。必要に応じて、ファイアウォールルールを調整したり、無効にしたりできます。

### 既存のSparkクラスタにTiSparkをデプロイ {#deploy-tispark-on-an-existing-spark-cluster}

既存のSparkクラスタでTiSparkを実行する場合、クラスタを再起動する必要はありません。 Sparkの`--jars`パラメーターを使用して、依存関係としてTiSparkを導入できます。

{{< copyable "" >}}

```shell
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

### SparkクラスタなしでTiSparkをデプロイ {#deploy-tispark-without-a-spark-cluster}

Sparkクラスタがない場合は、スタンドアロンモードを使用することをお勧めします。詳細については、 [Sparkスタンドアロン](https://spark.apache.org/docs/latest/spark-standalone.html)を参照してください。問題が発生した場合は、 [Spark公式サイト](https://spark.apache.org/docs/latest/spark-standalone.html)を参照してください。そして、GitHubで[問題を提出する](https://github.com/pingcap/tispark/issues/new)へようこそ。

## SparkShellとSparkSQLを使用する {#use-spark-shell-and-spark-sql}

上記のように、TiSparkクラスタが正常に開始されたと想定します。以下では、 `tpch`データベースの`lineitem`という名前のテーブルでOLAP分析にSparkSQLを使用する方法について説明します。

`192.168.1.101`で利用可能なTiDBサーバーを介してテストデータを生成するには：

{{< copyable "" >}}

```shell
tiup bench tpch prepare --host 192.168.1.101 --user root
```

PDノードが`192.168.1.100` 、ポート`2379`にあると仮定して、次のコマンドを`$SPARK_HOME/conf/spark-defaults.conf`に追加します。

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

SparkShellを起動します。

{{< copyable "" >}}

```shell
./bin/spark-shell
```

次に、ネイティブApache Sparkと同様に、SparkShellに次のコマンドを入力します。

{{< copyable "" >}}

```scala
spark.sql("use tpch")
spark.sql("select count(*) from lineitem").show
```

結果は次のとおりです。

```
+-------------+
| Count (1) |
+-------------+
| 2000      |
+-------------+
```

Spark Shellの他に、SparkSQLも利用できます。 Spark SQLを使用するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
./bin/spark-sql
```

同じクエリを実行できます。

{{< copyable "" >}}

```scala
use tpch;
select count(*) from lineitem;
```

結果は次のとおりです。

```
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

## ThriftServerでJDBCサポートを使用する {#use-jdbc-support-with-thriftserver}

JDBCサポートなしでSparkShellまたはSparkSQLを使用できます。ただし、beelineなどのツールにはJDBCサポートが必要です。 JDBCサポートは、Thriftサーバーによって提供されます。 SparkのThriftサーバーを使用するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
./sbin/start-thriftserver.sh
```

JDBCをThriftサーバーに接続するには、beelineなどのJDBC対応ツールを使用できます。

たとえば、beelineで使用するには：

{{< copyable "" >}}

```shell
./bin/beeline jdbc:hive2://localhost:10000
```

次のメッセージが表示された場合は、beelineが正常に有効になっています。

```
Beeline version 1.2.2 by Apache Hive
```

次に、queryコマンドを実行できます。

```
1: jdbc:hive2://localhost:10000> use testdb;
+---------+--+
| Result  |
+---------+--+
+---------+--+
No rows selected (0.013 seconds)

select count(*) from account;
+-----------+--+
| count(1)  |
+-----------+--+
| 1000000   |
+-----------+--+
1 row selected (1.97 seconds)
```

## TiSparkをHiveと一緒に使用する {#use-tispark-together-with-hive}

TiSparkはHiveと一緒に使用できます。 Sparkを起動する前に、 `HADOOP_CONF_DIR`の環境変数をHadoop構成フォルダーに設定し、 `hive-site.xml`を`spark/conf`フォルダーにコピーする必要があります。

```scala
val tisparkDF = spark.sql("select * from tispark_table").toDF
tisparkDF.write.saveAsTable("hive_table") // save table to hive
spark.sql("select * from hive_table a, tispark_table b where a.col1 = b.col1").show // join table across Hive and Tispark
```

## TiSparkを使用してDataFrameをTiDBにバッチ書き込み {#batch-write-dataframes-into-tidb-using-tispark}

v2.3以降、TiSparkはデータフレームのTiDBクラスターへのバッチ書き込みをネイティブにサポートします。この書き込みモードは、TiKVの2フェーズコミットプロトコルを介して実装されます。

Spark + JDBCを介した書き込みと比較して、TiSparkバッチ書き込みには次の利点があります。

| 比較する側面 | TiSparkバッチ書き込み                          | Spark+JDBC書き込み                                                                                                                                            |
| ------ | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| アトミシティ | DataFrameはすべて正常に書き込まれるか、すべて書き込みに失敗します。  | 書き込みプロセス中にSparkタスクが失敗して終了した場合、データの一部が正常に書き込まれている可能性があります。                                                                                                 |
| 隔離     | 書き込みプロセス中、書き込まれるデータは他のトランザクションからは見えません。 | 書き込みプロセス中に、正常に書き込まれたデータの一部が他のトランザクションに表示されます。                                                                                                             |
| エラー回復  | バッチ書き込みが失敗した場合は、Sparkを再実行するだけで済みます。     | べき等を達成するには、アプリケーションが必要です。たとえば、バッチ書き込みが失敗した場合は、正常に書き込まれたデータの一部をクリーンアップして、Sparkを再実行する必要があります。タスクの再試行によるデータの重複を防ぐには、 `spark.task.maxFailures=1`を設定する必要があります。 |
| スピード   | データはTiKVに直接書き込まれます。TiKVはより高速です。         | データはTiDBを介してTiKVに書き込まれ、速度に影響します。                                                                                                                          |

次の例は、scalaAPIを介してTiSparkを使用してデータをバッチ書き込みする方法を示しています。

```scala
// select data to write
val df = spark.sql("select * from tpch.ORDERS")

// write data to tidb
df.write.
  format("tidb").
  option("tidb.addr", "127.0.0.1").
  option("tidb.port", "4000").
  option("tidb.user", "root").
  option("tidb.password", "").
  option("database", "tpch").
  option("table", "target_orders").
  mode("append").
  save()
```

書き込むデータ量が多く、書き込み時間が10分を超える場合は、GC時間が書き込み時間より長くなるようにする必要があります。

```sql
UPDATE mysql.tidb SET VARIABLE_VALUE="6h" WHERE VARIABLE_NAME="tikv_gc_life_time";
```

詳細は[このドキュメント](https://github.com/pingcap/tispark/blob/master/docs/datasource_api_userguide.md)を参照してください。

## JDBCを使用してSparkデータフレームをTiDBにロードする {#load-spark-dataframe-into-tidb-using-jdbc}

TiSparkを使用してDataFrameをTiDBクラスタにバッチ書き込みすることに加えて、データ書き込みにSparkのネイティブJDBCサポートを使用することもできます。

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// You might repartition the source to make it balance across nodes
// and increase the concurrency.
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // Replace the host and port with that of your own and be sure to use the rewrite batch
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// As tested, 150 is good practice
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // database name and table name here
.option("isolationLevel", "NONE") // recommended to set isolationLevel to NONE if you have a large DF to load.
.option("user", "root") // TiDB user here
.save()
```

TiDB OOMにつながる可能性のある大規模な単一トランザクションを回避するために、 `isolationLevel`から`NONE`に設定することをお勧めします。

> **ノート：**
>
> JDBCを使用する場合、デフォルト値の`isolationLevel`は`READ_UNCOMMITTED`です。これにより、サポートされていない分離レベルのトランザクションのエラーが発生します。 `isolationLevel`の値を設定することをお勧めし`NONE` 。

## 統計情報 {#statistics-information}

TiSparkは、次の項目にTiDB統計情報を使用します。

1.  推定最小コストでクエリプランのどのインデックスを使用するかを決定します。
2.  効率的な放送参加を可能にする小さなテーブル放送。

TiSparkで統計情報を使用する場合は、最初に、関連するテーブルがすでに分析されていることを確認する必要があります。 [テーブルを分析する方法](/statistics.md)についてもっと読む。

TiSpark 2.0以降、統計情報はデフォルトで自動ロードされます。

## 安全 {#security}

TiSpark v2.5.0以降のバージョンを使用している場合は、TiDBを使用してTiSparkユーザーを認証および承認できます。

認証および承認機能はデフォルトで無効になっています。これを有効にするには、次の構成をSpark構成ファイル`spark-defaults.conf`に追加します。

```
// Enable authentication and authorization
spark.sql.auth.enable true

// Configure TiDB information
spark.sql.tidb.addr $your_tidb_server_address
spark.sql.tidb.port $your_tidb_server_port
spark.sql.tidb.user $your_tidb_server_user
spark.sql.tidb.password $your_tidb_server_password
```

詳細については、 [TiDBサーバーを介した承認と認証](https://github.com/pingcap/tispark/blob/master/docs/authorization_userguide.md)を参照してください。

> **ノート：**
>
> 認証および承認機能を有効にすると、TiSpark Spark SQLはデータソースとしてTiDBのみを使用できるため、他のデータソース（Hiveなど）に切り替えると、テーブルが非表示になります。

## TiSpark FAQ {#tispark-faq}

Q：既存のSpark / Hadoopクラスタとの共有リソースとは対照的に、独立したデプロイメントの長所/短所は何ですか？

A：個別のデプロイなしで既存のSparkクラスタを使用できますが、既存のクラスタがビジーの場合、TiSparkは目的の速度を達成できません。

Q：SparkをTiKVと混合できますか？

A：TiDBとTiKVが過負荷になり、重要なオンラインタスクを実行する場合は、TiSparkを個別に展開することを検討してください。また、OLTPのネットワークリソースが危険にさらされてオンラインビジネスに影響を与えないように、さまざまなNICの使用を検討する必要があります。オンラインビジネスの要件が高くない場合、または負荷が十分に大きくない場合は、TiSparkとTiKVの展開を混在させることを検討できます。

Q：TiSparkを使用してSQLステートメントを実行するときに`warning: WARN ObjectStore:568 - Failed to get database`が返された場合はどうすればよいですか？

A：この警告は無視してかまいません。これは、Sparkがカタログに存在しない2つのデータベース（ `default`と`global_temp` ）を読み込もうとしたために発生します。この警告をミュートする場合は、 `tispark/conf`の`log4j`ファイルに`log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR`を追加して[log4j](https://github.com/pingcap/tidb-docker-compose/blob/master/tispark/conf/log4j.properties#L43)を変更します。 Sparkの下の`config`の`log4j`ファイルにパラメーターを追加できます。サフィックスが`template`の場合、 `mv`コマンドを使用して`properties`に変更できます。

Q：TiSparkを使用してSQLステートメントを実行するときに`java.sql.BatchUpdateException: Data Truncated`が返された場合はどうすればよいですか？

A：このエラーは、書き込まれたデータの長さがデータベースで定義されたデータ型の長さを超えているために発生します。フィールドの長さを確認し、それに応じて調整できます。

Q：TiSparkはデフォルトでHiveメタデータを読み取りますか？

A：デフォルトでは、TiSparkはhiveサイトのHiveメタデータを読み取ることによってHiveデータベースを検索します。検索タスクが失敗した場合は、代わりにTiDBメタデータを読み取ってTiDBデータベースを検索します。

このデフォルトの動作が必要ない場合は、hive-siteでHiveメタデータを構成しないでください。

Q：TiSparkがSparkタスクを実行しているときに`Error: java.io.InvalidClassException: com.pingcap.tikv.region.TiRegion; local class incompatible: stream classdesc serialVersionUID ...`が返された場合、どうすればよいですか？

A：エラーメッセージは`serialVersionUID`の競合を示しています。これは、 `class`つと`TiRegion`の異なるバージョンを使用したために発生します。 `TiRegion`はTiSparkにのみ存在するため、TiSparkパッケージの複数のバージョンが使用される可能性があります。このエラーを修正するには、TiSpark依存関係のバージョンがクラスタのすべてのノード間で一貫していることを確認する必要があります。
