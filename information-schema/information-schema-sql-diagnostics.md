---
title: SQL Diagnostics
summary: Understand SQL diagnostics in TiDB.
---

# SQL 診断 {#sql-diagnostics}

SQL 診断は、TiDB v4.0 で導入された機能です。この機能を使用すると、TiDB の問題をより効率的に見つけることができます。 TiDB v4.0 より前では、さまざまなツールを使用してさまざまな情報を取得する必要があります。

SQL 診断システムには次の利点があります。

-   システムのすべてのコンポーネントからの情報を全体として統合します。
-   これは、システム テーブルを介して上位レイヤーに一貫したインターフェイスを提供します。
-   監視の概要と自動診断を提供します。
-   クラスタ情報を簡単にクエリできます。

## 概要 {#overview}

SQL 診断システムは、次の 3 つの主要部分で構成されています。

-   **クラスタ情報テーブル**: SQL 診断システムには、各インスタンスの個別の情報を取得するための統一された方法を提供するクラスター情報テーブルが導入されています。このシステムは、クラスター トポロジ、ハードウェア情報、ソフトウェア情報、カーネル パラメーター、監視、システム情報、スロー クエリ、ステートメント、およびクラスター全体のログをテーブルに完全に統合します。そのため、SQL ステートメントを使用してこれらの情報を照会できます。

-   **クラスタ監視テーブル**: SQL 診断システムでは、クラスター監視テーブルが導入されています。これらの表はすべて`metrics_schema`にあり、SQL ステートメントを使用してモニター情報を照会できます。 v4.0 より前の視覚化された監視と比較して、この SQL ベースの方法を使用して、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。 TiDB クラスターには多くの監視メトリクスがあるため、SQL 診断システムには監視の概要テーブルも用意されているため、異常な監視項目をより簡単に見つけることができます。

**自動診断**: SQL ステートメントを手動で実行して、クラスター情報テーブル、クラスター監視テーブル、および要約テーブルにクエリを実行して問題を特定することもできますが、自動診断により、一般的な問題をすばやく特定できます。 SQL診断システムは、既存のクラスタ情報テーブルと監視テーブルに基づいて自動診断を実行し、関連する診断結果テーブルと診断要約テーブルを提供します。

## クラスタ情報テーブル {#cluster-information-tables}

クラスター情報テーブルは、すべてのインスタンスとクラスター内のインスタンスの情報をまとめます。これらのテーブルを使用すると、1 つの SQL ステートメントのみを使用してすべてのクラスター情報を照会できます。以下は、クラスター情報テーブルのリストです。

-   クラスタ トポロジ テーブル[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)から、クラスタの現在のトポロジ情報、各インスタンスのバージョン、バージョンに対応する Git ハッシュ、各インスタンスの開始時刻、および各インスタンスの実行時刻を取得できます。
-   クラスター構成テーブル[`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md)から、クラスター内のすべてのインスタンスの構成を取得できます。 4.0 より前のバージョンの場合、これらの構成情報を取得するには、各インスタンスの HTTP API に 1 つずつアクセスする必要があります。
-   クラスター ハードウェア テーブル[`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md)では、クラスター ハードウェア情報をすばやくクエリできます。
-   クラスター負荷テーブル[`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md)では、クラスターのさまざまなインスタンスとハードウェア タイプの負荷情報を照会できます。
-   カーネル パラメーター テーブル[`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md)では、クラスター内のさまざまなインスタンスのカーネル構成情報を照会できます。現在、TiDB は sysctl 情報のクエリをサポートしています。
-   クラスター ログ テーブル[`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md)で、クラスター ログをクエリできます。クエリ条件を各インスタンスにプッシュ ダウンすることにより、クラスター パフォーマンスに対するクエリの影響は、 `grep`コマンドの影響よりも少なくなります。

TiDB v4.0 より前のシステム テーブルでは、現在のインスタンスのみを表示できます。 TiDB v4.0 では、対応するクラスター テーブルが導入され、単一の TiDB インスタンスでクラスター全体のグローバル ビューを持つことができます。これらのテーブルは現在`information_schema`にあり、クエリ方法は他の`information_schema`のシステム テーブルと同じです。

## クラスタ監視テーブル {#cluster-monitoring-tables}

さまざまな期間におけるクラスターの状態を動的に観察して比較するために、SQL 診断システムにはクラスター監視システム テーブルが導入されています。すべての監視テーブルは`metrics_schema`にあり、SQL ステートメントを使用して監視情報をクエリできます。この方法を使用すると、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。

-   [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md) : 多くのシステム テーブルが存在するため、これらの監視テーブルのメタ情報を`information_schema.metrics_tables`テーブルでクエリできます。

TiDB クラスターには多くのモニタリング メトリックがあるため、TiDB は v4.0 で次のモニタリング サマリー テーブルを提供します。

-   モニタリング サマリー テーブル[`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md)は、すべてのモニタリング データを要約して、各モニタリング メトリックをより効率的に確認できるようにします。
-   [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md)は、すべての監視データも要約します。特に、このテーブルは、各モニタリング メトリックの異なるラベルを使用して統計を集計します。

## 自動診断 {#automatic-diagnostics}

上記のクラスター情報テーブルとクラスター監視テーブルでは、SQL ステートメントを手動で実行してクラスターのトラブルシューティングを行う必要があります。 TiDB v4.0 は自動診断をサポートしています。既存の基本情報テーブルを基に、診断関連のシステムテーブルを利用して、診断を自動で実行できます。以下は、自動診断に関連するシステム テーブルです。

-   診断結果テーブル[`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md)は、システムの診断結果を表示します。診断は受動的にトリガーされます。 `select * from inspection_result`を実行すると、すべての診断ルールがトリガーされてシステムが診断され、システムの障害またはリスクが結果に表示されます。
-   診断要約表[`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md)は、特定のリンクまたはモジュールのモニター情報を要約したものです。モジュール全体またはリンクのコンテキストに基づいて、トラブルシューティングを行い、問題を特定できます。
