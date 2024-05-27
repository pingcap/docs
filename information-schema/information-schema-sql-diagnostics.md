---
title: SQL Diagnostics
summary: TiDB での SQL 診断を理解します。
---

# SQL 診断 {#sql-diagnostics}

SQL 診断は、TiDB v4.0 で導入された機能です。この機能を使用すると、TiDB の問題をより効率的に特定できます。TiDB v4.0 より前では、さまざまな情報を取得するためにさまざまなツールを使用する必要がありました。

SQL 診断システムには次の利点があります。

-   システム全体のすべてのコンポーネントからの情報を統合します。
-   システム テーブルを通じて上位レイヤーへの一貫したインターフェイスを提供します。
-   監視の概要と自動診断を提供します。
-   クラスター情報のクエリが簡単になります。

## 概要 {#overview}

SQL 診断システムは、次の 3 つの主要部分で構成されています。

-   **クラスタ情報テーブル**: SQL 診断システムでは、各インスタンスの個別の情報を統一された方法で取得できるクラスター情報テーブルが導入されています。このシステムは、クラスター全体のクラスター トポロジ、ハードウェア情報、ソフトウェア情報、カーネル パラメーター、監視、システム情報、スロー クエリ、ステートメント、ログをテーブルに完全に統合します。そのため、SQL ステートメントを使用してこれらの情報を照会できます。

-   **クラスタ監視テーブル**: SQL 診断システムは、クラスター監視テーブルを導入しました。これらのテーブルはすべて`metrics_schema`にあり、SQL ステートメントを使用して監視情報を照会できます。v4.0 以前の視覚化された監視と比較して、この SQL ベースの方法を使用して、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。TiDB クラスターには多くの監視メトリックがあるため、SQL 診断システムは監視サマリーテーブルも提供し、異常な監視項目をより簡単に見つけることができます。

**自動診断**: クラスター情報テーブル、クラスター監視テーブル、およびサマリー テーブルをクエリして問題を特定する SQL ステートメントを手動で実行することもできますが、自動診断を使用すると、一般的な問題をすばやく特定できます。SQL 診断システムは、既存のクラスター情報テーブルと監視テーブルに基づいて自動診断を実行し、関連する診断結果テーブルと診断サマリー テーブルを提供します。

## クラスタ情報テーブル {#cluster-information-tables}

クラスター情報テーブルには、すべてのインスタンスとクラスター内のインスタンスの情報がまとめられています。これらのテーブルを使用すると、1 つの SQL ステートメントのみを使用してすべてのクラスター情報を照会できます。次に、クラスター情報テーブルの一覧を示します。

-   クラスタートポロジテーブル[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)からは、クラスターの現在のトポロジ情報、各インスタンスのバージョン、バージョンに対応する Git ハッシュ、各インスタンスの開始時刻、各インスタンスの実行時間を取得できます。
-   クラスター構成テーブル[`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md)から、クラスター内のすべてのインスタンスの構成を取得できます。4.0 より前のバージョンでは、これらの構成情報を取得するには、各インスタンスの HTTP API に 1 つずつアクセスする必要があります。
-   クラスター ハードウェア テーブル[`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md)では、クラスター ハードウェア情報をすばやく照会できます。
-   クラスター負荷テーブル[`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md)では、クラスターのさまざまなインスタンスとハードウェア タイプの負荷情報を照会できます。
-   カーネル パラメータ テーブル[`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md)では、クラスター内のさまざまなインスタンスのカーネル構成情報を照会できます。現在、TiDB は sysctl 情報の照会をサポートしています。
-   クラスター ログ テーブル[`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md)では、クラスター ログをクエリできます。クエリ条件を各インスタンスにプッシュダウンすることで、クエリがクラスターのパフォーマンスに与える影響は、 `grep`コマンドよりも少なくなります。

TiDB v4.0 より前のシステム テーブルでは、現在のインスタンスのみを表示できます。TiDB v4.0 では、対応するクラスター テーブルが導入され、単一の TiDB インスタンスでクラスター全体のグローバル ビューを取得できます。これらのテーブルは現在`information_schema`にあり、クエリ方法は他の`information_schema`つのシステム テーブルと同じです。

## クラスタ監視テーブル {#cluster-monitoring-tables}

異なる期間のクラスターの状態を動的に観察および比較するために、SQL 診断システムはクラスター監視システム テーブルを導入しています。すべての監視テーブルは`metrics_schema`にあり、SQL ステートメントを使用して監視情報を照会できます。この方法を使用すると、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。

-   [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md) : 現在多くのシステム テーブルが存在するため、 `information_schema.metrics_tables`テーブルでこれらの監視テーブルのメタ情報を照会できます。

TiDB クラスターには多くの監視メトリックがあるため、TiDB は v4.0 で次の監視サマリー テーブルを提供します。

-   監視概要表[`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md)には、すべての監視データがまとめられており、各監視メトリックをより効率的に確認できます。
-   [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) 、すべての監視データも要約します。特に、このテーブルは、各監視メトリックの異なるラベルを使用して統計を集計します。

## 自動診断 {#automatic-diagnostics}

上記のクラスター情報テーブルとクラスター監視テーブルでは、クラスターのトラブルシューティングを行うために SQL 文を手動で実行する必要があります。TiDB v4.0 は自動診断をサポートしています。既存の基本情報テーブルに基づいて診断関連のシステム テーブルを使用することで、診断が自動的に実行されます。自動診断に関連するシステム テーブルは次のとおりです。

-   診断結果テーブル[`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md)には、システムの診断結果が表示されます。診断は受動的にトリガーされます`select * from inspection_result`を実行すると、すべての診断ルールがトリガーされてシステムが診断され、システム内の障害またはリスクが結果に表示されます。
-   診断サマリー テーブル[`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md)には、特定のリンクまたはモジュールの監視情報が要約されています。モジュールまたはリンク全体のコンテキストに基づいて、トラブルシューティングや問題の特定を行うことができます。
