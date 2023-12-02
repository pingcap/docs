---
title: SQL Diagnostics
summary: Understand SQL diagnostics in TiDB.
---

# SQL診断 {#sql-diagnostics}

SQL 診断は、TiDB v4.0 で導入された機能です。この機能を使用すると、TiDB 内の問題をより効率的に特定できます。 TiDB v4.0 より前は、さまざまな情報を取得するにはさまざまなツールを使用する必要がありました。

SQL 診断システムには次の利点があります。

-   システムのすべてのコンポーネントからの情報を全体として統合します。
-   システム テーブルを通じて上位レイヤーに一貫したインターフェイスを提供します。
-   監視の概要と自動診断を提供します。
-   クラスター情報のクエリが簡単になることがわかります。

## 概要 {#overview}

SQL 診断システムは、次の 3 つの主要な部分で構成されます。

-   **クラスタ情報テーブル**: SQL 診断システムには、各インスタンスの個別の情報を取得する統一された方法を提供するクラスター情報テーブルが導入されています。このシステムは、クラスタ全体のクラスタ トポロジ、ハードウェア情報、ソフトウェア情報、カーネル パラメータ、モニタリング、システム情報、スロー クエリ、ステートメント、ログをテーブルに完全に統合します。したがって、SQL ステートメントを使用してこれらの情報をクエリできます。

-   **クラスタ監視テーブル**: SQL 診断システムにはクラスター監視テーブルが導入されています。これらのテーブルはすべて`metrics_schema`にあり、SQL ステートメントを使用して監視情報をクエリできます。 v4.0 より前の視覚化された監視と比較して、この SQL ベースの方法を使用すると、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較してパフォーマンスのボトルネックを迅速に特定できます。 TiDB クラスターには多くの監視メトリックがあるため、SQL 診断システムには監視概要テーブルも用意されているため、異常な監視項目をより簡単に見つけることができます。

**自動診断**: SQL ステートメントを手動で実行して、クラスター情報テーブル、クラスター監視テーブル、およびサマリー テーブルをクエリして問題を特定することもできますが、自動診断を使用すると、一般的な問題を迅速に見つけることができます。 SQL 診断システムは、既存のクラスター情報テーブルと監視テーブルに基づいて自動診断を実行し、関連する診断結果テーブルと診断概要テーブルを提供します。

## クラスタ情報テーブル {#cluster-information-tables}

クラスター情報テーブルには、すべてのインスタンスとクラスター内のインスタンスの情報がまとめられます。これらのテーブルを使用すると、1 つの SQL ステートメントだけを使用してすべてのクラスター情報をクエリできます。以下はクラスター情報テーブルのリストです。

-   クラスタ トポロジ テーブル[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)から、クラスタの現在のトポロジ情報、各インスタンスのバージョン、バージョンに対応する Git ハッシュ、各インスタンスの開始時刻、各インスタンスの実行時間を取得できます。
-   クラスター構成テーブル[`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md)から、クラスター内のすべてのインスタンスの構成を取得できます。 4.0 より前のバージョンの場合、これらの構成情報を取得するには、各インスタンスの HTTP API に 1 つずつアクセスする必要があります。
-   クラスター ハードウェア テーブル[`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md)では、クラスター ハードウェア情報を簡単にクエリできます。
-   クラスター負荷テーブル[`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md)では、クラスターのさまざまなインスタンスおよびハードウェア タイプの負荷情報をクエリできます。
-   カーネル パラメータ テーブル[`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md)では、クラスタ内のさまざまなインスタンスのカーネル構成情報をクエリできます。現在、TiDB は sysctl 情報のクエリをサポートしています。
-   クラスター ログ テーブル[`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md)では、クラスター ログをクエリできます。クエリ条件を各インスタンスにプッシュダウンすることにより、クラスターのパフォーマンスに対するクエリの影響は、 `grep`のコマンドよりも少なくなります。

TiDB v4.0 より前のシステム テーブルでは、現在のインスタンスのみを表示できます。 TiDB v4.0 では、対応するクラスター テーブルが導入されており、単一の TiDB インスタンス上でクラスター全体のグローバル ビューを得ることができます。これらのテーブルは現在`information_schema`にあり、クエリ方法は他の`information_schema`のシステム テーブルと同じです。

## クラスタ監視テーブル {#cluster-monitoring-tables}

さまざまな期間でクラスターの状態を動的に観察および比較するために、SQL 診断システムにはクラスター監視システム テーブルが導入されています。すべての監視テーブルは`metrics_schema`にあり、SQL ステートメントを使用して監視情報をクエリできます。この方法を使用すると、クラスター全体のすべての監視情報に対して相関クエリを実行し、さまざまな期間の結果を比較して、パフォーマンスのボトルネックを迅速に特定できます。

-   [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md) : 現在、多くのシステム テーブルが存在するため、これらの監視テーブルのメタ情報を`information_schema.metrics_tables`テーブルでクエリできます。

TiDB クラスターには多くの監視メトリックがあるため、TiDB は v4.0 で次の監視概要テーブルを提供します。

-   監視概要表[`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md)は、各監視メトリックをより効率的に確認できるように、すべての監視データを要約しています。
-   [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md)はすべての監視データも要約します。特に、このテーブルは、各監視メトリックの異なるラベルを使用して統計を集計します。

## 自動診断 {#automatic-diagnostics}

上記のクラスター情報テーブルとクラスター監視テーブルでは、クラスターのトラブルシューティングを行うために SQL ステートメントを手動で実行する必要があります。 TiDB v4.0 は自動診断をサポートしています。既存の基本情報テーブルに基づいて診断関連のシステム テーブルを使用すると、診断が自動的に実行されます。以下は、自動診断に関連するシステム テーブルです。

-   診断結果表[`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md)には、システムの診断結果が表示されます。診断は受動的にトリガーされます。 `select * from inspection_result`を実行すると、すべての診断ルールがトリガーされてシステムを診断し、システムの障害またはリスクが結果に表示されます。
-   診断概要テーブル[`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md)には、特定のリンクまたはモジュールの監視情報がまとめられています。モジュール全体またはリンクのコンテキストに基づいてトラブルシューティングを行い、問題を特定できます。
