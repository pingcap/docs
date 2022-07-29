---
title: SQL Diagnostics
summary: Understand SQL diagnostics in TiDB.
---

# SQL診断 {#sql-diagnostics}

> **警告：**
>
> SQL診断はまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

SQL診断は、TiDBv4.0で導入された機能です。この機能を使用すると、TiDBの問題をより効率的に見つけることができます。 TiDB v4.0より前は、さまざまなツールを使用してさまざまな情報を取得する必要がありました。

SQL診断システムには次の利点があります。

-   システム全体のすべてのコンポーネントからの情報を統合します。
-   システムテーブルを介して上位層への一貫したインターフェイスを提供します。
-   監視の概要と自動診断を提供します。
-   クラスタ情報の照会が簡単になります。

## 概要 {#overview}

SQL診断システムは、次の3つの主要部分で構成されています。

-   **クラスター情報テーブル**：SQL診断システムは、各インスタンスの個別の情報を取得するための統一された方法を提供するクラスタ情報テーブルを導入します。このシステムは、クラスタトポロジ、ハードウェア情報、ソフトウェア情報、カーネルパラメーター、監視、システム情報、低速クエリ、ステートメント、およびクラスタ全体のログをテーブルに完全に統合します。したがって、SQLステートメントを使用してこれらの情報を照会できます。

-   **クラスター監視テーブル**：SQL診断システムはクラスタ監視テーブルを導入します。これらのテーブルはすべて`metrics_schema`にあり、SQLステートメントを使用して監視情報を照会できます。 v4.0より前の視覚化された監視と比較すると、このSQLベースの方法を使用して、クラスタ全体のすべての監視情報に対して相関クエリを実行し、さまざまな期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。 TiDBクラスタには多くの監視メトリックがあるため、SQL診断システムは監視要約テーブルも提供し、異常な監視項目をより簡単に見つけることができます。

**自動診断**：SQLステートメントを手動で実行して、クラスタ情報テーブル、クラスタ監視テーブル、および要約テーブルを照会して問題を見つけることができますが、自動診断を使用すると、一般的な問題をすばやく見つけることができます。 SQL診断システムは、既存のクラスタ情報テーブルと監視テーブルに基づいて自動診断を実行し、関連する診断結果テーブルと診断要約テーブルを提供します。

## クラスター情報テーブル {#cluster-information-tables}

クラスタ情報テーブルは、クラスタのすべてのインスタンスとインスタンスの情報をまとめたものです。これらのテーブルを使用すると、1つのSQLステートメントのみを使用してすべてのクラスタ情報を照会できます。以下は、クラスタ情報テーブルのリストです。

-   クラスタトポロジテーブル[`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md)から、クラスタの現在のトポロジ情報、各インスタンスのバージョン、バージョンに対応するGitハッシュ、各インスタンスの開始時間、および各インスタンスの実行時間を取得できます。
-   クラスタ構成テーブル[`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md)から、クラスタ内のすべてのインスタンスの構成を取得できます。 4.0より前のバージョンの場合、これらの構成情報を取得するには、各インスタンスのHTTPAPIに1つずつアクセスする必要があります。
-   クラスタハードウェアテーブル[`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md)で、クラスタハードウェア情報をすばやく照会できます。
-   クラスタ負荷テーブル[`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md)で、クラスタのさまざまなインスタンスとハードウェアタイプの負荷情報を照会できます。
-   カーネルパラメータテーブル[`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md)で、クラスタのさまざまなインスタンスのカーネル構成情報をクエリできます。現在、TiDBはsysctl情報のクエリをサポートしています。
-   クラスタログテーブル[`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md)で、クラスタログを照会できます。クエリ条件を各インスタンスにプッシュダウンすることにより、クラスタのパフォーマンスに対するクエリの影響は、 `grep`コマンドの影響よりも少なくなります。

TiDB v4.0より前のシステムテーブルでは、現在のインスタンスのみを表示できます。 TiDB v4.0では、対応するクラスタテーブルが導入されており、単一のTiDBインスタンスでクラスタ全体のグローバルビューを表示できます。これらのテーブルは現在`information_schema`にあり、クエリ方法は他の`information_schema`のシステムテーブルと同じです。

## クラスター監視テーブル {#cluster-monitoring-tables}

さまざまな期間のクラスタ状態を動的に監視および比較するために、SQL診断システムはクラスタ監視システムテーブルを導入しています。すべての監視テーブルは`metrics_schema`にあり、SQLステートメントを使用して監視情報を照会できます。この方法を使用すると、クラスタ全体のすべての監視情報に対して相関クエリを実行し、さまざまな期間の結果を比較して、パフォーマンスのボトルネックをすばやく特定できます。

-   [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md) ：現在多くのシステムテーブルが存在するため、 `information_schema.metrics_tables`のテーブルでこれらの監視テーブルのメタ情報を照会できます。

TiDBクラスタには多くの監視メトリックがあるため、TiDBはv4.0で次の監視要約テーブルを提供します。

-   監視の要約表[`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md)は、すべての監視データを要約して、各監視メトリックをより効率的にチェックできるようにします。
-   [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md)は、すべての監視データも要約します。特に、このテーブルは、各監視メトリックの異なるラベルを使用して統計を集約します。

## 自動診断 {#automatic-diagnostics}

上記のクラスタ情報テーブルとクラスタ監視テーブルで、SQLステートメントを手動で実行してクラスタのトラブルシューティングを行う必要があります。 TiDB v4.0は、自動診断をサポートしています。既存の基本情報テーブルに基づいた診断関連のシステムテーブルを使用して、診断が自動的に実行されるようにすることができます。自動診断に関連するシステムテーブルは次のとおりです。

-   診断結果表[`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md)は、システムの診断結果を示しています。診断は受動的にトリガーされます。 `select * from inspection_result`を実行すると、システムを診断するためのすべての診断ルールがトリガーされ、システムの障害またはリスクが結果に表示されます。
-   診断要約表[`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md)は、特定のリンクまたはモジュールの監視情報を要約したものです。モジュール全体またはリンク全体のコンテキストに基づいて、問題のトラブルシューティングと特定を行うことができます。
