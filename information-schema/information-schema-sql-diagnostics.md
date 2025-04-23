---
title: SQL Diagnostics
summary: TiDB での SQL 診断を理解します。
---

# SQL診断 {#sql-diagnostics}

SQL診断はTiDB v4.0で導入された機能です。この機能を使用すると、TiDB内の問題をより効率的に特定できます。TiDB v4.0より前のバージョンでは、異なる情報を取得するために異なるツールを使用する必要がありました。

SQL 診断システムには、次の利点があります。

-   システム全体のすべてのコンポーネントからの情報を統合します。
-   システム テーブルを通じて上位レイヤーへの一貫したインターフェイスを提供します。
-   監視の概要と自動診断を提供します。
-   クラスター情報のクエリが簡単になります。

## 概要 {#overview}

SQL 診断システムは、次の 3 つの主要部分で構成されます。

-   **クラスタ情報テーブル**：SQL診断システムは、各インスタンスの個別情報を統一的に取得できるクラスタ情報テーブルを導入します。このシステムは、クラスタトポロジ、ハードウェア情報、ソフトウェア情報、カーネルパラメータ、監視情報、システム情報、スロークエリ、ステートメント、そしてクラスタ全体のログをテーブルに完全に統合します。そのため、これらの情報をSQL文で照会できます。

-   **クラスタ監視テーブル**：SQL診断システムは、クラスター監視テーブルを導入しました。これらのテーブルはすべて`metrics_schema`にまとめられており、SQL文を使用して監視情報を照会できます。v4.0以前の可視化監視と比較して、このSQLベースの方法を使用することで、クラスター全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較することで、パフォーマンスのボトルネックを迅速に特定できます。TiDBクラスターには多くの監視メトリックがあるため、SQL診断システムは監視サマリーテーブルも提供しており、異常な監視項目をより簡単に見つけることができます。

**自動診断**：クラスタ情報テーブル、クラスタ監視テーブル、サマリーテーブルをクエリするSQL文を手動で実行して問題を特定することもできますが、自動診断を利用することで、一般的な問題を迅速に特定できます。SQL診断システムは、既存のクラスタ情報テーブルと監視テーブルに基づいて自動診断を実行し、関連する診断結果テーブルと診断サマリーテーブルを提供します。

## クラスタ情報テーブル {#cluster-information-tables}

クラスタ情報テーブルは、すべてのインスタンスとクラスタ内のインスタンスの情報を集約します。これらのテーブルを使用すると、1つのSQL文だけですべてのクラスタ情報を照会できます。以下はクラスタ情報テーブルの一覧です。

-   クラスタートポロジテーブル[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)からは、クラスターの現在のトポロジ情報、各インスタンスのバージョン、バージョンに対応する Git ハッシュ、各インスタンスの開始時刻、および各インスタンスの実行時間を取得できます。
-   クラスター構成テーブル[`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md)から、クラスター内のすべてのインスタンスの構成を取得できます。4.0より前のバージョンでは、これらの構成情報を取得するには、各インスタンスのHTTP APIに個別にアクセスする必要があります。
-   クラスター ハードウェア テーブル[`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md)では、クラスター ハードウェア情報を簡単に照会できます。
-   クラスター負荷テーブル[`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md)では、クラスターのさまざまなインスタンスとハードウェア タイプの負荷情報を照会できます。
-   カーネルパラメータテーブル[`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md)では、クラスター内の異なるインスタンスのカーネル構成情報を照会できます。現在、TiDBはsysctl情報の照会をサポートしています。
-   クラスターログテーブル[`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md)では、クラスターログをクエリできます。クエリ条件を各インスタンスにプッシュダウンすることで、クエリがクラスターのパフォーマンスに与える影響は、 `grep`コマンドよりも小さくなります。

TiDB v4.0より前のシステムテーブルでは、現在のインスタンスのみを参照できます。TiDB v4.0では、対応するクラスタテーブルが導入され、単一のTiDBインスタンスでクラスタ全体のグローバルビューを取得できます。これらのテーブルは現在`information_schema`にあり、クエリ方法は他の`information_schema`システムテーブルと同じです。

## クラスタ監視テーブル {#cluster-monitoring-tables}

異なる期間におけるクラスタの状態を動的に監視・比較するために、SQL診断システムはクラスタ監視システムテーブルを導入しています。すべての監視テーブルは`metrics_schema`に格納されており、SQL文を用いて監視情報を照会できます。この方法を用いることで、クラスタ全体のすべての監視情報に対して相関クエリを実行し、異なる期間の結果を比較することで、パフォーマンスのボトルネックを迅速に特定できます。

-   [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md) : 現在、多くのシステム テーブルが存在するため、 `information_schema.metrics_tables`テーブルでこれらの監視テーブルのメタ情報を照会できます。

TiDB クラスターには多くの監視メトリックがあるため、TiDB は v4.0 で次の監視サマリー テーブルを提供します。

-   監視概要表[`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md)は、すべての監視データがまとめられており、各監視メトリックをより効率的に確認できます。
-   [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md)はすべての監視データを要約します。特に、この表は各監視メトリックの異なるラベルを使用して統計情報を集計します。

## 自動診断 {#automatic-diagnostics}

上記のクラスタ情報テーブルおよびクラスタ監視テーブルでは、クラスタのトラブルシューティングを行うために手動でSQL文を実行する必要があります。TiDB v4.0は自動診断をサポートしています。既存の基本情報テーブルをベースにした診断関連のシステムテーブルを使用することで、診断を自動実行できます。自動診断に関連するシステムテーブルは以下のとおりです。

-   診断結果テーブル[`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md)には、システムの診断結果が表示されます。診断は受動的にトリガーされます。3 `select * from inspection_result`実行すると、すべての診断ルールがトリガーされ、システムが診断され、システム内の障害またはリスクが結果に表示されます。
-   診断サマリーテーブル[`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md) 、特定のリンクまたはモジュールの監視情報を要約したものです。モジュールまたはリンク全体のコンテキストに基づいて、トラブルシューティングを行い、問題を特定することができます。
